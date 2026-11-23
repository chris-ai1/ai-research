# Circuit container + exact integer evaluation + input generators for Andreev's function.
# Inputs z = (x_0..x_{N-1}, a_{1,1..m}, ..., a_{k,1..m});  s_i = |block i|, b_i = s_i mod 2, A = x_b.
# Circuit: bottom gates (w, theta) integer, g = [w.z >= theta]; top: P = sum_g v_g g + u.z + K ;
# output = [P < 0]   (all integers; Python int / numpy int64 with overflow checks).
import sys; sys.path.insert(0,'/tmp/pydeps')
import numpy as np, itertools
class Circuit:
    def __init__(s,k,m):
        s.k,s.m=k,m; s.N=1<<k; s.n=s.N+k*m
        s.W=[]; s.T=[]; s.V=[]; s.u=np.zeros(s.n,dtype=object); s.K=0
    def gate(s,w,th,v):
        w=np.asarray(w,dtype=np.int64)
        assert w.shape==(s.n,)
        s.W.append(w); s.T.append(int(th)); s.V.append(int(v))
    def finalize(s):
        """merge identical (w,theta) gates, drop zero-coefficient and constant gates"""
        d={}
        for w,t,v in zip(s.W,s.T,s.V):
            key=(w.tobytes(),t)
            if key in d: d[key][2]+=v
            else: d[key]=[w,t,v]
        W=[];T=[];V=[];K=s.K
        for w,t,v in d.values():
            if v==0: continue
            lo=int(np.minimum(w,0).sum()); hi=int(np.maximum(w,0).sum())
            if t<=lo: K+=v; continue          # always 1
            if t>hi: continue                  # always 0
            W.append(w);T.append(t);V.append(v)
        s.W,s.T,s.V,s.K=W,T,V,K
        return s
    def size(s): return len(s.W)
    def eval(s,Z,chunk=2048):
        W=np.array(s.W,dtype=np.int64); T=np.array(s.T,dtype=np.int64)
        V=np.array(s.V,dtype=np.int64); u=np.array([int(x) for x in s.u],dtype=np.int64)
        assert np.abs(V).sum()+np.abs(u).sum()*1+abs(s.K) < 2**62
        out=np.empty(len(Z),dtype=np.int64)
        for a in range(0,len(Z),chunk):
            z=Z[a:a+chunk].astype(np.int64)
            out[a:a+chunk]=((z@W.T)>=T).astype(np.int64)@V + z@u + s.K
        return out
def target(k,m,Z):
    N=1<<k
    b=np.zeros(len(Z),dtype=np.int64)
    for i in range(k): b|=((Z[:,N+i*m:N+(i+1)*m].sum(1)&1).astype(np.int64)<<i)
    return Z[np.arange(len(Z)),b].astype(np.int64), b
def all_inputs(n):
    return ((np.arange(1<<n,dtype=np.int64)[:,None]>>np.arange(n))&1).astype(np.int8)
def adversarial_inputs(k,m,nrand=20000,seed=0):
    """every address b (all if N<=128 else 128 incl. 0, e_i, N-1, weight-2) x block-weight patterns x tables"""
    rng=np.random.default_rng(seed); N=1<<k; n=N+k*m
    if N<=128: addrs=list(range(N))
    else:
        addrs=sorted(set([0,N-1]+[1<<i for i in range(k)]+[(1<<i)|(1<<j) for i in range(k) for j in range(i+1,k)][:40]+list(rng.integers(0,N,60))))
    def weights_for(b,mode):
        w=[]
        for i in range(k):
            par=(b>>i)&1
            opts=[v for v in range(m+1) if v%2==par]
            if mode=='min': w.append(opts[0])
            elif mode=='max': w.append(opts[-1])
            elif mode=='mix': w.append(opts[0] if rng.random()<.5 else opts[-1])
            else: w.append(int(rng.choice(opts)))
        return w
    tabs=[]
    tabs.append(np.zeros(N,np.int8)); tabs.append(np.ones(N,np.int8))
    for c in sorted(set([0,1,N//2,N-1]+[1<<i for i in range(k)])):
        t=np.zeros(N,np.int8); t[c]=1; tabs.append(t)
        t=np.ones(N,np.int8); t[c]=0; tabs.append(t)
    for p in (.1,.5,.9): tabs.append((rng.random(N)<p).astype(np.int8))
    rows=[]
    for b in addrs:
        tl=list(tabs)
        for v in (0,1):  # tables with x_b forced, rest extreme
            t=np.ones(N,np.int8); t[b]=v; tl.append(t)
            t=np.zeros(N,np.int8); t[b]=v; tl.append(t)
        for mode in ('min','max','mix','rand'):
            w=weights_for(b,mode)
            blk=np.zeros(k*m,np.int8)
            for i in range(k):
                bits=np.zeros(m,np.int8); bits[:w[i]]=1; rng.shuffle(bits); blk[i*m:(i+1)*m]=bits
            for t in tl: rows.append(np.concatenate([t,blk]))
    R=rng.integers(0,2,(nrand,n)).astype(np.int8)
    # half of random inputs forced to b=0 or b=e_i
    for r in range(nrand//2):
        b=0 if r%3==0 else (1<<int(rng.integers(0,k)))
        for i in range(k):
            bits=R[r,N+i*m:N+(i+1)*m]
            if (bits.sum()&1)!=((b>>i)&1):
                j=int(rng.integers(0,m)); bits[j]^=1
    return np.vstack([np.array(rows,np.int8),R])
def check(C,Z):
    P=C.eval(Z); y,b=target(C.k,C.m,Z)
    ok=np.array_equal((P<0).astype(np.int64),y)
    marg=int(np.min(np.abs(P))) if len(P) else None
    return ok,marg,int(np.sum((P<0).astype(np.int64)!=y))
