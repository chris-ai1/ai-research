#!/usr/bin/env python3
# Copyright (c) 2026 Christian Reitwiessner.
# Authors: Christian Reitwiessner
"""Check learner/compiler agreement without trusting learned gate activations."""
from fractions import Fraction as Q
import json
from pathlib import Path
import random
import unittest
from experiment import FrozenBottomTemplate, Learner, Template, check, rat, target, z3

class ExactTests(unittest.TestCase):
    def test_fixed_parameters_match_raw_evaluation(self):
        rng = random.Random(41)
        for kind,types,width in [('positional',1,2),('coupled',2,3)]:
            template = Template(kind,types,width)
            theta = {p:Q(rng.randrange(-3,4),rng.randrange(1,4)) for p in template.names}
            for k,m in [(1,2),(2,2)]:
                circuit = template.compile(k,m,theta)
                n = (1 << k)+k*m
                for _ in range(6):
                    point = tuple(rng.randrange(2) for _ in range(n))
                    learner = Learner(template,2000,0)
                    self.assertTrue(learner.add(k,m,point))
                    self.assertFalse(learner.add(k,m,point))
                    learner.solver.add(*[learner.theta[p]==rat(q) for p,q in theta.items()])
                    got = learner.solver.check()
                    self.assertNotEqual(got,z3.unknown)
                    self.assertEqual(got==z3.sat,circuit.value(point)==target(k,m,point))

    def test_miter_detects_invalid_shared_rule(self):
        t = Template('positional',1,2)
        c = t.compile(2,2,{p:Q(0) for p in t.names})
        result = check(c,2000,batch=1)
        self.assertEqual(result['status'],'COUNTEREXAMPLES')
        self.assertEqual(len(result['points']),1)

    def test_freezing_retains_exact_bottom_gates(self):
        t=Template('coupled',2,3)
        theta={p:Q((i%5)-2,3) for i,p in enumerate(t.names)}
        frozen=FrozenBottomTemplate(t,theta)
        top={p:theta[p] for p in frozen.names}
        for k,m in [(2,2),(3,3)]:
            self.assertEqual(t.compile(k,m,theta),frozen.compile(k,m,top))

    def test_known_shared_rule_and_ties(self):
        t=Template('calibration')
        theta=dict(v=Q(1),direct=Q(-1),cutoff=Q(1))
        for k in (1,2,3):
            c=t.compile(k,2,theta)
            self.assertEqual(check(c,5000)['status'],'VERIFIED')
        c=t.compile(2,3,theta)
        self.assertEqual(check(c,2000,batch=1)['status'],'COUNTEREXAMPLES')

if __name__=='__main__':
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(ExactTests))
    Path(__file__).with_name('test_results.json').write_text(json.dumps(dict(Authors='Christian Reitwiessner',tests=result.testsRun,success=result.wasSuccessful(),learner_compiler_comparisons=24),indent=2)+'\n')
    raise SystemExit(not result.wasSuccessful())
