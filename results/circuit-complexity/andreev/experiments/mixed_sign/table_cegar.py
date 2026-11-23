#!/usr/bin/env python3
"""CEGAR over TABLES for Andreev A_{k,m}, full model, S gates, class free|coherent.
Start from a table set closed under c -> c xor e_i; solve (z3, incremental); check the circuit on all
tables (exact); add the orbit of the failing tables; repeat.
  * UNSAT at any stage is a proof that S gates do not suffice for the sub-instance, hence for A_{k,m}.
  * SAT on all tables = a verified circuit (re-checked exactly on all points).
Symmetry breaking as in andreev_min.py (valid because the table set is always closed under the flips).
Usage: python3 -I table_cegar.py K M S [--init 0110,0001] [--cls free|coherent] [--tl SEC] [--seed N]
"""
import sys, os, time, argparse, itertools
sys.path.insert(0, '/tmp/pydeps'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import z3
from mscore import andreev_points, andreev_blocks, Enc, eval_circuit, fmt_circ

ap = argparse.ArgumentParser()
ap.add_argument('k', type=int); ap.add_argument('m', type=int); ap.add_argument('S', type=int)
ap.add_argument('--init', default='0110,0001')
ap.add_argument('--cls', default='free')
ap.add_argument('--tl', type=float, default=7200)
ap.add_argument('--seed', type=int, default=None)
o = ap.parse_args()
k, m, S = o.k, o.m, o.S
N = 1 << k


def orbit(t):
    out = {t}; grow = True
    while grow:
        grow = False
        for u in list(out):
            for i in range(k):
                u2 = tuple(u[c ^ (1 << i)] for c in range(N))
                if u2 not in out: out.add(u2); grow = True
    return out


blocks = andreev_blocks(k, m)
usym = []
for B in blocks:
    for a, b in zip(B, B[1:]): usym.append(('le', a, b))
    if o.cls == 'free':
        for d in B: usym.append(('ge0', d))
opts = dict(vsym=True, seed=o.seed, usym=usym)
if o.cls == 'coherent':
    opts.update(cls='coherent', blocks=blocks)
    def blocksum(e, blocks=blocks):
        for B in blocks: e.so.add(z3.Sum([e.u[d] for d in B]) >= 0)
    opts['extra'] = [blocksum]
allpts = andreev_points(k, m)
# dummy point list for Enc construction (dimension only)
e = Enc(allpts[:1], S, opts)
e.pts = []
tabs = set()
for t in o.init.split(','):
    tabs |= orbit(tuple(int(ch) for ch in t))
t0 = time.time(); rounds = 0
added_tabs = set()


def add_tables(ts):
    for t in ts:
        if t in added_tabs: continue
        added_tabs.add(t)
        for p, y in andreev_points(k, m, [t]):
            e.pts.append((p, y)); e.add_point(len(e.pts) - 1)


add_tables(sorted(tabs))
while True:
    rounds += 1
    rem = o.tl - (time.time() - t0)
    if rem <= 0:
        print(f'TABLE-CEGAR k={k} m={m} S={S} cls={o.cls}: UNKNOWN (time) tables={len(added_tabs)}', flush=True); break
    e.so.set('timeout', int(rem * 1000))
    r = e.so.check()
    dt = time.time() - t0
    if r == z3.unsat:
        print(f'TABLE-CEGAR k={k} m={m} S={S} cls={o.cls}: UNSAT on sub-instance with {len(added_tabs)} tables '
              f'({dt:.1f}s, {rounds} rounds) => {o.cls} circuits for A_{{{k},{m}}} need >= {S + 1} gates (proved)', flush=True)
        print('  tables:', sorted(''.join(map(str, t)) for t in added_tabs), flush=True)
        break
    if r != z3.sat:
        print(f'TABLE-CEGAR k={k} m={m} S={S} cls={o.cls}: UNKNOWN tables={len(added_tabs)} ({dt:.1f}s)', flush=True); break
    c = e.circuit(e.so.model())
    bad_tabs = set()
    for x in itertools.product((0, 1), repeat=N):
        if x in added_tabs: continue
        if eval_circuit(c, andreev_points(k, m, [x])):
            bad_tabs.add(x)
    print(f'  round {rounds}: SAT on {len(added_tabs)} tables, fails on {len(bad_tabs)} others ({dt:.1f}s)', flush=True)
    if not bad_tabs:
        bad = eval_circuit(c, allpts)
        assert not bad
        print(f'TABLE-CEGAR k={k} m={m} S={S} cls={o.cls}: SAT -- circuit VERIFIED exactly on all {len(allpts)} points '
              f'({dt:.1f}s)', flush=True)
        names = [f'x{c_}' for c_ in range(N)] + [f'a{i + 1}{l + 1}' for i in range(k) for l in range(m)]
        print(fmt_circ(c, names), flush=True)
        break
    # add the orbit of one failing table (the lexicographically first), keeps the set closed
    t = sorted(bad_tabs)[0]
    add_tables(sorted(orbit(t)))
