#!/usr/bin/env python3
# Copyright (c) 2026 Christian Reitwiessner. All rights reserved.
# Authors: Christian Reitwiessner
"""Exact symbolic checking of rational depth-two threshold circuits.

A target callback builds a Boolean circuit, rather than enumerating its truth table.
Candidate format matches mixed_sign/mscore.py: bottom, v, u, tau.
UNSAT means equivalence on the full Boolean domain; SAT returns a counterexample.
No solver UNKNOWN is treated as a proof. No floating-point weights are accepted.
"""
from fractions import Fraction
from functools import reduce
from math import gcd, lcm
import time
import z3


def rational(value):
    if isinstance(value, float):
        raise TypeError('Use Fraction, integer, or rational string; floats are inexact')
    return Fraction(value)


def threshold(features, weights, cutoff):
    if len(features) != len(weights):
        raise ValueError('Wrong threshold arity')
    weights = list(map(rational, weights))
    cutoff = rational(cutoff)
    scale = lcm(*(w.denominator for w in weights), cutoff.denominator)
    ints = [int(w * scale) for w in weights]
    bound = int(cutoff * scale)
    divisor = reduce(gcd, ints + [bound], 0) or 1
    ints = [w // divisor for w in ints]
    bound //= divisor
    terms = [(b, w) for b, w in zip(features, ints) if w]
    if not terms:
        return z3.BoolVal(0 >= bound)
    # The Python PB interface uses C-sized integers. Fall back to exact arbitrary
    # integer arithmetic for large rational models; never truncate coefficients.
    if max(abs(bound), *(abs(w) for _, w in terms)) < (1 << 30):
        return z3.PbGe(terms, bound)
    return z3.Sum([z3.If(b, w, 0) for b, w in terms]) >= bound


def parity(bits):
    return reduce(z3.Xor, bits, z3.BoolVal(False))


def andreev_target(k, m):
    """Ordinary Andreev; table index bits are little-endian, as in mscore.py."""
    if k < 0 or m < 1:
        raise ValueError('Require k >= 0, m >= 1')
    ntable = 1 << k
    def build(bits):
        if len(bits) != ntable + k * m:
            raise ValueError('Wrong input length')
        values = list(bits[:ntable])
        for i in range(k):
            address_bit = parity(bits[ntable+i*m:ntable+(i+1)*m])
            values = [z3.If(address_bit, values[j+1], values[j])
                      for j in range(0, len(values), 2)]
        return values[0]
    return build


def check(candidate, target, timeout_ms=10000):
    inputs = [z3.Bool(f'input_{i}') for i in range(len(candidate['u']))]
    if len(candidate['v']) != len(candidate['bottom']):
        raise ValueError('Wrong number of top coefficients')
    solver = z3.Solver()
    solver.set(timeout=timeout_ms)
    gates = []
    for j, (weights, cutoff) in enumerate(candidate['bottom']):
        gate = z3.Bool(f'bottom_{j}')
        solver.add(gate == threshold(inputs, weights, cutoff))
        gates.append(gate)
    output = threshold(gates + inputs, candidate['v'] + candidate['u'], candidate['tau'])
    solver.add(z3.Xor(output, target(inputs)))
    t0 = time.monotonic()
    result = solver.check()
    elapsed = time.monotonic() - t0
    if result == z3.unsat:
        return dict(status='VERIFIED', seconds=elapsed)
    if result == z3.sat:
        model = solver.model()
        point = tuple(int(z3.is_true(model.eval(b, model_completion=True))) for b in inputs)
        return dict(status='COUNTEREXAMPLE', point=point, seconds=elapsed)
    return dict(status='UNKNOWN', reason=solver.reason_unknown(), seconds=elapsed)


def parity_candidate(n):
    # sum(x) - 2 floor(sum(x)/2) is the parity bit.
    bottom = [([1]*n, 2*j) for j in range(1, n//2+1)]
    return dict(bottom=bottom, v=[-2]*len(bottom), u=[1]*n, tau=1)


if __name__ == '__main__':
    import json
    for n in (8, 12, 16):
        c = parity_candidate(n)
        print(json.dumps(dict(target='parity', inputs=n, bottom=len(c['bottom']),
                              **check(c, parity, timeout_ms=2000))), flush=True)
    # A symbolic checker can immediately refute a bad candidate on a domain far
    # too large to list. This is not a successful synthesis or a size lower bound.
    k, m = 8, 8
    c = dict(bottom=[], v=[], u=[1]+[0]*((1<<k)+k*m-1), tau=1)
    r = check(c, andreev_target(k,m), timeout_ms=2000)
    if r['status'] == 'COUNTEREXAMPLE':
        p = r['point']; index = sum((sum(p[(1<<k)+i*m:(1<<k)+(i+1)*m])%2)<<i for i in range(k))
        assert p[0] != p[index]
    r.pop('point', None)
    print(json.dumps(dict(target='andreev', k=k, m=m, inputs=len(c['u']), **r)), flush=True)
