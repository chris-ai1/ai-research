"""k=2 pool experiments: block-symmetric pools vs part-symmetric (mixed) pools."""
import sys; sys.path.insert(0,'/tmp/andreev_gap/mixed_upper')
from lpcore import *
import argparse
ap=argparse.ArgumentParser()
ap.add_argument('m',type=int)
ap.add_argument('--pool',default='bs')
ap.add_argument('--amax',type=int,default=1)
ap.add_argument('--bmax',type=int,default=2)
ap.add_argument('--iters',type=int,default=6)
ap.add_argument('--milp',type=int,default=0)
ap.add_argument('--seed',type=int,default=0)
args=ap.parse_args()
m=args.m
def dirs(nc,bmax,mixed):
    out=set()
    for b in itertools.product(range(-bmax,bmax+1),repeat=nc):
        if all(v==0 for v in b): continue
        # normalise sign: first nonzero positive
        f=[v for v in b if v!=0][0]
        if f<0: continue
        from math import gcd
        g=0
        for v in b: g=gcd(g,abs(v))
        if g!=1: continue
        out.add(b)
    return sorted(out)
t0=time.time()
if args.pool=='bs':
    dom=Domain(2,[[m],[m]])
    B=dirs(2,args.bmax,False)
elif args.pool=='half':
    h1=(m+1)//2; h2=m//2
    dom=Domain(2,[[h1,h2],[h1,h2]])
    B=dirs(4,args.bmax,True)
pool=Pool(dom)
A=list(itertools.product(range(-args.amax,args.amax+1),repeat=4))
for b in B:
    for a in A:
        pool.add_direction(a,b,tag='%s|%s'%(a,b))
print(f'm={m} pool={args.pool} points={dom.P} directions={len(B)}x{len(A)} gates={len(pool)}  ({time.time()-t0:.1f}s)',flush=True)
best,active=reweighted_l1(dom,pool,iters=args.iters,seed=args.seed,verbose=True)
print('rwL1 best support',len(best),flush=True)
sup,active=prune(dom,pool,best,active=active)
print('pruned support',len(sup),flush=True)
ok,cert,ms=exact_certificate(dom,pool,sup,active=active)
print('exact certificate',ok,'minslack',ms)
for j in sup: print('  gate',pool.alpha[j].tolist(),pool.beta[j].tolist(),pool.theta[j])
if args.milp:
    st,sup2,active,db=solve_milp(dom,pool,range(len(pool)),active,time_limit=args.milp,verbose=False)
    print('MILP',st,None if sup2 is None else len(sup2),'dual bound',db)
print(f'RESULT m={m} pool={args.pool} amax={args.amax} bmax={args.bmax} gates={len(sup)} time={time.time()-t0:.0f}s')
