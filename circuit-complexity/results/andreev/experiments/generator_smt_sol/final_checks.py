#!/usr/bin/env python3
# Copyright (c) 2026 Christian Reitwiessner
# Authors: Christian Reitwiessner
import engine as e
from pathlib import Path
records=[]
for k,m,r in [(2,3,1),(3,3,2),(3,3,5)]:
 c=e.library(k,m);result=e.check(c,k,m,r,timeout=30000,batch=1);records.append(dict(k=k,m=m,r=r,bottoms=len(c['bottom']),result=result));print(records[-1],flush=True)
e.save(Path(__file__).with_name('generic_budget_checks.json'),dict(results=records))
