#!/usr/bin/env python3
# Authors: Christian Reitwiessner
# Exact rational checks of the separated-direction dual in report Section 5.

from fractions import Fraction
from math import comb
from pathlib import Path
import json
import random

ROOT = Path('/tmp/andreev_gap/swarm/up2')


def kernel(M, t):
    if t % 2:
        return Fraction(0)
    return Fraction((-1) ** (t // 2) * comb(M // 2, t // 2), comb(M, t))


def sign_character(B, z):
    return (-1) ** ((B & z).bit_count())


def solve(A, b):
    n = len(b)
    mat = [[Fraction(v) for v in row] + [Fraction(t)] for row, t in zip(A, b)]
    for c in range(n):
        pivot = next(r for r in range(c, n) if mat[r][c])
        mat[c], mat[pivot] = mat[pivot], mat[c]
        scale = mat[c][c]
        mat[c] = [v / scale for v in mat[c]]
        for r in range(n):
            if r != c:
                scale = mat[r][c]
                mat[r] = [a - scale * v for a, v in zip(mat[r], mat[c])]
    return [row[-1] for row in mat]


def small_exact_certificate():
    M, B = 8, 15
    centers = [0, 15, 51, 85]
    K = [[kernel(M, (a ^ b).bit_count()) for b in centers] for a in centers]
    c = solve(K, [sign_character(B, z) for z in centers])
    assert c == [Fraction(35, 44)] * 4
    P = [sum((v * kernel(M, (z ^ s).bit_count()) for v, s in zip(c, centers)), Fraction(0))
         for z in range(2 ** M)]
    masses = [(1 - sign_character(B, z) * P[z]) / (2 ** M) for z in range(2 ** M)]
    assert min(masses) == 0 and all(v >= 0 for v in masses)
    normalizer = sum(masses)
    assert normalizer == Fraction(21, 22)
    masses = [v / normalizer for v in masses]
    signed = [v * sign_character(B, z) for z, v in enumerate(masses)]
    assert sum(masses) == 1 and sum(signed) == 0
    for i in range(M):
        assert sum(signed[z] * ((z >> i) & 1) for z in range(2 ** M)) == 0
    for s in centers:
        for t in range(M + 1):
            assert sum(signed[z] for z in range(2 ** M) if (z ^ s).bit_count() == t) == 0
        for t in range(M + 2):
            assert sum(signed[z] for z in range(2 ** M) if (z ^ s).bit_count() >= t) == 0
    certificate = {'authors': 'Christian Reitwiessner', 'M': M, 'target_subset_mask': B,
                   'center_bitmasks': centers, 'coefficients': [str(v) for v in c],
                   'normalizer_before_rescaling': str(normalizer),
                   'normalized_masses': [str(v) for v in masses],
                   'status': 'exact nonnegative dual for all radial functions and affine inputs'}
    (ROOT / 'separated_dual_certificate.json').write_text(json.dumps(certificate, indent=2) + '\n')
    return {'M': M, 'directions': len(centers), 'vertices': 2 ** M,
            'positive_masses': sum(v > 0 for v in masses), 'radial_shell_equalities': len(centers) * (M + 1),
            'threshold_equalities': len(centers) * (M + 2), 'affine_equalities': M + 1,
            'largest_abs_P': str(max(abs(v) for v in P))}


def theorem_hypothesis_check():
    rng = random.Random(2026111105)
    M, R = 64, 4
    B = 2 ** 32 - 1
    centers = []
    while len(centers) < R:
        z = rng.getrandbits(M)
        if all(M // 4 <= (z ^ s).bit_count() <= 3 * M // 4 for s in centers):
            centers.append(z)
    eta = Fraction(1, 3 ** (M // 16))
    assert R * eta <= Fraction(1, 8)
    assert max(abs(kernel(M, t)) for t in range(M // 8, 7 * M // 8 + 1)) <= eta
    assert max(abs(kernel(M, t)) for t in range(1, M)) <= Fraction(1, M - 1)
    K = [[kernel(M, (a ^ b).bit_count()) for b in centers] for a in centers]
    v = [sign_character(B, z) for z in centers]
    c = solve(K, v)
    assert max(abs(a) for a in c) <= Fraction(8, 7)
    assert all(sum(K[i][j] * c[j] for j in range(R)) == v[i] for i in range(R))
    assert Fraction(2, M - 1) + 2 * R * eta < 1
    q = comb(M, M // 2)
    norm = 1 - sum(Fraction(a) * b for a, b in zip(v, c)) / q
    assert norm > 0
    return {'M': M, 'directions': R, 'center_bitmasks': centers,
            'eta': str(eta), 'noncenter_pointwise_bound': str(Fraction(2, M - 1) + 2 * R * eta),
            'all_theorem_hypotheses': True, 'kernel_interpolation_exact': True}


def kernel_identity_checks():
    checks = 0
    for M in range(2, 65, 2):
        d = M // 2
        for t in range(M + 1):
            numerator = sum((-1) ** j * comb(t, j) * comb(M - t, d - j)
                            for j in range(max(0, d - (M - t)), min(t, d) + 1))
            assert Fraction(numerator, comb(M, d)) == kernel(M, t)
            if 0 < t < M:
                assert abs(kernel(M, t)) <= Fraction(1, M - 1)
            checks += 1
    return checks


def main():
    results = {'authors': 'Christian Reitwiessner', 'kernel_identities': kernel_identity_checks(),
               'small_exact_dual': small_exact_certificate(),
               'theorem_hypotheses': theorem_hypothesis_check(), 'status': 'all passed'}
    (ROOT / 'separated_dual_checks.json').write_text(json.dumps(results, indent=2) + '\n')
    print(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
