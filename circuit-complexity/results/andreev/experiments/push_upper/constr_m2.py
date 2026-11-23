# (d2): variant for block size m<=2 that removes BOTH the residue and the per-character override:
#  * residue dropped: for m<=2 the residue's non-collapsible part is N*sigma[b!=0] + N*sum_i [b=e_i] + N[b!=0]
#    (s_i=1 whenever b=e_i), i.e. linear + an ADDRESS FUNCTION, which is free: adding kappa_S to every gate of
#    main ridge S adds kappa_S*Y_S + kappa_S*t_S/2 + kappa_S/4 - (kappa_S/4)(-1)^{t_S}.  The leftover -N*sigma*[b=0]
#    only matters at b=0 and is covered by a larger override.
#  * override x0*[b=0] by the corner trick: m=2: sum_eps [eps.(s-1) + B x0 >= k + B]  (2^k gates);  m=1: one gate.
import sys; sys.path.insert(0,'/tmp/andreev_gap/push_upper'); sys.path.insert(0,'/tmp/pydeps')
import numpy as np, itertools
from circ import Circuit
from constr import forms, stair, cu
def build_m2(k,m):
    assert m in (1,2)
    N,n,tw,yw,ex,blk=forms(k,m); C=Circuit(k,m); B=4*N+4*k*m+8
    xp=np.zeros(n,np.int64); xp[1:N]=1; sg=np.zeros(n,np.int64); sg[N:]=1
    C.K+=N
    for S in range(1,N):
        T=bin(S).count('1')*m
        kap=-4*(k-2*bin(S).count('1')-1)          # realises +N*sum_i[b=e_i] - N[b=0] (free address function)
        stair(C,2*yw(S)+tw(S),0,N+T,lambda u,kap=kap:-8*cu(u)**2+kap*cu(u),1)
        C.u+=-kap*yw(S); C.u+=np.array([-(kap*int(v))//2 if False else 0 for v in tw(S)],dtype=object)
        # remove kappa*t_S/2 (linear) exactly: kappa even -> integer
        C.u+= -(kap//2)*tw(S); C.K+= -(kap//4) if kap%4==0 else 0
        assert kap%4==0
    # replacement of the residue's collapsible part:  (N/2)(sigma^2+sum s_i^2) + N*sigma + N  (+ N*sum[b=e_i]-N[b=0] above)
    stair(C,sg,0,k*m,lambda u:u*u,N//2)
    for i in range(k): stair(C,blk(i),0,m,lambda u:u*u,N//2)
    C.u+=N*sg; C.K+=N
    # quadratic leftovers of the ridges (as in (d'))
    C.u+=4*N*xp
    stair(C,2*xp+sg,0,2*(N-1)+k*m,lambda u:u*u,N//2)
    stair(C,sg,0,k*m,lambda u:u*u,-(N//2))
    for i in range(k):
        for l in range(1,m+1): C.gate(blk(i)+B*ex(1<<i),l+B,2*N)
    # override: -Cov * x0 * [b=0] , Cov > N + 2N(N-1) + N*(km) + N  (covers the dropped -N*sigma*[b=0] term)
    Cov=2*N*N+N*k*m+2*N
    if m==2:
        for eps in itertools.product((-1,1),repeat=k):
            w=np.zeros(n,np.int64); thr=k
            for i,e in enumerate(eps): w[N+i*m:N+(i+1)*m]=e; thr+=e   # eps.(s-1) >= k  <=>  eps.s >= k+sum(eps)
            C.gate(w+B*ex(0),thr+B,-Cov)
    else:
        C.gate(-sg+B*ex(0),B,-Cov)                                      # x0 and all address bits 0
    return C.finalize()
if __name__=='__main__':
    from circ import all_inputs, adversarial_inputs, check
    from constr2 import build_dp
    for k,m in [(1,1),(1,2),(2,1),(2,2),(3,1),(3,2),(4,1),(4,2),(5,2),(6,2),(7,2),(8,1)]:
        C=build_m2(k,m); Z=all_inputs(C.n) if C.n<=20 else adversarial_inputs(k,m,nrand=8000)
        ok,marg,bad=check(C,Z)
        print(f"(k,m)=({k},{m}) n={C.n} gates={C.size()} (d')={build_dp(k,m).size()} inputs={len(Z)} {'exhaustive' if C.n<=20 else 'adversarial'} correct={ok} wrong={bad} min|P|={marg}",flush=True)
