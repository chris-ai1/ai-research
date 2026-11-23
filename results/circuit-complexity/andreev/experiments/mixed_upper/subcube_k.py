"""'Subcube-dominance' pattern (generalising Theorem G and the k=3 family):
character S gets one period-2 atom on t_S + x_c for every table address c with c_i = 0 for all i in S.
Slope = (kN/4)(3/2)^(k-1).  Test LP feasibility with LINEAR D(x), constraint generation over points."""
import sys; sys.path.insert(0,'/tmp/pydeps')
import numpy as np, itertools, time
from scipy.optimize import linprog
from scipy import sparse
k=int(sys.argv[1]); N=1<<k
atoms=[]
for S in range(1,N):
    for c in range(N):
        if c & S == 0: atoms.append((S,c))
print(f'k={k} atoms={len(atoms)} slope={sum(bin(S).count("1") for S,c in atoms)/2}',flush=True)
T=np.arange(1<<N,dtype=np.int64)
X=((T[:,None]>>np.arange(N)[None,:])&1).astype(np.int8)      # tables
par=lambda v: bin(v).count('1')&1
# points: (table t, address b);  atom value = (e_S(b) + x_c) mod 2
def rows(tidx,bidx):
    Xs=X[tidx].astype(np.float64)
    M=np.empty((len(tidx),len(atoms)))
    for j,(S,c) in enumerate(atoms):
        eS=np.array([par(S&b) for b in range(N)])[bidx]
        M[:,j]=(eS+X[tidx,c])%2
    sig=2*X[tidx,bidx].astype(np.float64)-1
    return M,Xs,sig
rng=np.random.default_rng(0)
nt=1<<N
act_t=rng.integers(0,nt,20000); act_b=rng.integers(0,N,20000)
for rnd in range(40):
    M,Xs,sig=rows(act_t,act_b)
    A=len(atoms)
    Aub=np.hstack([-sig[:,None]*M, sig[:,None]*M, -sig[:,None]*Xs, -sig[:,None]])
    c=np.concatenate([np.ones(2*A),np.zeros(N+1)])
    res=linprog(c,A_ub=sparse.csr_matrix(Aub),b_ub=-np.ones(len(sig)),bounds=[(0,None)]*(2*A)+[(None,None)]*(N+1),method='highs')
    if res.status!=0: print('round',rnd,'INFEASIBLE on active set',len(sig)); break
    w=res.x[:A]-res.x[A:2*A]; d=res.x[2*A:2*A+N]; d0=res.x[-1]
    # full check, chunked over tables
    bad_t=[];bad_b=[]
    for st in range(0,nt,4096):
        tt=np.arange(st,min(nt,st+4096))
        for b in range(N):
            bb=np.full(len(tt),b)
            Mb,Xb,sb=rows(tt,bb)
            val=sb*(Mb@w+Xb@d+d0)
            bad=np.nonzero(val<1-1e-7)[0]
            bad_t+=list(tt[bad]); bad_b+=[b]*len(bad)
    print(f'round {rnd}: active {len(sig)} violated {len(bad_t)}',flush=True)
    if not bad_t: print('FEASIBLE with linear D; weights',np.round(w,3).tolist(),'d',np.round(d,3).tolist(),'d0',round(d0,3)); break
    sel=rng.permutation(len(bad_t))[:20000]
    act_t=np.concatenate([act_t,np.array(bad_t)[sel]]); act_b=np.concatenate([act_b,np.array(bad_b)[sel]])
