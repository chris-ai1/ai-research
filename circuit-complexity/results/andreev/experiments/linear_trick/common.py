import sys; sys.path.insert(0,'/tmp/pydeps')
import numpy as np
phi=lambda u:(-1)**(u%2)*u
def stair(gates,w,lo,hi,g,coef,lam=None):
    """add coef*g(L) for integer form L=w.z with range [lo,hi]; if lam given, subtract lam*L
    (free linear term returned as weight vector).  Returns (const, linear_weight_vector)."""
    lin=np.zeros(len(w))
    if lam is None:
        for th in range(lo+1,hi+1):
            d=coef*(g(th)-g(th-1))
            if d!=0: gates.append((np.array(w,float),th,d))
        return coef*g(lo),lin
    for th in range(lo+1,hi+1):
        d=coef*(g(th)-g(th-1))-lam
        if d!=0: gates.append((np.array(w,float),th,d))
    return coef*g(lo)-lam*lo, lam*np.array(w,float)
def layout(k,m):
    N=1<<k; n=N+k*m
    def tw(S):
        v=np.zeros(n)
        for i in range(k):
            if S>>i&1: v[N+i*m:N+(i+1)*m]=1
        return v
    def yw(S):
        v=np.zeros(n)
        for c in range(N):
            if bin(S&c).count('1')%2: v[c]=1
        return v
    def ex(c): v=np.zeros(n); v[c]=1; return v
    return N,n,tw,yw,ex
def inputs(k,m,samples=20000,seed=1):
    N=1<<k; n=N+k*m; rng=np.random.default_rng(seed)
    if n<=18:
        return ((np.arange(1<<n)[:,None]>>np.arange(n))&1).astype(np.int8),True
    Z=rng.integers(0,2,(samples,n)).astype(np.int8)
    q=samples//8
    # adversarial families
    for i in range(k):  # forced even blocks -> b=0
        pass
    Z[:q,N:]=0                                   # all blocks weight 0 (b=0)
    blk=Z[q:2*q,N:].reshape(q,k,m); w=rng.integers(0,m//2+1,(q,k))*2  # random even weights
    blk[:]=(np.arange(m)[None,None,:]<w[:,:,None]); Z[q:2*q,N:]=blk.reshape(q,k*m)
    Z[2*q:3*q,:N]=1                              # all-ones table
    Z[3*q:4*q,:N]=0                              # all-zeros table
    Z[4*q:5*q,N:]=1                              # all blocks full weight m
    # single address bit table / complement table
    a=rng.integers(0,N,q); Z[5*q:6*q,:N]=0; Z[5*q+np.arange(q),a]=1
    a=rng.integers(0,N,q); Z[6*q:7*q,:N]=1; Z[6*q+np.arange(q),a]=0
    # extreme weights per block: each block weight in {0,1,m-1,m}
    blk=Z[7*q:,N:].reshape(-1,k,m); w=rng.choice([0,1,max(m-1,0),m],(blk.shape[0],k))
    blk[:]=(np.arange(m)[None,None,:]<w[:,:,None]); Z[7*q:,N:]=blk.reshape(-1,k*m)
    # random permutations inside blocks for the structured ones
    for i in range(k):
        perm=rng.permuted(np.tile(np.arange(m),(samples,1)),axis=1)
        Z[:,N+i*m:N+(i+1)*m]=np.take_along_axis(Z[:,N+i*m:N+(i+1)*m],perm,axis=1)
    return Z,False
def evaluate(gates,K,lin,Z,chunk=4096):
    W=np.array([g[0] for g in gates]); T=np.array([g[1] for g in gates]); V=np.array([g[2] for g in gates],float)
    out=np.empty(len(Z))
    for s in range(0,len(Z),chunk):
        z=Z[s:s+chunk].astype(float)
        out[s:s+chunk]=((z@W.T)>=T-1e-9).astype(float)@V+z@lin+K
    return out
def target(k,m,Z):
    N=1<<k
    addr=sum(((Z[:,N+i*m:N+(i+1)*m].sum(1)%2).astype(int)<<i) for i in range(k))
    return Z[np.arange(len(Z)),addr]
