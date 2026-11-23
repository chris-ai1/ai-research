import sys, time
sys.dont_write_bytecode=True
sys.path.insert(0,'/tmp/pydeps'); sys.path.insert(0,'/tmp/andreev_gap/verify')
import z3, mc_dev as mc
k,m,Smax=int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3])
t0=time.process_time()
M=mc.Model(k,m,'blocksym',Smax)
for pi in range(len(M.P)): M.add_point(pi)
off=[z3.Bool(f'off{j}') for j in range(Smax)]
for j in range(Smax): M.so.add(z3.Implies(off[j],M.v[j]==0))
for S in range(Smax+1):
    t1=time.process_time()
    M.so.set('timeout',600000)
    r=M.so.check(*[off[j] for j in range(Smax-S)])
    print('incremental S=',S,r,round(time.process_time()-t1,1),flush=True)
    if r==z3.sat: break
print('total cpu',round(time.process_time()-t0,1))
t0=time.process_time()
for S in range(Smax+1):
    t1=time.process_time(); r,c,_,_,_=mc.decide(k,m,'blocksym',S,600)
    print('fresh S=',S,r,round(time.process_time()-t1,1),flush=True)
    if r=='SAT': break
print('total cpu',round(time.process_time()-t0,1))
