# Copyright (c) 2026 Christian Reitwiessner. All rights reserved.
# Authors: Christian Reitwiessner
"""Bounded exploratory support deletion for parity-label-only kernels.

Floating-point LP statuses are computational evidence only, never proofs.
This does not search arbitrary raw-address halfspace dictionaries.
"""

import json
from pathlib import Path
import random
import sys
import time

sys.path.insert(0, "/tmp/andreev_gap/coherence_fable/pydeps_local")
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import lil_matrix


def setup(k, rho):
    n = 1 << k
    off = [(b, c) for b in range(n) for c in range(n) if b != c]
    h = np.array([[(-1) ** ((b & t).bit_count()) for t in range(n)] for b in range(n)])
    matrix = lil_matrix((2*len(off) + n, n*n + len(off)), dtype=float)
    rhs = np.zeros(matrix.shape[0])
    for j, (b, c) in enumerate(off):
        matrix[2*j, c*n:(c+1)*n] = h[b]
        matrix[2*j+1, c*n:(c+1)*n] = -h[b]
        matrix[2*j, n*n+j] = -1
        matrix[2*j+1, n*n+j] = -1
        matrix[2*len(off)+b, n*n+j] = 1
    for b in range(n):
        matrix[2*len(off)+b, b*n:(b+1)*n] = -rho*h[b]
        rhs[2*len(off)+b] = -1
    return n, h, matrix.tocsr(), rhs, len(off)


def trial(k, seed, rho=0.3):
    n, h, matrix, rhs, noff = setup(k, rho)
    objective = np.zeros(n*n + noff)
    bounds = [(None, None)]*(n*n) + [(0, None)]*noff
    order = list(range(n*n))
    random.Random(seed).shuffle(order)
    latest = None
    statuses = {}
    start = time.monotonic()
    for index in order:
        bounds[index] = (0, 0)
        solved = linprog(objective, A_ub=matrix, b_ub=rhs, bounds=bounds,
                         method="highs", options={"time_limit": 1.0})
        statuses[str(solved.status)] = statuses.get(str(solved.status), 0) + 1
        if solved.status == 0:
            latest = solved.x[:n*n].reshape(n, n)
        else:
            bounds[index] = (None, None)
    support = [(c, t) for c in range(n) for t in range(n) if bounds[c*n+t] != (0, 0)]
    if latest is not None:
        values = h @ latest.T
        margins = rho*np.diag(values) - (np.abs(values).sum(axis=1)-np.abs(np.diag(values)))
        residual = float(margins.min())
    else:
        residual = None
    result = dict(k=k, seed=seed, rho=rho, support_size=len(support),
                  baseline=3**k, support=support, lp_status_counts=statuses,
                  minimum_float_margin=residual, seconds=time.monotonic()-start)
    print(json.dumps({key: val for key, val in result.items() if key != "support"}), flush=True)
    return result


def main():
    print("Authors: Christian Reitwiessner", flush=True)
    results = []
    for k, trials in [(3, 8), (4, 3)]:
        for seed in range(trials):
            results.append(trial(k, seed))
            data = {"Authors": "Christian Reitwiessner",
                    "copyright": "Copyright (c) 2026 Christian Reitwiessner. All rights reserved.",
                    "status": "Exploratory floating-point support deletion; no optimality claim.",
                    "trials": results}
            Path(__file__).with_name("fourier_probe.json").write_text(json.dumps(data, indent=2)+"\n")


if __name__ == "__main__":
    main()
