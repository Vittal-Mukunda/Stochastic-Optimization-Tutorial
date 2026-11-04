"""Full local model of a tight pair in an S_4 tournament on 52 vertices, T[R] variable, j-vector fixed.

Adds to n52_pairlevel.py the individual outside vertices (as multiplicities of miss-sets M_y = R \\ Q_y, typed by
their arcs to a and b, with a -> b), and the rows
  |D(U)| >= nu_|U|        for U subset of R, |U| = 2, 3, 4            (nu_2 = 11, nu_3 = 5, nu_4 = 1)
  |D(U + a)|, |D(U + b)| >= nu_{|U|+1}  for |U| = 1, 2, 3   (type 0: y -> a, b -> y; type 1: a -> y, y -> b; type 2)
  d^-(a) = 11 + n_0 >= 23,  d^-(b) = 12 + n_1 >= 23
  M_y contains no N^-_R(z)                                  (Lemma 1.2 for the triple {a, b, z})
Usage: python n52_full.py J j0,j1,... [time_limit] [workers]     or     python n52_full.py --survivors LOG [tl] [w]
"""
import itertools
import json
import sys
import time
from pathlib import Path

from ortools.sat.python import cp_model

NR, NO = 11, 39
LAM = {6: 4, 7: 7, 8: 9, 9: 10, 10: 10, 11: 10}
NU = {2: 11, 3: 5, 4: 1}


def model(jvec, tl=300.0, workers=16):
    J = sum(jvec)
    pos = [r for r in range(NR) if jvec[r] > 0]
    zero = [r for r in range(NR) if jvec[r] == 0]
    m = cp_model.CpModel()
    arc = {}
    for u, v in itertools.combinations(range(NR), 2):
        arc[u, v] = m.NewBoolVar('')
        arc[v, u] = arc[u, v].Not()
    for u in range(NR):
        m.Add(sum(arc[u, v] for v in range(NR) if v != u) == 5)

    def dom_count(U):
        """number of w in R \\ U beating every vertex of U (as a linear expression of aux booleans)."""
        terms = []
        for w in range(NR):
            if w in U:
                continue
            p = m.NewBoolVar('')
            lits = [arc[w, u] for u in U]
            m.AddBoolAnd(lits).OnlyEnforceIf(p)
            m.AddBoolOr([l.Not() for l in lits]).OnlyEnforceIf(p.Not())
            terms.append(p)
        return sum(terms)

    c = {}
    for u, v in itertools.combinations(range(NR), 2):
        c[u, v] = c[v, u] = m.NewIntVar(1, 4, '')
        m.Add(c[u, v] == dom_count((u, v)))
    cR3 = {U: dom_count(U) for U in itertools.combinations(range(NR), 3)}
    cR4 = {U: dom_count(U) for U in itertools.combinations(range(NR), 4)}

    heavy_sets = [frozenset(M) for size in range(6) for M in itertools.combinations(pos, size)]
    light_sets = [frozenset(S) for S in itertools.combinations(range(NR), 6)]
    allsets = [(M, 'h') for M in heavy_sets] + [(S, 'l') for S in light_sets]
    x = {(M, t): m.NewIntVar(0, NO if kind == 'l' else 14 - J, '') for M, kind in allsets for t in (0, 1, 2)}
    tot = {M: sum(x[M, t] for t in (0, 1, 2)) for M, _ in allsets}
    n = {M: tot[M] for M in heavy_sets}
    m.Add(sum(tot.values()) == NO)
    m.Add(sum(n[M] * (6 - len(M)) for M in heavy_sets) == 14 - J)
    m.Add(sum(x[M, 0] for M, _ in allsets) >= 12)
    m.Add(sum(x[M, 1] for M, _ in allsets) >= 11)

    inn = {z: [w for w in range(NR) if w != z] for z in range(NR)}
    for M, kind in allsets:
        if len(M) < 5:
            continue
        for z in range(NR):
            outside = [arc[w, z] for w in inn[z] if w not in M]
            if not outside:
                m.Add(tot[M] == 0)
            else:
                m.Add(tot[M] <= NO * sum(outside))

    def missing(U, types=(0, 1, 2)):
        Us = set(U)
        return sum(x[M, t] for M, _ in allsets if Us <= M for t in types)

    for U in itertools.combinations(range(NR), 2):
        m.Add(c[U] + missing(U) >= NU[2])
    for U, e in cR3.items():
        m.Add(e + missing(U) >= NU[3])
    for U, e in cR4.items():
        m.Add(e + missing(U) >= NU[4])
    for t in (0, 1):
        for u in range(NR):
            m.Add(5 + missing((u,), (t,)) >= NU[2])
        for U in itertools.combinations(range(NR), 2):
            m.Add(c[U] + missing(U, (t,)) >= NU[3])
        for U, e in cR3.items():
            m.Add(e + missing(U, (t,)) >= NU[4])

    Ex = {}
    for u in range(NR):
        m.Add(sum(tot[M] for M, _ in allsets if u in M) == 20 + jvec[u])
        Ex[u] = m.NewIntVar(0, 5 + 10 * jvec[u], '')
        m.Add(Ex[u] == 5 + 10 * jvec[u] - sum(n[M] * LAM[11 - len(M)] for M in heavy_sets if u in M))
    D, s = {}, {}
    for u, v in itertools.combinations(range(NR), 2):
        D[u, v] = D[v, u] = m.NewIntVar(12, 43, '')
        m.Add(D[u, v] == c[u, v] + missing((u, v)))
        hs = [M for M in heavy_sets if u in M and v in M]
        s[u, v] = s[v, u] = m.NewIntVar(0, 5 + 10 * max(jvec[u], jvec[v]), '')
        m.Add(s[u, v] == 4 * D[u, v] - c[u, v] - 45 - sum(n[M] * (6 - len(M)) for M in hs))
        m.Add(s[u, v] <= Ex[u])
        m.Add(s[u, v] <= Ex[v])
    for u in range(NR):
        m.Add(sum(s[u, v] for v in range(NR) if v != u) == 2 * Ex[u])
    for u in zero:
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
            'out': [[v for v in range(NR) if v != u and sol.BooleanValue(arc[u, v])] for u in range(NR)],
            'sets': [[sorted(M), t, sol.Value(x[M, t])] for M, _ in allsets for t in (0, 1, 2) if sol.Value(x[M, t])],
        }
    return sol.StatusName(st), info


def main():
    if sys.argv[1] == '--survivors':
        raw = open(sys.argv[2], 'rb').read()
        txt = raw.decode('utf-16') if raw[:2] in (b'\xff\xfe', b'\xfe\xff') else raw.decode()
        todo = [json.loads(l) for l in txt.splitlines() if l.startswith('{')]
        todo = [(r['J'], r['j']) for r in todo if r['status'] != 'INFEASIBLE']
        tl = float(sys.argv[3]) if len(sys.argv) > 3 else 300.0
        w = int(sys.argv[4]) if len(sys.argv) > 4 else 16
    else:
        todo = [(int(sys.argv[1]), [int(t) for t in sys.argv[2].split(',')])]
        tl = float(sys.argv[3]) if len(sys.argv) > 3 else 300.0
        w = int(sys.argv[4]) if len(sys.argv) > 4 else 16
    for J, part in todo:
        jvec = list(part) + [0] * (NR - len(part))
        t0 = time.time()
        st, info = model(jvec, tl, w)
        rec = {'J': J, 'j': part, 'status': st, 'secs': round(time.time() - t0, 1)}
        if info:
            rec |= info
        print(json.dumps(rec), flush=True)


if __name__ == '__main__':
    main()
