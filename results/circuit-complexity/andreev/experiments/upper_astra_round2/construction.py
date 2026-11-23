# Copyright (c) 2026 Christian Reitwiessner.
# Authors: Christian Reitwiessner
"""Explicit raw-input gate builder for fixed independently chosen masks.

Random sampling alone does not certify a seed's agreement. The report proves
existence; verify a chosen seed or use exhaustive conditional expectation.
"""
from math import ceil,sqrt,log

def radius(k,m,r,delta):
    t=1<<r;V=(1<<k)+r*m/4
    if t==1:return 0
    return ceil(4*sqrt(V*log(16*V/(t*delta))))

def build(k,m,r,R,masks):
    assert k>=1 and m>=1 and 0<=r<=k and R>=0
    N=1<<k;t=1<<r;gates=[]
    for s in range(1,t):
        chi=[(-1)**((s&c).bit_count()%2) for c in range(N)]
        active=[i*m+j for i in range(r) if s>>i&1 for j in range(m)]
        z=masks[s];assert len(z)==len(active) and all(v in (0,1) for v in z)
        h=len(active)//2;sig=(-1)**((sum(z)+h)%2)
        def f(u):return (-1)**(u%2)*u if abs(u)<=R else 0
        for sign in (1,-1):
            w=[2*v for v in chi]+[0]*(k*m)
            for j,v in zip(active,z):w[N+j]=sign*(1-2*v)
            const=-sum(chi)+sign*(sum(z)-h)
            for ell in range(-R,R+2):
                top=sig*(f(ell)-f(ell-1))
                if top:gates.append({'weights':w.copy(),'threshold':ell-const,'top_weight':top})
    return {'Authors':'Christian Reitwiessner','k':k,'m':m,'r':r,'R':R,
            'gates':gates,'raw_top_weights':[4]*N+[0]*(k*m),
            'top_constant':-2*N,'top_threshold':0 if t==N else -2*t}
