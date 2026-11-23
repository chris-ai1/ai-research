#!/usr/bin/env python3
# Copyright (c) 2026 Christian Reitwiessner
# Authors: Christian Reitwiessner
"""Independent finite integer audit; exhaustive address counts only after symmetry proof."""
import itertools, json, sys, math
from pathlib import Path
from fractions import Fraction as F
import engine as e

def tables(k,r):
 N=1<<k;mask=(1<<N)-1;inputs=[0,mask]+[sum(((c>>i)&1)<<c for c in range(N)) for i in range(k)]
 states=[(inputs,[])];out={v:dict(gates=[],output=i) for i,v in enumerate(inputs)}
 for j in range(r):
  new=[]
  for vals,gs in states:
   distinct={}
   for p,a in enumerate(vals):
    for q,b in enumerate(vals):
     cells=[(a if t&1 else a^mask)&(b if t&2 else b^mask) for t in range(4)]
     for lut in range(16):
      v=0
      for t in range(4):
       if lut>>t&1:v|=cells[t]
      distinct.setdefault(v,dict(p=p,q=q,lut=[lut>>t&1 for t in range(4)]))
   for v,g in distinct.items():
    desc=dict(gates=gs+[g],output=len(vals));out.setdefault(v,desc)
    if j+1<r:new.append((vals+[v],gs+[g]))
  states=new
 return out

def exhaustive(c,k,m,tabs):
 N=1<<k
 rows=[(list(map(F,w)),F(t)) for w,t in c['bottom']];u=list(map(F,c['u']));v=list(map(F,c['v']));tau=F(c['tau'])
 # Prove that counts cover every raw arrangement, instead of assuming it.
 for w in [w for w,t in rows]+[u]:
  for i in range(k):assert len(set(w[N+i*m:N+(i+1)*m]))==1
 scale=math.lcm(*[q.denominator for w,t in rows for q in w+[t]],*[q.denominator for q in u+v+[tau]])
 rows=[([int(q*scale) for q in w],int(t*scale)) for w,t in rows];u=[int(q*scale) for q in u];v=[int(q*scale) for q in v];tau=int(tau*scale)
 counts=list(itertools.product(range(m+1),repeat=k));points=0
 for mask in tabs:
  x=[mask>>c&1 for c in range(N)];base=sum(q*z for q,z in zip(u,x));hs=[sum(q*z for q,z in zip(w,x)) for w,t in rows]
  for ss in counts:
   score=base+sum(u[N+i*m]*ss[i] for i in range(k))+sum(vj for vj,h,(w,t) in zip(v,hs,rows) if h+sum(w[N+i*m]*ss[i] for i in range(k))>=t)
   y=x[sum((s%2)<<i for i,s in enumerate(ss))];points+=1
   if (score>=tau)!=bool(y):return dict(status='COUNTEREXAMPLE',table=mask,counts=ss,points=points)
 return dict(status='VERIFIED',count_cases=points,raw_cases=len(tabs)*(1<<(k*m)),integer_scale=scale)

if __name__=='__main__':
 root=Path(__file__).resolve().parent;results=[]
 families={}
 for d in sorted(root.iterdir()):
  if not d.is_dir():continue
  files=list(d.glob('verified_*.json'))
  if not files:continue
  p=min(files,key=lambda p:int(p.stem.split('_')[1]));obj=json.loads(p.read_text());k,m,r=obj['k'],obj['m'],obj['r'];c=obj['candidate']
  if r>=0:
   if (k,r) not in families:families[k,r]=tables(k,r)
   
   try:fam=exhaustive(c,k,m,families[k,r])
   except AssertionError:fam=dict(status='NOT_COUNT_SYMMETRIC',exact_matrix=obj.get('exact_matrix'))
  else:fam=None
  
  try:full=exhaustive(c,k,m,range(1<<(1<<k))) if k<=3 else None
  except AssertionError:full=dict(status='NOT_COUNT_SYMMETRIC',exact_matrix=obj.get('exact_matrix'))
  record=dict(path=str(p.relative_to(root)),k=k,m=m,r=r,bottoms=len(c['bottom']),family_tables=len(families[k,r]) if r>=0 else None,family_exact=fam,ordinary_exact=full,ordinary_symbolic=e.independent.check(c,e.independent.andreev_target(k,m),timeout_ms=3000))
  print(json.dumps(record),flush=True);results.append(record)
 e.save(root/'audit_results.json',dict(results=results))
