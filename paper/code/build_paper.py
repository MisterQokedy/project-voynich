# Builds the appendices from master_results_table.csv and renders paper.pdf (pandoc + WeasyPrint).
import csv, re, html, subprocess, sys, os
P='./work/paper/'; S=P+'src/'
rows=list(csv.DictReader(open(P+'master_results_table.csv')))
def clean(t,n=None):
    t=re.sub(r'\|[-\s|]*\|',' ',t); t=t.replace('|',' · ').replace('**','').replace('`','')
    t=re.sub(r'\s+',' ',t).strip()
    if n and len(t)>n: t=t[:n].rsplit(' ',1)[0]+' …'
    return html.escape(t)
out=['\n# Appendix A: test register {.appendix .unnumbered}\n',
 f'All {len(rows)} test entries in the consolidated findings, one row per test, in the order recorded. "Pre" marks pre-registered tests. Verdicts are quoted from each entry, or written by hand where an entry had none. The machine-readable table is `master_results_table.csv`.\n',
 '<table class="reg"><thead><tr><th>ID</th><th>Theme</th><th>Test</th><th>Pre</th><th>Verdict</th></tr></thead><tbody>']
for r in rows:
    out.append(f"<tr><td>{clean(r['id'])}</td><td>{clean(r['theme'])}</td><td>{clean(r['title'],140)}</td><td>{'yes' if r['prereg'] else ''}</td><td>{clean(r['verdict'])}</td></tr>")
out.append('</tbody></table>\n')
out+=['\n# Appendix B: pre-registrations {.appendix .unnumbered}\n',
 f"{sum(1 for r in rows if r['prereg'])} of {len(rows)} tests were pre-registered: the decision rule, bands and controls were written to a `PREREG.md` file in the test's folder before the data were examined. The list below gives each pre-registered test and its folder in the repository's results archive.\n",
 '<table class="reg"><thead><tr><th>ID</th><th>Test</th><th>Folder</th></tr></thead><tbody>']
for r in rows:
    if r['prereg']: out.append(f"<tr><td>{clean(r['id'])}</td><td>{clean(r['title'],120)}</td><td>{clean(r['files'],60)}</td></tr>")
out.append('</tbody></table>\n')
out+=['\n# Appendix C: methods and numbers by test {.appendix .unnumbered}\n',
 '![P3-d, illustration only: mean segmenter masks for line-edge and mid-line glyphs. Red marks more ink at the line edge, blue more ink mid-line. Band-fit error at line ends partly confounds these means, so they are not evidence. Derived from images of MS 408, Beinecke Rare Book and Manuscript Library, Yale University.](../figures/fig9_p3d_line_edge_masks.png){width=48%}\n',
 'Each entry gives the test, its verdict, its controls and an excerpt of the recorded result. Full write-ups, code and outputs are in the folders named in Appendix B.\n']
order={};[order.setdefault(r['theme'],len(order)) for r in rows]
th=None
for r in sorted(rows,key=lambda r:order[r['theme']]):
    if r['theme']!=th: th=r['theme']; out.append(f'\n## {clean(th)} {{.unnumbered}}\n')
    out.append(f"<div class='entry'><p><b>{clean(r['id'])}. {clean(r['title'],200)}</b> <span class='v'>{clean(r['verdict'])}</span></p>"
               f"<p>{clean(r['summary'],520)}</p>" + (f"<p class='c'>Controls: {clean(r['controls'],260)}</p>" if r['controls'].strip() else '') + "</div>")
out+=['\n# Appendix D: code and data availability {.appendix .unnumbered}\n', open(S+'availability.md').read()]
out+=['\n', open(S+'appendix_e.md').read()]
open(S+'appendix.md','w').write('\n'.join(out))
os.chdir(S)
subprocess.run(['pandoc','paper.md','appendix.md','-s','--toc','--toc-depth=1','-N','--css','paper.css','--metadata','toc-title=Contents','-B','titlepage.html','-o','paper.html'],check=True)
import weasyprint; weasyprint.HTML('paper.html',base_url=S).write_pdf(P+'paper.pdf')
print('ok')
