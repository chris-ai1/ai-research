# Copyright (c) 2026 Christian Reitwiessner
# Authors: Christian Reitwiessner
"""Exact merged-construction costs and finite Fourier checks; no solver jobs."""
import sys, json, math, itertools
sys.path[:0]=['/tmp/pydeps','/tmp/andreev_gap/push_upper']
import numpy as np
from constr3 import build_dpp

def costs(k,m):
    C=build_dpp(k,m)
    # Normalize each bottom threshold by its positive coefficient gcd.
    # ceil(theta/gcd) preserves the Boolean gate on integer inputs.
    B=pad=normB=normpad=0
    for w,t in zip(C.W,C.T):
        w=[int(z) for z in w]; b=sum(abs(z) for z in w)
        q=math.gcd(*w); tt=-((-t)//q); bb=b//q
        # sum positive literal wires >= t + sum negative weights.
        r=t+sum(-z for z in w if z<0)
        rr=tt+sum(-z//q for z in w if z<0)
        B+=b; pad+=abs(b-2*r+1)
        normB+=bb; normpad+=abs(bb-2*rr+1)
    top=sum(abs(int(v)) for v in C.V)
    direct=sum(abs(int(v)) for v in C.u)
    neg=sum(-int(v) for v in C.V if v<0)+sum(-int(v) for v in C.u if v<0)
    # Actual output is [P<0], or [-sum v*g -u*z >= K+1].
    # Padding cost invariant under complement (threshold B-r+1).
    r=-C.K+neg # [P >= 0], whose complement is desired output.
    tp=abs(top+direct-2*r+1)
    return dict(k=k,m=m,N=C.N,gates=C.size(),bottom_L1=B,bottom_padding=pad,
                bottom_gcd_L1=normB,bottom_gcd_padding=normpad,top_L1=top,
                direct_L1=direct,bias=int(C.K),top_padding=int(tp),
                coefficient_total=B+top+direct,
                gcd_coefficient_total=normB+top+direct,
                majority_wires_with_constants=normB+normpad+top+direct+int(tp),
                clones_bottom_L1=sum(abs(int(v))*sum(abs(int(w)) for w in row) for row,v in zip(C.W,C.V)))

def fourier_checks():
    checks=[]
    for M in range(2,8):
        Z=np.array(list(itertools.product([0,1],repeat=M)),dtype=int)
        chi=(-1.)**Z.sum(1)
        best=0
        for signs in itertools.product([-1,1],repeat=M):
            L=Z@np.array(signs)
            for t in range(int(L.min()),int(L.max())+2):
                best=max(best,abs(float(chi@(L>=t)/(2**M))))
        bound=math.comb(M-1,(M-1)//2)/2**M
        assert best==bound
        checks.append(dict(M=M,max_parity_coefficient=best))
    # Degree-d address coefficients for each gate have rank one across table settings.
    rng=np.random.default_rng(17)
    for k,m in [(2,2),(2,3),(3,2)]:
        M=k*m; Z=np.array(list(itertools.product([0,1],repeat=M)),dtype=int)
        for _ in range(20):
            w=rng.integers(-1,2,size=M); L=Z@w
            for d in range(2,M+1):
                subsets=list(itertools.combinations(range(M),d))
                chars=np.array([(-1.)**Z[:,T].sum(1) for T in subsets]).T
                H=np.array([(L>=t)@chars for t in range(int(L.min()),int(L.max())+2)])
                assert np.linalg.matrix_rank(H,tol=1e-7)<=1
    return checks
if __name__=='__main__':
    result=dict(costs=[costs(k,m) for k,m in [(2,2),(3,2),(4,4),(5,6),(6,10),(7,18)]],fourier_checks=fourier_checks())
    print(json.dumps(result,indent=2))
