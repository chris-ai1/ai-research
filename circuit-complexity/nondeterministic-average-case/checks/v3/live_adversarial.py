"""Independent re-implementation and adversarial test of Theorem L (live branch points) and Theorem P.

Nodes 0..n-1: inputs x; n..n+k-1: witness inputs; then gates (table, c1, c2); last gate = output.
Variants of the lifting:
  A  : fan-out counted with multiplicity; join on every shared name (live points AND a child that is itself live at the other child)
  B  : fan-out = number of DISTINCT consumer gates (so g = op(c,c) does not make c a branch point), join as in A
  C  : literal text: join only on L_c1 & L_c2 (a child's own value is not identified with its copy in the other relation)
  D  : branch points restricted to gates (witness inputs excluded)
"""
import itertools, random, sys

def analyse(n, k, gates, variant):
    N = n + k + len(gates); out = N - 1
    ch = {n + k + i: (c1, c2) for i, (_, c1, c2) in enumerate(gates)}
    alive = set(); st = [out]
    while st:
        v = st.pop()
        if v in alive: continue
        alive.add(v); st.extend(ch.get(v, ()))
    cons = {v: [] for v in range(N)}
    for g in sorted(ch):
        if g in alive:
            c1, c2 = ch[g]; cons[c1].append(g); cons[c2].append(g)
    wdep = [False] * N
    for v in range(N):
        wdep[v] = (n <= v < n + k) if v < n + k else (wdep[ch[v][0]] or wdep[ch[v][1]])
    def fanout(v): return len(set(cons[v])) if variant == 'B' else len(cons[v])
    branch = {v for v in alive if wdep[v] and fanout(v) >= 2 and not (variant == 'D' and v < n + k)}
    # reach[g] = set of nodes from which out is reachable avoiding g
    def avoid_set(g):
        ok = set()
        if g == out: return ok
        ok.add(out); st = [out]
        while st:
            v = st.pop()
            for c in ch.get(v, ()):
                if c != g and c not in ok: ok.add(c); st.append(c)
        return ok
    live = {}
    for v in sorted(alive):
        if v < n + k: live[v] = (); continue
        c1, c2 = ch[v]; ok = avoid_set(v)
        cand = set(live[c1]) | set(live[c2]) | ({c1, c2} & branch)
        live[v] = tuple(sorted(z for z in cand if z in ok))
    return out, ch, alive, branch, live

def lifted(n, k, gates, x, info, variant):
    out, ch, alive, branch, live = info
    psi = {}
    for v in sorted(alive):
        if v < n: psi[v] = {((), x[v])}; continue
        if v < n + k: psi[v] = {((), 0), ((), 1)}; continue
        t = gates[v - n - k][0]; c1, c2 = ch[v]; rel = set()
        common = set(live[c1]) & set(live[c2])
        for (b1, v1) in psi[c1]:
            d1 = dict(zip(live[c1], b1))
            for (b2, v2) in psi[c2]:
                d2 = dict(zip(live[c2], b2))
                if variant == 'C':
                    if any(d1[z] != d2[z] for z in common): continue
                    env = dict(d2); env.update(d1)
                    env.setdefault(c1, v1); env.setdefault(c2, v2)
                else:
                    env = {}; ok = True
                    for z, val in list(d1.items()) + list(d2.items()) + [(c1, v1), (c2, v2)]:
                        if z in (c1, c2) and z not in branch and not (c1 == c2 and variant != 'B'):
                            continue
                        if env.setdefault(z, val) != val: ok = False; break
                    if not ok: continue
                rel.add((tuple(env[z] for z in live[v]), t[2 * v1 + v2]))
        psi[v] = rel
    return any(val == 1 for _, val in psi[out]), max(len(l) for l in live.values())

def brute(n, k, gates, x):
    for w in itertools.product((0, 1), repeat=k):
        v = list(x) + list(w)
        for t, c1, c2 in gates: v.append(t[2 * v[c1] + v[c2]])
        if v[-1]: return True
    return False

def profile_accepts(n, k, gates, x):
    # Theorem P, independent form: carry the full truth table over ALL k witness bits restricted to dependence set
    N = n + k + len(gates); dep = []; prof = []
    for v in range(N):
        if v < n: dep.append(()); prof.append({(): x[v]})
        elif v < n + k: dep.append((v,)); prof.append({(0,): 0, (1,): 1})
        else:
            t, c1, c2 = gates[v - n - k]; W = tuple(sorted(set(dep[c1]) | set(dep[c2]))); p = {}
            for a in itertools.product((0, 1), repeat=len(W)):
                e = dict(zip(W, a))
                p[a] = t[2 * prof[c1][tuple(e[u] for u in dep[c1])] + prof[c2][tuple(e[u] for u in dep[c2])]]
            dep.append(W); prof.append(p)
    return any(prof[-1].values())

def rt(rng): return [rng.randrange(2) for _ in range(4)]

def gen_random(rng):
    n, k, m = rng.randint(1, 3), rng.randint(1, 4), rng.randint(3, 12)
    return n, k, [(rt(rng), rng.randrange(n + k + g), rng.randrange(n + k + g)) for g in range(m)]

def gen_window(rng):                      # children from a short window: many re-convergences, chains of branch points
    n, k, m = rng.randint(1, 2), rng.randint(1, 3), rng.randint(6, 14); win = rng.randint(2, 4); gates = []
    for g in range(m):
        lo = max(0, n + k + g - win) if g >= 2 else 0
        gates.append((rt(rng), rng.randrange(lo, n + k + g), rng.randrange(lo, n + k + g)))
    return n, k, gates

def gen_ladder(rng):                      # z_{i+1} = op(z_i, z_{i-1} or x), everything reused; random long-range taps
    n, k = 2, rng.randint(1, 3); m = rng.randint(6, 13); gates = []; base = n + k
    for g in range(m):
        cur = base + g
        a = cur - 1 if g else rng.randrange(n, base)
        b = cur - 2 if (g >= 2 and rng.random() < 0.6) else rng.randrange(cur)
        if rng.random() < 0.15: b = a                      # both children equal
        gates.append((rt(rng), a, b))
    return n, k, gates

def gen_nested(rng):                      # diamond of diamonds built recursively on a witness-dependent root
    n, k = 2, rng.randint(1, 2); gates = []; base = n + k
    def new(c1, c2): gates.append((rt(rng), c1, c2)); return base + len(gates) - 1
    def diamond(z, depth):
        if depth == 0: return new(z, rng.randrange(base))
        a = diamond(z, depth - 1) if rng.random() < 0.7 else new(z, rng.randrange(base))
        b = diamond(z, depth - 1) if rng.random() < 0.5 else new(z, rng.randrange(n))
        j = new(a, b)
        if rng.random() < 0.4: j = new(j, z)               # the branch point is needed again after the join
        if rng.random() < 0.3: j = new(j, a)               # an inner wire is needed again after the join
        return j
    r = diamond(rng.randrange(n, base), rng.randint(1, 2))
    if len(gates) > 16: return gen_nested(rng)
    return n, k, gates

def run(name, gen, trials, seed):
    rng = random.Random(seed)
    st = {v: 0 for v in 'ABCD'}; inputs = 0; badP = 0; hist = {}
    for _ in range(trials):
        n, k, gates = gen(rng)
        infos = {v: analyse(n, k, gates, v) for v in 'ABCD'}
        for x in itertools.product((0, 1), repeat=n):
            b = brute(n, k, gates, x); inputs += 1
            badP += profile_accepts(n, k, gates, x) != b
            for v in 'ABCD':
                a, ml = lifted(n, k, gates, x, infos[v], v)
                st[v] += a != b
                if v == 'A': hist[ml] = hist.get(ml, 0) + 1
    print(f'{name:9s} circuits={trials} inputs={inputs} mismatches: A={st["A"]} B={st["B"]} C={st["C"]} D={st["D"]} P={badP}  max-live hist(A)={dict(sorted(hist.items()))}', flush=True)

def exhaustive(m, n=1, k=2, reps=2, seed=5):
    rng = random.Random(seed); base = n + k; bad = {v: 0 for v in 'AB'}; cnt = 0
    ranges = []
    for g in range(m): ranges += [range(base + g), range(base + g)]
    for cs in itertools.product(*ranges):
        if any(cs[2 * g] > cs[2 * g + 1] and False for g in range(m)): continue
        for _ in range(reps):
            gates = [(rt(rng), cs[2 * g], cs[2 * g + 1]) for g in range(m)]
            infoA = analyse(n, k, gates, 'A')
            for x in itertools.product((0, 1), repeat=n):
                b = brute(n, k, gates, x); cnt += 1
                bad['A'] += lifted(n, k, gates, x, infoA, 'A')[0] != b
    print(f'exhaustive wiring m={m} n={n} k={k}, {reps} random gate tables each: inputs={cnt} mismatches A={bad["A"]}', flush=True)

if __name__ == '__main__':
    T = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    run('random', gen_random, T, 1)
    run('window', gen_window, T, 2)
    run('ladder', gen_ladder, T, 3)
    run('nested', gen_nested, T, 4)
    exhaustive(3); exhaustive(4, reps=1)
