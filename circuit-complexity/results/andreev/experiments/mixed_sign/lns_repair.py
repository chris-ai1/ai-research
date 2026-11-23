#!/usr/bin/env python3
"""Large-neighbourhood repair of near-solutions from the relaxation (nnsearch.train).
For a near-solution with hidden truth tables H (err <= E): freeze g_{j,p} = H[p,j] on every point p that is
farther than radius r (Hamming distance in the address bits, same table) from all misclassified points,
leave the rest free, and solve exactly with z3.  SAT => circuit, re-verified exactly on ALL points.
UNSAT for a given freezing proves nothing about the instance (it is a heuristic SAT-finder).
Usage: python3 -I lns_repair.py andreevsub:K,M,T1+T2 S [--seed N] [--tl SEC] [--radius R]
"""
import sys, os, time, argparse
sys.path.insert(0, '/tmp/pydeps'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, z3
from nnsearch import train
from mscore import andreev_points, andreev_blocks, Enc, eval_circuit, fmt_circ

ap = argparse.ArgumentParser()
ap.add_argument('inst'); ap.add_argument('S', type=int)
ap.add_argument('--seed', type=int, default=0); ap.add_argument('--tl', type=float, default=1800)
ap.add_argument('--maxerr', type=int, default=4); ap.add_argument('--steps', type=int, default=3000)
o = ap.parse_args()
kind, par = o.inst.split(':')
k, m, tl_ = par.split(','); k, m = int(k), int(m); N = 1 << k
tabs = set(tuple(int(ch) for ch in t) for t in tl_.split('+'))
grow = True
while grow:
    grow = False
    for t in list(tabs):
        for i in range(k):
            t2 = tuple(t[c ^ (1 << i)] for c in range(N))
            if t2 not in tabs: tabs.add(t2); grow = True
pts = andreev_points(k, m, sorted(tabs)); blocks = andreev_blocks(k, m)
X = np.array([p for p, _ in pts], float); y = np.array([t for _, t in pts])
rng = np.random.default_rng(o.seed)
t0 = time.time(); tries = 0
while time.time() - t0 < o.tl:
    Hs, err, params = train(X, y, o.S, rng, o.steps, 'free', blocks)
    if err > o.maxerr: continue
    A, th, v, u, tauv = params
    out = Hs @ v + X @ u - tauv[0]
    bad = np.where((out >= 0).astype(int) != y)[0]
    if len(bad) == 0: bad = np.array([0])
    for r in (1, 2, 3, 6):
        tries += 1
        # free points: same table as a bad point and address Hamming distance <= r
        free = set()
        for b in bad:
            for i in range(len(pts)):
                if np.all(X[i, :N] == X[b, :N]) and np.abs(X[i, N:] - X[b, N:]).sum() <= r:
                    free.add(i)
        e = Enc(pts, o.S, dict(vsym=False, seed=o.seed))
        for i in range(len(pts)): e.add_point(i)
        for i in range(len(pts)):
            if i not in free:
                for j in range(o.S):
                    e.so.add(e.g[(j, i)] == bool(Hs[i, j]))
        e.so.set('timeout', 60000)
        res = e.so.check()
        print(f'  near-solution err={err}, radius {r}: {len(free)} free points -> {res} (t={time.time() - t0:.0f}s)', flush=True)
        if res == z3.sat:
            c = e.circuit(e.so.model())
            badc = eval_circuit(c, pts)
            if not badc:
                print(f'FOUND {o.inst} S={o.S} by LNS repair, VERIFIED exactly on all {len(pts)} points', flush=True)
                names = [f'x{c_}' for c_ in range(N)] + [f'a{i + 1}{l + 1}' for i in range(k) for l in range(m)]
                print(fmt_circ(c, names), flush=True)
                sys.exit(0)
        if res == z3.sat: break
print(f'NOTFOUND {o.inst} S={o.S} (LNS tries={tries}, t={time.time() - t0:.0f}s)', flush=True)
