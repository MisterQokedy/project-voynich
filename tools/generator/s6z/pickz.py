"""S6-Z pick + TEST generation for one (run, group). env S6Z_TAG; S6Z_NOSEARCH=1 -> use PQ as is."""
import json, os
exec(open('./work/s6z/code/basez.py').read())
TAG = os.environ['S6Z_TAG']; OUT = f'./work/s6z/out/{TAG}/{_RUN}'; os.makedirs(OUT, exist_ok=True)
if os.environ.get('S6Z_NOSEARCH'):
    best = (None, dict(PQ), 'base')
else:
    import optuna
    from optuna.storages import JournalStorage
    from optuna.storages.journal import JournalFileBackend, JournalFileOpenLock
    p = f'/tmp/s6z/{TAG}/{_RUN}_{_GRP}/study.log'
    st = optuna.load_study(study_name="Z", storage=JournalStorage(JournalFileBackend(p, lock_obj=JournalFileOpenLock(p))))
    T = sorted([t for t in st.trials if t.value is not None], key=lambda t: t.value)[:8]; best = None; print('trials', len(st.trials))
    for t in T:
        prm = dict(PQ, **t.params); L = [loss_y(gen12(FITSH, PEF, prm, s))[1] for s in (11, 12, 13)]; m = sum(L) / 3
        print(t.number, round(t.value, 1), [round(float(x), 1) for x in L], round(m, 1), {k: round(v, 3) for k, v in t.params.items()}, flush=True)
        if best is None or m < best[0]: best = (m, prm, t.number)
    print('chosen', best[2], round(best[0], 1))
json.dump(best[1], open(f'{OUT}/best_{_GRP}.json', 'w'), indent=1)
for s in range(900, 905): json.dump({str(k): v for k, v in gen_group(best[1], s).items()}, open(f'{OUT}/part_{_GRP}_{s}.json', 'w'))
print('TEST parts written', flush=True)
