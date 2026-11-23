import sys; sys.path.insert(0,'/tmp/pydeps')
import numpy as np, itertools, random
pc = lambda v: bin(v).count('1')
ceil2 = lambda u: (u + 1) // 2
random.seed(5)
# 1. scalar identity Y e = ceil((2Y+t)/2)^2 - Y^2 - ceil(t/2)^2 - Y t
for Y in range(0, 200):
    for t in range(0, 200):
        assert Y * (t % 2) == ceil2(2*Y+t)**2 - Y*Y - ceil2(t)**2 - Y*t
        assert 4*Y*(-1)**t == 4*Y - 8*ceil2(2*Y+t)**2 + 8*Y*Y + 8*ceil2(t)**2 + 8*Y*t
# staircases: f(u)=ceil(u/2)^2 = sum_{odd th<=u} th ; |x|^2=sum (2th-1)[x>=th]; floor(t/2)=sum [t>=2j]; gated forms
for u in range(0, 300):
    assert ceil2(u)**2 == sum(th for th in range(1, u+1, 2))
    assert u*u == sum(2*th-1 for th in range(1, u+1))
    assert u*(u+1) == sum(2*th for th in range(1, u+1))
for p in range(0, 60):
    for q in range(0, 60):   # |x'| = p, sigma = q: |x'|sigma = ((p+q)^2-(p-q)^2)/4 with two-sided staircase
        sq_pos = sum(2*th-1 for th in range(1, p+q+1))
        sq_q = sum(2*th-1 for th in range(1, p+1) if p-q >= th) + sum(2*th-1 for th in range(1, q+1) if q-p >= th)
        assert 4*p*q == sq_pos - sq_q
B = 1000
for T in range(0, 40):
    for t in range(0, T+1):
        for x0 in (0, 1):
            assert x0*(-1)**t == x0*(1 - 2*t) + 4*sum(1 for j in range(1, T//2+1) if t + B*x0 >= 2*j + B)
            assert x0*t == sum(1 for l in range(1, T+1) if t + B*x0 >= l + B)
# 2. sums over S for all tables, all block weights (small k exhaustive, bigger sampled)
def check_k(k, m, samples=None):
    N = 1 << k
    tabs = list(itertools.product((0,1), repeat=N)) if samples is None else [tuple(random.randint(0,1) for _ in range(N)) for _ in range(samples)]
    wts = list(itertools.product(range(m+1), repeat=k)) if samples is None else [tuple(random.randint(0,m) for _ in range(k)) for _ in range(samples)]
    cnt = 0
    for x in tabs:
        xp = sum(x[1:]); 
        Y = [sum(x[c] for c in range(1, N) if pc(S & c) & 1) for S in range(N)]
        sumY2 = sum(Y[S]**2 for S in range(1, N)); sumY = sum(Y[1:])
        assert sumY == N//2 * xp
        assert 4*sumY2 == N*(xp*xp + xp)
        for s in (wts if samples is None else random.sample(wts, min(len(wts), 20))):
            t = [sum(s[i] for i in range(k) if S >> i & 1) for S in range(N)]
            sig = sum(s)
            assert 4*sum(Y[S]*t[S] for S in range(1, N)) == N*xp*sig + N*sum(x[1 << i]*s[i] for i in range(k))
            assert 4*sum(t[S]**2 for S in range(1, N)) == N*(sig*sig + sum(v*v for v in s))
            assert sum(t[1:]) == N//2*sig
            # b-dependence: sum_S (-1)^{t_S} over S != empty = N[b=0]-1 ; sum_S Y_S (-1)^{t_S} closed form
            b = sum((s[i] & 1) << i for i in range(k))
            assert sum((-1)**t[S] for S in range(1, N)) == N*(b == 0) - 1
            lhs = 4*sum(Y[S]*(-1)**t[S] for S in range(1, N))
            rhs = 2*N*(b == 0)*xp - 2*N*(x[b] if b else 0)
            assert lhs == rhs, (x, s)
            # full P closed form
            P = N + lhs - 2*N*N*x[0]*(b == 0)
            assert P == N - 2*N*x[b] + (b == 0)*(2*N*sum(x) - 2*N*N*x[0])
            cnt += 1
    return cnt
print('k=1,m=3 exhaustive', check_k(1, 3))
print('k=2,m=2 exhaustive', check_k(2, 2))
print('k=3,m=1 exhaustive (2^8 tables x 2^3 weights)', check_k(3, 1))
print('k=3,m=3 sampled', check_k(3, 3, 400))
print('k=4,m=3 sampled', check_k(4, 3, 400))
print('k=5,m=2 sampled', check_k(5, 2, 100))
print('ALL IDENTITIES OK')
