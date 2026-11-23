"""Parity-only model, arbitrary two-valued amplitudes, gadget counts n_{|S|} per character size,
Delta depending only on (|S|, j) (block-permutation symmetric ansatz).  Feasibility of a table is
invariant under address translations (flip signs of amplitudes) and complement; with symmetric Delta also
under block permutations -> use one representative per orbit.  CP-SAT."""
import sys; sys.path.insert(0,'/tmp/pydeps')
import itertools, argparse, time
from ortools.sat.python import cp_model
ap=argparse.ArgumentParser(); ap.add_argument('--k',type=int,default=4); ap.add_argument('--W',type=int,default=24)
ap.add_argument('--counts',default='2,2,2,1', help='n per |S| = 1..k'); ap.add_argument('--tl',type=float,default=900)
ap.add_argument('--workers',type=int,default=4)
args=ap.parse_args()
k=args.k; N=1<<k
ns=[int(v) for v in args.counts.split(',')]
chars=list(range(1,N)); sz=lambda S: bin(S).count('1')
par=lambda v: bin(v).count('1')&1
perms=list(itertools.permutations(range(k)))
def permaddr(c,pm): return sum(((c>>i)&1)<<pm[i] for i in range(k))
def canon(t):
    best=None
    xs=[(t>>c)&1 for c in range(N)]
    for pm in perms:
        for v in range(N):
            for comp in (0,1):
                y=0
                for c in range(N):
                    if xs[c]^comp: y|=1<<(permaddr(c,pm)^v)
                if best is None or y<best: best=y
    return best
t0=time.time()
import numpy as np
T=np.arange(1<<N,dtype=np.int64)
bits=((T[:,None]>>np.arange(N)[None,:])&1)
best=T.copy()
for pm in perms:
    for v in range(N):
        pos=np.array([permaddr(c,pm)^v for c in range(N)],dtype=np.int64)
        y=(bits<<pos[None,:]).sum(1)
        best=np.minimum(best,y)
        yc=((1-bits)<<pos[None,:]).sum(1)
        best=np.minimum(best,yc)
reps=sorted(set(int(v) for v in best))
print(f'k={k} orbit representatives: {len(reps)} ({time.time()-t0:.0f}s)',flush=True)
md=cp_model.CpModel()
Dl={(s,j):md.NewIntVar(1,args.W,f'D{s}_{j}') for s in range(1,k+1) for j in range(ns[s-1])}
gad=[(S,j) for S in chars for j in range(ns[sz(S)-1])]
for t in reps:
    a={}
    for g in gad:
        tau=md.NewBoolVar('')
        a[g]=md.NewIntVar(-args.W,args.W,'')
        d=Dl[(sz(g[0]),g[1])]
        md.Add(a[g]==d).OnlyEnforceIf(tau); md.Add(a[g]==-d).OnlyEnforceIf(tau.Not())
    D=md.NewIntVar(-200*args.W,200*args.W,'')
    for b in range(N):
        e=sum(a[g] for g in gad if par(g[0]&b))+D
        if (t>>b)&1: md.Add(e>=1)
        else: md.Add(e<=-1)
sol=cp_model.CpSolver(); sol.parameters.max_time_in_seconds=args.tl; sol.parameters.num_workers=args.workers
st=sol.Solve(md)
cost=sum(ns[s-1]*s*sum(1 for S in chars if sz(S)==s) for s in range(1,k+1))/2
print(f'k={k} counts={ns} slope={cost} status={sol.StatusName(st)} time={time.time()-t0:.0f}s',flush=True)
if st in (cp_model.OPTIMAL,cp_model.FEASIBLE): print('  Deltas',{key:sol.Value(v) for key,v in Dl.items()})
