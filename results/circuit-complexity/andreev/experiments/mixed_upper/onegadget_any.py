"""Is 'one two-valued gadget per character' possible at k (amplitudes arbitrary functions of x)?
A_S(x) = Delta_S * (2 tau_{S,x} - 1),  Delta_S in [1,W] integers, tau free booleans, D_x free.
For every table x and address b: sign(D_x + sum_{S.b odd} A_S(x)) = 2x_b - 1 (margin 1)."""
import sys; sys.path.insert(0,'/tmp/pydeps')
import argparse, time
from ortools.sat.python import cp_model
ap=argparse.ArgumentParser(); ap.add_argument('--k',type=int,default=3); ap.add_argument('--W',type=int,default=12)
ap.add_argument('--tl',type=float,default=600); ap.add_argument('--workers',type=int,default=4)
ap.add_argument('--extra',default='', help='comma list of characters (ints) that get a second gadget')
ap.add_argument('--counts',default='', help='S:n,... number of gadgets per character (overrides)')
args=ap.parse_args()
k=args.k; N=1<<k; chars=list(range(1,N))
gad=[(S,0) for S in chars]+[(int(S),1) for S in args.extra.split(',') if S]
if args.counts:
    cnt={int(a.split(':')[0]):int(a.split(':')[1]) for a in args.counts.split(',')}
    gad=[(S,j) for S in chars for j in range(cnt.get(S,1))]
md=cp_model.CpModel()
Dl={g:md.NewIntVar(1,args.W,f'Dl{g}') for g in gad}
par=lambda v: bin(v).count('1')&1
for t in range(1<<N):
    a={}
    for g in gad:
        tau=md.NewBoolVar('')
        a[g]=md.NewIntVar(-args.W,args.W,'')
        md.Add(a[g]==Dl[g]).OnlyEnforceIf(tau); md.Add(a[g]==-Dl[g]).OnlyEnforceIf(tau.Not())
    D=md.NewIntVar(-100*args.W,100*args.W,'')
    for b in range(N):
        e=sum(a[g] for g in gad if par(g[0]&b))+D
        if (t>>b)&1: md.Add(e>=1)
        else: md.Add(e<=-1)
sol=cp_model.CpSolver(); sol.parameters.max_time_in_seconds=args.tl; sol.parameters.num_workers=args.workers
t0=time.time(); st=sol.Solve(md)
print(f'k={k} extra={args.extra} counts={args.counts} W={args.W} status={sol.StatusName(st)} time={time.time()-t0:.0f}s',flush=True)
if st in (cp_model.OPTIMAL,cp_model.FEASIBLE):
    print('  Deltas',{g:sol.Value(Dl[g]) for g in gad})
