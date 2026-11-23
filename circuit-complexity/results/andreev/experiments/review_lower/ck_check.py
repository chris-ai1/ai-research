"""Referee: C_k = max over h:{0,1}^k->{0,1} of the min #bottom gates (top gate reads gates AND inputs).
Constructive integer-weight search (no LP): if every h is found with <=1 gate, then C_k<=1; C_k>=1 because
parity is not a threshold function.  k=2,3."""
import itertools
import numpy as np
for k in (2, 3):
    Z = np.array(list(itertools.product((0, 1), repeat=k)))
    # all threshold functions of k bits with integer weights in [-3,3] (complete for k<=3)
    TF = set()
    for w in itertools.product(range(-3, 4), repeat=k):
        v = Z @ np.array(w)
        for t in range(-10, 11):
            TF.add(tuple((v >= t).astype(int)))
    TF = sorted(TF)
    print(f'k={k}: threshold functions found = {len(TF)} (known: k=2 -> 14, k=3 -> 104)')
    reach = set(TF)  # 0 gates
    for g in TF:
        G = np.column_stack([np.array(g), Z])       # inputs to top gate: (g, z)
        for w in itertools.product(range(-4, 5), repeat=k + 1):
            v = G @ np.array(w)
            for t in np.unique(v):
                reach.add(tuple((v >= t).astype(int)))
    allf = set(itertools.product((0, 1), repeat=2 ** k))
    print(f'k={k}: functions computable with <=1 bottom gate (integer search) = {len(reach & allf)} of {len(allf)};  C_{k} = {1 if reach >= allf else ">1 or search too small"}')
