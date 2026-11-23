"""Column generation over REALISABLE pure-parity atoms on the P=2 domain:
 p=2: beta=1_S, alpha in {0,1}^N (monomial amplitudes);  p=4: beta=2*1_S, alpha in {0..3}^N, support<=asupp
 (comb/threshold amplitudes).  Reweighted L1 on slope cost, then greedy prune."""
import sys; sys.path.insert(0,'/tmp/andreev_gap/mixed_upper')
from cg2 import *
ap=argparse.ArgumentParser(); ap.add_argument('--k',type=int,default=3); ap.add_argument('--asupp',type=int,default=3)
ap.add_argument('--iters',type=int,default=6); ap.add_argument('--p4',type=int,default=1); ap.add_argument('--seed',type=int,default=0)
args=ap.parse_args()
k=args.k; N=1<<k
dom=PDomain(k,1,2)
chars=[tuple((S>>i)&1 for i in range(k)) for S in range(1,N)]
betas={2:[c for c in chars]}
alphas={2:list(itertools.product((0,1),repeat=N))}
if args.p4:
    betas[4]=[tuple(2*v for v in c) for c in chars]
    alphas[4]=[a for a in itertools.product(range(4),repeat=N) if sum(1 for v in a if v)<=args.asupp]
sp=Space(dom,betas,alphas,1.0)
print(f'k={k} points={dom.npts} atoms={sum(len(betas[p])*len(alphas[p])*p for p in betas)}',flush=True)
t0=time.time(); wt={}; active=[]; best=None
wfun=lambda a: sp.cost(a[0],a[1])
for it in range(args.iters):
    r=solve(sp,wfun,active)
    if r is None: print('infeasible'); sys.exit()
    w,active,f=r
    supp=[active[j] for j in range(len(active)) if abs(w[j])>1e-7*max(1,np.abs(w).max())]
    tot=sum(sp.cost(a[0],a[1]) for a in supp)
    print(f'  rw it {it}: support {len(supp)} slope {tot:.3f} active {len(active)} ({time.time()-t0:.0f}s)',flush=True)
    if best is None or tot<best[1]: best=(supp,tot)
    mx=max(abs(v) for v in w)
    wt={a:1.0/(abs(w[j])+1e-3*mx) for j,a in enumerate(active)}
    dflt=1.0/(1e-3*mx)
    wfun=lambda a,wt=wt,dflt=dflt: sp.cost(a[0],a[1])*wt.get(a,dflt)
rng=np.random.default_rng(args.seed)
bestsel=None
for trial in range(4):
    sel=sorted(best[0],key=lambda a:-sp.cost(a[0],a[1])) if trial==0 else list(rng.permutation(np.array(best[0],dtype=object)))
    sel=[tuple(a) for a in sel]
    i=0
    while i<len(sel):
        tr=sel[:i]+sel[i+1:]
        rr=master(sp,tr,np.zeros(len(tr)))
        if rr is not None and rr[3]<1e-7: sel=tr
        else: i+=1
    c=sum(sp.cost(a[0],a[1]) for a in sel)
    print(f'  prune trial {trial}: slope {c} atoms {len(sel)}',flush=True)
    if bestsel is None or c<bestsel[1]: bestsel=(sel,c)
sel=bestsel[0]
print('pruned slope',bestsel[1],'atoms',len(sel),flush=True)
for a in sel: print('   p=%d beta=%s alpha=%s r=%d cost=%.3f'%(a[0],a[1],alphas[a[0]][a[2]],a[3],sp.cost(a[0],a[1])),flush=True)
import json
json.dump([[a[0],list(a[1]),list(alphas[a[0]][a[2]]),a[3]] for a in sel],open(f'logs/cg_parity_k{k}_atoms.json','w'))
print(f'time {time.time()-t0:.0f}s')
