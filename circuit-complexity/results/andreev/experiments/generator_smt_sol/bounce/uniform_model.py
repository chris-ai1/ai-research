#!/usr/bin/env python3
# Copyright (c) 2026 Christian Reitwiessner
# Authors: Christian Reitwiessner
"""Simplified all-m ordinary A_(3,m) model: equal character-channel coefficients."""
import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import engine as e
from constructions import atoms3,character
from audit import exhaustive

def build(m):
 bottom=[];v=[]
 for s,r,_ in atoms3():
  al=[character(s,c) for c in range(8)];address=[6*int(bool(s>>i&1)) for i in range(3) for _ in range(m)]
  for j in range(s.bit_count()*m//2+1):bottom.append((al+address,12*j+r));v.append(12)
  bottom.append((al+[0]*(3*m),r));v.append(-6)
 return dict(bottom=bottom,v=v,u=[4]*8+[-42]*(3*m),tau=55)

if __name__=='__main__':
 root=Path(__file__).resolve().parent;records=[]
 for m in [1,2,3,4,6]:
  c=build(m);full=exhaustive(c,3,m,range(256));assert full['status']=='VERIFIED';records.append(dict(m=m,bottoms=len(c['bottom']),ordinary_exact=full))
 c=build(3);symbolic=e.independent.check(c,e.independent.andreev_target(3,3),timeout_ms=10000)
 e.save(root/'uniform_model.json',dict(candidate=c,k=3,m=3,r=-1,records=records,ordinary_symbolic=symbolic,finite_core_margin=3,uniform_count='6 floor(m/2)+6m+floor(3m/2)+26'))
 print(records,symbolic,flush=True)
