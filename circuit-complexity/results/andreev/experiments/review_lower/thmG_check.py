"""Referee re-verification of Theorem G (k=2, 4*ceil(m/2)+m block-symmetric gates), independent code.
Everything is scaled by 2 so all weights are integers (top weights become -8,-4; s-weights 10; x-weights 16,4,3,2; threshold 13).
(1) Bit-level, exhaustive over ALL 2^(4+2m) inputs for m<=8: gates are explicit weight vectors on (x0..x3, block1 bits, block2 bits).
(2) Block-sum level (valid because every gate and the top gate are block-symmetric) for all m<=400, all 16 tables, all (s1,s2).
Table index: c = b1 + 2*b2, b_i = s_i mod 2."""
import itertools, math, sys
import numpy as np

def gates(m):
    J = (m + 1) // 2; G = []   # (alpha[4], beta[2], theta, v*2)
    for j in range(1, J + 1):
        G.append(((1, 0, 0, 0), (1, 0), 2 * j, -8)); G.append(((0, 0, 1, 0), (1, 0), 2 * j, -4))
        G.append(((1, 0, 0, 0), (0, 1), 2 * j, -8)); G.append(((0, 1, 0, 0), (0, 1), 2 * j, -4))
    for j in range(1, m + 1):
        G.append(((1, 0, 0, 0), (1, 1), 2 * j, -8))
    return G
TOP_S = (10, 10); TOP_X = (16, 4, 3, 2); TOP_T = 13      # output [ sum + 10 s1 + 10 s2 + 16x0+4x1+3x2+2x3 - 13 >= 0 ]

def bitlevel(m):
    G = gates(m); n = 4 + 2 * m
    W = np.zeros((len(G), n), dtype=np.int64); T = np.zeros(len(G), dtype=np.int64); V = np.zeros(len(G), dtype=np.int64)
    for r, (al, be, th, v) in enumerate(G):
        W[r, :4] = al; W[r, 4:4 + m] = be[0]; W[r, 4 + m:] = be[1]; T[r] = th; V[r] = v
    u = np.zeros(n, dtype=np.int64); u[:4] = TOP_X; u[4:4 + m] = TOP_S[0]; u[4 + m:] = TOP_S[1]
    bad = 0; tot = 0; minmarg = None
    Z = ((np.arange(1 << n)[:, None] >> np.arange(n)) & 1).astype(np.int64)
    for s0 in range(0, len(Z), 1 << 16):
        z = Z[s0:s0 + (1 << 16)]
        g = (z @ W.T >= T).astype(np.int64)
        top = g @ V + z @ u - TOP_T
        b1 = z[:, 4:4 + m].sum(1) & 1; b2 = z[:, 4 + m:].sum(1) & 1
        tgt = z[np.arange(len(z)), b1 + 2 * b2]
        out = (top >= 0).astype(np.int64)
        bad += int((out != tgt).sum()); tot += len(z)
        mm = np.where(tgt == 1, top, -top - 1).min()   # margin: top>=0 for 1s, top<=-1 for 0s (integers)
        minmarg = mm if minmarg is None else min(minmarg, mm)
    return len(G), tot, bad, int(minmarg)

def blocklevel(m):
    G = gates(m)
    al = np.array([g[0] for g in G]); be = np.array([g[1] for g in G]); th = np.array([g[2] for g in G]); v = np.array([g[3] for g in G])
    X = np.array([[(r >> c) & 1 for c in range(4)] for r in range(16)])
    s1, s2 = np.meshgrid(np.arange(m + 1), np.arange(m + 1), indexing='ij'); s1 = s1.ravel(); s2 = s2.ravel()
    bad = 0
    for x in X:
        lin = (al @ x)[:, None] + be[:, :1] * s1[None, :] + be[:, 1:] * s2[None, :]
        top = v @ (lin >= th[:, None]).astype(np.int64) + TOP_S[0] * s1 + TOP_S[1] * s2 + TOP_X @ x - TOP_T
        tgt = x[(s1 & 1) + 2 * (s2 & 1)]
        bad += int(((top >= 0).astype(int) != tgt).sum())
    return len(G), bad

if __name__ == '__main__':
    for m in range(1, 9):
        S, tot, bad, mg = bitlevel(m)
        print(f'bit-level m={m}: gates={S} (4*ceil(m/2)+m={4*((m+1)//2)+m})  inputs={tot}  errors={bad}  min integer slack={mg}', flush=True)
    worst = 0
    for m in range(1, 121):
        S, bad = blocklevel(m); worst += bad
        assert S == 4 * ((m + 1) // 2) + m
    print('block-level m=1..120: total errors =', worst)
