"""Run the ORIGINAL z3_min.py encoding (source patched only to also return the model) on every
instance where it reports SAT, and verify the extracted circuit with exact rational arithmetic."""
import sys, os
sys.path.insert(0, '/tmp/pydeps'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import andreev_points, eval_circuit
src = open('/tmp/andreev_gap/z3_min.py').read().split("if __name__")[0]
old = "r=so.check(); return 'SAT' if r==z3.sat else ('UNSAT' if r==z3.unsat else 'UNKNOWN')"
assert old in src
src = src.replace(old, "r=so.check(); return ('SAT' if r==z3.sat else ('UNSAT' if r==z3.unsat else 'UNKNOWN')), (so.model() if r==z3.sat else None), (al,th,v,u,tau), P")
ns = {}; exec(src, ns); z3 = ns['z3']
for mode, k, m in [(a, int(b), int(c)) for a, b, c in (x.split(',') for x in sys.argv[1:])]:
    for S in range(0, 8):
        r, mdl, (al, th, v, u, tau), P = ns['feasible'](k, m, S, mode, 3000)
        if r != 'SAT':
            continue
        q = lambda x: mdl.eval(x, model_completion=True).as_fraction()
        circ = dict(bottom=[([q(a) for a in al[j]], q(th[j])) for j in range(S)], v=[q(x) for x in v],
                    u=[q(x) for x in u], tau=q(tau))
        mine = andreev_points(k, m, mode)
        assert sorted(P) == sorted(mine), 'point set / target mismatch'
        bad = eval_circuit(circ, mine)
        print(f'orig {mode} k={k} m={m}: first SAT at S={S}; exact check on {len(mine)} points: '
              f'{"OK" if not bad else "FAIL %d" % len(bad)}; point set+target identical to independent impl', flush=True)
        break
