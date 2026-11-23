# Copyright (c) 2026 Christian Reitwiessner
# Authors: Christian Reitwiessner
"""One bounded feasibility search for at most 47 bottoms for A_(3,3)."""
import sys
sys.path.insert(0,'/tmp/pydeps')
import numpy as np
from itertools import product
from scipy.optimize import milp, Bounds, LinearConstraint
from scipy.sparse import csc_matrix
from pathlib import Path
import json
OUT=Path(__file__).resolve().parent
k=3;d=9;N=8
A=np.array(list(product((0,1),repeat=d)),dtype=np.int64)
meta=[];E=[];Z=[]
for c in range(N):
 for t in range(4):
  e=np.array([[t&1,t>>1,((c>>i)&1)^(t&1)^(t>>1)] for i in range(k)])
  for sign in (-1,1):
   q=np.array([sign*3**i for i in range(k)])
   wa=np.concatenate([q[i]*(1-2*e[i]) for i in range(k)])
   const=sum(int(q[i])*(int(e[i].sum())-2) for i in range(k))
   L=A@wa+const
   E.append(L>=1);Z.append(L==0)
   meta.append({'c':c,'address_weights':wa.tolist(),'threshold':int(1-const)})
E=np.stack(E,axis=1).astype(int);Z=np.stack(Z,axis=1).astype(int)
F=np.c_[A,np.ones(len(A),dtype=int)];H=len(meta)
C=np.r_[np.c_[E,F],-np.c_[E+Z,F]]
C=np.c_[C,np.zeros((len(C),H))]
cap=np.c_[np.eye(H),np.zeros((H,d+1)),-128*np.eye(H)]
count=np.r_[np.zeros(H+d+1),np.ones(H)][None,:]
CC=np.r_[C,cap,count];rhs=np.r_[-np.ones(len(C)),np.zeros(H),47]
r=milp(np.zeros(CC.shape[1]),integrality=np.r_[np.zeros(H+d+1),np.ones(H)],bounds=Bounds(np.r_[np.zeros(H),-np.full(d+1,np.inf),np.zeros(H)],np.r_[np.full(H,128),np.full(d+1,np.inf),np.ones(H)]),constraints=LinearConstraint(csc_matrix(CC),-np.inf,rhs),options={'time_limit':40})
result={'Authors':'Christian Reitwiessner','status':int(r.status),'message':r.message,'success':bool(r.success),'top_gate_weight_cap':128,'target_bottoms':47}
if r.x is not None:
 scale=10**6
 vv=np.rint(r.x[:H+d+1]*scale).astype(np.int64)
 ids=np.flatnonzero(vv[:H])
 margins=-(C[:,:H+d+1].astype(np.int64)@vv)
 result.update(bottoms=len(ids),exact_integer_margin=int(margins.min()),verified=bool(margins.min()>0))
 if margins.min()>0:
  witness={'Authors':'Christian Reitwiessner','copyright':'Copyright (c) 2026 Christian Reitwiessner','k':3,'m':3,'gates':[dict(meta[j],table_weight=1,top_weight=int(vv[j])) for j in ids],'top_raw_address':vv[H:H+d].tolist(),'top_constant':int(vv[-1])}
  (OUT/'sparse_witness.json').write_text(json.dumps(witness,indent=2)+'\n')
print(json.dumps(result),flush=True)
(OUT/'sparse_search_results.json').write_text(json.dumps(result,indent=2)+'\n')
