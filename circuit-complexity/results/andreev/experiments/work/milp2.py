import sys; sys.path.insert(0,'/tmp/pydeps'); sys.path.insert(0,'/tmp/andreev_gap/work')
import numpy as np, time, json, itertools
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import csr_matrix, lil_matrix, vstack, hstack, identity
from dich import all_dichotomies
from view import exact_weights
def build_lams(R,T):
    pts=[(y,t) for y in range(R+1) for t in range(T+1)]; idx={p:i for i,p in enumerate(pts)}; P=len(pts)
    L=[]
    for a,b in itertools.combinations(pts,2):
        v=np.zeros(P); v[idx[a]]=1; v[idx[b]]=-1; L.append(v)
    for y in range(R):
        for t in range(T):
            v=np.zeros(P); v[idx[(y,t)]]=1; v[idx[(y+1,t+1)]]=1; v[idx[(y+1,t)]]=-1; v[idx[(y,t+1)]]=-1; L.append(v)
    return np.array(L)
def solve(R,T,f=None,tl=600,B=None,restrict=None,cuts=True,label=''):
    if f is None: f=lambda y,t:y*(-1)**t
    pts=[(y,t) for y in range(R+1) for t in range(T+1)]; P=len(pts)
    H=all_dichotomies(pts); keys=list(H)
    if restrict=='row0':
        r0=[i for i,(y,t) in enumerate(pts) if y==0]
        keys=[k for k in keys if len(set(k[i] for i in r0))==1]
    G=len(keys)
    if B is None: B=4*P+8
    K=np.array(keys,float).T
    fv=np.array([f(*p) for p in pts],float)
    nv=2*G+1
    rowsA=[]; lb=[]; ub=[]
    A1=np.zeros((P,nv)); A1[:,:G]=K; A1[:,-1]=1; rowsA.append(csr_matrix(A1)); lb+=list(fv); ub+=list(fv)
    # big-M
    I=identity(G,format='csr'); Z=csr_matrix((G,1))
    rowsA.append(hstack([I,-B*I,Z])); lb+=[-np.inf]*G; ub+=[0]*G
    rowsA.append(hstack([I,B*I,Z])); lb+=[0]*G; ub+=[np.inf]*G
    if cuts:
        L=build_lams(R,T); S=(np.abs(L@K)>1e-9).astype(float); lf=L@fv
        cov=np.unique(S[np.abs(lf)>1e-9],axis=0)
        rowsA.append(hstack([csr_matrix((len(cov),G)),csr_matrix(cov),csr_matrix((len(cov),1))])); lb+=[1]*len(cov); ub+=[np.inf]*len(cov)
        zr=[]
        for r in np.unique(S[np.abs(lf)<=1e-9],axis=0):
            sup=np.nonzero(r)[0]
            if len(sup)==0: continue
            for j in sup:
                row=np.zeros(G); row[sup]=1; row[j]=-1; zr.append(row)
        if zr:
            zr=np.unique(np.array(zr),axis=0)
            rowsA.append(hstack([csr_matrix((len(zr),G)),csr_matrix(zr),csr_matrix((len(zr),1))])); lb+=[0]*len(zr); ub+=[np.inf]*len(zr)
    A=vstack(rowsA,format='csr')
    c=np.zeros(nv); c[G:2*G]=1
    integ=np.zeros(nv); integ[G:2*G]=1
    t0=time.time()
    res=milp(c,constraints=LinearConstraint(A,lb,ub),integrality=integ,bounds=Bounds(np.r_[[-B]*G,[0]*G,-1e6],np.r_[[B]*G,[1]*G,1e6]),options={'time_limit':tl})
    out=dict(R=R,T=T,restrict=restrict,status=int(res.status),G=G,time=round(time.time()-t0,1),dual=getattr(res,'mip_dual_bound',None))
    if res.x is not None:
        used=[keys[j] for j in range(G) if res.x[G+j]>0.5]
        w=exact_weights(pts,used,list(fv))
        assert w is not None
        out['best']=len(used); out['keys']=[list(k) for k in used]; out['weights']=[str(x) for x in w]
    return out
if __name__=="__main__":
    tl=float(sys.argv[1]); restrict=None if sys.argv[2]=='all' else sys.argv[2]
    for a in sys.argv[3:]:
        R,T=map(int,a.split(','))
        o=solve(R,T,tl=tl,restrict=restrict)
        print(json.dumps({k:v for k,v in o.items() if k not in('keys','weights')}),flush=True)
        json.dump(o,open(f'/tmp/andreev_gap/work/m2_{sys.argv[2]}_{R}_{T}.json','w'))
