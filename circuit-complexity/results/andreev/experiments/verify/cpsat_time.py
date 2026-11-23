import sys,time
sys.dont_write_bytecode=True
sys.path.insert(0,'/tmp/pydeps')
src=open('/tmp/andreev_gap/cpsat_min.py').read().split("if __name__")[0]
ns={}; exec(src,ns)
for k,m,S in [(1,3,1),(1,3,2),(2,1,2),(2,1,3),(2,2,2),(2,2,3)]:
    t=time.time(); r=ns['feasible'](k,m,S,tl=100); print('cpsat',k,m,S,r,round(time.time()-t,1),flush=True)
