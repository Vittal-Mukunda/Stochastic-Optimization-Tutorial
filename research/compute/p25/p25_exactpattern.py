#!/usr/bin/env python3
"""Exact-pattern search: is there a 12-regular tournament on 25 vertices whose codegree matrix is exactly 5 + Y?
Used for patterns that survive spectral_engine.analyse but are spectrally degenerate (reconstruct() does not apply).

Model (both back-ends): arc variables x_ab; out-degree 12; for every pair {a, b}: sum_w [w -> a][w -> b] = 5 + Y_ab.
Optional: the commuting relation T Y = Y T (Lemma 7.1: M Y = Y M), i.e. for all a, c:
    sum_b [a -> b] Y_bc = sum_b Y_ab [b -> c]      (linear in the arcs);
optional S_3.  Symmetry: Y is reversal-invariant, so the arc 0 -> 1 is fixed.

Usage:
  python3 p25_exactpattern.py cpsat <pattern-source> <time_limit> [nocommute] [s3] [workers=N]
  python3 p25_exactpattern.py sat   <pattern-source> <time_limit> [solver=cadical195|kissat404] [s3]
<pattern-source>: a tournament file (its own pattern, for calibration), or srg:<line index> (Y = adjacency of the
graph on that line of srg25_12_5_6.txt), or npy:<file>.
"""
import itertools
import sys
import time

import numpy as np

sys.path.insert(0, 'research/compute/p25')
import spectral_engine as se  # noqa: E402

N = 25


def get_pattern(src):
    if src.startswith('srg:'):
        rows = open('research/compute/p25/srg25_12_5_6.txt').read().split()
        s = rows[int(src[4:])]
        A = np.zeros((N, N), dtype=np.int64)
        for (i, j), ch in zip(itertools.combinations(range(N), 2), s):
            A[i, j] = A[j, i] = int(ch)
        return A, None
    if src.startswith('npy:'):
        return np.load(src[4:]), None
    T = se.load_tournament(src)
    return se.pattern_of(T), T


def verify(T, Y, s3):
    T = np.asarray(T)
    ok = (T + T.T + np.eye(N, dtype=np.int64) == 1).all() and (T.sum(axis=1) == 12).all()
    ok = ok and (se.pattern_of(T) == Y).all()
    if s3:
        ok = ok and se.has_S3(T)
    return bool(ok)


def run_cpsat(Y, tlimit, commute=True, s3=False, workers=4):
    from ortools.sat.python import cp_model
    m = cp_model.CpModel()
    x = [[None] * N for _ in range(N)]
    for a, b in itertools.combinations(range(N), 2):
        v = m.NewBoolVar('x%d_%d' % (a, b))
        x[a][b] = v
        x[b][a] = v.Not()
    for a in range(N):
        m.Add(sum(x[a][b] for b in range(N) if b != a) == 12)
    y = {}
    for a, b in itertools.combinations(range(N), 2):
        terms = []
        for w in range(N):
            if w in (a, b):
                continue
            t = m.NewBoolVar('')
            m.AddBoolAnd([x[w][a], x[w][b]]).OnlyEnforceIf(t)
            m.AddBoolOr([x[w][a].Not(), x[w][b].Not()]).OnlyEnforceIf(t.Not())
            y[(w, a, b)] = t
            terms.append(t)
        m.Add(sum(terms) == 5 + int(Y[a][b]))
    if commute:
        for a in range(N):
            for c in range(N):
                if a == c:
                    continue
                lhs = [int(Y[b][c]) * x[a][b] for b in range(N) if b != a and Y[b][c]]
                rhs = [int(Y[a][b]) * x[b][c] for b in range(N) if b != c and Y[a][b]]
                # [a -> c] appears on both sides only through b = c / b = a with Y_cc = Y_aa = 0
                m.Add(sum(lhs) == sum(rhs))
    if s3:
        for a, b, c in itertools.combinations(range(N), 3):
            lits = []
            for w in range(N):
                if w in (a, b, c):
                    continue
                z = m.NewBoolVar('')
                m.AddImplication(z, y[(w, a, b)])
                m.AddImplication(z, x[w][c])
                lits.append(z)
            m.AddBoolOr(lits)
    m.Add(x[0][1] == 1)
    s = cp_model.CpSolver()
    s.parameters.max_time_in_seconds = tlimit
    s.parameters.num_workers = workers
    t0 = time.time()
    st = s.Solve(m)
    dt = time.time() - t0
    name = s.StatusName(st)
    T = None
    if name in ('OPTIMAL', 'FEASIBLE'):
        T = np.zeros((N, N), dtype=np.int64)
        for a in range(N):
            for b in range(N):
                if a != b and s.Value(x[a][b]):
                    T[a, b] = 1
    return name, dt, T


def run_sat(Y, tlimit, solver='cadical195', s3=False):
    from pysat.card import CardEnc, EncType
    from pysat.formula import IDPool
    from pysat.solvers import Solver
    import threading
    pool = IDPool()
    arc = {}
    for a, b in itertools.combinations(range(N), 2):
        v = pool.id(('x', a, b))
        arc[(a, b)] = v
        arc[(b, a)] = -v
    cnf = []
    for a in range(N):
        cnf += CardEnc.equals([arc[(a, b)] for b in range(N) if b != a], 12, vpool=pool,
                              encoding=EncType.seqcounter).clauses
    yv = {}
    for a, b in itertools.combinations(range(N), 2):
        lits = []
        for w in range(N):
            if w in (a, b):
                continue
            t = pool.id(('y', w, a, b))
            cnf += [[-t, arc[(w, a)]], [-t, arc[(w, b)]], [t, -arc[(w, a)], -arc[(w, b)]]]
            yv[(w, a, b)] = t
            lits.append(t)
        cnf += CardEnc.equals(lits, 5 + int(Y[a][b]), vpool=pool, encoding=EncType.seqcounter).clauses
    if s3:
        for a, b, c in itertools.combinations(range(N), 3):
            lits = []
            for w in range(N):
                if w in (a, b, c):
                    continue
                z = pool.id(('z', w, a, b, c))
                cnf += [[-z, yv[(w, a, b)]], [-z, arc[(w, c)]]]
                lits.append(z)
            cnf.append(lits)
    cnf.append([arc[(0, 1)]])
    t0 = time.time()
    with Solver(name=solver, bootstrap_with=cnf) as s:
        timer = threading.Timer(tlimit, lambda: s.interrupt())
        timer.start()
        r = s.solve_limited(expect_interrupt=True)
        timer.cancel()
        dt = time.time() - t0
        if r is None:
            return 'UNKNOWN', dt, None
        if not r:
            return 'UNSAT', dt, None
        model = set(l for l in s.get_model() if l > 0)
    T = np.zeros((N, N), dtype=np.int64)
    for (a, b), v in arc.items():
        if v > 0:
            if v in model:
                T[a, b] = 1
            else:
                T[b, a] = 1
    return 'SAT', dt, T


def main():
    mode, src, tl = sys.argv[1], sys.argv[2], float(sys.argv[3])
    flags = sys.argv[4:]
    Y, T0 = get_pattern(src)
    s3 = 's3' in flags
    if mode == 'cpsat':
        workers = int(next((f.split('=')[1] for f in flags if f.startswith('workers=')), 4))
        name, dt, T = run_cpsat(Y, tl, commute='nocommute' not in flags, s3=s3, workers=workers)
    else:
        solver = next((f.split('=')[1] for f in flags if f.startswith('solver=')), 'cadical195')
        name, dt, T = run_sat(Y, tl, solver=solver, s3=s3)
    ver = verify(T, Y, s3) if T is not None else None
    print({'src': src, 'mode': mode, 'flags': flags, 'status': name, 'time': round(dt, 1), 'verified': ver})
    if T is not None:
        np.save('research/compute/p25/exactpattern_solution_%s.npy' % src.replace('/', '_').replace(':', '_'), T)


if __name__ == '__main__':
    main()
