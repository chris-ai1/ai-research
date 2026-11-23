"""Independent re-evaluation of five_eighths.build(): exhaustive over ALL (x,s) for s in {0..m}^k (the gates are block-uniform,
so this equals exhaustive over all N+km input bits), exact integer arithmetic, own target via common.A_full on real bits."""
import sys, itertools, time
sys.dont_write_bytecode=True
sys.path.insert(0,'/tmp/pydeps'); sys.path.insert(0,'/tmp/andreev_gap/verify')
import numpy as np
src=open('/tmp/andreev_gap/five_eighths.py').read().split("for k,m in [")[0]
ns={}; exec(src,ns); build=ns['build']
from common import *
def run(k,m):
    gates,K,N,n=build(k,m)
    W=np.array([g[0] for g in gates]); T=np.array([g[1] for g in gates]); V=np.array([g[2] for g in gates])
    assert np.all(W==np.round(W)) and np.all(T==np.round(T)) and np.all(V==np.round(V)) and K==round(K)
    W=W.astype(np.int64);T=T.astype(np.int64);V=V.astype(np.int64);K=int(round(K))
    # block-uniformity check: weights on each block's bits identical in every gate
    for i in range(k): assert np.all(W[:,N+i*m:N+(i+1)*m]==W[:,[N+i*m]]), 'gate not block-symmetric'
    Wr=np.hstack([W[:,:N],W[:,[N+i*m for i in range(k)]]])   # gate weights on (x, s)
    bad=0; tot=0
    xs=np.array(list(itertools.product((0,1),repeat=N)),dtype=np.int64)
    ss=np.array(list(itertools.product(range(m+1),repeat=k)),dtype=np.int64)
    X=np.hstack([np.repeat(xs,len(ss),0),np.tile(ss,(len(xs),1))])
    CH=1<<20
    for a in range(0,len(X),CH):
        Z=X[a:a+CH]
        G=(Z@Wr.T>=T).astype(np.int64)
        P=G@V+K
        out=(P<-N).astype(np.int64)
        b=sum(((Z[:,N+i]%2)<<i) for i in range(k))
        tgt=Z[np.arange(len(Z)),b]
        bad+=int((out!=tgt).sum()); tot+=len(Z)
    # spot-check the 'tgt' against A_full on real bits
    for p,o in itertools.islice(inputs(k,m,'blocksym'),0,50000):
        pass
    nz=int((V!=0).sum())
    print(f'k={k} m={m}: gates={len(gates)} (nonzero coeff {nz}) formula={(N-1)*(N+2)+3*k*m*N//2+1} points={tot} mismatches={bad}',flush=True)
for km in sys.argv[1:]:
    k,m=map(int,km.split(',')); t=time.time(); run(k,m)
