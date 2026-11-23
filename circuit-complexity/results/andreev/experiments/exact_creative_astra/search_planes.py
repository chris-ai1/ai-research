# Copyright (c) 2026 Christian Reitwiessner
# Authors: Christian Reitwiessner
"""Bounded exact-cover architecture search; solver results are checked with integers."""
import sys
sys.path.insert(0,'/tmp/pydeps')
import numpy as np
from itertools import product, permutations
from scipy.optimize import milp, Bounds, LinearConstraint
from scipy.sparse import csc_matrix
import json
from pathlib import Path
OUT=Path(__file__).resolve().parent
k=3;m=3;N=1<<k;d=k*m
A=np.array(list(product((0,1),repeat=d)),dtype=np.int64)
B=np.array([sum((sum(a[i*m:(i+1)*m])%2)<<i for i in range(k)) for a in A])
planes=[]
for c in range(N):
 for t in range(4):
  e=np.array([[t&1,t>>1,((c>>i)&1)^(t&1)^(t>>1)] for i in range(k)])
  D=np.array([np.abs(A[:,i*m:(i+1)*m]-e[i]).sum(axis=1)-2 for i in range(k)]).T
  planes.append((c,t,e,D))
M=np.stack([np.all(p[3]==0,axis=1) for p in planes],axis=1)
assert np.all(M.sum(axis=1)>=1)
assert all(np.all(B[M[:,j]]==p[0]) for j,p in enumerate(planes))
results={'Authors':'Christian Reitwiessner','copyright':'Copyright (c) 2026 Christian Reitwiessner','coverage_min':int(M.sum(axis=1).min()),'coverage_max':int(M.sum(axis=1).max()),'runs':[]}
for variant in ('fixed','all_lex'):
 vectors=[];meta=[]
 for j,(c,t,e,D) in enumerate(planes):
  opts=[((0,1,2),s) for s in [(1,1,1),(-1,-1,-1)]] if variant=='fixed' else product(permutations(range(k)),product((-1,1),repeat=k))
  seen=set()
  for perm,sgn in opts:
   q=np.zeros(k,dtype=np.int64)
   for pos,idx in enumerate(perm):q[idx]=sgn[idx]*3**pos
   F=np.sign(D@q)
   key=F.tobytes()
   if key in seen:continue
   seen.add(key);vectors.append(F);meta.append((j,q.tolist()))
 F=np.stack(vectors,axis=1)
 # Values on the affine basis (row ordering is big-endian binary).
 E=np.stack([F[1<<(d-1-i)]-F[0] for i in range(d)])
 R=F-F[0]-A@E
 selector=np.zeros((len(planes),len(meta)),dtype=np.int64)
 for j,(p,q) in enumerate(meta):selector[p,j]=1
 C=np.concatenate([R,selector],axis=0)
 rhs=np.concatenate([np.zeros(len(A)),np.ones(len(planes))])
 r=milp(np.zeros(len(meta)),integrality=np.ones(len(meta)),bounds=Bounds(0,1),constraints=LinearConstraint(csc_matrix(C.astype(float)),rhs,rhs),options={'time_limit':35,'mip_rel_gap':0})
 result={'variant':variant,'variables':len(meta),'status':int(r.status),'message':r.message,'success':bool(r.success)}
 if r.x is not None:
  z=np.rint(r.x).astype(np.int64)
  ok=np.array_equal(C@z,rhs)
  result['exact_integer_check']=bool(ok)
  if ok:
   result['selected']=[meta[j] for j in np.flatnonzero(z)]
   result['affine_constant']=int(F[0]@z)
   result['affine_weights']=(E@z).tolist()
 results['runs'].append(result)
 print(json.dumps(result),flush=True)
 (OUT/'plane_search_results.json').write_text(json.dumps(results,indent=2)+'\n')
