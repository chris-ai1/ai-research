"""Does the derivative of a small circuit behave like a circuit twice as rich?

For random fan-in-2 circuits we compare, as a function of the number of gates s,
  direct:      f = C(y)                    C a random circuit on n inputs with s gates
  derivative:  f = T(0,y) XOR T(1,y)       T a random circuit on n+1 inputs with s gates
by a spectral proxy for "small bias on large rectangles at every cut": over sampled cuts X of the
n variables, the largest singular value of the +-1 communication matrix of f divided by
sqrt(rows)+sqrt(cols) (about 1 for a random function, large for structured ones).

Capacity prediction: a derivative with s gates should look like a direct circuit with about
n + 2(s-n) gates.  If the two runs were too correlated to use the doubled capacity, the
derivative curve would instead track the direct curve at about the same s.
"""
import sys, random
import numpy as np

AND_T = [(a, b, c) for a in (0, 1) for b in (0, 1) for c in (0, 1)]       # ((u^a)&(v^b))^c

def random_circuit(rng, n_in, s, skew, p_xor=0.5):
    """s gates. Every wire except the output is consumed exactly once; the remaining
    s - n_in + 1 operand slots are taps of an arbitrary earlier wire (this is the cycle rank).
    skew: the first operand of gate i is the previous gate (input 0 for gate 0), so every gate
    depends on input 0."""
    n_taps = s - n_in + 1
    assert n_taps >= 0
    free = 2 * s - (s if skew else 0)                      # slots chosen at random
    n_cons = (n_in + s - 1) - (s if skew else 0)           # consumes still to schedule there
    labels = ['c'] * n_cons + ['t'] * (free - n_cons); rng.shuffle(labels)
    open_w = list(range(n_in)); gates = []; n_w = n_in; pos = 0
    for g in range(s):
        ops = []
        for slot in range(2):
            if skew and slot == 0:
                w = 0 if g == 0 else n_w - 1
                open_w.remove(w); ops.append(w); continue
            lab = labels[pos]
            if lab == 'c' and not open_w:                  # postpone this consume
                j = next(k for k in range(pos + 1, len(labels)) if labels[k] == 't')
                labels[pos], labels[j] = labels[j], labels[pos]; lab = 't'
            pos += 1
            if lab == 'c': w = open_w.pop(rng.randrange(len(open_w)))
            else: w = rng.randrange(n_w)
            ops.append(w)
        if rng.random() < p_xor or g == s - 1 or (skew and g == 0):
            kind = ('x', rng.randrange(2))
        else:
            kind = ('a',) + rng.choice(AND_T)
        gates.append((kind, ops[0], ops[1])); open_w.append(n_w); n_w += 1
    assert len(open_w) == 1, len(open_w)
    return gates, 1

def truth_table(n_in, gates):
    N = 1 << n_in; full = (1 << N) - 1
    w = []
    for i in range(n_in):                                  # variable i: bit pattern with period 2^(i+1)
        blk = ((1 << (1 << i)) - 1) << (1 << i)
        v = 0
        for k in range(0, N, 1 << (i + 1)): v |= blk << k
        w.append(v)
    for kind, a, b in gates:
        if kind[0] == 'x': v = w[a] ^ w[b] ^ (full if kind[1] else 0)
        else:
            u = w[a] ^ (full if kind[1] else 0); t = w[b] ^ (full if kind[2] else 0)
            v = (u & t) ^ (full if kind[3] else 0)
        w.append(v)
    return w[-1], N

def bits(v, N):
    return np.unpackbits(np.frombuffer(v.to_bytes(N // 8, 'little'), dtype=np.uint8), bitorder='little')

def make_cuts(rng, n, sizes, per):
    cuts = []
    idx = np.arange(1 << n)
    for t in sizes:
        for _ in range(per):
            X = sorted(rng.sample(range(n), t)); Y = [i for i in range(n) if i not in X]
            r = sum(((idx >> x) & 1) << j for j, x in enumerate(X))
            c = sum(((idx >> y) & 1) << j for j, y in enumerate(Y))
            cuts.append((1 << t, 1 << (n - t), r, c))
    return cuts

def score(f, cuts):
    sig = 1.0 - 2.0 * f
    sig = sig - sig.mean()                                 # centred: the global bias is reported separately
    best = 0.0
    for R, C, r, c in cuts:
        M = np.empty((R, C)); M[r, c] = sig
        best = max(best, np.linalg.norm(M, 2) / (R ** 0.5 + C ** 0.5))
    return best

def run(n, reps, seed=1):
    rng = random.Random(seed)
    cuts = make_cuts(rng, n, [n // 2 - 2, n // 2 - 1, n // 2], 10)
    rnd = [score(np.array([rng.randrange(2) for _ in range(1 << n)]), cuts) for _ in range(20)]
    print(f'n={n}: random functions score median {np.median(rnd):.3f}')
    out = {}
    for name, extra in (('direct', 0), ('derivative', 1)):
        for skew in (False, True):
            for x in (2, 4, 6, 8, 10, 12, 16, 20, 24, 30, 36, 48):       # x = s - (number of inputs)
                s = n + extra + x; sc = []
                for _ in range(reps):
                    gates, left = random_circuit(rng, n + extra, s, skew)
                    v, N = truth_table(n + extra, gates)
                    if extra:
                        half = N // 2
                        b = bits(v, N); f = b[0::2] ^ b[1::2]              # input 0 is the least significant bit
                    else:
                        f = bits(v, N)
                    sc.append(score(f, cuts) if abs(f.mean() - 0.5) < 0.1 else 99.0)
                sc = np.array(sc)
                out[(name, skew, x)] = (np.median(sc), np.quantile(sc, 0.1), float((sc < 1.25).mean()), float((sc < 2).mean()))
    for skew in (False, True):
        print(f'  {"skew" if skew else "uniform"} circuits: x = gates beyond the inputs;  median / best decile / fraction with score < 1.25 / fraction < 2  (99 = unbalanced)')
        print('     x   direct                    derivative')
        for x in (2, 4, 6, 8, 10, 12, 16, 20, 24, 30, 36, 48):
            a = out[('direct', skew, x)]; b = out[('derivative', skew, x)]
            print(f'   {x:3d}   {a[0]:6.2f} {a[1]:6.2f} {a[2]:5.2f} {a[3]:5.2f}       {b[0]:6.2f} {b[1]:6.2f} {b[2]:5.2f} {b[3]:5.2f}')
    return out

if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 12
    reps = int(sys.argv[2]) if len(sys.argv) > 2 else 200
    run(n, reps)
