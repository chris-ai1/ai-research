# Copyright (c) 2026 Christian Reitwiessner.
# Authors: Christian Reitwiessner
"""Exact finite checks for UP1's mask obstruction and tail counterexamples."""
from fractions import Fraction as F
from itertools import product, combinations
from random import Random
import json
from pathlib import Path


def dot(x, y):
    return sum(a*b for a,b in zip(x,y))


def nullvector(rows):
    a = [[F(x) for x in row] for row in rows]
    nr, nc = len(a), len(a[0])
    pivots = []
    rank = 0
    for col in range(nc):
        piv = next((i for i in range(rank,nr) if a[i][col]), None)
        if piv is None:
            continue
        a[rank],a[piv] = a[piv],a[rank]
        d = a[rank][col]
        a[rank] = [x/d for x in a[rank]]
        for i in range(nr):
            if i != rank and a[i][col]:
                d = a[i][col]
                a[i] = [x-d*y for x,y in zip(a[i],a[rank])]
        pivots.append(col)
        rank += 1
        if rank == nr:
            break
    free = next(j for j in range(nc) if j not in pivots)
    v = [F(0)]*nc
    v[free] = 1
    for i,piv in enumerate(pivots):
        v[piv] = -a[i][free]
    assert any(v) and all(dot(row,v)==0 for row in rows)
    return v


def adversarial_vertex(rows):
    R,M = len(rows),len(rows[0])
    best = None
    for eps in product((-1,1),repeat=R):
        v = [sum(e*row[j] for e,row in zip(eps,rows)) for j in range(M)]
        norm = dot(v,v)
        if best is None or norm > best[0]:
            best = norm,eps,v
    _,eps,v = best
    assert all(e*dot(row,v)>=M for e,row in zip(eps,rows))
    u = [F(x,R) for x in v]
    target = [dot(row,u) for row in rows]
    while True:
        active = [j for j,x in enumerate(u) if -1 < x < 1]
        if len(active)<=R:
            break
        cols = active[:R+1]
        d = nullvector([[row[j] for j in cols] for row in rows])
        step = min(((1-u[j])/h if h>0 else (-1-u[j])/h)
                   for j,h in zip(cols,d) if h)
        assert step>0
        for j,h in zip(cols,d):
            u[j] += step*h
        assert all(-1<=x<=1 for x in u)
        assert [dot(row,u) for row in rows] == target
    z = [1 if x>=0 else -1 for x in u]
    corr = [abs(dot(row,z)) for row in rows]
    assert min(corr)>=F(M,R)-R
    return z,corr


def f(u,w):
    return ((-1 if u%2 else 1)*u) if abs(u)<=w else 0


def main():
    exhaustive = 0
    # Up to sign/complement symmetry, all one-, two-, and three-mask families.
    for M in range(1,7):
        masks = [(1,)+tail for tail in product((-1,1),repeat=M-1)]
        vertices = list(product((-1,1),repeat=M))
        corrs = [[abs(dot(row,z)) for z in vertices] for row in masks]
        for R in range(1,min(3,len(masks))+1):
            for ix in combinations(range(len(masks)),R):
                best = max(min(corrs[i][v] for i in ix) for v in range(len(vertices)))
                assert F(best)>=F(M,R)-R
                exhaustive += 1
    rng = Random(110511)
    constructive = []
    for M,R in [(16,2),(32,3),(64,4),(128,5),(256,6)]:
        for trial in range(4):
            rows = [[rng.choice((-1,1)) for _ in range(M)] for _ in range(R)]
            z,corr = adversarial_vertex(rows)
            constructive.append({'M':M,'R':R,'trial':trial,
                                 'minimum_correlation':min(corr),'proved_bound':str(F(M,R)-R)})
    tails = 0
    for k,m,w in [(2,2,1),(2,2,2),(3,2,4)]:
        N = 1<<k
        for T in range(1,N):
            if w >= N-(T.bit_count()*m+1)//2:
                continue
            # X_T=N, X_S=0 otherwise, on the character table chi_T.
            for S in range(1,N):
                M = S.bit_count()*m
                X = N if S==T else 0
                for a in range(1<<M):
                    for mask in range(1<<M):
                        D = (a^mask).bit_count()-M//2
                        assert f(X+D,w)+f(X-D,w)==0
                        tails += 1
    pool_duals = 0
    for k,m,w in [(2,2,1),(2,2,2),(3,2,4)]:
        N = 1<<k
        for T in range(1,N):
            if w >= N-(T.bit_count()*m+1)//2:
                continue
            selected_bit = (T & -T).bit_length()-1
            a0,a1 = 0,1<<(selected_bit*m)
            for S in range(1,N):
                coords = [i*m+j for i in range(k) if S>>i&1 for j in range(m)]
                M = len(coords)
                packed = [sum(((a>>j)&1)<<r for r,j in enumerate(coords)) for a in (a0,a1)]
                for mask in range(1<<M):
                    ds = [(a^mask).bit_count()-M//2 for a in packed]
                    for orient in (-1,1):
                        for theta in range(-w,w+2):
                            differences = []
                            for D in ds:
                                X = N if S==T else 0
                                differences.append(int(X+orient*D>=theta)-int(-X+orient*D>=theta))
                            assert differences[0]==differences[1]
                            pool_duals += 1
    staircase = 0
    for w in range(1,8):
        for u in range(-20,21):
            value = sum((f(t,w)-f(t-1,w))*(u>=t) for t in range(-w,w+2))
            assert value==f(u,w)
            staircase += 1
    collisions = 0
    for k in range(2,6):
        N = 1<<k
        xa = [int(c in (0,3)) for c in range(N)]
        xb = [int(c in (1,2)) for c in range(N)]
        qa = [sum(xa[c] for c in range(N) if c>>i&1) for i in range(k)]
        qb = [sum(xb[c] for c in range(N) if c>>i&1) for i in range(k)]
        assert qa==qb and xa[0]>xb[0] and xa[1]<xb[1]
        collisions += 1
    result = {'authors':'Christian Reitwiessner','status':'all exact checks passed',
              'mask_families_exhausted':exhaustive,'constructive_rational_checks':constructive,
              'character_tail_summands':tails,'whole_pool_four_point_duals':pool_duals,'staircase_checks':staircase,
              'low1_collisions':collisions}
    Path(__file__).with_name('checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':
    main()
