import pickle, mmap
comp = pickle.load(open('comp4.pkl','rb'))
bms = {}
for G in (1,2,3,4,5,6):
    f = open('bm5_%d.bin' % G, 'rb'); bms[G] = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
def easy5(tt, G): return (bms[G][tt >> 3] >> (tt & 7)) & 1
def blow(psi, c):
    t = 0
    for r in range(32):
        if ((r >> c) & 1) == ((r >> 4) & 1) and (psi >> (r & 15)) & 1: t |= 1 << r
    return t
def cof(psi, c, v): return [(psi >> r) & 1 for r in range(16) if ((r >> c) & 1) == v]
from collections import Counter
viol = Counter(); tot = Counter()
ex = {}
for psi in range(1 << 16):
    k = comp[psi]
    if k > 5: continue
    for c in range(4):
        c0, c1 = cof(psi, c, 0), cof(psi, c, 1)
        if not any(c0) or not any(c1): continue      # hypothesis: both cofactors nonzero
        tot[k] += 1
        if k == 0:
            if easy5(blow(psi, c), 1): viol[k] += 1; ex.setdefault(k, (hex(psi), c))
        elif easy5(blow(psi, c), k + 1):
            viol[k] += 1; ex.setdefault(k, (hex(psi), c))
print('cases by C(psi):', dict(tot)); print('violations by C(psi):', dict(viol), ex)
