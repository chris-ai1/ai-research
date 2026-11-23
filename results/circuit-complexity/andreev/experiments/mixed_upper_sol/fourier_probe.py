# Copyright (c) 2026 Christian Reitwiessner
# Authors: Christian Reitwiessner
import sys,itertools
sys.path.insert(0,'/tmp/pydeps')
import numpy as np
from scipy.optimize import linprog
k=3;n=8;X=np.array(list(itertools.product([0,1],repeat=n)));H=np.array([[(-1)**((s&c).bit_count()%2) for c in range(n)] for s in range(n)])
h=X@H.T
for r in [0,1]:
 cols=[]
 for s in range(1,n):
  for th in ([r] if s==7 else [0,1]): cols.append(np.repeat(2*(h[:,s]>=th)-1,n)*np.tile(H[s],256))
 cols.extend([np.repeat(X[:,c],n) for c in range(n)]+[np.ones(256*n)])
 A=np.array(cols).T; sig=(2*X-1).ravel()
 res=linprog(np.zeros(A.shape[1]),A_ub=-sig[:,None]*A,b_ub=-np.ones(len(sig)),bounds=[(None,None)]*A.shape[1],method='highs')
 print('triple threshold',r,'status',res.message)
 if res.success:print(res.x)
