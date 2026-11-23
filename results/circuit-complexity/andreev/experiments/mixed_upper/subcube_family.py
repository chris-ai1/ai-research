"""Subcube-dominance family (generalises Theorem G of push_lower to all k).
For every table address c (support C) and every nonempty S subset of complement(C): the period-2 staircase
   gates [t_S + x_c >= 2j], j = 1..ceil(|S|m/2), top weight -2*lam_c,  linear term lam_c*(t_S + x_c).
D(x) = sum_c d_c x_c + d0 with d_c = lam_c (|c|<k), d_{1..1} = kap_k, d0 = -kap_k/2 - K'/2.
kap_j > sum_{t>=1} C(k-j,t) kap_{j+t}  (dominance),  lam_c = kap_{|c|} / 2^{k-|c|}.
Output [top > 0].  Gates: G(k,m) = sum_t C(k,t) 2^(k-t) ceil(t m/2);  slope k 3^(k-1)/2."""
import sys; sys.path.insert(0,'/tmp/andreev_gap/mixed_upper')
from build_periodic import build, verify_counts, verify_bits
from fractions import Fraction as Fr
from math import comb
def kappas(k):
    kap=[0]*(k+1); kap[k]=Fr(2)
    for j in range(k-1,-1,-1):
        kap[j]=1+sum(comb(k-j,t)*kap[j+t] for t in range(1,k-j+1))
    return kap
def family(k,m):
    N=1<<k; kap=kappas(k); atoms=[]; Kp=Fr(0); d=[Fr(0)]*N
    for c in range(N):
        j=bin(c).count('1')
        if j==k: d[c]=kap[k]; continue
        lam=kap[j]/2**(k-j); d[c]=lam; Kp+=kap[j]
        comp=[i for i in range(k) if not (c>>i)&1]
        for r in range(1,len(comp)+1):
            for S in __import__('itertools').combinations(comp,r):
                beta=tuple(1 if i in S else 0 for i in range(k))
                alpha=tuple(1 if cc==c else 0 for cc in range(N))
                atoms.append((beta,alpha,2,0,lam))
    d0=-kap[k]/2-Kp/2
    return build(k,[[m]]*k,atoms,None,linearD=(d,d0))
def G(k,m): return sum(comb(k,t)*2**(k-t)*(-(-t*m//2)) for t in range(1,k+1))
if __name__=='__main__':
    for k,ms,bitmax in [(2,range(1,31),8),(3,range(1,13),4),(4,[1,2,3],1)]:
        for m in ms:
            circ=family(k,m)
            okb=None
            if m<=bitmax: okb,_=verify_bits(k,[[m]]*k,circ)
            ok,mn,npts=verify_counts(k,[[m]]*k,circ) if (k<4 or m<=2) else (None,None,None)
            print(f'k={k} m={m} gates={len(circ[0])} formula={G(k,m)} counts_ok={ok} bits_ok={okb} min|top|={mn}',flush=True)
