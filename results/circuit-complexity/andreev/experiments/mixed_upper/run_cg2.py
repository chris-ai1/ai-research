import sys; sys.path.insert(0,'/tmp/andreev_gap/mixed_upper')
from cg2 import *
ap=argparse.ArgumentParser()
ap.add_argument('--k',type=int,default=2); ap.add_argument('--mode',default='bs'); ap.add_argument('--P',type=int,default=8)
ap.add_argument('--periods',default='2,4,8'); ap.add_argument('--amax',type=int,default=7); ap.add_argument('--maxbeta1',type=int,default=99)
ap.add_argument('--iters',type=int,default=8); ap.add_argument('--asupp',type=int,default=99)
args=ap.parse_args()
k=args.k; N=1<<k; per=2 if args.mode=='half' else 1
dom=PDomain(k,per,args.P); hm=1.0/per; nc=k*per
betas={}; alphas={}
for p in [int(v) for v in args.periods.split(',')]:
    lo=-(p//2)+1 if p>2 else 0; hi=p//2
    betas[p]=[b for b in itertools.product(range(lo,hi+1),repeat=nc) if any(b) and sum(abs(v) for v in b)<=args.maxbeta1]
    alphas[p]=[a for a in itertools.product(range(0,min(p-1,args.amax)+1),repeat=N) if sum(1 for v in a if v)<=args.asupp]
sp=Space(dom,betas,alphas,hm)
natoms=sum(len(betas[p])*len(alphas[p])*p for p in betas)
print(f'k={k} mode={args.mode} P={args.P} periods={args.periods} points={dom.npts} atoms={natoms}',flush=True)
t0=time.time()
wt={}
wfun=lambda a: sp.cost(a[0],a[1])*wt.get(a,1.0)
active=[]; best=None
for it in range(args.iters):
    r=solve(sp,wfun,active,verbose=True,maxit=12)
    if r is None: print('infeasible'); sys.exit()
    w,active,f=r
    supp=[active[j] for j in range(len(active)) if abs(w[j])>1e-7*max(1,np.abs(w).max())]
    tot=sum(sp.cost(a[0],a[1]) for a in supp)
    print(f'  rw it {it}: support {len(supp)} slope {tot:.3f} active {len(active)} ({time.time()-t0:.0f}s)',flush=True)
    if best is None or tot<best[1]: best=(supp,tot)
    mx=max(abs(v) for v in w) if len(w) else 1
    wt={a:1.0/(abs(w[j])+1e-3*mx) for j,a in enumerate(active)}
    dflt=1.0/(1e-3*mx)
    wfun=lambda a,wt=wt,dflt=dflt: sp.cost(a[0],a[1])*wt.get(a,dflt)
sel=sorted(best[0],key=lambda a:-sp.cost(a[0],a[1]))
i=0
while i<len(sel):
    trial=sel[:i]+sel[i+1:]
    r=master(sp,trial,np.zeros(len(trial)))
    if r is not None and r[3]<1e-7: sel=trial
    else: i+=1
print('pruned slope',sum(sp.cost(a[0],a[1]) for a in sel),'atoms',len(sel),flush=True)
for a in sel: print('   p=%d beta=%s alpha=%s r=%d cost=%.3f'%(a[0],a[1],alphas[a[0]][a[2]],a[3],sp.cost(a[0],a[1])),flush=True)
print(f'time {time.time()-t0:.0f}s')
