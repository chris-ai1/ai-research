"""Independent cross-check: CP-SAT with integer weights whose bounds are PROVEN sufficient
(Cramer + Hadamard; see report.md section 'Weight bounds').  Different method from z3/LRA.

usage: python3 -I cpsat_check.py MODE TL k,m [k,m ...]   [--maxS 8] [--workers 8] [--plain]
"""
import sys, time, math, argparse
sys.path.insert(0, '/tmp/pydeps'); sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from ortools.sat.python import cp_model
from fractions import Fraction as F
from common import andreev_points, eval_circuit


def hadamard_bound(rows_sq_max, d):
    # |det| of d x d matrix with every row squared-norm <= rows_sq_max  (plus 1 for the replaced RHS column)
    return math.isqrt((rows_sq_max + 1) ** d) + 1


def solve(k, m, mode, S, tl, workers=8, symbreak='v'):
    pts = andreev_points(k, m, mode)
    D = len(pts[0][0])
    R2 = max(sum(c * c for c in p) for p, _ in pts) + 1          # row (p,-1)
    if mode in ('full', 'thermo'):
        # all tight systems are (after row/column sign changes) 0/1 matrices: |det| of a d x d
        # 0/1 matrix is <= (d+1)^((d+1)/2) / 2^d
        b01 = lambda d: math.isqrt((d + 1) ** (d + 1) // 4 ** d) + 1
        Wb, Wt = b01(D + 1), b01(D + S + 1)
    else:
        Wb = hadamard_bound(R2, D + 1)
        Wt = hadamard_bound(R2 + S, D + S + 1)                   # row (g,p,-1)
    md = cp_model.CpModel()
    al = [[md.NewIntVar(-Wb, Wb, f'a{j}_{d}') for d in range(D)] for j in range(S)]
    th = [md.NewIntVar(-Wb, Wb, f't{j}') for j in range(S)]
    v = [md.NewIntVar(-Wt, Wt, f'v{j}') for j in range(S)]
    u = [md.NewIntVar(-Wt, Wt, f'u{d}') for d in range(D)]
    tau = md.NewIntVar(-Wt, Wt, 'tau')
    if symbreak == 'theta':
        # complement normalisation g_j(0)=0  <=>  theta_j >= 1 ; then sort gates by theta (permutation)
        for j in range(S):
            md.Add(th[j] >= 1)
        for j in range(S - 1):
            md.Add(th[j] <= th[j + 1])
    elif symbreak == 'v':
        # complement gates with v_j<0, permute so v sorted; extra rows (unit / difference vectors) have
        # norm <= sqrt2 <= row-norm bound, so the Cramer/Hadamard bound Wt still applies
        for j in range(S):
            md.Add(v[j] >= 0)
        for j in range(S - 1):
            md.Add(v[j] <= v[j + 1])
    for p, out in pts:
        terms = []
        for j in range(S):
            g = md.NewBoolVar('')
            lin = sum(al[j][d] * p[d] for d in range(D) if p[d])
            md.Add(lin >= th[j]).OnlyEnforceIf(g)
            md.Add(lin <= th[j] - 1).OnlyEnforceIf(g.Not())
            e = md.NewIntVar(-Wt, Wt, '')
            md.Add(e == v[j]).OnlyEnforceIf(g)
            md.Add(e == 0).OnlyEnforceIf(g.Not())
            terms.append(e)
        top = sum(terms) + sum(u[d] * p[d] for d in range(D) if p[d])
        md.Add(top >= tau) if out else md.Add(top <= tau - 1)
    sol = cp_model.CpSolver()
    sol.parameters.max_time_in_seconds = tl
    sol.parameters.num_workers = workers
    r = sol.Solve(md)
    if r in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        circ = dict(bottom=[([sol.Value(a) for a in al[j]], sol.Value(th[j])) for j in range(S)],
                    v=[sol.Value(x) for x in v], u=[sol.Value(x) for x in u], tau=sol.Value(tau))
        bad = eval_circuit(circ, pts)
        return ('SAT' if not bad else 'SAT-BUT-WRONG'), circ, (Wb, Wt)
    return ('UNSAT' if r == cp_model.INFEASIBLE else 'UNKNOWN'), None, (Wb, Wt)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('mode'); ap.add_argument('tl', type=float); ap.add_argument('inst', nargs='+')
    ap.add_argument('--maxS', type=int, default=8); ap.add_argument('--workers', type=int, default=8)
    ap.add_argument('--sym', default='v', choices=['none', 'theta', 'v'])
    a = ap.parse_args()
    for km in a.inst:
        k, m = map(int, km.split(','))
        tr = []
        for S in range(a.maxS + 1):
            t0 = time.time()
            r, circ, (Wb, Wt) = solve(k, m, a.mode, S, a.tl, a.workers, a.sym)
            tr.append(f'{S}:{r}[{time.time() - t0:.1f}s]')
            if r != 'UNSAT':
                print(f'cpsat {a.mode} k={k} m={m}: {"minimum" if r == "SAT" else "stopped"} S={S}  bounds Wb={Wb} Wt={Wt}  trace {" ".join(tr)}', flush=True)
                if circ: print('   circuit:', circ, flush=True)
                break
        else:
            print(f'cpsat {a.mode} k={k} m={m}: UNSAT up to {a.maxS}  trace {" ".join(tr)}', flush=True)
