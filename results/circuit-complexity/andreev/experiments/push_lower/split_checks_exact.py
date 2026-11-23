"""Exact-integer re-run of the splitting-lemma checks (the float version can mis-count when a threshold equals
a vertex value).  Gate [beta.s >= T] splits the unit cube c+{0,1}^k iff lo(c) < T <= hi(c).
Integer normals and integer weights; all integer thresholds are tried (that covers every dichotomy)."""
import sys, itertools, math
sys.path.insert(0,'/tmp/pydeps')
import numpy as np
rng=np.random.default_rng(11)

def max_split(lo,hi):
    # max over integer T of #{c: lo<T<=hi}: sweep events (+1 at lo+1, -1 at hi+1)
    ev={}
    for a in lo: ev[a+1]=ev.get(a+1,0)+1
    for b in hi: ev[b+1]=ev.get(b+1,0)-1
    cur=best=0
    for t in sorted(ev):
        cur+=ev[t]; best=max(best,cur)
    return best

def bs(k,m,trials):
    cubes=np.array(list(itertools.product(range(m),repeat=k)),dtype=np.int64)
    worst=0; wb=None
    normals=[np.ones(k,dtype=np.int64)]+[rng.integers(-1000,1001,k) for _ in range(trials)]+[rng.integers(-3,4,k) for _ in range(trials)]
    for b in normals:
        if not b.any(): continue
        base=cubes@b; lo=base+np.minimum(b,0).sum(); hi=base+np.maximum(b,0).sum()
        c=max_split(lo.tolist(),hi.tolist())
        if c>worst: worst,wb=c,b
    return worst,wb

def coherent(k,m,trials):
    cubes=np.array(list(itertools.product(range(m),repeat=k)),dtype=np.int64)
    worst=0
    for _ in range(trials):
        sg=rng.choice([-1,1],k); kind=rng.integers(0,3)
        if kind==0: W=rng.integers(0,1000,(k,m))
        elif kind==1: W=rng.integers(0,4,(k,m))**4
        else: W=(rng.random((k,m))<0.3)*rng.integers(1,50,(k,m))
        W=W*sg[:,None]
        P=np.zeros((k,m+1),dtype=np.int64)
        for i in range(k): P[i,1:]=np.cumsum(W[i,rng.permutation(m)])
        lo=np.zeros(len(cubes),dtype=np.int64); hi=np.zeros(len(cubes),dtype=np.int64)
        for i in range(k):
            a=P[i,cubes[:,i]]; b=P[i,cubes[:,i]+1]; lo+=np.minimum(a,b); hi+=np.maximum(a,b)
        worst=max(worst,max_split(lo.tolist(),hi.tolist()))
    return worst

for k,m in [(2,6),(2,9),(3,5),(3,8),(4,4),(5,3),(6,3)]:
    w,b=bs(k,m,300)
    print(f'[blocksym exact] k={k} m={m}: max split = {w}  (2D: 2m-1={2*m-1})  bound min(k,2sqrt(2k))m^(k-1)={min(k,2*math.sqrt(2*k))*m**(k-1):.0f}  worst normal {b}',flush=True)
for k,m in [(2,6),(3,5),(3,8),(4,4),(5,3)]:
    w=coherent(k,m,300)
    print(f'[coherent exact] k={k} m={m}: max split = {w}  <= m^k-(m-1)^k = {m**k-(m-1)**k}  ok={w<=m**k-(m-1)**k}',flush=True)
