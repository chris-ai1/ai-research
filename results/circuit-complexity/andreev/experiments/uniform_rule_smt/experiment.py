#!/usr/bin/env python3
# Copyright (c) 2026 Christian Reitwiessner.
# Authors: Christian Reitwiessner
"""Exact multi-size affine-rule CEGIS; all checkers use independent raw bits."""
import argparse
from collections import Counter
from fractions import Fraction as Q
from itertools import product
import json
from pathlib import Path
import random
import sys
import time

sys.path.insert(0, '/tmp/pydeps')
import z3
from rules import Circuit, Gate, globally_reorientable, rank_m2_program, smt_miter, target

AUTHOR = 'Christian Reitwiessner'
SIZES = [(2, 2), (3, 3), (4, 3), (4, 4)]

def save(path, obj):
    path.write_text(json.dumps(obj, indent=2) + '\n')

def parity(x):
    return -1 if x.bit_count() % 2 else 1

def rat(v):
    v = Q(v)
    return z3.RealVal(f'{v.numerator}/{v.denominator}')

class Template:
    """Fixed, public feature programs; only named numerical holes are learned."""
    def __init__(self, kind, types=1, width=2):
        self.kind, self.types, self.width = kind, types, width
        if kind == 'calibration':
            self.names = ['v', 'direct', 'cutoff']
        else:
            self.names = [f'{f}{h}_{q}' for h in range(types)
                          for f in ('a', 'w', 't', 'v') for q in range(width)]
            self.names += [f'{f}_{q}' for f in ('d', 'e', 'cutoff') for q in range(width)]
        self.cache = {}

    def size(self, k, m):
        if (k, m) not in self.cache:
            self.cache[k, m] = self.build(k, m)
        return self.cache[k, m]

    def build(self, k, m):
        N = 1 << k
        if self.kind == 'calibration':
            fixture = rank_m2_program().compile(k, m)
            gates = [(tuple((w, {}) for w in g.weights), (g.threshold, {}), (0, {'v': 1}))
                     for g in fixture.gates]
            direct = [(0, {}) for _ in range(N)]
            direct += [(0, {'direct': (1 << i) if t == 0 else 0})
                       for i in range(k) for t in range(m)]
            return gates, direct, (0, {'cutoff': 1})
        q = self.width
        gates = []
        def field(f, features):
            return 0, {f'{f}_{j}': v for j, v in enumerate(features[:q]) if v}
        for h in range(self.types):
            for u in range(N):
                for r in range(m):
                    weights = [field(f'a{h}', [int(c == u), parity(u & c),
                                              parity((u ^ 1) & c) + int(c == (u ^ 1))])
                               for c in range(N)]
                    for i in range(k):
                        for t in range(m):
                            if self.kind == 'positional':
                                f0 = (1 << i) * parity((u ^ (r+1)*(i+1) ^ h) & t)
                                f1 = 3**i * parity((u + (h+1)*(r+1) + i) & (t ^ (t >> 1)))
                                f2 = (1 << t) * parity((u ^ (i+1)*(h+1)) & (t+r))
                            else:
                                f0 = (1 << i) * (1 if t == 0 else 2*((u >> i)&1)-1)
                                f1 = 3**i * parity((u ^ (r+1)*(i+1) ^ (h+1)) & t)
                                f2 = (1 << i) * int(t == r) * (2*((u >> i)&1)-1)
                            weights.append(field(f'w{h}', [f0, f1, f2]))
                    gates.append((tuple(weights), field(f't{h}', [u+1, N*(r+1), 1]),
                                  field(f'v{h}', [1, (-1)**r, parity(u)])))
        direct = [field('d', [1, parity(c & 1), c+1]) for c in range(N)]
        direct += [field('e', [m*(1 << i)*int(t == 0), (-1)**t,
                              (i+1)*int(t == m-1)]) for i in range(k) for t in range(m)]
        return gates, direct, field('cutoff', [m, 1, N])

    def compile(self, k, m, theta):
        def value(aff):
            base, terms = aff
            return Q(base) + sum((theta[p]*v for p,v in terms.items()), Q(0))
        gates, direct, threshold = self.size(k, m)
        return Circuit(k, m, tuple(Gate(tuple(map(value, ws)), value(t)) for ws,t,v in gates),
                       tuple(value(v) for ws,t,v in gates), tuple(map(value, direct)), value(threshold))

class FrozenBottomTemplate(Template):
    """Diagnostic restriction: keep the candidate's bottom rules fixed exactly."""
    def __init__(self, source, theta):
        self.source = source
        self.fixed = {p:theta[p] for p in source.names if p[0] in ('a','w','t')}
        self.names = [p for p in source.names if p not in self.fixed]
        self.cache = {}

    def build(self, k, m):
        gates,direct,threshold=self.source.size(k,m)
        def specialize(aff):
            base,terms=aff
            return (Q(base)+sum((self.fixed[p]*v for p,v in terms.items() if p in self.fixed),Q(0)),
                    {p:v for p,v in terms.items() if p not in self.fixed})
        return [(tuple(map(specialize,ws)),specialize(t),specialize(v)) for ws,t,v in gates],list(map(specialize,direct)),specialize(threshold)

def samples(k, m, count, seed, xor_corners=True):
    N = 1 << k
    rng = random.Random(seed + k*100 + m)
    tables = [(0,)*N, (1,)*N]
    tables += [tuple(int(c == u) for c in range(N)) for u in range(N)]
    tables += [tuple(int((c & u).bit_count()%2) for c in range(N)) for u in range(1,N)]
    # These are samples only: the checker will universally range over all tables.
    points = set()
    for j in range(count):
        x = tables[j % len(tables)] if j < count*3//4 else tuple(rng.randrange(2) for _ in range(N))
        a = tuple(rng.randrange(2) for _ in range(k*m))
        points.add(tuple(x)+a)
    # Exclude spurious raw-affine-only fits from tiny curricula: each fixed
    # XOR table has four raw-address corners that no single top LTF separates.
    if xor_corners and k >= 2:
        for complement in (0,1):
            x=tuple(((c & 3).bit_count()%2)^complement for c in range(N))
            for b0,b1 in product((0,1),repeat=2):
                a=[0]*(k*m);a[0]=b0;a[m]=b1
                points.add(x+tuple(a))
    return sorted(points)

def linear(aff, variables):
    base, terms = aff
    return rat(base) + z3.Sum([v*variables[p] for p,v in terms.items() if v])

class Learner:
    def __init__(self, template, timeout, seed):
        self.template = template
        self.theta = {p:z3.Real(p) for p in template.names}
        self.solver = z3.SolverFor('QF_LRA')
        self.solver.set(timeout=timeout, random_seed=seed)
        self.points = set()
        self.activations = 0

    def add(self, k, m, point):
        key = k,m,tuple(point)
        if key in self.points:
            return False
        self.points.add(key)
        gates, direct, threshold = self.template.size(k,m)
        terms = []
        for j,(weights,cutoff,top) in enumerate(gates):
            const = -cutoff[0]
            coeff = Counter({p:-v for p,v in cutoff[1].items()})
            for bit,(base,cs) in zip(point,weights):
                if bit:
                    const += base
                    for p,v in cs.items(): coeff[p] += v
            expr = linear((const,dict(coeff)),self.theta)
            if not any(coeff.values()):
                if const >= 0: terms.append(linear(top,self.theta))
            else:
                active = z3.Bool(f'g_{len(self.points)}_{j}')
                self.solver.add(active == (expr >= 0))
                terms.append(z3.If(active,linear(top,self.theta),0))
                self.activations += 1
        total = z3.Sum(terms) + z3.Sum([linear(d,self.theta) for bit,d in zip(point,direct) if bit])
        total -= linear(threshold,self.theta)
        # Exact tie semantics; no independently imposed unit margins or weight bounds.
        self.solver.add(total >= 0 if target(k,m,point) else total < 0)
        return True

    def model(self):
        model = self.solver.model()
        return {p:Q(str(model.eval(v,model_completion=True))) for p,v in self.theta.items()}

def check(circuit, timeout, batch=4):
    s = z3.Solver()
    s.set(timeout=max(1,timeout))
    s.from_string(smt_miter(circuit))
    points = []
    start = time.monotonic()
    for _ in range(batch):
        remaining = timeout-int((time.monotonic()-start)*1000)
        if remaining <= 0:
            return dict(status='COUNTEREXAMPLES' if points else 'UNKNOWN',points=points,reason='checker budget',seconds=time.monotonic()-start)
        s.set(timeout=remaining)
        answer = s.check()
        if answer == z3.unsat:
            return dict(status='COUNTEREXAMPLES' if points else 'VERIFIED',points=points,seconds=time.monotonic()-start)
        if answer == z3.unknown:
            return dict(status='COUNTEREXAMPLES' if points else 'UNKNOWN',points=points,reason=s.reason_unknown(),seconds=time.monotonic()-start)
        model = s.model()
        n = (1 << circuit.k)+circuit.k*circuit.m
        zs = [z3.Bool(f'z{j}') for j in range(n)]
        point = tuple(int(z3.is_true(model.eval(z,model_completion=True))) for z in zs)
        assert circuit.value(point) != target(circuit.k,circuit.m,point)
        points.append(list(point))
        s.add(z3.Or([z != bool(v) for z,v in zip(zs,point)]))
    return dict(status='COUNTEREXAMPLES',points=points,seconds=time.monotonic()-start)

def run(args):
    out = Path(args.out); out.mkdir(parents=True,exist_ok=True)
    if (out/'events.jsonl').exists():
        raise SystemExit('Use a fresh output directory; existing research logs are preserved.')
    template = Template(args.kind,args.types,args.width)
    if args.freeze_bottom:
        theta={p:Q(v) for p,v in json.loads(Path(args.freeze_bottom).read_text())['theta'].items()}
        template=FrozenBottomTemplate(template,theta)
    sizes = [(1,2),(2,2)] if args.kind == 'calibration' else SIZES
    if args.only32: sizes = [(4,4)]
    start = time.monotonic()
    events = []
    def event(**d):
        d['elapsed'] = round(time.monotonic()-start,4)
        events.append(d)
        with (out/'events.jsonl').open('a') as f: f.write(json.dumps(d)+'\n')
        print(json.dumps({k:v for k,v in d.items() if k not in ('points','theta')}),flush=True)
    learner = Learner(template,args.timeout*1000,args.seed)
    for k,m in sizes:
        pts = list(product((0,1),repeat=(1<<k)+k*m)) if args.kind=='calibration' else samples(k,m,args.examples,args.seed,xor_corners=not args.legacy_samples)
        for point in pts: learner.add(k,m,point)
    save(out/'configuration.json',dict(Authors=AUTHOR,kind=args.kind,types=args.types,width=args.width,
         parameters=template.names,sizes=sizes,bottoms=[len(template.size(k,m)[0]) for k,m in sizes],
         seed=args.seed,call_timeout_seconds=args.timeout,outer_budget_seconds=args.budget,
         requested_examples_per_size=args.examples,
         frozen_bottom_source=args.freeze_bottom,
         sample_policy='legacy' if args.legacy_samples else 'xor_corners',
         initial_points=len(learner.points),initial_activation_booleans=learner.activations,
         solver_version=z3.get_version_string(),gate_count_rule='N for calibration; types*N*m otherwise',
         semantics='arbitrary real shared coefficients, exact >= ties, no unit margins, no weight bounds'))
    event(phase='initialized',parameters=len(template.names),examples=len(learner.points),activation_booleans=learner.activations)
    result='BUDGET_EXHAUSTED';round_no=0;solver_seconds=0
    while time.monotonic()-start < args.budget:
        round_no += 1
        learner.solver.set(timeout=max(1,int(min(args.timeout,args.budget-(time.monotonic()-start))*1000)))
        t0=time.monotonic();answer=learner.solver.check();seconds=time.monotonic()-t0;solver_seconds+=seconds
        event(phase='learner',round=round_no,status=str(answer).upper(),seconds=seconds,
              examples=len(learner.points),activation_booleans=learner.activations)
        if answer == z3.unsat:
            result='UNSAT_RESTRICTED_RULES_ON_SAMPLES';break
        if answer == z3.unknown:
            result='UNKNOWN';event(phase='reason',reason=learner.solver.reason_unknown());break
        theta=learner.model()
        # Independent exact evaluation of every learner constraint before verification.
        circuits={(k,m):template.compile(k,m,theta) for k,m in sizes}
        assert all(circuits[k,m].value(p)==target(k,m,p) for k,m,p in learner.points)
        save(out/'latest.json',dict(Authors=AUTHOR,status='UNPROVED_CANDIDATE',theta={p:str(v) for p,v in theta.items()}))
        added=0;unknown=False
        for (k,m),c in circuits.items():
            remaining=args.budget-(time.monotonic()-start)
            if remaining <= 0: unknown=True;break
            checked=check(c,int(min(args.check_timeout,remaining)*1000));solver_seconds+=checked['seconds']
            event(phase='checker',round=round_no,k=k,m=m,**checked)
            for p in checked['points']: added+=learner.add(k,m,p)
            unknown |= checked['status']=='UNKNOWN'
        if not added:
            if unknown: result='CHECKER_UNKNOWN';break
            result='VERIFIED_TRAINING_SIZES_ONLY'
            save(out/'verified_training.json',dict(Authors=AUTHOR,theta={p:str(v) for p,v in theta.items()},
                  stats=[dict(k=k,m=m,**c.stats(),globally_reorientable=globally_reorientable(c.gates,1<<k,k,m)) for (k,m),c in circuits.items()]))
            for k,m in ([(3,2)] if args.kind=='calibration' else [(2,3),(3,2),(3,4),(4,2)]):
                c=template.compile(k,m,theta)
                checked=check(c,args.check_timeout*1000)
                event(phase='holdout',k=k,m=m,**checked)
            break
    summary=dict(Authors=AUTHOR,result=result,kind=args.kind,types=args.types,width=args.width,
                 sizes=sizes,parameters=len(template.names),rounds=round_no,examples=len(learner.points),
                 activation_booleans=learner.activations,solver_seconds=solver_seconds,
                 wall_seconds=time.monotonic()-start,
                 status_scope='Finite training sizes in the declared rule family; not an all-size theorem')
    save(out/'examples.json',dict(Authors=AUTHOR,examples=[dict(k=k,m=m,point=list(p),target=target(k,m,p)) for k,m,p in sorted(learner.points)]))
    save(out/'summary.json',summary);event(phase='finished',**summary)

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--kind',choices=['calibration','positional','coupled'],required=True)
    p.add_argument('--types',type=int,default=1);p.add_argument('--width',type=int,choices=[2,3],default=2)
    p.add_argument('--timeout',type=int,default=60);p.add_argument('--check-timeout',type=int,default=15)
    p.add_argument('--budget',type=int,default=180);p.add_argument('--examples',type=int,default=48)
    p.add_argument('--seed',type=int,default=7);p.add_argument('--only32',action='store_true');p.add_argument('--out',required=True)
    p.add_argument('--freeze-bottom')
    p.add_argument('--legacy-samples',action='store_true',help='Reproduce the initial runs before XOR corner seeding')
    run(p.parse_args())
