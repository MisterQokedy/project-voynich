# Interpolated back-off letter LM (4-gram down to unigram), for D6-V2 addendum attempt 4.
import numpy as np
def lm4_backoff(text, SYM, lam=(0.5, 0.25, 0.15, 0.1)):
    NS = len(SYM); ids = np.array([SYM.index(c) for c in text])
    u = np.bincount(ids, minlength=NS) + 1.0; u /= u.sum()
    B = np.zeros((NS, NS)); np.add.at(B, (ids[:-1], ids[1:]), 1); B2 = (B + 1e-9) / (B.sum(-1, keepdims=True) + 1e-9 * NS)
    T3 = np.zeros((NS,) * 3); np.add.at(T3, (ids[:-2], ids[1:-1], ids[2:]), 1); T3 = (T3 + 1e-9) / (T3.sum(-1, keepdims=True) + 1e-9 * NS)
    Q = np.zeros((NS,) * 4); np.add.at(Q, (ids[:-3], ids[1:-2], ids[2:-1], ids[3:]), 1); Q = (Q + 1e-9) / (Q.sum(-1, keepdims=True) + 1e-9 * NS)
    P = lam[0] * Q + lam[1] * T3[None] + lam[2] * B2[None, None] + lam[3] * u[None, None, None]
    return np.log2(P)
