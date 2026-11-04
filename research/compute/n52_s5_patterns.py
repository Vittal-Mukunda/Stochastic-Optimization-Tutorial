"""J = 5, s = 5 (j = 1,1,1,1,1): which heavy patterns survive the pair-level identities, with c >= 0 and with c >= 1?

Heavy vertices miss only V_+ = {0..4} (Lemma A); a heavy vertex of excess e misses 6 - e of them.  Heavy excess 9.
For each pattern (up to permutations of V_+) the pair-level system of n52_pairlevel.py with free c is solved
with the heavy multiset fixed.
"""
import itertools
import sys
from pathlib import Path

from ortools.sat.python import cp_model

sys.path.insert(0, str(Path(__file__).resolve().parent))
from n52_pairlevel import LAM, NO, NR, partitions  # noqa: E402

POS = range(5)


def feasible(heavy, cmin):
    jv = [1] * 5 + [0] * 6
    m = cp_model.CpModel()
    c = {}
    for u, v in itertools.combinations(range(NR), 2):
        c[u, v] = c[v, u] = m.NewIntVar(cmin, 3 if (u >= 5 or v >= 5) else 4, '')
    for u in range(NR):
        m.Add(sum(c[u, v] for v in range(NR) if v != u) == 20)
    nlight = NO - len(heavy)
    L, Ex = {}, {}
    for u in range(NR):
        hs = [M for M in heavy if u in M]
        L[u] = 20 + jv[u] - len(hs)
        Ex[u] = 5 + 10 * jv[u] - sum(LAM[11 - len(M)] for M in hs)
        if L[u] < 0 or Ex[u] < 0:
            return False
    if sum(L.values()) != 6 * nlight:
        return False
    D, s, k = {}, {}, {}
    for u, v in itertools.combinations(range(NR), 2):
        hs = [M for M in heavy if u in M and v in M]
        D[u, v] = D[v, u] = m.NewIntVar(12, 43, '')
        k[u, v] = k[v, u] = m.NewIntVar(0, NO, '')
        m.Add(D[u, v] == c[u, v] + k[u, v] + len(hs))
        s[u, v] = s[v, u] = m.NewIntVar(0, min(Ex[u], Ex[v]), '')
        m.Add(s[u, v] == 4 * D[u, v] - c[u, v] - 45 - sum(6 - len(M) for M in hs))
        if u >= 5 or v >= 5:
            m.Add(D[u, v] == 12)
    for u in range(NR):
        o = [v for v in range(NR) if v != u]
        m.Add(sum(s[u, v] for v in o) == 2 * Ex[u])
        m.Add(sum(k[u, v] for v in o) == 5 * L[u])
    sol = cp_model.CpSolver()
    sol.parameters.num_workers = 8
    sol.parameters.max_time_in_seconds = 30
    st = sol.Solve(m)
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return {f'{u}{v}': (sol.Value(D[u, v]), sol.Value(c[u, v]), sol.Value(s[u, v]))
                for u, v in itertools.combinations(POS, 2)}
    assert st == cp_model.INFEASIBLE, sol.StatusName(st)
    return False


def canon(heavy):
    best = None
    for p in itertools.permutations(POS):
        key = tuple(sorted(tuple(sorted(p[x] for x in M)) for M in heavy))
        best = key if best is None or key < best else best
    return best


seen = set()
for part in partitions(9, 6, 9):
    choices = [list(itertools.combinations(POS, 6 - e)) for e in part]
    for combo in itertools.product(*choices):
        heavy = [frozenset(M) for M in combo]
        key = canon(heavy)
        if key in seen:
            continue
        seen.add(key)
        f0 = feasible(heavy, 0)
        if f0:
            f1 = feasible(heavy, 1)
            print(part, [sorted(M) for M in heavy], 'c>=0: feasible', '| c>=1:', 'feasible' if f1 else 'INFEASIBLE')
            print('    one c>=0 solution on V_+ pairs (D, c, s):', f0)
print('patterns examined:', len(seen))
