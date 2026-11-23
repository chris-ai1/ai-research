from fractions import Fraction as F
import itertools
def gates(m):
    J=(m+1)//2; G=[]
    for j in range(1,J+1):
        G+= [((1,0),0,2*j,-4),((1,0),2,2*j,-2),((0,1),0,2*j,-4),((0,1),1,2*j,-2)]
    for j in range(1,m+1): G.append(((1,1),0,2*j,-4))
    return G
def ok(m):
    G=gates(m); assert len(G)==4*((m+1)//2)+m
    minmarg=None
    for x in itertools.product([0,1],repeat=4):
        for s1 in range(m+1):
            for s2 in range(m+1):
                Fv=sum(v for (bs,c,th,v) in G if bs[0]*s1+bs[1]*s2+x[c]>=th)
                Fv+=5*s1+5*s2+8*x[0]+2*x[1]+F(3,2)*x[2]+x[3]-F(13,2)
                b=(s1%2)+2*(s2%2)
                if (Fv>=0)!=(x[b]==1): return False,None
                mg=abs(Fv); minmarg=mg if minmarg is None else min(minmarg,mg)
    return True,minmarg
print([ (m,)+ok(m) for m in range(1,41)])
