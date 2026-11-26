# Exploratory (not pre-registered): is the Voynich A4 link (onset of word i -> onset of word i+2) grammar, line position, or repetition?
import sys, re
exec(open('./work/meaning_procedure/code/d3b_d2a.py').read().split("\nif __name__ == '__main__':")[0])
def a4_parts(F, T, sp, en, rng, nsh=20):
    voc = {'on': {}, 'en': {}}; FS, TS = Seq(slot_seqs(F, sp, en), voc), Seq(slot_seqs(T, sp, en), voc); nx = len(voc['on'])
    def interior(S):
        # drop first and last word of each line
        keep = np.ones(len(S.line), bool); st = np.r_[True, S.line[1:] != S.line[:-1]]; en_ = np.r_[S.line[1:] != S.line[:-1], True]; keep &= ~st & ~en_
        n = Seq.__new__(Seq); n.on = S.on[keep]; n.en = S.en[keep]; n.line = S.line[keep]; return n
    out = {}
    for tag, (A, B) in (('all', (FS, TS)), ('interior', (interior(FS), interior(TS)))):
        g = dep_gain(A, B, 2, 'on', 'on', nx, nx); sh = np.mean([dep_gain(A.shuffled(rng), B.shuffled(rng), 2, 'on', 'on', nx, nx) for _ in range(nsh)]); out[tag] = g - sh
    # repetition share: how often on_i == on_{i+2}, real vs within-line shuffled (TEST)
    def rep(S):
        ok = S.line[2:] == S.line[:-2]; return float((S.on[:-2][ok] == S.on[2:][ok]).mean())
    def rep1(S):
        ok = S.line[1:] == S.line[:-1]; return float((S.on[:-1][ok] == S.on[1:][ok]).mean())
    out['rep2'] = rep(TS); out['rep2_shuf'] = float(np.mean([rep(TS.shuffled(rng)) for _ in range(nsh)])); out['rep1'] = rep1(TS); out['rep1_shuf'] = float(np.mean([rep1(TS.shuffled(rng)) for _ in range(nsh)]))
    # gain with the diagonal removed: predict on_{i+2} only on pairs where on_i != on_{i+2} is impossible to condition on; instead recode X as (same-as-target?) -> report A4 on pairs with on_i not equal to on_{i+1}
    return out
if __name__ == '__main__':
    S = load_all(want_lang=True, want_gib=True); rng = np.random.default_rng(3); OUT = {}
    # other transliterations
    exec(open('./work/transcriptions/replicate.py').read().split("r = random.Random(1)")[0].replace("import re, random", "import random"))
    meta = {}
    for line in open('./work/transcriptions/ZL3b-n.txt', errors='ignore'):
        m = re.match(r'<(f\w+)>\s+<!(.*)>', line)
        if m: meta[m.group(1)] = dict(re.findall(r'\$(\w)=(\w+)', m.group(2)))
    for f in ('ZL3b-n.txt', 'IT2a-n.txt', 'RF1b-e.txt'):
        pages = collections.OrderedDict()
        for line in open('./work/transcriptions/' + f, encoding='utf-8', errors='ignore'):
            m = re.match(r'<(f\w+)\.\d+,[@+=*]P\w*>\s+(.*)', line)
            if not m: continue
            t = m.group(2); t = re.sub(r'@\d+;', '?', t); t = re.sub(r'\[([^:\]]*):[^\]]*\]', r'\1', t); t = re.sub(r'<[^>]*>', '', t); t = re.sub(r"[{}']", '', t)
            w = [x for x in re.split(r'[.,]', t) if x and '?' not in x and '*' not in x]
            if w: pages.setdefault(m.group(1), []).append(w)
        keys = list(pages); P = [pages[k] for k in keys]
        # sheet-free split: alternate quire halves by page index pairs (4 pages per block)
        F = [p for i, p in enumerate(P) if (i // 4) % 2 == 0]; T = [p for i, p in enumerate(P) if (i // 4) % 2 == 1]
        OUT[f] = a4_parts(F, T, gg, v_end, rng)
        for lang in 'AB':
            PL = [pages[k] for k in keys if meta.get(k, {}).get('L') == lang]
            F = [p for i, p in enumerate(PL) if (i // 4) % 2 == 0]; T = [p for i, p in enumerate(PL) if (i // 4) % 2 == 1]
            OUT[f + '_' + lang] = a4_parts(F, T, gg, v_end, rng)
        print(f, json.dumps({k: v for k, v in OUT.items() if k.startswith(f)}), flush=True)
    for name, (F, T, sp, en) in S.items():
        OUT[name] = a4_parts(F, T, sp, en, rng); print(name, json.dumps(OUT[name]), flush=True)
    json.dump(OUT, open('./work/meaning_procedure/a4x.json', 'w'), indent=1)
