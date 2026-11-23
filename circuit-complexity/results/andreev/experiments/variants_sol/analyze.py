# Copyright (c) 2026 Christian Reitwiessner. All rights reserved.
# Authors: Christian Reitwiessner
"""Exact diagnostics and neighbor checks for the refuted seven-gate candidate."""
from research import *
from collections import Counter
for m in (1,2,3,4):
    n=4+2*m
    x=lambda j:[int(i==j) for i in range(n)]
    s1=[int(4<=i<4+m) for i in range(n)]
    r1=[(1 if i==4 else -1) if 4<=i<4+m else 0 for i in range(n)]
    r2=[(1 if i==4+m else -1) if i>=4+m else 0 for i in range(n)]
    plus=lambda *vs:[sum(a) for a in zip(*vs)]
    neg=lambda v:[-a for a in v]
    gates=[(plus(s1,neg(x(3))),1),(plus(s1,neg(x(3))),3),(plus(r1,neg(x(0))),0),(plus(r2,neg(x(0))),0),(plus(neg(r2),neg(x(1))),0),(plus(r1,r2,neg(x(0))),1),(plus(r1,r2,neg(x(0))),-1)]
    u=plus([2*a for a in x(2)],[2*a for a in s1],[-4*a for a in r2])
    c=Circuit(gates,[-4,-4,-6,-6,-8,6,6],u,-3)
    Z=((np.arange(1<<n)[:,None]>>np.arange(n))&1).astype(int);y=np.array([target(2,m,p) for p in Z]);bad=Z[c.eval_batch(Z)!=y]
    print('NEIGHBOR',m,'errors',len(bad),'domain',len(Z))
    if m==3:
        saved=Circuit.from_json(json.load(open(ROOT+'/near_2_3.json')))
        assert np.array_equal(saved.eval_batch(Z),c.eval_batch(Z))
        assert len(bad)==56
        assert all(tuple(p[4:7])==(0,1,1) or tuple(p[7:])==(0,1,1) for p in bad)
        print('BAD_BLOCK_PAIRS',dict(Counter((''.join(map(str,p[4:7])),''.join(map(str,p[7:]))) for p in bad)))
for m in (3,4,6):
    c=known(m);proof=check(c.to_json(),andreev_target(2,m),5000)
    save(c,f'baseline_2_{m}',dict(k=2,m=m,status='KNOWN_CONSTRUCTION_NOT_NEW',proof=proof))
    print('KNOWN',m,'bottom',c.S,'top',1,proof)
