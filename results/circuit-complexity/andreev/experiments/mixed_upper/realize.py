"""Given periodic atoms (beta,alpha,p,r), find exact rational weights (LP, margin 1, D linear if possible),
build the finite circuits for a range of m and verify them exactly (count vectors; bits for small n)."""
import sys; sys.path.insert(0,'/tmp/andreev_gap/mixed_upper')
from periodic_lp import PDomain
from build_periodic import build, verify_counts, verify_bits
import numpy as np, itertools, json, math
from fractions import Fraction as Fr
from scipy.optimize import linprog
from scipy import sparse

def lp_weights(k, per, P, atoms, linearD=True, l1=True):
    dom=PDomain(k,per,P)
    cols=[]
    for (b,a,p,r) in atoms:
        L=dom.C@np.array(b)+dom.X@np.array(a); cols.append(np.mod(L-r,p))
    M=np.array(cols,dtype=float).T; A=M.shape[1]; sg=dom.sig.astype(float)[:,None]
    if linearD: Dm=np.hstack([dom.X.astype(float),np.ones((dom.npts,1))])
    else: Dm=sparse.csr_matrix((np.ones(dom.npts),(np.arange(dom.npts),dom.tix)),shape=(dom.npts,len(dom.tables))).toarray()
    nd=Dm.shape[1]
    Aub=np.hstack([-sg*M,sg*M,-sg*Dm]); c=np.concatenate([np.ones(2*A),np.zeros(nd)]) if l1 else np.zeros(2*A+nd)
    res=linprog(c,A_ub=Aub,b_ub=-np.ones(dom.npts),bounds=[(0,None)]*(2*A)+[(None,None)]*nd,method='highs')
    if res.status!=0: return None
    w=res.x[:A]-res.x[A:2*A]; d=res.x[2*A:]
    return w,d,dom

def rationalize(v,den=64):
    return [Fr(int(round(x*den)),den) for x in v]

def realize(k, per, P, atoms, ms, linearD=True, den=64, bits_max_n=20, verbose=True):
    r=lp_weights(k,per,P,atoms,linearD)
    if r is None: return None
    w,d,dom=r
    W=rationalize(w,den); Dd=rationalize(d,den)
    N=1<<k
    out=[]
    for m in ms:
        if per==1: parts=[[m]]*k
        else: parts=[[(m+1)//2, m//2]]*k
        at=[(tuple(int(v) for v in b),tuple(int(v) for v in a),int(p),int(rr),ww) for (b,a,p,rr),ww in zip(atoms,W)]
        if linearD:
            circ=build(k,parts,at,None,linearD=(Dd[:N],Dd[N]))
        else:
            circ=build(k,parts,at,{t:Dd[t] for t in range(len(Dd))})
        ok,mn,npts=verify_counts(k,parts,circ)
        n=N+k*m
        okb=None
        if n<=bits_max_n: okb,_=verify_bits(k,parts,circ)
        G=len(circ[0])
        out.append((m,G,ok,okb,mn))
        if verbose: print(f'  k={k} m={m} n={n} gates={G} count-check={ok} bit-check={okb} min|top|={mn}',flush=True)
    return out,W,Dd
