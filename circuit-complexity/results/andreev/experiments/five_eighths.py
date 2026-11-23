import itertools, numpy as np
def stair(gates,w,lo,hi,g,coef):
    """coef*g(L) for integer linear form L=w.z in [lo,hi]: gates [w.z>=th], returns constant."""
    for th in range(lo+1,hi+1): gates.append((w,th,coef*(g(th)-g(th-1))))
    return coef*g(lo)
phi=lambda u:(-1)**(u%2)*u
def build(k,m):
    N=1<<k; n=N+k*m; gates=[]; K=0.0; M=2*N*N
    sets=[S for S in range(1,N)]
    for S in sets:
        sz=bin(S).count('1')
        tw=np.zeros(n); 
        for i in range(k):
            if S>>i&1: tw[N+i*m:N+(i+1)*m]=1
        yw=np.zeros(n)
        for c in range(N):
            if bin(S&c).count('1')%2: yw[c]=2
        x0=np.zeros(n); x0[0]=2
        K+=stair(gates,yw+tw,0,N+sz*m,phi,2.0)                 # 2 phi(2Y_S+t_S)
        K+=stair(gates,tw,0,sz*m,lambda u:-2*phi(u)+M/(2*N)*phi(u),1.0)  # shared t_S staircase
        K+=stair(gates,x0+tw,0,2+sz*m,phi,-M/(2*N))              # fix: 2x_0+t_S
    e0=np.zeros(n); e0[0]=1
    K+=stair(gates,e0,0,1,lambda u:u,-M/N)                        # S=empty fix term
    return gates,K,N,n
def check(k,m,samples=20000,rng=np.random.default_rng(1)):
    gates,K,N,n=build(k,m)
    W=np.array([g[0] for g in gates]); T=np.array([g[1] for g in gates]); V=np.array([g[2] for g in gates])
    if n<=16: Z=((np.arange(1<<n)[:,None]>>np.arange(n))&1).astype(float)
    else:
        Z=rng.integers(0,2,(samples,n)).astype(float)
        Z[:samples//4,N:]=0              # force b=0 often (all blocks even)
        Z[samples//4:samples//2,:N]=1    # all-ones tables (worst garbage)
    P=((Z@W.T)>=T-1e-9).astype(float)@V+K
    addr=sum(((Z[:,N+i*m:N+(i+1)*m].sum(1)%2).astype(int)<<i) for i in range(k))
    xb=Z[np.arange(len(Z)),addr]
    out=(P< -N).astype(int)
    full=(N-1)*(N+2)+3*k*m*N//2+1
    print(f"k={k} m={m} N={N} n={n}: gates={len(gates)} formula={full} old(2N^2+kmN)={2*N*N+k*m*N} correct={np.array_equal(out,xb)} on {len(Z)} inputs")
for k,m in [(1,1),(1,3),(2,1),(2,2),(2,3),(3,1),(3,2),(4,3),(5,4)]: check(k,m)
