# Authors: Christian Reitwiessner
"""Exact integer probes of clipped Walsh reconstruction, not circuit searches."""
import itertools
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent

def walsh(v):
    v = list(v)
    h = 1
    while h < len(v):
        for start in range(0, len(v), 2*h):
            for j in range(start, start+h):
                a, b = v[j], v[j+h]
                v[j], v[j+h] = a+b, a-b
        h *= 2
    return v

def clip(v, B):
    return [max(-B, min(B, a)) for a in v]

if __name__ == '__main__':
    result = None
    for N in (2, 4, 8, 16):
        best = N+1
        for tail in itertools.product((-1, 1), repeat=N-1):
            y = [1] + list(tail)
            h = walsh(y)
            score = sum(clip(h, 1))
            best = min(best, score)
            if score < 0:
                result = dict(N=N, y=y, walsh=h, clipped=clip(h, 1), score_at_zero=score)
                break
        print('N', N, 'minimum examined score', best, 'strict failure', result is not None)
        if result:
            break
    if result is None:
        raise SystemExit('No strict witness found')
    (OUT/'clipping_witness.json').write_text(json.dumps({'Authors':'Christian Reitwiessner', **result}, indent=2)+'\n')
    print(json.dumps(result, indent=2))
