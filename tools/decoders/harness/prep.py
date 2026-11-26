"""Build target-language corpora. Usage: prep.py SRC_DIR. Output ../corpora.json (token lists).
Sources: thelatinlibrary.com isidore/12-17.shtml, caesar/gall1-4.shtml; Gutenberg (pglaf) 1012 Dante, 2000 Quijote, 3333 Lusiadas, 49513 Culpeper."""
import re, sys, json, html, unicodedata
S = sys.argv[1]
def toks(t):
    t = unicodedata.normalize('NFKD', t); t = ''.join(c for c in t if not unicodedata.combining(c)).lower()
    t = t.replace('æ', 'ae').replace('œ', 'oe').replace('ß', 'ss').replace('j', 'i').replace('v', 'u')   # Latin-style u/v, i/j merged everywhere
    return re.findall(r'[a-z]+', re.sub(r'\[\d+\]', ' ', t))
def lat(f):
    t = open(f'{S}/{f}', 'rb').read().decode('latin-1'); t = re.sub(r'(?is)<(script|style|head).*?</\1>', ' ', t)
    return toks(html.unescape(re.sub(r'<[^>]+>', ' ', t)).split('The Latin Library')[0])
def gut(f):
    t = open(f'{S}/{f}', 'rb').read().decode('utf-8', 'replace'); s = re.search(r'\*\*\* ?START OF.*?\*\*\*', t); e = re.search(r'\*\*\* ?END OF', t)
    return t[s.end() if s else 0: e.start() if e else len(t)]
C = {}
C['latin'] = sum((lat(f'is{b}.html') for b in (12, 13, 14, 15, 16, 17)), []) + sum((lat(f'c{b}.html') for b in (1, 2, 3)), [])
C['latin_plain'] = lat('c4.html')                       # calibration plaintext, not in the Latin LM
d = gut('pg1012.txt'); k = d.find('PARADISO', len(d) // 2)
C['italian'] = toks(d[:k]); C['italian_plain'] = toks(d[k:])  # Inferno+Purgatorio = LM; Paradiso = calibration plaintext
C['spanish'] = toks(gut('pg2000.txt'))[:200000]
C['portuguese'] = toks(gut('pg3333.txt'))
c = gut('pg49513.txt'); C['english'] = toks(c[c.find('AMARA DULCIS'): c.find('DIRECTIONS FOR MAKING SYRUPS')])
for k2, v in C.items(): print(k2, len(v), v[:8])
json.dump(C, open('./work/decipherment_harness/corpora.json', 'w'))
