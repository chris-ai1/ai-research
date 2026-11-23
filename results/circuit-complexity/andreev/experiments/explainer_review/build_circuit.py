#!/usr/bin/env python3
# Copyright (c) 2026 Christian Reitwiessner.
# Authors: Christian Reitwiessner
"""Independent rebuild of the 5/16 circuit from the text of Theorem 5 (thm:exact).

Pure Python (the numpy in /tmp/pydeps has no compiled extensions).
Gates are stored as (table-weight tuple, block-coefficient tuple, threshold) -> top coefficient.
Every block is seen only through its count s_i, so on raw address bits a gate has
weight blockcoef[i] on every bit of block i.  We check
  * gate-level score == closed form (bestclosed) on all tables x all block counts,
  * the same on raw address vectors for small cases,
  * output [-P>=0] == x_b and margin >= N,
  * gate count vs formula (bestcount), with a per-category breakdown,
  * all block coefficients >= 0 (sign-coherence),
  * sizes of bottom weights / thresholds / top coefficients.
Run: python3 -I build_circuit.py
"""
from itertools import product
import json, random, sys

def popcount(v):
    return bin(v).count('1')

def build(k, m):
    N = 1 << k; n = N + k * m; alpha = (m - 1) // 2; B = n + 2
    R = 2 * (N - 1) + 2 * alpha * k + k * m; C = N * (R + 4)
    e = [1 << i for i in range(k)]
    gates = {}; cat = {}
    def add(tw, bc, th, coef, category):
        key = (tuple(tw), tuple(bc), th)
        gates[key] = gates.get(key, 0) + coef
        cat.setdefault(key, set()).add(category)
    for S in range(1, N):
        size = popcount(S)
        bc = [(S >> i) & 1 for i in range(k)]
        tw = [2 * (popcount(S & c) % 2) + 2 * alpha * int(c in e and (S & c) != 0) for c in range(N)]
        kap = -4 * (2 * alpha + 1) * (k - 2 * size)
        for th in range(1, N + 2 * alpha * size + size * m + 1, 2):
            add(tw, bc, th, -8 * th + kap, 'main')
        tw0 = [B] + [0] * (N - 1)
        assert (4 * C) % N == 0
        for j in range(1, size * m // 2 + 1):
            add(tw0, bc, B + 2 * j, -(4 * C) // N, 'x0corr_tS')
    tww = [0] + [2 + 2 * alpha * int(c in e) for c in range(1, N)]
    for th in range(1, R + 1):
        add(tww, [1] * k, th, (N // 2) * (2 * th - 1), 'w_square')
    for i in range(k):
        bci = [int(j == i) for j in range(k)]
        for th in range(1, m + 1):
            add([0] * N, bci, th, (N // 2) * (2 * th - 1), 's_square')
            add([B * int(c == e[i]) for c in range(N)], bci, B + th, 2 * N * (1 + alpha), 'product')
    for l in range(1, k * m + 1):
        add([B] + [0] * (N - 1), [1] * k, B + l, C, 'x0corr_sigma')
    gates = {key: v for key, v in gates.items() if v != 0}
    dt = [-C] + [4 * N - 2 * N * (alpha ** 2 + 1) * int(c in e) for c in range(1, N)]
    db = [-2 * alpha * N] * k
    # group by form for fast evaluation
    forms = {}
    for (tw, bc, th), coef in gates.items():
        forms.setdefault((tw, bc), []).append((th, coef))
    return dict(k=k, m=m, N=N, n=n, alpha=alpha, B=B, R=R, C=C, e=e, gates=gates, cat=cat,
                dt=dt, db=db, const=2 * N, forms=forms)

def formula(k, m):
    N = 1 << k; alpha = (m - 1) // 2
    return N * (N - 1) // 2 + k * N * (m + alpha) // 2 + 2 * (N - 1) + 2 * alpha * k + 3 * k * m + (k * m + 1) // 2

def dot(u, v):
    return sum(a * b for a, b in zip(u, v))

def make_evaluator(c, tables, counts_or_raw, raw=False):
    """returns P as dict over (table index, address index)"""
    k, m = c['k'], c['m']
    lists = []
    for (tw, bc), ths in c['forms'].items():
        ths.sort()
        tvals = [dot(tw, x) for x in tables]
        if raw:
            bw = [w for w in bc for _ in range(m)]
        else:
            bw = bc
        bvals = [dot(bw, a) for a in counts_or_raw]
        lists.append((tvals, bvals, [t for t, _ in ths], [cf for _, cf in ths]))
    dtv = [dot(c['dt'], x) for x in tables]
    dbw = [w for w in c['db'] for _ in range(m)] if raw else c['db']
    dbv = [dot(dbw, a) for a in counts_or_raw]
    import bisect
    # prefix sums
    pref = []
    for tvals, bvals, ths, cfs in lists:
        ps = [0]
        for cf in cfs:
            ps.append(ps[-1] + cf)
        pref.append((tvals, bvals, ths, ps))
    def P(ti, ai):
        tot = c['const'] + dtv[ti] + dbv[ai]
        for tvals, bvals, ths, ps in pref:
            L = tvals[ti] + bvals[ai]
            tot += ps[bisect.bisect_right(ths, L)]
        return tot
    return P

def closed(c, x, s):
    k, N, alpha, C = c['k'], c['N'], c['alpha'], c['C']
    b = sum((s[i] % 2) << i for i in range(k))
    z = sum(x[1:]); E = sum(x[ei] for ei in c['e']); sig = sum(s)
    w = 2 * z + 2 * alpha * E + sig
    assert 0 <= w <= c['R']
    if b == 0:
        return N * (w + 2) - C * x[0]
    if b & (b - 1) == 0:
        i = b.bit_length() - 1
        return 2 * N * (1 + alpha) * (1 - x[b]) - N * s[i]
    return N * (1 - 2 * x[b])

def check(c, tables, counts):
    P = make_evaluator(c, tables, counts)
    margin = None; correct = True; closed_ok = True
    for ti, x in enumerate(tables):
        for ai, s in enumerate(counts):
            p = P(ti, ai)
            if p != closed(c, x, s):
                closed_ok = False
            b = sum((s[i] % 2) << i for i in range(c['k']))
            if int(-p >= 0) != x[b]:
                correct = False
            sm = (1 - 2 * x[b]) * p
            margin = sm if margin is None else min(margin, sm)
    return closed_ok, correct, margin

def stats(c):
    cats = {}
    for key in c['gates']:
        for t in c['cat'][key]:
            cats[t] = cats.get(t, 0) + 1
    coh = all(min(bc) >= 0 for (tw, bc, th) in c['gates'])
    maxb = max(max(abs(v) for v in tw + bc) for (tw, bc, th) in c['gates'])
    maxth = max(abs(th) for (tw, bc, th) in c['gates'])
    maxtop = max([abs(v) for v in c['gates'].values()] + [abs(v) for v in c['dt'] + c['db']])
    return dict(gates=len(c['gates']), formula=formula(c['k'], c['m']), cats=cats, coherent_nonneg=coh,
                max_bottom_weight=maxb, max_threshold=maxth, max_top=maxtop, n=c['n'], N=c['N'], C=c['C'])

if __name__ == '__main__':
    report = {}
    total_cases = 0
    for k in range(1, 4):
        for m in range(1, 7):
            c = build(k, m)
            tables = list(product((0, 1), repeat=c['N']))
            counts = list(product(range(m + 1), repeat=k))
            closed_ok, correct, margin = check(c, tables, counts)
            st = stats(c)
            st.update(cases=len(tables) * len(counts), closed_ok=closed_ok, correct=correct, margin=margin)
            if m <= 4:
                total_cases += len(tables) * len(counts)
            report[f'k={k},m={m}'] = st
            print(f'k={k} m={m}', st, flush=True)
    print('total exhaustive cases for k<=3, m<=4:', total_cases)

    # raw address vectors: every a in {0,1}^{km}
    for k, m in [(1, 1), (1, 4), (2, 2), (2, 3), (3, 2), (3, 3)]:
        c = build(k, m)
        tables = list(product((0, 1), repeat=c['N']))
        raws = list(product((0, 1), repeat=k * m))
        P = make_evaluator(c, tables, raws, raw=True)
        ok = True; margin = None
        for ti, x in enumerate(tables):
            for ai, a in enumerate(raws):
                s = [sum(a[i * m:(i + 1) * m]) for i in range(k)]
                b = sum((s[i] % 2) << i for i in range(k))
                p = P(ti, ai)
                ok &= (int(-p >= 0) == x[b]) and p == closed(c, x, s)
                sm = (1 - 2 * x[b]) * p
                margin = sm if margin is None else min(margin, sm)
        print('raw', k, m, 'ok', ok, 'margin', margin, 'N', c['N'], flush=True)

    # k=4,5: random tables x all block counts
    rng = random.Random(5)
    for k, m in [(4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (5, 2), (5, 3)]:
        c = build(k, m)
        tables = [tuple([0] * c['N']), tuple([1] * c['N'])] + [tuple(rng.randrange(2) for _ in range(c['N'])) for _ in range(60)]
        counts = list(product(range(m + 1), repeat=k))
        closed_ok, correct, margin = check(c, tables, counts)
        st = stats(c)
        st.update(sampled_tables=len(tables), closed_ok=closed_ok, correct=correct, margin=margin)
        report[f'k={k},m={m}'] = st
        print(f'sampled k={k} m={m}', st, flush=True)
    json.dump(report, open('/tmp/andreev_gap/explainer_review/build_circuit.json', 'w'), indent=1, default=str)
