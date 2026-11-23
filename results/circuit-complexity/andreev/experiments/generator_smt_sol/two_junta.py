#!/usr/bin/env python3
# Copyright (c) 2026 Christian Reitwiessner
# Authors: Christian Reitwiessner
"""Exact all-k one-LUT-family construction by sign-only Walsh inversion."""
from pathlib import Path
import engine as e
from audit import tables,exhaustive

def build(k,m):
 N=1<<k;L=N+1;bottom=[];v=[];u=[4]*N+[0]*(k*m);constant=-2*N
 for s in range(1,N):
  if s.bit_count()>2:continue
  al=[(-1)**((s&c).bit_count()%2) for c in range(N)]
  for r in [0,1]:
   for j in range(s.bit_count()*m//2+1):
    bottom.append((al+[L*int(bool(s>>i&1)) for i in range(k) for _ in range(m)],2*L*j+r));v.append(2*N)
   bottom.append((al+[0]*(k*m),r));v.append(-N)
   constant-=N//2
   for i in range(k):
    for j in range(m):u[N+i*m+j]-=N*int(bool(s>>i&1))
 return dict(bottom=bottom,v=v,u=u,tau=1-constant)

if __name__=='__main__':
 root=Path(__file__).resolve().parent;records=[]
 # Core sign reconstruction certificate; higher-k two-juntas are embeddings.
 for tab in range(16):
  x=[tab>>c&1 for c in range(4)]
  for b in range(4):
   score=sum(x)-2
   for s in range(1,4):
    h=sum((-1)**((s&c).bit_count()%2)*x[c] for c in range(4))
    score+=(int(h>0)-int(h<0))*(-1)**((s&b).bit_count()%2)
   assert (2*x[b]-1)*score>=1
 for k,m in [(2,6),(3,3),(3,6),(4,2),(4,3),(5,2)]:
  c=build(k,m);family=exhaustive(c,k,m,tables(k,1));assert family['status']=='VERIFIED'
  symbolic=e.check(c,k,m,1,timeout=10000,batch=1);ordinary=e.independent.check(c,e.independent.andreev_target(k,m),timeout_ms=3000)
  rec=dict(k=k,m=m,r=1,bottoms=len(c['bottom']),family_exact=family,family_symbolic=symbolic,ordinary=ordinary)
  e.save(root/('twojunta_k%dm%d.json'%(k,m)),dict(**rec,candidate=c));records.append(rec);print(rec,flush=True)
 e.save(root/'twojunta_results.json',dict(results=records,core_cases=64))
