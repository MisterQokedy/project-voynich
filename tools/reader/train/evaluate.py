"""Score bundle-7 models on the 36 held-out pages. Writes results.json and RESULTS_SUMMARY.md."""
import argparse, json, math, sys, collections
from pathlib import Path
import numpy as np
import torch
from PIL import Image
sys.path.insert(0, str(Path(__file__).parent))
import common as C

VLM_CER = 0.607   # Qwen2.5-VL-3B through Jan, same 36 test pages (RESULTS_VLM.md)


class Reader:
    def __init__(self, path, device):
        from kraken.models import load_models
        from kraken.lib.dataset import ImageInputTransforms
        self.net = load_models(path)[0]; self.net.eval().to(device); self.dev = device
        b, c, h, w = self.net.input
        self.tf = ImageInputTransforms(1, h, w, c, (16, 0), valid_norm=True)
        self.codec = self.net.codec

    @torch.inference_mode()
    def probs(self, img_path):
        x = self.tf(Image.open(img_path)).unsqueeze(0).to(self.dev)
        logits, olens = self.net.nn(x, torch.LongTensor([x.shape[3]]))
        return logits.softmax(1).squeeze(2)[0, :, :int(olens[0])].float().cpu().numpy()   # (C, W)

    def greedy(self, P):
        from kraken.lib.ctc_decoder import greedy_decoder
        return ''.join(c for c, *_ in self.codec.decode(greedy_decoder(torch.as_tensor(P))[0]))


# ---------- side ablation: char n-gram LM + CTC prefix beam search (never used in the main result) ----------
class CharLM:
    def __init__(self, lines, n=6):
        self.n = n; self.c = [collections.defaultdict(collections.Counter) for _ in range(n)]
        self.V = sorted(set(''.join(lines)) | {'\n'})
        for l in lines:
            s = '\x02' * (n - 1) + l + '\n'
            for i in range(n - 1, len(s)):
                for k in range(n):
                    self.c[k][s[i - k:i]][s[i]] += 1
        self.cache = {}

    def logp(self, hist, ch):
        h = ('\x02' * (self.n - 1) + hist)[-(self.n - 1):]
        key = (h, ch)
        if key in self.cache:
            return self.cache[key]
        p = 1.0 / len(self.V)
        for k in range(self.n):          # interpolated Witten-Bell, low to high order
            ctx = h[len(h) - k:] if k else ''
            cnt = self.c[k].get(ctx)
            if not cnt:
                continue
            tot = sum(cnt.values()); typ = len(cnt); lam = tot / (tot + typ)
            p = lam * cnt[ch] / tot + (1 - lam) * p
        v = math.log(max(p, 1e-12)); self.cache[key] = v
        return v


def beam_decode(P, l2c, lm, alpha, beta, beam=12, prune=1e-3):
    """P: (C, W) softmax, class 0 = blank. l2c: class -> char."""
    beams = {'': (0.0, -1e30)}   # prefix -> (log p ending in blank, log p ending in non-blank)
    lse = np.logaddexp
    for t in range(P.shape[1]):
        col = P[:, t]; cand = [k for k in np.where(col > prune)[0]]
        nb = collections.defaultdict(lambda: [-1e30, -1e30])
        for pre, (pb, pnb) in beams.items():
            tot = lse(pb, pnb)
            for k in cand:
                lp = math.log(col[k])
                if k == 0:
                    nb[pre][0] = lse(nb[pre][0], tot + lp); continue
                ch = l2c.get(int(k))
                if ch is None:
                    continue
                last = pre[-1:]
                new = pre + ch
                lmw = alpha * lm.logp(pre, ch) + beta
                if ch == last:
                    nb[new][1] = lse(nb[new][1], pb + lp + lmw)
                    nb[pre][1] = lse(nb[pre][1], pnb + lp)
                else:
                    nb[new][1] = lse(nb[new][1], tot + lp + lmw)
        beams = dict(sorted(((k, tuple(v)) for k, v in nb.items()), key=lambda kv: -lse(*kv[1]))[:beam])
    return max(beams.items(), key=lambda kv: lse(*kv[1]))[0]


def page_cer(hyp_rows, ref):
    hyp = '\n'.join(hyp_rows)
    return C.lev(hyp, ref) / max(len(ref), 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--work', required=True); ap.add_argument('--out', required=True)
    ap.add_argument('--device', default='cuda:0'); ap.add_argument('--lm', action='store_true')
    a = ap.parse_args()
    W = Path(a.work); out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    test = json.load(open(W / 'test.json')); pages = sorted(test)
    sect = {p: test[p]['section'] for p in pages}
    der = C.derange_within(pages, sect)
    models = json.load(open(W / 'models.json'))       # {name: path}
    res = {'pages': pages, 'derangement': der, 'models': {}}
    cache = {}
    for name, path in models.items():
        if not path or not Path(path).exists():
            res['models'][name] = {'status': 'NOT RUN'}; continue
        rd = Reader(path, a.device)
        P = {p: [rd.probs(r) for r in test[p]['rows']] for p in pages}
        cache[name] = (rd, P)
    def score(hyp):  # hyp: {page: [row strings]}
        own = [page_cer(hyp[p], test[p]['ref_zl']) for p in pages]
        shuf_img = [page_cer(hyp[der[p]], test[p]['ref_zl']) for p in pages]   # another page's lines read for this page
        it = [page_cer(hyp[p], test[p]['ref_it']) for p in pages if test[p]['ref_it']]
        lz = [(C.lev(hyp[p][q['row']], q['zl']), len(q['zl'])) for p in pages for q in test[p]['pairs']]
        li = [(C.lev(hyp[p][q['row']], q['it']), len(q['it'])) for p in pages for q in test[p]['pairs'] if q['it']]
        return {'page_cer': C.boot_ci(own), 'page_cer_vals': own,
                'shuffled_image_minus_real': C.paired_boot(shuf_img, own),
                'page_cer_vs_IT': C.boot_ci(it) if it else None,
                'line_cer_zl': sum(e for e, _ in lz) / max(sum(n for _, n in lz), 1),
                'line_cer_it': sum(e for e, _ in li) / max(sum(n for _, n in li), 1), 'n_lines': len(lz)}
    hyps = {}
    for name, (rd, P) in cache.items():
        hyps[name] = {p: [rd.greedy(x) for x in P[p]] for p in pages}
        res['models'][name] = score(hyps[name])
    # ensemble: mean of the three main seeds' frame posteriors (same architecture -> same frame count)
    seeds = [n for n in ('main_s1', 'main_s2', 'main_s3') if n in cache]
    if len(seeds) == 3:
        rd = cache[seeds[0]][0]
        hyps['ensemble3'] = {p: [rd.greedy(np.mean([cache[s][1][p][i] for s in seeds], 0)) for i in range(len(test[p]['rows']))] for p in pages}
        res['models']['ensemble3'] = score(hyps['ensemble3'])
    # side ablation: LM decoding on main_s1 (alpha, beta tuned on validation lines of training pages only)
    if a.lm and 'main_s1' in cache:
        rd, P = cache['main_s1']
        lm = CharLM([l.strip() for l in open(W / 'train_text.txt') if l.strip()])
        l2c = {int(l[0]): c for c, l in rd.codec.c2l.items() if len(l) == 1}
        val = [l.strip() for l in open(W / 'arms' / 'main' / 'val.txt') if l.strip()][:150]
        vP = [rd.probs(v) for v in val]; vR = [Path(v).with_suffix('.gt.txt').read_text().strip() for v in val]
        best = None
        for al in (0.0, 0.3, 0.6, 1.0):
            for be in (0.0, 0.5, 1.0, 2.0):
                e = sum(C.lev(beam_decode(p, l2c, lm, al, be), r) for p, r in zip(vP, vR)) / sum(map(len, vR))
                if best is None or e < best[0]:
                    best = (e, al, be)
        hyps['main_s1_lm'] = {p: [beam_decode(x, l2c, lm, best[1], best[2]) for x in P[p]] for p in pages}
        res['models']['main_s1_lm'] = score(hyps['main_s1_lm']); res['models']['main_s1_lm']['alpha_beta_val'] = best
    res['models_paths'] = models
    json.dump(res, open(out / 'results.json', 'w'), indent=1)
    json.dump(hyps, open(out / 'predictions.json', 'w'))
    summary(res, out, test)


def fmt(t):
    return f'{t[0]:.3f} [{t[1]:.3f}, {t[2]:.3f}]' if t else 'n/a'


def summary(res, out, test):
    M = res['models']; L = []
    L.append(f'# Bundle 7 results: Kraken line reader on {len(res["pages"])} held-out pages\n')
    m = M.get('main_s1', {}); s = M.get('shuflab', {})
    ok = 'page_cer' in m and 'page_cer' in s
    if ok:
        c1 = m['page_cer'][2] < VLM_CER
        c2 = m['shuffled_image_minus_real'][1] > 0
        c3 = C.paired_boot(s['page_cer_vals'], m['page_cer_vals'])
        M['_shuflab_minus_main'] = c3
        verdict = 'PASS' if (c1 and c2 and c3[1] > 0) else 'FAIL'
        L.append(f'**Verdict (PREREG): {verdict}**\n')
        L.append(f'- P1 page CER of main model {fmt(m["page_cer"])} vs VLM 0.607: {"met" if c1 else "NOT met"}')
        L.append(f'- P2 shuffled image minus real {fmt(m["shuffled_image_minus_real"])}: {"met" if c2 else "NOT met"}')
        L.append(f'- P3 shuffled-label model minus main {fmt(c3)}: {"met" if c3[1] > 0 else "NOT met"}\n')
    else:
        L.append('**Verdict: INCOMPLETE** (main or shuffled-label model missing)\n')
    L.append('| Model | Page CER vs ZL [95% CI] | Shuffled image − real | Page CER vs IT | Line CER ZL / IT (paired lines) |')
    L.append('|---|---|---|---|---|')
    for k, v in M.items():
        if k.startswith('_'):
            continue
        if 'page_cer' not in v:
            L.append(f'| {k} | {v.get("status", "?")} | | | |'); continue
        L.append(f'| {k} | {fmt(v["page_cer"])} | {fmt(v["shuffled_image_minus_real"])} | {fmt(v["page_cer_vs_IT"])} | '
                 f'{v["line_cer_zl"]:.3f} / {v["line_cer_it"]:.3f} (n={v["n_lines"]}) |')
    if ok:
        L.append('\n## Ablations (paired page bootstrap, model − main_s1; negative = better)')
        for k in ('noaug', 'synth', 'twolab', 'ensemble3', 'main_s1_lm'):
            if k in M and 'page_cer_vals' in M[k]:
                d = C.paired_boot(M[k]['page_cer_vals'], m['page_cer_vals'])
                tag = 'better' if d[2] < 0 else ('worse' if d[1] > 0 else 'no clear difference')
                L.append(f'- {k}: {fmt(d)} → {tag}')
        seeds = [M[n]['page_cer'][0] for n in ('main_s1', 'main_s2', 'main_s3') if 'page_cer' in M.get(n, {})]
        if seeds:
            L.append(f'- seed spread of main model (page CER): {", ".join(f"{x:.3f}" for x in seeds)}')
    L.append(f'\nTest pages scored: {len(res["pages"])}. Paired test lines: {sum(len(test[p]["pairs"]) for p in res["pages"])}.')
    (out / 'RESULTS_SUMMARY.md').write_text('\n'.join(L) + '\n')
    print('\n'.join(L))


if __name__ == '__main__':
    main()
