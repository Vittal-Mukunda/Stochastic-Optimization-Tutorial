#!/usr/bin/env python3
"""[check] Every necessary condition in spectral_engine.analyse must hold for EVERY regular tournament on 25 vertices
(codegrees unrestricted, non-strict mode), and reconstruct() must return the tournament whenever its pattern is
nondegenerate.  Test families with factored / degenerate spectra so that EDC, HM and GHC are exercised:
  * Cayley tournaments on Z_25 and on Z_5 x Z_5 (random connection sets),
  * Z_5-invariant tournaments (5 orbits of size 5) and Z_3-invariant ones (8 orbits of 3 + a fixed point),
  * random regular tournaments (3-cycle reversal walk).
Negative controls: patterns that are not codegree patterns of any tournament must be killed.
Usage: python3 spectral_validate.py [samples_per_family]
"""
import collections
import random
import sys

import numpy as np

sys.path.insert(0, 'research/compute/p25')
import spectral_engine as se  # noqa: E402

N = 25


def cayley(group, D):
    T = np.zeros((N, N), dtype=np.int64)
    for i, g in enumerate(group):
        for j, h in enumerate(group):
            if i != j and group.sub(h, g) in D:
                T[i, j] = 1
    return T


class Zn:
    def __init__(self):
        self.els = list(range(25))

    def __iter__(self):
        return iter(self.els)

    def sub(self, a, b):
        return (a - b) % 25

    def neg(self, a):
        return (-a) % 25


class Z5sq:
    def __init__(self):
        self.els = [(i, j) for i in range(5) for j in range(5)]

    def __iter__(self):
        return iter(self.els)

    def sub(self, a, b):
        return ((a[0] - b[0]) % 5, (a[1] - b[1]) % 5)

    def neg(self, a):
        return ((-a[0]) % 5, (-a[1]) % 5)


def random_cayley(G, rng):
    pairs, seen = [], set()
    for g in G:
        if g in seen or g == G.els[0]:
            continue
        seen |= {g, G.neg(g)}
        pairs.append((g, G.neg(g)))
    D = set(p[rng.randrange(2)] for p in pairs)
    return cayley(G, D)


def random_regular(rng, steps=4000):
    T = np.zeros((N, N), dtype=np.int64)
    for i in range(N):
        for d in range(1, 13):
            T[i, (i + d) % N] = 1
    for _ in range(steps):
        a, b, c = rng.sample(range(N), 3)
        if T[a, b] and T[b, c] and T[c, a]:
            T[a, b] = T[b, c] = T[c, a] = 0
            T[b, a] = T[c, b] = T[a, c] = 1
    return T


def random_symmetric(rng, order, orbits, fixed):
    """Tournament invariant under the permutation sigma = product of `orbits` cycles of length `order` (+ `fixed`
    fixed points, fixed <= 1), regular, found by a 3-cycle-orbit reversal walk started from a rotational tournament."""
    n = order * orbits + fixed
    assert n == N
    # vertex (o, t) -> o*order + t ; fixed point -> n-1
    def sig(v):
        if v == n - 1 and fixed:
            return v
        o, t = divmod(v, order)
        return o * order + (t + 1) % order
    # start: regular tournament on Z_25 relabelled is not invariant in general; instead build orbit-wise:
    # use the Cayley tournament on Z_25 with D = {1..12} under the labelling v -> v, and the shift by `orbits`
    # is not available for order 3, so do a constructive start: greedy invariant orientation then balance by walk.
    T = np.zeros((N, N), dtype=np.int64)
    orbit_of = {}
    for a in range(N):
        for b in range(N):
            if a == b or (a, b) in orbit_of:
                continue
            orb, x, y = [], a, b
            for _ in range(order):
                orb.append((x, y))
                x, y = sig(x), sig(y)
            rev = [(y_, x_) for (x_, y_) in orb]
            if set(orb) & set(rev):        # pair orbit contains both orientations: impossible for odd order
                raise RuntimeError('odd order should prevent this')
            choice = rng.randrange(2)
            for (x_, y_) in (orb if choice else rev):
                T[x_, y_] = 1
                orbit_of[(x_, y_)] = orbit_of[(y_, x_)] = True
    # balance out-degrees with invariant moves: reverse the sigma-orbit of a directed path u->v... simplest: reverse
    # orbits of 3-cycles (keeps all degrees), so first fix degrees by reversing orbits of arcs from high to low.
    def outdeg():
        return T.sum(axis=1)
    for _ in range(20000):
        d = outdeg()
        if (d == 12).all():
            break
        hi = [v for v in range(N) if d[v] > 12]
        lo = [v for v in range(N) if d[v] < 12]
        a, b = rng.choice(hi), rng.choice(lo)
        if not T[a, b]:
            continue
        x, y = a, b
        for _ in range(order):
            T[x, y], T[y, x] = 0, 1
            x, y = sig(x), sig(y)
    if not (outdeg() == 12).all():
        return None
    for _ in range(3000):
        a, b, c = rng.sample(range(N), 3)
        if T[a, b] and T[b, c] and T[c, a]:
            x, y, z = a, b, c
            for _ in range(order):
                T[x, y] = T[y, z] = T[z, x] = 0
                T[y, x] = T[z, y] = T[x, z] = 1
                x, y, z = sig(x), sig(y), sig(z)
            if not (outdeg() == 12).all():       # orbit of the 3-cycle overlapped itself; undo
                x, y, z = a, b, c
                for _ in range(order):
                    T[x, y] = T[y, z] = T[z, x] = 1
                    T[y, x] = T[z, y] = T[x, z] = 0
                    x, y, z = sig(x), sig(y), sig(z)
    assert (T + T.T + np.eye(N, dtype=np.int64) == 1).all()
    return T


def check(T, label, stats):
    Y = se.pattern_of(T)
    res = se.analyse(Y, strict=False)
    status, sols = se.reconstruct(Y)
    hit = None
    if status == 'ok':
        hit = any((S == T).all() or (S == T.T).all() for S in sols)
    nf = len(res.get('g_factors', []))
    maxk = max([f[1] for f in res.get('g_factors', [])] or [0])
    key = (label, res['alive'], status, hit)
    stats[key] += 1
    stats[(label, 'nfactors', nf, 'maxk', maxk)] += 1
    if not res['alive'] or (status == 'ok' and not hit):
        print('FAIL', label, res.get('killed_by'), res.get('edc'), res.get('ghc_bad_primes'), status, hit)
        np.save('/tmp/fail_%s.npy' % label, T)
    return res


def main():
    S = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    rng = random.Random(2026)
    stats = collections.Counter()
    for label, G in (('cay_Z25', Zn()), ('cay_Z5sq', Z5sq())):
        for _ in range(S):
            check(random_cayley(G, rng), label, stats)
    for label, (order, orbits, fixed) in (('sym_Z5', (5, 5, 0)), ('sym_Z3', (3, 8, 1))):
        done = 0
        while done < S:
            T = random_symmetric(rng, order, orbits, fixed)
            if T is None:
                continue
            check(T, label, stats)
            done += 1
    for _ in range(S):
        check(random_regular(rng), 'random', stats)
    for k in sorted(stats, key=str):
        print(k, stats[k])
    # negative controls
    print('--- negative controls (must be killed)')
    rngn = np.random.default_rng(1)
    killed = collections.Counter()
    for _ in range(S):
        # random symmetric 0/1 pattern with row sums 12 via a random 12-regular graph (configuration-free: switch walk)
        A = np.zeros((N, N), dtype=np.int64)
        for i in range(N):
            for d in (1, 2, 3, 4, 5, 6):
                A[i, (i + d) % N] = A[(i + d) % N, i] = 1
        for _ in range(3000):
            a, b, c, d = rngn.choice(N, 4, replace=False)
            if A[a, b] and A[c, d] and not A[a, c] and not A[b, d]:
                A[a, b] = A[b, a] = A[c, d] = A[d, c] = 0
                A[a, c] = A[c, a] = A[b, d] = A[d, b] = 1
        killed[se.analyse(A).get('killed_by')] += 1
    print('random 12-regular graphs as m = 1 patterns:', dict(killed))


if __name__ == '__main__':
    main()
