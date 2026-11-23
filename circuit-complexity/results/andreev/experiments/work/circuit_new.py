# Compare the original per-S gadget (five_eighths.py) with the improved one, exactly, on circuit inputs.
import sys; sys.path.insert(0,'/tmp/pydeps')
import numpy as np
from fractions import Fraction
phi=lambda u:(-1)**(u%2)*u
def stair(gates,w,lo,hi,g,coef):
    c0=coef*g(lo)
    for th in range(lo+1,hi+1):
        j=coef*(g(th)-g(th-1))
        if j!=0: gates.append((w,th,j))
    return c0
def build_old(k,m):
    N=1<<k; n=N+k*m; gates=[]; K=0; M=2*N*N
    for S in range(1,N):
        sz=bin(S).count('1'); tw=np.zeros(n,int)
        for i in range(k):
            if S>>i&1: tw[N+i*m:N+(i+1)*m]=1
        yw=np.zeros(n,int)
        for c in range(N):
            if bin(S&c).count('1')%2: yw[c]=2
        x0=np.zeros(n,int); x0[0]=2
        K+=stair(gates,yw+tw,0,N+sz*m,phi,2)
        K+=stair(gates,tw,0,sz*m,lambda u:-2*phi(u)+(M//(2*N))*phi(u),1)
        K+=stair(gates,x0+tw,0,2+sz*m,phi,-(M//(2*N)))
    e0=np.zeros(n,int); e0[0]=1
    K+=stair(gates,e0,0,1,lambda u:u,-(M//N))
    return gates,K,N,n
def build_new(k,m):
    """per S: 4G(2Y+t) - [4G(t)+2C floor(t/2)] + 2C floor((t+x0)/2) ; -C*x0 merged into the single x0 gate.
       G(u)=phi(u)/2-(-1)^u/4, so 4G(u)=2phi(u)-(-1)^u (integer)."""
    N=1<<k; n=N+k*m; gates=[]; K=0; M=2*N*N; C=M//N
    G4=lambda u:2*phi(u)-(-1)**(u%2)
    x0coef=-(M//N)          # original S=empty term
    for S in range(1,N):
        sz=bin(S).count('1'); T=sz*m; tw=np.zeros(n,int)
        for i in range(k):
            if S>>i&1: tw[N+i*m:N+(i+1)*m]=1
        yw=np.zeros(n,int)
        for c in range(N):
            if bin(S&c).count('1')%2: yw[c]=2
        x0=np.zeros(n,int); x0[0]=1
        K+=stair(gates,yw+tw,0,N+T,G4,1)
        K+=stair(gates,tw,0,T,lambda u:-G4(u)-2*C*(u//2),1)
        K+=stair(gates,x0+tw,0,T+1,lambda u:2*C*(u//2),1)
        x0coef+=-C
    e0=np.zeros(n,int); e0[0]=1
    gates.append((e0,1,x0coef))
    return gates,K,N,n
def evalP(gates,K,Z):
    W=np.array([g[0] for g in gates]); T=np.array([g[1] for g in gates]); V=np.array([g[2] for g in gates],dtype=np.int64)
    return ((Z@W.T)>=T).astype(np.int64)@V+K
def check(k,m,samples=4000,rng=np.random.default_rng(1)):
    go,Ko,N,n=build_old(k,m); gn,Kn,_,_=build_new(k,m)
    if n<=16: Z=((np.arange(1<<n)[:,None]>>np.arange(n))&1)
    else:
        Z=rng.integers(0,2,(samples,n)); Z[:samples//4,N:]=0; Z[samples//4:samples//2,:N]=1
    Po=evalP(go,Ko,Z); Pn=evalP(gn,Kn,Z)
    addr=sum(((Z[:,N+i*m:N+(i+1)*m].sum(1)%2).astype(int)<<i) for i in range(k))
    xb=Z[np.arange(len(Z)),addr]
    pred=sum(N+2*(bin(S).count('1')*m)+(bin(S).count('1')*m+1)//2-2 for S in range(1,N))+1
    print(f"k={k} m={m} N={N}: old gates={len(go)} new gates={len(gn)} (formula {pred}); P identical={np.array_equal(Po,Pn)}; "
          f"new correct={np.array_equal((Pn< -N).astype(int),xb)} on {len(Z)} inputs",flush=True)
for k,m in [(1,1),(1,3),(2,1),(2,2),(2,3),(3,1),(3,2),(4,3),(5,4),(6,5)]: check(k,m)
