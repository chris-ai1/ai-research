import sys; sys.path.insert(0,'/tmp/pydeps')
exec(open('gadget_min.py').read().split('if __name__')[0])
import time
for R,T,D in [(3,2,3),(3,3,3),(4,3,3),(4,4,3),(5,5,3),(6,6,3)]:
    t0=time.time(); st,opt,used,G=solve(R,T,D,tl=240)
    print(f"R={R} T={T} D={D}: best={opt} status={st} ({'optimal' if st==0 else 'time limit'}) cands={G} R+T={R+T} ours={2*R+2*T} [{time.time()-t0:.0f}s]",flush=True)
