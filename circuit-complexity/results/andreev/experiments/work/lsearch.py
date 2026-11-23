import sys; sys.path.insert(0,'/tmp/pydeps'); sys.path.insert(0,'/tmp/andreev_gap/work')
import numpy as np, itertools, json, time
from dich import all_dichotomies
from constr import parallel_construction
from view import exact_weights
def setup(R,T,f=None):
    if f is None: f=lambda y,t:y*(-1)**t
    pts=[(y,t) for y in range(R+1) for t in range(T+1)]
    H=all_dichotomies(pts); keys=list(H)
    K=np.array(keys,float)            # G x P
    fv=np.array([f(*p) for p in pts],float)
    return pts,keys,K,fv
def feasible(K,idx,fv):
    A=np.c_[K[idx].T,np.ones(K.shape[1])]
    w=np.linalg.lstsq(A,fv,rcond=None)[0]; return np.abs(A@w-fv).max()<1e-8
def canon(v):
    v=tuple(int(x) for x in v); return v if v[0]==0 else tuple(1-x for x in v)
def try_reduce(K,S,fv,remove=2,rng=None):
    """find S' of size |S|-1: remove `remove` elements, add remove-1 (only remove=2 => add 1)"""
    S=list(S); n=len(S)
    pairs=list(itertools.combinations(range(n),2)); rng.shuffle(pairs)
    for i,j in pairs:
        base=[S[k] for k in range(n) if k not in (i,j)]
        A=np.c_[K[base].T,np.ones(K.shape[1])]
        Q,_=np.linalg.qr(A)
        r=fv-Q@(Q.T@fv)
        if np.linalg.norm(r)<1e-9: return base
        Kp=K.T-Q@(Q.T@K.T)       # P x G
        num=(r@Kp)**2; den=(Kp**2).sum(0)*(r@r)
        ok=np.nonzero((den>1e-9)&(np.abs(num-den)<1e-7*np.maximum(1,den)))[0]
        if len(ok): return base+[int(ok[0])]
    return None
def random_swap(K,S,fv,rng,tries=200):
    S=list(S); n=len(S)
    for _ in range(tries):
        i=rng.integers(n); base=S[:i]+S[i+1:]
        A=np.c_[K[base].T,np.ones(K.shape[1])]
        Q,_=np.linalg.qr(A); r=fv-Q@(Q.T@fv)
        Kp=K.T-Q@(Q.T@K.T); num=(r@Kp)**2; den=(Kp**2).sum(0)*(r@r)
        ok=np.nonzero((den>1e-9)&(np.abs(num-den)<1e-7*np.maximum(1,den)))[0]
        ok=[k for k in ok if k!=S[i] and k not in base]
        if ok: return base+[int(rng.choice(ok))]
    return S
def search(R,T,seconds=300,seed=0,start=None):
    pts,keys,K,fv=setup(R,T); kidx={k:i for i,k in enumerate(keys)}; kidx.update({tuple(1-x for x in k):i for i,k in enumerate(keys)})
    rng=np.random.default_rng(seed)
    if start is None:
        gates,_=parallel_construction(R,T)
        start=[]
        for (a,b),th,w in gates:
            v=tuple(int(a*y+b*t>=th) for y,t in pts); start.append(kidx[v])
    S=list(dict.fromkeys(start)); assert feasible(K,S,fv)
    best=list(S); t0=time.time()
    while time.time()-t0<seconds:
        S2=try_reduce(K,S,fv,rng=rng)
        if S2 is not None:
            S=S2
            if len(S)<len(best): best=list(S); print(f"  R={R} T={T} size {len(best)} at {time.time()-t0:.0f}s",flush=True)
        else:
            for _ in range(rng.integers(1,6)): S=random_swap(K,S,fv,rng)
    w=exact_weights(pts,[keys[i] for i in best],list(fv))
    return best,[keys[i] for i in best],w
if __name__=="__main__":
    secs=float(sys.argv[1])
    for a in sys.argv[2:]:
        R,T=map(int,a.split(','))
        best,bk,w=search(R,T,secs)
        print(json.dumps(dict(R=R,T=T,best=len(best),par=2*R+2*T-2,conj=2*R+2*T-4)),flush=True)
        json.dump(dict(R=R,T=T,keys=[list(k) for k in bk],weights=[str(x) for x in w]),open(f'ls_{R}_{T}.json','w'))
