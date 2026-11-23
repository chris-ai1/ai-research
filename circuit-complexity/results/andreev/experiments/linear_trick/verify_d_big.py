import sys; sys.path.insert(0,"/tmp/andreev_gap/linear_trick")
from constr_d import *
import numpy as np
def exact_count(k,m):
    N=1<<k
    return sum(N//2+2*((bin(S).count('1')*m+1)//2)+(bin(S).count('1')*m)//2 for S in range(1,N))+3*(N-1)+4*k*m
for k,m in [(4,6),(4,8),(5,4),(5,6),(6,4),(6,6),(7,3)]:
    gates,K,lin,N,n=build(k,m)
    for seed in (2,3):
        Z,_=inputs(k,m,60000,seed=seed)
        P=evaluate(gates,K,lin,Z); xb=target(k,m,Z)
        ok=np.array_equal((P<0).astype(int),xb)
        addr=sum(((Z[:,N+i*m:N+(i+1)*m].sum(1)%2).astype(int)<<i) for i in range(k))
        print(f"k={k} m={m} n={n} gates={len(gates)} exact_formula={exact_count(k,m)} seed={seed} correct={ok} margin={np.min(np.abs(P)):.1f} frac_b0={np.mean(addr==0):.2f} frac_|b|=1={np.mean([bin(int(a)).count('1')==1 for a in addr]):.2f} maxcoef={max(abs(g[2]) for g in gates):.0f} maxlin={np.max(np.abs(lin)):.0f}",flush=True)
