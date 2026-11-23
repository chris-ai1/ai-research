# Copyright (c) 2026 Christian Reitwiessner
# Authors: Christian Reitwiessner
"""Verify saved final witnesses without invoking or trusting any solver."""
import sys
sys.path.insert(0,'/tmp/pydeps')
import numpy as np
from pathlib import Path
from itertools import product
import json
P=Path(__file__).resolve().parent
results=[]
for name in ('exact_k3_m2.json','exact_k3_m3.json','exact_k3_m4.json','exact_k4_m4.json'):
 w=json.loads((P/name).read_text());k=w['k'];m=w['m'];N=1<<k;gs=w['gates']
 A=np.array(list(product((0,1),repeat=k*m)),dtype=np.int64)
 B=np.zeros(len(A),dtype=np.int64)
 for i in range(k):B+=(A[:,i*m:(i+1)*m].sum(axis=1)%2)<<i
 WA=np.array([g['address_weights'] for g in gs],dtype=np.int64)
 th=np.array([g['threshold'] for g in gs],dtype=np.int64)
 v=np.array([g['top_weight'] for g in gs],dtype=np.int64)
 raw=np.array(w['top_raw_address'],dtype=np.int64)
 offset=A@raw+w['top_constant']
 minimum=10**30
 if N<=8:
  D=A@WA.T-th
  for x in product((0,1),repeat=N):
   shift=np.array([x[g['c']]*g['table_weight'] for g in gs],dtype=np.int64)
   score=(D+shift>=0).astype(np.int64)@v+offset
   target=np.array(x,dtype=np.int64)[B]
   assert np.all((score>=0)==target)
   minimum=min(minimum,int(np.min(np.where(target,score+1,-score))))
  method='direct exhaustive integer evaluation'
 else:
  base=offset.copy();coef=np.zeros((len(A),N),dtype=np.int64)
  for start in range(0,len(gs),32):
   stop=min(start+32,len(gs));D=A@WA[start:stop].T-th[start:stop]
   for local,j in enumerate(range(start,stop)):
    g=gs[j];f0=(D[:,local]>=0).astype(np.int64);f1=(D[:,local]+g['table_weight']>=0).astype(np.int64)
    base+=v[j]*f0;coef[:,g['c']]+=v[j]*(f1-f0)
  main=coef[np.arange(len(A)),B].copy();coef[np.arange(len(A)),B]=0
  max0=base+np.maximum(coef,0).sum(axis=1)
  min1=base+main+np.minimum(coef,0).sum(axis=1)
  assert np.all(max0<0) and np.all(min1>=0)
  minimum=int(min(np.min(-max0),np.min(min1+1)))
  method='all raw addresses, exact extrema over every independent table bit'
 result={'file':name,'bottoms':len(gs),'total_gates':len(gs)+1,'method':method,'raw_addresses':len(A),'tables':1<<N,'certified_inputs':len(A)*(1<<N),'integer_classification_gap':minimum}
 results.append(result);print(json.dumps(result),flush=True)
(P/'final_checks.json').write_text(json.dumps({'Authors':'Christian Reitwiessner','copyright':'Copyright (c) 2026 Christian Reitwiessner','results':results},indent=2)+'\n')
