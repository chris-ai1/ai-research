# Copyright (c) 2026 Christian Reitwiessner.
# Authors: Christian Reitwiessner
"""Support-wire upper count for the paper's exact 5/16 construction.

All counts are upper bounds: retain zero top-coefficient cuts, ignore
possible coincidences other than the documented sigma/S=[k] overlap.
Each main ridge reads N/2 table bits and m*j address bits: amplified
singleton entries already belong to its odd-character table half.
All auxiliary families are counted from the actual raw gates in the proof.

At M=km=N and even m, main-ridge input wires equal
 N^3/4-N^2/4 + N^2*(2*m-1)*k/4 + m*(m-1)*k*(k+1)*N/4.
The subset-override family contributes
 m^2*k*(k+1)*N/8 + m*k*N/4.
Other input wires and all top edges are O(n^2), except terms already
explicit above. Therefore total W <= (9/64+3/(64*k))*n^3+O(k*n^2)
at exact balance, and W <= (9/64+o(1))*n^3 at floor balance.
This improves a coefficient, not the cubic exponent.
"""
import json
from math import comb
from pathlib import Path


def counts(k,m):
    N=1<<k; M=k*m; n=N+M; a=(m-1)//2
    ridge=sum(comb(k,j)*((N+(m+2*a)*j+1)//2) for j in range(1,k+1))
    ridge_w=sum(comb(k,j)*((N+(m+2*a)*j+1)//2)*(N//2+m*j) for j in range(1,k+1))
    sub=sum(comb(k,j)*(m*j//2) for j in range(1,k+1))
    sub_w=sum(comb(k,j)*(m*j//2)*(m*j+1) for j in range(1,k+1))
    R=2*(N-1)+2*a*k+M
    G=ridge+R+3*M+sub-M//2
    formula=N*(N-1)//2+k*N*(m+a)//2+2*(N-1)+2*a*k+3*M+(M+1)//2
    assert G==formula
    Wbot=ridge_w+R*(N-1+M)+M*m+M*(m+1)+M*(M+1)+sub_w-(M//2)*(M+1)
    if M==N and m%2==0:
        main4=N**3-N**2+N**2*(2*m-1)*k+m*(m-1)*k*(k+1)*N
        sub8=m*m*k*(k+1)*N+2*m*k*N
        assert 4*ridge_w==main4 and 8*sub_w==sub8
    return {'k':k,'m':m,'n':n,'bottoms_upper':G,'input_to_bottom_upper':Wbot,
            'all_support_wires_upper':Wbot+G+n,'ratio_to_n_cubed':(Wbot+G+n)/n**3}

small=[counts(k,m) for k in range(1,7) for m in range(1,9)]
# Independently enumerate subsets for the two large families.
for k in range(1,6):
    for m in range(1,7):
        N=1<<k; a=(m-1)//2
        cuts=sum(((N+(m+2*a)*s.bit_count()+1)//2) for s in range(1,N))
        assert cuts==sum(comb(k,j)*((N+(m+2*a)*j+1)//2) for j in range(1,k+1))
balanced=[counts(k,(1<<k)//k) for k in [1,2,4,8,16,32]]
result={'Authors':'Christian Reitwiessner','status':'All combinatorial identities passed; underlying correctness is the existing paper proof.',
        'small_parameter_checks':len(small),'balanced_counts':balanced,'asymptotic_leading_constant':9/64,
        'limitations':'No subcubic bound; counts are upper bounds on literal compiled supports, not claims of minimal semantic fan-in.'}
Path(__file__).with_name('checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
