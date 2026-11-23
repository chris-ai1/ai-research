"""k=2 'parity-only' bulk model: F = D(x) + sum_S A_S(x) e_S, where A_S = sum of n_S two-valued
gadgets  Delta_g * t_g(x),  t_g(x) in {+1,-1} ARBITRARY functions of x.  For a configuration (n_1,n_2,n_12)
decide feasibility: exists Delta>0 such that every table x admits signs making the scores separate.
Search: random + grid Delta vectors (necessary-condition search, prints the best fraction of tables)."""
import sys; sys.path.insert(0,"/tmp/pydeps")
import itertools, numpy as np
rng=np.random.default_rng(1)
tabs=[tuple((t>>c)&1 for c in range(4)) for t in range(16)]
def table_ok(x,E):
    ones=[E[i] for i in range(4) if x[i]]; zeros=[E[i] for i in range(4) if not x[i]]
    return (not ones) or (not zeros) or min(ones)>max(zeros)+1e-9
def count_ok(conf,D):
    # conf: list of character ids per gadget (1,2,3); D: deltas
    G=len(conf); ok=0
    signs=list(itertools.product((1,-1),repeat=G))
    for x in tabs:
        good=False
        for sg in signs:
            A={1:0.0,2:0.0,3:0.0}
            for g in range(G): A[conf[g]]+=sg[g]*D[g]
            E=[0,A[1]+A[3],A[2]+A[3],A[1]+A[2]]
            if table_ok(x,E): good=True;break
        ok+=good
    return ok
for name,conf in [('(1,1,1)',[1,2,3]),('(2,1,1)',[1,1,2,3]),('(1,1,2)',[1,2,3,3]),('(3,1,1)',[1,1,1,2,3]),('(2,2,1)',[1,1,2,2,3]),('(2,1,2)',[1,1,2,3,3])]:
    best=0;bestD=None
    for trial in range(4000):
        D=rng.uniform(0.05,1,len(conf))*rng.choice([1,2,4,8],len(conf))
        c=count_ok(conf,D)
        if c>best: best=c;bestD=D
        if best==16: break
    print(name,'best #tables satisfiable =',best,'/16', 'D=',None if bestD is None else np.round(bestD,3),flush=True)
