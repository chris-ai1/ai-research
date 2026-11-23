"""Search for small circuits whose output (direct) or whose derivative in one input (derivative)
looks extractor-like at every sampled cut, and compare the sizes needed.

Objective (lower is better, about 1 for a random function): the maximum over sampled cuts of the
largest singular value of the +-1 communication matrix divided by sqrt(rows)+sqrt(cols).
The matrix is not centred, so a biased function is penalised.
Local search at a fixed number of gates s: rewire one operand or change one gate type; accept if
the objective does not get worse (plus a little annealing).
"""
import sys, os, random, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from derivative_capacity import random_circuit, truth_table, bits, make_cuts, AND_T

def objective(gates, n, extra, cuts):
    v, N = truth_table(n + extra, gates)
    b = bits(v, N)
    f = (b[0::2] ^ b[1::2]) if extra else b
    sig = 1.0 - 2.0 * f
    best = 0.0
    for R, C, r, c in cuts:
        M = np.empty((R, C)); M[r, c] = sig
        best = max(best, np.linalg.norm(M, 2) / (R ** 0.5 + C ** 0.5))
    return best

def mutate(rng, gates, n_in):
    g = list(gates); i = rng.randrange(len(g)); kind, a, b = g[i]
    r = rng.random()
    if r < 0.4: a = rng.randrange(n_in + i)
    elif r < 0.8: b = rng.randrange(n_in + i)
    else: kind = ('x', rng.randrange(2)) if rng.random() < 0.5 else ('a',) + rng.choice(AND_T)
    g[i] = (kind, a, b); return g

def search(args):
    name, n, x, steps, seed = args
    extra = 1 if name == 'derivative' else 0
    rng = random.Random(seed); n_in = n + extra; s = n_in + x
    cuts = make_cuts(random.Random(1000), n, [n // 2 - 2, n // 2 - 1, n // 2], 14)
    gates, _ = random_circuit(rng, n_in, s, False)
    cur = objective(gates, n, extra, cuts); best = cur; bestg = gates
    for t in range(steps):
        cand = mutate(rng, gates, n_in); val = objective(cand, n, extra, cuts)
        temp = 0.02 * (1 - t / steps)
        if val <= cur or rng.random() < math.exp(-(val - cur) / max(temp, 1e-9)):
            gates, cur = cand, val
            if cur < best: best, bestg = cur, gates
    test = make_cuts(random.Random(99), n, [n // 2 - 2, n // 2 - 1, n // 2], 12)   # fresh cuts
    return name, x, seed, best, objective(bestg, n, extra, test)

if __name__ == '__main__':
    # one job per process: derivative_search.py NAME N X STEPS SEED   -> one result line
    name, n, x, steps, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
    r = search((name, n, x, steps, seed))
    print(f'{r[0]} n={n} x={r[1]} steps={steps} seed={r[2]} search={r[3]:.3f} fresh={r[4]:.3f}', flush=True)
