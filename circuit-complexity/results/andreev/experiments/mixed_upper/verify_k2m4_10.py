"""Bit-level exhaustive check of the 10-gate block-symmetric circuit for A_{2,4} found by the pool MILP."""
import itertools
gates=[((0,1,0,0),(0,1),2,-12),((0,1,0,0),(0,1),4,-12),((1,0,0,0),(0,1),2,-16),((1,0,0,0),(0,1),4,-16),
       ((0,0,0,1),(1,-1),1,6),((0,1,0,0),(1,-1),1,-6),((0,1,0,0),(1,0),2,8),((0,1,0,0),(1,0),4,8),
       ((0,0,0,1),(1,1),5,6),((0,1,0,0),(1,1),5,-6)]
mu=(16,12,2,0); nu=(-4,14); t0=15; m=4
bad=0; minslack=None
for z in itertools.product((0,1),repeat=4+2*m):
    x=z[:4]; a1=z[4:4+m]; a2=z[4+m:]
    s=(sum(a1),sum(a2))
    tot=sum(w for (al,be,th,w) in gates if sum(p*q for p,q in zip(al,x))+be[0]*s[0]+be[1]*s[1]>=th)
    tot+=sum(p*q for p,q in zip(mu,x))+nu[0]*s[0]+nu[1]*s[1]-t0
    y=x[(s[0]%2)+2*(s[1]%2)]
    sl=tot if y else -tot
    minslack=sl if minslack is None else min(minslack,sl)
    if sl<1: bad+=1
print('inputs',2**(4+2*m),'errors',bad,'min signed slack',minslack)
