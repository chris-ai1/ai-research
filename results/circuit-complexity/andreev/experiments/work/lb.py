import sys; sys.path.insert(0,'/tmp/pydeps'); sys.path.insert(0,'/tmp/andreev_gap/work')
import numpy as np, itertools, time, json
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import lil_matrix, csr_matrix, vstack
from dich import all_dichotomies
def lambdas(R,T):
    idx={(y,t):i for i,(y,t) in enumerate((y,t) for y in range(R+1) for t in range(T+1))}
    P=len(idx); L=[]
    def vec(d):
        v=np.zeros(P,np.int8)
        for p,c in d: v[idx[p]]+=c
        return v
    pts=list(idx)
    for a,b in itertools.combinations(pts,2): L.append(vec([(a,1),(b,-1)]))
    # column-pair interval combos
    for t1,t2 in itertools.combinations(range(T+1),2):
        for y1,y2 in itertools.combinations(range(R+1),2):
            for u1,u2 in itertools.combinations(range(R+1),2):
                for s in (1,-1): L.append(vec([((y2,t1),1),((y1,t1),-1),((u2,t2),s),((u1,t2),-s)]))
    for y1,y2 in itertools.combinations(range(R+1),2):
        for a1,a2 in itertools.combinations(range(T+1),2):
            for b1,b2 in itertools.combinations(range(T+1),2):
                for s in (1,-1): L.append(vec([((y1,a2),1),((y1,a1),-1),((y2,b2),s),((y2,b1),-s)]))
    L=np.unique(np.array(L),axis=0)
    L=L[np.abs(L).sum(1)>0]
    return L
def lower_bound(R,T,f=None,tl=600,extra=None):
    if f is None: f=lambda y,t:y*(-1)**t
    pts=[(y,t) for y in range(R+1) for t in range(T+1)]
    H=all_dichotomies(pts); keys=list(H); G=len(keys)
    K=np.array(keys,np.int64).T  # P x G
    fv=np.array([f(*p) for p in pts],float)
    L=lambdas(R,T)
    S=(L.astype(np.int64)@K)!=0  # nL x G
    lf=L@fv
    rows=[];lb=[];ub=[]
    A=lil_matrix((0,G))
    cov=S[np.abs(lf)>1e-9]
    cov=np.unique(cov,axis=0)
    zer=S[np.abs(lf)<=1e-9]; zer=np.unique(zer,axis=0)
    cons=[]
    if len(cov): cons.append(LinearConstraint(csr_matrix(cov.astype(float)),1,np.inf))
    # zero-type: for each j in support: sum_{i in supp, i!=j} z_i - z_j >=0
    data=[]
    for r in zer:
        sup=np.nonzero(r)[0]
        if len(sup)==0: continue
        for j in sup:
            row=np.zeros(G); row[sup]=1; row[j]=-1; data.append(row)
    if data:
        D=np.unique(np.array(data),axis=0)
        cons.append(LinearConstraint(csr_matrix(D),0,np.inf))
    c=np.ones(G)
    t0=time.time()
    res=milp(c,constraints=cons,integrality=np.ones(G),bounds=Bounds(0,1),options={'time_limit':tl})
    return dict(R=R,T=T,lb=(round(res.fun) if res.status==0 else getattr(res,'mip_dual_bound',None)),status=int(res.status),time=time.time()-t0,ncov=len(cov),nzer=len(data))
if __name__=="__main__":
    for a in sys.argv[1:]:
        R,T=map(int,a.split(','))
        print(json.dumps(lower_bound(R,T)),flush=True)
