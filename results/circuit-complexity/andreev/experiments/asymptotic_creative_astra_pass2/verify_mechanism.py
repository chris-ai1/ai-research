# Authors: Christian Reitwiessner
"""Exact checks supporting report.md. No external solvers or dependencies."""
from clipping_probe import walsh
from fractions import Fraction
from itertools import product
import json
from pathlib import Path

OUT=Path(__file__).resolve().parent
A={1,2,4,8,15}
z=[1-2*int(i in A) for i in range(16)]
h=walsh(z)
assert z[0]==1 and h.count(-2)==10 and h.count(6)==6

# Universal spectrum formulas are proved in the report; these are independent
# finite implementation checks of both different extensions.
for M in (1,2,4,8,16,32,64):
    punctured=z+[1]*(16*(M-1))
    hp=walsh(punctured)
    expected=[16*M-10]+[-10]*(M-1)+[-2]*(10*M)+[6]*(5*M)
    assert sorted(hp)==sorted(expected)
    repeated=[v for v in z for _ in range(M)]
    hr=walsh(repeated)
    assert sorted(hr)==sorted([-2*M]*10+[6*M]*6+[0]*(16*M-16))
    for B in range(1,6*M+1):
        score=sum(max(-B,min(B,v)) for v in hr)
        assert score==6*min(B,6*M)-10*min(B,2*M)

# Exact raw-LTF equality interaction and clipped amplitude compiler.
checks=0
N=16
for B in range(1,7):
    T=6
    big=2*N+2*B+2
    for hval in range(-N,N+1):
        for t in range(T+1):
            twice=0
            for r in range(-B+1,B+1):
                L=2*hval-2*r+1
                for j in range(T+1):
                    diff=int(big*(t-j)+L>=0)-int(big*(t-j)-L>=0)
                    twice+=(-1)**j*diff
            assert Fraction(twice,2)==(-1)**t*max(-B,min(B,hval))
            checks+=1

# Modulation covariance and spike formulas underlying the affine-repair lemma.
for B in (1,2,3):
    def score(y,b):
        v=[max(-B,min(B,t)) for t in walsh(y)]
        return walsh(v)[b]
    base=score(z,0)
    for b in range(16):
        translated=[z[c^b] for c in range(16)]
        for r in range(16):
            modulated=[v*(-1)**((r & (c^b)).bit_count()) for c,v in enumerate(translated)]
            assert modulated[b]==1 and score(modulated,b)==base
        spike=[2*int(c==b)-1 for c in range(16)]
        assert score(spike,b)==15*min(2,B)-min(14,B)

result={'Authors':'Christian Reitwiessner','five_point_seed':z,'seed_spectrum':h,
        'spectrum_extensions':'passed, M=1,2,4,8,16,32,64',
        'raw_gate_checks':checks,'modulation_and_spike_checks':'passed'}
(OUT/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
