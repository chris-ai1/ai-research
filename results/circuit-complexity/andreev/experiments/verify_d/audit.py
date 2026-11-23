import sys; sys.path.insert(0,'/tmp/andreev_gap/verify_d')
from impl import *
import random, time
random.seed(3)
print("== pure-Python exact-integer evaluation of the explicit gates (no numpy arithmetic) ==")
for build in (build_d, build_c):
  for (k, m) in [(2,2),(3,3),(4,3),(5,2),(5,3)]:
    c = build(k, m); N = c.N; n = c.n
    W = [list(map(int, w)) for w in c.Wm]; th = [int(t) for t in c.thv]
    v = [int(a) for a in c.v]; u = [int(a) for a in c.u]; tau = int(c.tau)
    bad = 0; tot = 0
    for trial in range(1500):
        z = [random.randint(0, 1) for _ in range(n)]
        if trial % 3 == 0:  # force b=0
            for i in range(k):
                w = random.choice([a for a in range(m+1) if a % 2 == 0]); blk = [1]*w + [0]*(m-w); random.shuffle(blk); z[N+i*m:N+(i+1)*m] = blk
        if trial % 7 == 0: z[:N] = [1]*N
        if trial % 11 == 0: z[:N] = [1]*N; z[0] = 0
        g = [1 if sum(wj*zj for wj, zj in zip(w, z)) >= t else 0 for w, t in zip(W, th)]
        out = 1 if sum(a*b for a, b in zip(v, g)) + sum(a*b for a, b in zip(u, z)) >= tau else 0
        bidx = sum(((sum(z[N+i*m:N+(i+1)*m]) & 1) << i) for i in range(k))
        tot += 1; bad += out != z[bidx]
    print(f"{c.name} (k={k},m={m}) gates={c.size}: {tot} inputs, wrong={bad}")

print("\n== audit: constant gates, duplicates, weight magnitudes, counts ==")
print("name  k m  n  N  gates  formula  const_gates  dup_gates  max|bottom w|  max|top coef|  max|direct coef|  gates_merged  G/n^2  G/(N^2/2+.75kmN)")
for (k, m) in [(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,3),(6,3),(5,8),(4,16)]:
    c = build_d(k, m)
    const = 0
    for w, t in zip(c.Wm, c.thv):
        mn = int(w[w < 0].sum()); mx = int(w[w > 0].sum())
        if t <= mn or t > mx: const += 1
    keys = set((tuple(w.tolist()), int(t)) for w, t in zip(c.Wm, c.thv))
    dup = c.size - len(keys)
    d2 = dedupe(c)
    N = c.N; n = c.n
    print(f"d {k} {m} {n} {N} {c.size} {d_count_formula(k,m)} {const} {dup} {np.abs(c.Wm).max()} {np.abs(c.cv).max()} {np.abs(c.lin).max()} {d2.size} {c.size/n**2:.4f} {c.size/(N*N/2+.75*k*m*N):.4f}")
print("\n== (c) counts ==")
for (k, m) in [(3,3),(4,4),(5,5)]:
    c = build_c(k, m); d2 = dedupe(c)
    N = c.N
    form = N*(N-1) + sum(2*popc(S)*m + (popc(S)*m)//2 for S in range(1, N))
    print(f"c ({k},{m}) gates={c.size} (=N(N-1)+sum_S(2T+floor(T/2))+km: {form + k*m}) merged={d2.size} (=...+ceil(km/2): {form + (k*m+1)//2}) N^2+1.25kmN={N*N+1.25*k*m*N:.0f}")

print("\n== asymptotics (formula, exact) ==")
print("balanced km=N: k, N, G_d, G_d/n^2 (->5/16=0.3125),  G_d/(N^2/2+.75kmN)")
for k in [1,2,4,8,16,32,64]:
    N = 1 << k
    if k > 22:   # use closed form: sum_{S} (N/2 + 2ceil(T/2)+floor(T/2)), with T=|S|m, m=N/k
        continue
    m = N // k
    if N % k: continue
    G = d_count_formula(k, m); n = N + k*m
    print(k, N, G, f"{G/n**2:.5f}", f"{G/(N*N/2+.75*k*m*N):.5f}")
