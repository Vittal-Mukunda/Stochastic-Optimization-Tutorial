#!/usr/bin/env python3
"""(R25)/(P25)/NDR(25) restricted to tournaments with a prescribed automorphism sigma of odd prime order.

Why this is the right symmetric family for the pattern search: if the codegree pattern Y is invariant under a group G
of odd order and every eigenvalue of Y on 1^⊥ has multiplicity 2, then every tournament with pattern Y is G-invariant
(G acts on each eigenplane by rotations, which commute with the quarter-turn B_j; see spectral_engine.reconstruct).
So "G-invariant patterns, nondegenerate case" = "G-invariant tournaments".

sigma is given by its cycle type: c cycles of length p plus f fixed points (c*p + f = 25).  Arc variables are shared
along sigma-orbits of ordered pairs (odd order: the orbit of (a, b) never contains (b, a)); every constraint is imposed
for one representative of each orbit of pairs / triples.

Usage: python3 p25_symsat.py p c f problem time_limit [solver=cadical195]
  problem: R25 (codegree >= 5), P25 (codegree >= 5 and S_3), NDR (codegree in {5, 6}), NDRS3 (NDR + S_3),
           P26 (26 vertices, every in-degree >= 12, codegree >= 5, S_3: the in-neighbourhood of an in-degree-26 vertex
           without tight in-pairs), P25j<j> (25 vertices, in-degrees >= 11 with exactly j of them = 11, codegree >= 5,
           S_3: an in-degree-25 vertex with exactly j tight in-pairs)
"""
import collections
import itertools
import multiprocessing as mp
import sys
import time

import numpy as np
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
from pysat.solvers import Solver

sys.path.insert(0, 'research/compute/p25')
import spectral_engine as se  # noqa: E402

N = 25


def build(p, c, f, problem):
    n = 26 if problem == 'P26' else 25
    assert c * p + f == n
    N = n
    sig = list(range(N))
    for i in range(c):
        for t in range(p):
            sig[i * p + t] = i * p + (t + 1) % p
    pool = IDPool()
    rep = {}

    def orbit(tup):
        out, cur = [], tup
        while True:
            out.append(cur)
            cur = tuple(sig[v] for v in cur)
            if cur == tup:
                return out

    def arc(a, b):
        if (a, b) in rep:
            return rep[(a, b)]
        orb = orbit((a, b))
        v = pool.id(('x', min(orb)))
        for (x, y) in orb:
            rep[(x, y)] = v
            rep[(y, x)] = -v
        return rep[(a, b)]

    for a, b in itertools.combinations(range(N), 2):
        arc(a, b)
    cnf = []
    seen = set()
    elevens = []
    for a in range(N):
        o = min(orbit((a,)))
        if o in seen:
            continue
        seen.add(o)
        ins = [arc(b, a) for b in range(N) if b != a]
        if problem == 'P26':
            cnf += CardEnc.atleast(ins, 12, vpool=pool, encoding=EncType.seqcounter).clauses
        elif problem.startswith('P25j'):
            cnf += CardEnc.atleast(ins, 11, vpool=pool, encoding=EncType.seqcounter).clauses
            e11 = pool.id(('eleven', a))          # e11 <-> in-degree of a is exactly 11 (i.e. <= 11)
            le = CardEnc.atmost(ins, 11, vpool=pool, encoding=EncType.seqcounter).clauses
            cnf += [cl + [-e11] for cl in le]     # e11 -> in-degree <= 11
            ge = CardEnc.atleast(ins, 12, vpool=pool, encoding=EncType.seqcounter).clauses
            cnf += [cl + [e11] for cl in ge]      # not e11 -> in-degree >= 12
            elevens += [e11] * len(orbit((a,)))
        else:
            cnf += CardEnc.equals([arc(a, b) for b in range(N) if b != a], 12, vpool=pool,
                                  encoding=EncType.seqcounter).clauses
    if problem.startswith('P25j'):
        j = int(problem[4:])
        # each orbit representative's flag is repeated once per orbit member, so this counts vertices
        cnf += CardEnc.equals(elevens, j, vpool=pool, encoding=EncType.seqcounter).clauses
    lo, hi = 5, (6 if problem.startswith('NDR') else 11)
    yv = {}
    seen = set()
    for a, b in itertools.combinations(range(N), 2):
        o = min(tuple(sorted(t)) for t in orbit((a, b)))
        if o in seen:
            continue
        seen.add(o)
        lits = []
        for w in range(N):
            if w in (a, b):
                continue
            t = pool.id(('y', w, a, b))
            cnf += [[-t, arc(w, a)], [-t, arc(w, b)], [t, -arc(w, a), -arc(w, b)]]
            lits.append(t)
        cnf += CardEnc.atleast(lits, lo, vpool=pool, encoding=EncType.seqcounter).clauses
        if hi < 11:
            cnf += CardEnc.atmost(lits, hi, vpool=pool, encoding=EncType.seqcounter).clauses
    if problem in ('P25', 'NDRS3', 'P26') or problem.startswith('P25j'):
        seen = set()
        for a, b, d in itertools.combinations(range(N), 3):
            o = min(tuple(sorted(t)) for t in orbit((a, b, d)))
            if o in seen:
                continue
            seen.add(o)
            lits = []
            for w in range(N):
                if w in (a, b, d):
                    continue
                z = pool.id(('z', w, a, b, d))
                cnf += [[-z, arc(w, a)], [-z, arc(w, b)], [-z, arc(w, d)]]
                lits.append(z)
            cnf.append(lits)
    return cnf, arc


def main():
    """pysat holds the GIL while solving, so the time limit is enforced by running the job in a child process."""
    tl = float(sys.argv[5])
    proc = mp.Process(target=job, args=(sys.argv[1:],))
    t0 = time.time()
    proc.start()
    proc.join(tl)
    if proc.is_alive():
        proc.terminate()
        proc.join()
        print({'sigma': '%s^%s 1^%s' % tuple(sys.argv[1:4]), 'problem': sys.argv[4], 'status': 'UNKNOWN',
               'time_limit': tl, 'time': round(time.time() - t0, 1)}, flush=True)


def job(argv):
    p, c, f, problem = int(argv[0]), int(argv[1]), int(argv[2]), argv[3]
    solver = next((a.split('=')[1] for a in argv[5:] if a.startswith('solver=')), 'cadical195')
    cnf, arc = build(p, c, f, problem)
    N = 26 if problem == 'P26' else 25
    nv = max(abs(l) for cl in cnf for l in cl)
    t0 = time.time()
    with Solver(name=solver, bootstrap_with=cnf) as s:
        r = s.solve()
        dt = time.time() - t0
        model = set(l for l in s.get_model() if l > 0) if r else None
    status = {None: 'UNKNOWN', False: 'UNSAT', True: 'SAT'}[r]
    rec = {'sigma': '%d^%d 1^%d' % (p, c, f), 'problem': problem, 'solver': solver, 'vars': nv, 'clauses': len(cnf),
           'status': status, 'time': round(dt, 1)}
    if r:
        T = np.zeros((N, N), dtype=np.int64)
        for a in range(N):
            for b in range(N):
                if a != b:
                    l = arc(a, b)
                    if (l > 0 and l in model) or (l < 0 and -l not in model):
                        T[a, b] = 1
        C = T.T @ T
        rec['tournament'] = bool((T + T.T + np.eye(N, dtype=np.int64) == 1).all())
        rec['indegrees'] = sorted(collections.Counter(T.sum(0).tolist()).items())
        rec['codeg_min_max'] = (int(C[~np.eye(N, dtype=bool)].min()), int(C[~np.eye(N, dtype=bool)].max()))
        inn = [set(np.nonzero(T[:, v])[0]) for v in range(N)]
        rec['S3'] = all(inn[a] & inn[b] & inn[d] for a, b, d in itertools.combinations(range(N), 3))
        fn = 'research/compute/p25/sym_%s_%d_%d_%d.npy' % (problem, p, c, f)
        np.save(fn, T)
        rec['saved'] = fn
    print(rec, flush=True)


if __name__ == '__main__':
    main()
