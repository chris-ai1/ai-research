# (d') = construction (d) with two exact lower-order savings (leading term unchanged):
#  (i)  2N(|x'|^2+|x'|) + 2N|x'|sigma = (N/2)(u^2 - sigma^2) + 2N|x'| with u = 2|x'|+sigma :
#       one staircase on u (2(N-1)+km gates) + one on sigma (km gates) instead of 3(N-1)+2km  -> saves N-1
#  (ii) the x0-gated sigma staircase [sigma+Bx0>=l+B] coincides with the S=[k] override gates for even l
#       -> merged (Circuit.finalize)                                                       -> saves floor(km/2)
import sys; sys.path.insert(0,'/tmp/andreev_gap/push_upper'); sys.path.insert(0,'/tmp/pydeps')
import numpy as np
from circ import Circuit
from constr import forms, stair, cu
def build_dp(k,m):
    N,n,tw,yw,ex,blk=forms(k,m); C=Circuit(k,m); B=N+k*m+2
    xp=np.zeros(n,np.int64); xp[1:N]=1; sg=np.zeros(n,np.int64); sg[N:]=1
    C.K+=N
    for S in range(1,N):
        T=bin(S).count('1')*m
        stair(C,2*yw(S)+tw(S),0,N+T,lambda u:cu(u)**2,-8)          # main ridge, odd thresholds
        stair(C,tw(S),0,T,lambda u:cu(u)**2,8)                     # residue, odd thresholds
        for j in range(1,T//2+1): C.gate(tw(S)+B*ex(0),2*j+B,-8*N) # override, x0-gated even thresholds
    C.u+=2*N*xp + 2*N*xp                                           # 4 sum_S Y_S = 2N|x'| ; and +2N|x'| from (i)
    stair(C,2*xp+sg,0,2*(N-1)+k*m,lambda u:u*u,N//2)               # (N/2) u^2
    stair(C,sg,0,k*m,lambda u:u*u,-(N//2))                         # -(N/2) sigma^2
    for i in range(k):
        for l in range(1,m+1): C.gate(blk(i)+B*ex(1<<i),l+B,2*N)  # 2N x_{e_i} s_i
    C.u+=-2*N*N*ex(0)
    for l in range(1,k*m+1): C.gate(sg+B*ex(0),l+B,2*N*N)          # 2N^2 x0 sigma
    return C.finalize()
def count_dp(k,m):
    N=1<<k; tot=0
    for S in range(1,N):
        T=bin(S).count('1')*m
        tot+=(N+T+1)//2 + (T+1)//2 + T//2
    tot+= 2*(N-1) + 3*k*m      # u^2: 2(N-1)+km ; sigma^2, x_{e_i}s_i, x0*sigma: km each ; minus km merged duplicates
    return tot
if __name__=='__main__':
    from circ import all_inputs, check
    from constr import build_d
    for k,m in [(1,1),(1,2),(1,3),(2,1),(2,2),(2,3),(2,4),(3,1),(3,2),(3,3)]:
        C=build_dp(k,m); Z=all_inputs(C.n); ok,marg,bad=check(C,Z)
        print(k,m,'n',C.n,'gates',C.size(),'formula',count_dp(k,m),'(d)',build_d(k,m).size(),'ok',ok,'margin',marg,flush=True)
