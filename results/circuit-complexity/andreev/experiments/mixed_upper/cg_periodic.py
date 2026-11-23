"""Column-generation version of the periodic slope LP (memory-light; atoms generated on the fly).
Master: min sum_a cost_a (wp_a + wm_a)  s.t.  sig_p (sum_a (wp_a - wm_a) col_a(p) + D_{t(p)}) >= 1.
Pricing: reduced cost of wp_a = cost_a - sum_p y_p sig_p col_a(p) ; of wm_a = cost_a + (same sum)."""
import sys; sys.path.insert(0,'/tmp/andreev_gap/mixed_upper')
from periodic_lp import PDomain
import numpy as np, itertools, time, argparse
from scipy.optimize import linprog
from scipy import sparse

class AtomSpace:
    def __init__(self, dom, specs, hm):
        self.dom=dom; self.specs=specs; self.hm=hm
        self.cost=np.array([float(np.abs(np.array(b)).sum())*hm/p for (b,a,p,r) in specs])
        self.Cb={}; 
    def col(self, j):
        b,a,p,r=self.specs[j]
        L=self.dom.C@np.array(b)+self.dom.X@np.array(a)
        return np.mod(L-r,p).astype(np.float64)
    def cols(self, idx):
        return np.array([self.col(j) for j in idx]).T

def master(dom, AS, active, weights):
    M=AS.cols(active); A=len(active); nt=len(dom.tables)
    sg=dom.sig.astype(np.float64)
    Dm=sparse.csr_matrix((np.ones(dom.npts),(np.arange(dom.npts),dom.tix)),shape=(dom.npts,nt))
    SM=sparse.csr_matrix(sg[:,None]*M)
    Aub=sparse.hstack([-SM,SM,-sparse.diags(sg)@Dm]).tocsr()
    c=np.concatenate([weights,weights,np.zeros(nt)])
    bounds=[(0,None)]*(2*A)+[(None,None)]*nt
    res=linprog(c,A_ub=Aub,b_ub=-np.ones(dom.npts),bounds=bounds,method='highs')
    if res.status!=0: return None
    w=res.x[:A]-res.x[A:2*A]
    y=-res.ineqlin.marginals   # >=0 duals of the >= constraints
    return w,y,res.fun

def price(dom, AS, y, weights_all, chunk=4000, tol=1e-9, maxadd=400):
    sg=dom.sig.astype(np.float64); ys=y*sg
    cand=[]
    J=len(AS.specs)
    for st in range(0,J,chunk):
        idx=list(range(st,min(J,st+chunk)))
        M=AS.cols(idx)
        g=ys@M
        rc_p=weights_all[idx]-g; rc_m=weights_all[idx]+g
        rc=np.minimum(rc_p,rc_m)
        for t in np.nonzero(rc<-tol)[0]: cand.append((rc[t],idx[t]))
    cand.sort()
    return [j for _,j in cand[:maxadd]]

def solve_cg(dom, AS, weights_all, active=None, verbose=False, maxit=200):
    if active is None:
        # start: cheapest atoms of every (beta,p) class with alpha=0
        active=list(range(min(200,len(AS.specs))))
    active=list(dict.fromkeys(active))
    for it in range(maxit):
        r=None
        while r is None:
            r=master(dom,AS,active,weights_all[active])
            if r is None:
                # infeasible master: add random atoms
                rng=np.random.default_rng(it)
                active=list(dict.fromkeys(active+list(rng.choice(len(AS.specs),500,replace=False))))
        w,y,f=r
        add=price(dom,AS,y,weights_all)
        add=[j for j in add if j not in set(active)]
        if verbose: print(f'    cg it {it}: active {len(active)} obj {f:.4f} add {len(add)}',flush=True)
        if not add: return w,active,f
        active=active+add
    return w,active,f

def feasible_sel(dom, AS, sel):
    r=master(dom,AS,list(sel),np.zeros(len(sel)))
    return r is not None

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--k',type=int,default=2)
    ap.add_argument('--mode',default='bs')
    ap.add_argument('--P',type=int,default=8)
    ap.add_argument('--periods',default='2,4,8')
    ap.add_argument('--amax',type=int,default=3)
    ap.add_argument('--asupp',type=int,default=99)
    ap.add_argument('--maxbeta1',type=int,default=99)
    ap.add_argument('--iters',type=int,default=6)
    ap.add_argument('--seed',type=int,default=0)
    args=ap.parse_args()
    k=args.k; N=1<<k; per=2 if args.mode=='half' else 1
    dom=PDomain(k,per,args.P); hm=1.0/per; nc=k*per
    specs=[]; seen=set()
    for p in [int(v) for v in args.periods.split(',')]:
        lo=-(p//2)+1 if p>2 else 0; hi=p//2
        for b in itertools.product(range(lo,hi+1),repeat=nc):
            if not any(b) or sum(abs(v) for v in b)>args.maxbeta1: continue
            for a in itertools.product(range(0,min(p-1,args.amax)+1),repeat=N):
                if sum(1 for v in a if v)>args.asupp: continue
                for r in range(p): specs.append((b,a,p,r))
    AS=AtomSpace(dom,specs,hm)
    print(f'k={k} mode={args.mode} P={args.P} periods={args.periods} points={dom.npts} atoms={len(specs)}',flush=True)
    t0=time.time()
    wts=AS.cost.copy(); best=None; active=None
    rng=np.random.default_rng(args.seed)
    for it in range(args.iters):
        w,active,f=solve_cg(dom,AS,wts,active=active)
        supp=[active[j] for j in range(len(active)) if abs(w[j])>1e-7*max(1,np.abs(w).max())]
        tot=AS.cost[supp].sum()
        print(f'  rw it {it}: support {len(supp)} slope-cost {tot:.3f} ({time.time()-t0:.0f}s)',flush=True)
        if best is None or tot<best[1]: best=(supp,tot)
        wfull=np.zeros(len(specs)); 
        for j,a in enumerate(active): wfull[a]=abs(w[j])
        wts=AS.cost/(wfull+1e-3*max(1,wfull.max()))
    sel=sorted(best[0],key=lambda j:-AS.cost[j])
    i=0
    while i<len(sel):
        trial=sel[:i]+sel[i+1:]
        if feasible_sel(dom,AS,trial): sel=trial
        else: i+=1
    print('pruned slope',AS.cost[sel].sum(),'atoms',len(sel),flush=True)
    for j in sel: print('   ',specs[j],AS.cost[j],flush=True)
    print(f'time {time.time()-t0:.0f}s')
