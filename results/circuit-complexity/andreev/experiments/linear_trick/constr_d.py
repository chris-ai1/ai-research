import sys; sys.path.insert(0,"/tmp/andreev_gap/linear_trick")
# construction (d): polarization  Y e = (Y+ceil(t/2))^2 - Y^2 - ceil(t/2)^2 - Y t ,  e = t mod 2
# 4Y(-1)^t = 4Y - 8 ceil((2Y+t)/2)^2 + 8Y^2 + 8 ceil(t/2)^2 + 8 Y t
# sum_S Y_S^2 = (N/4)(|x'|^2+|x'|),  sum_S Y_S t_S = (N/4)|x'| sigma + (N/4) sum_i x_{e_i} s_i
# override -2N^2 x0 [b=0] = -2N x0 - 2N sum_S x0 (1 - 2 t_S + 4 floor(t_S/2))   (x0-gated parity)
from common import *
cu=lambda u: -((-u)//2)          # ceil(u/2)
def build(k,m):
    N,n,tw,yw,ex=layout(k,m); gates=[]; K=float(N); lin=np.zeros(n)
    BIG=k*m+N+2
    xp=np.zeros(n); xp[1:N]=1                     # |x'| (all table bits except x_0)
    sg=np.zeros(n); sg[N:]=1                       # sigma
    for S in range(1,N):
        T=bin(S).count('1')*m
        c,l=stair(gates,2*yw(S)+tw(S),0,N+T,lambda u:cu(u)**2,-8.0); K+=c; lin+=l
        c,l=stair(gates,tw(S),0,T,lambda u:cu(u)**2,8.0); K+=c; lin+=l
        for j in range(1,T//2+1): gates.append((tw(S)+BIG*ex(0),2*j+BIG,-8.0*N))   # x0[t_S>=2j]
    lin+=4*(N/2)*xp                                   # 4 sum_S Y_S = 2N|x'|
    c,l=stair(gates,xp,0,N-1,lambda u:u*u+u,8*N/4); K+=c; lin+=l          # 8 sum Y_S^2
    # 8 sum_S Y_S t_S = 2N |x'| sigma + 2N sum_i x_{e_i} s_i ;  |x'|sigma = ((a+b)^2-(a-b)^2)/4
    c,l=stair(gates,xp+sg,0,N-1+k*m,lambda u:u*u,2*N/4); K+=c; lin+=l
    c,l=stair(gates,xp-sg,-k*m,N-1,lambda u:u*u,-2*N/4); K+=c; lin+=l
    for i in range(k):
        e=1<<i; bi=np.zeros(n); bi[N+i*m:N+(i+1)*m]=1
        for l_ in range(1,m+1): gates.append((bi+BIG*ex(e),l_+BIG,2.0*N))         # x_{e_i}[s_i>=l]
    # override
    lin+=-2.0*N*ex(0)*N                              # -2N x0 (S=empty) - 2N(N-1) x0
    for l_ in range(1,k*m+1): gates.append((sg+BIG*ex(0),l_+BIG,4.0*N*(N/2)))   # +4N x0 sum_S t_S = 2N^2 x0 sigma
    return gates,K,lin,N,n
def count_formula(k,m):
    N=1<<k; tot=0
    for S in range(1,N):
        T=bin(S).count('1')*m
        tot+=(N+T+1)//2 + (T+1)//2 + T//2
    return tot+(N-2)+(N-1+k*m)+(N-1+k*m)+k*m+k*m
if __name__=="__main__":
    for k,m in [(1,1),(1,2),(1,3),(1,5),(2,1),(2,2),(2,3),(2,4),(3,1),(3,2),(3,3),(4,1),(3,4),(4,3),(4,4),(5,3),(5,5),(6,3)]:
        gates,K,lin,N,n=build(k,m); Z,ex_=inputs(k,m,40000)
        P=evaluate(gates,K,lin,Z); xb=target(k,m,Z)
        ok=np.array_equal((P<0).astype(int),xb); marg=np.min(np.abs(P))
        print(f"k={k} m={m} N={N} n={n} gates={len(gates)} est={count_formula(k,m)} N^2/2+.75kmN={N*N/2+.75*k*m*N:.0f} (5/8-constr {(N-1)*(N+2)+3*k*m*N//2+1}) correct={ok} minmargin={marg:.2f} {'exhaustive' if ex_ else 'sampled'} {len(Z)}",flush=True)
