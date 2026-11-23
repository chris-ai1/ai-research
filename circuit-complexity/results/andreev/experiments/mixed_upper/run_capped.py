"""periodic LP with only cheap atoms (cost <= cap) to look for slope < 3 at k=2."""
import sys; sys.path.insert(0,'/tmp/andreev_gap/mixed_upper')
from periodic_lp import *
import argparse
ap=argparse.ArgumentParser()
ap.add_argument('--P',type=int,default=4)
ap.add_argument('--periods',default='2,4')
ap.add_argument('--cap',type=float,default=0.5)
ap.add_argument('--mode',default='bs')
ap.add_argument('--k',type=int,default=2)
ap.add_argument('--amax',type=int,default=3)
ap.add_argument('--seed',type=int,default=0)
args=ap.parse_args()
k=args.k; N=1<<k
per=2 if args.mode=='half' else 1
dom=PDomain(k,per,args.P); hm=1.0/per; nc=k*per
atoms=Atoms(dom,hm)
periods=[int(v) for v in args.periods.split(',')]
for p in periods:
    lo=-(p//2)+1 if p>2 else 0; hi=p//2
    for b in itertools.product(range(lo,hi+1),repeat=nc):
        if not any(b): continue
        if sum(abs(v) for v in b)*hm/p>args.cap+1e-9: continue
        for a in itertools.product(range(0,min(p-1,args.amax)+1),repeat=N):
            for r in range(p): atoms.add(b,a,p,r)
print(f'k={k} mode={args.mode} P={args.P} cap={args.cap} atoms={len(atoms.spec)} points={dom.npts}',flush=True)
r=lp_weighted_l1(dom,atoms,np.array(atoms.cost))
if r is None: print('INFEASIBLE with cheap atoms only'); sys.exit()
best=reweighted(dom,atoms,iters=10,verbose=True)
sel,c=best
sel=greedy_prune(dom,atoms,sel)
print('pruned slope',sum(atoms.cost[j] for j in sel),'atoms',len(sel))
for j in sel: print('  ',tuple(int(v) for v in atoms.spec[j][0]),tuple(int(v) for v in atoms.spec[j][1]),atoms.spec[j][2],atoms.spec[j][3],atoms.cost[j])
