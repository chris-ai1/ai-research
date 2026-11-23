import sys, random, itertools
sys.path.insert(0, sys.argv[1])
import circuit_check as cc
rng = random.Random(5); diff = 0; tot = 0
for tr in range(60):
    n = rng.randint(3,4); k = rng.randint(1,3); s = rng.randint(4,7)
    gates = cc.rand_circuit(n, k, s, rng)
    V, edges = cc.build_graph(n, k, gates)
    layout = list(range(V)); rng.shuffle(layout)
    V, edges, frontiers, step = cc.hidden_nbp(n, k, gates, layout)
    # vertices with a directed path to the output gate
    out_gate = n + k + s - 1; reach = {out_gate}
    for i in range(s-1, -1, -1):
        g = n + k + i
        if g in reach: reach.update(gates[i][1:])
    rw = sorted(j for j in range(n, n+k) if j in reach)
    for x in itertools.product((0,1), repeat=n):
        p = cc.run_paths(V, step, x)
        acc = {tuple(wv[j-n] for j in rw) for wv in itertools.product((0,1), repeat=k) if cc.evaluate(n,k,gates,x,wv)[-1]==1}
        tot += 1; diff += (p != len(acc))
print(f"inputs where #paths != #accepting restrictions to output-reaching witnesses: {diff} of {tot}")
