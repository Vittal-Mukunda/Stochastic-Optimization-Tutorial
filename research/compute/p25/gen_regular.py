"""[experiment] All regular tournaments on n = 2t+1 vertices up to isomorphism, and those with property S_2.

Method.  Vertex 0 beats O = {1..t} and is beaten by R = {t+1..2t}.  Every regular tournament can be relabelled inside O and
inside R so that T[O] and T[R] equal fixed representatives of their isomorphism classes; then the O-R arcs form a 0/1 matrix
with forced margins (o in O beats t - out_O(o) vertices of R; r in R is beaten by 1 + out_R(r) vertices of O).  All such
candidates are enumerated and reduced to a canonical form: colour refinement on out/in colour multisets, then
individualisation of each vertex of the first smallest non-singleton cell, recursively; the canonical form is the
lexicographically least adjacency string over all leaves (an isomorphism invariant, since every step is).
usage: python3 gen_regular.py n outfile"""
import sys, itertools
from collections import Counter

def canon(n, out):
    outl = [sorted(s) for s in out]; inn = [[] for _ in range(n)]
    for v in range(n):
        for w in out[v]: inn[w].append(v)
    def refine(col):
        k = len(set(col))
        while True:
            sig = [(col[v], tuple(sorted(col[w] for w in outl[v])), tuple(sorted(col[w] for w in inn[v]))) for v in range(n)]
            keys = sorted(set(sig)); idx = {s: i for i, s in enumerate(keys)}
            col = [idx[s] for s in sig]
            if len(keys) == k: return col
            k = len(keys)
    best = [None]
    def search(col):
        col = refine(col)
        cnt = Counter(col)
        if len(cnt) == n:
            perm = sorted(range(n), key=lambda v: col[v])
            s = tuple(1 if perm[j] in out[perm[i]] else 0 for i in range(n) for j in range(i + 1, n))
            if best[0] is None or s < best[0]: best[0] = s
            return
        size, c = min((m, c) for c, m in cnt.items() if m > 1)
        for v in [v for v in range(n) if col[v] == c]:
            new = [2 * x for x in col]; new[v] = 2 * col[v] + 1
            search(new)
    search([0] * n)
    return best[0]

def from_canon(n, s):
    out = [set() for _ in range(n)]; it = iter(s)
    for i in range(n):
        for j in range(i + 1, n):
            if next(it): out[i].add(j)
            else: out[j].add(i)
    return out

def all_tournaments_reps(k):
    reps = {}
    pairs = list(itertools.combinations(range(k), 2))
    for bits in range(1 << len(pairs)):
        out = [set() for _ in range(k)]
        for b, (i, j) in enumerate(pairs):
            if bits >> b & 1: out[i].add(j)
            else: out[j].add(i)
        reps.setdefault(canon(k, out), out)
    return list(reps.values())

def matrices(rows, cols):
    """all 0/1 matrices with given row and column sums"""
    t = len(rows); res = []
    def rec(i, cap, acc):
        if i == t:
            if all(c == 0 for c in cap): res.append(acc[:])
            return
        for S in itertools.combinations(range(len(cols)), rows[i]):
            if all(cap[j] > 0 for j in S):
                for j in S: cap[j] -= 1
                acc.append(S); rec(i + 1, cap, acc); acc.pop()
                for j in S: cap[j] += 1
    rec(0, list(cols), [])
    return res

def has_S2(n, out):
    inn = [set(w for w in range(n) if v in out[w]) for v in range(n)]
    return all(inn[a] & inn[b] for a, b in itertools.combinations(range(n), 2))

def main():
    n = int(sys.argv[1]); t = (n - 1) // 2
    O = list(range(1, t + 1)); R = list(range(t + 1, n))
    reps = all_tournaments_reps(t)
    print("tournaments on", t, "vertices:", len(reps), flush=True)
    classes = {}; cand = 0
    for TO in reps:
        rows = [t - len(TO[i]) for i in range(t)]
        for TR in reps:
            cols = [1 + len(TR[i]) for i in range(t)]
            if sum(rows) != sum(cols): continue
            for B in matrices(rows, cols):
                out = [set() for _ in range(n)]
                for o in O: out[0].add(o)
                for r in R: out[r].add(0)
                for i in range(t):
                    for j in TO[i]: out[O[i]].add(O[j])
                    for j in TR[i]: out[R[i]].add(R[j])
                for i in range(t):
                    S = set(B[i])
                    for j in range(t):
                        if j in S: out[O[i]].add(R[j])
                        else: out[R[j]].add(O[i])
                assert all(len(out[v]) == t for v in range(n))
                cand += 1
                classes.setdefault(canon(n, out), True)
    print("candidates:", cand, " regular tournaments up to isomorphism:", len(classes), flush=True)
    s2 = [s for s in sorted(classes) if has_S2(n, from_canon(n, s))]
    print("with S_2:", len(s2), flush=True)
    with open(sys.argv[2], 'w') as f:
        for s in s2: f.write(''.join(map(str, s)) + '\n')

if __name__ == '__main__':
    main()
