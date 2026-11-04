"""R8-E: independent pair-level verifier for tight pairs at N = 52 (no CP-SAT, no import of n52_pairlevel.py).

Setting (research/AGENT_TASKS/BRIEF_R8.md): R = D(P), |R| = 11, T[R] 5-regular with S_2; O has 39 vertices;
y in O has miss-set M_y = R \\ N^-(y), |M_y| <= 6, excess e_y = 6 - |M_y|; heavy means e_y >= 1.
d^-(r) = 25 + j_r, J = sum j_r, V_+ = {j > 0}, V_0 = {j = 0}.

The pair-level system (same rows as the brief; derived here, not copied):
  (I1)  #{y : r in M_y} = 20 + j_r
  (LI)  sum_y e_y = 14 - J
  (A)   r in V_0  =>  r not in M_y for heavy y, c(r, v) <= 3 and |D(r, v)| = 12 for all v
  (PD)  |D(u, v)| = c(u, v) + #{y : u, v in M_y}
  (S)   s(u, v) = 4|D(u, v)| - c(u, v) - 45 - E_both(u, v),  0 <= s(u, v) <= min(Ex(u), Ex(v)),
        sum_v s(u, v) = 2 Ex(u),  Ex(u) = 5 + 10 j_u - sum_{y : u in M_y} lam(q_y) >= 0
  light y (e_y = 0) only through pair counts k(u, v) >= 0 with sum_v k(u, v) = 5 L_u, sum_u L_u = 6 #light.

Decision method.  Heavy miss-sets lie in V_+ (A), so a heavy pattern H is a multiset of subsets M of V_+ with
sum n_M (6 - |M|) = 14 - J; these are enumerated exhaustively.  Given H, every quantity except D on pairs inside
V_+ is determined:
  L_u = 20 + j_u - sum_{M ni u} n_M,  Ex_u as above,  h(u,v) = sum_{M sup {u,v}} n_M,  E(u,v) = sum_{M sup {u,v}} n_M e_M,
  D = 12 on every pair meeting V_0, so k = 12 - c there and s = 3 - c,
  for u, v in V_+:  k = D - c - h,  s = 4D - c - 45 - E.
Eliminating k and s, the rows sum_v k(u,v) = 5 L_u become  sum_{v in V_+} D(u, v) = rho_u :=
120 + 5 j_u - tau_u - 12 |V_0|  (tau_u = sum_{M ni u} n_M e_M), and sum_v s(u, v) = 2Ex(u) is then an identity because
2 lam(11 - m) = (6 - m)(m + 3) for m = 1..5; sum_u L_u = 6 #light is equivalent to (LI).  What remains:
  (P1) Ex_u >= 0, L_u >= 0 for u in V_+;
  (P2) for u in V_0, v in V_+: c(u, v) <= 3 and 3 - c(u, v) <= Ex_v   (s(u, v) <= Ex(v));
  (P3) integer D(u, v), u, v in V_+, in  [lo, hi]  with
       lo = max(12, c + h, ceil((c + 45 + E) / 4)),  hi = min(43, 39 + c + h, floor((c + 45 + E + min(Ex_u, Ex_v)) / 4)),
       and row sums rho_u.
"""
import itertools
import math

NR, NO = 11, 39
LAM = {5: 0, 6: 4, 7: 7, 8: 9, 9: 10, 10: 10, 11: 10}
for _m in range(1, 6):
    assert 2 * LAM[11 - _m] == (6 - _m) * (_m + 3)


# ---------------------------------------------------------------- tournaments
def parse(line):
    line = line.strip()
    assert len(line) == 55 and set(line) <= {'0', '1'}, line
    adj = [[0] * NR for _ in range(NR)]
    k = 0
    for i in range(NR):
        for j in range(i + 1, NR):
            if line[k] == '1':
                adj[i][j] = 1
            else:
                adj[j][i] = 1
            k += 1
    return adj


def to_string(adj):
    return ''.join('1' if adj[i][j] else '0' for i in range(NR) for j in range(i + 1, NR))


def cmatrix(adj):
    n = len(adj)
    return [[sum(adj[w][u] & adj[w][v] for w in range(n)) if u != v else 0 for v in range(n)] for u in range(n)]


def vertex_invariant(adj, c):
    n = len(adj)
    out = []
    for v in range(n):
        Np = [w for w in range(n) if adj[v][w]]
        Nm = [w for w in range(n) if adj[w][v]]
        sp = tuple(sorted(sum(adj[x][y] for y in Np) for x in Np))
        sm = tuple(sorted(sum(adj[x][y] for y in Nm) for x in Nm))
        out.append((tuple(sorted(c[v][w] for w in range(n) if w != v)), sp, sm))
    return out


def isomorphisms(adj1, adj2, inv1=None, inv2=None, first_only=False):
    """All bijections f with adj1[i][k] == adj2[f(i)][f(k)] (backtracking with vertex invariants)."""
    n = len(adj1)
    if inv1 is None:
        inv1 = vertex_invariant(adj1, cmatrix(adj1))
    if inv2 is None:
        inv2 = vertex_invariant(adj2, cmatrix(adj2))
    if sorted(inv1) != sorted(inv2):
        return []
    res = []
    f = [-1] * n
    used = [False] * n

    def rec(i):
        if i == n:
            res.append(tuple(f))
            return first_only
        for w in range(n):
            if used[w] or inv1[i] != inv2[w]:
                continue
            ok = True
            for k in range(i):
                if adj1[k][i] != adj2[f[k]][w]:
                    ok = False
                    break
            if ok:
                f[i] = w
                used[w] = True
                if rec(i + 1):
                    return True
                used[w] = False
                f[i] = -1
        return False

    rec(0)
    return res


def automorphisms(adj):
    inv = vertex_invariant(adj, cmatrix(adj))
    return isomorphisms(adj, adj, inv, inv)


# ---------------------------------------------------------------- partitions / placements
def partitions(n, maxpart=None, maxlen=NR):
    if maxpart is None:
        maxpart = n
    if n == 0:
        yield ()
        return
    if maxlen == 0:
        return
    for p in range(min(n, maxpart), 0, -1):
        for rest in partitions(n - p, p, maxlen - 1):
            yield (p,) + rest


def placements(part, n=NR):
    """All j-vectors on range(n) whose positive values form the multiset `part` (part sorted decreasingly)."""
    vals = sorted(set(part), reverse=True)
    groups = [(v, part.count(v)) for v in vals]

    def rec(gi, free, jv):
        if gi == len(groups):
            yield tuple(jv)
            return
        v, m = groups[gi]
        for S in itertools.combinations(free, m):
            for x in S:
                jv[x] = v
            rest = [x for x in free if x not in S]
            yield from rec(gi + 1, rest, jv)
            for x in S:
                jv[x] = 0

    yield from rec(0, list(range(n)), [0] * n)


def orbit_reps(jvecs, auts):
    """Lexicographically maximal representative of each Aut-orbit of j-vectors."""
    reps = set()
    for jv in jvecs:
        imgs = []
        for f in auts:
            img = [0] * len(jv)
            for x, val in enumerate(jv):
                img[f[x]] = val
            imgs.append(tuple(img))
        reps.add(max(imgs))
    return sorted(reps, reverse=True)


def positions(jv):
    """V_+ in canonical position order: decreasing j, then increasing vertex label."""
    return sorted([r for r in range(len(jv)) if jv[r] > 0], key=lambda r: (-jv[r], r))


# ---------------------------------------------------------------- heavy patterns
def heavy_patterns(jpos, total):
    """All multisets {M: n_M} of subsets M of range(p) (p = len(jpos)), with sum n_M (6 - |M|) = total,
    pruned only by Ex_u >= 0 and L_u >= 0 (both monotone in adding sets).  Returned as tuples of (M, n)."""
    p = len(jpos)
    subsets = [frozenset(S) for k in range(0, min(p, 5) + 1) for S in itertools.combinations(range(p), k)]
    exmax = [5 + 10 * j for j in jpos]
    lmax = [20 + j for j in jpos]
    out = []

    def rec(i, rem, ex, ll, chosen):
        if rem == 0:
            out.append(tuple(chosen))
            return
        if i == len(subsets):
            return
        M = subsets[i]
        e = 6 - len(M)
        lam = LAM[11 - len(M)]
        nmax = rem // e
        for nM in range(nmax, -1, -1):
            if nM:
                ex2 = list(ex)
                ll2 = list(ll)
                bad = False
                for u in M:
                    ex2[u] -= nM * lam
                    ll2[u] -= nM
                    if ex2[u] < 0 or ll2[u] < 0:
                        bad = True
                if bad:
                    continue
                rec(i + 1, rem - nM * e, ex2, ll2, chosen + [(tuple(sorted(M)), nM)])
            else:
                rec(i + 1, rem, ex, ll, chosen)

    rec(0, total, exmax, lmax, [])
    return out


def pattern_data(jpos, H):
    """Derived quantities of a heavy pattern H on positions range(p)."""
    p = len(jpos)
    J = sum(jpos)
    Ex = [5 + 10 * j for j in jpos]
    L = [20 + j for j in jpos]
    tau = [0] * p
    h = {}
    E = {}
    for a, b in itertools.combinations(range(p), 2):
        h[a, b] = 0
        E[a, b] = 0
    for M, nM in H:
        e = 6 - len(M)
        for u in M:
            Ex[u] -= nM * LAM[11 - len(M)]
            L[u] -= nM
            tau[u] += nM * e
        for a, b in itertools.combinations(M, 2):
            h[a, b] += nM
            E[a, b] += nM * e
    rho = [120 + 5 * jpos[u] - tau[u] - 12 * (NR - p) for u in range(p)]
    return dict(Ex=Ex, L=L, tau=tau, h=h, E=E, rho=rho)


def d_bounds(cpp, pd, p):
    """Interval [lo, hi] for D on each pair (a, b) of positions, given c on V_+ pairs (cpp[a, b])."""
    bnd = {}
    for a, b in itertools.combinations(range(p), 2):
        c = cpp[a, b]
        h = pd['h'][a, b]
        E = pd['E'][a, b]
        lo = max(12, c + h, -((-(c + 45 + E)) // 4))
        hi = min(43, 39 + c + h, (c + 45 + E + min(pd['Ex'][a], pd['Ex'][b])) // 4)
        bnd[a, b] = (lo, hi)
    return bnd


def solve_rows(bnd, rho, p):
    """Exact search: integer D on pairs of K_p within bnd with vertex sums rho.  Returns a solution or None."""
    if any(lo > hi for lo, hi in bnd.values()):
        return None
    return solve_sets({k: list(range(lo, hi + 1)) for k, (lo, hi) in bnd.items()}, rho, p)


def solve_sets(allowed, rho, p):
    """Exact search: D on pairs of K_p with D[a, b] in allowed[a, b] (sorted list) and vertex sums rho."""
    pairs = list(itertools.combinations(range(p), 2))
    if any(not allowed[pr] for pr in pairs):
        return None
    if p == 1:
        return {} if rho[0] == 0 else None
    bnd = {pr: (allowed[pr][0], allowed[pr][-1]) for pr in pairs}
    D = {}

    def feasible_partial(k):
        # remaining capacity check per vertex
        for u in range(p):
            s = 0
            lo = 0
            hi = 0
            for (a, b) in pairs:
                if u not in (a, b):
                    continue
                if (a, b) in D:
                    s += D[a, b]
                else:
                    lo += bnd[a, b][0]
                    hi += bnd[a, b][1]
            if not (s + lo <= rho[u] <= s + hi):
                return False
        return True

    def rec(k):
        if not feasible_partial(k):
            return False
        if k == len(pairs):
            return True
        pr = pairs[k]
        for d in allowed[pr]:
            D[pr] = d
            if rec(k + 1):
                return True
            del D[pr]
        return False

    if rec(0):
        return dict(D)
    return None


_PAT_CACHE = {}


def decide_placement(c, jv):
    """Exact verdict of the reduced system for class c-matrix and j-vector jv (with Lemma A).
    Returns (feasible, detail)."""
    part = tuple(sorted([x for x in jv if x > 0], reverse=True))
    J = sum(part)
    p = len(part)
    if part not in _PAT_CACHE:
        _PAT_CACHE[part] = [(H, pattern_data(list(part), H)) for H in heavy_patterns(list(part), 14 - J)]
    Vp = positions(jv)
    V0 = [r for r in range(NR) if jv[r] == 0]
    if any(c[u][v] > 3 for u in V0 for v in range(NR) if v != u):
        return False, 'lemmaA'
    pairs = list(itertools.combinations(range(p), 2))
    cpp = {(a, b): c[Vp[a]][Vp[b]] for a, b in pairs}
    for H, pd in _PAT_CACHE[part]:
        if any(3 - c[u][Vp[b]] > pd['Ex'][b] for u in V0 for b in range(p)):
            continue
        sol = solve_rows(d_bounds(cpp, pd, p), pd['rho'], p)
        if sol is not None:
            return True, (H, sol)
    return False, 'all patterns fail'


# ---------------------------------------------------------------- certificates for (P3)
def _farkas_ok(y, dom, rho, pairs):
    t = sum(y[u] * rho[u] for u in range(len(rho)))
    lo = hi = 0
    g = 0
    for pr in pairs:
        a = y[pr[0]] + y[pr[1]]
        if a == 0:
            continue
        x0, x1 = a * dom[pr][0], a * dom[pr][-1]
        lo += min(x0, x1)
        hi += max(x0, x1)
        g = math.gcd(g, abs(a))
    return t < lo or t > hi or (g > 0 and t % g != 0)


def cert_tree(dom, rho, p, yset=None):
    """Infeasibility certificate for (P3) on domains dom (pair -> sorted list), or None if a solution exists.
    Node forms: ['E', a, b] empty domain; ['F', y] integer row combination whose box range (or gcd) excludes
    sum y_u rho_u; ['S', a, b, t, left, right] split D(a, b) <= t | >= t + 1."""
    pairs = list(itertools.combinations(range(p), 2))
    if yset is None:
        yset = [y for y in itertools.product((-1, 0, 1), repeat=p) if any(y)]
    for pr in pairs:
        if not dom[pr]:
            return ['E', pr[0], pr[1]]
    for y in yset:
        if _farkas_ok(y, dom, rho, pairs):
            return ['F', list(y)]
    big = max(pairs, key=lambda pr: len(dom[pr])) if pairs else None
    if big is None or len(dom[big]) == 1:
        return None
    vals = dom[big]
    t = vals[(len(vals) - 1) // 2]
    left = dict(dom)
    left[big] = [d for d in vals if d <= t]
    right = dict(dom)
    right[big] = [d for d in vals if d > t]
    lt = cert_tree(left, rho, p, yset)
    if lt is None:
        return None
    rt = cert_tree(right, rho, p, yset)
    if rt is None:
        return None
    return ['S', big[0], big[1], t, lt, rt]


def tree_size(t):
    return 1 if t[0] != 'S' else 1 + tree_size(t[4]) + tree_size(t[5])
