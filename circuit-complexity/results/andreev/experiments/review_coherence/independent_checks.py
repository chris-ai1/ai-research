#!/usr/bin/env python3
# Authors: Christian Reitwiessner
"""Independent finite checks. No source-review scripts are imported.
Exact arithmetic for small instances; fixed-seed Monte Carlo is only evidence.
"""
import itertools
import json
import math
from collections import defaultdict
from fractions import Fraction
from pathlib import Path
import sys
sys.path.insert(0, '/tmp/andreev_gap/coherence_fable/pydeps_local')
import numpy as np

ROOT = Path(__file__).resolve().parent
OUT = {'authors': 'Christian Reitwiessner', 'seed': 20261109}
print('Authors: Christian Reitwiessner', flush=True)

def exact_block(weights):
    m = len(weights)
    out = defaultdict(Fraction)
    for live, w in enumerate(weights):
        others = weights[:live] + weights[live+1:]
        for bits in itertools.product((0, 1), repeat=m-1):
            r = sum(bits)
            f = sum(x*y for x, y in zip(others, bits))
            out[(f + min(0,w), f + max(0,w))] += Fraction(1, m*m*math.comb(m-1,r))
    assert sum(out.values()) == 1
    return out

def exact_split(blocks):
    dist = {(0,0): Fraction(1)}
    for block in blocks:
        nxt = defaultdict(Fraction)
        for (lo,hi), p in dist.items():
            for (l,h), q in exact_block(block).items():
                nxt[(lo+l,hi+h)] += p*q
        dist = nxt
    # Integer weights: theta=t+1/2 covers all distinct split events lo<theta<=hi.
    thresholds = range(min(lo for lo,hi in dist), max(hi for lo,hi in dist)+1)
    vals = [(sum(p for (lo,hi),p in dist.items() if lo<=t<hi), t) for t in thresholds]
    p,t = max(vals)
    return {'max_split': str(p), 'max_split_float':float(p), 'theta': t+0.5,
            'states':len(dist)}

small = {
    'coherent': [[1]*8,[1]*8],
    'biased': [[1]*6+[-1]*2,[1]*6+[-1]*2],
    'zero_drift': [[1]*4+[-1]*4]*2,
    'near_zero': [[1]*5+[-1]*3]*2,
    'bounded_magnitudes': [[4,4,1,1,1,-1,-1,-1],[1]*8],
    'few_drift_bits_W4': [[4,4,1,-1,1,-1,1,-1]]*2,
    'heavy_tail': [[1,-1,2,-2,4,-4,32,32]]*2,
    'local_global_counterexample': [[1]*8,[100]*4+[-100]*4],
}
OUT['exact_split'] = {}
for name, blocks in small.items():
    row=exact_split(blocks)
    row['blocks']=blocks
    OUT['exact_split'][name]=row
    print('EXACT',name,row,flush=True)

# Independent barrier entropy computation from the actual truth vectors, including
# merging BOTH constant vectors into the inactive symbol.
def symbol(vec):
    return 'inactive' if len(set(vec)) == 1 else tuple(vec)
barrier_count=0
for k in range(1,5):
    for K in range(7):
        actual=0
        total=2**(K+k)
        for signs in itertools.product((-1,1),repeat=K+k):
            f=sum(signs[:K]); lam=signs[K:]
            vecs=[tuple(int(f+sum(a*b for a,b in zip(lam,z))+x>=0.5)
                        for z in itertools.product((0,1),repeat=k)) for x in (0,1)]
            depends=vecs[0]!=vecs[1]
            informative=symbol(vecs[0])!=symbol(vecs[1])
            P=sum(w>0 for w in lam)
            formula=(-P<=f<=k-P)
            assert depends==informative==formula
            actual+=informative
            barrier_count+=1
        assert actual/total >= 1/math.sqrt(2*K+2)
OUT['barrier_truth_vector_cases']=barrier_count

# Counterexample to the source's reversed entropy activity interval.
# g=[x+z>=1], true active table x=0, source interval (0,1] selects x=1.
OUT['activity_endpoint_counterexample']={
    'gate':'[x+z>=1]', 'breakpoints':[0,1],
    'truth_at_x0':[0,1], 'truth_at_x1':[1,1],
    'actual_active_x':[0], 'source_window_selected_x':[1]}
# An unequal-mass tie example makes the source entropy bound itself fail.
# g=[x1+x2+z>=1] has activity 1/4 vs source p=1/2 (not failure);
# g=[x1+x2+z>=2] has activity 1/2 vs source p=1/4.
OUT['activity_endpoint_entropy_counterexample']={
    'gate':'[x1+x2+z>=2]', 'actual_H':1.0,
    'source_p':0.25, 'source_h_plus_p_k':-(.25*math.log2(.25)+.75*math.log2(.75))+.25}
# More table bits amplify it: choose gate at first count after the mode.
for r in range(2,31):
    for t in range(1,r+1):
        pa=math.comb(r,t-1)/2**r
        ps=math.comb(r,t)/2**r
        def h(p): return -(p*math.log2(p)+(1-p)*math.log2(1-p)) if 0<p<1 else 0.
        k=max(1,math.ceil(math.log2(r)))
        if h(pa)>h(ps)+k*ps+1e-12:
            OUT['activity_endpoint_entropy_counterexample']={'gate':f'[sum_{r}_table_bits+z>={t}]',
                'k':k,'N':2**k,'actual_p':pa,'source_p':ps,'actual_H':h(pa),'source_h_plus_p_k':h(ps)+k*ps}
            break
    else: continue
    break

# Proposition 5.1: sparse attainable range, verified on EVERY raw input.
# L=3(y1+y2); two steps suffice for sign parity although range/2=3.
assert all(int(-1+2*(3*sum(y)>=3)-2*(3*sum(y)>=6)>=0)==sum(y)%2
           for y in itertools.product((0,1),repeat=2))
OUT['prop5_counterexample']={'M':2,'coefficients':[3,3], 'range':6,
                           'bottom_gates':2,'claimed_minimum':3}
# Dictator dominance interval, exact exhaustive integer coefficients.
checked=0
for w in itertools.product(range(-2,3),repeat=3):
    for c in range(-6,7):
        actual=all(int(sum(a*b for a,b in zip(w,x))+c>=0)==x[0]
                   for x in itertools.product((0,1),repeat=3))
        bound=(c+sum(max(0,t) for t in w[1:])<0 <= c+w[0]+sum(min(0,t) for t in w[1:]))
        assert actual==bound
        checked+=1
OUT['dominance_cases']=checked

rng=np.random.default_rng(20261109)
def sample(blocks, trials=60000, batch=2000):
    weights=np.array(blocks,dtype=np.int64)
    k,m=weights.shape
    G=int(np.max(np.abs(weights)))
    threshold=float(weights.sum()/2+0.5)
    hits=0
    low_hits=0
    for start in range(0,trials,batch):
        B=min(batch,trials-start)
        lo=np.zeros(B,dtype=np.int64)
        hi=np.zeros(B,dtype=np.int64)
        for w in weights:
            live=rng.integers(m,size=B)
            q=rng.random(B)
            fixed=rng.random((B,m))<q[:,None]
            fixed[np.arange(B),live]=False
            f=fixed@w
            lo+=f+np.minimum(w[live],0)
            hi+=f+np.maximum(w[live],0)
        hits+=int(np.count_nonzero((lo<threshold)&(threshold<=hi)))
        low_hits+=int(np.count_nonzero((lo<0.5)&(0.5<=hi)))
    p=hits/trials
    row={'m':m,'k':k,'G':G,'delta_blocks':list(np.abs(weights.sum(axis=1))/(m*G)),
         'global_W_blocks':[float(G/min(abs(w))) if min(abs(w)) else None for w in weights],
         'theta':threshold,'trials':trials,'split':p,
         'standard_error':math.sqrt(p*(1-p)/trials),'theta_half_split':low_hits/trials}
    return row
OUT['monte_carlo']=[]
for m in (64,256,1024):
    r=int(math.sqrt(m))
    if r%2: r+=1
    families={
        'constant_drift': [1]*(3*m//4)+[-1]*(m//4),
        'zero_drift': [1]*(m//2)+[-1]*(m//2),
        'minimum_valid_drift': [1]*(m//2+1)+[-1]*(m//2-1),
        'few_drift_bits_W4': [4]*r+[1]*((m-r)//2)+[-1]*((m-r)//2),
        'heavy_tail_few_drift': [m]*r+[1]*((m-r)//2)+[-1]*((m-r)//2),
        'sparse_few_drift': [1]*r+[0]*(m-r),
    }
    for name,w in families.items():
        row=sample([w,w]);row['family']=name
        OUT['monte_carlo'].append(row)
        print('MC',row,flush=True)
    row=sample([[1]*m,[10*m]*(m//2)+[-10*m]*(m//2)])
    row['family']='local_global_counterexample'
    # median theta=m/2+.5 is between 0 and m, unlike the proof's m+.5;
    # this test still shows the same bridge crossing order, not its exact subset.
    OUT['monte_carlo'].append(row)
    print('MC',row,flush=True)
(ROOT/'checks.json').write_text(json.dumps(OUT,indent=2)+'\n')
print('DONE',flush=True)
