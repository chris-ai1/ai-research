"""Parity-only model with THRESHOLD amplitudes (realisable at cost |S|m/2+O(1) by a period-p staircase on
(p/2) t_S + alpha.x, p > 2 range(alpha.x)):   A_g(x) = Delta_g * (2[alpha_g.x >= theta_g] - 1).
F = D(x) + sum_g A_g(x) e_{S_g}(b).  D free per table, or linear (--linD).  Decide feasibility (CP-SAT)."""
import sys; sys.path.insert(0,'/tmp/pydeps')
import argparse, time
from ortools.sat.python import cp_model
ap=argparse.ArgumentParser(); ap.add_argument('--k',type=int,default=3); ap.add_argument('--W',type=int,default=16)
ap.add_argument('--A',type=int,default=3); ap.add_argument('--tl',type=float,default=600); ap.add_argument('--workers',type=int,default=4)
ap.add_argument('--counts',default=''); ap.add_argument('--linD',type=int,default=0); ap.add_argument('--DW',type=int,default=400)
args=ap.parse_args()
k=args.k; N=1<<k; chars=list(range(1,N))
cnt={}
if args.counts: cnt={int(a.split(':')[0]):int(a.split(':')[1]) for a in args.counts.split(',')}
gad=[(S,j) for S in chars for j in range(cnt.get(S,1))]
md=cp_model.CpModel()
Dl={g:md.NewIntVar(1,args.W,'') for g in gad}
al={g:[md.NewIntVar(-args.A,args.A,'') for c in range(N)] for g in gad}
th={g:md.NewIntVar(-N*args.A-1,N*args.A+1,'') for g in gad}
if args.linD:
    dl=[md.NewIntVar(-args.DW,args.DW,'') for c in range(N)]; d0=md.NewIntVar(-args.DW*N,args.DW*N,'')
par=lambda v: bin(v).count('1')&1
for t in range(1<<N):
    xs=[(t>>c)&1 for c in range(N)]
    a={}
    for g in gad:
        tau=md.NewBoolVar('')
        lin=sum(al[g][c] for c in range(N) if xs[c])
        md.Add(lin>=th[g]).OnlyEnforceIf(tau); md.Add(lin<=th[g]-1).OnlyEnforceIf(tau.Not())
        a[g]=md.NewIntVar(-args.W,args.W,'')
        md.Add(a[g]==Dl[g]).OnlyEnforceIf(tau); md.Add(a[g]==-Dl[g]).OnlyEnforceIf(tau.Not())
    if args.linD: D=sum(dl[c] for c in range(N) if xs[c])+d0
    else: D=md.NewIntVar(-100*args.W,100*args.W,'')
    for b in range(N):
        e=sum(a[g] for g in gad if par(g[0]&b))+D
        if (t>>b)&1: md.Add(e>=1)
        else: md.Add(e<=-1)
sol=cp_model.CpSolver(); sol.parameters.max_time_in_seconds=args.tl; sol.parameters.num_workers=args.workers
t0=time.time(); st=sol.Solve(md)
print(f'k={k} counts={args.counts} linD={args.linD} W={args.W} A={args.A} status={sol.StatusName(st)} time={time.time()-t0:.0f}s',flush=True)
if st in (cp_model.OPTIMAL,cp_model.FEASIBLE):
    for g in gad:
        print('  gadget S=%s j=%d Delta=%d alpha=%s theta=%d'%(format(g[0],'0%db'%k)[::-1],g[1],sol.Value(Dl[g]),[sol.Value(v) for v in al[g]],sol.Value(th[g])))
    if args.linD: print('  D linear',[sol.Value(v) for v in dl],sol.Value(d0))
