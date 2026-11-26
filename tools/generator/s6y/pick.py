import json
exec(open('./work/s6y/code/base.py').read())
import optuna
from optuna.storages import JournalStorage
from optuna.storages.journal import JournalFileBackend, JournalFileOpenLock
WD = f'/tmp/s6y/{_RUN}'; p = f'{WD}/study_Y.log'; OUT = f'./work/s6y/out/{_RUN}'
st = optuna.load_study(study_name="Y", storage=JournalStorage(JournalFileBackend(p, lock_obj=JournalFileOpenLock(p))))
T = sorted([t for t in st.trials if t.value is not None], key=lambda t: t.value)[:10]; best = None; print('trials', len(st.trials))
for t in T:
    prm = dict(PQ, **t.params); L = [loss_y(gen12(FITSH, PEF, prm, s))[1] for s in (11, 12, 13)]; m = sum(L) / 3
    print(t.number, round(t.value, 1), [round(float(x), 1) for x in L], round(m, 1), {k: round(v, 3) for k, v in t.params.items()}, flush=True)
    if best is None or m < best[0]: best = (m, prm, t.number)
print('chosen', best[2], round(best[0], 1), {k: round(best[1][k], 3) for k in STAGES}); json.dump(best[1], open(f'{OUT}/best.json', 'w'), indent=1)
PEALL = [[bool(x) for x in pe] for pe in PE]
for s in range(900, 905): json.dump(gen12(VLINES, PEALL, best[1], s), open(f'{OUT}/gen_S6-Y_{s}.json', 'w'))
print('TEST texts written', flush=True)
