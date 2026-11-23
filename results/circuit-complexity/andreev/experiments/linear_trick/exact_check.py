import sys; sys.path.insert(0,"/tmp/pydeps"); sys.path.insert(0,"/tmp/andreev_gap/linear_trick")
import numpy as np
from common import evaluate, target
import constr_c, constr_d
def forced(k,m,samples,rng):
    N=1<<k; n=N+k*m
    Z=rng.integers(0,2,(samples,n)).astype(np.int8)
    tab=rng.random(samples)
    Z[tab<0.15,:N]=1; Z[(tab>=0.15)&(tab<0.3),:N]=0
    mode=rng.integers(0,4,samples)
    for r in range(samples):
        if mode[r]==3: continue
        if mode[r]==0: b=0
        elif mode[r]==1: b=1<<rng.integers(k)
        else: b=rng.integers(N)
        for i in range(k):
            par=(b>>i)&1
            w=rng.choice([v for v in range(m+1) if v%2==par] or [par])
            if rng.random()<0.3: w=max([v for v in range(m+1) if v%2==par])
            blk=np.zeros(m,np.int8); blk[rng.permutation(m)[:w]]=1; Z[r,N+i*m:N+(i+1)*m]=blk
    return Z
rng=np.random.default_rng(7)
for name,mod in [("c",constr_c),("d",constr_d)]:
    for k,m in [(1,4),(2,3),(3,3),(4,4),(5,5),(6,3),(6,5)]:
        g,K,lin,N,n=mod.build(k,m); Z=forced(k,m,30000,rng)
        P=evaluate(g,K,lin,Z); xb=target(k,m,Z)
        addr=sum(((Z[:,N+i*m:N+(i+1)*m].sum(1)%2).astype(int)<<i) for i in range(k))
        X=Z[:,:N].astype(np.int64).sum(1); x0=Z[:,0].astype(np.int64); xb=xb.astype(np.int64)
        closed=N-2*N*xb+(addr==0)*(2*N*X-2*N*N*x0)
        print(f"({name}) k={k} m={m}: P==closed form exactly: {np.allclose(P,closed)}  sign-correct: {np.array_equal((P<0).astype(int),xb)}  #b=0:{(addr==0).sum()} #|b|=1:{sum(bin(int(a)).count('1')==1 for a in addr)}",flush=True)
