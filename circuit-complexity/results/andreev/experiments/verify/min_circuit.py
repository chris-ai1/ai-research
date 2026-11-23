#!/usr/bin/env python3
"""
min_circuit.py -- exact search / lower-bound proofs for depth-two threshold circuits computing Andreev's function.

Model (identical to z3_min.py): S bottom threshold gates [alpha.p >= theta] read the inputs p; one top threshold gate reads
the S gate outputs AND (unless --no-top-direct) the inputs directly; all weights real.  Andreev's function A(x,a)=x_b,
b = sum_i (s_i mod 2) 2^i, s_i = weight of address block i (m bits each), N=2^k table bits.
  --mode full      inputs = N + k*m bits                       (all 2^(N+km) inputs)
  --mode blocksym  every gate sees block i only via s_i in 0..m (inputs (x,s), s in {0..m}^k); a blocksym circuit
                   is a full circuit of the same size, so blocksym-SAT => full-SAT and full-UNSAT => blocksym-UNSAT
                   (NOT the converse).
Decision procedure: z3 QF_LRA (complete & exact over the rationals).  Since 'circuit with S gates exists' is monotone
in S, UNSAT at S proves min > S for ALL smaller S at once, so lower bounds only need the single call S = L-1.

CLI examples
  python3 -I min_circuit.py --k 2 --m 3 --S 3                 # decide one S (SAT/UNSAT/UNKNOWN)
  python3 -I min_circuit.py --k 2 --m 3 --lb 4 --tl 3600      # try to PROVE "S<4 impossible" (decides only S=3)
  python3 -I min_circuit.py --k 2 --m 3 --min --tl 600        # ascending scan; first SAT = exact minimum
  python3 -I min_circuit.py --k 2 --m 3 --min --incr 8 --show # same, one incremental solver with 8 gate slots
  python3 -I min_circuit.py --mode full --k 2 --m 1 --min     # full (all N+km input bits) instead of block-symmetric
Output: lines "RESULT <mode> k m S SAT|UNSAT|UNKNOWN time cpu ..."; every SAT model is re-verified on ALL inputs with exact
rational arithmetic ("verified_exact=True") and printed with --show.  "PROVEN: ... min >= L" is printed only for UNSAT.
Exit code 2 if an exact verification fails.

Symmetry breaking (all provably WLOG; disable with --no-sym / --no-sym2 to reproduce the unbroken model):
  --sym   complementing a gate (alpha,theta,v) -> (-alpha,1-theta,-v), tau -> tau-v, and permuting gates  =>  0<=v_0<=...<=v_{S-1}
  --sym2  (needs top-direct) input symmetries of A: reflect s_i -> m-s_i (blocksym; full: flip one bit of block i), together
          with x_c -> x_{c xor e_i} when the parity flips, flips the sign of the top weight u on that coordinate => u>=0;
          permuting blocks / bits inside a block sorts them => u_{s_1}<=...<=u_{s_k} (blocksym), bit weights sorted (full).
"""
import sys, itertools, time, argparse, random
sys.path.insert(0, '/tmp/pydeps')
from fractions import Fraction
import z3


# ---------------------------------------------------------------- inputs / target
def make_points(k, m, mode):
    N = 1 << k
    P = []
    for x in itertools.product((0, 1), repeat=N):
        if mode == 'blocksym':
            for s in itertools.product(range(m + 1), repeat=k):
                P.append((x + s, x[sum((s[i] & 1) << i for i in range(k))]))
        else:
            for a in itertools.product((0, 1), repeat=k * m):
                b = sum((sum(a[i * m:(i + 1) * m]) & 1) << i for i in range(k))
                P.append((x + a, x[b]))
    return P


def fr(v):
    return Fraction(v.numerator_as_long(), v.denominator_as_long())


# ---------------------------------------------------------------- core model
class Model:
    """Incremental z3 model for fixed (k,m,mode,S).  Options:
       enc   : 'twosided' (default; z3_min encoding with ITE), 'onesided' (needs v>=0; half the implications)
       sym   : sign/permutation symmetry breaking (v_j>=0, v sorted; block-bit order of u in full mode)
       topdir: top gate reads the inputs directly
    """

    def __init__(self, k, m, mode, S, enc='twosided', sym=True, topdir=True, points=None, seed=0, sym2=True):
        self.k, self.m, self.mode, self.S, self.enc, self.sym, self.topdir = k, m, mode, S, enc, sym, topdir
        if enc == 'onesided' and not sym:
            raise ValueError('onesided encoding requires --sym (v>=0)')
        self.P = points if points is not None else make_points(k, m, mode)
        self.D = len(self.P[0][0])
        D = self.D
        self.so = z3.SolverFor('QF_LRA')
        self.al = [[z3.Real(f'a{j}_{d}') for d in range(D)] for j in range(S)]
        self.th = [z3.Real(f't{j}') for j in range(S)]
        self.v = [z3.Real(f'v{j}') for j in range(S)]
        self.u = [z3.Real(f'u{d}') for d in range(D)]
        self.tau = z3.Real('tau')
        if not topdir:
            for d in range(D):
                self.so.add(self.u[d] == 0)
        if sym:
            for j in range(S):
                self.so.add(self.v[j] >= 0)
                if j: self.so.add(self.v[j - 1] <= self.v[j])
            if topdir and sym2:
                # Input symmetries of A (all act linearly on a circuit, so they preserve size and the model class):
                #  (a) blocksym: s_i -> m-s_i (with x_c -> x_{c xor e_i} if m odd) ;  full: flip one bit of block i
                #      (with x_c -> x_{c xor e_i}).  Flips the sign of the top weight on that coordinate => WLOG >= 0.
                #  (b) permuting bits inside a block (full) / blocks among themselves: sort the weights.
                N = 1 << k
                if mode == 'blocksym':
                    for i in range(k):
                        self.so.add(self.u[N + i] >= 0)
                        if i: self.so.add(self.u[N + i - 1] <= self.u[N + i])
                else:
                    for i in range(k):
                        for t in range(m):
                            self.so.add(self.u[N + i * m + t] >= 0)
                            if t: self.so.add(self.u[N + i * m + t - 1] <= self.u[N + i * m + t])
                        if i: self.so.add(self.u[N + (i - 1) * m] <= self.u[N + i * m])
        self.active = set()

    def add_point(self, pi):
        if pi in self.active: return
        self.active.add(pi)
        p, out = self.P[pi]
        so, S, D, enc = self.so, self.S, self.D, self.enc
        nz = [d for d in range(D) if p[d]]
        zero = z3.RealVal(0)
        terms = []
        for j in range(S):
            lin = z3.Sum([self.al[j][d] * p[d] for d in nz] + [zero])
            g = z3.Bool(f'g{j}_{pi}')
            if enc == 'onesided':
                e = z3.Real(f'e{j}_{pi}')
                if out:   # want g true: only g -> lin>=th ; e <= v*g
                    so.add(z3.Implies(g, lin >= self.th[j]), e <= self.v[j], z3.Implies(z3.Not(g), e <= 0))
                else:     # want g false: lin>=th -> g ;  e >= v*g, e>=0
                    so.add(z3.Or(g, lin <= self.th[j] - 1), e >= 0, z3.Implies(g, e >= self.v[j]))
                terms.append(e)
            else:
                so.add(z3.Implies(g, lin >= self.th[j]), z3.Implies(z3.Not(g), lin <= self.th[j] - 1))
                terms.append(z3.If(g, self.v[j], zero))
        top = z3.Sum(terms + [self.u[d] * p[d] for d in nz] + [zero])
        so.add(top >= self.tau if out else top <= self.tau - 1)

    def check(self, tl):
        self.so.set('timeout', max(1, int(tl * 1000)))
        r = self.so.check()
        return 'SAT' if r == z3.sat else ('UNSAT' if r == z3.unsat else 'UNKNOWN')

    def extract(self):
        M = self.so.model()
        e = lambda x: fr(M.eval(x, model_completion=True))
        gates = [([e(a) for a in self.al[j]], e(self.th[j])) for j in range(self.S)]
        return gates, [e(x) for x in self.v], [e(x) for x in self.u], e(self.tau)


def circuit_out(circ, p):
    gates, v, u, tau = circ
    tot = sum((vj for (al, th), vj in zip(gates, v) if sum(a * c for a, c in zip(al, p) if c) >= th), Fraction(0))
    tot += sum(uu * c for uu, c in zip(u, p) if c)
    return 1 if tot >= tau else 0


def violated(circ, P):
    return [i for i, (p, o) in enumerate(P) if circuit_out(circ, p) != o]


# ---------------------------------------------------------------- driver for one S
def decide(k, m, mode, S, tl, enc='twosided', sym=True, topdir=True, cegar=False, init_frac=0.15, batch=20, seed=1, verbose=False, sym2=True):
    t0 = time.time()
    M = Model(k, m, mode, S, enc, sym, topdir, sym2=sym2)
    n = len(M.P)
    rnd = random.Random(seed)
    if cegar:
        init = rnd.sample(range(n), max(1, int(init_frac * n)))
    else:
        init = range(n)
    for pi in init: M.add_point(pi)
    rounds = 0
    while True:
        left = tl - (time.time() - t0)
        if left <= 0: return 'UNKNOWN', None, rounds, len(M.active), n
        r = M.check(left)
        rounds += 1
        if r != 'SAT': return r, None, rounds, len(M.active), n
        circ = M.extract()
        bad = violated(circ, M.P)
        if verbose: print(f'  round {rounds}: active={len(M.active)}/{n} violated={len(bad)}', file=sys.stderr, flush=True)
        if not bad: return 'SAT', circ, rounds, len(M.active), n
        rnd.shuffle(bad)
        for pi in bad[:batch]: M.add_point(pi)


def verify_all(k, m, mode, circ):
    P = make_points(k, m, mode)
    return len(violated(circ, P)) == 0, len(P)


def show(circ, k, m):
    gates, v, u, tau = circ
    for j, ((al, th), vj) in enumerate(zip(gates, v)):
        print(f'  gate{j}: [{" ".join(str(a) for a in al)}] >= {th}   top weight {vj}')
    print(f'  top: u=[{" ".join(str(a) for a in u)}] tau={tau}')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--k', type=int, required=True); ap.add_argument('--m', type=int, required=True)
    ap.add_argument('--mode', choices=['blocksym', 'full'], default='blocksym')
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--S', type=int, help='decide: does a circuit with <=S bottom gates exist?')
    g.add_argument('--lb', type=int, help='try to prove lower bound min>=L (decides S=L-1; UNSAT proves it)')
    g.add_argument('--min', action='store_true', help='ascending scan S=0,1,..; first SAT is the exact minimum')
    ap.add_argument('--smax', type=int, default=40, help='max S for --min')
    ap.add_argument('--incr', type=int, default=0, metavar='SMAX', help='with --min: ONE solver with SMAX gates, scan S by assumptions (v_j=0 for disabled gates); ~1.3-2x faster scan, but SMAX must be >= the minimum')
    ap.add_argument('--tl', type=float, default=600, help='time limit (s) per decision call')
    ap.add_argument('--enc', choices=['onesided', 'twosided'], default='twosided')
    ap.add_argument('--no-sym', action='store_true'); ap.add_argument('--no-sym2', action='store_true'); ap.add_argument('--cegar', action='store_true', help='lazy point generation (measured: slower on UNSAT, off by default)')
    ap.add_argument('--no-top-direct', action='store_true')
    ap.add_argument('--init-frac', type=float, default=0.15); ap.add_argument('--batch', type=int, default=20)
    ap.add_argument('--seed', type=int, default=1)
    ap.add_argument('--show', action='store_true'); ap.add_argument('-v', '--verbose', action='store_true')
    a = ap.parse_args()
    enc = a.enc
    if a.no_sym and enc == 'onesided': enc = 'twosided'
    td = not a.no_top_direct
    def one(S):
        t0 = time.time(); c0 = time.process_time()
        r, circ, rounds, nact, n = decide(a.k, a.m, a.mode, S, a.tl, enc, not a.no_sym, td, a.cegar, a.init_frac, a.batch, a.seed, a.verbose, not a.no_sym2)
        dt = time.time() - t0
        ok = ''
        if r == 'SAT':
            good, cnt = verify_all(a.k, a.m, a.mode, circ)
            ok = f' verified_exact={good}({cnt} inputs)'
            if not good: print('VERIFICATION FAILED', file=sys.stderr); sys.exit(2)
        print(f'RESULT {a.mode} k={a.k} m={a.m} S={S} {r} time={dt:.1f}s cpu={time.process_time()-c0:.1f}s cegar_rounds={rounds} points_used={nact}/{n}{ok}', flush=True)
        if r == 'SAT' and a.show: show(circ, a.k, a.m)
        return r
    if a.S is not None: one(a.S)
    elif a.lb is not None:
        if a.lb <= 0: print('LOWER BOUND min>=0 trivially'); return
        r = one(a.lb - 1)
        print({'UNSAT': f'PROVEN ({a.mode} model, top-direct={td}): no circuit with {a.lb-1} (or fewer) gates => min >= {a.lb}',
               'SAT': f'REFUTED: a circuit with {a.lb-1} gates exists => min <= {a.lb-1}',
               'UNKNOWN': f'UNDECIDED within time limit'}[r])
    elif a.incr:
        t0 = time.time(); c0 = time.process_time()
        M = Model(a.k, a.m, a.mode, a.incr, enc, not a.no_sym, td, sym2=not a.no_sym2)
        for pi in range(len(M.P)): M.add_point(pi)
        off = [z3.Bool(f'off{j}') for j in range(a.incr)]
        for j in range(a.incr): M.so.add(z3.Implies(off[j], M.v[j] == 0))   # v sorted ascending => disabled gates are the first ones
        for S in range(a.incr + 1):
            M.so.set('timeout', max(1, int((a.tl - (time.time() - t0)) * 1000)))
            r = M.so.check(*off[:a.incr - S]); r = 'SAT' if r == z3.sat else ('UNSAT' if r == z3.unsat else 'UNKNOWN')
            ok = ''
            if r == 'SAT':
                circ = M.extract(); good, cnt = verify_all(a.k, a.m, a.mode, circ)
                if not good: print('VERIFICATION FAILED', file=sys.stderr); sys.exit(2)
                ok = f' verified_exact=True({cnt} inputs)'
            print(f'RESULT {a.mode} k={a.k} m={a.m} S={S} {r} (incremental) elapsed={time.time()-t0:.1f}s cpu={time.process_time()-c0:.1f}s{ok}', flush=True)
            if r == 'SAT':
                print(f'MINIMUM {a.mode} k={a.k} m={a.m}: {S}'); 
                if a.show: show(circ, a.k, a.m)
                break
            if r == 'UNKNOWN': print(f'LOWER BOUND {a.mode} k={a.k} m={a.m}: min >= {S} (S={S} undecided)'); break
    else:
        for S in range(a.smax + 1):
            r = one(S)
            if r == 'SAT': print(f'MINIMUM {a.mode} k={a.k} m={a.m}: {S}'); break
            if r == 'UNKNOWN': print(f'LOWER BOUND {a.mode} k={a.k} m={a.m}: min >= {S} (S={S} undecided)'); break


if __name__ == '__main__':
    main()
