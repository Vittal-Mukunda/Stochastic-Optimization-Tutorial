"""Pair-level relaxation of a tight pair in an S_4 tournament on 52 vertices, with T[R] as variables.

Setting: P tight, R = D(P) (11 vertices, T[R] 5-regular, S_2), O = 39 outside vertices, Q_y = R n N^-(y),
miss-set M_y = R \\ Q_y, e_y = q_y - 5 = 6 - |M_y| >= 0.  d^-(r) = 25 + j_r, j_r >= 0, J = sum j_r.

Rows (each a consequence of S_4 at N = 52; no case analysis on J is assumed):
  T[R] 5-regular; c(u,v) = #common in-neighbours in R >= 1           (S_2: {a,b,u,v} has a dominator, in R)
  #{y : r not in Q_y} = 20 + j_r                                      (I1)
  sum_y e_y = 14 - J                                                   (Lemma I)
  Lemma A: j_u = 0  =>  u in Q_y for every y with e_y >= 1, c(u,v) <= 3, |D(u,v)| = 12 for all v
  |D(u,v)| = c(u,v) + #{y : u, v in M_y}
  s(u,v) := sum_{w} (|D(u,v,w)| - 5) = 4|D(u,v)| - c(u,v) - 45 - E_both(u,v),  0 <= s(u,v) <= Ex(u)
  sum_v s(u,v) = 2 Ex(u),  Ex(u) = 5 + 10 j_u - sum_{y : u in M_y} lambda(q_y) >= 0
The light vertices (e_y = 0, |M_y| = 6) enter only through their pair counts k(u,v) >= 0 with
sum_v k(u,v) = 5 L_u and sum_u L_u = 6 * #light.

Usage: python n52_pairlevel.py [Jmin Jmax] [time_limit] [workers]
"""
import itertools
import json
import sys
import time
from pathlib import Path

from ortools.sat.python import cp_model

NR, NO = 11, 39
LAM = {6: 4, 7: 7, 8: 9, 9: 10, 10: 10, 11: 10}


def partitions(n, maxpart, maxlen):
    if n == 0:
        yield ()
        return
    if maxlen == 0:
        return
    for p in range(min(n, maxpart), 0, -1):
        for rest in partitions(n - p, p, maxlen - 1):
            yield (p,) + rest


def model(jvec, tl=60.0, workers=8, use_s2=True, use_lemma_a=True, free_c=False):
    J = sum(jvec)
    pos = [r for r in range(NR) if jvec[r] > 0]
    zero = [r for r in range(NR) if jvec[r] == 0]
    m = cp_model.CpModel()
    arc = {}
    c = {}
    if free_c:
        for u, v in itertools.combinations(range(NR), 2):
            c[u, v] = c[v, u] = m.NewIntVar(1 if use_s2 else 0, 4, f'c{u}_{v}')
        for u in range(NR):
            m.Add(sum(c[u, v] for v in range(NR) if v != u) == 20)
    for u, v in itertools.combinations(range(NR), 2):
        if free_c:
            break
        arc[u, v] = m.NewBoolVar(f'a{u}_{v}')
        arc[v, u] = arc[u, v].Not()
    for u in range(NR):
        if free_c:
            break
        m.Add(sum(arc[u, v] for v in range(NR) if v != u) == 5)
    for u, v in itertools.combinations(range(NR), 2):
        if free_c:
            break
        terms = []
        for w in range(NR):
            if w in (u, v):
                continue
            p = m.NewBoolVar('')
            m.AddBoolAnd([arc[w, u], arc[w, v]]).OnlyEnforceIf(p)
            m.AddBoolOr([arc[w, u].Not(), arc[w, v].Not()]).OnlyEnforceIf(p.Not())
            terms.append(p)
        c[u, v] = c[v, u] = m.NewIntVar(1 if use_s2 else 0, 4, f'c{u}_{v}')
        m.Add(c[u, v] == sum(terms))

    heavy_sets = []
    support = pos if use_lemma_a else list(range(NR))
    for size in range(0, 6):
        for M in itertools.combinations(support, size):
            heavy_sets.append(frozenset(M))
    n = {M: m.NewIntVar(0, 14 - J, '') for M in heavy_sets}
    m.Add(sum(n[M] * (6 - len(M)) for M in heavy_sets) == 14 - J)
    nheavy = sum(n.values()) if heavy_sets else 0
    nlight = m.NewIntVar(0, NO, 'nlight')
    m.Add(nlight + nheavy == NO)

    Ex, L = {}, {}
    for u in range(NR):
        hs = [M for M in heavy_sets if u in M]
        Ex[u] = m.NewIntVar(0, 5 + 10 * jvec[u], f'Ex{u}')
        m.Add(Ex[u] == 5 + 10 * jvec[u] - sum(n[M] * LAM[11 - len(M)] for M in hs))
        L[u] = m.NewIntVar(0, 20 + jvec[u], f'L{u}')
        m.Add(L[u] + sum(n[M] for M in hs) == 20 + jvec[u])
    m.Add(sum(L.values()) == 6 * nlight)

    D, k, s = {}, {}, {}
    for u, v in itertools.combinations(range(NR), 2):
        hs = [M for M in heavy_sets if u in M and v in M]
        D[u, v] = D[v, u] = m.NewIntVar(12, 43, '')
        k[u, v] = k[v, u] = m.NewIntVar(0, NO, '')
        m.Add(D[u, v] == c[u, v] + k[u, v] + sum(n[M] for M in hs))
        s[u, v] = s[v, u] = m.NewIntVar(0, 5 + 10 * max(jvec[u], jvec[v]), '')
        m.Add(s[u, v] == 4 * D[u, v] - c[u, v] - 45 - sum(n[M] * (6 - len(M)) for M in hs))
        m.Add(s[u, v] <= Ex[u])
        m.Add(s[u, v] <= Ex[v])
    for u in range(NR):
        others = [v for v in range(NR) if v != u]
        m.Add(sum(s[u, v] for v in others) == 2 * Ex[u])
        m.Add(sum(k[u, v] for v in others) == 5 * L[u])
        hs = [M for M in heavy_sets if u in M]
        m.Add(sum(D[u, v] for v in others) == 120 + 5 * jvec[u] - sum(n[M] * (6 - len(M)) for M in hs))
    for u in (zero if use_lemma_a else []):
        for v in range(NR):
            if v != u:
                m.Add(c[u, v] <= 3)
                m.Add(D[u, v] == 12)

    sol = cp_model.CpSolver()
    sol.parameters.max_time_in_seconds = tl
    sol.parameters.num_workers = workers
    st = sol.Solve(m)
    info = None
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        info = {
            'heavy': sorted([(6 - len(M), sorted(M), sol.Value(n[M])) for M in heavy_sets if sol.Value(n[M])],
                            key=lambda t: -t[0]),
            'out': [[v for v in range(NR) if v != u and sol.BooleanValue(arc[u, v])] for u in range(NR)] if arc else None,
            'c': {f'{u},{v}': sol.Value(c[u, v]) for u, v in itertools.combinations(range(NR), 2)},
        }
    return sol.StatusName(st), info


def main():
    Jmin = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    Jmax = int(sys.argv[2]) if len(sys.argv) > 2 else 14
    tl = float(sys.argv[3]) if len(sys.argv) > 3 else 60.0
    w = int(sys.argv[4]) if len(sys.argv) > 4 else 8
    results = []
    for J in range(Jmin, Jmax + 1):
        for part in partitions(J, J, NR):
            jvec = list(part) + [0] * (NR - len(part))
            t0 = time.time()
            st, info = model(jvec, tl, w)
            rec = {'J': J, 'j': list(part), 'status': st, 'secs': round(time.time() - t0, 1)}
            if info:
                rec['heavy'] = info['heavy']
            print(json.dumps(rec), flush=True)
            results.append(rec | ({'out': info['out']} if info else {}))
    tag = f'{Jmin}_{Jmax}'
    (Path(__file__).parent / f'n52_pairlevel_{tag}.json').write_text(json.dumps(results, indent=1))


if __name__ == '__main__':
    main()
