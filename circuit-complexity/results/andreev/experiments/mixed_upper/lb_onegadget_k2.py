"""Exhaustive check of the claim: at k=2, F = D(x) + A_1(x) e_1 + A_2(x) e_2 + A_12(x) e_12 with
TWO-VALUED amplitudes A_S(x) in {+Delta_S, -Delta_S} (arbitrary functions of x, arbitrary Delta_S>0)
can never sign-represent x_b.  Proof sketch (in report): table 1100 forces Delta_2 > Delta_1, Delta_12;
table 1010 forces Delta_1 > Delta_2, Delta_12.  Here: brute force over sign choices for these two tables
and over a grid of Delta's, plus an LP over all sign choices for the two tables."""
import itertools
def ok_table(x,a,b,c):
    E=[0,a+c,b+c,a+b]   # addresses 00,10,01,11  (index = b1 + 2 b2)
    ones=[E[i] for i in range(4) if x[i]]; zeros=[E[i] for i in range(4) if not x[i]]
    return (not ones) or (not zeros) or min(ones)>max(zeros)
# table x listed as (x_00,x_10,x_01,x_11)
T1=(1,1,0,0); T2=(1,0,1,0)
grid=[0.25*i for i in range(1,41)]
bad=0
for D1 in grid:
  for D2 in grid:
    for D3 in grid:
      f1=any(ok_table(T1,s1*D1,s2*D2,s3*D3) for s1 in (1,-1) for s2 in (1,-1) for s3 in (1,-1))
      f2=any(ok_table(T2,s1*D1,s2*D2,s3*D3) for s1 in (1,-1) for s2 in (1,-1) for s3 in (1,-1))
      if f1 and f2: bad+=1
print('grid points where both tables 1100 and 1010 are satisfiable:',bad,'(expected 0)')
