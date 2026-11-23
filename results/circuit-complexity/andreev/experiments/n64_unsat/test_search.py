#!/usr/bin/env python3
# Copyright (c) 2026 Christian Reitwiessner.
# Authors: Christian Reitwiessner
"""Validate target semantics, restriction embeddings, and the symbolic checker."""
import sys
from pathlib import Path
import unittest
from itertools import product
from rules import rank_m2_program
from search import checker, initial, label, spread, save, eval_circuit

class Tests(unittest.TestCase):
    def test_n64_restriction_embeddings(self):
        for lengths in ([12]*4,[7,7,6,6,6]):
            N=1<<len(lengths);x=tuple(c.bit_count()%2 for c in range(N))
            for bits in product((0,1),repeat=8):
                a=[0]*sum(lengths)
                for d,b in zip(spread(lengths)[:8],bits):a[d]=b
                p=x+tuple(a)
                self.assertEqual(len(p),64)
                self.assertEqual(label(p,lengths),sum(bits)%2)

    def test_checker_known_rank_and_false_circuit(self):
        c=rank_m2_program().compile(1,2)
        raw=dict(bottom=[(list(g.weights),g.threshold) for g in c.gates],v=c.top,u=c.direct,tau=c.threshold)
        self.assertEqual(checker(raw,[2],5)['status'],'VERIFIED')
        raw['v']=[0]*len(c.top);raw['u']=[0]*len(c.direct);raw['tau']=0
        result=checker(raw,[2],5,batch=3)
        self.assertEqual(result['status'],'COUNTEREXAMPLES')
        self.assertEqual(len(result['examples']),3)

    def test_sample_labels_and_serialization(self):
        for lengths in ([12]*4,[7,7,6,6,6]):
            pts=initial(lengths,4,7)
            self.assertEqual(len(pts),1152)
            self.assertEqual(len(set(p for p,y in pts)),len(pts))
            self.assertTrue(all(len(p)==64 and y==label(p,lengths) for p,y in pts))
        p=Path(__file__).with_name('serialization_test.json')
        save(p,value=1)
        import json
        self.assertEqual(json.loads(p.read_text())['value'],1)
        p.unlink()

    def test_input_symmetry_preserves_a_known_full_target(self):
        lengths=[2,2];N=4
        c=rank_m2_program().compile(2,2)
        bottom=[(list(g.weights),g.threshold) for g in c.gates]
        top=list(c.top);direct=list(c.direct);tau=c.threshold
        flip=[d for d in range(N,8) if direct[d]<0]
        mask=sum((sum(d in flip for d in range(N+2*i,N+2*i+2))%2)<<i for i in range(2))
        def permute_table_and_flip(ws):
            return [ws[j^mask] for j in range(N)]+[-ws[d] if d in flip else ws[d] for d in range(N,8)]
        bottom2=[(permute_table_and_flip(ws),t-sum(ws[d] for d in flip)) for ws,t in bottom]
        direct2=permute_table_and_flip(direct);tau2=tau-sum(direct[d] for d in flip)
        order=list(range(N))
        for i in range(2):order+=sorted(range(N+2*i,N+2*i+2),key=lambda d:direct2[d])
        raw=dict(bottom=[([ws[d] for d in order],t) for ws,t in bottom2],v=top,
                 u=[direct2[d] for d in order],tau=tau2)
        pts=[(p,label(p,lengths)) for p in product((0,1),repeat=8)]
        self.assertFalse(eval_circuit(raw,pts))
        self.assertTrue(all(v>=0 for v in raw['u'][N:]))
        self.assertTrue(all(raw['u'][N+2*i]<=raw['u'][N+2*i+1] for i in range(2)))

if __name__=='__main__':
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Tests))
    save(Path(__file__).with_name('test_results.json'),tests=result.testsRun,success=result.wasSuccessful())
    raise SystemExit(not result.wasSuccessful())
