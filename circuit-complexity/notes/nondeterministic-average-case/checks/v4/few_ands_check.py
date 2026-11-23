"""Check of the "few nonlinear gates" bound for one witness bit.

Run a circuit h(y, w) for w = 0 and w = 1.  For each wire let v be its value for w = 0 and d the
XOR of its two values.  Claim: d on every wire is a fixed F_2-linear combination of the d's of
the AND-type gates in the witness cone and of the constant d_w = 1.  Hence on any set E of cone
wires the pair (v, d) takes at most 2^(|E| + min(|E|, m+1)) values, m = number of such gates.
"""
import itertools, random

def gen(rng, n, s, p_xor):
    gates = []
    for g in range(s):
        a, b = rng.randrange(n + 1 + g), rng.randrange(n + 1 + g)
        if rng.random() < p_xor: gates.append(('x', rng.randrange(2), a, b))
        else: gates.append(('a', rng.randrange(2), rng.randrange(2), rng.randrange(2), a, b))
    return gates

def run(n, gates, y, w):
    v = list(y) + [w]
    for g in gates:
        if g[0] == 'x': v.append(v[g[2]] ^ v[g[3]] ^ g[1])
        else: v.append(((v[g[4]] ^ g[1]) & (v[g[5]] ^ g[2])) ^ g[3])
    return v

rng = random.Random(3); bad_lin = bad_cnt = wires = 0; worst = 0.0
for trial in range(400):
    n = rng.randint(4, 8); s = rng.randint(6, 18); gates = gen(rng, n, s, rng.choice([0.5, 0.7, 0.9]))
    W = n                                                   # index of the witness input
    cone = [False] * (n + 1 + s); cone[W] = True
    mask = [0] * (n + 1 + s); mask[W] = 1                   # bit 0 = the constant d_w
    gens = []                                               # wires that are generators
    for i, g in enumerate(gates):
        idx = n + 1 + i; a, b = g[-2], g[-1]
        cone[idx] = cone[a] or cone[b]
        if not cone[idx]: continue
        if g[0] == 'x': mask[idx] = mask[a] ^ mask[b]
        else: gens.append(idx); mask[idx] = 1 << len(gens)
    m = len(gens)
    ys = list(itertools.product((0, 1), repeat=n))
    V0 = [run(n, gates, y, 0) for y in ys]; V1 = [run(n, gates, y, 1) for y in ys]
    for e in range(n + 1 + s):
        if not cone[e]: continue
        wires += 1
        for r0, r1 in zip(V0, V1):
            pred = mask[e] & 1
            for j, gidx in enumerate(gens):
                if mask[e] >> (j + 1) & 1: pred ^= r0[gidx] ^ r1[gidx]
            bad_lin += pred != (r0[e] ^ r1[e])
    cw = [e for e in range(n + 1 + s) if cone[e] and e != W]
    for _ in range(20):                                     # random edge sets
        E = rng.sample(cw, min(len(cw), rng.randint(1, 6)))
        states = {tuple((r0[e], r0[e] ^ r1[e]) for e in E) for r0, r1 in zip(V0, V1)}
        bound = 2 ** (len(E) + min(len(E), m + 1))
        bad_cnt += len(states) > bound
print(dict(circuits=400, cone_wires=wires, linear_form_mismatches=bad_lin, count_violations=bad_cnt))
