# D3c-u ciphertexts (chosen settings from word_identity/d3cu.json) on FIT slots (design half) and TEST slots (held-out half).
exec(open('./work/word_identity/code/d3cu.py').read().split("\nif __name__ == '__main__':")[0])
D = json.load(open('./work/word_identity/d3cu.json')); out = {}
for pname in ('italian_dante', 'mhg_megenberg'):
    b = D[pname]['chosen']; toks = PLAIN[pname]; cut = int(0.6 * len(toks)); des, enc = toks[:cut], toks[cut:]
    cls, cnt = fit_classes(des, 3, random.Random(7)); code, used = build_code_u(cls, cnt, b['alpha'], random.Random(1))
    F, _, _ = encode_u(des, {k: list(v) for k, v in code.items()}, set(used), FI, random.Random(11), b['s'], b['e'], b['u']); F = lines_rules(F, random.Random(12))
    T, dec, _ = encode_u(enc, {k: list(v) for k, v in code.items()}, set(used), TI, random.Random(900), b['s'], b['e'], b['u']); T = lines_rules(T, random.Random(950))
    out['d3cu_' + pname] = dict(FIT=F, TEST=T); print(pname, b['alpha'], b['s'], b['e'], b['u'], 'dec', dec, flush=True)
json.dump(out, open('./work/meaning_procedure/cache/d3cu_cipher.json', 'w'))
