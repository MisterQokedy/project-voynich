# D3b (first/last glyph as context classes beyond adjacency) and D2a (order-specific slot dependencies). See ../PREREG.md
import sys, json, math, random, collections, numpy as np
exec(open('./work/meaning_procedure/code/texts.py').read())
C = collections.Counter
def pairs(P, sp):
    out = []
    for pi, p in enumerate(P):
        for l in p:
            for a, b in zip(l, l[1:]):
                ga, gb = sp(a), sp(b); out.append((pi, a, b, ga[0], ga[-1], gb[0], gb[-1]))
    return out
def ce_table(trainXY, k_ctx=None):
    pass
def d3b(F, T, sp, k=5, nperm=200, seed=1):
    PF, PT = pairs(F, sp), pairs(T, sp); res = {}
    # ---- G_left: predict F(b) from a vs from L(a)
    for side in ('left', 'right', 'left_g', 'right_g'):
        if side.startswith('left'):
            tgt = lambda x: x[5]; adj = lambda x: x[4]; ctx = (lambda x: x[1]) if side == 'left' else (lambda x: (x[4], x[3]))
        else:
            tgt = lambda x: x[4]; adj = lambda x: x[5]; ctx = (lambda x: x[2]) if side == 'right' else (lambda x: (x[5], x[6]))
        Y = sorted({tgt(x) for x in PF} | {tgt(x) for x in PT}); yi = {y: i for i, y in enumerate(Y)}; nY = len(Y)
        A = C(adj(x) for x in PF); AY = collections.defaultdict(C)
        for x in PF: AY[adj(x)][tgt(x)] += 1
        uni = C(tgt(x) for x in PF); N = len(PF)
        pu = np.array([(uni[y] + 0.5) / (N + 0.5 * nY) for y in Y])
        adjs = sorted({adj(x) for x in PF} | {adj(x) for x in PT}); ai = {a: i for i, a in enumerate(adjs)}
        PA = np.array([[(AY[a][y] + 1.0 * pu[j] * 5) / (A[a] + 5) for j, y in enumerate(Y)] for a in adjs])  # adjacency model, backs off to unigram
        WC = C(ctx(x) for x in PF); WY = collections.defaultdict(C)
        for x in PF: WY[ctx(x)][tgt(x)] += 1
        ctxs = [w for w in WC if WC[w] >= 5]; ci = {w: i for i, w in enumerate(ctxs)}
        # the context determines its own adjacent glyph (a fixes L(a); b fixes F(b); glyph contexts include it), so P(y | ctx) is one row per context
        t_y = np.array([yi[tgt(x)] for x in PT]); t_a = np.array([ai[adj(x)] for x in PT]); pg = np.array([x[0] for x in PT])
        base = -np.log2(PA[t_a, t_y])
        ctx_adj = {}
        for x in PF + PT: ctx_adj.setdefault(ctx(x), ai[adj(x)])
        PW = np.array([(np.array([WY[w][y] for y in Y], float) + k * PA[ctx_adj[w]]) / (WC[w] + k) for w in ctxs]) if ctxs else np.zeros((0, nY))
        LPW = -np.log2(PW) if len(ctxs) else PW
        t_c = np.array([ci.get(ctx(x), -1) for x in PT])
        def ce_of(c): return np.where(c >= 0, LPW[np.maximum(c, 0), t_y] if len(ctxs) else base, base)
        G = float(base.mean() - ce_of(t_c).mean())
        rng = np.random.default_rng(seed); grp = collections.defaultdict(list)
        for i in range(len(PT)): grp[(pg[i], t_a[i])].append(i)
        grp = [np.array(v) for v in grp.values() if len(v) > 1]; nulls = []
        for _ in range(nperm):
            c = t_c.copy()
            for idx in grp: c[idx] = t_c[rng.permutation(idx)]
            nulls.append(float(base.mean() - ce_of(c).mean()))
        res[side] = dict(G=G, rel=G / float(base.mean()), base=float(base.mean()), null99=float(np.percentile(nulls, 99)), null_mean=float(np.mean(nulls)),
                         p=float((1 + sum(n >= G for n in nulls)) / (1 + nperm)), npairs=len(PT))
    return res
# ---------------- D2a ----------------
def slot_seqs(P, sp, en):
    return [[(sp(w)[0], en(w)) for w in l] for p in P for l in p if l]
class Seq:
    """Flattened slot sequence: on/en integer codes, line ids; shuffles within lines are vectorised."""
    def __init__(self, S, vocab):
        self.on = np.array([vocab['on'].setdefault(s[0], len(vocab['on'])) for l in S for s in l]); self.en = np.array([vocab['en'].setdefault(s[1], len(vocab['en'])) for l in S for s in l])
        self.line = np.concatenate([np.full(len(l), i) for i, l in enumerate(S)]) if S else np.zeros(0, int)
    def shuffled(self, rng):
        o = np.lexsort((rng.random(len(self.line)), self.line)); n = Seq.__new__(Seq); n.on = self.on[o]; n.en = self.en[o]; n.line = self.line; return n
    def pairs(self, d, fx, fy):
        ok = self.line[d:] == self.line[:-d]; X = getattr(self, fx)[:-d][ok]; Y = getattr(self, fy)[d:][ok]; return X, Y
def dep_gain(FS, TS, d, fx, fy, nx, ny):
    Xf, Yf = FS.pairs(d, fx, fy); Xt, Yt = TS.pairs(d, fx, fy)
    J = np.zeros((nx, ny)); np.add.at(J, (Xf, Yf), 1); Xc = J.sum(1); Yc = J.sum(0); seen = Yc > 0; nY = seen.sum() + 1; N = Yc.sum()
    unk = ~seen[Yt]
    p0 = np.where(unk, 0.5, Yc[Yt] + 0.5) / (N + 0.5 * nY)
    p1 = np.where(unk, 0.5, J[Xt, Yt] + 0.5) / (Xc[Xt] + 0.5 * nY); p1 = np.where(Xc[Xt] > 0, p1, p0)
    return float((np.log2(p1) - np.log2(p0)).mean())
DEPS = {'A1_end_end_d1': (1, 'en', 'en'), 'A3_end_end_d2': (2, 'en', 'en'), 'A4_on_on_d2': (2, 'on', 'on'), 'A5_end_on_d2': (2, 'en', 'on')}
def d2a(F, T, sp, en, nperm=200, nsh=20, seed=2):
    voc = {'on': {}, 'en': {}}; FS, TS = Seq(slot_seqs(F, sp, en), voc), Seq(slot_seqs(T, sp, en), voc); rng = np.random.default_rng(seed); res = {}
    nx = {'on': len(voc['on']), 'en': len(voc['en'])}
    for name, (d, fx, fy) in DEPS.items():
        g = dep_gain(FS, TS, d, fx, fy, nx[fx], nx[fy])
        sh = [dep_gain(FS.shuffled(rng), TS.shuffled(rng), d, fx, fy, nx[fx], nx[fy]) for _ in range(nsh)]
        nl = [dep_gain(FS, TS.shuffled(rng), d, fx, fy, nx[fx], nx[fy]) for _ in range(nperm)]
        res[name] = dict(gain=g, order_specific=g - float(np.mean(sh)), shuf_mean=float(np.mean(sh)), p=float((1 + sum(x >= g for x in nl)) / (1 + nperm)), null99=float(np.percentile(nl, 99)))
    # descriptive: slot -> line position
    def pos_tokens(P):
        out = []
        for p in P:
            for l in p:
                for i, w in enumerate(l):
                    out.append(((sp(w)[0], en(w)), 'I' if i == 0 else 'F' if i == len(l) - 1 else 'M', len(sp(w))))
        return out
    pf, pt = pos_tokens(F), pos_tokens(T)
    def pos_gain(f):
        XY = C((f(t), t[1]) for t in pf); X = C(f(t) for t in pf); Y = C(t[1] for t in pf); N = len(pf); ce0 = ce1 = 0
        for t in pt:
            x, y = f(t), t[1]; p0 = (Y[y] + 0.5) / (N + 1.5); p1 = (XY[(x, y)] + 0.5) / (X[x] + 1.5) if X[x] else p0; ce0 -= math.log2(p0); ce1 -= math.log2(p1)
        return (ce0 - ce1) / len(pt)
    for nm, f in (('onset', lambda t: t[0][0]), ('ending', lambda t: t[0][1]), ('length', lambda t: min(t[2], 9))): res['pos_' + nm] = pos_gain(f)
    return res
if __name__ == '__main__':
    S = load_all(); OUT = {}
    only = sys.argv[1:]
    for name, (F, T, sp, en) in S.items():
        if only and not any(name.startswith(o) for o in only): continue
        r3 = d3b(F, T, sp); r2 = d2a(F, T, sp, en); OUT[name] = dict(d3b=r3, d2a=r2)
        print(f'{name:22} D3b ' + '  '.join(f'{s} {r3[s]["G"]:+.4f} (null99 {r3[s]["null99"]:+.4f}, p {r3[s]["p"]:.3f}, rel {r3[s]["rel"]:.3f})' for s in r3), flush=True)
        print(f'{"":22} D2a ' + '  '.join(f'{s} os {r2[s]["order_specific"]:+.4f} (g {r2[s]["gain"]:.4f}, p {r2[s]["p"]:.3f})' for s in DEPS) + f'  pos on {r2["pos_onset"]:.3f} end {r2["pos_ending"]:.3f} len {r2["pos_length"]:.3f}', flush=True)
        json.dump(OUT, open('./work/meaning_procedure/d3b_d2a' + ('_' + '_'.join(only) if only else '') + '.json', 'w'), indent=1)
