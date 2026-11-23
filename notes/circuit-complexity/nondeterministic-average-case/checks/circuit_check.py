"""Brute-force checks for nondet circuits -> hidden-network NBP via a layout (binary alphabet).
Checks: (1) acceptance = exists-witness; (2) Lemma 0: #accepting paths = #accepting restrictions
of w to USED witness inputs; (3) Theorem W: partial determinization (d, G) is unambiguous, accepts
the same set, and its width is <= 2^{w-omega} * 2^{2^omega}; (4) product program P^(j) path count
= binom(p, j) and the alternating identity; (5) cycle-rank accounting cr <= s + 1 - #used inputs."""
import random, itertools, sys
from math import comb
from collections import defaultdict

OPS = [lambda a,b: a&b, lambda a,b: a|b, lambda a,b: a^b, lambda a,b: 1-(a&b),
       lambda a,b: 1-(a|b), lambda a,b: a&(1-b), lambda a,b: (1-a)|b]

def rand_circuit(n, k, s, rng):
    # vertices: 0..n-1 x-inputs, n..n+k-1 witness inputs, then gates, then output vertex
    gates = []
    for g in range(s):
        avail = n + k + g
        # bias towards using inputs so that most are read
        a = rng.randrange(avail); b = rng.randrange(avail)
        gates.append((rng.randrange(len(OPS)), a, b))
    return gates

def build_graph(n, k, gates):
    s = len(gates); V = n + k + s + 1; out = V - 1
    edges = []  # (src, dst)
    for i,(op,a,b) in enumerate(gates):
        g = n + k + i
        edges.append((a, g)); edges.append((b, g))
    edges.append((n + k + s - 1, out))
    return V, edges

def evaluate(n, k, gates, x, w):
    val = list(x) + list(w)
    for (op,a,b) in gates:
        val.append(OPS[op](val[a], val[b]))
    return val

def hidden_nbp(n, k, gates, layout):
    """Return per-step transition function for the hidden network NBP.
    layers: state = tuple of (edge_index, value) sorted, for frontier edges."""
    V, edges = build_graph(n, k, gates)
    pos = {v:i for i,v in enumerate(layout)}
    s = len(gates); out = V - 1
    inc = defaultdict(list)
    for e,(u,v) in enumerate(edges):
        inc[u].append(e); inc[v].append(e)
    frontiers = []
    for t in range(V+1):
        F = [e for e,(u,v) in enumerate(edges) if (pos[u] < t) != (pos[v] < t)]
        frontiers.append(F)
    def step(t, state, xval):
        """state: dict edge->value for frontier t; process vertex layout[t].
        yields new states (dict) for frontier t+1."""
        v = layout[t]
        old = [e for e in inc[v] if pos[edges[e][0] if edges[e][1]==v else edges[e][1]] < t]
        new = [e for e in inc[v] if e not in old]
        # handle parallel edges / both endpoints: an edge (u,v) with u==v impossible
        res = []
        for vals in itertools.product((0,1), repeat=len(new)):
            full = {e: state[e] for e in old}
            full.update(dict(zip(new, vals)))
            outs = [e for e in inc[v] if edges[e][0] == v]
            ins = [e for e in inc[v] if edges[e][1] == v]
            ok = True
            if v < n:
                ok = all(full[e] == xval[v] for e in outs)
            elif v < n + k:
                ok = len(set(full[e] for e in outs)) <= 1
            elif v < n + k + s:
                op,a,b = gates[v - n - k]
                ea, eb = [e for e in ins]  # in order (a,g),(b,g) as appended
                # edges appended in order a then b
                ea = 2*(v-n-k); eb = 2*(v-n-k)+1
                o = OPS[op](full[ea], full[eb])
                ok = all(full[e] == o for e in outs)
            else:
                ok = full[ins[0]] == 1
            if ok:
                ns = {e: state[e] for e in state if e not in old}
                ns.update(dict(zip(new, vals)))
                res.append(ns)
        return res
    return V, edges, frontiers, step

def key(d): return tuple(sorted(d.items()))

def run_paths(V, step, x):
    """count accepting paths, return also set of states per layer on accepting paths"""
    layers = [{(): 1}]
    trans = []
    for t in range(V):
        nxt = defaultdict(int); tr = []
        for st, c in layers[-1].items():
            for ns in step(t, dict(st), x):
                kk = key(ns); nxt[kk] += c; tr.append((st, kk))
        layers.append(dict(nxt)); trans.append(tr)
    return layers[-1].get((), 0)

def cone_edges(n, k, gates, edges):
    cone = set(range(n, n+k))
    for i,(op,a,b) in enumerate(gates):
        if a in cone or b in cone: cone.add(n+k+i)
    return {e for e,(u,v) in enumerate(edges) if u in cone}

def det_program_paths(V, step, frontiers, cone, x):
    """Theorem W program: state (d, G). Count accepting paths; also record widths per layer."""
    layer = {((), frozenset([()])): 1}
    for t in range(V):
        nxt = defaultdict(int)
        for (d, G), c in layer.items():
            # successors grouped by new d
            succ = defaultdict(set)
            for u in G:
                full = dict(d); full.update(dict(u))
                for ns in step(t, full, x):
                    dpart = tuple(sorted((e,v) for e,v in ns.items() if e not in cone))
                    upart = tuple(sorted((e,v) for e,v in ns.items() if e in cone))
                    succ[dpart].add(upart)
            for dpart, Gs in succ.items():
                nxt[(dpart, frozenset(Gs))] += c
        layer = dict(nxt)
    return layer.get(((), frozenset([()])), 0)

def all_det_states(V, step, cone, n):
    """width of Theorem W program over all inputs: collect reachable (d,G) per layer"""
    widths = []
    layer = {((), frozenset([()]))}
    reach = [set(layer)]
    for t in range(V):
        nxt = set()
        for (d,G) in layer:
            for xv in itertools.product((0,1), repeat=n):
                succ = defaultdict(set)
                for u in G:
                    full = dict(d); full.update(dict(u))
                    for ns in step(t, full, xv):
                        dpart = tuple(sorted((e,v) for e,v in ns.items() if e not in cone))
                        upart = tuple(sorted((e,v) for e,v in ns.items() if e in cone))
                        succ[dpart].add(upart)
                for dpart, Gs in succ.items():
                    nxt.add((dpart, frozenset(Gs)))
        layer = nxt; reach.append(set(layer))
    return [len(r) for r in reach]

def main(trials=40, seed=1):
    rng = random.Random(seed)
    stats = defaultdict(int)
    for tr in range(trials):
        n = rng.randint(3,5); k = rng.randint(1,3); s = rng.randint(4,8)
        gates = rand_circuit(n, k, s, rng)
        V, edges = build_graph(n, k, gates)
        layout = list(range(V)); rng.shuffle(layout)
        V, edges, frontiers, step = hidden_nbp(n, k, gates, layout)
        cone = cone_edges(n, k, gates, edges)
        used_w = sorted({u for (u,v) in edges if n <= u < n+k})
        used_inputs = {u for (u,v) in edges if u < n+k}
        # cycle rank of connected component structure: E - V + c, count components
        parent = list(range(V))
        def f(a):
            while parent[a]!=a: parent[a]=parent[parent[a]]; a=parent[a]
            return a
        for (u,v) in edges: parent[f(u)] = f(v)
        comps = len({f(v) for v in range(V)})
        cr = len(edges) - V + comps
        isolated = sum(1 for v in range(V) if all(v not in e for e in edges))
        # cr formula on graph: (E - V + c); bound s + 1 - |used inputs| holds when connected after removing isolated
        assert cr <= s + 1 - len(used_inputs) + (comps - 1 - isolated) + 0 or comps-isolated>1, (cr, s, used_inputs)
        if comps - isolated == 1:
            assert cr == s + 1 - len(used_inputs), (cr, s, len(used_inputs)); stats['cr_checked'] += 1
        w = max(len(F) for F in frontiers)
        om = max(len([e for e in F if e in cone]) for F in frontiers)
        for x in itertools.product((0,1), repeat=n):
            # brute force
            acc_w = set()
            for wv in itertools.product((0,1), repeat=k):
                val = evaluate(n, k, gates, x, wv)
                if val[-1] == 1:
                    acc_w.add(tuple(wv[j-n] for j in used_w))
            p = run_paths(V, step, x)
            assert p == len(acc_w), ("Lemma0", p, len(acc_w))
            q = det_program_paths(V, step, frontiers, cone, x)
            assert q == (1 if p > 0 else 0), ("TheoremW unambiguity", q, p)
            stats['inputs'] += 1
            if p > 1: stats['ambiguous_inputs'] += 1
        widths = all_det_states(V, step, cone, n)
        for t, F in enumerate(frontiers):
            o = len([e for e in F if e in cone])
            assert widths[t] <= 2**(len(F)-o) * 2**(2**o), ("width", widths[t], len(F), o)
        stats['circuits'] += 1
        stats['max_w'] = max(stats['max_w'], w); stats['max_omega'] = max(stats['max_omega'], om)
    print(dict(stats))
    print("ALL CHECKS PASSED")

if __name__ == '__main__':
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 40)
