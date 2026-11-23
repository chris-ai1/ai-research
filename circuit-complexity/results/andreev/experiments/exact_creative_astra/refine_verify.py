# Copyright (c) 2026 Christian Reitwiessner
# Authors: Christian Reitwiessner
"""Simplify fixed supports, then independently check every raw input with integers."""
import sys
sys.path.insert(0,'/tmp/pydeps')
import numpy as np
from scipy.optimize import milp, Bounds, LinearConstraint
from scipy.sparse import csc_matrix
from pathlib import Path
from itertools import product
import json
OUT=Path(__file__).resolve().parent
results=[]
for m in (3,4):
 w=json.loads((OUT/('sparse_witness_m%d.json'%m)).read_text())
 k=w['k'];N=1<<k;d=k*m;gs=w['gates'];H=len(gs)
 A=np.array(list(product((0,1),repeat=d)),dtype=np.int64)
 B=np.array([sum((sum(a[i*m:(i+1)*m])%2)<<i for i in range(k)) for a in A])
 WA=np.array([g['address_weights'] for g in gs],dtype=np.int64)
 TH=np.array([g['threshold'] for g in gs],dtype=np.int64)
 L=A@WA.T-TH
 E=(L>=0).astype(np.int64);Z=(L==-1).astype(np.int64)
 for j,g in enumerate(gs):assert np.all(B[Z[:,j].astype(bool)]==g['c'])
 F=np.c_[A,np.ones(len(A),dtype=np.int64)]
 C=np.r_[np.c_[E,F],-np.c_[E+Z,F]]
 r=milp(np.r_[np.ones(H),np.zeros(d+1)],integrality=np.ones(H+d+1),bounds=Bounds(np.r_[np.ones(H),-np.full(d+1,np.inf)],np.full(H+d+1,np.inf)),constraints=LinearConstraint(csc_matrix(C.astype(float)),-np.inf,-np.ones(len(C))),options={'time_limit':12})
 result={'m':m,'simplification_status':int(r.status),'simplification_message':r.message}
 if r.x is not None:
  v=np.rint(r.x).astype(np.int64)
  if np.max(C@v)<=-1:
   for j,g in enumerate(gs):g['top_weight']=int(v[j])
   w['top_raw_address']=v[H:H+d].tolist();w['top_constant']=int(v[-1])
 weights=np.array([g['top_weight'] for g in gs],dtype=np.int64)
 raw=np.array(w['top_raw_address'],dtype=np.int64)
 base=A@raw+w['top_constant']
 margin=10**20;count=0
 # This check does not use the monochromatic-plane reduction.
 for xt in product((0,1),repeat=N):
  table=np.array(xt,dtype=np.int64)
  shifts=np.array([table[g['c']]*g['table_weight'] for g in gs],dtype=np.int64)
  gates=(A@WA.T+shifts>=TH).astype(np.int64)
  score=gates@weights+base
  targets=table[B]
  assert np.all((score>=0)==targets),(m,xt)
  margin=min(margin,int(np.min(score*(2*targets-1))));count+=len(A)
 w['verification']={'method':'all raw table/address assignments, integer arithmetic','inputs':count,'minimum_signed_margin':margin,'bottoms':H,'total_gates':H+1}
 (OUT/('exact_k3_m%d.json'%m)).write_text(json.dumps(w,indent=2)+'\n')
 coeffs=[g['threshold'] for g in gs]+[z for g in gs for z in g['address_weights']]+weights.tolist()+raw.tolist()+[w['top_constant']]
 result.update(w['verification'],maximum_absolute_integer=max(abs(z) for z in coeffs),maximum_magnitude_bits=max(abs(z) for z in coeffs).bit_length())
 results.append(result);print(json.dumps(result),flush=True)
(OUT/'verification_results.json').write_text(json.dumps({'Authors':'Christian Reitwiessner','copyright':'Copyright (c) 2026 Christian Reitwiessner','results':results},indent=2)+'\n')
