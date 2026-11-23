#!/usr/bin/env python3
# Copyright (c) 2026 Christian Reitwiessner.
# Authors: Christian Reitwiessner
"""Exact checks of scoped ETH-matrix transfers; no new circuit bound claimed."""
from fractions import Fraction as Q
from itertools import product
from math import comb
from pathlib import Path
import json


def binomial(z, j):
    v = Q(1)
    for i in range(j):
        v *= Q(z-i, i+1)
    return v


def interpolate(a, degree, z):
    return sum((-1)**a * (-2)**j * binomial(z-a, j)
               for j in range(degree+1))


def fwht(v):
    v = list(v)
    width = 1
    while width < len(v):
        for start in range(0, len(v), 2*width):
            for j in range(start, start+width):
                u, w = v[j], v[j+width]
                v[j], v[j+width] = u+w, u-w
        width *= 2
    return v


def character(s, c):
    return (-1)**((s & c).bit_count())


def cube_check(k, a, degree):
    N = 2**k
    eigenvalues = [character(s, (1 << k)-1)*interpolate(a, degree, s.bit_count())
                   for s in range(N)]
    kernel = [v/N for v in fwht(eigenvalues)]
    assert all(v == 0 for c, v in enumerate(kernel)
               if c.bit_count() < k-degree)
    assert fwht(kernel) == eigenvalues
    rank = sum(v != 1 for v in eigenvalues)
    assert rank == sum(comb(k, w) for w in range(k+1)
                       if interpolate(a, degree, w) != (-1)**w)
    reversed_s = [s for s, v in enumerate(eigenvalues) if v < 0]
    if k == 8:
        assert rank == 18 and eigenvalues[1] == -31
        y = [character(1, c) for c in range(N)]
        My = [v/N for v in fwht([u*v for u, v in zip(eigenvalues, fwht(y))])]
        assert all(z == -31*t for z, t in zip(My, y))
    return dict(k=k, interval=[a, a+degree], dimension=N, correction_rank=rank,
                spatial_support=sum(v != 0 for v in kernel),
                reversed_character_tables=len(reversed_s),
                eigenvalue_at_singleton=str(eigenvalues[1]))


def swap_check():
    # Four pairs of two-dimensional registers: dimension 4^4 = 256.
    # f(z)=1-2z+4*binom(z,2)=2z^2-4z+1; interval {0,1,2}.
    pairs = 4
    D = 4**pairs
    labels = list(product(range(4), repeat=pairs))
    index = {c:i for i,c in enumerate(labels)}
    exchange = (0, 2, 1, 3)
    perms = []
    for t in range(pairs):
        perms.append([index[c[:t]+(exchange[c[t]],)+c[t+1:]] for c in labels])
    full = [index[tuple(exchange[z] for z in c)] for c in labels]
    def twice_W(v):
        return [pairs*v[i]-sum(v[p[i]] for p in perms) for i in range(D)]
    def twice_M(v):
        w = twice_W(v)
        ww = twice_W(w)
        z = [2*u-4*t+s for u,t,s in zip(v,w,ww)]
        return [z[i] for i in full]
    local = [(1,0,0,0), (0,0,0,1), (0,1,1,0), (0,1,-1,0)]
    basis = []
    bad = []
    for types in product(range(4), repeat=pairs):
        v = []
        for c in labels:
            val = 1
            for t in range(pairs): val *= local[types[t]][c[t]]
            v.append(val)
        j = types.count(3)
        lam = (-1)**j * interpolate(0, 2, j)
        assert twice_M(v) == [2*lam*z for z in v]
        basis.append(v)
        if lam != 1: bad.append(v)
    # Check basis independence by exact orthogonality.
    for i, v in enumerate(basis):
        assert sum(z*z for z in v) > 0
        for w in basis[:i]: assert sum(a*b for a,b in zip(v,w)) == 0
    assert len(bad) == 13
    # Verify spatial support, including coincidences under partial swaps.
    nonzero = 0
    for col in range(D):
        v = [int(i == col) for i in range(D)]
        for row, entry in enumerate(twice_M(v)):
            if entry:
                nonzero += 1
                # Full label has local ordering (alpha,beta): 00,01,10,11.
                mismatches = sum((labels[col][t]//2) != (labels[row][t]%2)
                                 for t in range(pairs))
                assert mismatches <= 2
    return dict(register_pairs=pairs, dimension=D, interval=[0,2],
                correction_rank=len(bad), exact_eigenvectors_checked=len(basis),
                nonzero_matrix_entries=nonzero)


def repair_check():
    # Exhaustive arbitrary tables and raw addresses for A_(3,2).
    k, m, N = 3, 2, 8
    lam = [(-1)**s.bit_count()*interpolate(1,1,s.bit_count()) for s in range(N)]
    bad = [s for s in range(N) if lam[s] != 1]
    def phi(z): return (-1)**z*z
    cases = 0
    for y in product((-1,1), repeat=N):
        X = fwht(y)
        My = [v/N for v in fwht([u*v for u,v in zip(lam,X)])]
        for a in product((0,1), repeat=k*m):
            weights = [sum(a[i*m:(i+1)*m]) for i in range(k)]
            b = sum((w%2) << i for i,w in enumerate(weights))
            repair = Q(0)
            for s in bad:
                t = sum(weights[i] for i in range(k) if (s >> i)&1)
                gadget = phi(X[s]+t)-phi(t)
                assert gadget == X[s]*character(s,b)
                repair += (1-lam[s])*gadget/N
            assert My[b] + repair == y[b]
            cases += 1
    return dict(k=k,m=m,tables=2**N,raw_addresses=2**(k*m),
                exact_table_address_checks=cases,
                meaning='Exact residual only; main term My still needs a circuit.')


def slice_compiler_check():
    cases = 0
    for L in range(-20, 21):
        for y in (-1, 1):
            got = int(2*L+y >= 0)-int(2*L-y >= 0)
            assert got == y*int(L == 0)
            cases += 1
    for digits in product(range(-2, 3), repeat=5):
        packed = sum((5**i)*z for i, z in enumerate(digits))
        assert (packed == 0) == all(z == 0 for z in digits)
    return dict(gate_identity_checks=cases, radix_packing_checks=5**5)


if __name__ == '__main__':
    result = {'Authors':'Christian Reitwiessner', 'status':'passed',
              'scope':'Finite exact identities, not an improved Andreev upper bound',
              'cube_transfer':[cube_check(*p) for p in [(8,2,4),(12,3,6),(16,4,8)]],
              'original_swap_matrix':swap_check(), 'fourier_residual':repair_check(),
              'affine_slice_compiler':slice_compiler_check()}
    Path(__file__).with_name('verification.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))
