"""R8-A audit: solver-free exhaustive check that J <= 5 is impossible for a tight pair at N = 52.

Independent of CP-SAT and of n52_pairlevel.py (no imports from it).  For every J in 0..5, every
j-vector (partition of J placed on V_+ = {0..s-1}), every multiset of heavy miss-sets M (M a subset of
V_+, |M| <= 5, excess e = 6 - |M|, sum of e = 14 - J; Lemma A puts heavy miss-sets inside V_+), it tests
  Ex(u) = 5 + 10 j_u - sum_{M containing u} lambda(11 - |M|) >= 0,
and searches all integer dominator counts D(u, v) >= 12 on pairs inside V_+ with
  sum_{v in V_+} D(u, v) = 12 (s - 1) + 5 j_u - tau_u          (pair-sum, pairs into V_0 have D = 12)
  exists c in [cmin, 4]: 0 <= 4 D - c - 45 - E_both <= min(Ex(u), Ex(v)).
These are exactly the rows used by the hand proofs (R1-C, R3-C, R4-C, N52_TIGHT_J_GE_6.md section 2).
Run with cmin = 1 (S_2 of T[R]) and cmin = 0 (to locate where c >= 1 is needed).

Part 2 checks the double-counting identities numerically on random planted tournaments (no S_4 needed).
"""
import itertools
import json
import random
import sys
from math import comb
from pathlib import Path

LAM = {5: 0, 6: 4, 7: 7, 8: 9, 9: 10, 10: 10, 11: 10}


def partitions(n, maxpart):
    if n == 0:
        yield ()
        return
    for p in range(min(n, maxpart), 0, -1):
        for rest in partitions(n - p, p):
            yield (p,) + rest


def heavy_multisets(s, E):
    subsets = [frozenset(M) for k in range(0, min(s, 5) + 1) for M in itertools.combinations(range(s), k)]

    def rec(start, rem):
        if rem == 0:
            yield ()
            return
        for i in range(start, len(subsets)):
            e = 6 - len(subsets[i])
            if e <= rem:
                for rest in rec(i, rem - e):
                    yield (subsets[i],) + rest
    yield from rec(0, E)


def solve_pairs(s, j, heavy, cmin):
    Ex = [5 + 10 * j[u] - sum(LAM[11 - len(M)] for M in heavy if u in M) for u in range(s)]
    if min(Ex, default=0) < 0:
        return 'Ex<0', None
    tau = [sum(6 - len(M) for M in heavy if u in M) for u in range(s)]
    target = [12 * (s - 1) + 5 * j[u] - tau[u] for u in range(s)]
    pairs = list(itertools.combinations(range(s), 2))
    if not pairs:
        return ('ok', {}) if all(t == 0 for t in target) else ('pairsum', None)
    allowed = {}
    for u, v in pairs:
        eb = sum(6 - len(M) for M in heavy if u in M and v in M)
        cap = min(Ex[u], Ex[v])
        vals = []
        for D in range(12, 44):
            cs = [c for c in range(cmin, 5) if 0 <= 4 * D - c - 45 - eb <= cap]
            if cs:
                vals.append((D, cs))
        allowed[u, v] = vals
    if any(not allowed[p] for p in pairs):
        return 'nopairvalue', None
    rem = target[:]
    left = [s - 1] * s
    lo = {p: allowed[p][0][0] for p in pairs}
    hi = {p: allowed[p][-1][0] for p in pairs}
    assign = {}

    def feasible_rem():
        for u in range(s):
            if left[u] == 0:
                if rem[u] != 0:
                    return False
            else:
                mn = sum(lo[p] for p in pairs if u in p and p not in assign)
                mx = sum(hi[p] for p in pairs if u in p and p not in assign)
                if not mn <= rem[u] <= mx:
                    return False
        return True

    def rec(i):
        if i == len(pairs):
            return all(r == 0 for r in rem)
        u, v = pairs[i]
        for D, cs in allowed[u, v]:
            assign[u, v] = (D, cs)
            rem[u] -= D
            rem[v] -= D
            left[u] -= 1
            left[v] -= 1
            if feasible_rem() and rec(i + 1):
                return True
            rem[u] += D
            rem[v] += D
            left[u] += 1
            left[v] += 1
            del assign[u, v]
        return False

    if not feasible_rem():
        return 'pairsum', None
    if rec(0):
        return 'ok', {f'{u}{v}': assign[u, v] for u, v in pairs}
    return 'nosolution', None


def enumerate_all(cmin):
    out = []
    for J in range(0, 6):
        E = 14 - J
        for jp in partitions(J, J):
            s = len(jp)
            n_conf = 0
            survivors = []
            for heavy in heavy_multisets(s, E):
                if len(heavy) > 39:
                    continue
                n_conf += 1
                st, sol = solve_pairs(s, list(jp), heavy, cmin)
                if st == 'ok':
                    survivors.append({'heavy': [(6 - len(M), sorted(M)) for M in heavy], 'D_c': sol})
            out.append({'J': J, 'j': list(jp), 'configs': n_conf, 'survivors': len(survivors),
                        'examples': survivors[:3]})
    return out


def identity_check(trials=20, seed=1):
    """Random 52-vertex tournaments with a planted tight-pair skeleton: a -> b, R (11 vertices, 5-regular
    circulant) beating a and b, everything else random.  Checks the pure double-counting identities."""
    rng = random.Random(seed)
    worst = 0
    for _ in range(trials):
        N = 52
        a, b = 0, 1
        R = list(range(2, 13))
        O = list(range(13, 52))
        beat = [[False] * N for _ in range(N)]
        beat[a][b] = True
        for i, r in enumerate(R):
            beat[r][a] = beat[r][b] = True
            for d in range(1, 6):
                beat[r][R[(i + d) % 11]] = True
        for y in O:
            ya, yb = rng.choice([(False, False), (False, True), (True, False)])
            beat[y][a], beat[a][y] = ya, not ya
            beat[y][b], beat[b][y] = yb, not yb
        for x, y in itertools.combinations(range(N), 2):
            if not beat[x][y] and not beat[y][x]:
                if rng.random() < 0.5:
                    beat[x][y] = True
                else:
                    beat[y][x] = True
        rng.shuffle(R)
        dom = lambda X: [w for w in range(N) if w not in X and all(beat[w][x] for x in X)]
        assert sorted(dom([a, b])) == sorted(R)
        q = {y: sum(beat[r][y] for r in R) for y in O}
        M = {y: [r for r in R if not beat[r][y]] for y in O}
        jr = {r: sum(beat[w][r] for w in range(N)) - 25 for r in R}
        J = sum(jr.values())
        assert all(sum(1 for y in O if r in M[y]) == 20 + jr[r] for r in R)          # (I1)
        assert sum(q[y] - 5 for y in O) == 14 - J                                     # Lemma I
        for u, v in itertools.combinations(R, 2):
            c = sum(1 for w in R if beat[w][u] and beat[w][v])
            k = sum(1 for y in O if u in M[y] and v in M[y])
            Eb = sum(q[y] - 5 for y in O if u in M[y] and v in M[y])
            Duv = len(dom([u, v]))
            assert Duv == c + k
            assert c <= 4
            s_uv = sum(len(dom([u, v, w])) - 5 for w in R if w not in (u, v))
            assert s_uv == 4 * Duv - c - 45 - Eb
        for u in R:
            tau = sum(q[y] - 5 for y in O if u in M[y])
            assert sum(len(dom([u, v])) for v in R if v != u) == 120 + 5 * jr[u] - tau
            ex = sum(len(dom([u, v, w])) - 5 for v, w in itertools.combinations([x for x in R if x != u], 2))
            assert ex == 30 + sum(comb(10 - q[y], 2) for y in O if u in M[y]) - 225
            if all(q[y] >= 5 for y in O if u in M[y]):
                assert ex == 5 + 10 * jr[u] - sum(LAM[q[y]] for y in O if u in M[y])
            ssum = sum(sum(len(dom([u, v, w])) - 5 for w in R if w not in (u, v)) for v in R if v != u)
            assert ssum == 2 * ex
        worst += 1
    return worst


if __name__ == '__main__':
    res = {'identity_trials_passed': identity_check(int(sys.argv[1]) if len(sys.argv) > 1 else 10)}
    for cmin in (1, 0):
        rows = enumerate_all(cmin)
        res[f'cmin_{cmin}'] = rows
        for r in rows:
            print(cmin, r['J'], r['j'], 'configs', r['configs'], 'survivors', r['survivors'], flush=True)
    (Path(__file__).parent / 'r8a_vplus_enum.json').write_text(json.dumps(res, indent=1))
