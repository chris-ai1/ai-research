#!/usr/bin/env python3
"""Heuristic SAT-side search: train a depth-2 net with sigmoid hidden units + skip connections
(annealed towards step functions), then CERTIFY exactly:
  1. take the step-function truth tables H_j of the trained hidden units,
  2. re-solve every hidden gate as an exact LP over the rationals (z3 QF_LRA, no Booleans) and the top
     gate given the H_j,
  3. verify the resulting rational circuit on all points with Fraction arithmetic.
Only step 3 matters for correctness; the net only proposes candidates.

Usage: python3 -I nnsearch.py INSTANCE S [--cls free|coherent|blocksym|pm1] [--restarts R] [--steps T]
       [--seed N] [--tl SEC] [--out FILE]
INSTANCE: andreev:K,M | parity:M
"""
import sys, os, time, json, argparse
sys.path.insert(0, '/tmp/pydeps'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import z3
from fractions import Fraction as F
from mscore import andreev_points, andreev_blocks, parity_points, eval_circuit, fmt_circ


def sigmoid(t):
    return 0.5 * (1 + np.tanh(0.5 * t))


def train(X, y, S, rng, steps, cls, blocks, lr=0.03, beta0=1.0, beta1=60.0, l2=1e-4):
    n, D = X.shape
    ys = 2 * y - 1.0
    A = rng.normal(0, 1, (S, D))
    if cls == 'blocksym':
        for B in blocks:
            A[:, B] = A[:, [B[0]]]
    signs = None
    if cls == 'coherent':
        signs = rng.choice([-1.0, 1.0], size=(S, len(blocks)))
    th = rng.normal(0, 1, S) + 0.5 * A.sum(1)
    v = rng.normal(0, 1, S)
    u = rng.normal(0, 0.3, D)
    tau = 0.0
    params = [A, th, v, u, np.array([tau])]
    m_ = [np.zeros_like(p) for p in params]
    v_ = [np.zeros_like(p) for p in params]
    b1, b2, eps = 0.9, 0.999, 1e-8
    for it in range(1, steps + 1):
        beta = beta0 * (beta1 / beta0) ** (it / steps)
        A, th, v, u, tauv = params
        Z = X @ A.T - th            # n x S
        H = sigmoid(beta * Z)
        out = H @ v + X @ u - tauv[0]
        # logistic loss with margin scale
        marg = ys * out
        sg = sigmoid(-marg)          # d loss / d marg = -sigmoid(-marg)
        dout = -(sg * ys) / n
        gv = H.T @ dout + l2 * v
        gu = X.T @ dout
        gtau = np.array([-dout.sum()])
        dH = np.outer(dout, v)
        dZ = dH * beta * H * (1 - H)
        gA = dZ.T @ X + l2 * A
        gth = -dZ.sum(0)
        grads = [gA, gth, gv, gu, gtau]
        for i, (p, g) in enumerate(zip(params, grads)):
            m_[i] = b1 * m_[i] + (1 - b1) * g
            v_[i] = b2 * v_[i] + (1 - b2) * g * g
            mh = m_[i] / (1 - b1 ** it); vh = v_[i] / (1 - b2 ** it)
            p -= lr * mh / (np.sqrt(vh) + eps)
        if cls == 'blocksym':
            for B in blocks:
                A[:, B] = A[:, B].mean(1, keepdims=True)
        elif cls == 'coherent':
            for bi, B in enumerate(blocks):
                sub = A[:, B] * signs[:, [bi]]
                A[:, B] = np.maximum(sub, 0) * signs[:, [bi]]
    A, th, v, u, tauv = params
    Hs = (X @ A.T >= th).astype(int)
    out = Hs @ v + X @ u - tauv[0]
    err = int(((out >= 0).astype(int) != y).sum())
    return Hs, err, params


def exact_gate(Xl, h, cls, blocks, timeout=60):
    """exact rational threshold gate realising truth table h on points Xl (margin 1), or None"""
    D = len(Xl[0])
    so = z3.SolverFor('QF_LRA'); so.set('timeout', timeout * 1000)
    a = [z3.Real(f'a{d}') for d in range(D)]; t = z3.Real('t')
    if cls == 'blocksym':
        for B in blocks:
            for d in B[1:]: so.add(a[d] == a[B[0]])
    for p, hv in zip(Xl, h):
        lin = z3.Sum([a[d] for d in range(D) if p[d]] + [z3.RealVal(0)])
        so.add(lin >= t if hv else lin <= t - 1)
    if so.check() != z3.sat:
        return None
    md = so.model()
    q = lambda x: md.eval(x, model_completion=True).as_fraction()
    return [q(x) for x in a], q(t)


def exact_top(Xl, y, Hs, timeout=120):
    S = Hs.shape[1]; D = len(Xl[0])
    so = z3.SolverFor('QF_LRA'); so.set('timeout', timeout * 1000)
    v = [z3.Real(f'v{j}') for j in range(S)]; u = [z3.Real(f'u{d}') for d in range(D)]; tau = z3.Real('tau')
    for p, yy, h in zip(Xl, y, Hs):
        top = z3.Sum([v[j] for j in range(S) if h[j]] + [u[d] for d in range(D) if p[d]] + [z3.RealVal(0)])
        so.add(top >= tau if yy else top <= tau - 1)
    if so.check() != z3.sat:
        return None
    md = so.model()
    q = lambda x: md.eval(x, model_completion=True).as_fraction()
    return [q(x) for x in v], [q(x) for x in u], q(tau)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('inst'); ap.add_argument('S', type=int)
    ap.add_argument('--cls', default='free')
    ap.add_argument('--restarts', type=int, default=200)
    ap.add_argument('--steps', type=int, default=4000)
    ap.add_argument('--seed', type=int, default=0)
    ap.add_argument('--tl', type=float, default=3600)
    ap.add_argument('--lr', type=float, default=0.03)
    ap.add_argument('--out', default=None)
    o = ap.parse_args()
    kind, par = o.inst.split(':')
    if kind == 'andreev':
        k, m = map(int, par.split(','))
        pts = andreev_points(k, m); blocks = andreev_blocks(k, m)
    elif kind == 'andreevsub':   # andreevsub:K,M,T1+T2+...  (closed under c -> c xor e_i)
        k, m, tl_ = par.split(','); k, m = int(k), int(m); N_ = 1 << k
        tabs = set(tuple(int(ch) for ch in t) for t in tl_.split('+'))
        grow = True
        while grow:
            grow = False
            for t in list(tabs):
                for i in range(k):
                    t2 = tuple(t[c ^ (1 << i)] for c in range(N_))
                    if t2 not in tabs: tabs.add(t2); grow = True
        pts = andreev_points(k, m, sorted(tabs)); blocks = andreev_blocks(k, m)
    else:
        M = int(par); pts = parity_points(M); blocks = [list(range(M))]
    Xl = [p for p, _ in pts]
    X = np.array(Xl, dtype=float); y = np.array([t for _, t in pts])
    rng = np.random.default_rng(o.seed)
    t0 = time.time(); best = None
    for r in range(o.restarts):
        if time.time() - t0 > o.tl: break
        Hs, err, params = train(X, y, o.S, rng, o.steps, o.cls, blocks, lr=o.lr)
        if best is None or err < best: best = err
        if err == 0 or err <= 2:
            # try exact certification (top re-fit can repair a few errors)
            gates = []
            ok = True
            for j in range(o.S):
                gj = exact_gate(Xl, Hs[:, j], o.cls, blocks)
                if gj is None: ok = False; break
                gates.append(gj)
            if not ok: continue
            top = exact_top(Xl, y, Hs)
            if top is None: continue
            circ = dict(bottom=gates, v=top[0], u=top[1], tau=top[2])
            bad = eval_circuit(circ, pts)
            if not bad:
                print(f'FOUND {o.inst} S={o.S} cls={o.cls} restart={r} t={time.time() - t0:.1f}s '
                      f'VERIFIED exactly on all {len(pts)} points', flush=True)
                print(fmt_circ(circ), flush=True)
                if o.out:
                    with open(o.out, 'w') as fh:
                        json.dump({kk: ([[str(a) for a in al], str(th)] if False else None) for kk in []}, fh)
                        fh.seek(0)
                        json.dump(dict(bottom=[[[str(a) for a in al], str(th)] for al, th in circ['bottom']],
                                       v=[str(a) for a in circ['v']], u=[str(a) for a in circ['u']],
                                       tau=str(circ['tau'])), fh)
                return
        if r % 10 == 0:
            print(f'  restart {r}: err={err} best={best} t={time.time() - t0:.0f}s', flush=True)
    print(f'NOTFOUND {o.inst} S={o.S} cls={o.cls} best_err={best} restarts={r + 1} t={time.time() - t0:.0f}s', flush=True)


if __name__ == '__main__':
    main()
