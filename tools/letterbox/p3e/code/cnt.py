import json,re,collections as C
M=json.load(open('~/p3e_work/data/meta.json'))
L=C.Counter();Mi=C.Counter();RL=C.Counter();RM=C.Counter()
for m in M:
    if m['prob']<.5 or m['pstart'] or m['nw']<4: continue
    wi,nw,gi,wl,g=m['wi'],m['nw'],m['gi'],m['wl'],m['g']
    if gi==0:
        if wi==0:L[g]+=1
        elif 2<=wi<=nw-2:Mi[g]+=1
    if gi==wl-1 and wl>=2:
        if wi==nw-1:RL[g]+=1
        elif 1<=wi<=nw-3:RM[g]+=1
print('L',[(g,L[g],Mi[g]) for g,_ in L.most_common(12)]);print('R',[(g,RL[g],RM[g]) for g,_ in RL.most_common(12)])
print('lines',len({m['line'] for m in M}),'pages',len({m['page'] for m in M}))
