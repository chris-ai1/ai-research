# Builders.  All weights/thresholds integers.  Output = [P<0].
import sys; sys.path.insert(0,'/tmp/andreev_gap/push_upper'); sys.path.insert(0,'/tmp/pydeps')
import numpy as np
from circ import Circuit
def forms(k,m):
    N=1<<k; n=N+k*m
    def tw(S):
        v=np.zeros(n,np.int64)
        for i in range(k):
            if S>>i&1: v[N+i*m:N+(i+1)*m]=1
        return v
    def yw(S):
        v=np.zeros(n,np.int64)
        for c in range(1,N):
            if bin(S&c).count('1')&1: v[c]=1
        return v
    def ex(c): v=np.zeros(n,np.int64); v[c]=1; return v
    def blk(i): v=np.zeros(n,np.int64); v[N+i*m:N+(i+1)*m]=1; return v
    return N,n,tw,yw,ex,blk
def stair(C,w,lo,hi,f,coef=1):
    """add coef*f(L) for integer form L=w.z in [lo,hi]: gates [L>=th] th=lo+1..hi with step f(th)-f(th-1);
       returns nothing; constant coef*f(lo) added to C.K"""
    C.K+=coef*f(lo)
    for th in range(lo+1,hi+1):
        d=coef*(f(th)-f(th-1))
        if d: C.gate(w,th,d)
cu=lambda u:-((-u)//2)
def build_d(k,m):
    """construction (d) re-implemented (baseline)."""
    N,n,tw,yw,ex,blk=forms(k,m); C=Circuit(k,m); B=N+k*m+2
    xp=np.zeros(n,np.int64); xp[1:N]=1; sg=np.zeros(n,np.int64); sg[N:]=1
    C.K+=N
    for S in range(1,N):
        T=bin(S).count('1')*m
        stair(C,2*yw(S)+tw(S),0,N+T,lambda u:cu(u)**2,-8)
        stair(C,tw(S),0,T,lambda u:cu(u)**2,8)
        for j in range(1,T//2+1): C.gate(tw(S)+B*ex(0),2*j+B,-8*N)
    C.u+=2*N*xp
    stair(C,xp,0,N-1,lambda u:u*u+u,2*N)
    stair(C,xp+sg,0,N-1+k*m,lambda u:u*u,N//2)
    stair(C,xp-sg,-k*m,N-1,lambda u:u*u,-(N//2))
    for i in range(k):
        for l in range(1,m+1): C.gate(blk(i)+B*ex(1<<i),l+B,2*N)
    C.u+=-2*N*N*ex(0)
    for l in range(1,k*m+1): C.gate(sg+B*ex(0),l+B,2*N*N)
    return C
if __name__=='__main__':
    from circ import *
    for k,m in [(1,1),(1,3),(2,1),(2,2),(2,3),(3,1),(3,2),(3,3)]:
        C=build_d(k,m); g0=C.size(); C.finalize()
        Z=all_inputs(C.n); ok,marg,bad=check(C,Z)
        print(k,m,'gates',g0,'after merge',C.size(),'ok',ok,'margin',marg,flush=True)
