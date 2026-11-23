# Copyright (c) 2026 Christian Reitwiessner. All rights reserved.
# Authors: Christian Reitwiessner
"""Find then exactly verify an oriented-rectangle dual for unequal address rows.

Uses the round-one LOW2 oriented-cone method, now outside its full-sign class.
Numerical LP is discovery only. Certificate verification uses rational arithmetic.
"""
import sys
sys.path.insert(0, '/tmp/andreev_gap/coherence_fable/pydeps_local')
import numpy as np
from scipy.optimize import linprog
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import json
import random

base = Path(__file__).parent
xs = np.array(list(product((0,1),repeat=4)),dtype=int)
aas = np.array(list(product((0,1),repeat=4)),dtype=int)
labels = np.array([(a[0]^a[1])+2*(a[2]^a[3]) for a in aas])
inputs = np.array([list(x)+list(a) for x in xs for a in aas],dtype=int)
rects = []
for p in range(len(xs)):
    for q in range(p):
        delta = xs[p,labels]-xs[q,labels]
        for a in np.flatnonzero(delta>0):
            for b in np.flatnonzero(delta<0):
                rects.append((p,q,int(a),int(b)))

rng = random.Random(110112026)
W,T = [],[]
for j in range(48):
    adr = list(range(1,5)); rng.shuffle(adr)
    row = [rng.randint(1,5)*rng.choice((-1,1)) for _ in range(4)]
    row += [v*rng.choice((-1,1)) for v in adr]
    # Require genuinely mixed table signs and address signs.
    if min(row[:4])>0: row[0]*=-1
    if max(row[:4])<0: row[0]*=-1
    if min(row[4:])>0: row[4]*=-1
    if max(row[4:])<0: row[4]*=-1
    W.append(row); T.append(rng.choice((-1,0,1)))
W = np.array(W,dtype=int); T = np.array(T,dtype=int)
G = (((2*inputs-1)@W.T)>=T).astype(int).reshape((16,16,len(W)))
R = np.array([G[p,a]-G[q,a]-G[p,b]+G[q,b] for p,q,a,b in rects],dtype=int)
nonzero = int(np.count_nonzero(np.any(R!=0,axis=1)))
assert nonzero == len(rects), (nonzero,len(rects))
# Exact all-table-pair / ordinary-address-edge coverage.
coverage = []
for p in range(16):
    for q in range(p):
        for a in range(16):
            for i in range(4):
                b = a^(1<<i)
                if a < b:
                    row = G[p,a]-G[q,a]-G[p,b]+G[q,b]
                    coverage.append(int(np.count_nonzero(row)))
assert min(coverage)>0

# Exclude semantic full equal-magnitude address representations gate by gate.
semantic_witnesses = []
for j,row in enumerate(W):
    essential = []
    for i in range(4):
        # product-order address index changes bit 3-i.
        essential.append(any(G[p,a,j] != G[p,a^(1<<(3-i)),j]
                             for p in range(16) for a in range(16)))
    assert all(essential)
    counts = np.sum(aas*(row[4:]>0)+(1-aas)*(row[4:]<0),axis=1)
    wit = next(((p,a,b) for p in range(16) for a in range(16) for b in range(a)
                if counts[a]==counts[b] and G[p,a,j]!=G[p,b,j]),None)
    assert wit is not None
    semantic_witnesses.append(list(wit))

sol = linprog(np.zeros(len(R)), A_eq=np.vstack((R.T,np.ones(len(R)))),
              b_eq=np.r_[np.zeros(len(W)),1],bounds=(0,None),method='highs')
assert sol.status==0, sol.message
support = np.flatnonzero(sol.x>1e-8)
B = R[support]
nc = len(support)
eq = [[Q(int(B[i,j])) for i in range(nc)]+[Q(0)] for j in range(len(W))]
eq.append([Q(1)]*nc+[Q(1)])
rank,pivots=0,[]
for c in range(nc):
    pivot=next((i for i in range(rank,len(eq)) if eq[i][c]),None)
    if pivot is None: continue
    eq[rank],eq[pivot]=eq[pivot],eq[rank]
    f=eq[rank][c]; eq[rank]=[v/f for v in eq[rank]]
    for i in range(rank+1,len(eq)):
        f=eq[i][c]
        if f: eq[i]=[u-f*v for u,v in zip(eq[i],eq[rank])]
    pivots.append(c); rank+=1
assert rank==nc
weights=[Q(0)]*nc
for i,c in reversed(list(enumerate(pivots))):
    weights[c]=eq[i][-1]-sum(eq[i][j]*weights[j] for j in range(c+1,nc))
assert all(w>0 for w in weights) and sum(weights)==1
assert all(sum(weights[i]*int(B[i,j]) for i in range(nc))==0 for j in range(len(W)))

out={'authors':'Christian Reitwiessner','status':'VERIFIED EXACT FINITE',
     'method_attribution':'Round-one LOW2 oriented-rectangle cone method',
     'k':2,'m':2,'gates':len(W),'weights_signed_inputs':W.tolist(),'thresholds':T.tolist(),
     'rectangles':len(rects),'all_oriented_rows_nonzero':True,
     'ordinary_rectangles':len(coverage),'minimum_ordinary_witnesses':min(coverage),
     'all_address_magnitudes_distinct':True,
     'no_gate_semantically_full_sign':True,'semantic_witnesses':semantic_witnesses,
     'support_rectangles':nc,'selected_rectangles':[rects[i] for i in support],
     'certificate_weights':[str(w) for w in weights]}
(base/'unequal_certificate.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in
    ('weights_signed_inputs','thresholds','semantic_witnesses','selected_rectangles','certificate_weights')},indent=2))
