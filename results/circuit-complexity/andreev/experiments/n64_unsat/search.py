#!/usr/bin/env python3
# Copyright (c) 2026 Christian Reitwiessner.
# Authors: Christian Reitwiessner
"""Unrestricted real-weight lower-bound search on valid n64 Andreev inputs."""
import argparse
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
import random
import sys
import time

sys.path.insert(0,'/tmp/pydeps')
import z3
from mscore import Enc, eval_circuit, parity_points
import smt_symbolic_check as independent

AUTHOR='Christian Reitwiessner'
def save(p,obj=None,**fields):
    p.write_text(json.dumps(dict(Authors=AUTHOR,**(obj or {}),**fields),indent=2,default=str)+'\n')

def label(point,lengths):
    N=1<<len(lengths);offset=N;b=0
    for i,m in enumerate(lengths):
        b|=(sum(point[offset:offset+m])%2)<<i;offset+=m
    return point[b]

def spread(lengths):
    out=[];offsets=[];offset=0
    for m in lengths:offsets.append(offset);offset+=m
    for t in range(max(lengths)):
        out.extend(offsets[i]+t for i,m in enumerate(lengths) if t<m)
    return out

def initial(lengths,S,seed):
    N=1<<len(lengths);D=sum(lengths);rng=random.Random(seed);points={}
    # Every point below is a genuine input to the declared n64 target.
    # The fixed Walsh parity table turns the active address cube into parity.
    dimension=min(2*S+2,10);active=spread(lengths)[:dimension]
    x=tuple(c.bit_count()%2 for c in range(N))
    for bits in product((0,1),repeat=dimension):
        a=[0]*D
        for j,v in zip(active,bits):a[j]=v
        p=x+tuple(a);points[p]=label(p,lengths)
    tables=[tuple(int(c==u) for c in range(N)) for u in range(N)]
    tables+=[tuple((c&u).bit_count()%2 for c in range(N)) for u in range(1,N)]
    # Add multiple actual tables/arrangements, not a restricted circuit class.
    for j in range(128):
        xx=tables[j%len(tables)] if j<96 else tuple(rng.randrange(2) for _ in range(N))
        a=tuple(rng.randrange(2) for _ in range(D));p=xx+a;points[p]=label(p,lengths)
    return list(points.items())

def checker(c,lengths,timeout,batch=12):
    N=1<<len(lengths);D=sum(lengths)
    x=[z3.Bool(f'x{j}') for j in range(N)];a=[z3.Bool(f'a{j}') for j in range(D)]
    bits=x+a;gs=[independent.threshold(bits,w,t) for w,t in c['bottom']]
    prediction=independent.threshold(gs+bits,c['v']+c['u'],c['tau'])
    ps=[];offset=0
    for m in lengths:ps.append(independent.parity(a[offset:offset+m]));offset+=m
    values=x[:]
    for b in ps:values=[z3.If(b,values[j+1],values[j]) for j in range(0,len(values),2)]
    s=z3.Solver();s.add(z3.Xor(prediction,values[0]));start=time.monotonic();examples=[]
    for _ in range(batch):
        remaining=timeout-(time.monotonic()-start)
        if remaining<=0:return dict(status='COUNTEREXAMPLES' if examples else 'UNKNOWN',examples=examples,seconds=time.monotonic()-start)
        s.set(timeout=max(1,int(1000*remaining)));result=s.check()
        if result!=z3.sat:
            return dict(status=('COUNTEREXAMPLES' if examples else ('VERIFIED' if result==z3.unsat else 'UNKNOWN')),
                        examples=examples,seconds=time.monotonic()-start,reason=s.reason_unknown() if result==z3.unknown else '')
        model=s.model();p=tuple(int(z3.is_true(model.eval(b,model_completion=True))) for b in bits)
        y=label(p,lengths);assert eval_circuit(c,[(p,y)])
        examples.append((p,y));s.add(z3.Or([b!=bool(v) for b,v in zip(bits,p)]))
    return dict(status='COUNTEREXAMPLES',examples=examples,seconds=time.monotonic()-start)

def parity_certificate(out,timeout):
    """An exact n64 restriction, solved in its affine-equivalent 8-bit domain.
    Any Andreev circuit restricts to a parity circuit with unchanged bottom count.
    Parity's input flip/output complement symmetries justify sorted nonnegative
    direct weights here. They are NOT imposed on later arbitrary input samples.
    """
    pts=parity_points(8);t0=time.monotonic()
    e=Enc(pts,3,dict(vsym=True,usym='parity_even',seed=7))
    for j in sorted(range(len(pts)),key=lambda i:(sum(pts[i][0]),pts[i][0])):e.add_point(j)
    e.so.set(timeout=int(timeout*1000));started=time.monotonic();result=e.so.check()
    data=dict(kind='parity8_affine_restriction',bottoms=3,status=str(result).upper(),
              solver_seconds=time.monotonic()-started,wall_seconds=time.monotonic()-t0,
              points=256,logic='QF_LRA',weights='unrestricted reals',solver=z3.get_version_string(),
              normalization='Valid unrestricted finite-domain unit margins; gate complement/permutation; parity-only direct-weight symmetries')
    if result==z3.unsat:
        (out/'parity8_S3_unsat.smt2').write_text(e.so.to_smt2())
        data['consequence']='Both n64 instances need at least 4 bottom gates, hence 5 total gates, via the explicit restriction.'
    elif result==z3.sat:
        c=e.circuit(e.so.model());assert not eval_circuit(c,pts);save(out/'parity8_candidate.json',candidate=c)
    else:data['reason']=e.so.reason_unknown()
    embeddings=[]
    for lengths in ([12]*4,[7,7,6,6,6]):
        N=1<<len(lengths);x=tuple(c.bit_count()%2 for c in range(N));active=spread(lengths)[:8]
        rows=[]
        for bits,y in pts:
            a=[0]*sum(lengths)
            for d,b in zip(active,bits):a[d]=b
            p=x+tuple(a);assert len(p)==64 and label(p,lengths)==y
            rows.append(dict(input=p,target=y))
        embeddings.append(dict(block_lengths=lengths,points=rows))
    save(out/'parity_restriction_embeddings.json',embeddings=embeddings)
    save(out/'parity8_S3.json',**data);print(json.dumps(data),flush=True)

def run(args):
    out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    if args.certificate:return parity_certificate(out,args.timeout)
    lengths=list(map(int,args.blocks.split(',')));N=1<<len(lengths);assert N+sum(lengths)==64
    if (out/'events.jsonl').exists():raise SystemExit('Use a fresh output directory.')
    start=time.monotonic();pts=initial(lengths,args.S,args.seed);seen={p for p,y in pts}
    usym=[]
    if args.input_symmetry:
        offset=N
        for m in lengths:
            usym.extend(('ge0',d) for d in range(offset,offset+m))
            usym.extend(('le',d,d+1) for d in range(offset,offset+m-1))
            offset+=m
    e=Enc(pts,args.S,dict(cls='free',vsym=True,usym=usym,seed=args.seed))
    def event(**row):
        row['elapsed']=time.monotonic()-start
        with (out/'events.jsonl').open('a') as f:f.write(json.dumps(row,default=str)+'\n')
        print(json.dumps({k:v for k,v in row.items() if k!='examples'},default=str),flush=True)
    for j in sorted(range(len(pts)),key=lambda i:(sum(pts[i][0]),pts[i][0])):e.add_point(j)
    save(out/'configuration.json',n=64,table_bits=N,block_lengths=lengths,bottoms=args.S,
         parameters=args.S*66+65,initial_examples=len(pts),seed=args.seed,call_timeout=args.timeout,
         outer_budget=args.budget,logic='QF_LRA',weights='unrestricted reals',
         valid_symmetries=('Gate complement/permutation; raw-address flip with induced table permutation; within-block permutation' if args.input_symmetry else 'Only gate complement/permutation, no symmetry restrictions on raw weights'),
         domain='Every independent raw table/address bit; learner starts on a valid subset')
    save(out/'initial_examples.json',examples=pts)
    event(phase='initialized',bottoms=args.S,table_bits=N,block_lengths=lengths,examples_count=len(pts))
    result='BUDGET_EXHAUSTED';rounds=0;solver_seconds=0
    while time.monotonic()-start<args.budget:
        rounds+=1;remaining=args.budget-(time.monotonic()-start)
        e.so.set(timeout=max(1,int(min(remaining,args.timeout)*1000)))
        t0=time.monotonic();answer=e.so.check();dt=time.monotonic()-t0;solver_seconds+=dt
        event(phase='learner',round=rounds,status=str(answer).upper(),seconds=dt,examples_count=len(pts))
        if answer==z3.unsat:
            result='UNSAT_UNRESTRICTED_N64'
            (out/'unsat_instance.smt2').write_text(e.so.to_smt2())
            break
        if answer==z3.unknown:
            result='UNKNOWN';event(phase='reason',reason=e.so.reason_unknown());break
        c=e.circuit(e.so.model());assert not eval_circuit(c,pts)
        save(out/'latest.json',status='UNPROVED_CANDIDATE',candidate=c)
        remaining=args.budget-(time.monotonic()-start)
        if remaining<=0:break
        checked=checker(c,lengths,min(30,remaining));solver_seconds+=checked['seconds']
        event(phase='checker',round=rounds,**checked)
        if checked['status']=='VERIFIED':
            result='SAT_FULL_INPUT_DOMAIN';save(out/'verified.json',candidate=c);break
        if checked['status']=='UNKNOWN':result='CHECKER_UNKNOWN';break
        for p,y in checked['examples']:
            p=tuple(p);assert p not in seen;seen.add(p);pts.append((p,y));e.add_point(len(pts)-1)
    save(out/'examples.json',examples=pts)
    summary=dict(n=64,table_bits=N,block_lengths=lengths,bottoms=args.S,result=result,
                 rounds=rounds,examples=len(pts),solver_seconds=solver_seconds,wall_seconds=time.monotonic()-start)
    if result=='UNSAT_UNRESTRICTED_N64':summary['consequence']=f'At least {args.S+1} bottoms and {args.S+2} total gates.'
    save(out/'summary.json',**summary);event(phase='finished',**summary)

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--blocks',default='7,7,6,6,6');p.add_argument('--S',type=int,default=4)
    p.add_argument('--timeout',type=int,default=300);p.add_argument('--budget',type=int,default=600)
    p.add_argument('--seed',type=int,default=7);p.add_argument('--out',required=True);p.add_argument('--certificate',action='store_true')
    p.add_argument('--input-symmetry',action='store_true',help='WLOG for the full target: nonnegative, block-sorted direct address weights')
    run(p.parse_args())
