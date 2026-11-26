"""One-off statistics for Z2-b (S27, S28), same definitions as gapdiag/g4: S27 = share of tokens that occur once in the text;
S28 = share of those one-offs within one edit (or equal length+-1 edit) of a word among the previous 40 tokens on the same page."""
import collections
def _ed1(a, b):
    if a == b: return True
    la, lb = len(a), len(b)
    if abs(la - lb) > 1: return False
    if la == lb: return sum(x != y for x, y in zip(a, b)) == 1
    if la > lb: a, b, la, lb = b, a, lb, la
    i = 0
    while i < la and a[i] == b[i]: i += 1
    return a[i:] == b[i + 1:]
def oneoff(P):
    pages = [[w for l in p for w in l] for p in P]; T = [w for p in pages for w in p]; c = collections.Counter(T)
    hap = [(pi, i, w) for pi, p in enumerate(pages) for i, w in enumerate(p) if c[w] == 1]
    if not hap: return {'S27': 0.0, 'S28': 0.0}
    nl = sum(any(_ed1(w, x) for x in pages[pi][max(0, i - 40):i] if abs(len(x) - len(w)) <= 1) for pi, i, w in hap)
    return {'S27': len(hap) / len(T), 'S28': nl / len(hap)}
