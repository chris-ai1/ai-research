# Copyright (c) 2026 Christian Reitwiessner. All rights reserved.
# Authors: Christian Reitwiessner
"""Exact positive dependence among correctly oriented table/address rectangles."""
import sys
sys.path.insert(0, '/tmp/andreev_gap/coherence_fable/pydeps_local')
import numpy as np
from scipy.optimize import linprog
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import json
base = Path(__file__).parent
candidate = json.loads((base/'dual_candidate.json').read_text())
k,m = candidate['k'], candidate['m']
N = 2**k
xs = np.array(list(product((0,1),repeat=N)),dtype=int)
addresses = np.array(list(product((0,1),repeat=k*m)),dtype=int)
bs = np.array([sum((sum(a[i*m:(i+1)*m])%2)<<i for i in range(k)) for a in addresses])
inputs = np.array([list(x)+list(a) for x in xs for a in addresses],dtype=int)
W,T = np.array(candidate['weights_signed_inputs']),np.array(candidate['thresholds'])
G = (((2*inputs-1)@W.T)>=T).astype(int).reshape((len(xs),len(addresses),len(W)))
rectangles, rows = [],[]
for p in range(len(xs)):
    for q in range(p):
        delta = xs[p,bs]-xs[q,bs]
        for a in np.flatnonzero(delta>0):
            for b in np.flatnonzero(delta<0):
                rectangles.append([p,q,int(a),int(b)])
                rows.append(G[p,a]-G[q,a]-G[p,b]+G[q,b])
R = np.array(rows,dtype=int)
assert np.all(np.any(R != 0,axis=1))
primal = linprog(np.zeros(len(W)),A_ub=-R,b_ub=-np.ones(len(R)),bounds=[(None,None)]*len(W),method='highs')
output = {"authors":"Christian Reitwiessner","rectangles":len(R),"gates":len(W),"primal_status":primal.status}
if primal.status == 2:
    dual=linprog(np.zeros(len(R)),A_eq=np.vstack((R.T,np.ones(len(R)))),b_eq=np.r_[np.zeros(len(W)),1],bounds=(0,None),method='highs')
    assert dual.status==0
    support=np.flatnonzero(dual.x>1e-8)
    B=R[support]
    nc=len(support)
    equations=[[Q(int(B[i,j])) for i in range(nc)]+[Q(0)] for j in range(len(W))]
    equations.append([Q(1)]*nc+[Q(1)])
    rank,pivots=0,[]
    for c in range(nc):
        pivot=next((i for i in range(rank,len(equations)) if equations[i][c]),None)
        if pivot is None: continue
        equations[rank],equations[pivot]=equations[pivot],equations[rank]
        f=equations[rank][c]
        equations[rank]=[v/f for v in equations[rank]]
        for i in range(rank+1,len(equations)):
            f=equations[i][c]
            if f: equations[i]=[u-f*v for u,v in zip(equations[i],equations[rank])]
        pivots.append(c)
        rank+=1
    assert rank==nc
    weights=[Q(0)]*nc
    for i,c in reversed(list(enumerate(pivots))):
        weights[c]=equations[i][-1]-sum(equations[i][j]*weights[j] for j in range(c+1,nc))
    assert all(w>0 for w in weights) and sum(weights)==1
    assert all(sum(weights[i]*int(B[i,j]) for i in range(nc))==0 for j in range(len(W)))
    output.update({"exact_certificate":True,"support_rectangles":nc,"selected_rectangles":[rectangles[i] for i in support],"weights":[str(w) for w in weights]})
(base/'oriented_certificate.json').write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps({key:val for key,val in output.items() if key not in ('selected_rectangles','weights')},indent=2))
