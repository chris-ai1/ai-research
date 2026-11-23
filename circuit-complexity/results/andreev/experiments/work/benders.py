import sys; sys.path.insert(0,'/tmp/pydeps'); sys.path.insert(0,'/tmp/andreev_gap/work')
import numpy as np, time, json
from scipy.optimize import milp, LinearConstraint, Bounds, linprog
from scipy.sparse import csr_matrix
from dich import all_dichotomies
from lb import lambdas
from view import exact_weights
def in_span(KS,fv):
    A=np.hstack([KS,np.ones((KS.shape[0],1))])
    w=np.linalg.lstsq(A,fv,rcond=None)[0]
    return np.abs(A@w-fv).max()<1e-7
def cut_lambda(KS,fv,K,rng):
    P=KS.shape[0]
    A=np.hstack([KS,np.ones((P,1))])
    # L1-min lambda: lambda^T A=0, lambda.f=1 ; split lambda=lp-lm
    Aeq=np.vstack([np.hstack([A.T,-A.T]),np.r_[fv,-fv][None,:]])
    beq=np.r_[np.zeros(A.shape[1]),1]
    c=np.ones(2*P)+rng.random(2*P)*0.3
    r=linprog(c,A_eq=Aeq,b_eq=beq,bounds=(0,None),method='highs')
    lam=r.x[:P]-r.x[P:]
    return lam
def exact(R,T,f=None,tl_total=3000,init_lambdas=True,verbose=False,cands=None):
    if f is None: f=lambda y,t:y*(-1)**t
    pts=[(y,t) for y in range(R+1) for t in range(T+1)]
    H=all_dichotomies(pts) if cands is None else cands; keys=list(H); G=len(keys)
    K=np.array(keys,float).T
    fv=np.array([f(*p) for p in pts],float)
    covrows=[]; zrows=[]
    if init_lambdas:
        L=lambdas(R,T).astype(float); S=np.abs(L@K)>1e-9; lf=L@fv
        covrows=list(np.unique(S[np.abs(lf)>1e-9],axis=0).astype(float))
        for r in np.unique(S[np.abs(lf)<=1e-9],axis=0):
            sup=np.nonzero(r)[0]
            for j in sup:
                row=np.zeros(G); row[sup]=1; row[j]=-1; zrows.append(row)
    rng=np.random.default_rng(0)
    t0=time.time(); it=0; lbv=0
    while time.time()-t0<tl_total:
        it+=1
        cons=[LinearConstraint(csr_matrix(np.array(covrows)),1,np.inf)]
        if zrows: cons.append(LinearConstraint(csr_matrix(np.array(zrows)),0,np.inf))
        res=milp(np.ones(G),constraints=cons,integrality=np.ones(G),bounds=Bounds(0,1),options={'time_limit':max(10,tl_total-(time.time()-t0))})
        if res.status!=0: return dict(R=R,T=T,status='milp-timeout',lb=lbv,iters=it)
        z=res.x>0.5; lbv=int(round(res.fun))
        KS=K[:,z]
        if in_span(KS,fv):
            sel=[keys[j] for j in np.nonzero(z)[0]]
            w=exact_weights(pts,sel,list(fv))
            return dict(R=R,T=T,status='optimal',h=lbv,iters=it,time=time.time()-t0,keys=[list(k) for k in sel],weights=[str(x) for x in w])
        for rep in range(3):
            lam=cut_lambda(KS,fv,K,rng)
            row=(np.abs(lam@K)>1e-7).astype(float)
            covrows.append(row)
        if verbose and it%20==0: print(it,lbv,len(covrows),round(time.time()-t0),flush=True)
    return dict(R=R,T=T,status='timeout',lb=lbv,iters=it)
if __name__=="__main__":
    tl=float(sys.argv[1])
    for a in sys.argv[2:]:
        R,T=map(int,a.split(','))
        r=exact(R,T,tl_total=tl,verbose=True)
        print(json.dumps({k:v for k,v in r.items() if k not in('keys','weights')}),flush=True)
        if r['status']=='optimal': json.dump(r,open(f'/tmp/andreev_gap/work/exact_{R}_{T}.json','w'))
