"""Referee: independent z3 encoding of the EXACT-sum block-symmetric model (§4):
   exists S bottom gates g_j=[a_j.(x,s) >= t_j] (real weights) and reals v,u,c with
   sum_j v_j g_j(p) + u.p + c == x_{s mod 2}(p)  for every p=(x,s), x in {0,1}^N, s in {0..m}^k.
Margin normalisation (WLOG on finite point sets): g -> a.p >= t ; not g -> a.p <= t-1.
Own point generator; only symmetry breaking: v_1 <= ... <= v_S (gate permutation).
SAT models are re-verified with exact Fractions.   usage: exact_z3_indep.py k m S [timeout_s]"""
import sys, itertools, time
sys.path.insert(0, '/tmp/pydeps')
import z3
from fractions import Fraction
k, m, S = map(int, sys.argv[1:4]); tl = int(sys.argv[4]) if len(sys.argv) > 4 else 1800
N = 1 << k; D = N + k
pts = []
for s in itertools.product(range(m + 1), repeat=k):
    b = sum((s[i] % 2) << i for i in range(k))
    for x in itertools.product((0, 1), repeat=N):
        pts.append((x + s, x[b]))
sol = z3.SolverFor('QF_LRA'); sol.set('timeout', tl * 1000)
A = [[z3.Real(f'A_{j}_{d}') for d in range(D)] for j in range(S)]; T = [z3.Real(f'T_{j}') for j in range(S)]
V = [z3.Real(f'V_{j}') for j in range(S)]; U = [z3.Real(f'U_{d}') for d in range(D)]; C = z3.Real('C')
for j in range(S - 1): sol.add(V[j] <= V[j + 1])
G = {}
for pi, (p, y) in enumerate(pts):
    row = []
    for j in range(S):
        g = z3.Bool(f'g_{j}_{pi}'); G[(j, pi)] = g
        lin = z3.Sum([A[j][d] * p[d] for d in range(D) if p[d] != 0] + [z3.RealVal(0)])
        sol.add(z3.Implies(g, lin >= T[j])); sol.add(z3.Implies(z3.Not(g), lin <= T[j] - 1))
        row.append(z3.If(g, V[j], z3.RealVal(0)))
    sol.add(z3.Sum(row + [U[d] * p[d] for d in range(D) if p[d] != 0] + [C]) == y)
t0 = time.time(); r = sol.check(); dt = time.time() - t0
msg = f'INDEP exact blocksym k={k} m={m} S={S}: {r} ({dt:.1f}s)'
if r == z3.sat:
    M = sol.model(); fr = lambda e: Fraction(M.eval(e, model_completion=True).as_fraction())
    a = [[fr(A[j][d]) for d in range(D)] for j in range(S)]; t = [fr(T[j]) for j in range(S)]
    v = [fr(V[j]) for j in range(S)]; u = [fr(U[d]) for d in range(D)]; c = fr(C)
    ok = all(sum((v[j] for j in range(S) if sum(a[j][d] * p[d] for d in range(D)) >= t[j]), Fraction(0)) + sum(u[d] * p[d] for d in range(D)) + c == y for p, y in pts)
    msg += f'  exact re-verification: {ok}'
print(msg, flush=True)
