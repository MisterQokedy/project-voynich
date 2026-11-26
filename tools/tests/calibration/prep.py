"""Clean calibration texts into running token streams (known order). Usage: prep.py SRC_DIR OUT_JSON"""
import re, sys, json, html, unicodedata
import numpy as np
SRC, OUT = sys.argv[1], sys.argv[2]

def toks(t):
    t = unicodedata.normalize('NFKD', t)
    t = ''.join(c for c in t if not unicodedata.combining(c)).lower()
    t = t.replace('þ', 'th').replace('ð', 'th').replace('æ', 'ae').replace('œ', 'oe').replace('ȝ', 'y')
    t = re.sub(r'\[\d+\]', ' ', t)
    return re.findall(r"[a-z]+", t)

def rd(path):
    b = open(path, 'rb').read()
    return b.decode('utf-16') if b[:2] in (b'\xff\xfe', b'\xfe\xff') else b.decode('utf-8', errors='replace')

def strip_html(t):
    t = re.sub(r'(?is)<(script|style|head).*?</\1>', ' ', t)
    t = re.sub(r'<[^>]+>', ' ', t)
    return html.unescape(t)

def strip_footnotes(lines):
    out, inn = [], False
    for L in lines:
        if re.match(r'^\[\d+\]', L): inn = True; continue
        if inn and (L.startswith(' ') and L.strip()): continue
        inn = False; out.append(L)
    return out

texts = {}
# Forme of Cury (c.1390 roll + 'Ancient Cookery' MS 1381), recipes only, editor footnotes removed
L = open(f'{SRC}/cury.txt', encoding='utf-8').read().split('\n')
s = next(i for i, x in enumerate(L) if x.startswith('FOR TO MAKE GRONDEN BENES'))
e = next(i for i, x in enumerate(L) if x.startswith('INDEX AND GLOSSARY'))
body = [x for x in strip_footnotes(L[s:e]) if not x.startswith('[Illustration')]
texts['cury_ME_recipes'] = toks('\n'.join(body))
# Culpeper, Complete Herbal (1653): herbal entries only
L = open(f'{SRC}/g49513.txt', encoding='utf-8').read().split('\n')
s = next(i for i, x in enumerate(L) if x.strip() == 'AMARA DULCIS.')
e = next(i for i, x in enumerate(L) if x.startswith('DIRECTIONS FOR MAKING SYRUPS'))
texts['culpeper_herbal'] = toks('\n'.join(L[s:e]))
# Isidore Etymologiae XII (animals), XVI (stones), XVII (plants), in book order
t = ''
for b in (12, 16, 17):
    h = strip_html(rd(f'{SRC}/ll/isidore{b}.html'))
    h = h.split('The Latin Library')[0]
    t += ' ' + h
texts['isidore_12_16_17'] = toks(t)
# Apicius I-V
t = ''
for b in range(1, 6):
    h = strip_html(open(f'{SRC}/ll/apicius{b}.html', encoding='utf-8', errors='replace').read())
    t += ' ' + h.split('The Latin Library')[0]
texts['apicius_1_5'] = toks(t)
# Gesta Romanorum (narrative control)
h = strip_html(open(f'{SRC}/ll/gesta.html', encoding='utf-8', errors='replace').read())
h = h.split('The Latin Library')[0]
texts['gesta_romanorum'] = toks(h)
# ---- units: self-contained items (recipe / herb entry / numbered section / paragraph), in true order
units = {}
L = open(f'{SRC}/cury.txt', encoding='utf-8').read().split('\n')
s = next(i for i, x in enumerate(L) if x.startswith('FOR TO MAKE GRONDEN BENES'))
e = next(i for i, x in enumerate(L) if x.startswith('INDEX AND GLOSSARY'))
U, cur = [], []
for x in strip_footnotes(L[s:e]):
    if x.startswith('[Illustration'): continue
    if x.strip() and not re.search(r'[a-z]', x) and len(x.strip()) > 3:
        if cur: U.append(cur)
        cur = []
    cur += toks(x)
U.append(cur); units['cury_ME_recipes'] = [u for u in U if u]
L = open(f'{SRC}/g49513.txt', encoding='utf-8').read().split('\n')
s = next(i for i, x in enumerate(L) if x.strip() == 'AMARA DULCIS.')
e = next(i for i, x in enumerate(L) if x.startswith('DIRECTIONS FOR MAKING SYRUPS'))
U, cur = [], []
for x in L[s:e]:
    if re.match(r'^ {4}[A-Z][^a-z]{2,}$', x):
        if cur: U.append(cur)
        cur = []
    cur += toks(x)
U.append(cur); units['culpeper_herbal'] = [u for u in U if u]
U = []
for b in (12, 16, 17):
    h = rd(f'{SRC}/ll/isidore{b}.html')
    h = strip_html(h).split('The Latin Library')[0]
    U += [toks(x) for x in re.split(r'\[\d+\]', h)]
units['isidore_12_16_17'] = [u for u in U if u]
U = []
for b in range(1, 6):
    h = open(f'{SRC}/ll/apicius{b}.html', encoding='utf-8', errors='replace').read()
    h = h.split('The Latin Library')[0]
    U += [toks(strip_html(x)) for x in re.split(r'(?i)<p>\s*(?=\d+\.\s+[A-Z])', h)]
units['apicius_1_5'] = [u for u in U if u]
h = open(f'{SRC}/ll/gesta.html', encoding='utf-8', errors='replace').read().split('The Latin Library')[0]
units['gesta_romanorum'] = [u for u in (toks(strip_html(x)) for x in re.split(r'(?i)<p[ >]', h)) if u]
for k, v in texts.items():
    us = units[k]; print(k, len(v), 'words;', len(us), 'units, median', int(np.median([len(u) for u in us])), 'words;', sum(map(len, us)), 'in units |', ' '.join(v[:10]))
json.dump(dict(stream=texts, units=units), open(OUT, 'w'))
