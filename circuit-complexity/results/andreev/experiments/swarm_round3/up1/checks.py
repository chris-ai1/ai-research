# Copyright (c) 2026 Christian Reitwiessner.
# Authors: Christian Reitwiessner
"""Exact finite guardrails for the written UP1 round-three proofs."""
import itertools
from math import comb, gcd
import json
import random
from fractions import Fraction
from pathlib import Path

rng = random.Random(3112026)
counts = dict(conjunction_gate=0, polynomial_score=0, cocycle=0,
              witness_inputs=0, optimum_error=0, hull_witness=0, bridge_localtime=0, difference_stencil=0)

for ntable, naddress in [(2,2),(3,2),(4,2)]:
    rows=list(itertools.product((0,1),repeat=ntable+naddress))
    for _ in range(35):
        coeff=[rng.randint(-5,5) for _ in range(ntable+naddress)]
        bias=rng.randint(-6,6)
        vals=[bias+sum(c*z for c,z in zip(coeff,row)) for row in rows]
        big=1+max(map(abs,vals))
        lits={i:rng.randrange(2) for i in range(ntable) if rng.randrange(2)}
        for row, val in zip(rows,vals):
            sat=sum(row[i]==bit for i,bit in lits.items())
            lhs=int(sat==len(lits))*int(val>=0)
            rhs=int(val+big*(sat-len(lits))>=0)
            assert lhs==rhs
            counts['conjunction_gate']+=1
        bank=[]
        for j in range(3):
            cc=[rng.randint(-3,3) for _ in row]
            bb=rng.randint(-4,4)
            bank.append((cc,bb,rng.randint(-3,3)))
        raw=[rng.randint(-3,3) for _ in row]
        constant=rng.randint(-4,4)
        monomials=[]
        for j in range(3):
            ll={i:rng.randrange(2) for i in range(ntable) if rng.randrange(2)}
            monomials.append((rng.randint(-3,3),ll))
        for row in rows:
            H=constant+sum(c*z for c,z in zip(raw,row))
            H+=sum(v*int(bb+sum(c*z for c,z in zip(cc,row))>=0) for cc,bb,v in bank)
            P=sum(p*int(all(row[i]==bit for i,bit in ll.items())) for p,ll in monomials)
            out=0
            for p,ll in monomials:
                C=int(all(row[i]==bit for i,bit in ll.items()))
                out+=p*constant*C
                out+=sum(p*c*int(C and z) for c,z in zip(raw,row))
                sat=sum(row[i]==bit for i,bit in ll.items())
                for cc,bb,v in bank:
                    B=1+abs(bb)+sum(map(abs,cc))
                    out+=p*v*int(bb+sum(c*z for c,z in zip(cc,row))+B*(sat-len(ll))>=0)
            assert out==P*H
            counts['polynomial_score']+=1

for R in range(1,41):
    r=(R+1)//2
    fun=[{t:rng.randint(-20,20) for t in range(-2*R,2*R+1)} for _ in range(4)]
    def H(u,v):
        return fun[0][u+v]+fun[1][u-v]+fun[2][u]+fun[3][v]
    def odd4(u,v):
        return H(u,v)-H(u,-v)-H(-u,v)+H(-u,-v)
    for q in range(1,r+1):
        assert sum(odd4(2*i-1,1) for i in range(1,q+1))==odd4(q,q)
        counts['cocycle']+=1
    amp=[]
    errors=[]
    def F(t):
        return min(abs(t)//2,r)
    values=[i for i in range(-R,R+1) if i]
    for u,v in itertools.product(values,repeat=2):
        value=F(u+v)-F(u-v)
        expanded=0
        for q in range(1,r+1):
            expanded+=int(u+v>=2*q)+int(-u-v>=2*q)-int(u-v>=2*q)-int(-u+v>=2*q)
        assert value==expanded
        target=1 if u*v>0 else -1
        amp.append(target*value)
        errors.append(abs(Fraction(2*value,r+1)-target))
        counts['witness_inputs']+=1
    assert min(amp)==1 and max(amp)==r
    assert max(errors)==Fraction(r-1,r+1)
    counts['optimum_error']+=1

for R in [Fraction(31,10),Fraction(7,2),Fraction(4),Fraction(10),Fraction(101)]:
    t=(1+(R-1)/2)/2
    hi=(2*t+1+R)/2
    lo=hi-2*t
    assert 1<t<R and 1<hi<R and 1<lo<R
    assert (hi-lo)/2==t
    counts['hull_witness']+=1

for h in range(0,15):
    for q in range(h//2+1):
        p=h-q
        delta=p-q
        visits={ell:0 for ell in range(-h-1,h+2)}
        total=comb(h,q)
        for minus in itertools.combinations(range(h),q):
            minus=set(minus)
            pos=0
            visits[pos]+=1
            for t in range(h):
                pos+=-1 if t in minus else 1
                visits[pos]+=1
            assert pos==delta
        for ell,v in visits.items():
            distance=max(0,-ell,ell-delta)
            predicted=sum(comb(h+1,i) for i in range(q-distance+1))
            assert v==predicted
            assert Fraction(v,total)<=Fraction(h+1,delta+1)
            counts['bridge_localtime']+=1

certificate=None
for trial in range(120):
    directions=set()
    for _ in range(1+trial%5):
        a,b=rng.randint(1,4),rng.choice((-1,1))*rng.randint(1,4)
        common=gcd(abs(a),abs(b))
        directions.add((a//common,b//common))
    directions=sorted(directions)
    tangent=[(b,-a) for a,b in directions]
    slope=1
    while any(x+slope*y==0 for x,y in tangent):
        slope+=1
    chosen=[v for v in tangent if v[0]+slope*v[1]>0]
    sx=sum(x for x,y in chosen)
    sy=sum(y for x,y in chosen)
    start=(-1-sx,-1-sy)
    steps=[(1,0),(0,1)]+tangent
    stencil={}
    for bits in itertools.product((0,1),repeat=len(steps)):
        x=start[0]+sum(bit*v[0] for bit,v in zip(bits,steps))
        y=start[1]+sum(bit*v[1] for bit,v in zip(bits,steps))
        point=(2*x+1,2*y+1)
        sign=(-1)**(len(steps)-sum(bits))
        stencil[point]=stencil.get(point,0)+sign
    stencil={p:c for p,c in stencil.items() if c}
    D=max(sum(abs(a) for a,b in directions),sum(abs(b) for a,b in directions))
    assert all(u and v and max(abs(u),abs(v))<=2*D+1 for u,v in stencil)
    target=sum(c*(1 if u*v>0 else -1) for (u,v),c in stencil.items())
    assert target==4*(-1)**(len(tangent)-len(chosen))
    for a,b in directions+[(1,0),(0,1)]:
        totals={}
        for (u,v),c in stencil.items():
            value=a*u+b*v
            totals[value]=totals.get(value,0)+c
        assert all(c==0 for c in totals.values())
    counts['difference_stencil']+=1
    if certificate is None or len(stencil)>len(certificate['stencil']):
        certificate={'Authors':'Christian Reitwiessner',
            'scope':'Equality obstruction only, not a positive sign-computation dual.',
            'directions':directions,'radius':2*D+1,'target_evaluation':target,
            'stencil':[[u,v,c] for (u,v),c in sorted(stencil.items())]}
Path(__file__).with_name('stencil_certificate.json').write_text(json.dumps(certificate,indent=2)+'\n')

result={'Authors':'Christian Reitwiessner','status':'all exact checks passed','counts':counts,
        'scope':'Finite algebraic guardrails, not asymptotic inference or an Andreev circuit.'}
Path(__file__).with_name('checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
