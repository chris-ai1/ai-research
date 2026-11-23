# Copyright (c) 2026 Christian Reitwiessner. All rights reserved.
# Authors: Christian Reitwiessner
"""Exact depth-two threshold circuits (THR o THR) with direct raw-input wires to the top gate.

Semantics, fixed for the whole package:

    g_j(z) = [ alpha_j . z >= theta_j ]                      bottom gates, j = 0..S-1
    C(z)   = [ sum_j v_j g_j(z) + u . z >= tau ]             top gate (reads the gates AND the inputs)

z ranges over {0,1}^n.  Every parameter is a Fraction; floats are rejected because they are inexact.

`int_form` turns one rational threshold constraint into an equivalent integer one,
Sum W_d z_d >= B, with gcd(W) = 1.  The only rounding is B = ceil(.), which is exact because the
left-hand side is an integer.  Constant gates (all weights zero) are kept and evaluated exactly.
"""
import json
import math
from fractions import Fraction

import numpy as np


def rat(x):
    if isinstance(x, float):
        raise TypeError('floats are inexact; use Fraction, int or a rational string')
    if isinstance(x, Fraction):
        return x
    return Fraction(x)


def int_form(weights, cutoff):
    """Return (W, B), integers, with  [sum w_d z_d >= cutoff] == [sum W_d z_d >= B]  for all z in Z^n
    with z >= 0 integer (in particular all 0/1 vectors).  gcd(W) = 1 unless all weights vanish."""
    ws = [rat(w) for w in weights]
    c = rat(cutoff)
    L = math.lcm(*[w.denominator for w in ws]) if ws else 1
    W = [int(w * L) for w in ws]
    g = 0
    for w in W:
        g = math.gcd(g, w)
    if g == 0:                      # constant gate [0 >= c]
        return [0] * len(W), (0 if c <= 0 else 1)
    W = [w // g for w in W]
    B = math.ceil(c * L / g)        # sum W z is an integer, so >= c*L/g  <=>  >= ceil(c*L/g)
    return W, B


class Circuit:
    def __init__(self, bottom, v, u, tau):
        self.bottom = [([rat(a) for a in al], rat(th)) for al, th in bottom]
        self.v = [rat(x) for x in v]
        self.u = [rat(x) for x in u]
        self.tau = rat(tau)
        if len(self.v) != len(self.bottom):
            raise ValueError('need one top weight per bottom gate')
        for al, _ in self.bottom:
            if len(al) != len(self.u):
                raise ValueError('bottom gate arity differs from the number of inputs')
        self._ib = None
        self._it = None

    # ------------------------------------------------------------------ basic data
    @property
    def n(self):
        return len(self.u)

    @property
    def S(self):
        return len(self.bottom)

    def int_bottom(self):
        if self._ib is None:
            self._ib = [int_form(al, th) for al, th in self.bottom]
        return self._ib

    def int_top(self):
        """(V, U, B): integer form of the top gate over the variables (g_0..g_{S-1}, z_0..z_{n-1})."""
        if self._it is None:
            W, B = int_form(self.v + self.u, self.tau)
            self._it = (W[:self.S], W[self.S:], B)
        return self._it

    def max_abs_coef(self):
        m = 0
        for W, B in self.int_bottom():
            m = max(m, abs(B), *(abs(w) for w in W)) if W else max(m, abs(B))
        V, U, B = self.int_top()
        m = max(m, abs(B), *(abs(w) for w in V + U)) if (V or U) else max(m, abs(B))
        return m

    def wires(self):
        """number of nonzero bottom weights plus nonzero top weights"""
        return sum(1 for al, _ in self.bottom for a in al if a) + sum(1 for x in self.v + self.u if x)

    # ------------------------------------------------------------------ exact evaluation
    def eval(self, z):
        z = [int(b) for b in z]
        g = [1 if sum(w for w, b in zip(W, z) if b) >= B else 0 for W, B in self.int_bottom()]
        V, U, B = self.int_top()
        t = sum(w for w, b in zip(V, g) if b) + sum(w for w, b in zip(U, z) if b)
        return 1 if t >= B else 0

    def eval_batch(self, Z):
        """Exact evaluation on the rows of a 0/1 matrix Z (shape (num, n)).  Uses float64 BLAS only when
        every partial sum is an integer of magnitude < 2^52 (then float64 arithmetic is exact), int64 when
        < 2^62, and Python integers otherwise."""
        Z = np.asarray(Z)
        ib = self.int_bottom()
        V, U, Bt = self.int_top()
        S = self.S
        if S:
            Wm = [W for W, _ in ib]
            Bb = [B for _, B in ib]
            bound_b = max(sum(abs(w) for w in W) + abs(B) for W, B in ib)
        else:
            bound_b = 0
        bound_t = sum(abs(w) for w in V + U) + abs(Bt)
        bound = max(bound_b, bound_t)
        if bound < 2 ** 52:
            dt = np.float64
        elif bound < 2 ** 62:
            dt = np.int64
        else:
            dt = object
        Zc = Z.astype(dt)
        if S:
            G = (Zc @ np.array(Wm, dtype=dt).T >= np.array(Bb, dtype=dt)).astype(dt)
            T = G @ np.array(V, dtype=dt) + Zc @ np.array(U, dtype=dt)
        else:
            T = Zc @ np.array(U, dtype=dt)
        return (T >= Bt).astype(np.int8)

    def gate_values(self, z):
        return [1 if sum(w for w, b in zip(W, z) if b) >= B else 0 for W, B in self.int_bottom()]

    # ------------------------------------------------------------------ (de)serialisation
    def to_json(self):
        s = lambda x: str(x)
        return dict(n=self.n, S=self.S,
                    bottom=[[[s(a) for a in al], s(th)] for al, th in self.bottom],
                    v=[s(x) for x in self.v], u=[s(x) for x in self.u], tau=s(self.tau))

    @staticmethod
    def from_json(d):
        if isinstance(d, str):
            d = json.loads(d)
        return Circuit([(al, th) for al, th in d['bottom']], d['v'], d['u'], d['tau'])

    @staticmethod
    def from_mscore(d):
        """mixed_sign/mscore.py format: dict(bottom=[(alpha, theta)], v, u, tau); same semantics."""
        return Circuit(d['bottom'], d['v'], d['u'], d['tau'])

    @staticmethod
    def from_push_upper(C):
        """push_upper/circ.py Circuit: integer gates [w.z >= th], top P = sum V g + u.z + K, output [P < 0].
        For integers, P < 0  <=>  -P >= 1, i.e. sum(-V) g + (-u).z >= 1 + K."""
        bottom = [([int(a) for a in w], int(t)) for w, t in zip(C.W, C.T)]
        return Circuit(bottom, [-int(v) for v in C.V], [-int(a) for a in C.u], 1 + int(C.K))

    def format(self, names=None, max_terms=None):
        nm = names or [f'z{d}' for d in range(self.n)]
        def lin(coefs, vars_):
            parts = [f'{c}*{x}' for c, x in zip(coefs, vars_) if c]
            if max_terms and len(parts) > max_terms:
                parts = parts[:max_terms] + [f'... ({len(parts) - max_terms} more)']
            return ' + '.join(parts) if parts else '0'
        lines = [f'  g{j} = [{lin(al, nm)} >= {th}]' for j, (al, th) in enumerate(self.bottom)]
        lines.append(f'  out = [{lin(self.v + self.u, [f"g{j}" for j in range(self.S)] + nm)} >= {self.tau}]')
        return '\n'.join(lines)
