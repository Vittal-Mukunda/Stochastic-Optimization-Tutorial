"""R8-B: diagnose which row groups make the fixed-W, all-|Q'_b|=12 set model infeasible.
Runs r8b_vlocal_sets-style models with row groups switched on cumulatively and prints each verdict.
Usage: python r8b_core.py Wfile.json goodsets.json
"""
import itertools
import json
import sys
from pathlib import Path

import numpy as np
from ortools.sat.python import cp_model


def run(A, sets_all, groups, tl=120):
    n = 25
    W = range(n)
    inn = [frozenset(z for z in W if A[z, w]) for w in W]
    sets = list(sets_all)
    if 'V5set' in groups:
        cin2 = [inn[w] & inn[x] for w, x in itertools.combinations(W, 2)]
        sets = [Q for Q in sets if all(Q & c for c in cin2)]
    S = len(sets)
    m = cp_model.CpModel()
    nQ = [m.NewIntVar(0, 26, '') for _ in range(S)]
    p = [m.NewBoolVar('') for _ in range(S)]
    for i in range(S):
        m.Add(nQ[i] >= 1).OnlyEnforceIf(p[i])
        m.Add(nQ[i] == 0).OnlyEnforceIf(p[i].Not())
    m.Add(sum(nQ) == 26)
    e = [m.NewBoolVar('') for _ in W]
    m.Add(sum(e) == 13)
    for w in W:
        m.Add(sum(nQ[i] for i in range(S) if w in sets[i]) == 13 - e[w])
    if 'V4' in groups or 'V5pair' in groups:
        for i, j in itertools.combinations(range(S), 2):
            I = sets[i] & sets[j]
            bad = ('V4' in groups and len(I) < 5) or ('V5pair' in groups and any(not (I & inn[w]) for w in W))
            if bad:
                m.AddBoolOr([p[i].Not(), p[j].Not()])
    Dp = {}
    if 'V6pair' in groups or 'V7' in groups:
        for X in itertools.combinations(W, 2):
            kw = int(np.all(A[:, list(X)] == 1, axis=1).sum())
            Dp[X] = kw + sum(nQ[i] for i in range(S) if not (sets[i] & set(X)))
            m.Add(Dp[X] >= 12)
            if 'V7' in groups:
                u, w = X
                head = w if A[u, w] else u
                m.Add(Dp[X] == 12).OnlyEnforceIf(e[head].Not())
    s = cp_model.CpSolver()
    s.parameters.max_time_in_seconds = tl
    s.parameters.num_workers = 3
    st = s.Solve(m)
    return S, s.StatusName(st), round(s.WallTime(), 1)


def main():
    A = np.array(json.loads(Path(sys.argv[1]).read_text())['A'], dtype=int)
    sets = [frozenset(s) for s in json.loads(Path(sys.argv[2]).read_text())['12']['sets']]
    seqs = [[], ['V5set'], ['V4'], ['V6pair'], ['V6pair', 'V7'], ['V4', 'V5pair'], ['V5set', 'V4', 'V5pair'],
            ['V5set', 'V6pair', 'V7'], ['V4', 'V6pair', 'V7']]
    out = []
    for g in seqs:
        S, st, t = run(A, sets, set(g))
        out.append({'groups': g, 'sets': S, 'status': st, 'secs': t})
        print(json.dumps(out[-1]), flush=True)
    Path(__file__).parent.joinpath(f'r8b_core_{Path(sys.argv[1]).stem}.json').write_text(json.dumps(out))


if __name__ == '__main__':
    main()
