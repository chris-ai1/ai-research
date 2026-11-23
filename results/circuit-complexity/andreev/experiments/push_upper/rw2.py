# Reweighted-L1 (LP) search for sparse halfplane representations of Y(-1)^t + q(Y,t) + a(-1)^t on [0,R]x[0,T]
# then exact re-solve on the support (LP feasibility) and greedy pruning.  Upper bounds only.
import sys; sys.path.insert(0,'/tmp/pydeps')
import itertools, math, numpy as np
from scipy.optimize import linprog
def cands(pts,D):
    out=[];seen=set()
    for a in itertools.product(range(-D,D+1),repeat=pts.shape[1]):
        if all(x==0 for x in a) or math.gcd(*[abs(x) for x in a])!=1: continue
        if [x for x in a if x!=0][0]<0: continue
        L=pts@np.array(a)
        for th in np.unique(L)[1:]:
            col=(L>=th).astype(np.int8); key=col.tobytes()
            if key in seen: continue
            seen.add(key); out.append((a,int(th),col))
    return out
def setup(R,T,extra_basis=()):
    pts=np.array([(y,t) for y in range(R+1) for t in range(T+1)])
    Y=pts[:,0].astype(float); t=pts[:,1].astype(float); sg=(-1.0)**t
    B=np.array([np.ones(len(pts)),Y,t,Y*Y,Y*t,t*t,sg]+[f(Y,t) for f in extra_basis]).T
    return pts,Y*sg,B
def feasible(H,B,target):
    # solve H v - B c = target (any v, c) via least squares, check residual
    A=np.hstack([H,-B]); sol,res,rk,sv=np.linalg.lstsq(A,target,rcond=None)
    return np.max(np.abs(A@sol-target))<1e-7, sol
def prune(H,B,target,supp):
    supp=list(supp); changed=True
    while changed:
        changed=False
        for j in sorted(supp,key=lambda j:np.random.rand()):
            s2=[x for x in supp if x!=j]
            ok,_=feasible(H[:,s2],B,target)
            if ok: supp=s2; changed=True; break
    return supp
def rwl1(R,T,D=3,iters=12,seed=0):
    rng=np.random.default_rng(seed)
    pts,target,B=setup(R,T); C=cands(pts,D); H=np.array([c[2] for c in C]).T.astype(float); J=H.shape[1]; nb=B.shape[1]
    w=np.ones(J)*(1+0.1*rng.random(J)); best=None
    for it in range(iters):
        # vars: vp(J) vm(J) c(nb free)
        cost=np.concatenate([w,w,np.zeros(nb)])
        Aeq=np.hstack([H,-H,-B])
        bounds=[(0,None)]*(2*J)+[(None,None)]*nb
        r=linprog(cost,A_eq=Aeq,b_eq=target,bounds=bounds,method='highs')
        if r.status!=0: break
        v=r.x[:J]-r.x[J:2*J]
        supp=[j for j in range(J) if abs(v[j])>1e-6]
        supp=prune(H,B,target,supp)
        if best is None or len(supp)<len(best): best=supp
        w=1.0/(np.abs(v)+1e-3)*(1+0.05*rng.random(J))
    return best,C
if __name__=='__main__':
    R,T,D=map(int,sys.argv[1:4]); seeds=int(sys.argv[4]) if len(sys.argv)>4 else 3
    bb=None
    for s in range(seeds):
        b,C=rwl1(R,T,D,seed=s)
        if bb is None or len(b)<len(bb): bb=b
    print(f"R={R} T={T} D={D} best={len(bb)} R+T={R+T} R+T/2={R+(T+1)//2}",flush=True)
    print('   ',[ (C[j][0],C[j][1]) for j in bb])
