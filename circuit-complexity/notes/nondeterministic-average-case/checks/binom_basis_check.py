"""Approximate inclusion-exclusion for Theorem F2: r(p) = q(p/D) with the Chebyshev step q of degree d
(alpha = 1/D).  Write r(p) = sum_{j=1}^d c_j binom(p,j) (Newton forward differences).  Report
delta = max_{1<=p<=D} |r(p)-1| (r(0)=0 exactly) and B = sum_j |c_j| binom(D,j) (error amplification)."""
from fractions import Fraction as Fr
import math, sys
sys.path.insert(0, sys.argv[1])
from cheb_check import cheb_coeffs, compose_lin
def run(D, d):
    al = Fr(1, D); a = (1+al)/(1-al); c = 2/(1-al)
    P = compose_lin(cheb_coeffs(d), a, c); Ta = P[0]
    q = [-x/Ta for x in P]; q[0] += 1
    r = lambda p: sum(qi*Fr(p, D)**i for i, qi in enumerate(q))
    vals = [r(p) for p in range(d+1)]
    cs = []
    for j in range(d+1):
        cs.append(sum((-1)**(j-i)*math.comb(j,i)*vals[i] for i in range(j+1)))
    assert cs[0] == 0
    delta = max(abs(float(r(p))-1) for p in range(1, D+1))
    B = sum(abs(float(cs[j]))*math.comb(D, j) for j in range(1, d+1))
    return delta, B
for D in (16, 64, 256, 1024):
    for d in sorted({max(1,int(math.sqrt(D))//2), int(math.sqrt(D)), 2*int(math.sqrt(D))}):
        delta, B = run(D, d)
        print(f"D={D:5d} d={d:3d}: delta={delta:.3e}  B={B:.3e}  B^(1/d)={B**(1/d):.2f}")
