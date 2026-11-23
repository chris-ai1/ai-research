"""Checks on random read-once NBPs (binary, one coordinate per step, prefix cuts):
(a) layer-cake lemma for nonnegative product functions;
(b) the ordered-distinct j-fold product program has path count binom(p, j);
(c) weighted peeling (Lemma WP): each peel obeys the layer-cake bound, the terminal program has
    small supports (SmallSides(K')), and the final inequality holds."""
import random, itertools, sys
from math import comb
from collections import defaultdict

def rand_nbp(n, W, dens, rng):
    widths = [1] + [W]*(n-1) + [1]
    E = []  # E[t] = set of (q, bit, q')
    for t in range(n):
        Et = set()
        for q in range(widths[t]):
            for bit in (0,1):
                for q2 in range(widths[t+1]):
                    if rng.random() < dens: Et.add((q,bit,q2))
        E.append(Et)
    return widths, E

def pre_counts(n, widths, E, alive):
    # pre[t][q] = dict prefix(tuple)->#paths from start
    pre = [ {0: {(): 1}} ]
    for t in range(n):
        nxt = defaultdict(lambda: defaultdict(int))
        for q, d in pre[t].items():
            for (a,bit,b) in E[t]:
                if a == q and alive[t+1].get(b, True):
                    for pf, c in d.items(): nxt[b][pf+(bit,)] += c
        pre.append({q: dict(d) for q,d in nxt.items()})
    return pre

def suf_counts(n, widths, E, alive):
    suf = [None]*(n+1); suf[n] = {0: {(): 1}}
    for t in range(n-1, -1, -1):
        cur = defaultdict(lambda: defaultdict(int))
        for (a,bit,b) in E[t]:
            if alive[t].get(a, True) and b in suf[t+1]:
                for sf, c in suf[t+1][b].items(): cur[a][(bit,)+sf] += c
        suf[t] = {q: dict(d) for q,d in cur.items()}
    return suf

def path_count(n, E, alive, x):
    cur = {0:1}
    for t in range(n):
        nxt = defaultdict(int)
        for (a,bit,b) in E[t]:
            if bit == x[t] and a in cur and alive[t+1].get(b, True): nxt[b] += cur[a]
        cur = nxt
    return cur.get(0, 0)

def bias_exact(S, n, K):
    b = 0.0
    for t in range(1, n):
        rows = list(itertools.product((0,1), repeat=t)); cols = list(itertools.product((0,1), repeat=n-t))
        if len(rows) < K or len(cols) < K: continue
        small, big, tr = (rows, cols, False) if len(rows) <= len(cols) else (cols, rows, True)
        for m in range(K, len(small)+1):
            for Aset in itertools.combinations(small, m):
                c = []
                for y in big:
                    sm = 0
                    for a in Aset:
                        x = (y + a) if tr else (a + y)
                        sm += 2*S[x] - 1
                    c.append(sm)
                c.sort()
                for mb in range(K, len(big)+1):
                    v = max(abs(sum(c[:mb])), abs(sum(c[-mb:])))
                    b = max(b, v / (2*m*mb))
    return b

def layer_cake_check(rng, trials=200):
    for _ in range(trials):
        r, c = rng.randint(2,6), rng.randint(2,6); K = rng.randint(1,3)
        M = [[rng.choice((-1,1)) for _ in range(c)] for _ in range(r)]
        # exact bias of M on rectangles with sides >= K
        b = 0
        for ra in range(K, r+1):
            for A in itertools.combinations(range(r), ra):
                cs = sorted(sum(M[i][j] for i in A) for j in range(c))
                for cb in range(K, c+1):
                    b = max(b, max(abs(sum(cs[:cb])), abs(sum(cs[-cb:])))/(2*ra*cb))
        f = [rng.choice([0, rng.randint(1,5)]) for _ in range(r)]
        g = [rng.choice([0, rng.randint(1,5)]) for _ in range(c)]
        lhs = abs(sum(M[i][j]*f[i]*g[j] for i in range(r) for j in range(c)))
        F, G = sum(f), sum(g)
        rhs = 2*b*F*G + (K-1)*(max(f)*G + F*max(g))
        assert lhs <= rhs + 1e-9, (lhs, rhs)
    return True

def product_check(n, widths, E, j, rng):
    # ordered distinct j-tuples of paths, lexicographic by state sequence
    # state: (tuple of states, tuple of diverged flags for consecutive pairs)
    alive = [dict() for _ in range(n+1)]
    for x in itertools.product((0,1), repeat=n):
        p = path_count(n, E, alive, x)
        cur = {((0,)*j, (False,)*(j-1)): 1}
        for t in range(n):
            nxt = defaultdict(int)
            succ = defaultdict(list)
            for (a,bit,b) in E[t]:
                if bit == x[t]: succ[a].append(b)
            for (qs, fl), c in cur.items():
                for nq in itertools.product(*[succ[q] for q in qs]):
                    nfl = list(fl); ok = True
                    for i in range(j-1):
                        if not fl[i]:
                            if nq[i] < nq[i+1]: nfl[i] = True
                            elif nq[i] > nq[i+1]: ok = False; break
                    if ok: nxt[(nq, tuple(nfl))] += c
            cur = nxt
        q = cur.get(((0,)*j, (True,)*(j-1)), 0) if j > 1 else cur.get(((0,), ()), 0)
        assert q == comb(p, j), (q, p, j)
        assert (1 if p >= 1 else 0) == sum((-1)**(i+1)*comb(p,i) for i in range(1, p+1))
    return True

def peel_check(n, widths, E, S, K, beta, rng):
    b = bias_exact(S, n, K)
    alive = [dict() for _ in range(n+1)]
    xs = list(itertools.product((0,1), repeat=n))
    p0 = {x: path_count(n, E, alive, x) for x in xs}
    D = max(p0.values())
    if D == 0: return None
    total = sum((2*S[x]-1)*p0[x] for x in xs); mass = sum(p0.values())
    peeled = 0.0; npeel = 0
    while True:
        pre = pre_counts(n, widths, E, alive); suf = suf_counts(n, widths, E, alive)
        found = None
        for t in range(1, n):
            for q in range(widths[t]):
                if not alive[t].get(q, True): continue
                f = pre[t].get(q, {}); g = suf[t].get(q, {})
                if not f or not g: continue
                F, G = sum(f.values()), sum(g.values())
                if (K-1)*max(f.values()) <= beta*F and (K-1)*max(g.values()) <= beta*G:
                    found = (t, q, f, g); break
            if found: break
        if not found: break
        t, q, f, g = found
        phi = sum((2*S[a+bb]-1)*f[a]*g[bb] for a in f for bb in g)
        nphi = sum(f.values())*sum(g.values())
        assert abs(phi) <= (2*b + 2*beta)*nphi + 1e-9, ("peel bound", phi, nphi, b, beta)
        before = {x: path_count(n, E, alive, x) for x in xs}
        alive[t][q] = False; npeel += 1
        after = {x: path_count(n, E, alive, x) for x in xs}
        # removed path mass equals phi pointwise
        for x in xs:
            assert before[x] - after[x] == f.get(x[:t],0)*g.get(x[t:],0)
        peeled += phi
    # terminal: every useful state has small support on one side
    Kp = int((K-1)*D/beta) + 1
    pre = pre_counts(n, widths, E, alive); suf = suf_counts(n, widths, E, alive)
    for t in range(1, n):
        for q in range(widths[t]):
            if not alive[t].get(q, True): continue
            f = pre[t].get(q, {}); g = suf[t].get(q, {})
            if f and g: assert len(f) < Kp or len(g) < Kp
    pf = {x: path_count(n, E, alive, x) for x in xs}
    rest = sum((2*S[x]-1)*pf[x] for x in xs)
    assert abs(total - peeled - rest) < 1e-9
    size = sum(len(Et) for Et in E)
    rhs = (2*b + 2*beta)*mass + D*(Kp-1)**2*size
    assert abs(total) <= rhs + 1e-9
    return dict(b=round(b,3), D=D, peels=npeel, lhs=total, peeled_mass=mass - sum(pf.values()), mass=mass)

def main(trials=30, seed=7):
    rng = random.Random(seed)
    layer_cake_check(rng); print("layer-cake lemma: 200 random instances pass")
    for _ in range(10):
        n = 5; widths, E = rand_nbp(n, 3, 0.35, rng)
        for j in (1,2,3): product_check(n, widths, E, j, rng)
    print("product program P^(j): path count = binom(p,j), alternating identity: pass")
    nonvac = 0
    for tr in range(trials):
        n = 6; widths, E = rand_nbp(n, 3, rng.choice((0.3,0.45)), rng)
        S = {x: rng.random() < 0.5 for x in itertools.product((0,1), repeat=n)}
        r = peel_check(n, widths, E, S, K=4, beta=rng.choice((0.5,0.75,1.0)), rng=rng)
        if r and r['peels'] > 0: nonvac += 1; print(r)
    print("weighted peeling: all checks pass; instances with >=1 peel:", nonvac)

if __name__ == '__main__':
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 30)
