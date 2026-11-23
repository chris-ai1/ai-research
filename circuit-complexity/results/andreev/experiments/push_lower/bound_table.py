"""Evaluate the explicit lower bounds of Corollary C in the balanced case km=N (n=2N), next to n^{3/2},
n^{3/2}/log2(n)^2 and the (5/16)n^2 upper bound.  Bounds are solved self-consistently in S (log2(S+1) term)."""
import math
def lb(k,m,split_frac):
    # smallest S with S*split_frac >= (2^k-k-1-L)/(k+L), L=log2(S+1)  (monotone in S)
    N=2**k; lo,hi=0,4*N*N
    f=lambda S: S*split_frac-(N-k-1-math.log2(S+1))/(k+math.log2(S+1))
    if f(hi)<0: return hi
    while hi-lo>1:
        mid=(lo+hi)//2
        if f(mid)>=0: hi=mid
        else: lo=mid
    return hi
print(f"{'k':>3} {'N':>12} {'n':>12} {'coherent LB':>12} {'blocksym LB':>12} {'n^1.5':>12} {'n^1.5/log^2':>12} {'5n^2/16':>12}")
for k in [10,16,20,24,30,36,40,50]:
    N=2**k; m=N//k; n=N+k*m
    coh=(m**k-(m-1)**k)/m**k if k<=12 else 1-(1-1/m)**k
    bs=min(k,2*math.sqrt(2*k))/m
    print(f"{k:>3} {N:>12.3e} {n:>12.3e} {lb(k,m,coh):>12.3e} {lb(k,m,bs):>12.3e} {n**1.5:>12.3e} {n**1.5/math.log2(n)**2:>12.3e} {5*n*n/16:>12.3e}")
