# D2a measures on the D2b constructed-language outputs (does D2a detect a conlang grammar?)
exec(open('./work/meaning_procedure/code/d3b_d2a.py').read().split("\nif __name__ == '__main__':")[0])
D = json.load(open('./work/meaning_procedure/cache/d2b_pages.json')); OUT = {}
for k, v in D.items():
    F, T = nonempty(v['FIT']), nonempty(v['TEST']); r = d2a(F, T, gg, v_end, nperm=200); OUT[k] = r
    print(k, {x: round(r[x]['order_specific'], 4) for x in DEPS}, flush=True)
json.dump(OUT, open('./work/meaning_procedure/d2b_detect.json', 'w'), indent=1)
