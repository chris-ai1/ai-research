"""Brute-force check of the tree-cone theorem.

A nondeterministic circuit C(x, w) whose witness cone is tree-like (every witness input and
every witness-dependent gate feeds at most one gate) is simulated exactly by a deterministic
circuit on the same graph over the alphabet {{0},{1},{0,1}} of achievable value sets.
Control: when one witness bit is used twice, the simulation is only an over-approximation.
"""
import itertools, random

def rand_op(rng):
    t = [rng.randrange(2) for _ in range(4)]
    return lambda a, b: t[2 * a + b]

def build(rng, n, n_det, n_cone, reuse):
    det = []                                   # x-determined gates: (op, i, j) over earlier wires
    for g in range(n_det):
        det.append((rand_op(rng), rng.randrange(n + g), rng.randrange(n + g)))
    k = 0
    def tree(size):                            # returns a cone node
        nonlocal k
        if size == 0:
            if rng.random() < 0.5:
                k += 1; return ('w', k - 1)
            return ('y', rng.randrange(n + n_det))
        l = rng.randrange(size)
        return ('g', rand_op(rng), tree(l), tree(size - 1 - l))
    root = tree(n_cone)
    if reuse and k >= 2:                       # control: make witness 1 an alias of witness 0
        def alias(t):
            if t[0] == 'w': return ('w', 0) if t[1] == 1 else t
            if t[0] == 'g': return ('g', t[1], alias(t[2]), alias(t[3]))
            return t
        root = alias(root)
    return det, root, k

def det_vals(det, x):
    v = list(x)
    for op, i, j in det: v.append(op(v[i], v[j]))
    return v

def ev(t, y, w):
    if t[0] == 'w': return w[t[1]]
    if t[0] == 'y': return y[t[1]]
    return t[1](ev(t[2], y, w), ev(t[3], y, w))

def lifted(t, y):                              # achievable value set, computed gate by gate
    if t[0] == 'w': return frozenset((0, 1))
    if t[0] == 'y': return frozenset((y[t[1]],))
    A, B = lifted(t[2], y), lifted(t[3], y)
    return frozenset(t[1](a, b) for a in A for b in B)

def run(reuse, trials=400, seed=1):
    rng = random.Random(seed); bad = 0; inputs = 0; amb = 0; over = 0
    for _ in range(trials):
        n = rng.randint(3, 5); det, root, k = build(rng, n, rng.randint(2, 6), rng.randint(3, 9), reuse)
        if k == 0: continue
        for x in itertools.product((0, 1), repeat=n):
            y = det_vals(det, x)
            true = frozenset(ev(root, y, w) for w in itertools.product((0, 1), repeat=k))
            L = lifted(root, y); inputs += 1
            cnt = sum(ev(root, y, w) for w in itertools.product((0, 1), repeat=k))
            amb += cnt > 1
            if L != true:
                bad += 1; over += true < L
    return dict(inputs=inputs, ambiguous_inputs=amb, mismatches=bad, strict_overapprox=over)

print('tree-like cone   :', run(False))
print('one reused witness:', run(True))
