# D6-C3 multiple-comparison check for the zodiac onset/month hit: 200 shuffled-crib runs (permutation p), and reversed label order (exploratory).
import sys
ARGV = list(sys.argv)
exec(open('./work/meaning_procedure/code/d6c3.py').read().split("\nif __name__ == '__main__':")[0])
ch, cs = ARGV[1], ARGV[2]; cribs = MONTH if cs == 'month' else LATIN
v = zrun(ZLAB, ch, cribs); nl = [zrun(ZLAB, ch, zshuf(cribs, 1000 + i), seed=500 + i) for i in range(200)]
p = (1 + sum(x >= v for x in nl)) / 201
rev = {s: v_[::-1] for s, v_ in ZLAB.items()}; vr = zrun(rev, ch, cribs)
OUT = dict(channel=ch, crib=cs, voynich=v, null200_p99=float(np.percentile(nl, 99)), null200_max=max(nl), p=p, reversed_order=vr)
print(json.dumps(OUT), flush=True); json.dump(OUT, open(f'./work/meaning_procedure/d6c3_mc_{ch}_{cs}.json', 'w'), indent=1)
