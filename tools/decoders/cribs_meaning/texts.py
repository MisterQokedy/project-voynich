# Shared text sets for D3b and D2a: every text as (FIT pages, TEST pages, glyph splitter, ending function).
import json, random, re, glob, collections, sys
_src = open('./work/target_profile/score.py').read().split("REF = {**vm")[0].replace("ARG = sys.argv[1:]", "ARG = []")
exec(_src)
END = re.compile(r'(aiin|ain|iin|eedy|edy|dy|eey|ey|ol|or|ar|al|am|y|s|r|l|n|m)$')
def v_end(w):
    g = gg(w); rest = ''.join(g[1:]); m = END.search(rest); return m.group(1) if m else ('-' + (g[-1] if len(g) == 1 else ''))
def l_split(w): return list(w)
def l_end(w): return w[-2:] if len(w) >= 3 else w[-1]
def nonempty(P): return [[l for l in p if l] for p in P]
VF = [VLINES[i] for i in FI]; VT = [VLINES[i] for i in TI]
NF = sum(len(l) for p in VF for l in p); NT = sum(len(l) for p in VT for l in p)
def lang_pages(toks, off):
    toks = toks[off:] + toks[:off]
    lines = [toks[i:i + 9] for i in range(0, len(toks) - 9, 9)]
    pages = [lines[i:i + 25] for i in range(0, len(lines), 25)]
    sheets = [pages[i:i + 4] for i in range(0, len(pages), 4)]
    F = [p for s in sheets[0::2] for p in s]; T = [p for s in sheets[1::2] for p in s]
    def cut(P, n):
        out = []; c = 0
        for p in P:
            if c >= n: break
            out.append(p); c += sum(len(l) for l in p)
        return out
    return cut(F, NF), cut(T, NT)
def clean_words(ws):
    out = []
    for w in ws:
        w = ''.join(ch for ch in w.lower() if ch.isalpha())
        if w: out.append(w)
    return out
def load_all(want_lang=True, want_gib=True, want_gen=True):
    S = {'voynich': (VF, VT, gg, v_end)}
    if want_gen:
        T = json.load(open('./work/timm_rules/timm_rules_pages.json'))
        for s in T: S[f'timm_{s}'] = (nonempty([T[s][i] for i in FI]), nonempty([T[s][i] for i in TI]), gg, v_end)
        try:
            P = json.load(open('./work/meaning_procedure/cache/proc_controls.json'))
            for k, v in P.items(): S[k] = (nonempty(v['FIT']), nonempty(v['TEST']), gg, v_end)
        except FileNotFoundError: print('no proc controls yet', file=sys.stderr)
        try:
            D = json.load(open('./work/meaning_procedure/cache/d3cu_cipher.json'))
            for k, v in D.items(): S[k] = (nonempty(v['FIT']), nonempty(v['TEST']), gg, v_end)
        except FileNotFoundError: print('no d3cu yet', file=sys.stderr)
    if want_gib:
        fs = sorted(glob.glob('./work/controls/gibberish/*.txt')); G = []
        for f in fs:
            ls = [clean_words(l.split()) for l in open(f, errors='ignore')]; G.append([l for l in ls if l])
        S['gibberish'] = (G[0::2], G[1::2], l_split, l_end)
    if want_lang:
        SEC = json.load(open('./work/word_identity/texts/sections.json'))
        COR = json.load(open('./work/decipherment_harness/corpora.json'))
        L = {'latin': clean_words(SEC['pliny_garden'] + SEC['pliny_herbal'] + SEC['pliny_waters'] + SEC['pliny_astro']),
             'italian': clean_words(COR['italian']),
             'mhg': clean_words(SEC['meg_herbs'] + SEC['meg_trees'] + SEC['meg_heavens'] + SEC['meg_man'])}
        for k, toks in L.items():
            F, T = lang_pages(toks, 0); S[f'lang_{k}'] = (F, T, l_split, l_end)
    return S
