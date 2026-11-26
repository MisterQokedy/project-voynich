"""Sheet-level FIT/TEST split stratified by majority (hand, illustration). Writes ../split.json."""
import json, random, collections
D = json.load(open('./work/manuscript_wide/pages2.json'))
sh = collections.defaultdict(list)
for p in D: sh[p['Q'] + p['B']].append(p)
strat = collections.defaultdict(list)
for s, ps in sorted(sh.items()):
    strat[collections.Counter((p.get('H'), p['I']) for p in ps).most_common(1)[0][0]].append(s)
r = random.Random(2026); fit, test = [], []; k = 0
for key in sorted(strat, key=str):
    L = strat[key]; r.shuffle(L)
    for s in L: (fit if k % 2 == 0 else test).append(s); k += 1
json.dump(dict(fit=sorted(fit), test=sorted(test), strata={str(k): v for k, v in strat.items()}), open('../split.json', 'w'), indent=0)
pf = sum(len(sh[s]) for s in fit); pt = sum(len(sh[s]) for s in test)
print(len(fit), len(test), 'sheets;', pf, pt, 'pages;', sum(p['nwords'] for s in fit for p in sh[s]), sum(p['nwords'] for s in test for p in sh[s]), 'words')
