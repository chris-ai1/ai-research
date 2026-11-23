# Copyright (c) 2026 Christian Reitwiessner
# Authors: Christian Reitwiessner
"""Bounded nonnegative covering LP; rational certificates checked exactly."""
import sys
sys.path.insert(0,'/tmp/pydeps')
import numpy as np
from scipy.optimize import linprog
from itertools import product
from fractions import Fraction
import json
from pathlib import Path

results=[]
for blocks in [(3,3),(4,4),(2,2,2),(2,2,2,2)]:
    M=sum(blocks)
    addresses=list(product((0,1),repeat=M))
    masks=[]
    for z in addresses:
        if z[0]: continue  # symmetric windows identify complementary masks
        offset=0;good=True
        for length in blocks:
            if len(set(z[offset:offset+length]))!=2: good=False
            offset+=length
        if good:masks.append(z)
    columns=[];descriptions=[]
    for z in masks:
        distances=[sum(u!=v for u,v in zip(a,z)) for a in addresses]
        for radius in range(M//2):
            p,q=M//2-radius,M//2+radius
            columns.append([int(p<=d<=q) for d in distances])
            descriptions.append((z,p,q))
    mat=np.array(columns,dtype=float).T
    # Mass is a diagnostic objective, not the number of nonzero gates.
    lp=linprog(np.ones(len(columns)),A_eq=mat,b_eq=np.ones(len(addresses)),bounds=(0,None),method='highs')
    item=dict(blocks=blocks,candidates=len(columns),status=lp.message)
    if lp.success:
        terms=[(descriptions[i],Fraction(float(v)).limit_denominator(1000000)) for i,v in enumerate(lp.x) if v>1e-8]
        assert all(sum(w*int(p<=sum(u!=v for u,v in zip(a,z))<=q) for (z,p,q),w in terms)==1 for a in addresses)
        item.update(verified=True,windows=len(terms),unmerged_bottom_bound=sum(q-p+3 for (z,p,q),w in terms),
                    witness=[dict(mask=z,p=p,q=q,weight=str(w)) for (z,p,q),w in terms])
    results.append(item)
Path(__file__).with_name('cover_results.json').write_text(json.dumps(dict(Authors='Christian Reitwiessner',results=results),indent=2)+'\n')
for r in results:print({k:v for k,v in r.items() if k!='witness'})
