"""J = 6 at order 52: which heavy patterns survive the pair-level identities (free c in [1,4], row sums 20)?

j-shapes (2,2,1,1), (2,1,1,1,1), (1,1,1,1,1,1) are placed on vertices 0..s-1; V_0 = the rest.  Heavy excess 14 - 6 = 8.
Heavy vertices miss only V_+ (Lemma A); a heavy vertex of excess e misses 6 - e vertices of V_+.
Patterns are enumerated up to permutations of V_+ preserving j.  For each, the pair-level system (same rows as
n52_pairlevel.py with free c) is solved with the heavy multiset fixed.  Output: research/compute/r8main_j6_patterns.json
"""
import itertools
import json
import sys
from pathlib import Path

from ortools.sat.python import cp_model

sys.path.insert(0, str(Path(__file__).resolve().parent))
from n52_pairlevel import LAM, NO, NR, partitions  # noqa: E402


def solve_fixed(jv, heavy, cmin=1, workers=3):
    pos = [r for r in range(NR) if jv[r] > 0]
    m = cp_model.CpModel()
    c = {}
    for u, v in itertools.combinations(range(NR), 2):
        hi = 3 if (jv[u] == 0 or jv[v] == 0) else 4
        c[u, v] = c[v, u] = m.NewIntVar(cmin, hi, '')
    for u in range(NR):
        m.Add(sum(c[u, v] for v in range(NR) if v != u) == 20)
    L, Ex = {}, {}
    for u in range(NR):
        hs = [M for M in heavy if u in M]
        L[u] = 20 + jv[u] - len(hs)
        Ex[u] = 5 + 10 * jv[u] - sum(LAM[11 - len(M)] for M in hs)
        if L[u] < 0 or Ex[u] < 0:
            return None
    if sum(L.values()) != 6 * (NO - len(heavy)):
        return None
    D, s = {}, {}
    for u, v in itertools.combinations(range(NR), 2):
        hs = [M for M in heavy if u in M and v in M]
        E = sum(6 - len(M) for M in hs)
        D[u, v] = D[v, u] = m.NewIntVar(12, 43, '')
        m.Add(D[u, v] >= c[u, v] + len(hs))
        s[u, v] = s[v, u] = m.NewIntVar(0, min(Ex[u], Ex[v]), '')
        m.Add(s[u, v] == 4 * D[u, v] - c[u, v] - 45 - E)
        if jv[u] == 0 or jv[v] == 0:
            m.Add(D[u, v] == 12)
    for u in range(NR):
        o = [v for v in range(NR) if v != u]
        m.Add(sum(s[u, v] for v in o) == 2 * Ex[u])
        hs = [M for M in heavy if u in M]
        m.Add(sum(D[u, v] for v in o) == 120 + 5 * jv[u] - sum(6 - len(M) for M in hs))
    sol = cp_model.CpSolver()
    sol.parameters.num_workers = workers
    sol.parameters.max_time_in_seconds = 60
    st = sol.Solve(m)
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return {f'{u},{v}': [sol.Value(D[u, v]), sol.Value(c[u, v]), sol.Value(s[u, v])]
                for u, v in itertools.combinations(pos, 2)}
    assert st == cp_model.INFEASIBLE, sol.StatusName(st)
    return None


def canon(jv, heavy, pos):
    best = None
    for p in itertools.permutations(pos):
        if any(jv[p[i]] != jv[pos[i]] for i in range(len(pos))):
            continue
        mp = dict(zip(pos, p))
        key = tuple(sorted(tuple(sorted(mp[x] for x in M)) for M in heavy))
        best = key if best is None or key < best else best
    return best


def main():
    out = []
    for shape in ((2, 2, 1, 1), (2, 1, 1, 1, 1), (1, 1, 1, 1, 1, 1)):
        jv = list(shape) + [0] * (NR - len(shape))
        pos = list(range(len(shape)))
        seen = set()
        nzero = NR - len(pos)
        tau_cap = {u: 120 + 5 * jv[u] - 12 * nzero - 12 * (len(pos) - 1) for u in pos}
        for part in partitions(8, 6, 8):
            if any(6 - e > len(pos) for e in part):
                continue
            groups = {}
            for e in part:
                groups[e] = groups.get(e, 0) + 1
            per_e = [list(itertools.combinations_with_replacement(
                [frozenset(M) for M in itertools.combinations(pos, 6 - e)], k)) for e, k in groups.items()]
            for combo in itertools.product(*per_e):
                heavy = [M for grp in combo for M in grp]
                tau = {u: sum(6 - len(M) for M in heavy if u in M) for u in pos}
                lam = {u: sum(LAM[11 - len(M)] for M in heavy if u in M) for u in pos}
                if any(tau[u] > tau_cap[u] or lam[u] > 5 + 10 * jv[u] for u in pos):
                    continue
                key = canon(jv, heavy, pos)
                if key in seen:
                    continue
                seen.add(key)
                f1 = solve_fixed(jv, heavy, 1)
                if f1:
                    rec = {'shape': shape, 'heavy': [[6 - len(M), sorted(M)] for M in heavy], 'D_c_s': f1}
                    out.append(rec)
                    print(shape, rec['heavy'], flush=True)
        print(shape, 'patterns examined', len(seen), flush=True)
    (Path(__file__).parent / 'r8main_j6_patterns.json').write_text(json.dumps(out, indent=1))


if __name__ == '__main__':
    main()
