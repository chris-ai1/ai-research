import sys; sys.path.insert(0,'/tmp/pydeps'); sys.path.insert(0,'/tmp/andreev_gap/linear_trick')
import numpy as np, math
from scipy.optimize import linprog
from g2d_sat import dich
def rwl1(R,T,D=2,iters=25,seed=0,f=lambda y,t:y*(-1)**t,dirs=None):
    pts=[(y,t) for y in range(R+1) for t in range(T+1)]
    H=dich(pts,D); keys=list(H)
    if dirs is not None: keys=[k for k in keys if H[k][:2] in dirs]
    A=np.array(keys,float).T; P,G=A.shape
    A=np.hstack([A,np.ones((P,1)),np.array(pts,float)])  # affine
    b=np.array([f(*p) for p in pts],float)
    rng=np.random.default_rng(seed); w=1+0.1*rng.random(G); best=None
    for it in range(iters):
        # min sum w|c| s.t. A c = b ; split c=cp-cn
        nG=A.shape[1]
        cost=np.r_[w,w,np.zeros(3)]
        Aeq=np.hstack([A[:,:G],-A[:,:G],A[:,G:]])
        res=linprog(cost,A_eq=Aeq,b_eq=b,bounds=[(0,None)]*(2*G)+[(None,None)]*3,method='highs')
        c=res.x[:G]-res.x[G:2*G]
        sup=np.abs(c)>1e-7
        # verify exact with support only
        cnt=sup.sum()
        if best is None or cnt<best[0]: best=(cnt,[(H[keys[j]],round(c[j],4)) for j in range(G) if sup[j]])
        w=1/(np.abs(c)+1e-3)*(1+0.05*rng.random(G))
    return best
if __name__=="__main__":
    D=int(sys.argv[1])
    for R,T in [(3,3),(4,4),(2,6),(6,2),(5,5),(6,6),(8,8),(4,8),(8,4),(10,10),(12,12)]:
        bs=min((rwl1(R,T,D,seed=s) for s in range(4)),key=lambda x:x[0])
        print(f"R={R} T={T} ub={bs[0]} R+T={R+T} 2R+T={2*R+T} 2R+2T={2*R+2*T} dirs={sorted(set(u[0][:2] for u in bs[1]))}",flush=True)
