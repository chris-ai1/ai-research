import sys; sys.path.insert(0,"/tmp/andreev_gap/linear_trick")
# construction (c): 5/8 construction with the b=0 override replaced by an x_0-gated parity trick
from common import *
def build(k,m):
    N,n,tw,yw,ex=layout(k,m); gates=[]; K=float(N); lin=np.zeros(n)
    BIG=k*m+1
    for S in range(1,N):
        sz=bin(S).count('1'); T=sz*m
        c,l=stair(gates,2*yw(S)+tw(S),0,N+T,phi,2.0); K+=c; lin+=l     # 2 phi(2Y_S+t_S)
        c,l=stair(gates,tw(S),0,T,phi,-2.0); K+=c; lin+=l              # -2 phi(t_S)
        # override part for S: -2N x0 (-1)^{t_S} = -2N x0 (1-2 t_S) - 8N sum_j x0[t_S>=2j]
        for j in range(1,T//2+1): gates.append((tw(S)+BIG*ex(0),2*j+BIG,-8.0*N))
        lin+=-2.0*N*ex(0)            # -2N x0 * 1
        # +4N x0 t_S handled globally below
    lin+=-2.0*N*ex(0)                # S = empty: -2N x0
    # +4N x0 * sum_{S!=0} t_S = +4N*(N/2) * x0*sigma ; x0*sigma = sum_l x0[sigma>=l]
    # even l already present as gates of S=[k] (coef -8N each); add odd l and adjust even ones
    full=N-1; Tf=k*m
    for l in range(1,Tf+1):
        if l%2: gates.append((tw(full)+BIG*ex(0),l+BIG,2.0*N*N))
    # adjust even-l gates of S=full: they carry -8N, need extra +2N^2
    for idx,(w,th,d) in enumerate(gates):
        if np.array_equal(w,tw(full)+BIG*ex(0)) and (th-BIG)%2==0: gates[idx]=(w,th,d+2.0*N*N)
    return gates,K,lin,N,n
def formula(k,m):
    N=1<<k; return N*(N-1)+sum((bin(S).count('1')*m)*2+(bin(S).count('1')*m)//2 for S in range(1,N))+(k*m+1)//2
if __name__=="__main__":
    for k,m in [(1,1),(1,2),(1,3),(1,5),(2,1),(2,2),(2,3),(2,4),(3,1),(3,2),(3,3),(4,1),(3,4),(4,3),(4,4),(5,3),(5,5)]:
        gates,K,lin,N,n=build(k,m); Z,ex_=inputs(k,m,40000)
        P=evaluate(gates,K,lin,Z); xb=target(k,m,Z)
        ok=np.array_equal((P<0).astype(int),xb); marg=np.min(np.abs(P))
        print(f"k={k} m={m} N={N} n={n} gates={len(gates)} formula={formula(k,m)} (5/8-constr {(N-1)*(N+2)+3*k*m*N//2+1}) correct={ok} minmargin={marg:.1f} {'exhaustive' if ex_ else 'sampled'} {len(Z)}")
