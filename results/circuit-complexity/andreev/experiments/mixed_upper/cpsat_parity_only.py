"""Exact minimisation (bounded integer weights) of the PARITY-ONLY periodic slope for any k:
   F(x,b) = D(x) + sum_S A_S(x) e_S(b),   A_S(x) = sum_alpha w_{S,alpha} (-1)^{alpha.x},
each monomial term = one period-2 staircase on t_S + alpha.x  (cost |S|/2 per unit m).
Minimise sum_S |S|/2 * #{alpha: w_{S,alpha} != 0}.  D(x) free per table.
Option --tsupp restricts alpha to monomials of degree <= tsupp."""
import sys; sys.path.insert(0,'/tmp/pydeps')
import itertools, numpy as np, argparse, time
from ortools.sat.python import cp_model
ap=argparse.ArgumentParser()
ap.add_argument('--k',type=int,default=3)
ap.add_argument('--W',type=int,default=4)
ap.add_argument('--tsupp',type=int,default=1)
ap.add_argument('--tl',type=float,default=900)
ap.add_argument('--workers',type=int,default=4)
ap.add_argument('--ub',type=float,default=99)
args=ap.parse_args()
k=args.k; N=1<<k
chars=list(range(1,N))
alphas=[a for a in range(1<<N) if bin(a).count('1')<=args.tsupp and a!=0] + [0]
tabs=list(range(1<<N))
md=cp_model.CpModel()
w={}
z={}
for S in chars:
    for a in alphas:
        w[S,a]=md.NewIntVar(-args.W,args.W,f'w{S}_{a}')
        z[S,a]=md.NewBoolVar(f'z{S}_{a}')
        md.Add(w[S,a]==0).OnlyEnforceIf(z[S,a].Not())
D=[md.NewIntVar(-10000,10000,f'D{t}') for t in tabs]
par=lambda v: bin(v).count('1')&1
for t in tabs:
    for b in range(N):
        terms=[]
        for S in chars:
            if par(S&b):
                for a in alphas:
                    terms.append((1-2*par(a&t))*w[S,a])
        expr=sum(terms)+D[t]
        if (t>>b)&1: md.Add(expr>=1)
        else: md.Add(expr<=-1)
cost={S:bin(S).count('1') for S in chars}     # in units of 1/2
obj=sum(cost[S]*z[S,a] for S in chars for a in alphas)
md.Add(obj<=int(2*args.ub))
md.Minimize(obj)
sol=cp_model.CpSolver(); sol.parameters.max_time_in_seconds=args.tl; sol.parameters.num_workers=args.workers
t0=time.time(); st=sol.Solve(md)
print(f'k={k} tsupp={args.tsupp} W={args.W} status={sol.StatusName(st)} slope={sol.ObjectiveValue()/2 if st in (cp_model.OPTIMAL,cp_model.FEASIBLE) else None} bound={sol.BestObjectiveBound()/2} time={time.time()-t0:.0f}s',flush=True)
if st in (cp_model.OPTIMAL,cp_model.FEASIBLE):
    for S in chars:
        terms=[(a,sol.Value(w[S,a])) for a in alphas if sol.Value(z[S,a])]
        print('  S=',format(S,'0%db'%k)[::-1],'terms',[(format(a,'0%db'%N)[::-1],v) for a,v in terms])
