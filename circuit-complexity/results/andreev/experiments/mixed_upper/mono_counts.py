"""Pure-parity model with MONOMIAL amplitudes and prescribed gadget counts per character:
A_g(x) = Delta_g * (-1)^{alpha_g . x} * sigma_g, alpha_g in {0,1}^N chosen by the solver.  Feasibility (CP-SAT).
Monomial atoms are realisable at cost |S|m/2 + O(1) (period-2 staircase on t_S + alpha_g.x)."""
import sys; sys.path.insert(0,'/tmp/pydeps')
import argparse, time
from ortools.sat.python import cp_model
ap=argparse.ArgumentParser(); ap.add_argument('--k',type=int,default=3); ap.add_argument('--W',type=int,default=12)
ap.add_argument('--counts',default='1:2,2:2,4:2,3:2,5:2,6:2,7:1'); ap.add_argument('--tl',type=float,default=600)
ap.add_argument('--workers',type=int,default=3); ap.add_argument('--linD',type=int,default=1)
args=ap.parse_args()
k=args.k; N=1<<k; chars=list(range(1,N))
cnt={int(a.split(':')[0]):int(a.split(':')[1]) for a in args.counts.split(',')}
gad=[(S,j) for S in chars for j in range(cnt.get(S,1))]
md=cp_model.CpModel()
Dl={g:md.NewIntVar(-args.W,args.W,'') for g in gad}
for g in gad: md.Add(Dl[g]!=0)
al={g:[md.NewBoolVar('') for c in range(N)] for g in gad}
if args.linD:
    dl=[md.NewIntVar(-50*args.W,50*args.W,'') for c in range(N)]; d0=md.NewIntVar(-400*args.W,400*args.W,'')
par=lambda v: bin(v).count('1')&1
for t in range(1<<N):
    xs=[c for c in range(N) if (t>>c)&1]
    a={}
    for g in gad:
        tau=md.NewBoolVar('')   # tau = parity(alpha_g restricted to xs)
        md.AddBoolXOr([al[g][c] for c in xs]+[tau.Not()]) if xs else md.Add(tau==0)
        a[g]=md.NewIntVar(-args.W,args.W,'')
        md.Add(a[g]==Dl[g]).OnlyEnforceIf(tau.Not()); md.Add(a[g]==-Dl[g]).OnlyEnforceIf(tau)
    D=(sum(dl[c] for c in xs)+d0) if args.linD else md.NewIntVar(-400*args.W,400*args.W,'')
    for b in range(N):
        e=sum(a[g] for g in gad if par(g[0]&b))+D
        if (t>>b)&1: md.Add(e>=1)
        else: md.Add(e<=-1)
sol=cp_model.CpSolver(); sol.parameters.max_time_in_seconds=args.tl; sol.parameters.num_workers=args.workers
t0=time.time(); st=sol.Solve(md)
slope=sum(bin(S).count('1') for S,j in gad)/2
print(f'k={k} counts={args.counts} slope={slope} linD={args.linD} status={sol.StatusName(st)} time={time.time()-t0:.0f}s',flush=True)
if st in (cp_model.OPTIMAL,cp_model.FEASIBLE):
    for g in gad: print('  S=%s Delta=%d alpha=%s'%(format(g[0],'0%db'%k)[::-1],sol.Value(Dl[g]),''.join(str(sol.Value(v)) for v in al[g])))
    if args.linD: print('  D',[sol.Value(v) for v in dl],sol.Value(d0))
