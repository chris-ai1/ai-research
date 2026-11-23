"""Fast column generation for the periodic slope LP (vectorised pricing over all alpha at once).
Atom (beta,alpha,p,r): value ((C.beta + X.alpha - r) mod p).  Pricing groups points by
(table t, v = C.beta mod p):  value = sum_t G_t[(X.alpha - r) mod p],  G_t[u] = sum_v Y_{t,v} ((v+u) mod p)."""
import sys; sys.path.insert(0,'/tmp/andreev_gap/mixed_upper')
from periodic_lp import PDomain
import numpy as np, itertools, time, argparse
from scipy.optimize import linprog
from scipy import sparse

class Space:
    def __init__(self, dom, betas_by_p, alphas_by_p, hm):
        self.dom=dom; self.hm=hm
        self.groups=[]   # (p, beta) 
        for p,bl in betas_by_p.items():
            for b in bl: self.groups.append((p,tuple(b)))
        self.alphas=alphas_by_p      # p -> array (nA, N)
        nt=len(dom.tables)
        self.XA={p:np.mod(dom.tables@np.array(al).T,p) for p,al in alphas_by_p.items()}   # (nt, nA)
        self.Cb={}
        for (p,b) in self.groups:
            self.Cb[(p,b)]=np.mod(dom.res@np.array(b),p)     # residue -> v
    def cost(self,p,b): return float(np.abs(np.array(b)).sum())*self.hm/p
    def col(self, atom):
        p,b,ai,r=atom
        dom=self.dom
        a=np.array(self.alphas[p][ai])
        L=dom.C@np.array(b)+dom.X@a
        return np.mod(L-r,p).astype(float)
    def price(self, y, weights_fn, tol=1e-9, maxadd=1500):
        dom=self.dom; nt=len(dom.tables); nr=len(dom.res)
        ys=(y*dom.sig).reshape(nt,nr)
        cand=[]
        for (p,b) in self.groups:
            v=self.Cb[(p,b)]
            Y=np.zeros((nt,p))
            for vv in range(p): Y[:,vv]=ys[:,v==vv].sum(1)
            G=np.zeros((nt,p))
            for u in range(p):
                G[:,u]=(Y*np.mod(np.arange(p)+u,p)[None,:]).sum(1)
            XA=self.XA[p]
            c=self.cost(p,b)
            for r in range(p):
                idx=np.mod(XA-r,p)                       # (nt,nA)
                g=np.take_along_axis(G,idx,axis=1).sum(0) # (nA,)
                rc=c-np.abs(g)
                for ai in np.nonzero(rc< -tol)[0]:
                    cand.append((rc[ai],(p,b,int(ai),r)))
        cand.sort(key=lambda z:z[0])
        return [a for _,a in cand[:maxadd]]

PEN=1e4
def master(sp, active, weights, pen=None):
    dom=sp.dom
    if pen is None: pen=PEN
    A=len(active); nt=len(dom.tables)
    sg=dom.sig.astype(float)
    Dm=sparse.csr_matrix((sg,(np.arange(dom.npts),dom.tix)),shape=(dom.npts,nt))
    I=sparse.identity(dom.npts,format='csr')
    if A:
        M=np.array([sp.col(a) for a in active]).T
        SM=sparse.csr_matrix(sg[:,None]*M)
        Aub=sparse.hstack([-SM,SM,-Dm,-I]).tocsr()
    else:
        Aub=sparse.hstack([-Dm,-I]).tocsr()
    c=np.concatenate([weights,weights,np.zeros(nt),pen*np.ones(dom.npts)])
    res=linprog(c,A_ub=Aub,b_ub=-np.ones(dom.npts),bounds=[(0,None)]*(2*A)+[(None,None)]*nt+[(0,None)]*dom.npts,method='highs')
    if res.status!=0: return None
    slack=res.x[2*A+nt:]
    return res.x[:A]-res.x[A:2*A], -res.ineqlin.marginals, res.fun, slack.sum()

def solve(sp, wfun, active, verbose=False, maxit=500):
    """wfun(atom)->weight.  Returns w, active, obj."""
    hist=[]
    for it in range(maxit):
        r=master(sp,active,np.array([wfun(a) for a in active]))
        if r is None:
            # master infeasible -> phase 1: price with zero-ish weights on a feasibility LP
            return None
        w,y,f,sl=r
        hist.append(f)
        if len(hist)>=3 and sl<1e-7 and hist[-3]-f<=1e-6*max(1,abs(f)):
            if verbose: print(f'    it {it}: stalled at obj {f:.5f}',flush=True)
            return w,active,f
        # pricing with general weights: reduced cost = weight(atom) - |sum y sig col|
        add=sp.price(y,wfun)
        if wfun is not None:
            add=[a for a in add if wfun(a)-0>0]  # all
        aset=set(active)
        add=[a for a in add if a not in aset]
        # exact reduced cost check with the true weights
        good=[]
        for a in add:
            col=sp.col(a); g=(y*sp.dom.sig)@col
            if wfun(a)-abs(g)< -1e-9: good.append(a)
        if verbose: print(f'    it {it}: active {len(active)} obj {f:.5f} slack {sl:.3g} add {len(good)}',flush=True)
        if not good: return (w,active,f) if sl<1e-7 else None
        active=active+good
    return (w,active[:len(w)],f) if sl<1e-7 else None
