import re
hdr=open('report.md').read().split('PLACEHOLDER-SUMMARY')[0]
summ=open('summary.md').read()
body=open('report_body.md').read()
end=open('sec_end.md').read()
# split body into sections by '## '
parts=re.split(r'(?m)^(?=## )',body)
secs={}
for p in parts:
    m=re.match(r'## (\d)\.',p)
    if m: secs[int(m.group(1))]=p
    elif p.strip(): secs[0]=p
order=[secs[i] for i in sorted(secs) if i>0]
out=hdr+summ+'\n---\n\n'+'\n'.join(o.rstrip()+'\n' for o in order)+end
out=out.replace('PLACEHOLDER-SLOPE-TABLE',open('slope_table.md').read())
out=out.replace('PLACEHOLDER-FINITE-TABLE',open('finite_table.md').read())
open('report_assembled.md','w').write(out)
print(len(out),'chars; placeholders left:',re.findall(r'PLACEHOLDER-[A-Z0-9-]+',out))
# ---- finite table rows from logs
import collections
res=collections.defaultdict(dict)
for line in open('logs/finite_k2.log'):
    m_=re.match(r'RESULT k=2 m=(\d+) pool=(\w+) heuristic=(\d+) milp=(\w+)',line)
    if m_:
        m,pool,h,ml=int(m_.group(1)),m_.group(2),int(m_.group(3)),m_.group(4)
        res[m][pool]=(h,None if ml=='None' else int(ml))
exact={1:'3 / 3',2:'3 / 3',3:'$\\ge5$ / $\\ge4$',4:'$\\ge5$ / $\\ge4$',5:'– / $\\ge4$',6:'$\\ge6$ / $\\ge4$'}
rows=[]
for m in sorted(res):
    cells=[]
    for pool in ('axis','bsrich','half'):
        if pool in res[m]:
            h,ml=res[m][pool]; cells.append(f'{ml if ml is not None else h} (heur. {h})')
        else: cells.append('not run')
    tg=4*((m+1)//2)+m
    rows.append(f'| {m} | '+' | '.join(cells)+f' | {tg} | {exact.get(m,"–")} |')
out=open('report_assembled.md').read().replace('PLACEHOLDER-ROWS','\n'.join(rows))
open('report_assembled.md','w').write(out)
print('rows',len(rows))

exec(open('fills.py').read())
out=open('report_assembled.md').read()
for k_,v_ in fills.items(): out=out.replace(k_,v_)
open('report_assembled.md','w').write(out)
print('left:',re.findall(r'PLACEHOLDER-[A-Z0-9-]+',out))
