"""Independent verification of every step in ERDOS902_PROOF.md.

Run from the project root:   python proof/verify_proof.py

Sections (numbered as in the proof document):
  V1  basic lemmas (1.1-1.3), brute force on real S_k tournaments
  V2  generic Lemma T, including the equality case QR_19 (k = 3)
  V3  every inequality used in the proof of Theorem A, in exact integers
  V4  Theorem B: the binomial inequality for 5 <= n <= 2000
  V5  Theorem C: the numbers a_j, the bracket 2b < a < 2b+1, c*, and the
      integral comparison G(m,h) >= n*Phi((m+1)/n, h/n)
  V6  Theorem D: independent run of the sharpened cross-level recursion
  V7  Claim L (pair-link in DRT(51)): check the saved realisation, if present
Exit status is 0 iff every check passes.
"""

from __future__ import annotations

import itertools
import math
import os
import sys
import time
from math import comb

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FAILURES: list[str] = []


def check(cond: bool, msg: str) -> bool:
    if not cond:
        FAILURES.append(msg)
        print("    FAIL:", msg, flush=True)
    return cond


def popcount(x: int) -> int:
    return x.bit_count()


def members(mask: int) -> list[int]:
    out = []
    while mask:
        low = mask & -mask
        out.append(low.bit_length() - 1)
        mask ^= low
    return out


# --------------------------------------------------------------------------
# Tournaments as bitmasks: out[v] = set of vertices beaten by v.
# --------------------------------------------------------------------------
class Tournament:
    def __init__(self, name: str, out: list[int]):
        self.name = name
        self.N = len(out)
        self.out = out
        self.inn = [0] * self.N
        for v in range(self.N):
            for u in members(out[v]):
                self.inn[u] |= 1 << v
        for u in range(self.N):
            assert not (out[u] >> u) & 1, f"{name}: loop at {u}"
            for v in range(u + 1, self.N):
                a = (out[u] >> v) & 1
                b = (out[v] >> u) & 1
                assert a + b == 1, f"{name}: pair {u},{v} is not a single arc"
        self.full = (1 << self.N) - 1

    def D(self, X) -> int:
        """Dominators of X: vertices outside X beating every vertex of X."""
        mask = self.full
        for x in X:
            mask &= self.inn[x]
        return mask  # x is never in inn[x], so X is excluded automatically

    def has_S(self, k: int) -> bool:
        N, inn = self.N, self.inn
        for X in itertools.combinations(range(N), k - 1):
            base = self.full
            for x in X:
                base &= inn[x]
            if base == 0:
                return False
            for y in range(X[-1] + 1 if X else 0, N):
                if base & inn[y] == 0:
                    return False
        return True


def paley(p: int) -> Tournament:
    qr = {pow(a, 2, p) for a in range(1, p)}
    out = [0] * p
    for i in range(p):
        for s in qr:
            out[i] |= 1 << ((i + s) % p)
    return Tournament(f"QR_{p}", out)


def read_adjlist(path: str, name: str) -> Tournament:
    rows = []
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            rows.append([int(t) for t in line.split()])
    out = [0] * len(rows)
    for v, nbrs in enumerate(rows):
        for u in nbrs:
            out[v] |= 1 << u
    return Tournament(name, out)


# --------------------------------------------------------------------------
# V1. Lemmas 1.1-1.3 and the cross-level lemma, by brute force.
# --------------------------------------------------------------------------
def nu_profile(T: Tournament, k: int) -> list[int]:
    nu = [T.N]
    for s in range(1, k + 1):
        nu.append(min(popcount(T.D(A)) for A in itertools.combinations(range(T.N), s)))
    return nu


def v1_basic(T: Tournament, k: int, full_cross_limit: int = 6000) -> list[int]:
    t0 = time.time()
    print(f"  {T.name} (N={T.N}), property S_{k}", flush=True)
    check(T.has_S(k), f"{T.name} should have S_{k}")
    check(not T.has_S(k + 1), f"{T.name} should not have S_{k+1}")
    nu = nu_profile(T, k)
    print(f"    nu_0..nu_{k} = {nu}", flush=True)
    check(nu[k] >= 1, "S_k means nu_k >= 1")
    for s in range(k):
        check(nu[s] >= 2 * nu[s + 1] + 1, f"(M2) at s={s}")
    check(nu[k - 1] >= k + 1, "(M1) nu_{k-1} >= k+1")

    n_sets = n_cross = 0
    for s in range(k):
        for A in itertools.combinations(range(T.N), s):
            R = T.D(A)
            m = popcount(R)
            Aset = set(A)
            # Lemma 1.2: D(A) has no dominator, so |D(A)| >= k+1
            dom = T.full
            for w in members(R):
                dom &= T.inn[w]
            check(dom == 0, f"{T.name}: D({A}) is dominated")
            check(m >= k + 1, f"{T.name}: |D({A})| = {m} < k+1")
            # Lemma 1.3: D(A+y) = D(A) & N^-(y) for every y outside A
            for y in range(T.N):
                if y in Aset:
                    continue
                Dy = T.D(A + (y,))
                check(Dy == R & T.inn[y], f"{T.name}: D(A+y) identity, A={A}, y={y}")
                if (R >> y) & 1:
                    check(popcount(Dy) >= nu[s + 1], "Lemma 1.3 inner in-degree")
            # cross-level lemma, sharpened, every k' in 1..k
            h = nu[s + 1]
            for kk in range(1, k + 1):
                # exact pair count via the dominators y
                via_y = sum(comb(popcount(R & T.out[y]), kk) for y in range(T.N) if y not in Aset)
                upper = (T.N - s - m) * comb(m - h, kk) + m * comb(m - h - 1, kk)
                lower = nu[kk] * comb(m, kk)
                check(lower <= via_y <= upper, f"{T.name}: cross-level, A={A}, k={kk}")
                if comb(m, kk) <= full_cross_limit:
                    direct = sum(popcount(T.D(U)) for U in itertools.combinations(members(R), kk))
                    check(direct == via_y, f"{T.name}: pair-count identity, A={A}, k={kk}")
                    n_cross += 1
            n_sets += 1
    print(f"    checked {n_sets} sets A (|A| <= {k-1}), {n_cross} direct pair counts, "
          f"{time.time()-t0:.1f}s", flush=True)
    return nu


# --------------------------------------------------------------------------
# V2. Generic Lemma T (S_k version).  A tight (k-2)-set A has |D(A)| = 2k+3.
# --------------------------------------------------------------------------
def lemma_T_threshold(k: int) -> int:
    need = (k + 1) * comb(2 * k + 2, k - 2)
    d = k + 1
    while (k + 1) * comb(k, k - 2) + (d - (k + 1)) * comb(k + 1, k - 2) < need:
        d += 1
    return d


def v2_lemma_T(T: Tournament, k: int) -> None:
    thr = lemma_T_threshold(k)
    tight = 0
    equality = 0
    for A in itertools.combinations(range(T.N), k - 2):
        R = T.D(A)
        if popcount(R) != 2 * k + 3:
            continue
        tight += 1
        Rl = members(R)
        Aset = set(A)
        for y in Rl:
            check(popcount(R & T.inn[y]) == k + 1, f"{T.name}: T[D(A)] not (k+1)-regular")
        for y in range(T.N):
            if y in Aset or (R >> y) & 1:
                continue
            check(popcount(R & T.out[y]) <= k + 2, f"{T.name}: outside vertex beats > k+2 of R")
        for r in Rl:
            others = [x for x in Rl if x != r]
            direct = sum(popcount(T.D((r,) + U)) for U in itertools.combinations(others, k - 2))
            via_w = sum(comb(popcount(R & T.out[w] & ~(1 << r)), k - 2)
                        for w in members(T.inn[r]))
            check(direct == via_w, f"{T.name}: Lemma T incidence identity")
            check(direct >= (k + 1) * comb(2 * k + 2, k - 2), f"{T.name}: Lemma T lower count")
            check(not any((T.inn[r] >> a) & 1 for a in A), f"{T.name}: r should beat A")
            d = popcount(T.inn[r])
            check(d >= thr, f"{T.name}: Lemma T bound d^-(r) >= {thr} fails")
            equality += d == thr
    print(f"    {T.name}: generic Lemma T (k={k}, threshold d^- >= {thr}): {tight} tight "
          f"{k-2}-sets, {equality} dominators attain the bound with equality", flush=True)


# --------------------------------------------------------------------------
# V3. Exact arithmetic of the proof of Theorem A.
# --------------------------------------------------------------------------
def v3_theorem_A() -> None:
    # F1-F3 via (M1),(M2): triple >= 5, pair >= 2*5+1, vertex >= 2*11+1
    check((5, 11, 23) == (4 + 1, 2 * 5 + 1, 2 * 11 + 1), "F1-F3 values")
    # Lemma T: 5 inner dominators * C(4,2) + (d-5) outer * C(5,2) >= 5 * C(10,2)
    check((comb(10, 2), comb(4, 2), comb(5, 2)) == (45, 6, 10), "Lemma T binomials")
    check(lemma_T_threshold(4) == 25, "Lemma T threshold is 25")
    # Corollary 1: 11(N-24) <= 23(N-38) iff N >= 51  (scan a wide range)
    ok = [N for N in range(24, 2000) if 11 * (N - 24) <= 23 * (N - 38)]
    check(ok[0] == 51 and ok == list(range(51, 2000)), "Corollary 1 threshold N >= 51")
    check(comb(23, 2) == 23 * 11 and comb(24, 2) - 24 * 11 == 12, "in-degree sums 253, excess 12")
    # Claim Q: for 12 <= l <= 24, 0 <= q <= 24-l, the inequality
    #   12 >= q(l-11) + C(q,2) + (24-l-q)   holds  iff  q <= 1
    for l in range(12, 25):
        for q in range(0, 24 - l + 1):
            lhs_ok = 12 >= q * (l - 11) + comb(q, 2) + (24 - l - q)
            factored = (q - 1) * (l - 12) + comb(q, 2) <= 0
            check(lhs_ok == factored, f"Claim Q rearrangement l={l} q={q}")
            check(lhs_ok == (q <= 1), f"Claim Q conclusion l={l} q={q}")
    # |Z| <= 5 from C(z,2) <= 2z
    check(max(z for z in range(0, 100) if comb(z, 2) <= 2 * z) == 5, "|Z| <= 5")
    # Final count: N(N-1)/2 >= 24N iff N >= 49; excess N(N-49)/2 at N = 49, 50
    check(min(N for N in range(1, 100) if comb(N, 2) >= 24 * N) == 49, "N >= 49")
    for N, exc in ((49, 0), (50, 25)):
        check(comb(N, 2) - 24 * N == exc, f"excess at N={N}")
        check(N - exc > 5, f"|Z| >= {N-exc} > 5 at N={N}")
    print("    all inequalities of Theorem A verified (Lemma T, Cor. 1, Claim Q, final count)",
          flush=True)


# --------------------------------------------------------------------------
# V4. Theorem B: (n+1) C(2n+3, n-1) > (2n+5) 2^(n-2) C(n+2, 3) for n >= 5.
# --------------------------------------------------------------------------
def v4_theorem_B(nmax: int = 2000) -> None:
    for n in range(5, nmax + 1):
        lhs = (n + 1) * comb(2 * n + 3, n - 1)
        rhs = (2 * n + 5) * 2 ** (n - 2) * comb(n + 2, 3)
        check(lhs > rhs, f"Theorem B inequality at n={n}")
        check(n**3 - n**2 - 13 * n - 5 > 0, f"Theorem B polynomial at n={n}")
    # it must fail at n = 4 (that is why n = 4 needs Theorem A)
    check(5 * comb(11, 3) <= 13 * 4 * comb(6, 3), "Theorem B inequality fails at n=4, as stated")
    # the base value and the ratio claim used in the induction
    check(6 * comb(13, 4) * 1 > 15 * 8 * comb(7, 3), "Theorem B base n=5")
    from fractions import Fraction
    for n in range(5, 400):
        Lam = Fraction((n + 1) * comb(2 * n + 3, n - 1), comb(n + 2, 3))
        Lam1 = Fraction((n + 2) * comb(2 * n + 5, n), comb(n + 3, 3))
        check(Lam1 / Lam == Fraction(2 * (n + 2) ** 2 * (2 * n + 5), (n + 1) * (n + 3) * (n + 5)),
              f"Theorem B ratio formula at n={n}")
        check(Lam1 / Lam >= 3 and Fraction(2 * (2 * n + 7), 2 * n + 5) < 3, f"Theorem B ratio bounds n={n}")
    # values of (2n+5) 2^(n-2) - 1 quoted in the Theorem D table
    table_B = {4: 51, 5: 119, 6: 271, 7: 607, 8: 1343, 9: 2943, 10: 6399, 11: 13823, 12: 29695}
    for n, v in table_B.items():
        check((2 * n + 5) * 2 ** (n - 2) - 1 == v, f"Theorem B value n={n}")
        check((n + 2) * 2 ** (n - 1) - 1 + 2 ** (n - 2) == v, f"Theorem B beats Szekeres by 2^(n-2), n={n}")
    print(f"    Theorem B inequality holds for 5 <= n <= {nmax} and fails at n = 4", flush=True)


# --------------------------------------------------------------------------
# V5. Theorem C.
# --------------------------------------------------------------------------
def v5_theorem_C() -> None:
    import mpmath as mp

    mp.mp.dps = 110

    def F(x):
        # F(x) = x ln x - (x-1) ln(x-1), written as ln x - (x-1) log1p(-1/x)
        # so that no digits cancel when x is huge (a_j grows like 2^j)
        x = mp.mpf(x)
        if x == 1:
            return mp.mpf(0)
        return mp.log(x) - (x - 1) * mp.log1p(-1 / x)

    def root(fun, lo, hi):
        flo = fun(lo)
        for _ in range(400):
            mid = (lo + hi) / 2
            fm = fun(mid)
            if (fm > 0) == (flo > 0):
                lo, flo = mid, fm
            else:
                hi = mid
        return (lo + hi) / 2

    def Phi(a, b):
        return F(a) - F(a - b)

    ln2 = mp.log(2)
    # closed form of Phi against the defining integral at a few points
    for a, b in ((3.1, 1.5), (5.0, 2.0), (2.5622, 1.0), (40.0, 17.0)):
        integral = mp.quad(lambda y: mp.log((a - y) / (a - b - y)), [0, 1])
        check(abs(integral - Phi(a, b)) < mp.mpf(10) ** -40, f"Phi closed form at {(a, b)}")

    a = [None, mp.mpf(1)]
    for j in range(2, 151):
        b = a[-1]
        lo, hi = 2 * b, 2 * b + 1
        check(Phi(lo, b) > ln2 and Phi(hi, b) < ln2, f"bracket 2b < a_j < 2b+1 at j={j}")
        # Phi(b+1, b) = F(b+1) - F(1) = F(b+1); evaluate it directly so that
        # rounding in (b+1)-b cannot push the argument of F below 1
        check(F(b + 1) > ln2, f"Phi(b+1,b) > ln 2 at j={j}")
        a.append(root(lambda x: Phi(x, b) - ln2, lo, hi))
    ratios = [a[j] / 2**j for j in range(1, len(a))]
    check(all(ratios[i] < ratios[i + 1] for i in range(len(ratios) - 1)), "a_j/2^j increasing")
    cstar = ratios[-1]
    stated = mp.mpf("0.7695032191504894326990652683098231346767")
    check(abs(cstar - stated) < mp.mpf(10) ** -38, "c* agrees with 40-digit value")
    print("    a_2..a_6 =", [mp.nstr(a[j], 6) for j in range(2, 7)], flush=True)
    print("    c* =", mp.nstr(cstar, 40), flush=True)

    # G(m,h) = sum_{t<n} ln((m-t)/(m-h-t)) >= n*Phi((m+1)/n, h/n) whenever m-h >= n
    mp.mp.dps = 30
    worst = mp.mpf(10)
    cnt = 0
    for n in range(1, 21):
        for h in range(1, 3 * n + 2):
            for m in range(h + n, h + 4 * n + 2):
                G = mp.fsum(mp.log(mp.mpf(m - t) / (m - h - t)) for t in range(n))
                rhs = n * Phi(mp.mpf(m + 1) / n, mp.mpf(h) / n)
                worst = min(worst, G - rhs)
                cnt += 1
    check(worst > 0, "integral comparison G >= n*Phi((m+1)/n,h/n)")
    print(f"    integral comparison checked on {cnt} triples (n,m,h); min slack {mp.nstr(worst, 5)}",
          flush=True)


# --------------------------------------------------------------------------
# V6. Theorem D: the sharpened cross-level recursion, implemented afresh.
# --------------------------------------------------------------------------
def recursion_rules_out(n: int, N: int) -> bool:
    """True if the recursion proves that no S_n tournament has N vertices."""
    L = {n: 1}
    for s in range(n - 1, -1, -1):
        h = L[s + 1]

        def nu_low(k: int) -> int:
            return L[k] if k > s else 2 ** (s + 1 - k) * (h + 1) - 1

        m = 2 * h + 1
        while True:
            if m > N - s:
                return True
            good = True
            for k in range(1, n + 1):
                if k > m:
                    break
                lhs = (N - s - m) * comb(m - h, k) + m * comb(m - h - 1, k)
                if lhs < nu_low(k) * comb(m, k):
                    good = False
                    break
            if good:
                break
            m += 1
        L[s] = m
    return L[0] > N


def v6_theorem_D() -> None:
    claimed = {2: 7, 3: 19, 4: 49, 5: 121, 6: 281, 7: 665, 8: 1485, 9: 3388,
               10: 7398, 11: 16569, 12: 35655}
    for n, X in claimed.items():
        t0 = time.time()
        # monotone in N, so ruling out X-1 rules out every N < X
        out_below = recursion_rules_out(n, X - 1)
        out_at = recursion_rules_out(n, X)
        check(out_below and not out_at, f"recursion bound for n={n} should be exactly {X}")
        # spot-check monotonicity on a few smaller N
        for N in (X - 2, X - 7, (X * 9) // 10):
            if N > n:
                check(recursion_rules_out(n, N), f"monotonicity n={n}, N={N}")
        print(f"    n={n:2d}: every N <= {X-1} ruled out, N = {X} not ruled out "
              f"({time.time()-t0:.1f}s)", flush=True)


# --------------------------------------------------------------------------
# V7. Claim L realisation (DRT(51) pair-link), if the search output is present.
# --------------------------------------------------------------------------
def v7_claim_L() -> None:
    d = os.path.join(ROOT, "ai-debate")
    paths = [os.path.join(d, f) for f in ("claim_l_tournament.npy", "claim_l_mult.npy", "claim_l_valid.npy")]
    if not all(os.path.exists(p) for p in paths):
        print("    (ai-debate/claim_l_*.npy not found; skipped)", flush=True)
        return
    import numpy as np

    A = np.load(paths[0]).astype(int)
    mult = np.load(paths[1]).astype(int)
    valid = np.load(paths[2]).astype(int)
    X = 12
    check(A.shape == (X, X) and all(A[i, j] + A[j, i] == 1 for i in range(X) for j in range(X) if i != j)
          and all(A[i, i] == 0 for i in range(X)), "T_X is a tournament")
    indeg = A.sum(axis=0)
    check(indeg.min() >= 5, "(ii) in_X >= 5")
    check(int((indeg**2).sum()) <= 396, "sum in_X^2 <= 396")
    for i in range(X):
        for j in range(i + 1, X):
            check(any(A[z, i] and A[z, j] for z in range(X)), "(i) T_X is S_2")
    rows = []
    for t in np.flatnonzero(mult > 0):
        rows += [[(int(valid[t]) >> x) & 1 for x in range(X)]] * int(mult[t])
    M = np.array(rows)
    check(M.shape == (37, X), "37 external sets")
    check(M.sum(axis=1).min() >= 5, "(iii) c_u >= 5")
    for u in range(37):
        for y in range(X):
            check(any(M[u, x] and A[x, y] for x in range(X) if x != y), "(iv) N_u hits every N^-_X(y)")
        for v in range(u + 1, 37):
            check(bool(np.logical_and(M[u], M[v]).any()), "(v) N_u, N_v intersect")
    G = M.T @ M
    for x in range(X):
        check(G[x, x] == 12 + indeg[x], "Gram diagonal r_x = 12 + in_X(x)")
        for y in range(x + 1, X):
            check(G[x, y] == 10 - int(np.logical_and(A[x], A[y]).sum()), "Gram off-diagonal")
    tot = int((indeg**2).sum() + (M.sum(axis=1) ** 2).sum())
    check(tot == 1596, "pair-link identity sum in^2 + sum c^2 = 1596")
    print(f"    Claim L realisation verified: all of (i)-(v) and the exact Gram matrix hold "
          f"(row sizes {sorted(set(M.sum(axis=1).tolist()))}, identity total {tot})", flush=True)


def main() -> int:
    t_start = time.time()
    if "--from-v5" in sys.argv:
        return finish_from_v5(t_start)
    print("V1  basic lemmas, brute force", flush=True)
    v1_basic(paley(7), 2)
    v1_basic(paley(19), 3)
    T67 = paley(67)
    v1_basic(T67, 4, full_cross_limit=3000)
    thin = os.path.join(HERE, "thin_S4_N70.txt")
    T70 = read_adjlist(thin, "thin_S4_N70") if os.path.exists(thin) else None
    if T70:
        v1_basic(T70, 4, full_cross_limit=3000)
    print("V2  generic Lemma T", flush=True)
    v2_lemma_T(paley(7), 2)
    v2_lemma_T(paley(19), 3)
    v2_lemma_T(T67, 4)
    if T70:
        v2_lemma_T(T70, 4)
    print("V3  Theorem A arithmetic", flush=True)
    v3_theorem_A()
    print("V4  Theorem B", flush=True)
    v4_theorem_B()
    return finish_from_v5(t_start)


def finish_from_v5(t_start: float) -> int:
    print("V5  Theorem C", flush=True)
    v5_theorem_C()
    print("V6  Theorem D (sharpened recursion)", flush=True)
    v6_theorem_D()
    print("V7  Claim L realisation", flush=True)
    v7_claim_L()
    print(f"\nTotal time {time.time()-t_start:.0f}s.  Failures: {len(FAILURES)}", flush=True)
    for f in FAILURES[:20]:
        print("  ", f)
    return 1 if FAILURES else 0


if __name__ == "__main__":
    sys.exit(main())
