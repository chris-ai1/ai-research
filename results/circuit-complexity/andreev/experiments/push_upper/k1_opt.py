# Re-derived k=1 optimum: ceil(m/2) gates.  P' = C(x0+x1-1) - u + 4*sum_{theta = 3 mod 4} [u>=theta],  u = 2s + x1 - x0,
# output x_b = [P'>0].  In our convention (output=[P<0]) use P = -P' (shifted by 1/2 is unnecessary since P' != 0).
import sys; sys.path.insert(0,'/tmp/andreev_gap/push_upper'); sys.path.insert(0,'/tmp/pydeps')
import numpy as np
from circ import Circuit, all_inputs, check
for m in range(1,17):
    C=Circuit(1,m); n=C.n; C3=3
    u=np.zeros(n,np.int64); u[2:]=2; u[1]=1; u[0]=-1
    # P = -[C3(x0+x1-1) - u + 4 sum [u>=th]] 
    C.u+= -C3*np.array([1,1]+[0]*m,dtype=object); C.K+=C3
    C.u+= np.array([int(v) for v in u],dtype=object)
    th=3
    while th<=2*m+1: C.gate(u,th,-4); th+=4
    C.finalize(); ok,marg,bad=check(C,all_inputs(n))
    print(m,'gates',C.size(),'ceil(m/2)',(m+1)//2,'ok',ok,'min|P|',marg)
