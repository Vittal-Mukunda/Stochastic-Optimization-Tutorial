"""R8-F-asymptotic: barrier profiles for the nu-profile calculus of ERDOS902_PROOF.md.

Run from the project root:  python research/compute/r8f_barrier.py [--quick]

What it does
  1. a_j and c* (mpmath, 40 digits); c_I = (a_I + 1)/2^I, which decreases to c*.
  2. For given (n, I) builds the barrier profile P_n^(I):
        m_n = 1, m_{n-1} = n + 2,
        m_{n-i} = ceil(n * A_i) for 2 <= i <= I, where Phi(A_i, (m_{n-i+1}+1)/n) = ln 2,
        m_s = 2 m_{s+1} + n + 2 for 0 <= s < n - I,  N := m_0.
  3. Checks EXACTLY (python integers) that the profile satisfies every constraint of the
     nu-profile calculus, including the recursive (inner) instances:
        chain   m_s >= 2 m_{s+1} + 1,  m_{n-1} >= n + 1,  m_n >= 1,
        (R)     for 0 <= s <= n-1, 0 <= j <= n-s-1, 1 <= k <= n-s, t = s + j:
                m_{s+k} C(m_t,k) <= (m_s - j - m_t) C(m_t - m_{t+1}, k) + m_t C(m_t - m_{t+1} - 1, k).
     s = 0 is Lemma 3.1 in T for every level and every k (the Theorem D system, with
     nu_k = m_k, which dominates every lambda_k used there); s >= 1 is Lemma 3.1 applied
     inside T[D(A)], |A| = s, which has S_{n-s} and order m_s.
     Optionally (--full-hyp) it also checks the sufficient conditions (i)-(iii) of Lemma B1.
  4. Lower side: the exact integer recursion that uses only the k = n instance and doubling
     (a valid weakening of Lemma 3.1, monotone in m, so binary search is rigorous):
        l_n = 1, l_{n-1} = n + 1,
        l_s = max(2 l_{s+1} + 1, least m with C(m,n) <= (N - s) C(m - l_{s+1}, n)),
     N is excluded iff l_0 > N.  N_low(n) = least N not excluded.
  5. Prints the sandwich N_low(n) <= (threshold of the full calculus) <= N_bar(n), divided by n 2^n.
Writes research/compute/r8f_barrier.json.
"""
from __future__ import annotations

import json
import os
import sys
import time
from math import comb

import mpmath as mp

mp.mp.dps = 60
LN2 = mp.log(2)
HERE = os.path.dirname(os.path.abspath(__file__))


def F(x):
    x = mp.mpf(x)
    if x == 1:
        return mp.mpf(0)
    # = x ln x - (x-1) ln(x-1), written without cancellation for large x
    return mp.log(x) + (x - 1) * mp.log1p(1 / (x - 1))


def Phi(a, b):
    return F(a) - F(mp.mpf(a) - b)


def root_A(b):
    """Unique A in (2b, 2b+1) with Phi(A, b) = ln 2 (b >= 1)."""
    b = mp.mpf(b)
    lo, hi = 2 * b, 2 * b + 1
    for _ in range(200):
        mid = (lo + hi) / 2
        if Phi(mid, b) > LN2:
            lo = mid
        else:
            hi = mid
    return hi  # Phi(hi, b) <= ln 2


def a_sequence(J):
    a = [None, mp.mpf(1)]
    for j in range(2, J + 1):
        a.append(root_A(a[-1]))
    return a


IMAX = 40
_TOP = {}


def top_values(n):
    """top[i] = m_{n-i} under the top rule, for 1 <= i <= min(n, IMAX)."""
    if n not in _TOP:
        top = {1: n + 2}
        for i in range(2, min(n, IMAX) + 1):
            b = mp.mpf(top[i - 1] + 1) / n
            top[i] = int(mp.ceil(n * root_A(b)))
        _TOP[n] = top
    return _TOP[n]


def profile(n, I):
    I = min(I, n, IMAX)
    top = top_values(n)
    m = [0] * (n + 1)
    m[n] = 1
    for i in range(1, I + 1):
        m[n - i] = top[i]
    for s in range(n - I - 1, -1, -1):
        m[s] = 2 * m[s + 1] + n + 2
    return m


def check_profile(m, n, recursive=True):
    """Exact check of chain + (R). Returns (ok, first_violation, number_checked)."""
    if m[n] < 1 or m[n - 1] < n + 1:
        return False, ("top", m[n], m[n - 1]), 0
    for s in range(n):
        if m[s] < 2 * m[s + 1] + 1:
            return False, ("chain", s), 0
    cnt = 0
    for t in range(n):
        mt, h = m[t], m[t + 1]
        # running binomials over k
        c_m, c_a, c_b = 1, 1, 1
        bases = range(0, t + 1) if recursive else range(0, 1)
        for k in range(1, n + 1):
            c_m = c_m * (mt - k + 1) // k
            c_a = c_a * (mt - h - k + 1) // k if mt - h - k + 1 > 0 else 0
            c_b = c_b * (mt - h - 1 - k + 1) // k if mt - h - k > 0 else 0
            for s in bases:
                if k > n - s:
                    continue
                j = t - s
                lhs = m[s + k] * c_m
                rhs = (m[s] - j - mt) * c_a + mt * c_b
                cnt += 1
                if lhs > rhs:
                    return False, ("R", s, j, k), cnt
    return True, None, cnt


def check_hyp(m, n):
    """Sufficient conditions (i)-(iii) of Lemma B1 (Phi in mpmath, precision scaled with n)."""
    for s in range(n):
        if m[s] - m[s + 1] - 1 < n:
            return False, ("i", s)
        with mp.workdps(int(0.6 * n) + 60):
            # Phi(a, b) = F(a) - F(a - b), with a - b formed exactly from integers
            if F(mp.mpf(m[s]) / n) - F(mp.mpf(m[s] - m[s + 1] - 1) / n) > mp.log(2):
                return False, ("ii", s)
        if m[s] - 2 * m[s + 1] < max(1, n - s - 1):
            return False, ("iii", s)
    return True, None


def low_threshold(n):
    def excluded(N):
        l_next = 1
        l = n + 1
        for s in range(n - 2, -1, -1):
            l_next = l
            lo = 2 * l_next + 1
            if comb(lo, n) <= (N - s) * comb(lo - l_next, n):
                l = lo
            else:
                # monotone predicate in m: find least m >= lo
                hi = lo
                step = 1
                while comb(hi, n) > (N - s) * comb(hi - l_next, n):
                    hi = lo + step
                    step *= 2
                    if hi > N:
                        return True
                a, b = lo, hi
                while b - a > 1:
                    c = (a + b) // 2
                    if comb(c, n) <= (N - s) * comb(c - l_next, n):
                        b = c
                    else:
                        a = c
                l = b
            if l > N - s:
                return True
        return l > N
    lo, hi = (n + 2) * 2 ** (n - 1) - 2, n * 2 ** n
    assert excluded(lo)
    while excluded(hi):
        hi *= 2
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if excluded(mid):
            lo = mid
        else:
            hi = mid
    return hi


def theorem_D_rules_out(n, N):
    """The Section 6 recursion of ERDOS902_PROOF.md (same rule as proof/verify_proof.py V6)."""
    L = {n: 1}
    for s in range(n - 1, -1, -1):
        h = L[s + 1]
        m = 2 * h + 1
        while True:
            # m > N - s, or doubling from level s already exceeds N: then L_0 > N follows
            # (every later level has L_{s'} >= 2 L_{s'+1} + 1), so stopping early gives the same answer.
            if m > N - s or 2 ** s * (m + 1) - 1 > N:
                return True
            good = True
            for k in range(1, min(n, m) + 1):
                lam = L[k] if k > s else 2 ** (s + 1 - k) * (h + 1) - 1
                if (N - s - m) * comb(m - h, k) + m * comb(m - h - 1, k) < lam * comb(m, k):
                    good = False
                    break
            if good:
                break
            m += 1
        L[s] = m
    return L[0] > N


def theorem_D_threshold(n, hi):
    """Least N not ruled out (L_0(N) is non-increasing in N, Section 6)."""
    lo = (n + 2) * 2 ** (n - 1) - 2
    assert theorem_D_rules_out(n, lo) and not theorem_D_rules_out(n, hi)
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if theorem_D_rules_out(n, mid):
            lo = mid
        else:
            hi = mid
    return hi


def main():
    quick = "--quick" in sys.argv
    t0 = time.time()
    out = {}
    mp.mp.dps = 120
    a = a_sequence(300)
    cstar_lo = a[300] / mp.mpf(2) ** 300
    cstar_hi = (a[300] + 1) / mp.mpf(2) ** 300
    assert cstar_hi - cstar_lo < mp.mpf(10) ** -80
    cstar = cstar_lo
    mp.mp.dps = 60
    out["cstar_bracket_width"] = mp.nstr(cstar_hi - cstar_lo, 5)
    cI = {I: (a[I] + 1) / mp.mpf(2) ** I for I in range(1, 41)}
    out["cstar"] = mp.nstr(cstar, 40)
    out["a"] = {j: mp.nstr(a[j], 20) for j in range(1, 13)}
    out["c_I"] = {I: mp.nstr(cI[I], 20) for I in range(1, 21)}
    print("c* =", mp.nstr(cstar, 40))
    for I in range(1, 13):
        print(f"  a_{I} = {mp.nstr(a[I], 12):>16}   c_I = (a_I+1)/2^I = {mp.nstr(cI[I], 12)}")

    # --- barrier profiles ---------------------------------------------------
    ns_rec = [8, 10, 12, 16, 20, 24, 32, 40, 48, 64] if quick else [8, 10, 12, 16, 20, 24, 32, 40, 48, 64, 80, 100]
    ns_out = [128, 160, 200, 256, 320] if quick else [128, 160, 200, 256, 320, 400, 512]
    bar = {}
    for n in ns_rec + ns_out:
        recursive = n in ns_rec
        best = None
        cands = sorted((profile(n, I)[0], I) for I in range(2, min(n, IMAX) + 1))
        for N0, I in cands:
            m = profile(n, I)
            ok, viol, cnt = check_profile(m, n, recursive=recursive)
            if ok:
                best = (m[0], I, cnt)
                break
        if best is None:
            bar[n] = None
            print(f"n={n:4d}: no barrier profile passed")
            continue
        N, I, cnt = best
        hyp_ok = check_hyp(profile(n, I), n)[0] if n <= 200 else None
        r = N / (n * 2 ** n)
        bar[n] = {"N_bar": str(N) if N > 10 ** 15 else N, "ratio": r, "I": I, "constraints_checked": cnt,
                  "recursive_checked": recursive, "lemmaB1_hypotheses_hold": hyp_ok}
        print(f"n={n:4d}: N_bar/(n 2^n) = {r:.6f}  (I={I}, {cnt} exact constraints, recursive={recursive}, B1-hyp={hyp_ok})",
              flush=True)
    out["barrier"] = bar

    # fixed-I profiles at large n: convergence to c_I
    conv = {}
    for I in (4, 6, 8):
        row = {}
        for n in (64, 128, 256, 512):
            m = profile(n, I)
            ok, _, _ = check_profile(m, n, recursive=(n <= 64))
            hyp = check_hyp(m, n)
            row[n] = {"ratio": m[0] / (n * 2 ** n), "exact_ok": ok, "recursive_checked": n <= 64,
                      "lemmaB1_hypotheses_hold": hyp[0], "hyp_violation": hyp[1]}
        conv[I] = {"c_I": float(cI[I]), "rows": row}
        print(f"I={I}: c_I={float(cI[I]):.6f}  ",
              {n: (round(v['ratio'], 6), v['exact_ok'], v['lemmaB1_hypotheses_hold']) for n, v in row.items()})
    out["fixed_I_convergence"] = conv

    # --- Theorem D threshold (all k, all levels): the sandwich X_D <= L* <= N_bar ---
    tD = {}
    for n in ([5, 8, 10, 12, 16, 20, 24, 32] if quick else
              [5, 8, 10, 12, 16, 20, 24, 32, 40, 48, 64, 80, 100, 128, 160, 200]):
        hi = None
        if n in bar and bar[n] is not None:
            hi = int(bar[n]["N_bar"])
        if hi is None:
            hi = 2 * n * 2 ** n
        X = theorem_D_threshold(n, hi)
        tD[n] = {"X_D": str(X) if X > 10 ** 15 else X, "ratio": X / (n * 2 ** n),
                 "N_bar_ratio": (hi / (n * 2 ** n)) if n in bar and bar[n] else None}
        print(f"n={n:4d}: Theorem D threshold X_D/(n 2^n) = {X / (n * 2 ** n):.6f}   N_bar ratio = {tD[n]['N_bar_ratio']}",
              flush=True)
    out["theorem_D_threshold"] = tD

    # --- lower side ------------------------------------------------------------
    low = {}
    for n in ([8, 16, 32, 64] if quick else [8, 16, 32, 64, 128]):
        Nl = low_threshold(n)
        low[n] = {"N_low": str(Nl) if Nl > 10 ** 15 else Nl, "ratio": Nl / (n * 2 ** n)}
        print(f"n={n:4d}: N_low/(n 2^n) = {Nl / (n * 2 ** n):.6f}", flush=True)
    out["lower_k_eq_n_only"] = low
    out["seconds"] = time.time() - t0
    with open(os.path.join(HERE, "r8f_barrier.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1)
    print("done in %.1fs" % (time.time() - t0))


if __name__ == "__main__":
    main()
