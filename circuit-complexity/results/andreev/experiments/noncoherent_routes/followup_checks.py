#!/usr/bin/env python3
# Copyright (c) 2026 Christian Reitwiessner.
# Authors: Christian Reitwiessner
"""Standard-library exact checks, independent of the floating-point search."""
from itertools import product
from math import comb, factorial
from pathlib import Path
import json


def atom(H,L):
    return int(2*L+H>=0)-int(2*L-H>=0)


def kernel(t,L):
    j=(t-1)//2+L
    return comb(t-1,j) if 0<=j<=t-1 else 0


def dense_code():
    checks=0
    zero_sums=[]
    restored=0
    for t in (3,5,7):
        reps=[(1,)+s for s in product((-1,1),repeat=t-1)]
        radius=(t-1)//2
        for y in product((-1,1),repeat=t):
            H=[sum(a*b for a,b in zip(alpha,y)) for alpha in reps]
            for L in range(-radius-1,radius+2):
                values=[atom(h,L) for h in H]
                for i in range(t):
                    got=sum(alpha[i]*v for alpha,v in zip(reps,values))
                    assert got==kernel(t,L)*y[i]
                    checks+=1
        moment=sum((1 if L%2==0 else -1)*kernel(t,L) for L in range(-radius,radius+1))
        assert moment==0
        # Full kernel support included: alternating translated centers cancel.
        for L in range(-10,11):
            assert sum((1 if r%2==0 else -1)*kernel(t,L-r) for r in range(L-radius,L+radius+1))==0
                # Higher-degree weighting restores parity by a finite difference.
        for L in range(-10,11):
            got=sum((1 if r%2==0 else -1)*(r**(t-1))*kernel(t,L-r)
                    for r in range(L-radius,L+radius+1))
            expected=(1 if (L+radius)%2==0 else -1)*factorial(t-1)
            assert got==expected
            restored+=1
        zero_sums.append({'table_bits':t,'alternating_kernel_sum':moment})
    return {'exact_decoding_checks':checks,'parity_annihilation':zero_sums,
            'higher_degree_parity_restoration_checks':restored}


def certificate_checks():
    results=[]
    for p in sorted(Path(__file__).parent.glob('slab_certificate_m*.json')):
        c=json.loads(p.read_text());k,m=c['k'],c['m'];N=2**k
        margin=None;cases=0;atom_count=len(c['atoms'])
        for y in product((-1,1),repeat=N):
            table_values=[sum(v*z for v,z in zip(row['table'],y)) for row in c['atoms']]
            assert all(h%2 for h in table_values)
            for a in product((0,1),repeat=k*m):
                b=sum((sum(a[i*m:(i+1)*m])%2)<<i for i in range(k))
                score=sum(v*z for v,z in zip(c['affine_table_coefficients'],y))
                for row,H in zip(c['atoms'],table_values):
                    L=sum(v*z for v,z in zip(row['address'],a))-row['center']
                    score+=row['coefficient']*atom(H,L)
                signed=score*y[b]
                assert signed>0
                margin=signed if margin is None else min(margin,signed)
                cases+=1
        # Detect incompatible within-block sign patterns among actual atoms.
        incompatible=False
        for i in range(k):
            rows=[tuple(1 if w>0 else -1 for w in row['address'][i*m:(i+1)*m]) for row in c['atoms']]
            for p0 in rows:
                for q in rows:
                    incompatible |= p0!=q and p0!=tuple(-v for v in q)
        results.append({'file':p.name,'atoms':atom_count,'bottom_gates_unmerged':2*atom_count,
                        'raw_inputs_checked':cases,'exact_integer_margin':margin,
                        'no_common_coherent_reorientation':incompatible})
    return results


if __name__=='__main__':
    results={'Authors':'Christian Reitwiessner','status':'passed',
             'dense_code':dense_code(),'certificates':certificate_checks()}
    Path(__file__).with_name('followup_verification.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(results,indent=2))
