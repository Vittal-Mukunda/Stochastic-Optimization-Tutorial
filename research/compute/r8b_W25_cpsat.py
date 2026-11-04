"""R8-B: CP-SAT search for a tournament W on 25 vertices that is 12-regular and in which every pair has >= 5 common
in-neighbours (optionally also S_3: every triple has a common in-neighbour).  This is the structure forced on
T[N^-(v)] when d^-(v) = 25 in the no-tight branch.

Usage: python r8b_W25_cpsat.py [--s3] [--time T] [--workers K] [--cmax C]
  --cmax C additionally bounds every common-in-neighbour count by C (C = 6 is forced by nothing; exploration only).
"""
import argparse
import itertools
import json
from pathlib import Path

import numpy as np
from ortools.sat.python import cp_model

N = 25


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--s3', action='store_true')
    ap.add_argument('--time', type=float, default=600)
    ap.add_argument('--workers', type=int, default=3)
    ap.add_argument('--cmax', type=int, default=0)
    ap.add_argument('--sym', default='', help="'z5': x -> x+5 mod 25 (5 orbits of size 5); 'z3': 8 orbits of size 3 + fixed 24")
    a = ap.parse_args()
    m = cp_model.CpModel()
    V = range(N)
    arc = {}
    for u, w in itertools.combinations(V, 2):
        arc[u, w] = m.NewBoolVar(f'a{u}_{w}')
        arc[w, u] = arc[u, w].Not()
    for u in V:
        m.Add(sum(arc[w, u] for w in V if w != u) == 12)
    if a.sym:
        if a.sym == 'z5':
            sig = lambda x: (x + 5) % 25
        else:
            sig = lambda x: 24 if x == 24 else 3 * (x // 3) + (x % 3 + 1) % 3
        for u, w in itertools.combinations(V, 2):
            m.Add(arc[u, w] == arc[sig(u), sig(w)])
    else:
        m.AddBoolAnd([arc[0, w] for w in range(1, 13)])     # vertex 0 beats 1..12 (relabelling)
    both = {}
    for u, w in itertools.combinations(V, 2):
        terms = []
        for z in V:
            if z in (u, w):
                continue
            b = m.NewBoolVar('')
            m.AddBoolAnd([arc[z, u], arc[z, w]]).OnlyEnforceIf(b)
            m.AddBoolOr([arc[z, u].Not(), arc[z, w].Not()]).OnlyEnforceIf(b.Not())
            terms.append(b)
            both[z, u, w] = b
        m.Add(sum(terms) >= 5)
        if a.cmax:
            m.Add(sum(terms) <= a.cmax)
    if a.s3:
        for u, w, y in itertools.combinations(V, 3):
            lits = []
            for z in V:
                if z in (u, w, y):
                    continue
                b = m.NewBoolVar('')
                m.AddImplication(b, both[z, u, w])
                m.AddImplication(b, arc[z, y])
                lits.append(b)
            m.AddBoolOr(lits)
    s = cp_model.CpSolver()
    s.parameters.max_time_in_seconds = a.time
    s.parameters.num_workers = a.workers
    st = s.Solve(m)
    rec = {'s3': a.s3, 'cmax': a.cmax, 'status': s.StatusName(st), 'secs': round(s.WallTime(), 1)}
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        A = np.zeros((N, N), dtype=int)
        for u, w in itertools.combinations(V, 2):
            if s.BooleanValue(arc[u, w]):
                A[u, w] = 1
            else:
                A[w, u] = 1
        C = A.T @ A
        rec['A'] = A.tolist()
        rec['c_hist'] = {int(k): int(v) for k, v in zip(*np.unique(C[np.triu_indices(N, 1)], return_counts=True))}
        s3 = all((A[:, u] & A[:, w] & A[:, y]).any() for u, w, y in itertools.combinations(V, 3))
        rec['S3_check'] = bool(s3)
    print(json.dumps({k: v for k, v in rec.items() if k != 'A'}))
    tag = ('s3' if a.s3 else 'nos3') + (f'_c{a.cmax}' if a.cmax else '') + (f'_{a.sym}' if a.sym else '')
    (Path(__file__).parent / f'r8b_W25_cpsat_{tag}.json').write_text(json.dumps(rec))


if __name__ == '__main__':
    main()
