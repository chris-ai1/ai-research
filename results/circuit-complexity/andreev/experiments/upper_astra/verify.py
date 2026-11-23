# Copyright (c) 2026 Christian Reitwiessner.
# Authors: Christian Reitwiessner
print("# Authors: Christian Reitwiessner", flush=True)
import json,itertools,collections
root='/tmp/andreev_gap/upper_astra/'
def chi(s,c):return (-1)**((s&c).bit_count()%2)
def walsh(x): return [sum(chi(s,c)*(2*v-1) for c,v in enumerate(x)) for s in range(len(x))]
def q(v,r):return int(v>=r)-int(v<=-r)
# Translation sends a tested address b to zero and permutes tables. Thus
# all 65536 tables at b=0 certify all 1048576 table/address pairs.
margin=10**9; histogram=collections.Counter()
for bits in range(65536):
 x=[(bits>>c)&1 for c in range(16)]; X=walsh(x)
 F=4*X[0]+sum(11*q(v,2)+32*q(v,4) for v in X[1:])
 v=(2*x[0]-1)*F; margin=min(margin,v);histogram[v]+=1
assert margin==43
bad=[int(c in [0,1,2,4,8]) for c in range(16)]; X=walsh(bad)
R=[sum(q(X[s],2)*chi(s,b) for s in range(1,16)) for b in range(16)]
assert R[0]==R[15]==5 and bad[0]!=bad[15]
print('k4 exact certificate margin',margin,'tables at translated address zero',65536,flush=True)
print('sign-only collision',R,flush=True)
# Exact full-domain integer verification of genuinely mixed truncated ridges.
k=3;m=3;N=8;radii=[2,4,6,8,10,13]
stats={r:{'errors':0,'central_inputs':0,'central_errors':0} for r in radii}
def phi(v):return (-1 if v%2 else 1)*v
def psi(v,r):return phi(max(-r,min(r,v)))
views={}
for s in range(1,N):
 active=[i*m+j for i in range(k) if (s>>i)&1 for j in range(m)]
 z={i*m+(s+i)%m for i in range(k) if (s>>i)&1}
 M=len(active); e=2*((M+2)//4)
 views[s]=(active,z,e)
for bits in range(256):
 x=[(bits>>c)&1 for c in range(N)];X=walsh(x)
 for raw in range(512):
  a=[(raw>>j)&1 for j in range(9)]
  b=sum((sum(a[i*m:(i+1)*m])%2)<<i for i in range(k))
  forms=[]
  for s,(active,z,e) in views.items():
   L=sum(a[j]^(j in z) for j in active);d=L-e
   forms.append((X[s]+d,X[s]-d,(-1)**(len(z)+e)))
  assert 2*X[0]+sum(sign*(phi(u)+phi(v)) for u,v,sign in forms)==2*N*(2*x[b]-1)
  for r in radii:
   P=2*X[0]+sum(sign*(psi(u,r)+psi(v,r)) for u,v,sign in forms)
   wrong=int((P>=0)!=bool(x[b]));central=all(max(abs(u),abs(v))<=r for u,v,_ in forms)
   stats[r]['errors']+=wrong;stats[r]['central_inputs']+=int(central);stats[r]['central_errors']+=int(central)*wrong
for st in stats.values():assert st['central_errors']==0
assert stats[13]['errors']==0
out={'authors':'Christian Reitwiessner','k4_margin':margin,'k4_histogram':dict(histogram),'sign_collision':R,'truncation_k3m3':stats,'inputs':131072}
with open(root+'verification.json','w') as f:json.dump(out,f,indent=2)
print(json.dumps(stats,indent=2),flush=True)
