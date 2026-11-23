import math, sys
sys.path.insert(0,'/tmp/andreev_gap/push_lower')
from bound_table import lb
for name,frac in [('coherent',lambda k,m:1-(1-1/m)**k),('blocksym',lambda k,m:min(k,2*math.sqrt(2*k))/m)]:
    c1=c2=None
    for k in range(6,60):
        N=2**k; m=N//k; n=N+k*m; L=lb(k,m,frac(k,m))
        if c1 is None and L>n**1.5/math.log2(n)**2: c1=k
        if c2 is None and L>n**1.5: c2=k
    print(f'{name}: exceeds n^1.5/log2(n)^2 from k={c1}; exceeds n^1.5 from k={c2}')
