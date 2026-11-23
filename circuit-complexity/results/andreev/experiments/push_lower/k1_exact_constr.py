"""Verify the explicit exact-model k=1 construction of report §4 for m=1..40 (exact rationals):
   x_{s mod 2} = s + x0 - sum_{j=1}^{2*ceil(m/2)} [ s >= p_j(x) ],
   p_{2i-1} = 2i - 3/2 - (3/10) x0 + (3/4) x1 ,  p_{2i} = 2i - 1/2 - (3/5) x0 + (2/5) x1."""
from fractions import Fraction as F
import math
def p(j,x0,x1):
    i=(j+1)//2
    return (F(2*i)-F(3,2)-F(3,10)*x0+F(3,4)*x1) if j%2 else (F(2*i)-F(1,2)-F(3,5)*x0+F(2,5)*x1)
bad=0
for m in range(1,41):
    G=2*math.ceil(m/2)
    for x0 in (0,1):
        for x1 in (0,1):
            for s in range(m+1):
                val=s+x0-sum(1 for j in range(1,G+1) if s>=p(j,x0,x1))
                if val!=(x0,x1)[s%2]: bad+=1
print('k=1 exact construction: mismatches over m=1..40:',bad)
