# Copyright (c) 2026 Christian Reitwiessner.
# Authors: Christian Reitwiessner
print("# Authors: Christian Reitwiessner", flush=True)
import sys,json,itertools
sys.path.insert(0,'/tmp/pydeps')
import numpy as np
from scipy.optimize import linprog
from fractions import Fraction
N=16
chi=np.array([[(-1)**((s&c).bit_count()%2) for c in range(N)] for s in range(N)],dtype=np.int16)
rows=set(); bad=None
for mask in range(1<<N):
    xi=np.array([2*((mask>>c)&1)-1 for c in range(N)],dtype=np.int16)
    X=chi@xi
    row=(int(xi[0]*X[0]),)+tuple(int(xi[0]*sum((X[1:]>=r).astype(int)-(X[1:]<=-r).astype(int))) for r in range(2,17,2))
    rows.add(row)
    if bad is None and xi[0]*sum(np.sign(X[1:]))<=0 and X[0]==0: bad=mask
A=np.array(sorted(rows),dtype=float)
print('distinct constraints',len(rows),flush=True)
results=[]
for count in range(1,9):
    for inds in itertools.combinations(range(1,9),count):
        cols=(0,)+inds
        res=linprog(np.zeros(len(cols)),A_ub=-A[:,cols],b_ub=-np.ones(len(A)),bounds=[(None,None)]*len(cols),method='highs',options={'time_limit':5})
        if res.success:
            coeff=[Fraction(float(v)).limit_denominator(100000) for v in res.x]
            margin=min(sum(Fraction(int(row[c]))*v for c,v in zip(cols,coeff)) for row in rows)
            assert margin>0
            result={'thresholds':[2*i for i in inds],'coefficients':[str(x) for x in coeff],'margin':str(margin)}
            results.append(result)
            print(json.dumps(result),flush=True)
    if results: break
out={'authors':'Christian Reitwiessner','N':N,'constraints':len(rows),'first_feasible_number_of_odd_channels':count,'certificates':results}
with open('/tmp/andreev_gap/upper_astra/probe_results.json','w') as f: json.dump(out,f,indent=2)
