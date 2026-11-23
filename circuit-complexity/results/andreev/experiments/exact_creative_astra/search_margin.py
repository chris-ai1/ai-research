# Copyright (c) 2026 Christian Reitwiessner
# Authors: Christian Reitwiessner
"""Bounded sign-margin search over explicit monochromatic hyperplanes."""
import sys
sys.path.insert(0,'/tmp/pydeps')
import numpy as np
from itertools import product,permutations
from scipy.optimize import linprog
from scipy.sparse import csr_matrix
from fractions import Fraction
from pathlib import Path
import json
OUT=Path(__file__).resolve().parent
k=3;m=3;N=8;d=9
A=np.array(list(product((0,1),repeat=d)),dtype=np.int64)
B=np.array([sum((sum(a[i*m:(i+1)*m])%2)<<i for i in range(k)) for a in A])
features=[];zeros=[];meta=[]
for c in range(N):
 for t in range(4):
  e=np.array([[t&1,t>>1,((c>>i)&1)^(t&1)^(t>>1)] for i in range(k)])
  D=np.array([np.abs(A[:,i*m:(i+1)*m]-e[i]).sum(axis=1)-2 for i in range(k)]).T
  seen=set()
  for perm,sgn in product(permutations(range(k)),product((-1,1),repeat=k)):
   q=np.zeros(k,dtype=np.int64)
   for pos,idx in enumerate(perm):q[idx]=sgn[idx]*3**pos
   L=D@q;E=L>=1;Z=L==0
   key=E.tobytes()
   if key in seen:continue
   seen.add(key)
   assert np.all(B[Z]==c)
   features.append(E);zeros.append(Z)
   wa=np.concatenate([q[i]*(1-2*e[i]) for i in range(k)])
   const=sum(int(q[i])*(int(e[i].sum())-2) for i in range(k))
   assert np.array_equal(L,A@wa+const)
   meta.append({'c':c,'t':t,'address_weights':wa.tolist(),'threshold':int(1-const)})
E=np.stack(features,axis=1).astype(np.int64);Z=np.stack(zeros,axis=1).astype(np.int64)
F=np.concatenate([A,np.ones((len(A),1),dtype=np.int64)],axis=1)
C=np.concatenate([np.concatenate([E,F],axis=1),-np.concatenate([E+Z,F],axis=1)],axis=0)
H=len(meta);obj=np.ones(H);best=10**9;out=[]
for it in range(6):
 r=linprog(np.r_[obj,np.zeros(d+1)],A_ub=csr_matrix(C),b_ub=-np.ones(len(C)),bounds=[(0,None)]*H+[(None,None)]*(d+1),method='highs',options={'time_limit':20})
 record={'iteration':it,'status':int(r.status),'message':r.message}
 if r.success:
  fr=[Fraction(float(x)).limit_denominator(10**6) for x in r.x]
  ids=[j for j in range(H) if fr[j]>0]
  # Exact Fraction checking only on the support.
  cs=C[:,ids+list(range(H,H+d+1))]
  vv=[fr[j] for j in ids+list(range(H,H+d+1))]
  mx=max(sum(int(a)*v for a,v in zip(row,vv)) for row in cs)
  record.update(bottoms=len(ids),exact_max_constraint=str(mx),verified=bool(mx<0))
  if mx<0 and len(ids)<best:
   best=len(ids)
   witness={'Authors':'Christian Reitwiessner','copyright':'Copyright (c) 2026 Christian Reitwiessner','k':k,'m':m,'gates':[dict(meta[j],table_weight=1,top_weight=str(fr[j])) for j in ids],'top_raw_address':[str(v) for v in fr[H:H+d]],'top_constant':str(fr[-1]),'verified_margin':str(-mx)}
   (OUT/'margin_witness.json').write_text(json.dumps(witness,indent=2)+'\n')
  obj=1/(np.maximum(r.x[:H],0)+.1)
 print(json.dumps(record),flush=True);out.append(record)
 (OUT/'margin_search_results.json').write_text(json.dumps({'Authors':'Christian Reitwiessner','runs':out},indent=2)+'\n')
 if not r.success:break
