import sys; sys.path.insert(0,'/tmp/pydeps')
import math, time
from ortools.sat.python import cp_model
def dich(pts,D):
    seen={}
    for a in range(0,D+1):
        for b in range(-D,D+1):
            if (a,b)==(0,0) or math.gcd(a,abs(b))!=1 or (a==0 and b<0): continue
            vals=sorted(set(a*y+b*t for y,t in pts))
            for th in vals[1:]:
                key=tuple(int(a*y+b*t>=th) for y,t in pts)
                if key not in seen: seen[key]=(a,b,th)
    return seen
def solve(R,T,f,D=2,tl=600,B=None,workers=4,scale=2):
    pts=[(y,t) for y in range(R+1) for t in range(T+1)]
    H=dich(pts,D); keys=list(H)
    B=B or 4*(R+T+2)*scale
    m=cp_model.CpModel()
    c=[m.NewIntVar(-B,B,f"c{j}") for j in range(len(keys))]
    z=[m.NewBoolVar(f"z{j}") for j in range(len(keys))]
    for j in range(len(keys)): m.Add(c[j]==0).OnlyEnforceIf(z[j].Not())
    a0=m.NewIntVar(-50*B,50*B,"a0"); a1=m.NewIntVar(-B,B,"a1"); a2=m.NewIntVar(-B,B,"a2")
    for i,(y,t) in enumerate(pts):
        m.Add(sum(c[j] for j in range(len(keys)) if keys[j][i])+a0+a1*y+a2*t==scale*f(y,t))
    m.Minimize(sum(z))
    s=cp_model.CpSolver(); s.parameters.max_time_in_seconds=tl; s.parameters.num_workers=workers
    st=s.Solve(m)
    used=sorted((H[keys[j]],s.Value(c[j])) for j in range(len(keys)) if s.Value(z[j]))
    return s.StatusName(st),int(s.ObjectiveValue()),int(s.BestObjectiveBound()),used,(s.Value(a0),s.Value(a1),s.Value(a2))
if __name__=="__main__":
    R,T,D,tl=map(int,sys.argv[1:5])
    t0=time.time()
    st,v,lb,used,aff=solve(R,T,lambda y,t:y*(-1)**t,D,tl)
    print(f"R={R} T={T} D={D} {st} best={v} lb={lb} R+T={R+T} 2R+2T={2*R+2*T} {time.time()-t0:.0f}s aff={aff}",flush=True)
    for u in used: print("   ",u)
