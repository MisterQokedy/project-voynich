import time,json,sys
t=time.time()
sys.path.insert(0,'./work/meaning_procedure/code')
from hybrid import *
print('load',time.time()-t)
P=json.load(open('./work/hybrid_gen/final_test.json'))['params']
for k in INTS: P[k]=int(round(P[k]))
t=time.time(); pages=gen(TESTSH,P,900); print('gen',time.time()-t)
t=time.time(); g,ok,loss=score_on(pages,REF); print('score',time.time()-t, sum(ok.values()), [k for k in ok if not ok[k]])
