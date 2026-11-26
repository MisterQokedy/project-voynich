"""Summarise calib.py outputs into a markdown table. Usage: summ.py out.md c_*.json"""
import json, sys, math
import numpy as np
rows = []
for f in sys.argv[2:]:
    J = json.load(open(f)); N = math.factorial(J['n'])
    for t, R in J['results'].items():
        for m, L in R['metrics'].items():
            if not L: continue
            rk = np.array([r['rank_true'] for r in L]); ps = np.array([r['p_null'] for r in L if 'p_null' in r])
            rows.append(dict(shape=f"{'Q20' if J['n']==6 else 'Q13'}-like (W={J['W']}, {J['n']} sheets)", mode=J['mode'] + ('-scrambled' if J['scrambled'] else ''),
                text=t, metric=m, win=len(L), ind=R['independent'], top1=np.mean([r['top1'] for r in L]), medrank=np.median(rk), N=N,
                top5=np.mean(rk <= 0.05 * N), links=np.mean([r['links'] for r in L]), chance_links=1 / J['n'],
                p06=np.mean(ps < 0.06) if len(ps) else float('nan'), p05=np.mean(ps < 0.05) if len(ps) else float('nan'), ps=ps.tolist()))
json.dump(rows, open(sys.argv[1].replace('.md', '.json'), 'w'))
out = []
for shape in sorted({r['shape'] for r in rows}):
    for mode in ['run', 'aligned', 'run-scrambled', 'aligned-scrambled']:
        R = [r for r in rows if r['shape'] == shape and r['mode'] == mode]
        if not R: continue
        out.append(f"\n### {shape}, pages: {mode}\n\n| text | metric | windows (indep.) | best order = true | median rank of true / {R[0]['N']} | true in top 5% | true links kept (chance {R[0]['chance_links']:.2f}) | null p<0.06 | null p<0.05 |\n|---|---|---|---|---|---|---|---|---|")
        for r in R:
            out.append(f"| {r['text']} | {r['metric']} | {r['win']} ({r['ind']}) | {r['top1']:.0%} | {r['medrank']:.0f} | {r['top5']:.0%} | {r['links']:.2f} | "
                       + ('–' if math.isnan(r['p06']) else f"{r['p06']:.0%}") + ' | ' + ('–' if math.isnan(r['p05']) else f"{r['p05']:.0%}") + ' |')
open(sys.argv[1], 'w').write('\n'.join(out))
