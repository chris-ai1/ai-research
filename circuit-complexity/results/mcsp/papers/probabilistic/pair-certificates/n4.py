import sys, pickle
from multiprocessing import Pool
sys.path.insert(0, 'lib')  # python-sat installed with: pip install --target lib python-sat
from synth import size
n = 4; N = 16; FULL = (1 << N) - 1
def perm_tt(tt, rowmap):
    r = 0
    for t in range(N):
        if (tt >> rowmap[t]) & 1: r |= 1 << t
    return r
def swapmap(i, j):
    m = []
    for t in range(N):
        bi, bj = (t >> i) & 1, (t >> j) & 1
        u = t & ~(1 << i) & ~(1 << j) | (bj << i) | (bi << j)
        m.append(u)
    return m
gens = [swapmap(0,1), swapmap(1,2), swapmap(2,3), [t ^ 1 for t in range(N)]]
cls = [-1] * (1 << N); reps = []
for f in range(1 << N):
    if cls[f] >= 0: continue
    cid = len(reps); reps.append(f); cls[f] = cid; stack = [f]
    while stack:
        g = stack.pop()
        for h in [perm_tt(g, m) for m in gens] + [g ^ FULL]:
            if cls[h] < 0:
                cls[h] = cid; stack.append(h)
print('classes', len(reps), flush=True)

import subprocess, json
if __name__ == '__main__':
    if len(sys.argv) > 1:
        r, m = int(sys.argv[1]), int(sys.argv[2])
        out = {f: size(f, 4) for i, f in enumerate(reps) if i % m == r}
        json.dump(out, open('part%d.json' % r, 'w'))
    else:
        m = 18
        ps = [subprocess.Popen([sys.executable, 'n4.py', str(r), str(m)]) for r in range(m)]
        for p in ps: p.wait()
        szd = {}
        for r in range(m): szd.update({int(k): v for k, v in json.load(open('part%d.json' % r)).items()})
        sz = [szd[f] for f in reps]
        comp = bytes(sz[cls[f]] for f in range(1 << N))
        pickle.dump(comp, open('comp4.pkl', 'wb'))
        from collections import Counter
        print(sorted(Counter(sz).items()))
        print(sorted(Counter(comp).items()))
