"""Shared helpers: data, split, running Timm's jar, mapping generated pages to slots."""
import json, os, sys, subprocess, tempfile, collections
sys.path.insert(0, './work/language_test/code')
from stats import stats
JAR = '/home/user/torstentimm/selfcitationtextgenerator/executable/text-generator.jar'
BASECONF = '/home/user/torstentimm/selfcitationtextgenerator/executable/conf.properties'
D = json.load(open('./work/manuscript_wide/pages2.json'))
SP = json.load(open('./work/timm_generator/split.json'))
SHEET = [p['Q'] + p['B'] for p in D]
LANG = ['A' if p.get('L') == 'A' else 'B' for p in D]          # unlabelled pages go to the B run
HALF = ['fit' if s in SP['fit'] else 'test' for s in SHEET]
VLINES = [[L['w'] for L in p['lines'] if L['w'] and L['u'] != 'L'] for p in D]   # running text, no labels
def idx(lang=None, half=None): return [i for i in range(len(D)) if (lang is None or LANG[i] == lang) and (half is None or HALF[i] == half)]
def shape(lang):
    I = idx(lang, 'fit'); nl = [len(VLINES[i]) for i in I]
    ch = [len(' '.join(l)) for i in I for l in VLINES[i]]
    first = next(' '.join(VLINES[i][0]) for i in I if VLINES[i] and len(VLINES[i][0]) >= 6)
    return dict(lpp=max(2, round(sum(nl) / len(nl))), llen=max(41, round(sorted(ch)[len(ch) * 3 // 4])), seedline=first)
SHAPE = {L: shape(L) for L in 'AB'}
DEFAULTS = dict(same_pos=28, add_remove=20, combine_split=30, replace=50, reuse_last=10, sugg=40, max_rep=3, dismiss=30, chooser='page', canfollow='curveline', err=0, finalsub='true', sm='top', ip=20, op=25, dp=25)
def run_timm(lang, prm, seed):
    """Run Timm's unmodified jar; return list of pages (lists of lines of words)."""
    sh = SHAPE[lang]; need = sum(len(VLINES[i]) for i in idx(lang)) + 3 * sh['lpp']
    conf = open(BASECONF).read().splitlines(); rep = {
        'text.lines_to_create': need, 'text.max_line_length': sh['llen'], 'text.lines_per_page': sh['lpp'],
        'text.initial_line': sh['seedline'], 'method.random.pseudo.seed': seed, 'text.max_repeat_count': prm['max_rep'],
        'method.sourceChooser': prm['chooser'], 'method.sourceChooser.same_position_probability': prm['same_pos'],
        'method.morph.add_remove.probability': prm['add_remove'], 'method.morph.combine_split.probability': prm['combine_split'],
        'method.morph.replace.probability': prm['replace'], 'method.morph.reuse_last.probability': prm['reuse_last'],
        'method.suggestions.probability': prm['sugg'], 'method.morph.combined.dismiss_as_source_probability': prm['dismiss'],
        'method.canFollow': prm.get('canfollow', 'curveline'), 'method.canFollow.error_rate': prm.get('err', 0),
        'method.morph.use_word_final_substitutions': prm.get('finalsub', 'true'), 'method.suggestions': prm.get('sm', 'top'),
        'method.suggestions.iType_min_percentage': prm.get('ip', 20), 'method.suggestions.olType_min_percentage': prm.get('op', 25),
        'method.suggestions.dyType_min_percentage': prm.get('dp', 25),
        'save.path': './generate/', 'save.filename': 'out.txt'}
    out = [f'{k.split("=")[0]}={rep[k.split("=")[0]]}' if '=' in k and k.split('=')[0] in rep else k for k in conf]
    with tempfile.TemporaryDirectory() as d:
        os.makedirs(d + '/generate'); open(d + '/conf.properties', 'w').write('\n'.join(out) + '\n')
        subprocess.run(['java', '-jar', JAR], cwd=d, check=True, capture_output=True, timeout=600)
        lines = [l.split() for l in open(d + '/generate/out.txt') if not l.startswith('#') and l.strip()]
    lines = lines[:need]
    return [lines[k:k + sh['lpp']] for k in range(0, len(lines), sh['lpp'])]
def to_slots(genA, genB):
    """Generated pages fill A slots / B slots in binding order. Returns per-slot list of lines."""
    it = {'A': iter(genA), 'B': iter(genB)}
    return [next(it[LANG[i]]) for i in range(len(D))]
STATS = ['S1_h2', 'S2_meanlen', 'S3_sdlen', 'S4_zipf', 'S5_types', 'S6_orderMI', 'S8_nearcopy', 'S9_localrep', 'S10_immrep']
def st(pages, seed=1):
    import random
    pages = [p for p in pages if sum(len(l) for l in p) > 0]; s = stats(pages, random.Random(seed)); return {k: float(s[k]) for k in STATS}
