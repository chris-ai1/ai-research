# Copyright (c) 2026 Christian Reitwiessner
# Authors: Christian Reitwiessner
"""Exact recovered diagonal gadget and new slope-21/2 Fourier circuit."""
from itertools import product
from math import comb
import json
ROOT='/tmp/andreev_gap/mixed_upper_sol/'
def character(s,c): return (-1)**((s&c).bit_count()%2)
def atoms3():
 return [(s,r,15 if s.bit_count()!=2 else 18) for s in range(1,8) for r in ([0] if s==7 else [0,1])]
def score3(x,b):
 h={s:sum(character(s,c)*x[c] for c in range(8)) for s in range(1,8)}
 return sum((6 if c in (0,7) else 8)*x[c] for c in range(8))-30+sum(w*character(s,b)*(2*int(h[s]>=r)-1) for s,r,w in atoms3())
def build3(m):
 gates=[];mu=[6 if c in(0,7) else 8 for c in range(8)];nu=[0]*3;constant=-30
 for s,r,w in atoms3():
  al=[character(s,c) for c in range(8)]; be=[6*int((s>>i)&1) for i in range(3)]
  for j in range(s.bit_count()*m//2+1):gates.append((al,be,12*j+r,4*w))
  gates.append((al,[0]*3,r,-2*w))
  constant-=w
  for i in range(3):nu[i]-=2*w*((s>>i)&1)
 return gates,mu,nu,constant

def diagonal(m):
 # Modular diagonals containing odd--odd points; discard boundary-only ones.
 odd=range(1,m+1,2)
 ds=sorted({u-v for u in odd for v in odd if (u-v)%4==0})
 ss=sorted({u+v for u in odd for v in odd if (u+v)%4==0})
 gates=[]
 for j in range(1,(m+1)//2+1):
  for c,be,w in [(1,[0,1],-12),(0,[0,1],-16),(1,[1,0],8)]:
   al=[int(i==c) for i in range(4)];gates.append((al,be,2*j,w))
 for be,levels in [([1,-1],ds),([1,1],ss)]:
  for v in levels:
   for c,w in [(3,6),(1,-6)]:gates.append(([int(i==c) for i in range(4)],be,v+1,w))
 return gates,[16,12,2,0],[-4,14],-15

def check(m,k,builder,closed=None):
 gates,mu,nu,c0=builder(m); margin=10**20;points=0
 for x in product((0,1),repeat=1<<k):
  hs=[sum(a*b for a,b in zip(al,x)) for al,be,th,w in gates]
  base=sum(a*b for a,b in zip(mu,x))+c0
  for s in product(range(m+1),repeat=k):
   b=sum((v%2)<<i for i,v in enumerate(s))
   val=base+sum(a*b for a,b in zip(nu,s))+sum(w for h,(al,be,th,w) in zip(hs,gates) if h+sum(a*b for a,b in zip(be,s))>=th)
   if closed:assert val==closed(x,b),(m,x,s,val,closed(x,b))
   margin=min(margin,val*(2*x[b]-1));points+=1
 assert margin>=1,(m,margin)
 return dict(m=m,k=k,bottoms=len(gates),total=len(gates)+1,margin=margin,count_points=points)
if __name__=='__main__':
 # Full 256-table / eight-address certificate, independent of m.
 margins=[score3(x,b)*(2*x[b]-1) for x in product((0,1),repeat=8) for b in range(8)]
 assert min(margins)==15
 print('Fourier full-domain coefficient certificate:',len(margins),'cases; minimum',min(margins),flush=True)
 for m in [1,2,3,4,7,10]:
  r=check(m,3,build3,score3);assert r['bottoms']==6*(m//2)+6*m+3*m//2+26;print(r,flush=True)
 for m in range(1,17):print('diagonal',check(m,2,diagonal),flush=True)
 for m,k,builder in [(3,2,diagonal),(4,2,diagonal),(10,3,build3)]:
  gates,mu,nu,c=builder(m)
  with open(ROOT+'explicit_%d_%d.json'%(k,m),'w') as f:json.dump(dict(Authors='Christian Reitwiessner',copyright='Copyright (c) 2026 Christian Reitwiessner',k=k,m=m,gates=gates,mu=mu,nu=nu,constant=c),f,indent=2)
