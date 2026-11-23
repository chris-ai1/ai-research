import pickle
comp = pickle.load(open('comp4.pkl','rb'))
def good(h):   # all eight cofactors nonzero, and h not constant 1
    if h == 0xffff: return False
    for c in range(4):
        for v in (0, 1):
            if not any((h >> r) & 1 for r in range(16) if ((r >> c) & 1) == v): return False
    return True
print('rows: base threshold s0;  columns: distance d0 = 1..4;  entries: #XOR faces / #odd faces whose hard corners all have nonzero cofactors')
for s in range(3, 7):
    row = []
    for d, b in ((1,1),(2,3),(3,7),(4,15)):
        ma, mb = 1, 1 << b
        nx = no = 0
        for f in range(1 << 16):
            if f & (ma | mb): continue
            corners = [f, f|ma, f|mb, f|ma|mb]
            e = [comp[x] <= s for x in corners]
            hard_ok = all(good(x) for x, ee in zip(corners, e) if not ee)
            if not hard_ok: continue
            if sum(e) == 2 and e[0] == e[3]: nx += 1
            if sum(e) in (1, 3): no += 1
        row.append('%d/%d' % (nx, no))
    print('s0=%d ' % s, row)
