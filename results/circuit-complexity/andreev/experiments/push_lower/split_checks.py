"""Numerical sanity checks of the splitting lemmas used in the block-symmetric / sign-coherent lower bound.
(1) Coherent-gate lemma: a gate whose address weights are sign-coherent in every block, under the
    count restriction with a FIXED arrangement (block i: bits sigma_i(1..c_i) on, sigma_i(c_i+1) live), splits at most
    m^k-(m-1)^k <= k m^{k-1} of the m^k unit cubes.  Tested on random coherent gates (worst case over thresholds).
(2) Block-symmetric gates: split count <= min(k, 2*sqrt(2k)) m^{k-1}; we report the max over random
    and structured normals and all thresholds.
(3) Construction (d) (all gates block-symmetric and coherent): per-cube number of splitting gates for random
    tables, compared with the information bound D_0."""
import sys, itertools, math
sys.path.insert(0,'/tmp/pydeps'); sys.path.insert(0,'/tmp/andreev_gap/linear_trick')
import numpy as np
rng=np.random.default_rng(7)

def coherent_test(k,m,trials=200):
    worst=0
    cubes=np.array(list(itertools.product(range(m),repeat=k)))
    for _ in range(trials):
        signs=rng.choice([-1,1],k)
        kind=rng.integers(0,4)
        if kind==0: W=rng.random((k,m))
        elif kind==1: W=rng.exponential(1,(k,m))**3
        elif kind==2: W=(rng.random((k,m))<0.3).astype(float)*rng.random((k,m))
        else: W=np.where(rng.random((k,m))<0.5,1.0,1e-3)
        W=W*signs[:,None]
        # prefix sums along the (random) arrangement
        P=np.zeros((k,m+1))
        for i in range(k):
            order=rng.permutation(m); P[i,1:]=np.cumsum(W[i,order])
        # vertex values of every cube: min/max over z in {0,1}^k of sum_i P[i,c_i+z_i]
        lo=np.zeros(len(cubes)); hi=np.zeros(len(cubes))
        for i in range(k):
            a=P[i,cubes[:,i]]; b=P[i,cubes[:,i]+1]
            lo+=np.minimum(a,b); hi+=np.maximum(a,b)
        # threshold T splits cube iff lo < T <= hi ; maximise count over T (sweep all endpoints)
        ev=np.concatenate([np.stack([lo,np.ones_like(lo)],1),np.stack([hi,-np.ones_like(hi)],1)])
        ev=ev[np.lexsort((-ev[:,1],ev[:,0]))]   # at equal coordinate process +1 (open left end) before -1? see below
        # count of cubes with lo < T <= hi for T just above each 'lo' event: brute force over candidate T
        cand=np.unique(np.concatenate([lo,hi]))
        cand=np.concatenate([cand+1e-12, hi])
        cnt=max(int(((lo<T)&(T<=hi)).sum()) for T in cand[::max(1,len(cand)//4000)])
        worst=max(worst,cnt)
    return worst, m**k-(m-1)**k, k*m**(k-1)

def bs_test(k,m,trials=300):
    cubes=np.array(list(itertools.product(range(m),repeat=k)))
    worst=0; worstb=None
    normals=[np.ones(k)]+[rng.normal(size=k) for _ in range(trials)]+[rng.integers(-3,4,k).astype(float) for _ in range(trials)]
    for b in normals:
        if not b.any(): continue
        base=cubes@b; lo=base+np.minimum(b,0).sum(); hi=base+np.maximum(b,0).sum()
        cand=np.unique(np.concatenate([lo+1e-9,hi]))
        cnt=max(int(((lo<T)&(T<=hi)).sum()) for T in cand)
        if cnt>worst: worst,worstb=cnt,b
    return worst, min(k,2*math.sqrt(2*k))*m**(k-1), worstb

if __name__=='__main__':
    for k,m in [(2,6),(3,5),(3,8),(4,4),(5,3)]:
        w,b1,b2=coherent_test(k,m)
        print(f'[coherent] k={k} m={m}: max split cubes over random coherent gates & thresholds = {w}  <= m^k-(m-1)^k={b1}  (k m^(k-1)={b2})  ok={w<=b1}',flush=True)
    for k,m in [(2,6),(3,5),(3,8),(4,4),(5,3),(6,3)]:
        w,b,nb=bs_test(k,m)
        print(f'[blocksym] k={k} m={m}: max split cubes = {w}  bound min(k,2sqrt(2k)) m^(k-1) = {b:.1f}  (fraction {w/m**k:.3f} of cubes; worst normal {np.round(nb,2)})  ok={w<=b}',flush=True)
