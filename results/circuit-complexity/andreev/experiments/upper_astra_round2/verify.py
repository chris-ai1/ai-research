# Copyright (c) 2026 Christian Reitwiessner.
# Authors: Christian Reitwiessner
"""Independent exact integer audits of masks, cancellation, and actual raw gates."""
import sys,itertools,json,math,random
from fractions import Fraction
from pathlib import Path
sys.path.insert(0,'/tmp/pydeps')
import numpy as np
print('# Authors: Christian Reitwiessner',flush=True)
ROOT=Path('/tmp/andreev_gap/upper_astra_round2')
def parity(v):return (-1)**(v%2)
def phi(v):return np.where(v%2,-v,v)
def clipped(v,R):return np.where(np.abs(v)<=R,phi(v),0)
def domain(k,m):
 N=1<<k
 x=((np.arange(1<<N,dtype=np.int64)[:,None]>>np.arange(N))&1)
 a=((np.arange(1<<(k*m),dtype=np.int64)[:,None]>>np.arange(k*m))&1)
 b=np.sum((a.reshape(-1,k,m).sum(2)%2)*(1<<np.arange(k)),1)
 chi=np.array([[parity((s&c).bit_count()) for c in range(N)] for s in range(N)])
 X=(2*x-1)@chi.T
 return x,a,b,chi,X
results={"Authors":"Christian Reitwiessner"}
# Enumerate every mask marginal and every raw input; compute cross moments exactly.
k,m=2,3;N=1<<k;x,a,b,chi,X=domain(k,m);na=len(a);nt=len(x);Q=1<<(k*m)
records=[]
for R in range(1,8):
 means=[];seconds=[]
 for s in range(1,N):
  inds=[i*m+j for i in range(k) if s>>i&1 for j in range(m)]
  M=len(inds);h=M//2;Z=1<<M
  mu=np.zeros((nt,na),dtype=np.int64);sq=mu.copy()
  for mask in range(Z):
   z=np.array([(mask>>j)&1 for j in range(M)])
   D=np.sum(a[:,inds]^z,axis=1)-h;sig=parity(mask.bit_count()+h)
   full=sig*(phi(X[:,s,None]+D)+phi(X[:,s,None]-D))
   target=2*X[:,s,None]*chi[s,b]
   assert np.array_equal(full,target)
   e=sig*(clipped(X[:,s,None]+D,R)+clipped(X[:,s,None]-D,R))-target
   mu+=e;sq+=e*e
  # Bias divided by chi is independent of the full raw address arrangement.
  transformed=mu*chi[s,b]
  assert np.all(transformed==transformed[:,0,None])
  means.append(mu*(Q//Z));seconds.append(sq*(Q//Z))
 crosses=[int(np.sum(means[i]*means[j])) for i in range(N-1) for j in range(i)]
 assert all(v==0 for v in crosses)
 diagonal=Fraction(sum(int(np.sum(v)) for v in seconds),Q*nt*na)
 # Expected total MSE, averaging independent masks, computed by full second-moment expansion.
 total=diagonal+Fraction(2*sum(crosses),Q*Q*nt*na)
 assert diagonal==total
 rec={'radius':R,'mean_square_error':str(total),'cross_moment_numerators':crosses,'raw_inputs':nt*na,'mask_choices_joint':1<<(sum(s.bit_count()*m for s in range(1,N)))}
 records.append(rec)
results['full_mask_moments_k2m3']=records
print('Exact mask moments:',records,flush=True)
# Fixed mask circuit, independent raw-gate implementation and exhaustive target check.
k,m=3,3;N=1<<k;x,a,b,chi,X=domain(k,m);na=len(a);nt=len(x)
rng=random.Random(20261107)
zdict={}
for s in range(1,N):
 zdict[s]=[]
 for i in range(k):
  if s>>i&1:
   mask=rng.choice(range(1,(1<<m)-1));zdict[s].extend((mask>>j)&1 for j in range(m))
fixed=[]
for r in [1,2,3]:
 t=1<<r
 exact=2*sum(X[:,s,None]*chi[s,b] for s in range(t))
 cutoff=0 if t==N else -2*t
 target=((np.arange(1<<N)[:,None]>>b)&1)
 exact_wrong=int(np.count_nonzero((exact>=cutoff)!=target))
 for R in [1,2,3,4,6,8,12]:
  score=np.broadcast_to(2*X[:,0,None],(nt,na)).copy()
  gate_score=score.copy();gates=[]
  for s in range(1,t):
   inds=[i*m+j for i in range(k) if s>>i&1 for j in range(m)]
   z=np.array(zdict[s]);M=len(inds);h=M//2;sig=parity(int(z.sum())+h)
   D=(a[:,inds]^z).sum(1)-h
   score+=sig*(clipped(X[:,s,None]+D,R)+clipped(X[:,s,None]-D,R))
   for sign in [1,-1]:
    weights=[int(2*v) for v in chi[s]]+[0]*(k*m)
    for p,j in enumerate(inds):weights[N+j]=sign*(1-2*int(z[p]))
    constant=-int(chi[s].sum())+sign*(int(z.sum())-h)
    for ell in range(-R,R+2):
     def f(v):return parity(v)*v if abs(v)<=R else 0
     beta=sig*(f(ell)-f(ell-1))
     if not beta:continue
     threshold=ell-constant
     # Evaluate the actual raw-table/raw-address gate, not the ridge variables.
     activation=x@np.array(weights[:N])[:,None]+(a@np.array(weights[N:]))[None,:]>=threshold
     gate_score+=beta*activation
     gates.append({'weights':weights,'threshold':threshold,'top_weight':beta})
  assert np.array_equal(score,gate_score)
  wrong=int(np.count_nonzero((score>=cutoff)!=target));different=int(np.count_nonzero((score>=cutoff)!=(exact>=cutoff)))
  fixed.append({'r':r,'R':R,'bottoms':len(gates),'total_gates':len(gates)+1,'inputs':nt*na,'errors':wrong,'disagreements_with_majority':different,'majority_errors':exact_wrong,'MSE':str(Fraction(int(np.sum((score-exact)**2)),nt*na))})
  if r==3 and R==4:
   witness={'Authors':'Christian Reitwiessner','k':k,'m':m,'r':r,'R':R,'masks':zdict,'gates':gates,'raw_top_weights':[4]*N+[0]*(k*m),'top_constant':-2*N,'top_threshold':cutoff,'errors':wrong,'inputs':nt*na}
   (ROOT/'fixed_mask_witness.json').write_text(json.dumps(witness,indent=2))
results['fixed_mask_k3m3']=fixed
print('Raw-gate audits:',fixed,flush=True)
# Recheck selector witnesses using exact rational coefficients, including actual cost.
dictdata=json.loads((ROOT/'dictionary_results.json').read_text());checks=[]
for record in dictdata['results']:
 k,m=record['k'],record['m'];N=1<<k
 best=record['best'];C=[[Fraction(v) for v in row] for row in best['coefficients']]
 dirs=record['directions'];count=sum(v!=0 for row in C for v in row[1:])+sum(sum(C[c][j+1] for c in range(N))!=0 for j in range(len(dirs)))
 margins=[]
 for a0 in itertools.product((0,1),repeat=k*m):
  b0=sum((sum(a0[i*m:(i+1)*m])%2)<<i for i in range(k))
  E=[1]+[int(sum(v*w for v,w in zip(a0,direction))>=threshold) for direction,threshold in dirs]
  K=[sum(v*w for v,w in zip(row,E)) for row in C]
  margins.append(K[b0]-sum(abs(K[c]) for c in range(N) if c!=b0))
 assert min(margins)>0
 checks.append({'k':k,'m':m,'exact_bottoms':count,'claimed_bottoms':best['bottoms'],'exact_margin':str(min(margins))})
results['dictionary_audit']=checks
(ROOT/'verification.json').write_text(json.dumps(results,indent=2))
print('Dictionary audits:',checks,flush=True)
