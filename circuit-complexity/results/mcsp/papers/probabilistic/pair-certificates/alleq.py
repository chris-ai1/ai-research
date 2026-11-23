import sys, time
sys.path.insert(0,'lib')
from synth import size, has_circuit
def tt(k, fn):
    t = 0
    for r in range(1 << k):
        x = [(r >> i) & 1 for i in range(k)]
        if fn(x): t |= 1 << r
    return t
d = int(sys.argv[1]); k = d + 1          # c_1..c_d = x[0..d-1], p = x[d]
E = lambda x: len(set(x[:d-1])) == 1
g  = tt(k, lambda x: E(x) and (x[d] or not x[d-1]))
g2 = tt(k, lambda x: E(x) and (x[d] or x[0]))
lo = tt(k, lambda x: E(x) and (x[d] or (x[0] and not x[d-1])))
hi = tt(k, lambda x: E(x) and (x[d] or x[0] or not x[d-1]))
t = 2 * d - 3
print('d', d, 'k', k, 'claimed t', t, flush=True)
for name, f in (('g', g), ('g2', g2)):
    t0 = time.time(); print(name, 'has circuit with t gates:', has_circuit(f, k, t), 'and with t-1:', has_circuit(f, k, t-1), round(time.time()-t0,1), flush=True)
for name, f in (('g AND g2', lo), ('g OR g2', hi)):
    t0 = time.time(); print(name, 'has circuit with t gates:', has_circuit(f, k, t), ' with t+1:', has_circuit(f, k, t+1), round(time.time()-t0,1), flush=True)
