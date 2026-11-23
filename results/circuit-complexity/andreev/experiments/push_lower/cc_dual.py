import sys; sys.path.insert(0,'/tmp/pydeps'); sys.path.insert(0,'/tmp/andreev_gap/push_lower')
import numpy as np
from scipy.optimize import linprog
from cornercover import cut_sets
m=int(sys.argv[1])
sq,S=cut_sets(m)
A=np.zeros((len(S),len(sq)))
for i,s in enumerate(S):
    for e in s: A[i,e]=1
# dual: max sum w  s.t.  A w <= 1, w>=0
r=linprog(-np.ones(len(sq)),A_ub=A,b_ub=np.ones(len(S)),bounds=[(0,None)]*len(sq),method='highs')
w=r.x
print('dual value',-r.fun)
G=np.zeros((m,m))
for (a,b),val in zip(sq,w): G[m-1-b,a]=val
np.set_printoptions(precision=3,suppress=True,linewidth=200)
print(G)
