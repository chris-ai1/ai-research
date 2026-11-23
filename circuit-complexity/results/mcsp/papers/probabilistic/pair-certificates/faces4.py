import pickle
comp = pickle.load(open('comp4.pkl','rb'))
N=16
for d, b in ((1,0b0001),(2,0b0011),(3,0b0111),(4,0b1111)):
    a = 0
    ma, mb = 1 << a, 1 << b
    print('distance', d)
    for s in range(0, 7):
        xor = andf = 0; ex = None
        for f in range(1 << N):
            if f & ma or f & mb: continue   # fiber representative with f(a)=f(b)=0
            e = [comp[f] <= s, comp[f|ma] <= s, comp[f|mb] <= s, comp[f|ma|mb] <= s]
            k = sum(e)
            if k in (1,3): andf += 1
            if e == [True, False, False, True] or e == [False, True, True, False]:
                xor += 1
                if ex is None: ex = (f, e, [comp[f], comp[f|ma], comp[f|mb], comp[f|ma|mb]])
        print('  s=%d  XOR faces %6d  odd faces %6d   example %s' % (s, xor, andf, ex))
