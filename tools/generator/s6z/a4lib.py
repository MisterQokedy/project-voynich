"""A4 (onset -> onset two words on, order-specific, FIT model -> TEST, minus within-line shuffle) as in meaning_procedure/code/a4g.py; standalone copy for S6-Z (Z5 / A4-P full re-search)."""
import re as _re4, numpy as np
_GL4 = _re4.compile(r'cth|ckh|cph|cfh|ch|sh|.')
def gg(w): return _GL4.findall(w)
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
import re as _re
ENDR = _re.compile(r'(aiin|ain|iin|eedy|edy|dy|eey|ey|ol|or|ar|al|am|y|s|r|l|n|m)$')
def v_end(w):
    g = gg(w); rest = ''.join(g[1:]); m = ENDR.search(rest); return m.group(1) if m else ('-' + (g[-1] if len(g) == 1 else ''))
def A4(F, T, rng, nsh=20):
    F = [[l for l in p if l] for p in F]; T = [[l for l in p if l] for p in T]
    voc = {'on': {}, 'en': {}}; FS, TS = Seq(slot_seqs(F, gg, v_end), voc), Seq(slot_seqs(T, gg, v_end), voc); nx = len(voc['on'])
    g = dep_gain(FS, TS, 2, 'on', 'on', nx, nx); sh = np.mean([dep_gain(FS.shuffled(rng), TS.shuffled(rng), 2, 'on', 'on', nx, nx) for _ in range(nsh)]); return float(g - sh)
def internal(P):
    A = [p for i, p in enumerate(P) if (i // 4) % 2 == 0]; B = [p for i, p in enumerate(P) if (i // 4) % 2 == 1]; return A, B
