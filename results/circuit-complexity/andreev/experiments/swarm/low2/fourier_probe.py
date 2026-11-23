# Copyright (c) 2026 Christian Reitwiessner. All rights reserved.
# Authors: Christian Reitwiessner
"""Test a low-degree Fourier interpolation certificate on explicit central pools.

The Krawtchouk sum computes exact integer coefficients (scaled by 2**M).
Numerical LP outcomes are explicitly diagnostic; no asymptotic inference.
"""
import sys
sys.path.insert(0, '/tmp/andreev_gap/coherence_fable/pydeps_local')
import numpy as np
from scipy.optimize import linprog
from itertools import combinations
from math import comb
from fractions import Fraction as Q
import json
from pathlib import Path

def coeff(M,r,t):
    return sum((-1)**u*comb(r,u)*comb(M-r,v)
               for u in range(r+1) for v in range(M-r+1) if u+v>=t)

rng=np.random.default_rng(561832)
results=[]
for M,S in ((12,24),(16,32),(20,40),(24,96)):
    masks=rng.choice((-1,1),size=(S,M))
    thresholds=rng.integers(M//2-1,M//2+3,size=S)
    target=tuple(range(M//2))
    subsets=[U for r in (2,3) for U in combinations(range(M),r)]
    # Divide columns by their exact nonzero degree-1 coefficient for scaling only.
    scales=np.array([coeff(M,1,int(t)) for t in thresholds],dtype=float)
    assert np.all(scales!=0)
    L=np.array([[coeff(M,len(U),int(thresholds[j]))*int(np.prod(masks[j,list(U)]))/scales[j] for j in range(S)] for U in subsets])
    a=np.array([coeff(M,len(target),int(thresholds[j]))*int(np.prod(masks[j,list(target)]))/scales[j] for j in range(S)])
    q=len(subsets)
    fit=linprog(np.ones(2*q),A_eq=np.column_stack((L.T,-L.T)),b_eq=a,bounds=(0,None),method='highs')
    exact_cert = None
    if M == 12 and fit.status == 0:
        lamb = fit.x[:q]-fit.x[q:]
        support = np.flatnonzero(np.abs(lamb)>1e-8)
        chosen = [subsets[i] for i in support]
        nc = len(chosen)
        E = [[Q(coeff(M,len(U),int(thresholds[j]))*int(np.prod(masks[j,list(U)]))) for U in chosen]
             +[Q(coeff(M,len(target),int(thresholds[j]))*int(np.prod(masks[j,list(target)])))] for j in range(S)]
        rank,pivots=0,[]
        for c in range(nc):
            pivot=next((i for i in range(rank,len(E)) if E[i][c]),None)
            if pivot is None: continue
            E[rank],E[pivot]=E[pivot],E[rank]
            f=E[rank][c]
            E[rank]=[v/f for v in E[rank]]
            for i in range(rank+1,len(E)):
                f=E[i][c]
                if f: E[i]=[u-f*v for u,v in zip(E[i],E[rank])]
            pivots.append(c)
            rank+=1
        assert rank==nc
        exact=[Q(0)]*nc
        for i,c in reversed(list(enumerate(pivots))):
            exact[c]=E[i][-1]-sum(E[i][j]*exact[j] for j in range(c+1,nc))
        norm=sum(map(abs,exact))
        assert norm<1
        for j in range(S):
            lhs=sum(lam*coeff(M,len(U),int(thresholds[j]))*int(np.prod(masks[j,list(U)])) for U,lam in zip(chosen,exact))
            rhs=coeff(M,len(target),int(thresholds[j]))*int(np.prod(masks[j,list(target)]))
            assert lhs==rhs
        cert={"authors":"Christian Reitwiessner","status":"EXACT Fourier interpolation certificate", "M":M,"S":S,"masks":masks.tolist(),"thresholds_hamming_after_mask":thresholds.tolist(),"target":target,"subsets":chosen,"lambda":[str(x) for x in exact],"l1_norm":str(norm)}
        Path(__file__).with_name('fourier_certificate.json').write_text(json.dumps(cert,indent=2)+'\n')
        exact_cert={"support":nc,"l1_norm":str(norm)}
    results.append({"exact_certificate":exact_cert,"M":M,"S":S,"low_degree_rows":q,"LP_status":fit.status,"minimum_l1_numerical":None if fit.status else fit.fun})
out={"authors":"Christian Reitwiessner","status":"NUMERICAL diagnostics except the M12 EXACT certificate; no asymptotic theorem claimed", "seed":561832,"results":results}
Path(__file__).with_name('fourier_probe.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
