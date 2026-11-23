# Copyright (c) 2026 Christian Reitwiessner. All rights reserved.
# Authors: Christian Reitwiessner
"""Independent standard-library verifier for the saved unequal-magnitude dual."""
from fractions import Fraction
from itertools import product
from pathlib import Path
import json
base = Path(__file__).parent
c = json.loads((base/'unequal_certificate.json').read_text())
xs = list(product((0,1),repeat=4))
aas = list(product((0,1),repeat=4))
bs = [(a[0]^a[1])+2*(a[2]^a[3]) for a in aas]
W,T = c['weights_signed_inputs'],c['thresholds']
G = [[[int(sum(w*(2*v-1) for w,v in zip(row,x+a)) >= t)
       for row,t in zip(W,T)] for a in aas] for x in xs]
for j,row in enumerate(W):
    assert sorted(abs(v) for v in row[4:]) == [1,2,3,4]
    assert min(row[:4])<0<max(row[:4])
    assert min(row[4:])<0<max(row[4:])
    for i in range(4):
        assert any(G[p][a][j]!=G[p][a^(1<<(3-i))][j]
                   for p in range(16) for a in range(16))
    p,a,b = c['semantic_witnesses'][j]
    count = lambda a: sum(v if w>0 else 1-v for v,w in zip(aas[a],row[4:]))
    assert count(a)==count(b) and G[p][a][j]!=G[p][b][j]

weights = [Fraction(s) for s in c['certificate_weights']]
assert all(w>0 for w in weights) and sum(weights)==1
acc = [Fraction(0)]*(len(W)+9)
for wt,(p,q,a,b) in zip(weights,c['selected_rectangles']):
    assert xs[p][bs[a]] == 1 and xs[q][bs[a]] == 0
    assert xs[p][bs[b]] == 0 and xs[q][bs[b]] == 1
    vertices = [(p,a,1),(q,a,-1),(p,b,-1),(q,b,1)]
    for xidx,aidx,sign in vertices:
        features = [1]+list(xs[xidx]+aas[aidx])+G[xidx][aidx]
        for j,v in enumerate(features): acc[j]+=wt*sign*v
assert all(v==0 for v in acc)

oriented=ordinary=0
min_witnesses=len(W)
for p in range(16):
    for q in range(p):
        for a in range(16):
            for b in range(16):
                row=[G[p][a][j]-G[q][a][j]-G[p][b][j]+G[q][b][j] for j in range(len(W))]
                if xs[p][bs[a]]>xs[q][bs[a]] and xs[p][bs[b]]<xs[q][bs[b]]:
                    assert any(row); oriented+=1
                if a<b and (a^b).bit_count()==1:
                    n=sum(v!=0 for v in row)
                    assert n>0; ordinary+=1; min_witnesses=min(min_witnesses,n)
assert oriented==c['rectangles']==1536
assert ordinary==c['ordinary_rectangles']==3840
assert min_witnesses==c['minimum_ordinary_witnesses']==4
out={'authors':'Christian Reitwiessner','status':'VERIFIED EXACT',
     'signed_feature_equations':len(acc),'positive_rational_rectangle_weights':len(weights),
     'oriented_rows_checked':oriented,'ordinary_rows_checked':ordinary,
     'minimum_ordinary_witnesses':min_witnesses,'semantic_exclusions':len(W)}
(base/'certificate_verification.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
