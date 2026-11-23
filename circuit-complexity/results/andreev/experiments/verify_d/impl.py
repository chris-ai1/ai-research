"""Independent re-implementation of the depth-2 threshold circuits for Andreev's function.
Everything is an explicit integer (weight-vector, threshold) pair on the n raw input bits.
Input layout: z[0..N-1] = table x_c (c as k-bit integer), z[N+i*m+j] = bit j of block i.
"""
import sys
sys.path.insert(0, '/tmp/pydeps')
import numpy as np

def popc(v): return bin(v).count('1')

class Circuit:
    def __init__(self, k, m, name):
        self.k, self.m, self.N, self.name = k, m, 1 << k, name
        self.n = self.N + k * m
        self.W = []      # bottom weight vectors (list of np int64 arrays)
        self.th = []     # bottom thresholds
        self.coef = []   # coefficient of each bottom gate in P
        self.tag = []
        self.lin = np.zeros(self.n, dtype=np.int64)  # direct input coefficients in P
        self.const = 0                                # P = const + coef.g + lin.z
    def gate(self, w, theta, coef, tag):
        w = np.asarray(w, dtype=np.int64)
        self.W.append(w); self.th.append(int(theta)); self.coef.append(int(coef)); self.tag.append(tag)
    def finalize(self):
        self.Wm = np.array(self.W, dtype=np.int64)
        self.thv = np.array(self.th, dtype=np.int64)
        self.cv = np.array(self.coef, dtype=np.int64)
        # explicit top gate: output = [ v.g + u.z >= tau ]  with v=-coef, u=-lin, tau=const+1   (P<0  <=>  -(P-const) >= const+1)
        self.v = -self.cv; self.u = -self.lin; self.tau = self.const + 1
        # exactness guard for float64 evaluation
        assert np.abs(self.Wm).sum(axis=1).max() < 2**50
        assert np.abs(self.cv).sum() + np.abs(self.lin).sum() + abs(self.const) < 2**50
        self.Wf = self.Wm.astype(np.float64); self.cf = self.cv.astype(np.float64); self.lf = self.lin.astype(np.float64)
        return self
    @property
    def size(self): return len(self.W)

def xwv(N, n, c_list, wt=1):
    w = np.zeros(n, dtype=np.int64)
    for c in c_list: w[c] = wt
    return w

def blockbits(c, i):  # indices of block i
    return [c.N + i * c.m + j for j in range(c.m)]

def build_d(k, m):
    N = 1 << k; c = Circuit(k, m, 'd'); n = c.n; km = k * m
    B = N + km + 2
    c.const = N
    # --- per S != empty
    for S in range(1, N):
        T = popc(S) * m
        wu = np.zeros(n, dtype=np.int64); wt = np.zeros(n, dtype=np.int64)
        for cc in range(1, N):
            if popc(S & cc) & 1: wu[cc] = 2          # 2*Y_S
        for i in range(k):
            if S >> i & 1:
                for idx in blockbits(c, i): wu[idx] = 1; wt[idx] = 1   # + t_S
        # main ridge  -8 ceil(u/2)^2, u in [0, N+T]: odd thresholds, step = theta
        for th in range(1, N + T + 1, 2):
            c.gate(wu, th, -8 * th, ('ridge', S))
        # residue +8 ceil(t/2)^2, odd thresholds
        for th in range(1, T + 1, 2):
            c.gate(wt, th, +8 * th, ('resid', S))
        # override: -2N * 4 * x0 [t >= 2j]  gate [t + B x0 >= 2j + B]
        wo = wt.copy(); wo[0] = B
        for j in range(1, T // 2 + 1):
            c.gate(wo, 2 * j + B, -8 * N, ('ovr', S))
    # --- |x'| terms
    wx = np.zeros(n, dtype=np.int64); wx[1:N] = 1             # |x'|
    wsig = np.zeros(n, dtype=np.int64); wsig[N:] = 1          # sigma
    c.lin[1:N] += 4 * N                                       # 4*sum Y_S -> 2N|x'|, and 2N|x'| from 8 sum Y^2
    for th in range(1, N):                                    # 2N |x'|^2 = 2N sum (2th-1)[|x'|>=th]
        c.gate(wx, th, 2 * N * (2 * th - 1), ('xsq', 0))
    # 2N |x'| sigma = (N/2)(p^2 - q^2), p=|x'|+sigma, q=|x'|-sigma
    wp = wx + wsig; wq = wx - wsig
    for th in range(1, N - 1 + km + 1):
        c.gate(wp, th, (N // 2) * (2 * th - 1), ('p2', 0))
    for th in range(1, N):
        c.gate(wq, th, -(N // 2) * (2 * th - 1), ('q2+', 0))
    for th in range(1, km + 1):
        c.gate(-wq, th, -(N // 2) * (2 * th - 1), ('q2-', 0))
    # 2N sum_i x_{e_i} s_i : gates [s_i + B x_{e_i} >= l + B]
    for i in range(k):
        w = np.zeros(n, dtype=np.int64)
        for idx in blockbits(c, i): w[idx] = 1
        w[1 << i] = B
        for l in range(1, m + 1):
            c.gate(w, l + B, 2 * N, ('xe', i))
    # override remainder: -2N^2 x0 (linear) and +2N^2 x0*sigma via gates [sigma + B x0 >= l + B]
    c.lin[0] += -2 * N * N
    w = wsig.copy(); w[0] = B
    for l in range(1, km + 1):
        c.gate(w, l + B, 2 * N * N, ('x0sig', 0))
    return c.finalize()

def build_c(k, m):
    """(b)-style phi gadget + gated-parity override.  2Y(-1)^t = phi(2Y+t) - phi(t), phi(u)=(-1)^u u."""
    N = 1 << k; c = Circuit(k, m, 'c'); n = c.n; km = k * m
    B = N + km + 2
    c.const = N
    for S in range(1, N):
        T = popc(S) * m
        wu = np.zeros(n, dtype=np.int64); wt = np.zeros(n, dtype=np.int64)
        for cc in range(1, N):
            if popc(S & cc) & 1: wu[cc] = 2
        for i in range(k):
            if S >> i & 1:
                for idx in blockbits(c, i): wu[idx] = 1; wt[idx] = 1
        # 4Y(-1)^t = 2 phi(u) - 2 phi(t); phi(u)=sum_{th=1}^u (-1)^th (2th-1)
        for th in range(1, N + T + 1):
            c.gate(wu, th, 2 * (-1) ** th * (2 * th - 1), ('phiu', S))
        for th in range(1, T + 1):
            c.gate(wt, th, -2 * (-1) ** th * (2 * th - 1), ('phit', S))
        wo = wt.copy(); wo[0] = B
        for j in range(1, T // 2 + 1):
            c.gate(wo, 2 * j + B, -8 * N, ('ovr', S))
    wsig = np.zeros(n, dtype=np.int64); wsig[N:] = 1
    c.lin[0] += -2 * N * N
    w = wsig.copy(); w[0] = B
    for l in range(1, km + 1):
        c.gate(w, l + B, 2 * N * N, ('x0sig', 0))
    return c.finalize()

def d_count_formula(k, m):
    from math import comb
    N = 1 << k
    tot = 0
    for s in range(1, k + 1):
        T = s * m
        tot += comb(k, s) * (N // 2 + 2 * ((T + 1) // 2) + T // 2)
    return tot + 3 * (N - 1) + 4 * k * m

# ---------------- evaluation ----------------
def target(c, Z):
    """A(x,a) for rows of Z (0/1 int array)."""
    N, k, m = c.N, c.k, c.m
    blocks = Z[:, N:].reshape(len(Z), k, m).sum(axis=2) & 1
    b = (blocks * (1 << np.arange(k))).sum(axis=1)
    return Z[np.arange(len(Z)), b], b

def closed_form(c, Z, b):
    N = c.N
    xb = Z[np.arange(len(Z)), b].astype(np.int64)
    tot = Z[:, :N].sum(axis=1).astype(np.int64)
    x0 = Z[:, 0].astype(np.int64)
    P = N - 2 * N * xb
    P = P + (b == 0) * (2 * N * tot - 2 * N * N * x0)
    return P

def evaluate(c, Z):
    """returns dict with outputs from explicit top gate, P, mismatch counts."""
    Zf = Z.astype(np.float64)
    G = (Zf @ c.Wf.T >= c.thv[None, :].astype(np.float64))      # bottom gates (exact: small ints)
    Gf = G.astype(np.float64)
    Pf = c.const + Gf @ c.cf + Zf @ c.lf
    P = np.rint(Pf).astype(np.int64)
    # explicit top gate [v.g + u.z >= tau]
    top = (Gf @ c.v.astype(np.float64) + Zf @ c.u.astype(np.float64)) >= c.tau
    A, b = target(c, Z)
    CF = closed_form(c, Z, b)
    return dict(out=top.astype(np.int64), A=A.astype(np.int64), P=P, CF=CF)

def check(c, Z):
    r = evaluate(c, Z)
    wrong = int((r['out'] != r['A']).sum())
    cfbad = int((r['P'] != r['CF']).sum())
    minabs = int(np.abs(r['P']).min())
    return wrong, cfbad, minabs

def dedupe(c):
    """merge bottom gates that have identical (weight vector, threshold); drop zero-coefficient gates.
    returns new finalized Circuit (a legitimate smaller circuit, same function P)."""
    d = {}
    order = []
    for w, t, co, tg in zip(c.W, c.th, c.coef, c.tag):
        key = (tuple(w.tolist()), t)
        if key in d: d[key][0] += co
        else: d[key] = [co, w, tg]; order.append(key)
    c2 = Circuit(c.k, c.m, c.name + '+merge')
    c2.lin = c.lin.copy(); c2.const = c.const
    for key in order:
        co, w, tg = d[key]
        if co != 0: c2.gate(w, key[1], co, tg)
    return c2.finalize()
