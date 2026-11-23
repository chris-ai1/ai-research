"""Per-third-site version: for each relative position of the third site v (4-bit part g, number |J| of differing outside coordinates),
is there an XOR face (L,L') for the pair such that flipping v is certified hard from both L and L'?"""
import pickle, mmap
exec(open('isolate.py').read().split("for t in (3, 4):")[0])
def flip_ok(X, t, g, J):
    e = t - 4
    if J == 0: return comp[X ^ (1 << g)] >= t + 1
    m = dist_to_support(X, g)
    if m + J >= e + 4: return True
    nv = 4 + J
    if J == 1:   fn = lambda r: ((X >> (r & 15)) & 1) if (r >> 4) & 1 else int((r & 15) == g)
    elif J == 2: fn = lambda r: ((X >> (r & 15)) & 1) if (r >> 4) == 3 else (int((r & 15) == g) if (r >> 4) == 0 else 0)
    else:        fn = lambda r: ((X >> (r & 15)) & 1) if (r >> 4) == 7 else (int((r & 15) == g) if (r >> 4) == 0 else 0)
    return cert(ttable(nv, fn), nv, t + J + 1, J - 1)
for t in (3, 4):
    for d, b in ((4,15),):
        ma, mb = 1, 1 << b
        faces = []
        for f in range(1 << 16):
            if f & (ma | mb): continue
            for L in (f, f | ma):
                L2 = L ^ ma ^ mb
                if comp[L] <= t and comp[L2] <= t and comp[L ^ ma] > t and comp[L ^ mb] > t: faces.append((L, L2))
        bad = []
        for J in (0, 1, 2, 3):
            for g in range(16):
                if J == 0 and g in (0, b): continue
                if not any(flip_ok(L, t, g, J) and flip_ok(L2, t, g, J) for (L, L2) in faces): bad.append((J, format(g,'04b')))
        print('t=%d distance %d: %d faces; third-site positions (|J|, g) with no certified face: %s' % (t, d, len(faces), bad), flush=True)
