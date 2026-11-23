import sys; sys.path.insert(0,'/tmp/andreev_gap/verify_d')
from impl import *
import time
def all_inputs(n, lo, hi):
    r = np.arange(lo, hi, dtype=np.int64)
    return ((r[:, None] >> np.arange(n)) & 1).astype(np.int8)
res = []
cases = []
for k in range(1, 5):
    N = 1 << k
    for m in range(1, 40):
        if N + k*m <= 20: cases.append((k, m))
cases.sort(key=lambda t: (t[0]*0 + (1<<t[0]) + t[0]*t[1], t))
for build in (build_d, build_c):
  for (k, m) in cases:
    t0 = time.time()
    c = build(k, m); n = c.n
    tot = 1 << n; CH = 1 << 15
    wrong = cfbad = 0; mn = 10**18; outs1 = 0
    for lo in range(0, tot, CH):
        Z = all_inputs(n, lo, min(tot, lo + CH))
        w, cb, ma = check(c, Z)
        wrong += w; cfbad += cb; mn = min(mn, ma)
    print(f"{c.name} (k={k},m={m}) n={n} N={1<<k} gates={c.size} inputs=2^{n} wrong={wrong} closedform_mismatch={cfbad} min|P|={mn} N={1<<k} [{time.time()-t0:.1f}s]", flush=True)
