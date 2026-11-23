# Copyright (c) 2026 Christian Reitwiessner.
# Authors: Christian Reitwiessner
"""Check the precision proposal's local scalar algebra and preserved source blocks."""
from pathlib import Path
from itertools import product
from fractions import Fraction
import json
root=Path(__file__).resolve().parent.parent
old=(root/'baseline.tex').read_text()
new=(root/'paper.tex').read_text()
def block(s, a, b):
    return s[s.index(a):s.index(b)+len(b)]
for a,b in [(r'\begin{abstract}',r'\end{abstract}'),
            (r'\begin{table}',r'\end{table}'),
            (r'\begin{thebibliography}',r'\end{thebibliography}'),
            (r'\paragraph{Relation to earlier work.}',r'\section{Compiling functions of affine forms}')]:
    assert block(old,a,b)==block(new,a,b), a
assert r'\documentclass[11pt]{article}' in new
assert r'\usepackage[margin=1in]{geometry}' in new
assert r'https://github.com/cslib-community/cslib-frontier/pull/2813' in new
for kind in ['theorem','lemma','proposition','proof']:
    assert old.count('\\begin{'+kind+'}')==new.count('\\begin{'+kind+'}'),kind
assert r'\( ' not in new and r'\[' not in new
cases=0
for k in [1,2,3]:
    N=2**k
    for m in [1,2,3]:
        alpha=(m-1)//2
        R=2*(N-1)+2*alpha*k+k*m
        C0=N*(R+4)
        for x in product([0,1],repeat=N):
            z=sum(x[1:]); e=sum(x[1<<i] for i in range(k))
            for us in product(range(m+1),repeat=k):
                u=sum(us); omega=2*z+2*alpha*e+u
                beta=sum((s%2)<<i for i,s in enumerate(us))
                ws={S:sum(x[c] for c in range(N) if (S&c).bit_count()%2)+alpha*sum(x[1<<i] for i in range(k) if S>>i&1) for S in range(1,N)}
                ts={S:sum(us[i] for i in range(k) if S>>i&1) for S in range(1,N)}
                kap={S:-4*(2*alpha+1)*(k-2*S.bit_count()) for S in range(1,N)}
                assert 0<=omega<=R
                assert all(0<=ws[S]<=N//2+alpha*S.bit_count() for S in ws)
                assert sum(4*ws[S]*(-1)**ts[S] for S in ws)==2*N*(beta==0)*z-2*N*(beta!=0)*x[beta]+2*alpha*N*sum(x[1<<i]*((beta==0)-(beta==1<<i)) for i in range(k))
                assert 8*sum(ws[S]**2+ws[S]*ts[S] for S in ws)==N//2*(omega**2-u**2)+2*N*z+(4*alpha+2*alpha**2)*N*e+2*N*(1+alpha)*sum(x[1<<i]*us[i] for i in range(k))
                assert 8*sum(((ts[S]+1)//2)**2 for S in ts)==N//2*(u**2+sum(s*s for s in us))+N*(u+1)*(beta!=0)+N*sum(us[i]*(beta==1<<i) for i in range(k))
                assert sum(kap[S]*Fraction(ts[S]%2,2) for S in ts)==N*(2*alpha+1)*sum(beta==1<<i for i in range(k))
                assert sum(kap[S]*ws[S] for S in ws)==2*N*(2*alpha+1)*(1+alpha)*e
                assert sum(Fraction(kap[S]*ts[S],2) for S in ts)==N*(2*alpha+1)*u
                stair=sum(-8*((2*ws[S]+ts[S]+1)//2)**2+kap[S]*((2*ws[S]+ts[S]+1)//2) for S in ws)
                P=2*N+stair+N//2*(omega**2+sum(s*s for s in us))+4*N*z-2*N*(alpha**2+1)*e-2*alpha*N*u+2*N*(1+alpha)*sum(x[1<<i]*us[i] for i in range(k))-C0*x[0]*(beta==0)
                closed=N*(omega+2)-C0*x[0] if beta==0 else (2*N*(1+alpha)*(1-x[beta])-N*us[beta.bit_length()-1] if beta.bit_count()==1 else N*(1-2*x[beta]))
                assert P==closed
                assert P*(1-2*x[beta])>=N
                cases+=1
balance_cases=0
for k in [1,2,4,8,16]:
    N=2**k; m=N//k; n=2*N; alpha=(m-1)//2
    count=N*(N-1)//2+k*N*(m+alpha)//2+2*(N-1)+2*alpha*k+3*k*m+(k*m+1)//2+1
    assert count==Fraction(5*n*n,16)-Fraction(n*k,4)+3*n-2*k-1
    balance_cases+=1
result={'Authors':'Christian Reitwiessner','status':'passed','appendix_pointwise_inputs':cases,
        'identities_per_input':6,'closed_form_and_margin_checks':cases,
        'exact_balance_size_expansions':balance_cases,
        'source_invariants':['abstract including margin TODO byte-identical','epsilon table and caption byte-identical','bibliography byte-identical','literature comparison prose byte-identical','all nine result statements and nine proofs retained','11pt and one-inch margins retained','cslib-frontier link retained'],
        'scope':'Finite checks of the transcribed appendix identities; universal validity relies on the paper proofs.'}
(root/'validation'/'precision_audit.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
