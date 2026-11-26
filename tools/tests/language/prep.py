"""Build tokenised page/line corpora. Usage: prep.py SRC_DIR OUT_JSON"""
import re, sys, json, html, unicodedata
SRC, OUT = sys.argv[1], sys.argv[2]
VOY = './work/manuscript_wide/pages2.json'
CURY = './work/forme_of_cury_pg8102.txt'
def toks(t):
    t = unicodedata.normalize('NFKD', t); t = ''.join(c for c in t if not unicodedata.combining(c)).lower()
    t = t.replace('þ','th').replace('ð','th').replace('æ','ae').replace('œ','oe').replace('ȝ','y').replace('ß','ss')
    t = re.sub(r'\[\d+\]', ' ', t)
    return re.findall(r"[a-z]+", t)
def rd(p): return open(p, 'rb').read().decode('utf-8', errors='replace') if p.endswith('txt') else open(p,'rb').read().decode('latin-1')
def strip_html(t):
    t = re.sub(r'(?is)<(script|style|head).*?</\1>', ' ', t); t = re.sub(r'<[^>]+>', ' ', t); return html.unescape(t).split('The Latin Library')[0]
def gut(t):
    s = re.search(r'\*\*\* ?START OF.*?\*\*\*', t); e = re.search(r'\*\*\* ?END OF', t)
    return t[s.end() if s else 0: e.start() if e else len(t)]
def pages(tk, P=190, L=9):
    return [[tk[i+j:i+j+L] for j in range(0, min(P, len(tk)-i), L)] for i in range(0, len(tk)-P+1, P)]
T = {}
T['latin_isidore'] = toks(' '.join(strip_html(rd(f'{SRC}/is{b}.html')) for b in (12, 16, 17)))
T['latin_caesar'] = toks(' '.join(strip_html(rd(f'{SRC}/c{b}.html')) for b in (1, 2, 3)))
c = open(CURY, encoding='utf-8').read(); s = c.find('FOR TO MAKE GRONDEN BENES'); e = c.find('INDEX AND GLOSSARY')
T['ME_cury'] = toks(re.sub(r'(?m)^\[\d+\].*$', ' ', c[s:e]))
c = gut(rd(f'{SRC}/culpeper.txt')); s = c.find('AMARA DULCIS'); e = c.find('DIRECTIONS FOR MAKING SYRUPS')
T['EME_culpeper'] = toks(c[s:e])
T['italian_dante'] = toks(gut(rd(f'{SRC}/dante.txt')))
T['german_faust'] = toks(gut(rd(f'{SRC}/faust.txt')))
C = {k: pages(v[:40000]) for k, v in T.items()}
V = json.load(open(VOY))
C['voynich'] = [[L['w'] for L in p['lines'] if L['w']] for p in V]
C['voynich_A'] = [[L['w'] for L in p['lines'] if L['w']] for p in V if p.get('L') == 'A']
C['voynich_B'] = [[L['w'] for L in p['lines'] if L['w']] for p in V if p.get('L') == 'B']
for k, v in C.items(): print(k, len(v), sum(len(l) for p in v for l in p))
json.dump(C, open(OUT, 'w'))
