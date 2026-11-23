#!/usr/bin/env python3
# Copyright (c) 2026 Christian Reitwiessner
# Authors: Christian Reitwiessner
"""Coverage/evaluator regressions and known-witness checks, with exact results."""
import itertools, random
from pathlib import Path
import engine as e
from audit import tables,exhaustive
import z3
results=[]
for k,expected in [(2,16),(3,38),(4,70)]:
 ts=tables(k,1);assert len(ts)==expected
 valid,x,ev,decode=e.generator(k,1)
 for mask in ts:
  so=z3.Solver();so.add(*valid,*[v==bool(mask>>i&1) for i,v in enumerate(x)]);assert so.check()==z3.sat
  d=decode(so.model());assert sum(v<<i for i,v in enumerate(e.concrete(d,k)))==mask
 results.append(dict(test='one_LUT_coverage',k=k,count=len(ts)))
ts=tables(3,2);assert len(ts)==152
# Full coverage at k=3,r=5 by Shannon combination of two binary LUTs.
for mask in range(256):
 d=dict(gates=[dict(p=2,q=3,lut=[mask>>i&1 for i in range(4)]),dict(p=2,q=3,lut=[mask>>(i+4)&1 for i in range(4)]),dict(p=5,q=6,lut=[0,1,1,0]),dict(p=4,q=7,lut=[0,0,0,1]),dict(p=5,q=8,lut=[0,1,1,0])],output=9)
 assert sum(v<<i for i,v in enumerate(e.concrete(d,3)))==mask
results.append(dict(test='Shannon_full_coverage',k=3,r=5,count=256))
for k,m in [(2,3),(2,4),(2,6),(2,8),(3,3)]:
 c=e.library(k,m);full=e.independent.check(c,e.independent.andreev_target(k,m),timeout_ms=3000);finite=exhaustive(c,k,m,range(1<<(1<<k)));assert finite['status']=='VERIFIED';family=e.check(c,k,m,1,timeout=3000,batch=1);assert family['status']!='SAT'
 results.append(dict(test='inherited_witness',k=k,m=m,bottoms=len(c['bottom']),ordinary_symbolic=full,ordinary_exact=finite,family_symbolic=family))
# Threshold ties belong to output 1; non-integral exact coefficients retained.
c=dict(bottom=[(['1/2'], '1/2')],v=['2/3'],u=[0],tau='2/3')
assert e.independent.check(c,lambda bits:bits[0])['status']=='VERIFIED'
results.append(dict(test='rational_ties',status='VERIFIED'))
e.save(Path(__file__).with_name('regression_results.json'),dict(results=results));print(results)
