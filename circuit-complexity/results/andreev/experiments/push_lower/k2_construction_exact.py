"""Exact-rational verification of the k=2 block-symmetric circuit with 4*ceil(m/2)+m gates:
  gates  [s1 + x0 >= 2j] (top weight -4), [s1 + x2 >= 2j] (-2), j=1..ceil(m/2);
         [s2 + x0 >= 2j] (-4), [s2 + x1 >= 2j] (-2),           j=1..ceil(m/2);
         [s1 + s2 + x0 >= 2j] (-4),                           j=1..m;
  top:   F = sum v_j g_j + 5 s1 + 5 s2 + 8 x0 + 2 x1 + 3/2 x2 + x3 - 13/2 ,  output [F >= 0].
(table index c = b1 + 2 b2, b_i = s_i mod 2).  Correctness for ALL m follows from the gadget identity
 V t - 2V sum_{j<=ceil(T/2)} [t + x_c >= 2j] = V (-1)^{x_c} (t mod 2)   plus the finite 16x4 check below."""
from fractions import Fraction as F
import itertools
def circuit_value(m,x,s1,s2):
    J=(m+1)//2; tot=F(0)
    for j in range(1,J+1):
        tot+=-4*(s1+x[0]>=2*j)-2*(s1+x[2]>=2*j)-4*(s2+x[0]>=2*j)-2*(s2+x[1]>=2*j)
    for j in range(1,m+1): tot+=-4*(s1+s2+x[0]>=2*j)
    return tot+5*s1+5*s2+8*x[0]+2*x[1]+F(3,2)*x[2]+x[3]-F(13,2)
# finite check of the m-independent core: sign(D(x)+G(x,b)) == x_b
core_bad=0
for x in itertools.product((0,1),repeat=4):
    D=8*x[0]+2*x[1]+F(3,2)*x[2]+x[3]-F(13,2)
    for b1 in (0,1):
        for b2 in (0,1):
            X=lambda c:(-1)**x[c]
            G=(2*X(0)+X(2))*b1+(2*X(0)+X(1))*b2+2*X(0)*(b1^b2)
            if ((D+G)>=0)!=bool(x[b1+2*b2]): core_bad+=1
print('core 16x4 check errors:',core_bad)
for m in range(1,21):
    bad=sum(1 for x in itertools.product((0,1),repeat=4) for s1 in range(m+1) for s2 in range(m+1)
            if (circuit_value(m,x,s1,s2)>=0)!=bool(x[(s1&1)+2*(s2&1)]))
    print(f'm={m}: gates={4*((m+1)//2)+m}  errors={bad}')
