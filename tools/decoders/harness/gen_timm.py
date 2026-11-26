"""Generate fitted-Timm text (unmodified jar, fit.json params) for 3 seeds, saved per page slot. Output: ../timm_pages.json"""
import sys, json
sys.path.insert(0, './work/timm_generator/code')
from common import *
FIT = json.load(open('./work/timm_generator/fit.json'))
out = {s: to_slots(run_timm('A', FIT['A']['best'], s), run_timm('B', FIT['B']['best'], s)) for s in (2001, 2002, 2003)}
json.dump(out, open('./work/decipherment_harness/timm_pages.json', 'w'))
print({s: sum(len(l) for p in v for l in p) for s, v in out.items()})
