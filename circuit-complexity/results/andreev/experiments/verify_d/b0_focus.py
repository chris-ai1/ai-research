import sys; sys.path.insert(0,'/tmp/andreev_gap/verify_d')
from impl import *
# b = 0 focus: for every value of |x'| in 0..N-1 and x0 in {0,1}, random tables, block weights even (0, random even, max even)
rng = np.random.default_rng(99)
for (k, m) in [(2,3),(3,3),(4,4),(5,5),(6,3),(6,6),(7,3)]:
    c = build_d(k, m); N = c.N; n = c.n
    rows = []
    for x0 in (0, 1):
        for w in range(N):
            for rep in range(3):
                t = np.zeros(N, np.int8); t[0] = x0; t[rng.permutation(np.arange(1, N))[:w]] = 1
                mode = rep
                blk = np.zeros((k, m), np.int8)
                for i in range(k):
                    ws = [a for a in range(0, m+1, 2)]
                    a = ws[0] if mode == 0 else (ws[-1] if mode == 1 else ws[rng.integers(len(ws))])
                    blk[i, rng.permutation(m)[:a]] = 1
                rows.append(np.concatenate([t, blk.reshape(-1)]))
    Z = np.array(rows, np.int8)
    r = evaluate(c, Z)
    assert (r['A'] == Z[:, 0]).all()
    P = r['P']; x0 = Z[:, 0]; xs = Z[:, 1:N].sum(1)
    print(f"(k={k},m={m}) b=0 rows={len(Z)} wrong={int((r['out']!=r['A']).sum())} P==closed form: {bool((P==r['CF']).all())}  "
          f"min P over x0=0: {int(P[x0==0].min())} (=N={N}); max P over x0=1: {int(P[x0==1].max())} (=-N={-N})")
