"""Brute-force check of live-profile lifting (Theorem L) and parallel witnesses (Theorem P).

Circuit: nodes 0..n-1 are inputs x, n..n+k-1 are witness inputs, then gates (op, c1, c2) over
earlier nodes with arbitrary fan-out; the last gate is the output.

Theorem L state of a cone node v: a relation Psi_v on (values of the live branch points L_v, value
of v).  Branch point = witness-dependent node with fan-out >= 2 (among nodes that reach the
output).  L_g = { z in L_c1 | L_c2 | {branch children} : some path from z to the output avoids g }.
Claim: x is accepted iff Psi_out contains value 1, and Psi_g is a function of the children's
states, so the lifted circuit is deterministic.

Theorem P state: the profile of v, its value as a function of the witness bits it depends on.
"""
import itertools, random

def build(rng, n, k, m):
    gates = []
    for g in range(m):
        t = [rng.randrange(2) for _ in range(4)]
        gates.append((t, rng.randrange(n + k + g), rng.randrange(n + k + g)))
    return gates

def analyse(n, k, gates):
    N = n + k + len(gates); out = N - 1
    ch = {n + k + i: (c1, c2) for i, (_, c1, c2) in enumerate(gates)}
    alive = set(); st = [out]
    while st:
        v = st.pop()
        if v in alive: continue
        alive.add(v); st.extend(ch.get(v, ()))
    cons = {v: [] for v in range(N)}
    for g, (c1, c2) in ch.items():
        if g in alive:
            cons[c1].append(g); cons[c2].append(g)          # one entry per use
    wdep = {}
    for v in range(N):
        if v < n: wdep[v] = frozenset()
        elif v < n + k: wdep[v] = frozenset([v])
        else: wdep[v] = wdep[ch[v][0]] | wdep[ch[v][1]]
    branch = {v for v in alive if wdep[v] and len(cons[v]) >= 2}
    def reaches_avoiding(z, g):                              # path z -> out not through g
        if z == g: return False
        seen = set(); st = [z]
        while st:
            v = st.pop()
            if v == out: return True
            for c in cons[v]:
                if c != g and c not in seen: seen.add(c); st.append(c)
        return False
    live = {}
    for v in sorted(alive):
        if v < n + k: live[v] = (); continue
        c1, c2 = ch[v]
        cand = set(live[c1]) | set(live[c2]) | ({c1, c2} & branch)
        live[v] = tuple(sorted(z for z in cand if reaches_avoiding(z, v)))
    return out, ch, alive, wdep, branch, live

def lifted_accepts(n, k, gates, x, info):
    out, ch, alive, wdep, branch, live = info
    psi = {}
    for v in sorted(alive):
        if v < n: psi[v] = {((), x[v])}
        elif v < n + k: psi[v] = {((), 0), ((), 1)}
        else:
            t = gates[v - n - k][0]; c1, c2 = ch[v]; rel = set()
            for (b1, v1) in psi[c1]:
                for (b2, v2) in psi[c2]:
                    env = {}; ok = True
                    for z, val in list(zip(live[c1], b1)) + list(zip(live[c2], b2)) + \
                                  ([(c1, v1)] if c1 in branch else []) + ([(c2, v2)] if c2 in branch else []):
                        if env.setdefault(z, val) != val: ok = False; break
                    if not ok or (c1 == c2 and v1 != v2): continue
                    rel.add((tuple(env[z] for z in live[v]), t[2 * v1 + v2]))
            psi[v] = rel
    return any(val == 1 for _, val in psi[out]), psi

def profile_accepts(n, k, gates, x, info):
    out, ch, alive, wdep, branch, live = info
    prof = {}
    for v in sorted(alive):
        W = sorted(wdep[v])
        if v < n: prof[v] = {(): x[v]}
        elif v < n + k: prof[v] = {(0,): 0, (1,): 1}
        else:
            t = gates[v - n - k][0]; c1, c2 = ch[v]; p = {}
            for a in itertools.product((0, 1), repeat=len(W)):
                env = dict(zip(W, a))
                v1 = prof[c1][tuple(env[u] for u in sorted(wdep[c1]))]
                v2 = prof[c2][tuple(env[u] for u in sorted(wdep[c2]))]
                p[a] = t[2 * v1 + v2]
            prof[v] = p
    return any(prof[out].values())

def brute(n, k, gates, x):
    for w in itertools.product((0, 1), repeat=k):
        v = list(x) + list(w)
        for t, c1, c2 in gates: v.append(t[2 * v[c1] + v[c2]])
        if v[-1]: return True
    return False

rng = random.Random(7); stats = dict(circuits=0, inputs=0, bad_L=0, bad_P=0, max_live=0, max_rel=0, nontree=0)
hist = {}
for _ in range(3000):
    n, k, m = rng.randint(2, 4), rng.randint(1, 4), rng.randint(3, 10)
    gates = build(rng, n, k, m); info = analyse(n, k, gates)
    live = info[5]; r = max(len(l) for l in live.values())
    stats['circuits'] += 1; stats['max_live'] = max(stats['max_live'], r); hist[r] = hist.get(r, 0) + 1
    stats['nontree'] += bool(info[4])
    for x in itertools.product((0, 1), repeat=n):
        b = brute(n, k, gates, x)
        a, psi = lifted_accepts(n, k, gates, x, info)
        stats['max_rel'] = max(stats['max_rel'], max(len(p) for p in psi.values()))
        stats['inputs'] += 1; stats['bad_L'] += a != b; stats['bad_P'] += profile_accepts(n, k, gates, x, info) != b
print(stats)
print('circuits by max number of live branch points:', dict(sorted(hist.items())))
