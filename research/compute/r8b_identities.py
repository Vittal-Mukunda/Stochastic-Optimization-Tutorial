"""R8-B: check the counting identities used in the no-tight order-52 analysis on random tournaments.

Each check is an identity that holds in EVERY tournament (generic form), or in every tournament on 52 vertices with
twenty-six in-degrees 25 and twenty-six in-degrees 26 (degree form).  Steps that need the no-tight hypothesis
(12-regularity of T[N^-(v)] for d^-(v) = 25) are NOT identities and are not checked here; the report explains them.

  G1  sum_{b in N+(w)} |D(w,b)| = sum_{x in N-(w)} (d+(x) - 1) - C(d-(w), 2)
  G2  sum_{a in N-(b)} |D(a,b)| = C(d-(b), 2)                    (|D(a,b)| = in-degree of a in T[N-(b)] when a -> b)
  G3  sum_P |D(P)| = sum_v C(d+(v), 2) = sum_v C(d-(v), 2)
  G4  sum_{P subset N-(v)} |D(P)| = sum_{w in N-(v)} C(d+_{N-(v)}(w), 2) + sum_{b in N+(v)} C(|N-(v) \\ N-(b)|, 2)
  G5  for a pair P, R = D(P), u in R:
        sum_{w in R-u} |D(u,w)| = sum_{w' in N-_R(u)} (d+_R(w') - 1) + sum_{y notin P u R, y -> u} (|R \\ N-(y)| - 1)
  G6  for P, R = D(P), u != w in R, writing X = c + T_C + E_both (order-52 local quantities, |R| = 12 only):
        s(u,w) := sum_{x in R-u-w} (|D(u,w,x)| - 5) = 5|D(u,w)| - 50 - X(u,w)
  D1  (degrees 25/26)  w in L:  sum_{b in N+(w)} (|D(w,b)| - 12) = 13 - d+_L(w)
  D2  (degrees 25/26)  w in H:  sum_{b in N+(w)} (|D(w,b)| - 12) = d+_H(w)
  D3  (degrees 25/26)  b in L:  sum_{a in N-(b)} (|D(a,b)| - 12) = 0 ;  b in H: = 13
"""
import itertools
import random
from math import comb

import numpy as np


def rand_tour(n, rng):
    A = np.zeros((n, n), dtype=np.int64)
    for i, j in itertools.combinations(range(n), 2):
        if rng.random() < 0.5:
            A[i, j] = 1
        else:
            A[j, i] = 1
    return A


def tour_2526(rng, flips=20000):
    """52 vertices, in-degree 25 on 0..25 and 26 on 26..51, randomised by reversing directed 3-cycles."""
    n = 52
    A = np.zeros((n, n), dtype=np.int64)
    for i in range(n):
        for d in range(1, 26):
            A[i, (i + d) % n] = 1
    for i in range(26):
        A[i, i + 26] = 1
    for _ in range(flips):
        x, y, z = rng.sample(range(n), 3)
        if A[x, y] and A[y, z] and A[z, x]:
            A[x, y] = A[y, z] = A[z, x] = 0
            A[y, x] = A[z, y] = A[x, z] = 1
    return A


def D(A, X):
    X = list(X)
    n = len(A)
    return [w for w in range(n) if w not in X and all(A[w, x] for x in X)]


def check(A, rng, deg2526=False):
    n = len(A)
    din = A.sum(axis=0)
    dout = A.sum(axis=1)
    ok = True
    Dpair = {}
    for u, w in itertools.combinations(range(n), 2):
        Dpair[u, w] = Dpair[w, u] = len(D(A, (u, w)))
    for w in range(n):
        lhs = sum(Dpair[w, b] for b in range(n) if A[w, b])
        rhs = sum(dout[x] - 1 for x in range(n) if A[x, w]) - comb(int(din[w]), 2)
        ok &= lhs == rhs
        ok &= sum(Dpair[a, w] for a in range(n) if A[a, w]) == comb(int(din[w]), 2)
    ok &= sum(Dpair[u, w] for u, w in itertools.combinations(range(n), 2)) == sum(comb(int(d), 2) for d in dout)
    ok &= sum(comb(int(d), 2) for d in dout) == sum(comb(int(d), 2) for d in din)
    for v in rng.sample(range(n), 3):
        Wv = [x for x in range(n) if A[x, v]]
        Bv = [x for x in range(n) if A[v, x]]
        lhs = sum(Dpair[p, q] for p, q in itertools.combinations(Wv, 2))
        rhs = sum(comb(int(sum(A[w, x] for x in Wv)), 2) for w in Wv) + \
            sum(comb(len([x for x in Wv if not A[x, b]]), 2) for b in Bv)
        ok &= lhs == rhs
    tried12 = 0
    for _ in range(300):
        if tried12 >= 3:
            break
        p, q = rng.sample(range(n), 2)
        R = D(A, (p, q))
        if len(R) < 3:
            continue
        tried12 += len(R) == 12
        if len(R) != 12 and rng.random() < 0.9:
            continue
        O = [y for y in range(n) if y not in R and y not in (p, q)]
        for u in R:
            lhs = sum(Dpair[u, w] for w in R if w != u)
            rhs = sum(sum(A[wp, x] for x in R) - 1 for wp in R if A[wp, u]) + \
                sum(len([r for r in R if A[y, r]]) - 1 for y in O if A[y, u])
            ok &= lhs == rhs
        if len(R) == 12:
            t = {r: int(sum(A[x, r] for x in R)) - 5 for r in R}
            ey = {y: (12 - len([r for r in R if A[y, r]])) - 5 for y in O}
            for u, w in itertools.combinations(R, 2):
                s = sum(len(D(A, (u, w, x))) - 5 for x in R if x not in (u, w))
                C = [wp for wp in R if A[wp, u] and A[wp, w]]
                K = [y for y in O if A[y, u] and A[y, w]]
                X = len(C) + sum(t[x] for x in C) + sum(ey[y] for y in K)
                ok &= s == 5 * Dpair[u, w] - 50 - X
    if deg2526:
        L = [x for x in range(n) if din[x] == 25]
        H = [x for x in range(n) if din[x] == 26]
        assert len(L) == 26 and len(H) == 26
        Ls = set(L)
        for w in range(n):
            ex = sum(Dpair[w, b] - 12 for b in range(n) if A[w, b])
            if w in Ls:
                ok &= ex == 13 - sum(A[w, x] for x in L)
            else:
                ok &= ex == sum(A[w, x] for x in H)
            exin = sum(Dpair[a, w] - 12 for a in range(n) if A[a, w])
            ok &= exin == (0 if w in Ls else 13)
    check.g6 = getattr(check, 'g6', 0) + tried12
    return bool(ok)


def main():
    rng = random.Random(902)
    res = []
    for n in (20, 31, 52):
        for _ in range(3):
            res.append(('generic', n, check(rand_tour(n, rng), rng)))
    found12 = 0
    for k in range(4):
        A = tour_2526(rng)
        din = A.sum(axis=0)
        assert sorted(din.tolist()) == [25] * 26 + [26] * 26
        res.append(('deg25/26', 52, check(A, rng, deg2526=True)))
    for r in res:
        print(r)
    print('pairs with |D(P)| = 12 on which G6 was checked:', check.g6)
    print('ALL OK' if all(r[2] for r in res) else 'FAILURE')


if __name__ == '__main__':
    main()
