# Copyright (c) 2026 Christian Reitwiessner.
# Authors: Christian Reitwiessner
import json
import unittest
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
from rules import (Aff, Gate, GateType, Program, ev, exhaustive, globally_reorientable,
                   rank_m2_program, slice_pair, smt_miter, window)


class RuleTests(unittest.TestCase):
    def test_index_and_parameter_separation(self):
        e = ('*', ('pow', 3, 'i'), ('-', 1, ('*', 2, ('parity', ('and', 'j', 't')))))
        self.assertEqual(ev(e, dict(i=2, j=3, t=1)), -9)
        self.assertEqual(Aff(1, (('scale', e),)).value(dict(i=2, j=3, t=1), {'scale': Q(2, 3)}), -5)
        with self.assertRaises(KeyError): ev('raw_table_bit', {})
        with self.assertRaises(ValueError): ev(('mod', 1, 0), {})

    def test_shared_parameters_across_sizes(self):
        gt = GateType((('j', 'N'),), Aff(0, (('q', ('eq', 'j', 'c')),)),
                      Aff(0, (('q', ('pow', 2, 'i')),)), Aff(1), Aff(1))
        p = Program((gt,), Aff(), Aff(), Aff(1))
        for k, m in [(2, 2), (3, 3), (4, 3), (4, 4)]:
            c = p.compile(k, m, {'q': Q(2, 3)})
            self.assertEqual(c.gates[-1].weights[(1 << k)-1], Q(2, 3))
            self.assertEqual(c.gates[0].weights[-1], Q(2, 3)*(1 << (k-1)))

    def test_rank_identity_all_raw_inputs(self):
        for k in [1, 2, 3]:
            c = rank_m2_program().compile(k, 2)
            self.assertEqual(exhaustive(c)['status'], 'VERIFIED_FINITE')
            self.assertFalse(globally_reorientable(c.gates, 1 << k, k, 2))
        # An accidental extension to m=3 must fail, not become an all-size claim.
        self.assertEqual(exhaustive(rank_m2_program().compile(2, 3))['status'], 'COUNTEREXAMPLE')

    def test_slice_identity(self):
        for alpha, beta, w, d in [([2,-4,6], 1, [1,-2,3,-1], -1),
                                  ([2**80,-2**81], 3, [1,-3], 1)]:
            gp, gm = slice_pair(alpha, beta, w, d)
            for z in product((0, 1), repeat=len(alpha)+len(w)):
                x, a = z[:len(alpha)], z[len(alpha):]
                ell = beta + sum(v*b for v,b in zip(alpha,x))
                Z = d + sum(v*b for v,b in zip(w,a))
                want = (1 if ell > 0 else -1) * (Z == 0)
                self.assertEqual(gp.value(z)-gm.value(z), want)
        with self.assertRaises(ValueError): slice_pair([1], 0, [1], 0)

    def test_window_identity(self):
        alpha, cutoff, signs = [1, -2, 1], 0, [1, -1, 1, -1]
        for lo in range(5):
            for hi in range(lo, 5):
                gates, vs = window(alpha, cutoff, signs, lo, hi)
                for z in product((0, 1), repeat=7):
                    x, a = z[:3], z[3:]
                    L = signs.count(-1) + sum(s*b for s,b in zip(signs,a))
                    h = sum(v*b for v,b in zip(alpha,x))
                    want = (-1)**sum(a) * (2*(h >= cutoff)-1) * (lo <= L <= hi)
                    self.assertEqual(sum(v*g.value(z) for v,g in zip(vs,gates)), want)

    def test_reorientation_zeros_and_ties(self):
        coherent = [Gate((1, 0, 0), Q(0)), Gate((-2, 3, 0), Q(0))]
        self.assertTrue(globally_reorientable(coherent, 0, 1, 3))
        inconsistent = [Gate((1, 1), Q(0)), Gate((1, -1), Q(0))]
        self.assertFalse(globally_reorientable(inconsistent, 0, 1, 2))
        self.assertEqual(Gate((Q(1,3),), Q(1,3)).value((1,)), 1)
        self.assertEqual(Gate((Q(1,3),), Q(1,3)).value((0,)), 0)

    def test_resource_guards(self):
        with self.assertRaises(ValueError): rank_m2_program().compile(3,2,gate_cap=7)
        with self.assertRaises(ValueError): rank_m2_program().compile(3,2,bit_cap=2)
        with self.assertRaises(ValueError): exhaustive(rank_m2_program().compile(4,2))

    def test_miter_serialization(self):
        s = smt_miter(rank_m2_program().compile(2,2))
        self.assertEqual(s.count('(declare-fun z'), 8)
        self.assertEqual(s.count('(define-fun g'), 4)
        self.assertIn('(assert (xor out', s)
        self.assertEqual(s.count('('), s.count(')'))


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(RuleTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    here = Path(__file__).resolve().parent
    summary = {'Authors': 'Christian Reitwiessner',
               'copyright': 'Copyright (c) 2026 Christian Reitwiessner',
               'tests': result.testsRun, 'success': result.wasSuccessful(),
               'rank_finite_domains': [16, 256, 16384],
               'slice_cases': 144, 'window_cases': 1920,
               'solver_campaign_run': False}
    (here/'test_results.json').write_text(json.dumps(summary, indent=2)+'\n')
    (here/'rank_k2_m2.smt2').write_text(smt_miter(rank_m2_program().compile(2,2)))
    raise SystemExit(not result.wasSuccessful())
