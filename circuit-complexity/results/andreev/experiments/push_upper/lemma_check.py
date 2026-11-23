# Computational checks of the lemmas used in the report.
import sys; sys.path.insert(0,'/tmp/pydeps'); import numpy as np, itertools
cu=lambda u:-((-u)//2)
# (L1) free address functions: adding kappa to every odd-threshold gate [t>=th] of a t-staircase adds kappa*ceil(t/2)
#      = kappa*t/2 + kappa/4 - (kappa/4)(-1)^t ; summed over S with kappa_S=-4U/N gives U*[b=0] + linear + const.
def L1(k,m,U):
    N=1<<k; bad=0
    for s in itertools.product(range(m+1),repeat=k):
        b=sum(((s[i]&1)<<i) for i in range(k)); sig=sum(s)
        tot=0; lin=0; const=0
        for S in range(1,N):
            t=sum(s[i] for i in range(k) if S>>i&1); kap=-4*U//N
            tot+=kap*cu(t)                 # what the modified gates add
            lin+=kap*t/2                   # removable linear part (sum_S t_S = (N/2) sigma)
            const+=kap/4
        if abs(tot-lin-const-(U*(b==0)-U/N))>1e-9: bad+=1
    return bad
print('L1 free b-function, bad points:',[L1(k,m,8*(1<<k)) for k,m in [(2,3),(3,2),(3,3),(4,2)]])
# (L2) residue garbage location: sum_S t_S e_S = (N/4) sigma [b!=0] + (N/4) sum_i s_i [b=e_i]
def L2(k,m):
    N=1<<k; bad=0
    for s in itertools.product(range(m+1),repeat=k):
        b=sum(((s[i]&1)<<i) for i in range(k)); sig=sum(s)
        lhs=sum(sum(s[i] for i in range(k) if S>>i&1)*(sum(s[i] for i in range(k) if S>>i&1)&1) for S in range(1,N))
        rhs=N/4*sig*(b!=0)+N/4*sum(s[i]*(b==(1<<i)) for i in range(k))
        bad+= abs(lhs-rhs)>1e-9
    return bad
print('L2 residue identity, bad points:',[L2(k,m) for k,m in [(2,3),(3,3),(4,2)]])
# (L3) Parseval: for any integer h(S) with h(S) odd iff i in S, sum_{b!=0} hhat(b)^2 >= N^2/4  (random search for counterexamples)
rng=np.random.default_rng(0); worst=1e18
for k in (3,4,5):
    N=1<<k; H=np.array([[(-1)**bin(S&b).count('1') for b in range(N)] for S in range(N)])
    for trial in range(2000):
        i=0; h=np.array([ (2*rng.integers(-3,4)+1) if (S>>i)&1 else 2*rng.integers(-3,4) for S in range(N)])
        hh=h@H; val=(hh[1:]**2).sum()/(N*N/4); worst=min(worst,val)
print('L3 min over random trials of sum_{b!=0} hhat^2/(N^2/4):',round(worst,3),'(>=1 expected)')
