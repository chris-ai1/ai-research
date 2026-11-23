"""Check the Chebyshev one-sided step polynomial used in Theorem M:
q(t) = 1 - T_d(a - c t)/T_d(a), a=(1+al)/(1-al), c=2/(1-al): q(0)=0, |q-1| <= 2 exp(-2 d artanh(sqrt al))
on [al,1], and sum of |monomial coefficients| <= 1 + 2*((r+sqrt(r^2+1))/(a+sqrt(a^2-1)))^d, r=a+c."""
from fractions import Fraction as Fr
import math
def cheb_coeffs(d):
    T0, T1 = [Fr(1)], [Fr(0), Fr(1)]
    if d == 0: return T0
    for _ in range(d-1):
        T2 = [Fr(0)] + [2*c for c in T1]
        for i, c in enumerate(T0): T2[i] -= c
        T0, T1 = T1, T2
    return T1
def compose_lin(P, a, c):  # P(a - c t) monomial coeffs in t
    out = [Fr(0)]*len(P)
    for m, pm in enumerate(P):
        for i in range(m+1):
            out[i] += pm * math.comb(m, i) * a**(m-i) * (-c)**i
    return out
def main():
  ok = True
  for al in (Fr(1,16), Fr(1,4), Fr(1,2)):
      a = (1+al)/(1-al); c = 2/(1-al); r = a + c
      for d in (1,2,3,5,8):
          P = compose_lin(cheb_coeffs(d), a, c)
          Ta = sum(P[i]*0**i for i in range(len(P))) if True else None
          Ta = P[0]
          q = [-p/Ta for p in P]; q[0] += 1
          assert q[0] == 0
          err = 0.0
          for k in range(2001):
              t = float(al) + (1-float(al))*k/2000
              val = sum(float(qi)*t**i for i, qi in enumerate(q))
              err = max(err, abs(val-1))
          bound = 2*math.exp(-2*d*math.atanh(math.sqrt(float(al))))
          csum = sum(abs(float(x)) for x in q)
          cb = 1 + 2*((float(r)+math.sqrt(float(r)**2+1))/(float(a)+math.sqrt(float(a)**2-1)))**d
          ok &= err <= bound + 1e-12 and csum <= cb + 1e-9 and max(abs(float(x)) for x in q) >= 0
          print(f"alpha={float(al):.4f} d={d}: max|q-1| on [alpha,1]={err:.3e} <= {bound:.3e};  sum|q_j|={csum:.3e} <= {cb:.3e}")
  print("PASS" if ok else "FAIL")

if __name__ == '__main__':
  main()
