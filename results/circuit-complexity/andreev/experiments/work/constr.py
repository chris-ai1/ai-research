# explicit constructions + exact integer verification
def parallel_construction(R,T):
    """f = sum_{c=2}^{2R+T} (-1)^c (c-1) [2y+t>=c]  -  sum_{c=2}^{T} (-1)^c (c-1) [t>=c]; 2R+2T-2 gates"""
    gates=[]
    for c in range(2,2*R+T+1): gates.append(((2,1),c,(-1)**c*(c-1)))
    for c in range(2,T+1): gates.append(((0,1),c,-(-1)**c*(c-1)))
    return gates,0
def verify(R,T,gates,const,f=lambda y,t:y*(-1)**t):
    for y in range(R+1):
        for t in range(T+1):
            v=const+sum(w for (a,b),th,w in gates if a*y+b*t>=th)
            if v!=f(y,t): return False
    return True
if __name__=="__main__":
    ok=all(verify(R,T,*parallel_construction(R,T)) for R in range(0,31) for T in range(0,31))
    print("parallel 2R+2T-2 construction verified 0..30 x 0..30:",ok)

def floor_construction(R,T):
    """y(-1)^t = y + 2R*floor(t/2) - 2*sum_{k=1..R} sum_j [ (2R+1)t+y >= (2R+1)(2j-1)+k ]
       gates: [y>=k] (k=1..R, weight 1), [t>=2j] (2<=2j<=T, weight 2R), lexicographic thresholds (weight -2).
       count = R + floor(T/2) + R*ceil(T/2)."""
    g=[]
    for k in range(1,R+1): g.append(((1,0),k,1))
    for j in range(1,T//2+1): g.append(((0,1),2*j,2*R))
    for j in range(1,(T+1)//2+1):
        for k in range(1,R+1): g.append(((1,2*R+1),(2*R+1)*(2*j-1)+k,-2))
    return g,0
def gadget_x0(T,C):
    """-2phi(t) - C x0 (-1)^t on {0,1}x{0..T}:  T + floor((T+1)/2) + 1 gates.
       uses x0(-1)^t = x0 + 2floor(t/2) - 2floor((t+x0)/2)."""
    phi=lambda u:(-1)**(u%2)*u
    g=[]
    for c in range(1,T+1):
        j=-2*(phi(c)-phi(c-1)) - 2*C*(1 if c%2==0 else 0)
        if j: g.append(((0,1),c,j))
    for j in range(1,(T+1)//2+1): g.append(((1,1),2*j,2*C))
    g.append(((1,0),1,-C))
    return g,0
if __name__=="__main__":
    ok=all(verify(R,T,*floor_construction(R,T)) and len(floor_construction(R,T)[0])==R+T//2+R*((T+1)//2) for R in range(0,31) for T in range(0,31))
    print("lexicographic floor construction verified 0..30 x 0..30:",ok)
    phi=lambda u:(-1)**(u%2)*u
    ok=True
    for T in range(0,61):
        for C in (0,2,6,64,1000):
            g,c=gadget_x0(T,C)
            ok&=verify(1,T,g,c,f=lambda x,t:-2*phi(t)-C*x*(-1)**t)
            ok&=len(g)<=T+(T+1)//2+1
    print("x0 gadget -2phi(t)-C x0(-1)^t verified T<=60, C in {0,2,6,64,1000}:",ok)
