#!/usr/bin/env python3
# Copyright (c) 2026 Christian Reitwiessner
# Authors: Christian Reitwiessner
"""Independent integer certificate of the uniform all-m ordinary-Andreev bound."""
from pathlib import Path
from fractions import Fraction as F
import json,math
import engine as e
from constructions import atoms3
root=Path(__file__).resolve().parent;o=json.loads((root/'uniform_cancellation_results.json').read_text());atoms=atoms3();A=list(map(F,o['A']));C=list(map(F,o['C']));u=list(map(F,o['raw_table']));tau=F(o['tau']);scale=math.lcm(*(v.denominator for v in A+C+u+[tau]));A=[int(v*scale) for v in A];C=[int(v*scale) for v in C];u=[int(v*scale) for v in u];tau=int(tau*scale);margin=10**9
for mask in range(256):
 x=[mask>>c&1 for c in range(8)];H=[int(sum((-1)**((s&c).bit_count()%2)*x[c] for c in range(8))>=r) for s,r,w in atoms]
 for b in range(8):
  score=sum(v*z for v,z in zip(u,x))-tau+sum(a*((-1)**((s&b).bit_count()%2)*(2*h-1)+2*h)+c*h for (s,r,w),h,a,c in zip(atoms,H,A,C));margin=min(margin,(2*x[b]-1)*score)
assert margin>0
records=[]
for m,timeout in [(3,60000),(4,30000),(6,10000)]:
 p=root/('uniform_cancellation_m%d.json'%m);obj=json.loads(p.read_text());c=obj['candidate'];symbolic=e.independent.check(c,e.independent.andreev_target(3,m),timeout_ms=timeout);record=dict(m=m,bottoms=len(c['bottom']),independent_symbolic=symbolic);records.append(record);print(record,flush=True)
e.save(root/'uniform_integer_certificate.json',dict(atoms=[(s,r) for s,r,w in atoms],A=A,C=C,table=u,tau=tau,integer_scale=scale,exact_minimum=margin,cases=2048,formula='6 floor(m/2)+6m+floor(3m/2)+20 bottoms, for every m>=1',checks=records))
