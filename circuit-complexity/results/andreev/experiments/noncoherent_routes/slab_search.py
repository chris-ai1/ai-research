#!/usr/bin/env python3
# Copyright (c) 2026 Christian Reitwiessner.
# Authors: Christian Reitwiessner
"""Bounded LP search in a specified dense-table adaptive-slab dictionary.
Requires numpy/scipy. This is not a minimum-gate or asymptotic search.
"""
import argparse, itertools, json, time
from pathlib import Path
import numpy as np
import scipy
from scipy.optimize import linprog


def run(m, limit, centered=False):
    k,N=2,4
    Y=np.array(list(itertools.product((-1,1),repeat=N)),dtype=np.int64)
    raw=np.array(list(itertools.product((0,1),repeat=k*m)),dtype=np.int64)
    address=(raw[:,:m].sum(axis=1)%2)+2*(raw[:,m:].sum(axis=1)%2)
    target=Y[:,address].reshape(-1)
    # The entire dictionary and target are odd under table complement.
    take=np.repeat(Y[:,0]==1,len(raw))
    table=[np.repeat(Y[:,i],len(raw)) for i in range(N)]
    hs=[]
    for omit in range(N):
        support=[i for i in range(N) if i!=omit]
        for suffix in itertools.product((-1,1),repeat=2):
            h=[0]*N
            for i,v in zip(support,(1,)+suffix): h[i]=v
            hs.append(h)
    patterns=[s for s in itertools.product((-1,1),repeat=m) if len(set(s))==2]
    normals=[]
    for p,q in itertools.product(patterns,repeat=2):
        for scale in (1,2,3):
            w=p+tuple(scale*z for z in q)
            if w[0]>0: normals.append(w)
    seen={}; specs=[]; cols=[]
    start=time.monotonic()
    for w in normals:
        z=raw@np.array(w)
        for h in hs:
            H=Y@np.array(h)
            for center in ([sum(w)//2] if centered and sum(w)%2==0 else ([] if centered else range(int(z.min())-1,int(z.max())+2))):
                L=z-center
                values=(np.sign(H)[:,None]*(2*np.abs(L)[None,:]<np.abs(H)[:,None])).reshape(-1).astype(np.int8)
                v=values[take]
                if not np.any(v):continue
                key=v.tobytes()
                if key in seen:continue
                seen[key]=len(specs)
                specs.append({'table':h,'address':list(w),'center':center})
                cols.append(v)
    dictionary=np.array(cols,dtype=np.float64).T
    affine=np.array([v[take] for v in table],dtype=np.float64).T
    A=np.column_stack((dictionary,-dictionary,affine))
    target_sub=target[take]
    A *= -target_sub[:,None]
    ncols=len(specs)
    objective=np.r_[np.ones(2*ncols),np.zeros(N)]
    print(json.dumps({'m':m,'candidate_atoms':ncols,'constraints':len(target_sub),'stage':'solving'}),flush=True)
    result=linprog(objective,A_ub=A,b_ub=-np.ones(len(target_sub)),
                   bounds=[(0,None)]*(2*ncols)+[(None,None)]*N,
                   method='highs', options={'time_limit':limit})
    record={'m':m,'k':k,'table_rows':'all signed sums of three of four table signs, modulo overall sign',
            'address_rows':'mixed +/-1 in block one, mixed +/-s in block two, s=1,2,3; modulo global sign',
            'candidate_atoms':ncols,'centered_only':centered,'constraints_after_table_complement':len(target_sub),
            'time_limit_seconds':limit,'status':int(result.status),'message':result.message,
            'elapsed_seconds':time.monotonic()-start,'numpy_version':np.__version__,
            'scipy_version':scipy.__version__,'objective':'L1 norm of atom coefficients; not gate count'}
    if result.success:
        coeff=result.x[:ncols]-result.x[ncols:2*ncols]
        scale=10**6
        weights=np.rint(scale*coeff).astype(np.int64)
        linear=np.rint(scale*result.x[-N:]).astype(np.int64)
        chosen=np.flatnonzero(weights)
        cert={'Authors':'Christian Reitwiessner','k':k,'m':m,
              'table_sign_convention':'y=1-2x',
              'affine_table_coefficients':linear.tolist(),
              'atoms':[dict(specs[j],coefficient=int(weights[j])) for j in chosen]}
        scores=Y@linear
        scores=np.repeat(scores,len(raw))
        for j in chosen:
            h=np.array(specs[j]['table']);w=np.array(specs[j]['address'])
            H=Y@h; L=raw@w-specs[j]['center']
            values=(np.sign(H)[:,None]*(2*np.abs(L)[None,:]<np.abs(H)[:,None])).reshape(-1)
            scores += int(weights[j])*values
        margin=int(np.min(scores*target))
        assert margin>0
        record.update(atoms=len(chosen),bottom_gates_unmerged=2*len(chosen),
                      exact_integer_margin=margin,checked_raw_inputs=len(target))
        Path(__file__).with_name(f'slab_certificate_m{m}{"_centered" if centered else ""}.json').write_text(json.dumps(cert,indent=2)+'\n')
    Path(__file__).with_name(f'slab_search_m{m}{"_centered" if centered else ""}.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps(record,indent=2),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--m',type=int,default=3);p.add_argument('--seconds',type=float,default=30)
    p.add_argument('--centered',action='store_true')
    a=p.parse_args();run(a.m,a.seconds,a.centered)
