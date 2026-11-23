# Copyright (c) 2026 Christian Reitwiessner
# Authors: Christian Reitwiessner
"""Test the specific 32-gate m=3 orientations on m=4, without searching new orientations."""
import sys
sys.path.insert(0,'/tmp/pydeps')
import numpy as np,json
from itertools import product
from pathlib import Path
from scipy.optimize import linprog
P=Path(__file__).resolve().parent
w=json.loads((P/'exact_k3_m3.json').read_text());gs=w['gates'];A=np.array(list(product((0,1),repeat=12)),dtype=np.int64)
for g in gs:
 old=g['address_weights'];new=[]
 # In block 0, the product of the three signs is eta*(-1)^c0.
 eta=int(np.prod(old[:3]))*(-1)**(g['c']&1)
 for i in range(3):new+=old[3*i:3*i+3]+[eta*3**i]
 g['address_weights']=new
W=np.array([g['address_weights'] for g in gs]);th=np.array([g['threshold'] for g in gs]);D=A@W.T-th
E=(D>=0).astype(int);Z=(D==-1).astype(int);F=np.c_[A,np.ones(len(A),dtype=int)]
C=np.r_[np.c_[E,F],-np.c_[E+Z,F]]
r=linprog(np.r_[np.ones(32),np.zeros(13)],A_ub=C,b_ub=-np.ones(len(C)),bounds=[(0,None)]*32+[(None,None)]*13,method='highs')
result={'Authors':'Christian Reitwiessner','status':int(r.status),'message':r.message,'hypothesis':'extend the final m=3 orientations to m=4'}
if r.success:
 v=np.rint(r.x*1000000).astype(np.int64);margin=int(np.min(-C@v));result['exact_integer_margin']=margin
 if margin>0:
  for j,g in enumerate(gs):g['top_weight']=int(v[j])
  w['m']=4;w['top_raw_address']=v[32:44].tolist();w['top_constant']=int(v[-1]);w.pop('verification',None)
  (P/'extension_witness_m4.json').write_text(json.dumps(w,indent=2)+'\n')
print(json.dumps(result));(P/'extension_results.json').write_text(json.dumps(result,indent=2)+'\n')
