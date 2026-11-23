# Copyright (c) 2026 Christian Reitwiessner. All rights reserved.
# Authors: Christian Reitwiessner
"""Recover and check the selected dual using exact rational arithmetic only."""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import json
base = Path(__file__).parent
candidate = json.loads((base/'dual_candidate.json').read_text())
k, m = candidate['k'], candidate['m']
N = 2**k
xs = list(product((0, 1), repeat=N))
as_ = list(product((0, 1), repeat=k*m))
bs = [sum((sum(a[i*m:(i+1)*m]) % 2) << i for i in range(k)) for a in as_]
inputs = [x+a for x in xs for a in as_]
labels = [2*x[b]-1 for x in xs for b in bs]
W, T = candidate['weights_signed_inputs'], candidate['thresholds']
G = [[int(sum(w*(2*z-1) for w,z in zip(ws, inp)) >= t) for ws,t in zip(W,T)] for inp in inputs]
Phi = [[1]+list(inp)+g for inp,g in zip(inputs,G)]
supp = candidate['support_input_indices']
B = [[labels[i]*v for v in Phi[i]] for i in supp]
cols = len(supp)
rows = [[Q(B[i][j]) for i in range(cols)]+[Q(0)] for j in range(len(B[0]))]
rows.append([Q(1)]*cols+[Q(1)])
pivots = []
r = 0
for c in range(cols):
    pivot = next((i for i in range(r,len(rows)) if rows[i][c]), None)
    if pivot is None:
        continue
    rows[r],rows[pivot] = rows[pivot],rows[r]
    p = rows[r][c]
    rows[r] = [v/p for v in rows[r]]
    for i in range(r+1,len(rows)):
        f = rows[i][c]
        if f:
            rows[i] = [u-f*v for u,v in zip(rows[i],rows[r])]
    pivots.append(c)
    r += 1
assert r == cols, ('nonunique support',r,cols)
assert all(any(row[:-1]) or row[-1] == 0 for row in rows)
mu = [Q(0)]*cols
for i,c in reversed(list(enumerate(pivots))):
    mu[c] = rows[i][-1] - sum(rows[i][j]*mu[j] for j in range(c+1,cols))
assert all(v > 0 for v in mu)
assert sum(mu) == 1
assert all(sum(mu[i]*B[i][j] for i in range(cols)) == 0 for j in range(len(B[0])))

# Exhaust every table-pair / two-address rectangle obstruction.
rectangles = 0
na = len(as_)
for p in range(len(xs)):
    for q in range(p):
        signs = [xs[p][b]-xs[q][b] for b in bs]
        diffs = [tuple(u-v for u,v in zip(G[p*na+i],G[q*na+i])) for i in range(na)]
        pos = {d for d,s in zip(diffs,signs) if s>0}
        neg = {d for d,s in zip(diffs,signs) if s<0}
        rectangles += len(pos & neg)
assert rectangles == 0
out = {"authors":"Christian Reitwiessner", "status":"PROVED finite certificate, exact rational checks", "k":k,"m":m,"bottoms":len(W),"support":len(supp),"all_table_pair_rectangles":rectangles,"weights_signed_inputs":W,"thresholds":T,"support_input_indices":supp,"mu":[str(v) for v in mu]}
(base/'dual_certificate.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({key:out[key] for key in ('status','bottoms','support','all_table_pair_rectangles')},indent=2))
