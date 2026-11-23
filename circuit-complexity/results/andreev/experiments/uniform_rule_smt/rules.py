# Copyright (c) 2026 Christian Reitwiessner.
# Authors: Christian Reitwiessner
"""Small exact coefficient-rule compiler. No solver and no derived circuit inputs.
Index ASTs contain only public size/index data; coefficient parameters enter affinely.
"""
from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import product


def ev(e, env):
    if isinstance(e, int):
        return e
    if isinstance(e, str):
        return env[e]
    op, *args = e
    if op == 'if':
        return ev(args[1] if ev(args[0], env) else args[2], env)
    a = [ev(x, env) for x in args]
    if op == '+': return sum(a)
    if op == '-': return a[0] - a[1]
    if op == '*':
        z = 1
        for x in a: z *= x
        return z
    if op == 'bit': return (a[0] >> a[1]) & 1
    if op == 'and': return a[0] & a[1]
    if op == 'xor': return a[0] ^ a[1]
    if op == 'parity': return a[0].bit_count() & 1
    if op == 'eq': return int(a[0] == a[1])
    if op == 'lt': return int(a[0] < a[1])
    if op == 'div':
        if a[1] <= 0: raise ValueError('positive index divisor required')
        return a[0] // a[1]
    if op == 'mod':
        if a[1] <= 0: raise ValueError('positive index modulus required')
        return a[0] % a[1]
    if op == 'pow':
        if a[1] < 0 or a[0] < 0: raise ValueError('natural powers only')
        # Prototype resource guard, NOT a mathematical restriction on LTFs.
        if a[1] * max(1, a[0].bit_length()) > 100000:
            raise ValueError('index power exceeds prototype bit budget')
        return a[0] ** a[1]
    raise ValueError('unknown index operation: ' + op)


@dataclass(frozen=True)
class Aff:
    base: object = 0
    terms: tuple = ()  # (shared parameter name, public index expression)

    def value(self, env, theta):
        return Q(ev(self.base, env)) + sum(
            (Q(theta[p]) * ev(f, env) for p, f in self.terms), Q(0))


@dataclass(frozen=True)
class GateType:
    ranges: tuple  # (name, exclusive upper bound AST), nested in this order
    alpha: Aff
    address: Aff
    threshold: Aff
    top: Aff


@dataclass(frozen=True)
class Gate:
    weights: tuple
    threshold: Q

    def value(self, z):
        return int(sum(w * b for w, b in zip(self.weights, z)) >= self.threshold)


@dataclass(frozen=True)
class Circuit:
    k: int
    m: int
    gates: tuple
    top: tuple
    direct: tuple
    threshold: Q

    def score(self, z):
        return sum(v*g.value(z) for v, g in zip(self.top, self.gates)) + sum(
            u*b for u, b in zip(self.direct, z)) - self.threshold

    def value(self, z):
        return int(self.score(z) >= 0)

    def stats(self):
        coeffs = [self.threshold, *self.top, *self.direct]
        for g in self.gates: coeffs.extend((*g.weights, g.threshold))
        return dict(bottoms=len(self.gates), total_gates=len(self.gates)+1,
                    wires=sum(w != 0 for g in self.gates for w in g.weights)
                    + sum(v != 0 for v in self.top) + sum(u != 0 for u in self.direct),
                    max_rational_bits=max(max(Q(v).numerator.bit_length(),
                                              Q(v).denominator.bit_length()) for v in coeffs))


@dataclass(frozen=True)
class Program:
    types: tuple
    direct_table: Aff
    direct_address: Aff
    top_threshold: Aff

    def compile(self, k, m, theta=None, gate_cap=100000, bit_cap=100000):
        if k < 1 or m < 1: raise ValueError('positive k,m required')
        theta = theta or {}
        N = 1 << k
        env = dict(k=k, m=m, N=N, n=N+k*m)
        def indices(ranges, e):
            if not ranges:
                yield e
                return
            name, bound = ranges[0]
            upper = ev(bound, e)
            if upper < 0: raise ValueError('negative gate range')
            for j in range(upper):
                yield from indices(ranges[1:], dict(e, **{name: j}))
        gates, top = [], []
        for gt in self.types:
            for e in indices(gt.ranges, env):
                if len(gates) >= gate_cap: raise ValueError('gate budget exceeded')
                weights = tuple(gt.alpha.value(dict(e, c=c), theta) for c in range(N))
                weights += tuple(gt.address.value(dict(e, i=i, t=t), theta)
                                 for i in range(k) for t in range(m))
                gates.append(Gate(weights, gt.threshold.value(e, theta)))
                top.append(gt.top.value(e, theta))
        direct = tuple(self.direct_table.value(dict(env, c=c), theta) for c in range(N))
        direct += tuple(self.direct_address.value(dict(env, i=i, t=t), theta)
                        for i in range(k) for t in range(m))
        out = Circuit(k, m, tuple(gates), tuple(top), direct,
                      self.top_threshold.value(env, theta))
        if out.stats()['max_rational_bits'] > bit_cap:
            raise ValueError('coefficient bit budget exceeded')
        return out


def rank_m2_program():
    """Archived permutation-rank identity, valid for m=2; not a balanced construction."""
    place = ('pow', 2, 'i')
    sign = ('-', ('*', 2, ('bit', 'j', 'i')), 1)
    gt = GateType((('j', 'N'),), Aff(('eq', 'c', 'j')),
                  Aff(('*', place, ('if', ('eq', 't', 0), 1, sign))),
                  Aff(('+', 'j', 1)), Aff(1))
    return Program((gt,), Aff(),
                   Aff(('if', ('eq', 't', 0), ('-', 0, place), 0)), Aff(1))


def target(k, m, z):
    N = 1 << k
    b = sum((sum(z[N+i*m:N+(i+1)*m]) % 2) << i for i in range(k))
    return z[b]


def exhaustive(circuit, max_n=20):
    n = (1 << circuit.k) + circuit.k*circuit.m
    if n > max_n: raise ValueError('exhaustive domain too large')
    checked = 0
    for z in product((0, 1), repeat=n):
        checked += 1
        if circuit.value(z) != target(circuit.k, circuit.m, z):
            return dict(status='COUNTEREXAMPLE', checked=checked, input=list(z))
    return dict(status='VERIFIED_FINITE', checked=checked)


def slice_pair(alpha, beta, w, d):
    """ell=beta+alpha.x must be odd-valued: odd beta and even alpha.
    Returns two raw gates whose difference is sign(ell)*[d+w.a=0].
    """
    if beta % 2 != 1 or any(a % 2 for a in alpha):
        raise ValueError('odd-valued table form required')
    if any(not isinstance(z, int) for z in [*alpha, beta, *w, d]):
        raise ValueError('integer slice inputs required')
    M = abs(beta) + sum(abs(a) for a in alpha) + 1
    address = [2*M*v for v in w]
    return (Gate(tuple(alpha+address), Q(-2*M*d-beta)),
            Gate(tuple([-a for a in alpha]+address), Q(-2*M*d+beta)))


def window(alpha, cutoff, signs, lo, hi):
    """Integer raw-table form h. L=number of complemented address bits set.
    Return (gates, weights) for parity(raw a)*(2[h>=cutoff]-1)*[lo<=L<=hi].
    """
    if any(s not in (-1, 1) for s in signs): raise ValueError('sign must be +/-1')
    if not 0 <= lo <= hi <= len(signs): raise ValueError('invalid window')
    if any(not isinstance(v, int) for v in [*alpha, cutoff]):
        raise ValueError('integer table form required')
    hmin, hmax = sum(min(a, 0) for a in alpha), sum(max(a, 0) for a in alpha)
    B = max(abs(hmin-cutoff), abs(hmax-cutoff)) + 1
    offset = signs.count(-1)
    mask_sign = (-1)**offset
    gates, weights = [], []
    for level in range(lo, hi+1):
        gates.append(Gate(tuple(alpha+[B*s for s in signs]), Q(B*(level-offset)+cutoff)))
        weights.append(2*mask_sign*(-1)**level)
    for level, weight in [(lo, -mask_sign*(-1)**lo),
                          (hi+1, -mask_sign*(-1)**hi)]:
        gates.append(Gate(tuple([0]*len(alpha)+signs), Q(level-offset)))
        weights.append(weight)
    return gates, weights


def globally_reorientable(gates, N, k, m):
    """Exact sign-consistency test including zeros. True means coherent after
    one global coordinate flip. It does NOT itself reject an exact circuit.
    """
    for i in range(k):
        adj = {}
        for j, g in enumerate(gates):
            for t in range(m):
                w = g.weights[N+i*m+t]
                if not w: continue
                u, v, s = ('g', j), ('t', t), (1 if w > 0 else -1)
                adj.setdefault(u, []).append((v, s))
                adj.setdefault(v, []).append((u, s))
        val = {}
        for start in adj:
            if start in val: continue
            val[start] = 1
            todo = [start]
            while todo:
                u = todo.pop()
                for v, s in adj[u]:
                    want = s * val[u]
                    if v in val:
                        if val[v] != want: return False
                    else:
                        val[v] = want
                        todo.append(v)
    return True


def smt_miter(circuit):
    """SMT-LIB QF_LRA fixed rational candidate miter, arbitrary raw bits.
    UNSAT certifies only this (k,m). Boolean input conditionals keep arithmetic linear.
    """
    n = (1 << circuit.k) + circuit.k*circuit.m
    def num(q):
        q = Q(q)
        if q < 0: return '(- ' + num(-q) + ')'
        return str(q.numerator) if q.denominator == 1 else f'(/ {q.numerator} {q.denominator})'
    def add(parts): return '(+ ' + ' '.join(parts) + ')' if parts else '0'
    def form(ws, names):
        return add([f'(ite {z} {num(w)} 0)' for w, z in zip(ws, names) if w])
    lines = ['; Copyright (c) 2026 Christian Reitwiessner.',
             '; Authors: Christian Reitwiessner', '(set-logic QF_LRA)']
    names = [f'z{r}' for r in range(n)]
    lines += [f'(declare-fun {z} () Bool)' for z in names]
    for j, g in enumerate(circuit.gates):
        lines.append(f'(define-fun g{j} () Bool (>= {form(g.weights, names)} {num(g.threshold)}))')
    top = add([form(circuit.top, [f'g{j}' for j in range(len(circuit.gates))]),
               form(circuit.direct, names)])
    lines.append(f'(define-fun out () Bool (>= {top} {num(circuit.threshold)}))')
    N = 1 << circuit.k
    for i in range(circuit.k):
        bits = names[N+i*circuit.m:N+(i+1)*circuit.m]
        p = bits[0]
        for b in bits[1:]: p = f'(xor {p} {b})'
        lines.append(f'(define-fun b{i} () Bool {p})')
    def mux(start, depth):
        if depth == 0: return names[start]
        return f'(ite b{depth-1} {mux(start+(1 << (depth-1)), depth-1)} {mux(start, depth-1)})'
    lines += [f'(assert (xor out {mux(0, circuit.k)}))', '(check-sat)']
    return '\n'.join(lines) + '\n'
