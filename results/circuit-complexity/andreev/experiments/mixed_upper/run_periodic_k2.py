import sys; sys.path.insert(0,'/tmp/andreev_gap/mixed_upper')
from periodic_lp import *
import argparse
ap=argparse.ArgumentParser()
ap.add_argument('--P',type=int,default=4)
ap.add_argument('--periods',default='2,4')
ap.add_argument('--mode',default='bs')     # bs | half
ap.add_argument('--amax',type=int,default=3)
ap.add_argument('--bset',default='auto')
ap.add_argument('--milp',type=int,default=300)
ap.add_argument('--linearD',type=int,default=0)
args=ap.parse_args()
k=2; N=4
periods=[int(v) for v in args.periods.split(',')]
if args.mode=='bs':
    dom=PDomain(k,1,args.P); hm=1.0; nc=2
else:
    dom=PDomain(k,2,args.P); hm=0.5; nc=4
atoms=Atoms(dom,hm)
t0=time.time()
for p in periods:
    lo=-(p//2)+1 if p>2 else 0; hi=p//2
    breps=[b for b in itertools.product(range(lo,hi+1),repeat=nc) if any(b)]
    arange_=range(0,min(p,args.amax+1))
    for b in breps:
        for a in itertools.product(arange_,repeat=N):
            for r in range(p):
                atoms.add(b,a,p,r)
print(f'mode={args.mode} P={args.P} periods={periods} points={dom.npts} atoms={len(atoms.spec)} ({time.time()-t0:.1f}s)',flush=True)
best=reweighted(dom,atoms,iters=8,verbose=True,linearD=bool(args.linearD))
if best is None:
    print('INFEASIBLE with this atom set'); sys.exit()
sel,c=best
print('reweighted best cost',round(c,4),'atoms',len(sel))
sel=greedy_prune(dom,atoms,sel,linearD=bool(args.linearD))
print('after prune cost',round(sum(atoms.cost[j] for j in sel),4),'atoms',len(sel))
for j in sel: print('   ',atoms.spec[j],'cost',atoms.cost[j])
if args.milp:
    r=min_cost_milp(dom,atoms,time_limit=args.milp,linearD=bool(args.linearD))
    if r:
        ch,f,db,st=r
        print('MILP cost',f,'dual bound',db,'status',st)
        for j in ch: print('   ',atoms.spec[j],'cost',atoms.cost[j])
