# Copyright (c) 2026 Christian Reitwiessner.
# Authors: Christian Reitwiessner
import sys,itertools,json,time
sys.path.insert(0,'/tmp/pydeps')
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix,hstack,block_diag,eye
from fractions import Fraction
print('# Authors: Christian Reitwiessner',flush=True)
out=[]
for k,m in [(2,3),(3,2)]:
 start=time.time(); N=1<<k; D=k*m
 a=np.array(list(itertools.product((0,1),repeat=D)),dtype=int); A=len(a)
 b=np.sum((a.reshape(A,k,m).sum(axis=2)%2)*(1<<np.arange(k)),axis=1)
 blocks=[(0,)*m]+[w for w in itertools.product((-1,1),repeat=m) if len(set(w))==2]
 cols={}
 for bs in itertools.product(blocks,repeat=k):
  w=sum(bs,())
  if not any(w) or next(v for v in w if v)!=1:continue
  v=a@w
  for th in range(int(v.min())+1,int(v.max())+1):
   e=(v>=th).astype(int);cols.setdefault(tuple(e),(w,th))
 E=np.array(list(cols),dtype=int).T;H=E.shape[1]
 B=csr_matrix(np.column_stack([np.ones(A),E]));P=N*(H+1)
 # Variables coefficients for each column, and absolute values of each K_c(a).
 K=block_diag([B]*N,format='csr');I=eye(N*A,format='csr')
 from scipy.sparse import vstack
 r=[];co=[];dat=[]
 for aa in range(A):
  for c in range(N):
   if c!=b[aa]:r.append(aa);co.append(c*A+aa);dat.append(1)
 U=csr_matrix((dat,(r,co)),shape=(A,N*A))
 Sel=csr_matrix((-np.ones(A),(np.arange(A),b*A+np.arange(A))),shape=(A,N*A))
 # split coefficients beta=p-q; minimize weighted L1, constants unpenalized
 M=vstack([hstack([K,-K,-I]),hstack([-K,K,-I]),hstack([Sel@K,-Sel@K,U])],format='csr')
 rhs=np.r_[np.zeros(2*N*A),-np.ones(A)]
 weights=np.ones(P);weights[::H+1]=0
 best=None;runs=[]
 for it in range(4):
  res=linprog(np.r_[weights,weights,np.zeros(N*A)],A_ub=M,b_ub=rhs,bounds=(0,None),method='highs',options={'time_limit':15})
  rr={'iteration':it,'status':int(res.status),'message':res.message};runs.append(rr)
  if not res.success:break
  coef=res.x[:P]-res.x[P:2*P]; C=coef.reshape(N,H+1)
  nz=np.abs(C[:,1:])>1e-7
  count=int(nz.sum()+np.count_nonzero(np.abs(C[:,1:].sum(axis=0))>1e-7))
  rr.update(bottoms=count,nonzeros=int(nz.sum()))
  rational=[[Fraction(float(v)).limit_denominator(1000000) for v in row] for row in C]
  margin=min(sum(rational[b[aa]][j]*int(([1]+list(E[aa]))[j]) for j in range(H+1))-sum(abs(sum(rational[c][j]*int(([1]+list(E[aa]))[j]) for j in range(H+1))) for c in range(N) if c!=b[aa]) for aa in range(A))
  rr['exact_margin']=str(margin)
  if margin>0 and (best is None or count<best['bottoms']):best={'bottoms':count,'coefficients':[[str(v) for v in row] for row in rational],'margin':str(margin)}
  weights=1/(np.abs(coef)+.03);weights[::H+1]=0
 result={'k':k,'m':m,'dictionary_size':H,'runs':runs,'best':best,'directions':list(cols.values()),'seconds':time.time()-start};out.append(result)
 print({key:val for key,val in result.items() if key not in ('directions','best')},flush=True)
 with open('/tmp/andreev_gap/upper_astra_round2/dictionary_results.json','w') as f:json.dump({'Authors':'Christian Reitwiessner','results':out},f,indent=2)
