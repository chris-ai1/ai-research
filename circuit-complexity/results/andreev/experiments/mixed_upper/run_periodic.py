"""General driver for the periodic slope LP.  Writes progress unbuffered.
  --k 2|3  --mode bs|half  --P 4  --periods 2,4  --amode full|sparse  --amax a  --asupp s"""
import sys; sys.path.insert(0,'/tmp/andreev_gap/mixed_upper')
from periodic_lp import *
import argparse
ap=argparse.ArgumentParser()
ap.add_argument('--k',type=int,default=2)
ap.add_argument('--P',type=int,default=4)
ap.add_argument('--periods',default='2,4')
ap.add_argument('--mode',default='bs')
ap.add_argument('--amax',type=int,default=3)
ap.add_argument('--asupp',type=int,default=99)
ap.add_argument('--bmax',type=int,default=99)
ap.add_argument('--milp',type=int,default=0)
ap.add_argument('--iters',type=int,default=8)
ap.add_argument('--linearD',type=int,default=0)
ap.add_argument('--maxbeta1',type=int,default=99, help='max ||beta||_1')
args=ap.parse_args()
k=args.k; N=1<<k
periods=[int(v) for v in args.periods.split(',')]
per=2 if args.mode=='half' else 1
dom=PDomain(k,per,args.P); hm=1.0/per; nc=k*per
atoms=Atoms(dom,hm)
t0=time.time()
alist={}
for p in periods:
    amx=min(p-1,args.amax)
    al=[]
    for a in itertools.product(range(0,amx+1),repeat=N):
        if sum(1 for v in a if v)<=args.asupp: al.append(a)
    alist[p]=al
for p in periods:
    lo=-(p//2)+1 if p>2 else 0; hi=p//2
    lo=max(lo,-args.bmax); hi=min(hi,args.bmax)
    breps=[b for b in itertools.product(range(lo,hi+1),repeat=nc) if any(b) and sum(abs(v) for v in b)<=args.maxbeta1]
    for b in breps:
        for a in alist[p]:
            for r in range(p):
                atoms.add(b,a,p,r)
print(f'k={k} mode={args.mode} P={args.P} periods={periods} points={dom.npts} atoms={len(atoms.spec)} ({time.time()-t0:.1f}s)',flush=True)
best=reweighted(dom,atoms,iters=args.iters,verbose=True,linearD=bool(args.linearD))
if best is None:
    print('INFEASIBLE with this atom set',flush=True); sys.exit()
sel,c=best
print('reweighted best cost',round(c,4),'atoms',len(sel),flush=True)
sel=greedy_prune(dom,atoms,sel,linearD=bool(args.linearD))
print('after prune: slope',round(sum(atoms.cost[j] for j in sel),4),'atoms',len(sel),flush=True)
for j in sel: print('   ',atoms.spec[j],'cost',atoms.cost[j],flush=True)
if args.milp:
    r=min_cost_milp(dom,atoms,time_limit=args.milp,linearD=bool(args.linearD))
    if r:
        ch,f,db,st=r
        print('MILP slope',f,'dual bound',db,'status',st,flush=True)
        for j in ch: print('   ',atoms.spec[j],'cost',atoms.cost[j],flush=True)
print(f'total time {time.time()-t0:.0f}s',flush=True)
