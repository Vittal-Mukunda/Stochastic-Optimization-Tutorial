"""Full local model at a J = 6 survivor, with the full outside vertex X (Q_X = R) as a third anchor.

Setting as in n52_full.py (tight pair P = {a, b}, a -> b, R = D(P), T[R] variable 5-regular S_2, j-vector and heavy
pattern fixed).  The heavy vertex of excess 6 is X itself: every vertex of R beats X.  Every other outside vertex y
(38 of them) is typed by (t, x): t = 0 (y->a, b->y), 1 (a->y, y->b), 2 (a->y, b->y); x = 1 if y -> X, else 0.

Rows, each a consequence of S_4 at N = 52:
  |D(U)| >= nu_|U|                    U subset of R, |U| = 2, 3, 4
  |D(U + a)|, |D(U + b)| >= nu_{|U|+1}  |U| = 1, 2, 3   (dominators: R-dominators of U, plus typed outside vertices)
  |D(U + X)| >= nu_{|U|+1}              |U| = 1, 2, 3   (dominators: R-dominators of U, plus y -> X missing U;
                                                         a, b never beat a vertex of R)
  d^-(a) = 11 + n_{t=0} (+[X->a]) >= 23,  d^-(b) = 12 + n_{t=1} (+[X->b]) >= 23,  d^-(X) >= 23
  M_y contains no N^-_R(z);  (I1) for every r;  heavy pattern fixed;  pair-level rows (D, s, Ex, Lemma A).
Usage: python r8main_full_x.py SHAPE_INDEX PATTERN_INDEX TL WORKERS   (indices into r8main_j6_patterns.json)
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
HERE = Path(__file__).resolve().parent


def model(jvec, heavy_list, tl, workers):
    """heavy_list: list of (e, miss-set) including (6, []) for X."""
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

    others = [(e, frozenset(M)) for e, M in heavy_list if e != 6]
    assert len(others) == len(heavy_list) - 1
    light_sets = [frozenset(S) for S in itertools.combinations(range(NR), 6)]
    types = [(t, x) for t in (0, 1, 2) for x in (0, 1)]
    # light multiplicities
    z = {(S, ty): m.NewIntVar(0, NO, '') for S in light_sets for ty in types}
    # each non-X heavy vertex gets one type (booleans)
    hb = [{ty: m.NewBoolVar('') for ty in types} for _ in others]
    for h in hb:
        m.AddExactlyOne(h.values())
    m.Add(sum(z.values()) == NO - 1 - len(others))
    xa = m.NewBoolVar('X->a')   # X beats a
    xb = m.NewBoolVar('X->b')
    m.AddBoolOr([xa.Not(), xb.Not()])   # X beating both would put X in D(P) = R

    def count(U, pred):
        """number of outside vertices other than X with U subset of M_y and type satisfying pred."""
        Us = set(U)
        expr = sum(z[S, ty] for S in light_sets if Us <= S for ty in types if pred(ty))
        expr += sum(h[ty] for (e, M), h in zip(others, hb) if Us <= M for ty in types if pred(ty))
        return expr

    ALL = lambda ty: True
    for U in itertools.combinations(range(NR), 2):
        m.Add(c[U] + count(U, ALL) >= NU[2])
    for U, e in cR3.items():
        m.Add(e + count(U, ALL) >= NU[3])
    for U, e in cR4.items():
        m.Add(e + count(U, ALL) >= NU[4])
    anchors = [lambda ty: ty[0] == 0, lambda ty: ty[0] == 1, lambda ty: ty[1] == 1]
    for pred in anchors:
        for u in range(NR):
            m.Add(5 + count((u,), pred) >= NU[2])
        for U in itertools.combinations(range(NR), 2):
            m.Add(c[U] + count(U, pred) >= NU[3])
        for U, e in cR3.items():
            m.Add(e + count(U, pred) >= NU[4])
    # degrees of a, b, X
    m.Add(11 + count((), anchors[0]) + xa >= 23)
    m.Add(12 + count((), anchors[1]) + xb >= 23)
    m.Add(11 + count((), anchors[2]) + (1 - xa) + (1 - xb) >= 23)
    # admissibility: M_y contains no N^-_R(z)
    for S in light_sets:
        for zz in range(NR):
            outside = [arc[w, zz] for w in range(NR) if w != zz and w not in S]
            m.Add(sum(z[S, ty] for ty in types) <= NO * sum(outside))
    for (e, M) in others:
        if len(M) == 5:
            for zz in range(NR):
                outside = [arc[w, zz] for w in range(NR) if w != zz and w not in M]
                m.Add(sum(outside) >= 1)
    # (I1)
    for u in range(NR):
        m.Add(1 * 0 + count((u,), ALL) == 20 + jvec[u])
    # pair-level rows
    Ex = {}
    for u in range(NR):
        lam = sum(LAM[11 - len(M)] for e, M in others if u in M)
        Ex[u] = 5 + 10 * jvec[u] - lam
        assert Ex[u] >= 0
    for u, v in itertools.combinations(range(NR), 2):
        E = sum(e for e, M in others if u in M and v in M)
        D = c[u, v] + count((u, v), ALL)
        s = m.NewIntVar(0, min(Ex[u], Ex[v]), '')
        m.Add(s == 4 * D - c[u, v] - 45 - E)
    for u in zero:
        for v in range(NR):
            if v != u:
                m.Add(c[u, v] <= 3)

    sol = cp_model.CpSolver()
    sol.parameters.max_time_in_seconds = tl
    sol.parameters.num_workers = workers
    st = sol.Solve(m)
    info = None
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        info = {
            'out': [[v for v in range(NR) if v != u and sol.BooleanValue(arc[u, v])] for u in range(NR)],
            'light': [[sorted(S), list(ty), sol.Value(z[S, ty])] for S in light_sets for ty in types if sol.Value(z[S, ty])],
            'heavy_types': [[e, sorted(M), [ty for ty in types if sol.BooleanValue(h[ty])][0]] for (e, M), h in zip(others, hb)],
            'X->a': sol.BooleanValue(xa), 'X->b': sol.BooleanValue(xb),
        }
    return sol.StatusName(st), info, sol


def main():
    pats = json.loads((HERE / 'r8main_j6_patterns.json').read_text())
    idx = [int(sys.argv[1])] if len(sys.argv) > 1 and sys.argv[1] != 'all' else range(len(pats))
    tl = float(sys.argv[2]) if len(sys.argv) > 2 else 600
    w = int(sys.argv[3]) if len(sys.argv) > 3 else 4
    for i in idx:
        p = pats[i]
        jv = list(p['shape']) + [0] * (NR - len(p['shape']))
        t0 = time.time()
        st, info, sol = model(jv, p['heavy'], tl, w)
        rec = {'pattern': i, 'shape': p['shape'], 'heavy': p['heavy'], 'status': st,
               'secs': round(time.time() - t0, 1), 'conflicts': sol.NumConflicts(), 'branches': sol.NumBranches()}
        if info:
            rec['solution'] = info
        print(json.dumps(rec), flush=True)
        with open(HERE / 'r8main_full_x.log', 'a') as f:
            f.write(json.dumps(rec) + '\n')


if __name__ == '__main__':
    main()
