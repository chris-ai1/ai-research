# Copyright (c) 2026 Christian Reitwiessner
# Authors: Christian Reitwiessner
"""Time-bounded full mixed-sign exact-sum search; rational SAT recheck."""
import sys,itertools,json
sys.path.insert(0,'/tmp/pydeps')
import z3
from fractions import Fraction

def run(k,m,S,ms=15000):
 N=1<<k;n=N+k*m; so=z3.Solver();so.set(timeout=ms)
 W=[[z3.Real(f'w{j}_{i}') if i<N else z3.Int(f'w{j}_{i}') for i in range(n)] for j in range(S)]
 T=[z3.Real(f't{j}') for j in range(S)];V=[z3.Real(f'v{j}') for j in range(S)]
 U=[z3.Real(f'u{i}') for i in range(n)];K=z3.Real('bias')
 for row in W:
  for w in row[N:]:so.add(w>=-1,w<=1)
 for v in V:so.add(v>=0)
 for j in range(S-1):so.add(V[j]<=V[j+1])
 rows=[]
 for z in itertools.product([0,1],repeat=n):
  b=sum((sum(z[N+i*m:N+(i+1)*m])%2)<<i for i in range(k));y=z[b]
  gates=[z3.Sum([w*zz for w,zz in zip(row,z)])>=t for row,t in zip(W,T)]
  so.add(K+z3.Sum([u*zz for u,zz in zip(U,z)])+z3.Sum([z3.If(g,v,0) for g,v in zip(gates,V)])==y)
  rows.append((z,y))
 ans=so.check();out=dict(k=k,m=m,S=S,address_weight_bound=1,status=str(ans))
 if ans==z3.sat:
  model=so.model()
  def val(q):
   r=model.eval(q,model_completion=True);return Fraction(r.numerator_as_long(),r.denominator_as_long()) if z3.is_rational_value(r) else Fraction(r.as_long())
  ww=[[val(w) for w in row] for row in W];tt=list(map(val,T));vv=list(map(val,V));uu=list(map(val,U));kk=val(K)
  for z,y in rows:
   assert kk+sum(u*zz for u,zz in zip(uu,z))+sum(v for row,t,v in zip(ww,tt,vv) if sum(w*zz for w,zz in zip(row,z))>=t)==y
  out.update(W=ww,T=tt,V=vv,U=uu,bias=kk,verified_rows=len(rows))
 return out
if __name__=='__main__':
 print(json.dumps([run(1,3,3),run(2,1,3)],default=str,indent=2))
