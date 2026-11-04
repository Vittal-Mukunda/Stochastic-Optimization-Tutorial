"""Independent check that reg11_S2.txt lists every 5-regular S_2 tournament on 11 vertices exactly once (up to iso).

1. Count labelled regular tournaments on 11 vertices exactly (recursion on score sequences).
2. For every line of reg11.txt: 5-regular; automorphism group by exhaustive search; sum of 11!/|Aut| must equal (1).
   Together with pairwise non-isomorphism (3) this shows reg11.txt is complete: every labelled regular tournament
   is counted exactly once.
3. Pairwise non-isomorphism of the 1223 lines (canonical form = lexicographically least adjacency string over all
   relabellings that respect a vertex invariant, computed by exhaustive search).
4. The S_2 lines of reg11.txt, and the lines of reg11_S2.txt, give the same set of canonical forms, with no repeats.
Usage: python verify_classes.py reg11.txt reg11_S2.txt
"""
import sys, itertools
from functools import lru_cache
from math import factorial

n = 11


def parse(line):
    line = line.strip(); assert len(line) == 55
    A = [[0] * n for _ in range(n)]; k = 0
    for i in range(n):
        for j in range(i + 1, n):
            if line[k] == '1': A[i][j] = 1
            else: A[j][i] = 1
            k += 1
    return A


@lru_cache(maxsize=None)
def count(s):
    """labelled tournaments on len(s) vertices in which vertex i has out-degree s[i] (s sorted)."""
    m = len(s)
    if m == 0:
        return 1
    if any(x < 0 or x > m - 1 for x in s) or sum(s) != m * (m - 1) // 2:
        return 0
    s0, rest = s[0], s[1:]
    tot = 0
    for W in itertools.combinations(range(m - 1), s0):        # vertex 0 beats W; the others beat vertex 0
        Ws = set(W)
        s2 = tuple(sorted(rest[i] - (0 if i in Ws else 1) for i in range(m - 1)))
        tot += count(s2)
    return tot


def invariant(A):
    """per-vertex invariant: (sorted out-scores inside N+(v), sorted out-scores inside N-(v))."""
    inv = []
    for v in range(n):
        Np = [u for u in range(n) if A[v][u]]; Nm = [u for u in range(n) if A[u][v]]
        sp = tuple(sorted(sum(A[u][w] for w in Np) for u in Np))
        sm = tuple(sorted(sum(A[u][w] for w in Nm) for u in Nm))
        inv.append((sp, sm))
    return inv


def aut_size(A):
    inv = invariant(A); cnt = 0; m = []
    def ext(k):
        nonlocal cnt
        if k == n:
            cnt += 1; return
        for v in range(n):
            if v not in m and inv[v] == inv[k] and all(A[i][k] == A[m[i]][v] for i in range(k)):
                m.append(v); ext(k + 1); m.pop()
    ext(0)
    return cnt


def canon(A):
    """lexicographically least upper-triangle string over relabellings respecting the invariant, with pruning."""
    inv = invariant(A)
    cls = sorted(set(inv))
    order_slots = sorted(range(n), key=lambda v: inv[v])
    slots = [inv[v] for v in order_slots]
    best = [None]
    pos = []
    def rec(k, partial):
        # partial: string of the upper triangle entries among positions < k, in row-major order restricted to < k
        if best[0] is not None:
            # compare with the same restricted part of best
            if partial > best_restricted(k):
                return
        if k == n:
            s = full_string()
            if best[0] is None or s < best[0]:
                best[0] = s
            return
        for v in range(n):
            if v in pos or inv[v] != slots[k]:
                continue
            pos.append(v)
            rec(k + 1, partial + ''.join(str(A[pos[i]][v]) for i in range(k)))
            pos.pop()
    def full_string():
        return ''.join(str(A[pos[i]][pos[j]]) for j in range(n) for i in range(j))
    def best_restricted(k):
        return best[0][:k * (k - 1) // 2]
    rec(0, '')
    return best[0]


if __name__ == '__main__':
    L = factorial(n)
    total = count(tuple([5] * n))
    print('labelled regular tournaments on 11 vertices:', total)
    regs = [parse(l) for l in open(sys.argv[1]).read().split()]
    s2 = [parse(l) for l in open(sys.argv[2]).read().split()]
    assert all(all(sum(r) == 5 for r in A) for A in regs + s2)
    auts = [aut_size(A) for A in regs]
    assert all(L % a == 0 for a in auts)
    lab = sum(L // a for a in auts)
    print('reg11.txt lines:', len(regs), ' sum 11!/|Aut| =', lab, ' equal:', lab == total)
    cr = [canon(A) for A in regs]
    print('distinct canonical forms in reg11.txt:', len(set(cr)))
    def isS2(A):
        return all(any(A[w][u] and A[w][v] for w in range(n)) for u in range(n) for v in range(u + 1, n))
    crS2 = sorted(c for c, A in zip(cr, regs) if isS2(A))
    cs = sorted(canon(A) for A in s2)
    print('S_2 among reg11.txt:', len(crS2), ' reg11_S2.txt lines:', len(s2), ' distinct:', len(set(cs)),
          ' all S_2:', all(isS2(A) for A in s2), ' same set:', crS2 == cs)
    print('Aut orders in reg11_S2.txt:', sorted(set(aut_size(A) for A in s2)))
