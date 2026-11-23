# Copyright (c) 2026 Christian Reitwiessner
# Authors: Christian Reitwiessner
"""Small symmetry-reduced mixed-window cover, exact rational verification."""
import sys
sys.path.insert(0,'/tmp/pydeps')
import numpy as np
from scipy.optimize import linprog
from itertools import product
from fractions import Fraction
import json
from pathlib import Path
from central_windows import window_gates,evaluate
A=list(product((0,1),repeat=8))
columns=[];descs=[]
for typ in [(1,1),(1,2),(2,2)]:
    masks=[z for z in A if tuple(sorted([min(sum(z[:4]),4-sum(z[:4])),min(sum(z[4:]),4-sum(z[4:]))]))==typ]
    for rad in range(4):
        p,q=4-rad,4+rad
        columns.append([sum(p<=sum(u!=v for u,v in zip(a,z))<=q for z in masks) for a in A])
        descs.append((typ,rad,masks))
lp=linprog(np.ones(len(columns)),A_eq=np.array(columns).T,b_eq=np.ones(256),bounds=(0,None),method='highs')
assert lp.success
terms=[(descs[i],Fraction(float(v)).limit_denominator(1000000)) for i,v in enumerate(lp.x) if v>1e-8]
assert all(sum(w*columns[i][j] for i,v in enumerate(lp.x) if v>1e-8 for w in [Fraction(float(v)).limit_denominator(1000000)])==1 for j in range(256))
gates=[]
for (typ,rad,masks),w in terms:
    for z in masks:
        if z[0]: continue  # one representative of each complementary pair
        for aw,xw,t,v in window_gates([4,4],z,4-rad,4+rad,[1,-1,1,-1],0,4):
            gates.append((aw,xw,t,2*w*v))
# Merge equal bottom functions via positive rescaling and drop zero top weights.
from math import gcd
merged={}
for aw,xw,t,w in gates:
    g=0
    for v in aw+xw+[t]:g=gcd(g,abs(v))
    key=tuple(v//g for v in aw+xw+[t])
    merged[key]=merged.get(key,0)+w
actual=[(list(key[:8]),list(key[8:12]),key[12],w) for key,w in merged.items() if w]
checks=0
for a in A:
    for x in product((0,1),repeat=4):
        target=(-1)**sum(a)*(2*int(x[0]-x[1]+x[2]-x[3]>=0)-1)
        assert evaluate(actual,a,x)==target
        checks+=1
out=dict(Authors='Christian Reitwiessner',terms=[dict(type=typ,radius=rad,masks=len(masks),weight=str(w)) for (typ,rad,masks),w in terms],unmerged_bottoms=len(gates),merged_bottoms=len(actual),total_with_top=len(actual)+1,exact_checks=checks,
         gates=[dict(address=aw,table=xw,cutoff=t,top=str(w)) for aw,xw,t,w in actual])
Path(__file__).with_name('symmetric_witness.json').write_text(json.dumps(out,indent=2)+'\n')
print({k:v for k,v in out.items() if k!='gates'})
