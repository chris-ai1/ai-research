"""Monte Carlo of the split probability p(g) under the randomised count restriction (uniform arrangement, uniform
cube, uniform table) for several gate types; compare with Lemma B1 (coherent: <= 1-(1-1/m)^k), Proposition F
(balanced gates ~ sqrt(k/m)) and Lemma B3 (O(k m^{-1/3}))."""
import sys; sys.path.insert(0,'/tmp/pydeps')
import numpy as np
rng=np.random.default_rng(5)
def p_split(Gam,theta,trials=40000):
    k,m=Gam.shape; hits=0
    for _ in range(trials):
        fixed=0.0; lo=0.0; hi=0.0
        for i in range(k):
            perm=rng.permutation(m); c=rng.integers(0,m)
            fixed+=Gam[i,perm[:c]].sum(); lam=Gam[i,perm[c]]
            lo+=min(0,lam); hi+=max(0,lam)
        t=theta-fixed
        hits+= (lo<t<=hi)
    return hits/trials
k,m=3,64
gates={'block-symmetric (all ones)':np.ones((k,m)),
       'coherent heavy-tailed':rng.exponential(1,(k,m))**3,
       'subset-majority (|T|=8 per block)':np.array([[1.0 if t<8 else 0 for t in range(m)] for _ in range(k)]),
       'balanced +-1':rng.choice([-1.0,1.0],(k,m)),
       'gaussian':rng.normal(size=(k,m))}
for name,G in gates.items():
    # threshold at the median of the full sum over random inputs, to make survival as likely as possible
    th=np.median([ (G*(rng.random((k,m))<rng.random((k,1)))).sum() for _ in range(2000)])
    print(f'{name:36s}: p(g) ~ {p_split(G,th):.4f}   [coherent bound {1-(1-1/m)**k:.4f}; sqrt(k/m)={np.sqrt(k/m):.3f}; k m^(-1/3)={k*m**(-1/3):.3f}]',flush=True)
