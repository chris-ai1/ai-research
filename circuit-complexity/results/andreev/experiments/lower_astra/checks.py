# Copyright (c) 2026 Christian Reitwiessner.
# Authors: Christian Reitwiessner
"""Bounded exact checks; standard library only. No solvers or child jobs."""
import itertools, random, json, math
from fractions import Fraction as F
from pathlib import Path
print('Copyright (c) 2026 Christian Reitwiessner. Authors: Christian Reitwiessner')
OUT=Path(__file__).parent
rng=random.Random(736129)

def rank(rows):
    a=[[F(x) for x in row] for row in rows]
    if not a:return 0
    r=0
    for c in range(len(a[0])):
        piv=next((i for i in range(r,len(a)) if a[i][c]),None)
        if piv is None:continue
        a[r],a[piv]=a[piv],a[r]
        t=a[r][c];a[r]=[x/t for x in a[r]]
        for i in range(r+1,len(a)):
            t=a[i][c]
            if t:a[i]=[x-t*y for x,y in zip(a[i],a[r])]
        r+=1
        if r==len(a):break
    return r

def chi(mask,a):return (-1)**sum(a[i] for i in mask)

def profile_test(k,m,w):
    aa=list(itertools.product((0,1),repeat=k*m))
    sums=[sum(u*v for u,v in zip(w,a)) for a in aa]
    thresholds=range(min(sums),max(sums)+2)
    records=[]
    for r in range(1,k+1):
        RR=list(itertools.combinations(range(k),r))
        TT=[tuple(i*m+j for i in R for j in range(m)) for R in RR]
        eps=[math.prod(1 if w[i]>0 else -1 for i in T) if all(w[i] for i in T) else 0 for T in TT]
        vals=[]
        for t in thresholds:
            vals.append([sum(chi(T,a) for a,s in zip(aa,sums) if s>=t) for T in TT])
        rk=rank(vals)
        assert rk<=1
        for row in vals:
            for i,j in itertools.combinations(range(len(TT)),2):
                assert row[i]*eps[j]==row[j]*eps[i]
            assert all(v==0 for v,e in zip(row,eps) if e==0)
        records.append(rk)
    return records

results={'unit_profile':[], 'two_magnitude_counterexample':{}, 'mask_minimum':{}, 'survival_exact':[]}
for k,m in [(2,2),(2,3),(3,2)]:
    for trial in range(24):
        w=[rng.choice((-1,0,1)) for _ in range(k*m)]
        results['unit_profile'].append({'k':k,'m':m,'w':w,'ranks':profile_test(k,m,w)})
# Sharp first change of model: degree-1 profile rank can exceed one at |w| in {1,2}.
k=m=2
for w in itertools.product((1,2),repeat=4):
    aa=list(itertools.product((0,1),repeat=4))
    sums=[sum(u*v for u,v in zip(w,a)) for a in aa]
    rows=[[sum(chi(T,a) for a,s in zip(aa,sums) if s>=t) for T in [(0,1),(2,3)]] for t in range(sum(w)+2)]
    if rank(rows)>1:
        results['two_magnitude_counterexample']={'w':w,'threshold_rows_unnormalized':rows,'rank':rank(rows)};break
# Minimal number of full-support mask views meeting every layer-r rank condition.
for k in range(2,5):
    masks=list(itertools.product((0,1),repeat=k))
    lower=math.comb(k,k//2)
    found=None
    for dd in itertools.combinations(masks,lower):
        if all(rank([[chi(R,d) for d in dd] for R in itertools.combinations(range(k),r)])==math.comb(k,r) for r in range(1,k+1)):
            found=dd;break
    results['mask_minimum'][str(k)]={'lower_bound':lower,'attaining_rank_conditions':found}
# Exact count-restriction law: live position uniform, fixed ones size uniform.
# Check split iff the monotone min-to-max path crosses exactly once.
for k,m in [(1,6),(2,3),(3,2)]:
    for trial in range(10):
        w=[rng.choice((-13,-3,-1,0,1,2,17)) for _ in range(k*m)]
        t=rng.randrange(-12,13)
        p=F(0);cross=[F(0) for _ in range(k)];mass=F(0)
        choices=[]
        for i in range(k):
            cs=[]
            for live in range(m):
                other=[j for j in range(m) if j!=live]
                for vals in itertools.product((0,1),repeat=m-1):
                    s=sum(vals);prob=F(1,m*m*math.comb(m-1,s))
                    fixed=sum(w[i*m+j]*b for j,b in zip(other,vals))
                    cs.append((fixed,w[i*m+live],prob))
            choices.append(cs)
        for zz in itertools.product(*choices):
            prob=math.prod(z[2] for z in zz);mass+=prob
            low=sum(z[0]+min(0,z[1]) for z in zz)
            high=sum(z[0]+max(0,z[1]) for z in zz)
            split=low<t<=high
            if split:p+=prob
            current=low;n=0
            for i,z in enumerate(zz):
                nxt=current+abs(z[1]);hit=current<t<=nxt
                if hit:cross[i]+=prob;n+=1
                current=nxt
            assert n==int(split)
        assert mass==1 and p==sum(cross)
        results['survival_exact'].append({'k':k,'m':m,'weights':w,'threshold':t,'split':str(p),'path_terms':list(map(str,cross))})
(OUT/'checks.json').write_text(json.dumps({'authors':['Christian Reitwiessner'],**results},indent=2)+'\n')
print('PASS: 72 arbitrary-threshold unit-profile checks; 30 exact restriction distributions.')
print('Two-magnitude failure of rank-one:',results['two_magnitude_counterexample'])
print('Full-support mask rank minima:',results['mask_minimum'])
