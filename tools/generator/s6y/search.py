import sys, json, os
_argv = list(sys.argv)
exec(open('./work/s6y/code/base.py').read())
import optuna
from optuna.storages import JournalStorage
from optuna.storages.journal import JournalFileBackend, JournalFileOpenLock
ntr, wid = int(_argv[1]), int(_argv[2]); WD = f'/tmp/s6y/{_RUN}'; os.makedirs(WD, exist_ok=True); p = f'{WD}/study_Y.log'
st = optuna.create_study(study_name="Y", storage=JournalStorage(JournalFileBackend(p, lock_obj=JournalFileOpenLock(p))), load_if_exists=True, sampler=optuna.samplers.TPESampler(seed=1600 + wid, n_startup_trials=12))
if wid == 0: st.enqueue_trial(dict(bD=0.0, bW=PQ['bW'], bR=PQ['bR'], bJ=PQ['bJ']))
optuna.logging.set_verbosity(optuna.logging.WARNING)
def obj(t):
    prm = dict(PQ)
    for k, (a, b) in STAGES.items(): prm[k] = t.suggest_float(k, a, b)
    g = gen12(FITSH, PEF, prm, 1); ok, L, x, v, w = loss_y(g)
    t.set_user_attr('n', int(sum(ok.values()))); return float(L)
st.optimize(obj, n_trials=ntr)
