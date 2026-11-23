# Min #bottom gates for Andreev(k,m), full model, with integer bottom weights/thresholds |w|<=W
# (threshold unrestricted int), top weights real & unbounded (top reads gates + inputs).
import sys, itertools, time; sys.path.insert(0,'/tmp/pydeps'); import z3
k,m,S,W=map(int,sys.argv[1:5]); N=2**k; n=N+k*m
pts=[]
for x in itertools.product([0,1],repeat=N):
  for a in itertools.product([0,1],repeat=k*m):
    b=0
    for i in range(k): b|=(sum(a[i*m:(i+1)*m])%2)<<i
    pts.append((x+a, x[b]))
s=z3.Solver(); s.set('timeout',int(sys.argv[5])*1000 if len(sys.argv)>5 else 600000)
w=[[z3.Int(f'w{j}_{d}') for d in range(n)] for j in range(S)]; th=[z3.Int(f't{j}') for j in range(S)]
u=[z3.Real(f'u{j}') for j in range(S)]; v=[z3.Real(f'v{d}') for d in range(n)]; tau=z3.Real('tau')
for j in range(S):
  for d in range(n): s.add(w[j][d]>=-W, w[j][d]<=W)
for j in range(S-1): s.add(u[j]<=u[j+1])   # gate symmetry (complementing gates absorbed: u>=0 wlog)
for j in range(S): s.add(u[j]>=0)
for p,y in pts:
  top=z3.Sum([z3.If(z3.Sum([w[j][d] for d in range(n) if p[d]])>=th[j],u[j],0) for j in range(S)]+[v[d] for d in range(n) if p[d]])
  s.add(top>=tau+1 if y else top<=tau-1)
t=time.time(); r=s.check(); print(f'k={k} m={m} S={S} W={W}: {r} {time.time()-t:.1f}s',flush=True)
if r==z3.sat:
  M=s.model(); 
  for j in range(S): print(' gate',[M[w[j][d]] for d in range(n)],'>=',M[th[j]],'u=',M[u[j]])
