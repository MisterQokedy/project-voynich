import re, csv, sys, json
src, outdir = sys.argv[1], sys.argv[2]
L = open(src, encoding='utf-8').read().split('\n')
VERD = [('NOT TESTABLE','NOT TESTABLE'),('NOT RESOLVED','NOT RESOLVED'),('UNTESTABLE','NOT TESTABLE'),('CALIBRATION FAIL','CALIBRATION FAIL'),
 ('NOT ROBUST','PASS, NOT ROBUST'),('REPLICATES','REPLICATES'),('REPRODUCED','REPLICATES'),('ADOPTED','ADOPTED'),('NOT KEPT','NOT KEPT'),
 ('INCONCLUSIVE','INCONCLUSIVE'),('BORDERLINE','BORDERLINE'),('BLIND','BLIND'),('MIXED','MIXED'),('DESCRIPTIVE','DESCRIPTIVE'),
 ('NO FIX FOUND','FAIL'),('FAIL','FAIL'),('PASS','PASS'),('HOLD','HOLDS'),('NO EVIDENCE','FAIL'),('NONE HOLDS','FAIL'),('FAILS','FAIL'),('NULL','NULL')]
def verdict(t):
    u=t.upper()
    for k,v in VERD:
        if k in u: return v
    return 'SEE SUMMARY'
CTRL = re.compile(r'(shuffl|null|placebo|control|random|calibrat|baseline|generator|held-out|bootstrap|permut)', re.I)
def vtext(head,b):
    m=re.search(r'\*\*([^*]{3,80})\*\*',head_raw[0]) or re.search(r' [—–-]{1,2} ([^`(]{3,90})',head)
    if m: return clean(m.group(1)).strip(' ,;')
    v=verdict(head)
    if v not in('SEE SUMMARY','NULL','HOLDS'): return v
    m=re.search(r'\b(PASS|FAIL|NOT TESTABLE|REPLICATES|INCONCLUSIVE)\b',b[:500])
    if m: return m.group(1)+' (from text)'
    t=re.sub(r'^- [^.()]*(\([^)]*\))?[.:]?\s*','',b) if b.startswith('- ') else b
    t=re.sub(r'^\(?`[^`]*`[^)]*\)\.?\s*','',t)
    t=re.sub(r'^\|.*?\|\s*(?=[A-Z][a-z])','',t) if t.startswith('|') else t
    t=re.sub(r'^Result:\s*','',t)
    return '~ '+sentences(t)[0][:140]
head_raw=['']
def sentences(t): return re.split(r'(?<=[.;])\s+', t)
def clean(t): return re.sub(r'\s+',' ',t.replace('**','')).strip()
rows=[]
def add(tid, title, line, body, theme):
    head_raw[0]=title
    b=clean(' '.join(body))
    head=clean(title)
    files=re.findall(r'`([^`]+/[^`]*)`', title+' '+' '.join(body[:3]))
    date=re.search(r'(\d{1,2}(?:-\d{1,2})? Nov 2026|\d{1,2} Nov)', title)
    plat='PC' if re.search(r'\(PC', title) or 'PC bundle' in title or 'Bundle' in title[:12] else 'cloud'
    ctrls=[s for s in sentences(b) if CTRL.search(s)][:2]
    rows.append(dict(id=tid, theme=theme, title=head[:200], date=date.group(1) if date else '', platform=plat,
        prereg='yes' if re.search(r'pre-?regist', title+b, re.I) else '',
        verdict=vtext(head,b),
        summary=b[:420], controls=' '.join(ctrls)[:300], files='; '.join(dict.fromkeys(files)), source_line=line))
# split file into headed blocks
heads=[i for i,l in enumerate(L) if re.match(r'#{2,3} ',l)]
heads.append(len(L))
for a,b in zip(heads,heads[1:]):
    h=L[a].lstrip('#').strip()
    body=[l for l in L[a+1:b]]
    if h.startswith('0.') or h.startswith('1.') or h.startswith('11.') or h.startswith('12.') or h.startswith('14.'): continue
    m=re.match(r'(\d+[a-z]?)\. (.*)',h)
    if m and m.group(1) in ('13','13b'):
        # each top-level bold bullet is a test
        cur=None
        for j,l in enumerate(body):
            mm=re.match(r'- \*\*([^*]+)\*\*(.*)',l)
            if mm:
                if cur: add(*cur)
                name=mm.group(1).strip().rstrip('.:')
                cur=[f"S{m.group(1)}:{name[:40]}", name+mm.group(2)[:160], a+2+j, [l], 'Language, generator & decipherment (§13)']
            elif cur and l.strip(): cur[3].append(l)
        if cur: add(*cur)
        continue
    if m:
        tid='§'+m.group(1); title=m.group(2); theme='Page order & physical (§'+m.group(1).rstrip('abcdefg')+')'
    else:
        tid=(' '.join(h.split()[:2]) if h.startswith('Bundle') else re.split(r'[ (:]',h)[0]) if not h.startswith('PC bundle') else h.split('(')[0].strip()
        if h.startswith('Hidden') or h.startswith('Published') or h.startswith('Line endings') or h.startswith('Generator gap') or h.startswith('f57v') : tid=h.split('(')[0].strip()[:30]
        title=h; theme='Later tests (22–26 Nov)'
    subs=[(j,l) for j,l in enumerate(body) if re.match(r'\*\*[A-Z][A-Za-z0-9\-+ /]{0,20}[ (:]',l)]
    if len(subs)>=2 and not m:
        for k,(j,l) in enumerate(subs):
            bold=re.match(r'\*\*([^*]+)\*\*',l).group(1)
            sid=re.split(r'[ (:]',bold)[0]
            vt=re.split(r'\)[,:]\s*|:\s*|\),\s*',bold,maxsplit=1)
            add(sid, bold, a+2+j, [l], theme)
            v=clean(vt[-1]).strip(' .)') if len(vt)>1 else ''
            rows[-1]['verdict']=v if v else rows[-1]['verdict']
            rows[-1]['title']=clean(h+' / '+bold)[:200]
        continue
    add(tid,title,a+1,body,theme)
OV={'§4':'NO: text cannot recover sheet order','§4a':'FAIL: no quire beats shuffled-page null (9 quires); q20 borderline p 0.06–0.14',
 '§4b':'L&D orders reproducible but at random-assignment level','§5':'Physical evidence fits the current (old) nesting',
 '§9':'Calibration: q20-shape p cannot separate no-sequence from herbal-like sequence','§9d':'LSA weak (power 0.15), Timm blind, tf-idf discriminates',
 '§9e':'Same-leaf r→v carry real (R 2.53, p 0.0005); quire 20 no measurable carry','§10':'Published orders at random-assignment level',
 'S13b:Step 5, regional languages in real manus':'FAIL: no regional language has the Voynich boundary or line profile','S13b:Small neural model of the text':'Diagnostic: 1.97 bits/glyph held-out'}
from verdicts_hand import HAND, BYSTART
OV.update(HAND)
for r in rows:
    if r['id'] in OV and (r['verdict'].startswith('~') or r['id'] in OV): r['verdict']=OV[r['id']]
for r in rows:
    for k,v in BYSTART.items():
        if r['summary'].startswith(k): r['verdict']=v
# theme refine for later tests by id prefix
def th(r):
    if r['theme']!='Later tests (22–26 Nov)': return r['theme']
    i=r['id'].upper()
    for p,t in [('S6','Generator (S6 family)'),('WS','Generator (S6 family)'),('GG','Generator (S6 family)'),('OO','Generator: one-off words'),
        ('S17','Page order & calibration'),('S11','Page drift'),('LE','Line structure'),('P4','Ink & image tests'),('P3','Ink & image tests'),('P5','Ink & image tests'),
        ('H10','Ink & image tests'),('H8','Ink & image tests'),('M1','Machine transliteration'),('X','Robustness on machine transliteration'),('B9','Robustness on machine transliteration'),
        ('B1','Ring/diagram pages'),('BUNDLE','Ring/diagram pages'),('N','Hidden-signal / meaning tests'),('D','Decipherment / cribs'),('C','Comparison corpora'),('F57','Decipherment / cribs')]:
        if i.startswith(p): return t
    return 'Other'
for r in rows: r['theme']=th(r); r['id']=r['id'].strip('*: ')
keys=['id','theme','title','date','platform','prereg','verdict','summary','controls','files','source_line']
with open(outdir+'/master_results_table.csv','w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,keys); w.writeheader(); w.writerows(rows)
from collections import Counter
print(len(rows)); print(Counter(r['verdict'] for r in rows)); print(Counter(r['theme'] for r in rows))
json.dump(rows,open('/home/user/scripts/rows.json','w'))
