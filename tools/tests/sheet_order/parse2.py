"""Parse ZL3b-n IVTFF into page records with line-level words + unit type."""
import re, json, sys
src, out = sys.argv[1], sys.argv[2]
hdr = re.compile(r'^<(f\d+[rv]\d*)>\s*<!(.*)>')
loc = re.compile(r'^<(f\d+[rv]\d*)\.(\d+),([@+*=&~!])(\w+)>\s*(.*)$')
def clean(text):
    text = re.sub(r'<![^>]*>', '', text)
    text = re.sub(r'<->', '.', text)
    text = re.sub(r'<[^>]*>', '', text)
    text = re.sub(r'\[([^:\]]*):[^\]]*\]', r'\1', text)
    text = text.replace('{', '').replace('}', '')
    words = [w for w in re.split('[.,]', text) if w]
    return [w for w in words if re.fullmatch(r'[a-z]+', w)]
pages = {}; order = []
for line in open(src, encoding='latin-1'):
    line = line.rstrip('\n')
    if line.startswith('#') or not line.strip(): continue
    m = hdr.match(line)
    if m:
        cur = m.group(1); meta = dict(re.findall(r'\$(\w)=(\w+)', m.group(2)))
        pages[cur] = {'panel': cur, **meta, 'lines': []}; order.append(cur); continue
    m = loc.match(line)
    if m:
        pg, n, mark, unit, text = m.groups()
        pages[pg]['lines'].append({'n': int(n), 'u': unit[0], 'mark': mark, 'w': clean(text)})
# merge panels into pages f67r1 -> f67r
merged = {}; morder = []
for p in order:
    m = re.match(r'f(\d+)([rv])', p); key = '%s%s' % (m.group(1), m.group(2))
    if key not in merged:
        d = dict(pages[p]); d['page'] = key; d['leaf'] = int(m.group(1)); d['side'] = m.group(2)
        d['lines'] = list(pages[p]['lines']); merged[key] = d; morder.append(key)
    else: merged[key]['lines'] += pages[p]['lines']
res = [merged[k] for k in morder]
for r in res: r['nwords'] = sum(len(l['w']) for l in r['lines'])
json.dump(res, open(out, 'w'))
print(len(res), 'pages', sum(r['nwords'] for r in res), 'words')
