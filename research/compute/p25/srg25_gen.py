#!/usr/bin/env python3
"""Generate strongly regular graphs srg(25,12,5,6) (Paulus graphs; 15 exist up to isomorphism, Paulus 1973) without
network access: Paley P(25) from GF(25), SAT solutions with randomised encodings, and all Seidel-switching descendants
(conference two-graphs on 26 points), de-duplicated with VF2++ after invariant hashing.
Writes research/compute/p25/srg25_12_5_6.txt (one graph per line: 300 upper-triangle bits).
Usage: python3 srg25_gen.py [sat_runs]
"""
import itertools
import random
import sys

import networkx as nx
import numpy as np
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
from pysat.solvers import Solver

N = 25


def paley25():
    # GF(25) = GF(5)[i]/(i^2 - 2)  (2 is a non-square mod 5)
    els = [(a, b) for a in range(5) for b in range(5)]
    def mul(x, y):
        return ((x[0] * y[0] + 2 * x[1] * y[1]) % 5, (x[0] * y[1] + x[1] * y[0]) % 5)
    squares = set(mul(x, x) for x in els if x != (0, 0))
    assert len(squares) == 12
    A = np.zeros((N, N), dtype=np.int64)
    for i, x in enumerate(els):
        for j, y in enumerate(els):
            if i != j and ((x[0] - y[0]) % 5, (x[1] - y[1]) % 5) in squares:
                A[i, j] = 1
    return A


def is_srg(A):
    A2 = A @ A
    I = np.eye(N, dtype=np.int64)
    J = np.ones((N, N), dtype=np.int64)
    return (A == A.T).all() and (np.diag(A) == 0).all() and (A2 == 12 * I + 5 * A + 6 * (J - I - A)).all()


def sat_srg(seed):
    rng = random.Random(seed)
    perm = list(range(N))
    rng.shuffle(perm)
    pool = IDPool()
    e = {}
    for a, b in itertools.combinations(range(N), 2):
        e[(a, b)] = e[(b, a)] = pool.id(('e', a, b))
    cnf = []
    for a in range(N):
        lits = [e[(a, b)] for b in range(N) if b != a]
        cnf += CardEnc.equals(lits, 12, vpool=pool, encoding=EncType.seqcounter).clauses
    for a, b in itertools.combinations(range(N), 2):
        lits = [e[(a, b)]]
        for w in range(N):
            if w in (a, b):
                continue
            c = pool.id(('c', a, b, w))
            cnf += [[-c, e[(a, w)]], [-c, e[(b, w)]], [c, -e[(a, w)], -e[(b, w)]]]
            lits.append(c)
        cnf += CardEnc.equals(lits, 6, vpool=pool, encoding=EncType.seqcounter).clauses
    rng.shuffle(cnf)
    with Solver(name='cadical195', bootstrap_with=cnf) as s:
        # random phase via assumptions-free trick: add a random partial "preference" by solving with a random
        # first arc fixed; cheap diversification
        a, b = rng.sample(range(N), 2)
        ok = s.solve(assumptions=[e[(a, b)] if rng.random() < 0.5 else -e[(a, b)]])
        if not ok:
            ok = s.solve()
        if not ok:
            return None
        model = set(l for l in s.get_model() if l > 0)
    A = np.zeros((N, N), dtype=np.int64)
    for (a, b), v in e.items():
        if v in model:
            A[perm[a], perm[b]] = 1
    return A


def descendants(A):
    H = np.zeros((N + 1, N + 1), dtype=np.int64)
    H[:N, :N] = A
    out = []
    for v in range(N + 1):
        S = set(np.nonzero(H[v])[0])
        K = H.copy()
        for x in range(N + 1):
            for y in range(N + 1):
                if x != y and ((x in S) != (y in S)):
                    K[x, y] = 1 - K[x, y]
        assert K[v].sum() == 0
        keep = [x for x in range(N + 1) if x != v]
        out.append(K[np.ix_(keep, keep)])
    return out


def invariant(A):
    G = nx.from_numpy_array(A)
    loc = []
    for v in range(N):
        nb = list(np.nonzero(A[v])[0])
        sub = A[np.ix_(nb, nb)]
        tri = int(np.trace(sub @ sub @ sub)) // 6
        loc.append((tri, tuple(sorted(np.round(np.linalg.eigvalsh(sub.astype(float)), 6)))))
    return tuple(sorted(loc))


class Classes:
    def __init__(self):
        self.reps = []

    def add(self, A):
        inv = invariant(A)
        G = nx.from_numpy_array(A)
        for inv2, G2, _ in self.reps:
            if inv2 == inv and nx.vf2pp_is_isomorphic(G, G2):
                return False
        self.reps.append((inv, G, A))
        return True


def main():
    runs = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    C = Classes()
    queue = [paley25()]
    assert is_srg(queue[0])
    for seed in range(runs):
        A = sat_srg(seed)
        if A is not None:
            assert is_srg(A)
            queue.append(A)
    while queue:
        A = queue.pop()
        if C.add(A):
            print('new class #%d (K4-count %d)' % (len(C.reps), sum(t for t, _ in invariant(A)) // 4), flush=True)
            for D in descendants(A):
                assert is_srg(D)
                queue.append(D)
    with open('research/compute/p25/srg25_12_5_6.txt', 'w') as fh:
        for _, _, A in C.reps:
            fh.write(''.join(str(int(A[i, j])) for i, j in itertools.combinations(range(N), 2)) + '\n')
    print('classes found:', len(C.reps))


if __name__ == '__main__':
    main()
