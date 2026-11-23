#!/usr/bin/env python3
# Copyright (c) 2026 Christian Reitwiessner
# Authors: Christian Reitwiessner
"""Generic LUT-generator CEGIS; exact real learner, exact symbolic checkers."""
import sys, json, time, random, argparse, os
from pathlib import Path
from fractions import Fraction as F
sys.path.insert(0,'/tmp/pydeps')
import z3
import smt_symbolic_check as independent
from mscore import Enc, eval_circuit
from constructions import diagonal, build3
AUTH='Christian Reitwiessner'
def save(path,obj):
 Path(path).write_text(json.dumps(dict(Authors=AUTH,**obj),default=str,indent=2)+'\n')
def mux(sel,values):
 return z3.Or([z3.And(sel==j,v) for j,v in enumerate(values)])
def generator(k,r):
 """r slots, each arbitrary binary LUT. Predecessors: constants, k inputs, earlier slots.
 Output selects any source. Thus exactly the family of circuits with <=r LUTs."""
 ps=[(z3.Int('p%d'%j),z3.Int('q%d'%j)) for j in range(r)]
 luts=[[z3.Bool('l%d_%d'%(j,t)) for t in range(4)] for j in range(r)]
 out=z3.Int('out'); valid=[out>=0,out<k+2+r]
 for j,(p,q) in enumerate(ps):valid += [p>=0,p<k+2+j,q>=0,q<k+2+j]
 def evaluate(inputs):
  vals=[z3.BoolVal(False),z3.BoolVal(True)]+list(inputs)
  for (p,q),lut in zip(ps,luts):
   a,b=mux(p,vals),mux(q,vals)
   vals.append(z3.Or([z3.And(a if t&1 else z3.Not(a),b if t&2 else z3.Not(b),lut[t]) for t in range(4)]))
  return mux(out,vals)
 tables=[evaluate([z3.BoolVal(bool(c>>i&1)) for i in range(k)]) for c in range(1<<k)]
 def decode(m):
  return dict(gates=[dict(p=m.eval(p).as_long(),q=m.eval(q).as_long(),lut=[int(z3.is_true(m.eval(t,model_completion=True))) for t in lut]) for (p,q),lut in zip(ps,luts)],output=m.eval(out).as_long())
 return valid,tables,evaluate,decode

def check(c,k,m,r,timeout=10000,batch=12):
 if r == -1:
  valid=[];x=[z3.Bool('table%d'%i) for i in range(1<<k)];decode=lambda model:None
  def evaluate(address):
   vals=x[:]
   for b in address:vals=[z3.If(b,vals[j+1],vals[j]) for j in range(0,len(vals),2)]
   return vals[0]
 else:valid,x,evaluate,decode=generator(k,r)
 a=[z3.Bool('a%d'%i) for i in range(k*m)]
 bits=x+a; gates=[independent.threshold(bits,w,t) for w,t in c['bottom']]
 pred=independent.threshold(gates+bits,c['v']+c['u'],c['tau'])
 target=evaluate([independent.parity(a[i*m:(i+1)*m]) for i in range(k)])
 so=z3.Solver();so.set(timeout=timeout);so.add(*valid,z3.Xor(pred,target)); examples=[];t0=time.monotonic()
 for _ in range(batch):
  res=so.check()
  if res!=z3.sat:
   return dict(status=str(res).upper(),reason=so.reason_unknown() if res==z3.unknown else '',examples=examples,seconds=time.monotonic()-t0)
  model=so.model();p=tuple(int(z3.is_true(model.eval(b,model_completion=True))) for b in bits)
  y=int(z3.is_true(model.eval(target,model_completion=True)))
  examples.append(dict(point=p,target=y,description=decode(model)))
  so.add(z3.Or([b!=bool(v) for b,v in zip(bits,p)]))
 return dict(status='SAT',examples=examples,seconds=time.monotonic()-t0)

def concrete(d,k):
 tab=[]
 for c in range(1<<k):
  v=([0] if d.get('basis')=='complemented_AND_XOR' else [0,1])+[(c>>i)&1 for i in range(k)]
  for g in d['gates']:
   if d.get('basis')=='complemented_AND_XOR':
    p,q=g['p'],g['q'];aa=v[p//2]^(p%2);bb=v[q//2]^(q%2);v.append((aa^bb) if g['xor'] else (aa&bb))
   else:v.append(g['lut'][v[g['p']]+2*v[g['q']]])
  out=d['output'];tab.append(v[out//2]^(out%2) if d.get('basis')=='complemented_AND_XOR' else v[out])
 return tuple(tab)
def target(p,k,m):
 n=1<<k;return p[sum((sum(p[n+i*m:n+(i+1)*m])%2)<<i for i in range(k))]

def library(k,m):
 if k==4:
  # Exact two-junta Fourier library. Valid on r<=1; not full-table guarantee.
  N=1<<k;unit=N//4;L=N+1;bottom=[];v=[];u=[2]*N+[0]*(k*m);constant=0
  for s in range(1,N):
   if s.bit_count()>2:continue
   al=[(-1)**((s&c).bit_count()%2) for c in range(N)]
   for r in [-N//2+1,-N//4+1,1,N//4+1]:
    for j in range(s.bit_count()*m//2+1):
     bottom.append((al+[L*int(bool(s>>i&1)) for i in range(k) for _ in range(m)],2*L*j+r));v.append(4*unit)
    bottom.append((al+[0]*(k*m),r));v.append(-2*unit)
    constant-=unit
    for i in range(k):
     for z in range(m):u[N+i*m+z]-=2*unit*int(bool(s>>i&1))
  return dict(bottom=bottom,v=v,u=u,tau=N-constant)
 gs,u,nu,c0=(diagonal(m) if k==2 else build3(m))
 return dict(bottom=[(al+[nu[i] for i in range(k) for _ in range(m)],t) for al,nu,t,v in gs],v=[v for al,nu,t,v in gs],u=u+[nu[i] for i in range(k) for _ in range(m)],tau=-c0)

def run(k,m,r,S,mode,directory,budget=120,timeout=8000,seed=1):
 dest=Path(directory);dest.mkdir(parents=True,exist_ok=True)
 log=open(dest/'events.jsonl','a');start=time.monotonic()
 def event(**o):
  o.update(elapsed=round(time.monotonic()-start,3));log.write(json.dumps(o,default=str)+'\n');log.flush();print(json.dumps(o,default=str),flush=True)
 n=(1<<k)+k*m;pts=[];seen=set();rng=random.Random(seed)
 # Initial samples are generated from VALID generic descriptions, not arbitrary tables.
 for j in range(32):
  d=dict(gates=[dict(p=rng.randrange(k+2+i),q=rng.randrange(k+2+i),lut=[rng.randrange(2) for _ in range(4)]) for i in range(r)],output=rng.randrange(k+2+r))
  tab=tuple(rng.randrange(2) for _ in range(1<<k)) if r==-1 else concrete(d,k);p=tab+tuple(rng.randrange(2) for _ in range(k*m))
  if p not in seen:seen.add(p);pts.append((p,target(p,k,m)))
 if os.environ.get('WARM'):
  for pp,yy in json.loads(Path(os.environ['WARM']).read_text())['examples']:
   pp=tuple(pp)
   if pp not in seen:seen.add(pp);pts.append((pp,yy))
 fixed=library(k,m) if mode=='pool' else None
 e=Enc(pts,S,dict(cls='free',vsym=False,seed=seed)) if not fixed else None
 if e:
  for i in range(len(pts)):e.add_point(i)
 else:
  S=len(fixed['bottom']);so=z3.SolverFor('QF_LRA');v=[z3.Real('v%d'%j) for j in range(S)];u=[z3.Real('u%d'%i) for i in range(n)];tau=z3.Real('tau')
  def add(p,y):
   g=[int(sum(F(wi)*pi for wi,pi in zip(w,p))>=F(t)) for w,t in fixed['bottom']]
   score=z3.Sum([v[j] for j in range(S) if g[j]]+[u[i] for i in range(n) if p[i]])
   so.add(score>=tau if y else score<=tau-1)
  for p,y in pts:add(p,y)
 removed=[];banned=set();best=None;rounds=0;pending=None
 while time.monotonic()-start<budget:
  solver=e.so if e else so;solver.set(timeout=min(timeout,max(1,int(1000*(budget-time.monotonic()+start)))))
  t=time.monotonic();res=solver.check();rounds+=1
  event(phase='learner',round=rounds,status=str(res).upper(),examples=len(pts),seconds=time.monotonic()-t,removed=removed)
  if res!=z3.sat:
   if pending is not None:
    so.pop();removed.remove(pending);banned.add(pending);pending=None
    for pp,yy in pts:add(pp,yy)
    if res==z3.unknown:break
    continue
   break
  if e:c=e.circuit(solver.model())
  else:
   model=so.model();q=lambda t:str(model.eval(t,model_completion=True))
   inds=[j for j in range(S) if F(q(v[j]))]
   c=dict(bottom=[fixed['bottom'][j] for j in inds],v=[q(v[j]) for j in inds],u=[q(w) for w in u],tau=q(tau))
  assert not eval_circuit(c,pts)
  save(dest/'latest.json',dict(k=k,m=m,r=r,mode=mode,candidate=c))
  result=check(c,k,m,r,timeout=timeout);event(phase='family_checker',round=rounds,**result)
  for ex in result['examples']:
   p=tuple(ex['point']);assert ex['description'] is None or tuple(p[:1<<k])==concrete(ex['description'],k);assert ex['target']==target(p,k,m)
   assert p not in seen;seen.add(p);pts.append((p,ex['target']))
   if e:e.add_point(len(pts)-1)
   else:add(p,ex['target'])
  save(dest/'examples.json',dict(examples=pts))
  if result['status']=='UNSAT' and not result['examples']:
   full=independent.check(c,independent.andreev_target(k,m),timeout_ms=max(30000,timeout))
   event(phase='independent_checker',bottoms=len(c['bottom']),**full)
   name='verified_%d.json'%len(c['bottom']);save(dest/name,dict(k=k,m=m,r=r,mode=mode,candidate=c,family=result,ordinary=full))
   best=len(c['bottom']);pending=None
   if e:break
   # Greedy elimination, exact unrestricted top fitting on fixed bottom library.
   active=[j for j in range(S) if j not in removed and j not in banned]
   if not active:break
   pending=min(active,key=lambda j:abs(F(q(v[j]))));removed.append(pending);so.push();so.add(v[pending]==0)
  elif result['status']=='UNKNOWN':break
 event(phase='finished',best=best,rounds=rounds,mode=mode,k=k,m=m,r=r,S=S)
 log.close()
 return best
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--encoding',choices=['lut','xag','xag_canonical'],default='lut');p.add_argument('--k',type=int,required=True);p.add_argument('--m',type=int,required=True);p.add_argument('--r',type=int,required=True);p.add_argument('--S',type=int,default=6);p.add_argument('--mode',choices=['free','pool'],default='free');p.add_argument('--budget',type=int,default=120);p.add_argument('--timeout',type=int,default=8000);p.add_argument('--seed',type=int,default=1);p.add_argument('--out',required=True);a=p.parse_args()
 if a.encoding!='lut':
  from xag_encoding import generator as xag_generator,canonical_generator
  generator=canonical_generator if a.encoding=='xag_canonical' else xag_generator
 run(a.k,a.m,a.r,a.S,a.mode,a.out,a.budget,a.timeout,a.seed)
