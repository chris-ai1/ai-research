# Copyright (c) 2026 Christian Reitwiessner.
# Authors: Christian Reitwiessner
"""Independent exact verification of the saved profile dual."""
import json
from itertools import product
from pathlib import Path
root = Path(__file__).resolve().parent
c = json.loads((root / 'profile_dual_certificate.json').read_text())
k,m,G,R = (c[x] for x in ['k','m','G','R'])
N,M = 1 << k,k*m
assert c['L'] == len(c['pairs']) >= 2
assert 2*c['B'] < c['D']+1
masks = {}
for g in c['gates'][:G]:
    U = g['profile']
    a,b = g['scales']
    assert all(g['address'][q] == g['mask'][q]*(a if (U >> (q//m))&1 else b) for q in range(M))
    if a != b:
        key = min(U,U^((1<<k)-1))
        masks.setdefault(key,set()).add(tuple(g['mask']))
assert all(len(v) <= R for v in masks.values())
# Every nonexceptional gate loses a live coefficient, independently of offsets.
for g in c['gates'][1:G]:
    assert any(g['address'][u]+sign*g['address'][v] == 0
               for (u,v),sign in zip(c['pairs'],c['literal_signs']))
plus = [(1+(-1)**((x&c['target']).bit_count()))//2 for x in range(N)]
minus = [1-x for x in plus]
sums = [0]*(len(c['gates'])+N+M+1)
rows = [0]*len(c['gates'])
values = {}
constancy = [set(),set()]
for z in product([0,1],repeat=c['L']):
    address = c['fixed'].copy()
    for (u,v),sign,bit in zip(c['pairs'],c['literal_signs'],z):
        address[u] = bit
        address[v] = bit if sign == 1 else 1-bit
    label = sum((sum(address[i*m:(i+1)*m])%2)<<i for i in range(k))
    scores = []
    for ti,table in enumerate([plus,minus]):
        outputs = [int(sum(a*x for a,x in zip(g['table'],table))+
                       sum(a*x for a,x in zip(g['address'],address)) >= g['threshold'])
                   for g in c['gates']]
        target = 2*table[label]-1
        for i,f in enumerate(outputs+table+address+[1]):
            sums[i] += target*f
        scores.append(outputs)
        constancy[ti].add(outputs[0])
    values[z] = (2*plus[label]-1,scores)
assert not any(sums)
assert all(len(s)==1 for s in constancy)
nonzero = 0
for z,(sign,scores) in values.items():
    if sign == -1:
        continue
    zz = (1-z[0],)+z[1:]
    sign2,scores2 = values[zz]
    assert sign2 == -1
    row = [a-b-aa+bb for a,b,aa,bb in zip(*scores,*scores2)]
    rows = [a+b for a,b in zip(rows,row)]
    nonzero += any(row)
assert not any(rows)
result = {'authors':['Christian Reitwiessner'],'status':'VERIFIED EXACT',
          'input_count':2**(c['L']+1),'feature_equations':len(sums),
          'positive_rectangle_rows':2**(c['L']-1),'nonzero_rectangle_rows':nonzero,
          'model_mask_cap':R,'unrestricted_pure_address_helpers':3,
          'pure_table_helpers':2}
(root/'certificate_verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,sort_keys=True))
