"""Finite-m pool experiments (approach 1): minimum #gates within structured pools, k=2 (or 3).
pool 'axis' : block-symmetric, beta in {e_i, sum of pairs, all-ones...} (all 0/1 beta), alpha in {0,1}^N
pool 'bsrich': block-symmetric, beta in {-2..2}^k primitive, alpha in {0,1}^N
pool 'half'  : two halves per block, beta in {-1,0,1}^{2k} (mixed allowed), alpha in {0,1}^N
Heuristic: L1 (unit weights) -> greedy prune (3 random orders) ; then MILP on the union of supports
plus all gates in the directions used (all thresholds)."""
import sys; sys.path.insert(0,'/tmp/andreev_gap/mixed_upper')
from lpcore import *
import argparse
ap=argparse.ArgumentParser(); ap.add_argument('--k',type=int,default=2); ap.add_argument('--m',type=int,default=3)
ap.add_argument('--pool',default='axis'); ap.add_argument('--milp',type=int,default=300); ap.add_argument('--orders',type=int,default=3)
args=ap.parse_args()
k=args.k; m=args.m; N=1<<k
from math import gcd
def prim(b):
    g=0
    for v in b: g=gcd(g,abs(v))
    f=[v for v in b if v]
    return g==1 and f[0]>0
if args.pool in ('axis','bsrich'):
    dom=Domain(k,[[m]]*k)
    if args.pool=='axis': B=[b for b in itertools.product((0,1),repeat=k) if any(b)]
    else: B=[b for b in itertools.product(range(-2,3),repeat=k) if any(b) and prim(b)]
else:
    dom=Domain(k,[[(m+1)//2,m//2]]*k)
    B=[b for b in itertools.product((-1,0,1),repeat=2*k) if any(b) and prim(b)]
A=list(itertools.product((0,1),repeat=N))
pool=Pool(dom)
for b in B:
    for a in A: pool.add_direction(a,b)
t0=time.time()
print(f'k={k} m={m} pool={args.pool} points={dom.P} gates={len(pool)}',flush=True)
st,v,mu,nu,t0_,active=solve_lp(dom,pool,range(len(pool)),weights=np.ones(len(pool)))
if st!='ok': print('LP',st); sys.exit()
supp=[j for j in range(len(pool)) if abs(v[j])>1e-7]
best=None; rng=np.random.default_rng(0); union=set(supp)
for o in range(args.orders):
    order=list(rng.permutation(len(supp))) if o else None
    s2,active=prune(dom,pool,supp,active=active,order=order)
    union|=set(s2)
    if best is None or len(s2)<len(best): best=s2
print(f'  L1 support {len(supp)}  pruned best {len(best)}  ({time.time()-t0:.0f}s)',flush=True)
ok,cert,ms=exact_certificate(dom,pool,best,active=active)
print('  exact certificate',ok)
for j in best: print('    gate alpha=%s beta=%s theta=%d'%(pool.alpha[j].tolist(),pool.beta[j].tolist(),pool.theta[j]))
res_milp=None
if args.milp:
    # MILP on the gates sharing a direction with the pruned support (all thresholds)
    dirs={(pool.alpha[j].tobytes(),pool.beta[j].tobytes()) for j in union}
    cand=[j for j in range(len(pool)) if (pool.alpha[j].tobytes(),pool.beta[j].tobytes()) in dirs]
    stt,sup2,active,db=solve_milp(dom,pool,cand,active,time_limit=args.milp)
    if sup2 is not None:
        res_milp=len(sup2)
        print(f'  MILP over {len(cand)} gates ({len(dirs)} directions): {len(sup2)}  status {stt} dual bound {db}',flush=True)
        ok2,cert2,ms2=exact_certificate(dom,pool,sup2,active=active)
        print('  MILP circuit exact certificate',ok2,'min slack (scaled)',ms2,flush=True)
        if ok2:
            vi,mui,nui,t0i,sc=cert2
            for jj,j in enumerate(sup2): print('    MILPgate alpha=%s beta=%s theta=%d topw=%s/%d'%(pool.alpha[j].tolist(),pool.beta[j].tolist(),pool.theta[j],vi[jj],sc))
            print('    top linear: mu=%s nu=%s t0=%s (all /%d)'%(mui.tolist(),nui.tolist(),t0i,sc))
print(f'RESULT k={k} m={m} pool={args.pool} heuristic={len(best)} milp={res_milp} time={time.time()-t0:.0f}s',flush=True)
