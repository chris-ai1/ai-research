# Copyright (c) 2026 Christian Reitwiessner
# Authors: Christian Reitwiessner
"""Exact finite frontier for the simplest Walsh-sign generalization."""
import sys
sys.path.insert(0,'/tmp/pydeps')
import numpy as np
for k in [2,3,4]:
 n=1<<k
 X=2*((np.arange(1<<n)[:,None]>>np.arange(n))&1)-1
 H=np.array([[(-1)**((s&c).bit_count()%2) for c in range(n)] for s in range(n)])
 Z=X@H.T;Q=np.sign(Z);Q[:,0]=0;R=Q@H
 # Strict ordering with arbitrary table-dependent intercept.
 pos=np.min(np.where(X==1,R,1000),axis=1)
 neg=np.max(np.where(X==-1,R,-1000),axis=1)
 bad=np.flatnonzero(pos<=neg)
 print('k',k,'tables',len(X),'nonseparable',len(bad),flush=True)
 if len(bad):
  j=int(bad[0]);print('first bad table',((X[j]+1)//2).tolist(),'scores',R[j].tolist(),flush=True)
