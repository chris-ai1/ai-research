"""Second independent cross-check: MILP (HiGHS via scipy.optimize.milp), big-M, INTEGER weights with
the same proven Cramer bounds as cpsat_check.py (full: 0/1-determinant bound, blocksym: Hadamard).
Symmetry: v_j >= 0 (complement), v sorted (permutation).  SAT models are verified exactly.
usage: python3 -I milp_check.py MODE TL k,m [...] [--maxS 6]"""
import sys, os, time, math, argparse
sys.path.insert(0, '/tmp/pydeps'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import lil_matrix
from common import andreev_points, eval_circuit


def bounds(pts, mode, S):
    D = len(pts[0][0])
    if mode in ('full', 'thermo'):
        b01 = lambda d: math.isqrt((d + 1) ** (d + 1) // 4 ** d) + 1
        return b01(D + 1), b01(D + S + 1)
    R2 = max(sum(c * c for c in p) for p, _ in pts) + 1
    hb = lambda r2, d: math.isqrt((r2 + 1) ** d) + 1
    return hb(R2, D + 1), hb(R2 + S, D + S + 1)


def solve(k, m, mode, S, tl):
    pts = andreev_points(k, m, mode); P = len(pts); D = len(pts[0][0])
    Wb, Wt = bounds(pts, mode, S)
    pm = max(max(p) for p, _ in pts)
    Mb = Wb * (D * pm + 1) + 1
    # variable layout
    idx = {}; lo = []; hi = []; integ = []
    def var(name, l, h, i=1):
        idx[name] = len(lo); lo.append(l); hi.append(h); integ.append(i)
    for j in range(S):
        for d in range(D): var(('a', j, d), -Wb, Wb)
        var(('t', j), -Wb, Wb); var(('v', j), 0, Wt)
    for d in range(D): var(('u', d), -Wt, Wt)
    var('tau', -Wt * (S + D + 1), Wt * (S + D + 1))
    for pi in range(P):
        for j in range(S):
            var(('g', j, pi), 0, 1); var(('e', j, pi), 0, Wt, 0)
    nv = len(lo)
    rows = []; rl = []; ru = []
    def row(coefs, l, u):
        rows.append(coefs); rl.append(l); ru.append(u)
    for j in range(S - 1):
        row({idx[('v', j)]: 1, idx[('v', j + 1)]: -1}, -np.inf, 0)
    for pi, (p, out) in enumerate(pts):
        for j in range(S):
            lin = {idx[('a', j, d)]: p[d] for d in range(D) if p[d]}
            g = idx[('g', j, pi)]; e = idx[('e', j, pi)]; v = idx[('v', j)]; t = idx[('t', j)]
            c = dict(lin); c[t] = -1; c[g] = -Mb; row(c, -Mb, np.inf)       # g=1 -> lin-t >= 0
            c = dict(lin); c[t] = -1; c[g] = -Mb; row(c, -np.inf, -1)       # g=0 -> lin-t <= -1
            row({e: 1, v: -1}, -np.inf, 0)                                  # e <= v
            row({e: 1, g: -Wt}, -np.inf, 0)                                 # e <= Wt g
            row({e: 1, v: -1, g: -Wt}, -Wt, np.inf)                         # e >= v - Wt(1-g)
        c = {idx[('e', j, pi)]: 1 for j in range(S)}
        for d in range(D):
            if p[d]: c[idx[('u', d)]] = p[d]
        c[idx['tau']] = -1
        row(c, 0, np.inf) if out else row(c, -np.inf, -1)
    A = lil_matrix((len(rows), nv))
    for r, cs in enumerate(rows):
        for col, val in cs.items(): A[r, col] = val
    res = milp(np.zeros(nv), constraints=LinearConstraint(A.tocsr(), rl, ru), bounds=Bounds(lo, hi),
               integrality=np.array(integ), options=dict(time_limit=tl, presolve=True))
    if res.status == 0 and res.x is not None:
        x = np.round(res.x).astype(int)
        circ = dict(bottom=[([int(x[idx[('a', j, d)]]) for d in range(D)], int(x[idx[('t', j)]])) for j in range(S)],
                    v=[int(x[idx[('v', j)]]) for j in range(S)], u=[int(x[idx[('u', d)]]) for d in range(D)],
                    tau=int(x[idx['tau']]))
        return ('SAT' if not eval_circuit(circ, pts) else 'SAT-BUT-WRONG'), circ, (Wb, Wt)
    if res.status == 2 or 'infeasible' in str(res.message).lower():
        return 'UNSAT', None, (Wb, Wt)
    return 'UNKNOWN', None, (Wb, Wt)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('mode'); ap.add_argument('tl', type=float); ap.add_argument('inst', nargs='+')
    ap.add_argument('--maxS', type=int, default=6)
    a = ap.parse_args()
    for km in a.inst:
        k, m = map(int, km.split(',')); tr = []
        for S in range(a.maxS + 1):
            t0 = time.time(); r, circ, (Wb, Wt) = solve(k, m, a.mode, S, a.tl)
            tr.append(f'{S}:{r}[{time.time() - t0:.1f}s]')
            if r != 'UNSAT':
                print(f'milp {a.mode} k={k} m={m}: {"minimum" if r == "SAT" else "stopped"} S={S} Wb={Wb} Wt={Wt} trace {" ".join(tr)}', flush=True)
                if circ: print('   circuit:', circ, flush=True)
                break
        else:
            print(f'milp {a.mode} k={k} m={m}: UNSAT up to {a.maxS} trace {" ".join(tr)}', flush=True)
