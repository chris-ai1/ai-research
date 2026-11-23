#!/usr/bin/env python3
# Copyright (c) 2026 Christian Reitwiessner
# Authors: Christian Reitwiessner
import json,time
from pathlib import Path
import z3
import engine as e
from xag_encoding import canonical_generator,generator
from audit import tables
root=Path(__file__).resolve().parent;records=[]
for k,r in [(2,1),(3,1),(3,2),(4,1)]:
 valid,x,ev,decode=canonical_generator(k,r)
 for mask in tables(k,r):
  s=z3.Solver();s.add(*valid,*[v==bool(mask>>i&1) for i,v in enumerate(x)]);assert s.check()==z3.sat
  assert sum(v<<i for i,v in enumerate(e.concrete(decode(s.model()),k)))==mask
 print(dict(regression='canonical_coverage',k=k,r=r,tables=len(tables(k,r))),flush=True)
c=json.loads((root/'milp_k3m3full/verified_49.json').read_text())['candidate']
for name,gen in [('XAG',generator),('canonical_XAG',canonical_generator)]:
 e.generator=gen;t=time.monotonic();res=e.check(c,3,3,5,timeout=20000,batch=1);row=dict(basis=name,k=3,m=3,r=5,bottoms=49,result=res,wall_seconds=time.monotonic()-t);records.append(row);print(row,flush=True)
e.save(root/'canonical_benchmark.json',dict(results=records,coverage_regressions='all family tables at (2,1),(3,1),(3,2),(4,1)'))
