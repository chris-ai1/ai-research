"""C_k = max over h:{0,1}^k->{0,1} of the least number of bottom gates of a depth-2 threshold circuit
(top gate reads the gates AND the k inputs) computing h.  Exact for k<=3 by LP feasibility (HiGHS);
threshold functions of k bits are enumerated exactly by LP as well."""
import sys, itertools
sys.path.insert(0,'/tmp/pydeps')
import numpy as np
from scipy.optimize import linprog

def separable(points, labels):
    """is there (w,t) with w.p - t >= 1 for label 1 and <= -1 for label 0 ?  (exact up to LP tolerance; tiny sizes)"""
    d=len(points[0]); A=[]; b=[]
    for p,l in zip(points,labels):
        row=list(p)+[-1.0]
        if l: A.append([-c for c in row]); b.append(-1.0)
        else: A.append(row); b.append(-1.0)
    r=linprog(np.zeros(d+1),A_ub=np.array(A),b_ub=np.array(b),bounds=[(None,None)]*(d+1),method='highs')
    return r.status==0

def all_thresholds(k):
    Z=list(itertools.product((0,1),repeat=k)); T=[]
    for lab in itertools.product((0,1),repeat=len(Z)):
        if separable(Z,lab): T.append(lab)
    return Z,T

def min_gates(k, maxS=3):
    Z,T=all_thresholds(k)
    Tset=set(T)
    print(f'k={k}: {len(T)} threshold functions on {len(Z)} points')
    nonconst=[g for g in T if 0<sum(g)<len(Z)]
    res={}
    for h in itertools.product((0,1),repeat=len(Z)):
        if h in Tset: res[h]=0; continue
        found=None
        for S in range(1,maxS+1):
            for gs in itertools.combinations(nonconst,S):
                pts=[tuple(g[i] for g in gs)+Z[i] for i in range(len(Z))]
                if separable(pts,h): found=S; break
            if found: break
        res[h]=found
    return res

if __name__=='__main__':
    for k in (2,3):
        res=min_gates(k)
        from collections import Counter
        c=Counter(res.values()); print(f'k={k}: distribution of min #gates over all {2**(2**k)} functions: {dict(sorted(c.items(),key=lambda t:(t[0] is None,t[0])))}')
        worst=[h for h,v in res.items() if v==max(v for v in res.values() if v is not None)]
        print('  C_k =',max(v for v in res.values() if v is not None),' e.g.',worst[:3])
