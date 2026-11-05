#!/usr/bin/env python3
"""[experiment] Search for an S_k tournament on N vertices with a prescribed automorphism sigma of odd prime order p
(c cycles of length p plus f fixed points, c*p + f = N).

Arc variables are shared along sigma-orbits; the S_k clause ("some w beats all of S") is imposed for one representative
of each sigma-orbit of k-sets: OR_w d_{w,S}, d_{w,S} -> e_{w,{a,b}} and d_{w,S} -> e_{w,{c,d}} (k = 4) where
e_{w,P} <-> [w -> a][w -> b]; for k = 3, d_{w,S} -> e_{w,{a,b}}, d_{w,S} -> [w -> c].
Optional redundant counting rows (flag F, only meaningful for k = 4, N = 52; consequences of S_4 proved in the repo,
used for pruning only -- a SAT answer is re-verified from scratch): every triple has >= 5 dominators, every pair >= 11.
Clauses are streamed into the solver (no big Python lists).

Usage: python3 sk_symsat.py N k p c f time_limit [solver=cadical195] [F]
"""
import itertools
import multiprocessing as mp
import sys
import time

import numpy as np
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
from pysat.solvers import Solver


def main():
    """pysat does not release the GIL while solving, so a timer thread cannot interrupt it: run the whole job in a
    child process and kill it at the time limit."""
    tl = float(sys.argv[6])
    proc = mp.Process(target=job, args=(sys.argv[1:],))
    t0 = time.time()
    proc.start()
    proc.join(tl)
    if proc.is_alive():
        proc.terminate()
        proc.join()
        N, k, p, c, f = (int(a) for a in sys.argv[1:6])
        print({'N': N, 'k': k, 'sigma': '%d^%d 1^%d' % (p, c, f), 'F': 'F' in sys.argv[7:], 'status': 'UNKNOWN',
               'time_limit': tl, 'time': round(time.time() - t0, 1)}, flush=True)


def job(argv):
    N, k, p, c, f = (int(a) for a in argv[0:5])
    flags = argv[6:]
    solver = next((a.split('=')[1] for a in flags if a.startswith('solver=')), 'cadical195')
    useF = 'F' in flags
    assert c * p + f == N and k in (3, 4)
    sig = list(range(N))
    for i in range(c):
        for t in range(p):
            sig[i * p + t] = i * p + (t + 1) % p

    def orbit(tup):
        out, cur = [], tup
        while True:
            out.append(cur)
            cur = tuple(sig[v] for v in cur)
            if cur == tup:
                return out

    pool = IDPool()
    rep = {}

    def arc(a, b):
        r = rep.get((a, b))
        if r is not None:
            return r
        orb = orbit((a, b))
        v = pool.id(('x', min(orb)))
        for (x, y) in orb:
            rep[(x, y)] = v
            rep[(y, x)] = -v
        return rep[(a, b)]

    for a, b in itertools.combinations(range(N), 2):
        arc(a, b)
    s = Solver(name=solver)
    ncl = 0
    e = {}

    def epair(w, a, b):
        key = (w, a, b) if a < b else (w, b, a)
        v = e.get(key)
        if v is None:
            v = pool.id(('e',) + key)
            e[key] = v
            s.add_clause([-v, arc(w, a)])
            s.add_clause([-v, arc(w, b)])
            s.add_clause([v, -arc(w, a), -arc(w, b)])
        return v

    t0 = time.time()
    reps = 0
    for S in itertools.combinations(range(N), k):
        if min(tuple(sorted(o)) for o in orbit(S)) != S:
            continue
        reps += 1
        lits = []
        for w in range(N):
            if w in S:
                continue
            d = pool.id(('d', w) + S)
            if k == 4:
                s.add_clause([-d, epair(w, S[0], S[1])])
                s.add_clause([-d, epair(w, S[2], S[3])])
            else:
                s.add_clause([-d, epair(w, S[0], S[1])])
                s.add_clause([-d, arc(w, S[2])])
            ncl += 2
            lits.append(d)
        s.add_clause(lits)
        ncl += 1
    if useF:
        for lo, size in ((5, 3), (11, 2)):
            for S in itertools.combinations(range(N), size):
                if min(tuple(sorted(o)) for o in orbit(S)) != S:
                    continue
                lits = []
                for w in range(N):
                    if w in S:
                        continue
                    if size == 3:
                        t = pool.id(('t', w) + S)
                        s.add_clause([-t, epair(w, S[0], S[1])])
                        s.add_clause([-t, arc(w, S[2])])
                        lits.append(t)
                    else:
                        lits.append(epair(w, S[0], S[1]))
                for cl in CardEnc.atleast(lits, lo, vpool=pool, encoding=EncType.seqcounter).clauses:
                    s.add_clause(cl)
                    ncl += 1
    tbuild = time.time() - t0
    t1 = time.time()
    r = s.solve()
    dt = time.time() - t1
    rec = {'N': N, 'k': k, 'sigma': '%d^%d 1^%d' % (p, c, f), 'F': useF, 'solver': solver, 'ksets_reps': reps,
           'clauses_approx': ncl, 'build_s': round(tbuild, 1), 'status': {None: 'UNKNOWN', False: 'UNSAT', True: 'SAT'}[r],
           'time': round(dt, 1)}
    if r:
        model = set(l for l in s.get_model() if l > 0)
        T = np.zeros((N, N), dtype=np.int64)
        for a in range(N):
            for b in range(N):
                if a != b:
                    l = arc(a, b)
                    if (l > 0 and l in model) or (l < 0 and -l not in model):
                        T[a, b] = 1
        # independent verification with integer bitmasks
        inn = [sum(1 << w for w in range(N) if T[w, v]) for v in range(N)]
        ok = all(T[a, b] + T[b, a] == 1 for a in range(N) for b in range(N) if a != b)
        bad = 0
        for S in itertools.combinations(range(N), k):
            m = inn[S[0]]
            for v in S[1:]:
                m &= inn[v]
            if not m:
                bad += 1
        rec['verified_tournament'] = ok
        rec['undominated_ksets'] = bad
        fn = 'research/compute/p25/S%d_N%d_sym_%d_%d_%d.npy' % (k, N, p, c, f)
        np.save(fn, T)
        rec['saved'] = fn
    s.delete()
    print(rec, flush=True)


if __name__ == '__main__':
    main()
