"""S6-Z per-group search. argv: ntrials worker stage(json name of STAGES) ; env S6Z_RUN, S6Z_GRP, S6Z_TAG."""
import sys, json, os
_argv = list(sys.argv)
exec(open('./work/s6z/code/basez.py').read())
import optuna
from optuna.storages import JournalStorage
from optuna.storages.journal import JournalFileBackend, JournalFileOpenLock
STAGES = json.loads(os.environ['S6Z_STAGES'])
ntr, wid = int(_argv[1]), int(_argv[2]); TAG = os.environ['S6Z_TAG']
WD = f'/tmp/s6z/{TAG}/{_RUN}_{_GRP}'; os.makedirs(WD, exist_ok=True); p = f'{WD}/study.log'
st = optuna.create_study(study_name="Z", storage=JournalStorage(JournalFileBackend(p, lock_obj=JournalFileOpenLock(p))), load_if_exists=True, sampler=optuna.samplers.TPESampler(seed=2600 + int(os.environ.get("S6Z_SEEDOFF", 0)) + wid, n_startup_trials=10))
if wid == 0: st.enqueue_trial({k: min(max(PQ.get(k, a), a), b) for k, (a, b) in STAGES.items()})
optuna.logging.set_verbosity(optuna.logging.WARNING)
def obj(t):
    prm = dict(PQ)
    for k, (a, b) in STAGES.items(): prm[k] = t.suggest_float(k, a, b)
    g = gen12(FITSH, PEF, prm, 1); ok, L, *_ = loss_y(g)
    t.set_user_attr('n', int(sum(ok.values()))); return float(L)
st.optimize(obj, n_trials=ntr)
