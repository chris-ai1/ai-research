# (d''): no residue staircases at all.  The residue garbage at the weight-1 addresses e_i (= -N s_i) is
#   * centred by a FREE address function f(b) = N c' sum_i [b=e_i]  (coefficient shift kappa_S on the main ridge gates), and
#   * absorbed by amplifying x_{e_i} inside the main-ridge table forms: W_S = Y_S + alpha * sum_{i in S} x_{e_i},
#     alpha = floor((m_odd-1)/2) (m_odd = largest odd <= m), which raises the x_{e_i}-coefficient at b=e_i to 2N(1+alpha).
# Collapsed quadratics: 8 sum W^2 + 8 sum W t = (N/2)(w^2 - sigma^2) + lin + (2+2alpha)N sum_i x_{e_i}s_i,  w = 2|x'| + 2alpha E + sigma,
# E = sum_i x_{e_i};  the residue's collapsible part (N/2)(sigma^2 + sum s_i^2) + N sigma + N is added explicitly (sigma^2 cancels).
# Closed form:  b=0: N + 2N|x'| + 2 alpha N E + N(sigma+1) - Cov x0 ;  b=e_i: N(1+c') - 2N(1+alpha) x_{e_i} - N s_i ;  else N - 2N x_b.
import sys; sys.path.insert(0,'/tmp/andreev_gap/push_upper'); sys.path.insert(0,'/tmp/pydeps')
import numpy as np
from circ import Circuit
from constr import forms, stair, cu
def params(m):
    modd=m if m%2 else m-1
    alpha=(modd-1)//2
    cp=m if m%2 else m-1          # centre c' in (modd-1, 2+2alpha)
    return modd,alpha,cp
def build_dpp(k,m):
    N,n,tw,yw,ex,blk=forms(k,m); C=Circuit(k,m); B=N+k*m+2
    modd,alpha,cp=params(m)
    xp=np.zeros(n,np.int64); xp[1:N]=1; sg=np.zeros(n,np.int64); sg[N:]=1
    Ev=np.zeros(n,np.int64)
    for i in range(k): Ev[1<<i]=1
    C.K+=N
    for S in range(1,N):
        sz=bin(S).count('1'); T=sz*m
        A=np.zeros(n,np.int64)
        for i in range(k):
            if S>>i&1: A[1<<i]=1
        W=yw(S)+alpha*A
        kap=-4*cp*(k-2*sz)                       # free address function N c' sum_i [b=e_i]
        stair(C,2*W+tw(S),0,N+2*alpha*sz+T,lambda u,kap=kap:-8*cu(u)**2+kap*cu(u),1)
        C.u+= -kap*W - (kap//2)*tw(S); C.K+= -(kap//4)
        for j in range(1,T//2+1): pass            # override gates added below with their coefficient
    C.K+= cp*k                                  # S=emptyset Fourier coefficient of the address function
    # 4 sum_S W_S  and linear parts of 8 sum W^2:
    C.u+= 2*N*xp + 2*alpha*N*Ev                  # 4 sum W_S
    C.u+= 2*N*xp + 4*alpha*N*Ev + 2*alpha*alpha*N*Ev
    stair(C,2*xp+2*alpha*Ev+sg,0,2*(N-1)+2*alpha*k+k*m,lambda u:u*u,N//2)   # (N/2) w^2   (the -(N/2)sigma^2 cancels)
    for i in range(k):
        for l in range(1,m+1): C.gate(blk(i)+B*ex(1<<i),l+B,(2+2*alpha)*N)  # (2+2alpha)N x_{e_i} s_i
    # residue collapsible part: (N/2) sum_i s_i^2 + N sigma + N    [(N/2) sigma^2 cancelled above]
    for i in range(k): stair(C,blk(i),0,m,lambda u:u*u,N//2)
    C.u+= N*sg; C.K+= N
    # override  -Cov x0 [b=0]
    Cov=2*N*N+2*alpha*N*k+N*k*m+2*N; cq=Cov//N
    assert Cov%N==0
    C.u+= -Cov*ex(0)
    for S in range(1,N):
        T=bin(S).count('1')*m
        for j in range(1,T//2+1): C.gate(tw(S)+B*ex(0),2*j+B,-4*cq)
    for l in range(1,k*m+1): C.gate(sg+B*ex(0),l+B,Cov)
    return C.finalize()
def count_dpp(k,m):
    N=1<<k; modd,alpha,cp=params(m); tot=0
    for S in range(1,N):
        sz=bin(S).count('1'); T=sz*m; kap=-4*cp*(k-2*sz)
        # odd thresholds th in [1, N+2 alpha sz+T], coefficient -8 th + kap  (vanishes iff kap = 8 th)
        R=N+2*alpha*sz+T
        tot+=sum(1 for th in range(1,R+1,2) if -8*th+kap!=0)
        tot+=T//2
    tot+=(2*(N-1)+2*alpha*k+k*m) + k*m + k*m + k*m - (k*m)//2
    return tot
def closed(k,m,Z):
    from circ import target
    N=1<<k; modd,alpha,cp=params(m); y,b=target(k,m,Z); X=Z[:,:N].astype(np.int64)
    s=np.stack([Z[:,N+i*m:N+(i+1)*m].sum(1) for i in range(k)],1).astype(np.int64); sig=s.sum(1)
    E=sum(X[:,1<<i] for i in range(k)); xpn=X[:,1:].sum(1)
    Cov=2*N*N+2*alpha*N*k+N*k*m+2*N
    P=N-2*N*y
    P=np.where(b==0, N+2*N*xpn+2*alpha*N*E+N*(sig+1)-Cov*X[:,0], P)
    for i in range(k):
        P=np.where(b==(1<<i), N*(1+cp)-2*N*(1+alpha)*X[:,1<<i]-N*s[:,i], P)
    return P
if __name__=='__main__':
    from circ import all_inputs, adversarial_inputs, check
    from constr2 import build_dp
    mode=sys.argv[1] if len(sys.argv)>1 else 'exh'
    if mode=='exh': pairs=[(1,m) for m in range(1,19)]+[(2,m) for m in range(1,9)]+[(3,m) for m in range(1,5)]+[(4,1)]
    else: pairs=[(4,2),(4,3),(4,4),(4,6),(4,8),(5,3),(5,4),(5,5),(5,6),(6,3),(6,4),(6,5),(6,6),(7,2),(7,3),(8,1)]
    for k,m in pairs:
        C=build_dpp(k,m); Z=all_inputs(C.n) if mode=='exh' else adversarial_inputs(k,m,nrand=6000 if k>=7 else 12000)
        ok,marg,bad=check(C,Z); P=C.eval(Z); cf=np.array_equal(P,closed(k,m,Z))
        print(f"(k,m)=({k},{m}) n={C.n} gates={C.size()} formula={count_dpp(k,m)} (d')={build_dp(k,m).size()} inputs={len(Z)} correct={ok} wrong={bad} min|P|={marg} P==closed={cf}",flush=True)
