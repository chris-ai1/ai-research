#!/usr/bin/env python3
# Copyright (c) 2026 Christian Reitwiessner
# Authors: Christian Reitwiessner
"""Equivalent r>=1 complemented-edge AND/XOR generator; commutative pin symmetry."""
import time,json
from pathlib import Path
import engine as e
import z3

def generator(k,r):
 assert r>=1,'r=0 differs: signed input selection includes negated projections'
 # Literal 2*i is source i; literal 2*i+1 is its complement. Source 0=false.
 pins=[(z3.Int('xp%d'%j),z3.Int('xq%d'%j)) for j in range(r)];ops=[z3.Bool('xor%d'%j) for j in range(r)];out=z3.Int('xout');valid=[out>=0,out<2*(k+1+r)]
 for j,(p,q) in enumerate(pins):valid += [p>=0,p<=q,q<2*(k+1+j)]
 def select(lit,vals):
  return z3.Or([z3.And(lit==2*i,v) for i,v in enumerate(vals)]+[z3.And(lit==2*i+1,z3.Not(v)) for i,v in enumerate(vals)])
 def ev(inputs):
  vals=[z3.BoolVal(False)]+list(inputs)
  for (p,q),op in zip(pins,ops):
   a,b=select(p,vals),select(q,vals);vals.append(z3.If(op,z3.Xor(a,b),z3.And(a,b)))
  return select(out,vals)
 x=[ev([z3.BoolVal(bool(c>>i&1)) for i in range(k)]) for c in range(1<<k)]
 def decode(model):
  return dict(basis='complemented_AND_XOR',gates=[dict(p=model.eval(p).as_long(),q=model.eval(q).as_long(),xor=z3.is_true(model.eval(op,model_completion=True))) for (p,q),op in zip(pins,ops)],output=model.eval(out).as_long())
 return valid,x,ev,decode

def canonical_generator(k,r):
 valid,x,ev,decode=generator(k,r)
 valid.append(z3.Int('xout')>=2*(k+r)) # output is last node; preserve output polarity
 for j in range(r-1):
  source=k+1+j
  valid.append(z3.Or([z3.And(lit>=2*source,lit<=2*source+1) for h in range(j+1,r) for lit in (z3.Int('xp%d'%h),z3.Int('xq%d'%h))]))
 return valid,x,ev,decode

def all_tables(k,r):
 N=1<<k;mask=(1<<N)-1;ins=[0]+[sum(((c>>i)&1)<<c for c in range(N)) for i in range(k)];states=[ins];result=set()
 for j in range(r):
  new=[]
  for vals in states:
   lits=[v for a in vals for v in (a,a^mask)];result.update(lits);made={a&b for i,a in enumerate(lits) for b in lits[i:]}|{a^b for i,a in enumerate(lits) for b in lits[i:]}
   for v in made:
    result.update((v,v^mask))
    if j+1<r:new.append(vals+[v])
  states=new
 return result

if __name__=='__main__':
 from audit import tables
 for k,r in [(2,1),(3,1),(3,2),(4,1)]:assert all_tables(k,r)==set(tables(k,r))
 root=Path(__file__).resolve().parent;baseline=e.generator;records=[]
 cases=[(e.library(3,3),3,3,2,'inherited54'),(e.library(3,3),3,3,5,'inherited54'),(json.loads((root/'milp_k3m3full/verified_49.json').read_text())['candidate'],3,3,5,'new49')]
 for c,k,m,r,name in cases:
  for basis,gen in [('LUT',baseline),('XAG',generator)]:
   e.generator=gen;t=time.monotonic();res=e.check(c,k,m,r,timeout=20000,batch=1);record=dict(candidate=name,k=k,m=m,r=r,basis=basis,wall_seconds=time.monotonic()-t,result=res);records.append(record);print(record,flush=True)
 e.generator=baseline;e.save(root/'xag_benchmark.json',dict(results=records,coverage_regressions='exact set equality at (2,1),(3,1),(3,2),(4,1)'))
