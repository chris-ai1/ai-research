#!/usr/bin/env python3
"""Check the depth-two threshold circuits for Andreev's function at gate level.

Parameters: k address blocks, N = 2^k data bits x, block size m (any m >= 1).
A(x, a) = x[b], where b_i is the parity of block i.

Every bottom gate is built as an explicit (weights, threshold) pair over the
input vector (x, a); the top gate is an explicit integer weight vector. No
Fourier shortcut is used during evaluation, so a passing run tests the actual
circuit rather than the identity it was derived from.

Sections:
  exact    : exact circuit, exhaustive for small sizes, random for k up to 6
  average  : windowed circuit on Fourier set T = subsets of [r]
"""
import argparse
import math
import numpy as np


def popcount(v):
    return bin(v).count("1")


class Circuit:
    def __init__(self, k, m):
        self.k, self.m, self.N = k, m, 1 << k
        self.inputs = self.N + k * m
        self.W, self.th, self.top = [], [], []
        self.top_threshold_sum = 0  # constant added to the top linear form

    def x_index(self, c):
        return c

    def a_index(self, i, j):
        return self.N + i * self.m + j

    def u_weights(self, S, sign):
        """Integer weights and constant of u = X_S + sign * t_S over (x, a)."""
        w = np.zeros(self.inputs, dtype=np.int64)
        const = 0
        for c in range(self.N):
            chi = -1 if popcount(S & c) % 2 else 1
            # X_S = sum_c chi * (1 - 2 x_c)
            const += chi
            w[self.x_index(c)] = -2 * chi
        for i in range(self.k):
            if S >> i & 1:
                for j in range(self.m):
                    w[self.a_index(i, j)] = sign
        return w, const

    def add_ramp(self, w, const, lo, hi, coeff):
        """Add coeff * phi(clamp(u, lo, hi)), phi(u) = (-1)^u u, via gates [u >= th]."""
        phi = lambda v: (-1 if v % 2 else 1) * v
        self.top_threshold_sum += coeff * phi(lo)
        for th in range(lo + 1, hi + 1):
            self.W.append(w)
            self.th.append(th - const)  # gate: w.z >= th - const
            self.top.append(coeff * (phi(th) - phi(th - 1)))

    def add_subset(self, S, window=None):
        size = popcount(S)
        for sign in (1, -1):
            w, const = self.u_weights(S, sign)
            if window is None:
                lo, hi = -self.N, self.N + size * self.m
                if sign == -1:
                    lo, hi = -self.N - size * self.m, self.N
            else:
                centre = sign * (size * self.m // 2)
                lo, hi = centre - window, centre + window
            self.add_ramp(w, const, lo, hi, 1)

    def finalize(self):
        self.Wm = np.array(self.W, dtype=np.int64)
        self.thv = np.array(self.th, dtype=np.int64)
        self.topv = np.array(self.top, dtype=np.int64)

    @property
    def gates(self):
        return len(self.th)

    def top_sum(self, Z):
        """Top linear form on a batch Z of inputs (rows)."""
        out = np.zeros(Z.shape[0], dtype=np.int64)
        B = 4096
        for s in range(0, self.gates, B):
            G = (Z @ self.Wm[s:s + B].T) >= self.thv[s:s + B]
            out += G.astype(np.int64) @ self.topv[s:s + B]
        return out + self.top_threshold_sum


def andreev(Z, k, m):
    N = 1 << k
    addr = np.zeros(Z.shape[0], dtype=np.int64)
    for i in range(k):
        par = Z[:, N + i * m: N + (i + 1) * m].sum(axis=1) % 2
        addr |= par.astype(np.int64) << i
    return Z[np.arange(Z.shape[0]), addr]


def exact_circuit(k, m):
    c = Circuit(k, m)
    for S in range(1 << k):
        c.add_subset(S)
    c.finalize()
    return c


def check_exact(k, m, samples, rng):
    c = exact_circuit(k, m)
    n_inputs = c.inputs
    if n_inputs <= 16:
        Z = ((np.arange(1 << n_inputs)[:, None] >> np.arange(n_inputs)) & 1).astype(np.int64)
        mode = "exhaustive"
    else:
        Z = rng.integers(0, 2, size=(samples, n_inputs), dtype=np.int64)
        # Adversarial mix: extreme Hamming weights, where windows would fail.
        Z[: samples // 4, c.N:] = 1
        Z[samples // 4: samples // 2, c.N:] = 0
        Z[samples // 2: 5 * samples // 8, : c.N] = 1
        mode = f"{samples} random+extreme"
    s = c.top_sum(Z)
    xi = 1 - 2 * andreev(Z, k, m)
    ok = np.array_equal(s, 2 * c.N * xi)  # sum over S of phi(u+)+phi(u-) = 2N xi_b
    bound = 4 * c.N ** 2 + k * m * c.N
    print(f"exact k={k} m={m} N={c.N} inputs={n_inputs} gates={c.gates} "
          f"(4N^2+kmN={bound}) {mode}: identity_holds={ok}")
    assert c.gates == bound
    assert ok


def central(L):
    """Pr[sum of L-1 signs = -1] = C(L-1, L/2) / 2^(L-1); L = 1 gives 1."""
    return 1.0 if L == 1 else math.comb(L - 1, L // 2) / 2 ** (L - 1)


def check_average(k, r, delta, samples, rng):
    N = 1 << k
    m = N // k
    t = 1 << r
    lam = math.sqrt(2 * N * math.log(4 * t / delta))
    window = math.ceil(2 * lam) + 1
    c = Circuit(k, m)
    for S in range(t):
        c.add_subset(S, window)
    c.finalize()
    agree = 0
    tot = 0
    B = 2000
    for _ in range(0, samples, B):
        Z = rng.integers(0, 2, size=(B, c.inputs), dtype=np.int64)
        out = (c.top_sum(Z) < 0).astype(np.int64)  # sum >= 0 means xi=+1, i.e. A=0
        agree += int((out == andreev(Z, k, m)).sum())
        tot += B
    frac = agree / tot
    corr = central(N // t)
    pred = 0.5 + corr / 2
    se = math.sqrt(frac * (1 - frac) / tot)
    print(f"avg k={k} N={N} r={r} t={t} window=+-{window} gates={c.gates} "
          f"gates/(t*sqrt(N log N))={c.gates / (t * math.sqrt(N * math.log(N))):.2f} "
          f"agree={frac:.4f}+-{se:.4f} predicted={pred:.4f} (delta={delta})")
    assert frac > pred - delta - 5 * se


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--seed", type=int, default=1)
    args = p.parse_args()
    rng = np.random.default_rng(args.seed)
    for k, m in [(1, 1), (1, 3), (2, 1), (2, 2), (2, 3), (3, 1), (3, 2), (3, 3), (4, 2), (4, 4), (5, 3), (6, 4)]:
        check_exact(k, m, 400, rng)
    for k, r in [(8, 0), (8, 2), (8, 4), (8, 6), (8, 8), (10, 2), (10, 4), (10, 6)]:
        check_average(k, r, 0.01, 4000, rng)
