# Authors: Christian Reitwiessner
"""Verify scalable spectral witnesses with exact integer transforms."""
from clipping_probe import walsh
import itertools
import math
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent
BASE = [1,-1,-1,-1,-1,-1,1,1,-1,1,-1,1,-1,1,1,-1]

def verify():
    h = walsh(BASE)
    assert h.count(-2) == 10 and h.count(6) == 6 and h[0] == -2
    for M in (1,2,4,8,16,32,64):
        y = BASE + [1]*(16*(M-1))
        h = walsh(y)
        predicted = [16*M-18]+[-18]*(M-1)+[-2]*(9*M)+[6]*(6*M)
        assert sorted(h) == sorted(predicted)
        assert sum(h) == 16*M and y[0] == 1
        for Q in (1,2,4,8):
            lift = [v for v in y for _ in range(Q)]
            h_lift = walsh(lift)
            assert sorted(h_lift) == sorted([Q*v for v in h]+[0]*(len(lift)-len(y)))
    for M in (1,2,4,8,16,32,64):
        y = [v for v in BASE for _ in range(M)]
        h = walsh(y)
        for B in range(1,6*M+1):
            observed = sum(max(-B,min(B,v)) for v in h)
            expected = 6*min(B,6*M)-10*min(B,2*M)
            assert observed == expected
    print('Exact spectra and clipping formulas: all assertions passed.')

    # For alpha=1/2, choose M so the analytic upper bound is already negative.
    M=1024
    y = BASE + [1]*(16*(M-1))
    h = walsh(y)
    score=sum(math.copysign(math.sqrt(abs(v)),v) if v else 0 for v in h)
    formula=math.sqrt(16*M-18)+math.sqrt(18)-M*math.sqrt(2)*(math.sqrt(3)-3)**2
    assert abs(score-formula)<1e-7 and score<0
    print('Square-root witness:', {'N':16*M,'score':score,'true_bit':1})

    # Search a sharper punctured seed; this is a finite algebraic test, not an
    # asymptotic inference. An exact seed, if found, is used in a lift proof.
    best = (-1e100,None,None)
    for tail in itertools.product((-1,1),repeat=15):
        y=[1]+list(tail)
        h=walsh(y); h[0]-=16
        slope=sum(v*math.log(abs(v)) for v in h if v)
        if slope>best[0]: best=(slope,y,h)
    slope,y,h=best
    print('Best first-order seed:', {'slope':slope,'y':y,'spectrum_of_y_minus_one':h})
    (OUT/'shrinker_checks.json').write_text(json.dumps({'Authors':'Christian Reitwiessner','exact_spectrum_checks':'passed','sqrt_witness_N':16*M,'sqrt_score':score,'best_slope':slope,'best_seed':y,'best_punctured_spectrum':h},indent=2)+'\n')

if __name__=='__main__': verify()
