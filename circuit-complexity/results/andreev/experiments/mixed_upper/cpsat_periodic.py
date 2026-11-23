"""Exact (bounded-integer-weight) minimisation of the periodic slope with CP-SAT.
Weights w_a integer in [-W,W]; D_x integer; minimise sum cost_a [w_a != 0]."""
import sys; sys.path.insert(0,'/tmp/andreev_gap/mixed_upper')
from periodic_lp import *
from ortools.sat.python import cp_model
import argparse
ap=argparse.ArgumentParser()
ap.add_argument('--k',type=int,default=2)
ap.add_argument('--P',type=int,default=4)
ap.add_argument('--periods',default='2,4')
ap.add_argument('--mode',default='bs')
ap.add_argument('--W',type=int,default=6)
ap.add_argument('--cap',type=float,default=9)
ap.add_argument('--ub',type=float,default=99)
ap.add_argument('--tl',type=float,default=600)
ap.add_argument('--workers',type=int,default=4)
ap.add_argument('--amax',type=int,default=3)
args=ap.parse_args()
k=args.k; N=1<<k
per=2 if args.mode=='half' else 1
dom=PDomain(k,per,args.P); hm=1.0/per; nc=k*per
atoms=Atoms(dom,hm)
for p in [int(v) for v in args.periods.split(',')]:
    lo=-(p//2)+1 if p>2 else 0; hi=p//2
    for b in itertools.product(range(lo,hi+1),repeat=nc):
        if not any(b): continue
        if sum(abs(v) for v in b)*hm/p>args.cap+1e-9: continue
        for a in itertools.product(range(0,min(p-1,args.amax)+1),repeat=N):
            for r in range(p): atoms.add(b,a,p,r)
M=atoms.matrix().astype(int)
A=M.shape[1]
scale=max(1,int(round(1/min(atoms.cost)))) if min(atoms.cost)>0 else 4
scale=8
costi=[int(round(c*scale)) for c in atoms.cost]
print(f'atoms={A} points={dom.npts} cost scale={scale}',flush=True)
md=cp_model.CpModel()
w=[md.NewIntVar(-args.W,args.W,f'w{j}') for j in range(A)]
z=[md.NewBoolVar(f'z{j}') for j in range(A)]
for j in range(A):
    md.Add(w[j]==0).OnlyEnforceIf(z[j].Not())
nt=len(dom.tables)
Dv=[md.NewIntVar(-1000,1000,f'D{t}') for t in range(nt)]
for p in range(dom.npts):
    nz=np.nonzero(M[p])[0]
    expr=sum(int(M[p,j])*w[j] for j in nz)+Dv[dom.tix[p]]
    if dom.sig[p]>0: md.Add(expr>=1)
    else: md.Add(expr<=-1)
obj=sum(costi[j]*z[j] for j in range(A))
md.Add(obj<=int(round(args.ub*scale)))
md.Minimize(obj)
sol=cp_model.CpSolver(); sol.parameters.max_time_in_seconds=args.tl; sol.parameters.num_workers=args.workers
st=sol.Solve(md)
print('status',sol.StatusName(st),'obj',sol.ObjectiveValue()/scale if st in (cp_model.OPTIMAL,cp_model.FEASIBLE) else None,'bound',sol.BestObjectiveBound()/scale,flush=True)
if st in (cp_model.OPTIMAL,cp_model.FEASIBLE):
    for j in range(A):
        if sol.Value(z[j]): print('  ',tuple(int(v) for v in atoms.spec[j][0]),tuple(int(v) for v in atoms.spec[j][1]),atoms.spec[j][2],atoms.spec[j][3],'w=',sol.Value(w[j]),'cost',atoms.cost[j])
