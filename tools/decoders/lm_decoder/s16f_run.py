"""D1 stage 2 (frozen decoder, PREREG Amendment 1): fit on FIT, decode TEST, for Voynich and controls, per language."""
import os, sys, json, time, random, re
import numpy as np
D = '/tmp/w/d1'; sys.path.insert(0, D); sys.path.insert(0, '/tmp/w/s16e')
import hb
OUTD = os.environ.get('S16F_OUT', '/tmp/w/s16e/s16f')
import metrics, sa_decoder as S

V = json.load(open(os.path.join(D, "voynich.json")))
TP = json.load(open(os.path.join(D, "controls", "timm_pages.json")))["2001"]
GL = S.GL


def gshuf(pages, seed):
    r = random.Random(seed); glyphs = [g for p in pages for l in p for w in l for g in GL.findall(w)]; r.shuffle(glyphs); it = iter(glyphs)
    return [[["".join(next(it) for _ in GL.findall(w)) for w in l] for l in p] for p in pages]


def wshuf(pages, seed):
    r = random.Random(seed); ws = [w for p in pages for l in p for w in l]; r.shuffle(ws); it = iter(ws)
    return [[[next(it) for _ in l] for l in p] for p in pages]


TEXTS = {
    "voynich": (V["fit"], V["test"]),
    "timm": ([TP[i] for i in V["FI"]], [TP[i] for i in V["TI"]]),
    "word_shuffled": (wshuf(V["fit"], 1), wshuf(V["test"], 2)),
    "glyph_shuffled": (gshuf(V["fit"], 3), gshuf(V["test"], 4)),
}
def gibberish():
    """Gaskell & Bowern human gibberish: files alternate into FIT/TEST halves; lines of words, 20 lines per page."""
    import glob
    fs = sorted(glob.glob(os.path.join(D, "controls", "gibberish", "*.txt"))); halves = ([], [])
    for k, f in enumerate(fs):
        for l in open(f, encoding="utf-8", errors="ignore"):
            ws = [re.sub(r"[^a-z]", "", w.lower()) for w in l.split()]; ws = [w for w in ws if w]
            if ws: halves[k % 2].append(ws)
    return [[h[i:i + 20] for i in range(0, len(h), 20)] for h in halves]


def subsample(pages, ntok):
    out, n = [], 0
    for p in pages:
        if n >= ntok: break
        out.append(p); n += sum(len(l) for l in p)
    return out


if os.path.exists(os.path.join(D, "controls", "gibberish")):
    gF, gT = gibberish(); nF = sum(len(l) for p in gF for l in p); nT = sum(len(l) for p in gT for l in p)
    TEXTS["gibberish"] = (gF, gT)
    TEXTS["voynich_small"] = (subsample(V["fit"], nF), subsample(V["test"], nT))   # size-matched to gibberish
LANGS = sys.argv[1].split(",") if len(sys.argv) > 1 else ["latin", "mhg", "occitan", "italian"]
os.makedirs(OUTD, exist_ok=True); st = metrics.Status(os.path.join(OUTD, "status.txt"))
out_path = os.path.join(OUTD, "voynich_results.json")
RES = json.load(open(out_path)) if os.path.exists(out_path) else {}


def run(lang, name, fit, test, C, A, ALPHA, lp):
    t0 = time.time()
    sF = S.strip_nulls(fit); sT = S.strip_nulls(test)
    seg = S.Segmenter(sF); symix = {}
    seq, _ = S.symbols(sF, seg, symix, grow=True); nsym = len(symix); ptr, idx = S.positions(seq, nsym)
    keys, sc = hb.staged(seq, ptr, idx, nsym, lp, A, 4, 64, np.arange(64) + 100, S.freq_init(seq, nsym, C["lm"], ALPHA, 64, 3), 1.0, [1.0], 1000, 3.0, 1.0)
    b = int(np.argmax(sc)); key = keys[b]
    outT = S.decode_units(sT, seg, symix, key, ALPHA); txt = "".join(outT)
    clean = txt.replace("?", "")
    nletters = int((seq >= 0).sum())
    r = dict(nsym=nsym, lexicons={k: len(v) for k, v in seg.cnt.items()}, fit_objective_per_letter=float(sc[b]) / nletters,
             unknown_share_test=txt.count("?") / max(1, len(txt)), M1=metrics.m1(clean, C), M2=metrics.m2(clean, C),
             restart_agreement=float(np.mean([np.mean(k == key) for k in keys])), top8_agreement=float(np.mean([np.mean(keys[t] == key) for t in np.argsort(-sc)[1:8]])), sample=clean[:300], secs=round(time.time() - t0))
    outF = "".join(S.decode_units(sF, seg, symix, key, ALPHA)).replace("?", "")
    r["FIT_M1"] = metrics.m1(outF, C); r["FIT_M2"] = metrics.m2(outF, C)
    if name in ("voynich", "voynich_small"):
        rng = np.random.default_rng(7); f = np.bincount([ALPHA.index(c) for c in C["lm"][:200000] if c in ALPHA], minlength=A); f = f / f.sum()
        m2s = []
        for k in range(100):
            rk = rng.choice(A, size=nsym, p=f)
            m2s.append(metrics.m2("".join(S.decode_units(sT, seg, symix, rk, ALPHA)).replace("?", "")[:8000], C))
        r["random_key_M2_p99"] = float(np.percentile(m2s, 99)); r["random_key_M2_mean"] = float(np.mean(m2s))
        r["words_sample"] = words(clean[:400], C)
    return r


def words(s, C):
    W = set(C["words"]); i = 0; out = []
    while i < len(s):
        for L in range(14, 3, -1):
            if s[i:i + L] in W: out.append(s[i:i + L].upper()); i += L; break
        else: out.append(s[i]); i += 1
    return " ".join(out)


for lang in LANGS:
    C = json.load(open(os.path.join(D, "corpora", lang + ".json"))); ALPHA = metrics.alphabet(C["lm"]); A = len(ALPHA)
    lp = S.ngram_table(C["lm"], ALPHA, n=4)
    truthM1 = metrics.m1("".join(c for c in C["plain"] if c in ALPHA)[:20000], C)
    RES.setdefault(lang, {})["truth_M1"] = truthM1; RES[lang]["M1_bar"] = truthM1 + 0.7
    for name, (fit, test) in TEXTS.items():
        if name in RES[lang]: continue
        st.say(f"D1 Voynich run: {lang} / {name} (fit on FIT, decode TEST)")
        RES[lang][name] = run(lang, name, fit, test, C, A, ALPHA, lp)
        r = RES[lang][name]
        st.say(f"D1 Voynich run: {lang} / {name}: TEST M1 {r['M1']:.2f} (bar {truthM1 + 0.7:.2f}), M2 {r['M2']:.3f}, objective/letter {r['fit_objective_per_letter']:.3f}, {r['secs']}s")
        json.dump(RES, open(out_path, "w"), indent=1)
st.say("DONE D1 Voynich runs")
