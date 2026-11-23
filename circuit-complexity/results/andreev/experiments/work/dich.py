import sys; sys.path.insert(0,'/tmp/pydeps')
import math, numpy as np
from fractions import Fraction
def all_dichotomies(pts):
    """Complete list of halfplane dichotomies (as 0/1 tuples, canonical: contains no complement duplicate)
    returns dict key->(a,b,theta) with key[i]=[a*y+b*t>=theta] , a,b rational(float ok, we store Fractions)."""
    P=np.array(pts)
    angs=set()
    for i in range(len(pts)):
        for j in range(i+1,len(pts)):
            dy=pts[j][0]-pts[i][0]; dt=pts[j][1]-pts[i][1]
            # normal (a,b) orthogonal to (dy,dt): (dt,-dy) and opposite
            for (a,b) in ((dt,-dy),(-dt,dy)):
                angs.add(math.atan2(b,a))
    angs=sorted(angs)
    mids=[(angs[k]+angs[(k+1)%len(angs)]+(2*math.pi if k==len(angs)-1 else 0))/2 for k in range(len(angs))]
    seen={}
    for m in mids:
        a,b=math.cos(m),math.sin(m)
        v=P[:,0]*a+P[:,1]*b
        order=np.argsort(v)
        for k in range(1,len(pts)):
            key=[0]*len(pts)
            for idx in order[k:]: key[idx]=1
            key=tuple(key); comp=tuple(1-x for x in key)
            if key in seen or comp in seen: continue
            seen[key]=(a,b,(v[order[k-1]]+v[order[k]])/2)
    return seen
