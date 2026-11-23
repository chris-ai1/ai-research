"""Referee: how many gates of construction (d) split a cube, as k grows?  And what is the intrinsic cap of
the method "Theorem A (per-cube count) + a uniform per-gate split bound f"?

For each gate of (d) (built by the author's constr_d.build, used only as a gate list), the block part is a
block-symmetric direction beta (we assert this).  For a table x the gate splits cube c iff
    theta' - pos <= beta.c < theta' - neg,   theta' = T - alpha.x,  pos = sum max(beta,0), neg = sum min(beta,0)
(all quantities are integers).  The number of such c is read off the exact distribution of beta.c over
c in {0..m-1}^k (DP convolution).  We average over many random tables x (the count depends on x through
Y_S, x_0, x_{e_i}), so the result is the exact per-x mean, then averaged over x samples.

Outputs per (k,m): S, mean # splitting gates per cube (R_d), R_d/N, R_d/(kN), mean split fraction R_d/S,
max per-gate split fraction, and the method caps  R_d / f_coh  and  R_d / f_bs  where
  f_coh = 1-(1-1/m)^k   (Lemma B1, attained by some coherent gates)
  f_bs  = exact max split fraction of the block-symmetric gate [sum_i s_i >= theta] over theta (a lower bound
          on ANY valid uniform split bound for block-symmetric gates)."""
import sys, math, itertools
sys.path.insert(0, '/tmp/pydeps'); sys.path.insert(0, '/tmp/andreev_gap/linear_trick')
import numpy as np
from constr_d import build

def dist(beta, m):
    """counts[v - off] = #{c in {0..m-1}^k : beta.c = v}"""
    lo = sum(min(b, 0) * (m - 1) for b in beta); hi = sum(max(b, 0) * (m - 1) for b in beta)
    cnt = np.zeros(hi - lo + 1, dtype=np.float64); cnt[-lo] = 1.0   # value 0 at index -lo
    cur_lo = 0; cur = np.array([1.0])
    for b in beta:
        if b == 0:
            cur = cur * m; continue
        vals = [b * t for t in range(m)]
        nlo = cur_lo + min(vals); nhi = cur_lo + len(cur) - 1 + max(vals)
        new = np.zeros(nhi - nlo + 1)
        for v in vals:
            s = cur_lo + v - nlo; new[s:s + len(cur)] += cur
        cur, cur_lo = new, nlo
    return cur, cur_lo

def analyse(k, m, nx=64, seed=0):
    gates, K, lin, N, n = build(k, m); S = len(gates)
    W = np.array([g[0] for g in gates]); T = np.array([g[1] for g in gates])
    al = W[:, :N]; blk = W[:, N:].reshape(S, k, m)
    be = blk[:, :, 0]
    assert np.allclose(blk, be[:, :, None]), 'not block-symmetric'
    assert np.allclose(be, np.round(be)) and np.allclose(T, np.round(T)) and np.allclose(al, np.round(al))
    be = np.round(be).astype(np.int64); T = np.round(T).astype(np.int64); al = np.round(al).astype(np.int64)
    keys, inv = np.unique(be, axis=0, return_inverse=True); inv = np.ravel(inv)
    D = []
    for b in keys:
        cnt, off = dist(b.tolist(), m)
        cum = np.concatenate([[0.0], np.cumsum(cnt)])            # cum[i] = #{value - off < i}
        pos = int(np.maximum(b, 0).sum()); neg = int(np.minimum(b, 0).sum())
        D.append((cum, off, pos, neg))
    rng = np.random.default_rng(seed); tot = 0.0; fmax = 0.0; mk = float(m) ** k
    per_gate_mean = np.zeros(S)
    for _ in range(nx):
        x = rng.integers(0, 2, N)
        th = T - al @ x
        split = np.zeros(S)
        for gi_key, (cum, off, pos, neg) in enumerate(D):
            idx = np.nonzero(inv == gi_key)[0]
            a = th[idx] - pos - off; bnd = th[idx] - neg - off      # count values v with a <= v-off < bnd
            a = np.clip(a, 0, len(cum) - 1); bnd = np.clip(bnd, 0, len(cum) - 1)
            split[idx] = np.maximum(cum[bnd] - cum[a], 0)
        tot += split.sum() / mk; fmax = max(fmax, split.max() / mk); per_gate_mean += split / mk / nx
    Rd = tot / nx
    f_coh = 1 - (1 - 1 / m) ** k
    cnt, off = dist([1] * k, m); cum = np.concatenate([[0.0], np.cumsum(cnt)])
    f_bs = max(cum[min(len(cum) - 1, v + 1)] - cum[max(0, v + 1 - k)] for v in range(len(cnt))) / mk  # window of k consecutive values
    L = math.log2(S + 1); D0 = (2 ** k - k - 1 - L) / (k + L)
    return dict(k=k, m=m, N=N, S=S, Rd=Rd, D0=D0, fmax=fmax, fbar=Rd / S, f_coh=f_coh, f_bs=f_bs,
                cap_coh=Rd / f_coh, cap_bs=Rd / f_bs, pred=0.625 * k * N + 3 * k)

if __name__ == '__main__':
    cases = [(4, 4), (5, 5), (6, 6), (7, 18), (8, 32)] if len(sys.argv) < 2 else [tuple(map(int, a.split(','))) for a in sys.argv[1:]]
    for k, m in cases:
        r = analyse(k, m)
        print(f"k={r['k']} m={m} N={r['N']} S={r['S']}: mean splitting gates/cube R_d={r['Rd']:.1f}  (R_d/N={r['Rd']/r['N']:.2f}, R_d/(kN)={r['Rd']/(k*r['N']):.3f}; "
              f"0.625kN+3k={r['pred']:.0f})  D_0={r['D0']:.2f}  per-cube slack R_d/D_0={r['Rd']/r['D0']:.1f}\n"
              f"      mean split fraction R_d/S={r['fbar']:.4f} (=1/(2m)? {1/(2*m):.4f})  max per-gate fraction={r['fmax']:.3f}  "
              f"f_coh={r['f_coh']:.3f}  f_bs(all-ones, exact)={r['f_bs']:.3f}\n"
              f"      METHOD CAP (best possible output of A + uniform split bound): coherent R_d/f_coh={r['cap_coh']:.0f} = {r['cap_coh']/r['S']:.3f} S_d ; "
              f"block-sym R_d/f_bs={r['cap_bs']:.0f} = {r['cap_bs']/r['S']:.3f} S_d", flush=True)
