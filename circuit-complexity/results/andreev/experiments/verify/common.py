"""Independent helpers: input enumeration, target function, exact model verification."""
import sys, itertools
sys.path.insert(0,'/tmp/pydeps')
from fractions import Fraction

def A_full(k,m,x,a):
    """x: tuple of N bits, a: tuple of k*m bits. b = sum_i (s_i mod 2) 2^i"""
    b=0
    for i in range(k):
        s=sum(a[i*m:(i+1)*m]); b |= (s&1)<<i
    return x[b]

def inputs(k,m,mode):
    """yield (feature vector, target). full: x + a bits. blocksym: x + (s_1..s_k)."""
    N=1<<k
    for x in itertools.product((0,1),repeat=N):
        if mode=='full':
            for a in itertools.product((0,1),repeat=k*m):
                yield x+a, A_full(k,m,x,a)
        else:
            for s in itertools.product(range(m+1),repeat=k):
                # reference: realise s as bits a = (1^s_i 0^{m-s_i}) and evaluate A on the actual bits
                a=tuple(1 if j<s[i] else 0 for i in range(k) for j in range(m))
                yield x+s, A_full(k,m,x,a)

def verify_circuit(k,m,mode,gates,v,u,tau):
    """gates: list of (alpha list[Fraction], theta Fraction); v,u,tau Fractions. Exact. Returns (ok, #inputs)."""
    cnt=0
    for p,out in inputs(k,m,mode):
        tot=Fraction(0)
        for (al,th),vj in zip(gates,v):
            if sum(a*c for a,c in zip(al,p))>=th: tot+=vj
        tot+=sum(uu*c for uu,c in zip(u,p))
        if (tot>=tau)!=bool(out): return False,cnt
        cnt+=1
    return True,cnt

def zq(val):
    """z3 rational -> Fraction"""
    return Fraction(val.numerator_as_long(),val.denominator_as_long())
