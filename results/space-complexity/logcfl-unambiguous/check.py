"""Exhaustive seed checks for the proof-tree isolation lemma (paper.tex).

For small random layered alternating semi-unbounded circuits, enumerate every seed and check:
  * derr: violations of the derivative lemma (expected 0 for base 6);
  * worst_bad_over_bound: max over (OR gate, input pair) of #tying seeds / 2^#agreeing code bits
    (the collision lemma says <= 1);
  * noniso_frac: fraction of seeds that are not min-isolating.
Also shows that bases 2..5 violate the derivative bound and that an OR layer next to the leaves
defeats isolation for every seed. Run: python3 check.py
"""
import random, itertools, sys
from fractions import Fraction as Fr

def make_code(N, ell, d, rng):
    words=[]; tries=0
    allw=list(range(1<<ell)); rng.shuffle(allw)
    for w in allw:
        if all(bin(w^v).count('1')>=d for v in words):
            words.append(w)
            if len(words)==N: break
    if len(words)<N: return None
    # make some pairs at exactly distance d if possible: fine as is
    return [[(w>>(ell-1-j))&1 for j in range(ell)] for w in words]

def build(K, width, rng, dense, v1and=True):
    # layers: 0 leaves; AND at odd layers (AND-level k at layer 2k-1); OR at even
    L=[]
    leaves=[('leaf', rng.random()<0.8) for _ in range(width)]
    L.append(leaves)
    for layer in range(1, 2*K+1):
        isand = (layer%2==1) if v1and else (layer%2==0)
        prev=len(L[-1]); gates=[]
        for _ in range(width):
            if isand:
                if rng.random()<0.2: ch=[rng.randrange(prev)]
                else: ch=rng.sample(range(prev),2) if prev>1 else [0]
                gates.append(('and',ch))
            else:
                if dense: ch=[c for c in range(prev) if rng.random()<0.8] or [0]
                else: ch=rng.sample(range(prev), rng.randint(1,min(prev,3)))
                gates.append(('or',ch))
        L.append(gates)
    return L

def evaluate(L, wt):
    # returns per layer list of (mu, count) or None
    res=[[ (0,1) if g[1] else None for g in L[0]]]
    for li in range(1,len(L)):
        out=[]
        for gi,(t,ch) in enumerate(L[li]):
            vals=[res[li-1][c] for c in ch]
            if t=='and':
                if any(v is None for v in vals): out.append(None); continue
                mu=wt[(li,gi)]+sum(v[0] for v in vals); cnt=1
                for v in vals: cnt*=v[1]
                out.append((mu,cnt))
            else:
                vs=[v for v in vals if v is not None]
                if not vs: out.append(None); continue
                m=min(v[0] for v in vs); out.append((m,sum(v[1] for v in vs if v[0]==m)))
        res.append(out)
    return res

def weights(L, code, x, ell, base, v1and=True):
    wt={}; gid=0; ids={}
    for li in range(1,len(L)):
        for gi,(t,ch) in enumerate(L[li]):
            ids[(li,gi)]=gi
            if t=='and':
                k=(li+1)//2 if v1and else li//2
                c=code[ids[(li,gi)]]
                wt[(li,gi)]=sum(base**(k+ell-j-1)*c[j]*x[j] for j in range(ell))  # j 0-indexed -> exponent k+ell-(j+1)
            else: wt[(li,gi)]=0
    return wt, ids

def run(seed, K, width, ell, d, base=6, dense=True, v1and=True):
    rng=random.Random(seed)
    L=build(K,width,rng,dense,v1and)
    N=width
    code=make_code(N,ell,d,rng)
    if code is None: return None
    seeds=list(itertools.product([0,1],repeat=ell))
    R={}
    for x in seeds:
        wt,ids=weights(L,code,x,ell,base,v1and); R[x]=evaluate(L,wt)
    # derivative check
    derr=0
    for li in range(1,len(L)):
        for gi,(t,ch) in enumerate(L[li]):
            if t!='and': continue
            k=(li+1)//2 if v1and else li//2
            c=code[ids[(li,gi)]]
            for x in seeds:
                if x[0]==1: pass
                for j in range(ell):
                    if x[j]==1: continue
                    x1=list(x); x1[j]=1; x1=tuple(x1)
                    a=R[x][li][gi]; b=R[x1][li][gi]
                    if a is None: continue
                    der=b[0]-a[0]; B=base**(k+ell-j-1)
                    if not (B*c[j] <= der <= Fr(B)*(c[j]+Fr(1,2))): derr+=1
    # bad-event count per triple and isolation
    worst=0; triples=0; nonisoseeds=0
    for li in range(2,len(L)):
        for gi,(t,ch) in enumerate(L[li]):
            if t!='or': continue
            for u,v in itertools.combinations(ch,2):
                if R[seeds[0]][li-1][u] is None or R[seeds[0]][li-1][v] is None: continue
                triples+=1
                bad=sum(1 for x in seeds if R[x][li-1][u][0]==R[x][li-1][v][0])
                cu=code[ids[(li-1,u)]]; cv=code[ids[(li-1,v)]]
                agree=sum(1 for a,b in zip(cu,cv) if a==b)
                worst=max(worst, bad/2**agree)
    for x in seeds:
        if any(r is not None and r[1]>1 for layer in R[x] for r in layer): nonisoseeds+=1
    return dict(N=N,derr=derr,triples=triples,worst_bad_over_bound=worst,noniso_frac=nonisoseeds/len(seeds))

if __name__=='__main__':
    configs=[(1,3,4,8,3),(2,4,4,8,4),(3,3,6,9,4),(4,4,3,7,3),(5,2,8,10,4)]  # (rng seed, K, width, ell, d)
    print('base 6, AND layer next to the leaves:')
    for args in configs:
        for dense in (True,False):
            print(' ',args,'dense' if dense else 'sparse',run(*args,dense=dense))
    print('base sensitivity (summed over the configurations above):')
    for b in (2,3,4,5,6):
        res=[run(*a,base=b,dense=dn) for a in configs for dn in (True,False)]
        print(f'  base {b}: derivative violations {sum(r["derr"] for r in res)}, '
              f'max tying/bound {max(r["worst_bad_over_bound"] for r in res)}')
    print('OR layer next to the leaves:', run(*configs[0],v1and=False))
