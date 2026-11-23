#!/usr/bin/env python3
# Copyright (c) 2026 Christian Reitwiessner.
# Authors: Christian Reitwiessner
"""Exact checks for mixed odd-weight ladders and joint table/address atoms."""
import json
from itertools import product, permutations
from pathlib import Path


def sign(n):
    assert n != 0
    return 1 if n > 0 else -1


def phi(n):
    return (1 if n % 2 == 0 else -1)*n


def chi(s,c):
    return 1 if (s & c).bit_count()%2 == 0 else -1


def ladder(value,lo,hi):
    assert lo <= value <= hi
    return phi(lo)+sum((phi(t)-phi(t-1))*int(value>=t) for t in range(lo+1,hi+1))


def mixed_circuit(k,m,magnitudes):
    assert m & (m-1) == 0
    N=1<<k
    rows={}
    size=0
    for s in range(1,N):
        weights=[0]*(k*m)
        for i in range(k):
            if (s>>i)&1:
                for j in range(m):
                    weights[i*m+j]=chi(s & (m-1),j)*(1+2*(j%2) if magnitudes else 1)
        lo=sum(min(w,0) for w in weights)
        hi=sum(max(w,0) for w in weights)
        size += 2*N+2*(hi-lo)
        rows[s]=(weights,lo,hi)
    # Some block has two full-support rows not equal up to a global sign.
    incompatible=False
    for i in range(k):
        patterns=[tuple(1 if w>0 else -1 for w in row[i*m:(i+1)*m])
                  for s,(row,_,_) in rows.items() if (s>>i)&1]
        for p in patterns:
            for q in patterns:
                incompatible |= p!=q and p!=tuple(-v for v in q)
    assert incompatible
    cases=0
    for x in product((0,1),repeat=N):
        y=[1-2*z for z in x]
        X=[sum(chi(s,c)*y[c] for c in range(N)) for s in range(N)]
        for a in product((0,1),repeat=k*m):
            b=sum((sum(a[i*m:(i+1)*m])%2)<<i for i in range(k))
            score=X[0]  # Raw affine top contribution.
            for s,(weights,lo,hi) in rows.items():
                t=sum(w*v for w,v in zip(weights,a))
                assert (-1)**t == chi(s,b)
                # Both arguments below are affine forms of raw input bits.
                term=ladder(X[s]+t,-N+lo,N+hi)-ladder(t,lo,hi)
                assert term == X[s]*chi(s,b)
                score += term
            assert score == N*y[b]
            cases+=1
    return dict(k=k,m=m,bottom_gates_unmerged=size,
                exact_inputs=cases,no_common_coherent_reorientation=True,
                address_magnitudes=[1,3] if magnitudes else [1])


def atom_checks():
    slabs=0
    for H in range(-31,32,2):
        for L in range(-20,21):
            score=int(2*L+H>=0)-int(2*L-H>=0)
            assert score==sign(H)*int(2*abs(L)<abs(H))
            slabs+=1
    packed=0
    B=9
    for H in range(-B,B+1):
        for L in range(-B-3,B+4):
            expanded=int(L>=B)+sum(int(L==t)*int(H>=-t) for t in range(-B,B))
            assert int(H+L>=0)==expanded
            packed+=1
    # Concrete dense table form: the active width changes with the table.
    widths=set()
    for y in product((-1,1),repeat=5):
        H=sum(y)
        widths.add(sum(2*abs(L)<abs(H) for L in range(-4,5)))
    assert widths=={1,3,5}
    return dict(adaptive_slab_checks=slabs,diagonal_packing_checks=packed,
                dense_five_bit_table_active_widths=sorted(widths))


def mask_checks():
    # All orders and common column sign flips for m=4.
    m=4
    cases=0
    for order in permutations(range(m)):
        for flips in product((-1,1),repeat=m):
            counts=[]
            for r in range(m):
                row=[flips[j]*chi(r,j) for j in order]
                counts.append(sum(a!=b for a,b in zip(row,row[1:])))
            assert sum(counts)==m*(m-1)//2
            cases+=1
    # The argument depends only on adjacent distinct columns, so verify it
    # independently for every pair of columns at larger m as well.
    pairs=0
    for m in (2,4,8,16,32):
        for j in range(m):
            for l in range(j):
                assert sum(chi(r,j)!=chi(r,l) for r in range(m))==m//2
                pairs+=1
    return dict(all_order_and_reorientation_checks=cases,distinct_column_checks=pairs)


if __name__=='__main__':
    results={'Authors':'Christian Reitwiessner','status':'passed',
             'scope':'Exact identities and quadratic constructions; no improved asymptotic bound',
             'mixed_ladders':[mixed_circuit(2,4,False),mixed_circuit(2,4,True)],
             'joint_atoms':atom_checks(),'walsh_masks':mask_checks()}
    Path(__file__).with_name('verification.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(results,indent=2))
