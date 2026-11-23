# Copyright (c) 2026 Christian Reitwiessner
# Authors: Christian Reitwiessner
"""Exact mixed-mask coarse-product windows and convolution diagnostics."""
from itertools import product
from math import comb
import json
from pathlib import Path

def choose(n,r):
    return comb(n,r) if 0 <= r <= n else 0

def spectrum(M,p,q):
    return [sum((-1)**j*choose(d,j)*choose(M-d,t-j)
                for t in range(p,q+1) for j in range(d+1))
            for d in range(M+1)]

def window_gates(blocks,mask,p,q,hweights,r,B):
    """Each gate is (address weights, table weights, cutoff, top weight).
    L=|a XOR mask|. hweights acts directly on raw independent table bits.
    Requires |h-r| < B on the domain. Integer h,r,B are sufficient.
    """
    M=sum(blocks)
    assert len(mask)==M and 0<=p<=q<=M
    offset=sum(mask)
    pi=[1-2*z for z in mask]
    sign=(-1)**offset
    gates=[]
    for level in range(p,q+1):
        gates.append(([B*v for v in pi],list(hweights),
                      B*(level-offset)+r,2*sign*(-1)**level))
    for level,coefficient in [(p,-sign*(-1)**p),(q+1,-sign*(-1)**q)]:
        # Constant gates are retained, so length+2 is an unconditional count.
        gates.append((pi,[0]*len(hweights),level-offset,coefficient))
    return gates

def evaluate(gates,a,x):
    return sum(w for aw,xw,t,w in gates
               if sum(v*z for v,z in zip(aw,a))+sum(v*z for v,z in zip(xw,x))>=t)

def check():
    checks=0
    # Each active block mixes signs; masks are not a common input relabeling.
    blocks=[3,3]
    masks=[[0,0,1,0,1,1],[0,1,0,1,0,1],[1,0,0,0,1,0]]
    hweights=[1,-1,1,-1]
    for mask in masks:
        for p,q in [(3,3),(2,4),(1,5),(0,6)]:
            for r in [0,1]:
                gs=window_gates(blocks,mask,p,q,hweights,r,4)
                assert len(gs)==q-p+3
                for aw,_,_,_ in gs:
                    assert all(min(aw[3*i:3*i+3])<0<max(aw[3*i:3*i+3]) for i in range(2))
                for a in product((0,1),repeat=6):
                    L=sum(u!=v for u,v in zip(a,mask))
                    for x in product((0,1),repeat=4):
                        h=sum(u*v for u,v in zip(hweights,x))
                        target=(-1)**sum(a)*(2*int(h>=r)-1)*int(p<=L<=q)
                        assert evaluate(gs,a,x)==target
                        checks+=1
    # Independent Boolean Fourier summation, not the binomial formula.
    for M in range(2,11):
        for p,q in [(M//2,M//2),(max(0,M//2-1),min(M,M//2+1))]:
            sp=spectrum(M,p,q)
            for d in range(M+1):
                brute=sum((-1)**sum(a[:d]) for a in product((0,1),repeat=M) if p<=sum(a)<=q)
                assert brute==sp[d]
    rows=[]
    for M in [4,6,8,10,12,16,24,32,48,64]:
        for radius in range(min(4,M//2)):
            p,q=M//2-radius,M//2+radius
            sp=spectrum(M,p,q)
            zeros=[d for d in range(2,M+1,2) if sp[d]==0]
            if radius==0: assert not zeros
            rows.append(dict(M=M,radius=radius,layers=q-p+1,zero_even_degrees=zeros,
                             constant_coverage_support_lower=(1<<(M-1)) if not zeros else None))
    # Exact sharp constant-coverage witness for central layers: one mask from
    # every complement pair, uniformly weighted, makes all windows sum C(M,M/2)/2.
    # This uses coherent masks too; it is a diagnostic, not an admissible circuit.
    covers=[]
    for M in [2,4,6,8,10]:
        masks=list(product((0,1),repeat=M-1))
        values=[]
        for a in product((0,1),repeat=M):
            v=sum(sum(u!=v for u,v in zip(a,(0,)+z))==M//2 for z in masks)
            assert 2*v==comb(M,M//2)
            values.append(v)
        covers.append(dict(M=M,masks=len(masks),coverage=values[0]))
    # Simple exact mixed-only, variable-width identity on two four-bit blocks.
    mask44=[z for z in product((0,1),repeat=8)
            if sum(z[:4]) in (1,3) and sum(z[4:]) in (1,3)]
    for a in product((0,1),repeat=8):
        value=0
        for z in mask44:
            d=sum(u!=v for u,v in zip(a,z))
            value+=3*int(d==4)+4*int(3<=d<=5)+21*int(1<=d<=7)
        assert value==1568
    return dict(mixed44_cover=dict(masks=64,addresses=256,integer_constant=1568),Authors='Christian Reitwiessner',integer_gadget_checks=checks,
                central_cover_checks=covers,spectral_scan=rows)

if __name__=='__main__':
    result=check()
    Path(__file__).with_name('exact_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
