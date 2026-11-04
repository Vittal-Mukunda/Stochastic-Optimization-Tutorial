"""R8-F-asymptotic: Paley tournaments QR_p versus the Erdos random bound, small n.

Run from the project root:  python research/compute/r8f_paley.py [nmax_full] [p_max_witness]

QR_p (p = 3 mod 4 prime): x -> y iff y - x is a nonzero quadratic residue.
The maps x -> a x + b (a a nonzero square) are automorphisms and act transitively on arcs,
so every n-set (n >= 2) is equivalent to one containing the arc 0 -> 1.

Part 1 (exact, n = 2..nmax_full, default 5): for every prime p = 3 mod 4 in increasing order,
  decide S_n exactly. D(X) = intersection of in-neighbourhoods; the last two elements of X are
  handled by one integer matrix product, so |D(X)| is computed for EVERY n-set containing {0,1}.
  Reports p_n = least p with S_n, nu_n(QR_p) = min |D(X)|, and the number of undominated n-sets
  through {0,1} for every smaller p.
Part 2 (witnesses, n = 6 and 7): for every p = 3 mod 4 up to p_max_witness, a beam search for an
  undominated n-set; a found set is re-verified exactly. This gives a proved LOWER bound on p_n
  (all smaller p fail) but no proof that the first p without a witness has S_n.
Compares with ln2 n^2 2^n, with the exact first-moment threshold of a uniformly random
tournament, and with the Graham-Spencer sufficient condition p > n^2 2^(2n-2).
Writes research/compute/r8f_paley.json.
"""
from __future__ import annotations

import os

os.environ.setdefault("OMP_NUM_THREADS", "3")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "3")
os.environ.setdefault("MKL_NUM_THREADS", "3")

import itertools
import json
import math
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))


def is_prime(p):
    if p < 2:
        return False
    for q in range(2, int(p ** 0.5) + 1):
        if p % q == 0:
            return False
    return True


def paley_in(p):
    qr = np.zeros(p, dtype=bool)
    for x in range(1, p):
        qr[(x * x) % p] = True
    # Nin[x, w] = 1 iff w -> x iff x - w is a square
    idx = (np.arange(p)[:, None] - np.arange(p)[None, :]) % p
    return qr[idx]


def first_moment_threshold(n):
    """Least N with C(N,n) (1-2^-n)^(N-n) < 1 (random tournament has S_n with positive prob.)."""
    lq = math.log1p(-2.0 ** -n)
    N = n + 1
    while math.lgamma(N + 1) - math.lgamma(n + 1) - math.lgamma(N - n + 1) + (N - n) * lq >= 0:
        N += 1
    return N


def exact_Sn(p, n, Nin=None, stop_at_first=False):
    """Return (has_Sn, min|D|, #undominated n-sets through {0,1} (as ordered tails), witness)."""
    if Nin is None:
        Nin = paley_in(p)
    NinI = Nin.astype(np.int32)
    NinF = Nin.astype(np.float32)
    base = Nin[0] & Nin[1]
    best = None
    bad = 0
    witness = None
    if n == 2:
        c = int(base.sum())
        return c > 0, c, int(c == 0), ([0, 1] if c == 0 else None)
    if n == 3:
        cnt = NinI @ base.astype(np.int32)
        cnt = cnt[2:]
        mn = int(cnt.min())
        badc = int((cnt == 0).sum())
        w = None
        if badc:
            w = [0, 1, int(np.argmin(cnt)) + 2]
        return mn > 0, mn, badc, w
    free = n - 4  # elements chosen by explicit loop, the last two by a matrix product
    for tail in itertools.combinations(range(2, p), free):
        I = base.copy()
        for x in tail:
            I &= Nin[x]
        if not I.any():
            return False, 0, None, [0, 1] + list(tail)
        start = (tail[-1] + 1) if tail else 2
        if start >= p - 1:
            continue
        M = (Nin[start:] & I[None, :]).astype(np.float32)  # rows b >= start
        cnt = M @ NinF.T  # cnt[b', c] = |D({0,1,tail,b,c})|
        nb = cnt.shape[0]
        bidx = np.arange(start, p)
        mask = np.arange(p)[None, :] > bidx[:, None]
        vals = np.where(mask, cnt, np.inf)
        mn = float(vals.min())
        if best is None or mn < best:
            best = mn
        z = int(((cnt == 0) & mask).sum())
        if z:
            bad += z
            if witness is None:
                r, c = np.argwhere((cnt == 0) & mask)[0]
                witness = [0, 1] + list(tail) + [int(bidx[r]), int(c)]
            if stop_at_first:
                return False, 0, bad, witness
    return bad == 0, int(best), bad, witness


def D_size(Nin, X):
    I = np.ones(Nin.shape[0], dtype=bool)
    for x in X:
        I &= Nin[x]
    return int(I.sum())


def beam_witness(p, n, Nin, width=64, rng=None, rounds=4):
    """Beam search for an n-set through {0,1} with empty dominator set."""
    if rng is None:
        rng = np.random.default_rng(p * 1000 + n)
    NinI = Nin.astype(np.int32)
    for r in range(rounds):
        beam = [((0, 1), Nin[0] & Nin[1])]
        for depth in range(2, n):
            cand = {}
            for X, I in beam:
                cnt = NinI @ I.astype(np.int32)
                cnt[list(X)] = 10 ** 9
                noise = rng.random(p) * (0.5 if r else 0.0)
                order = np.argsort(cnt + noise)[: max(4, width // 4)]
                for c in order:
                    Y = tuple(sorted(X + (int(c),)))
                    if Y not in cand:
                        cand[Y] = int(cnt[c])
            items = sorted(cand.items(), key=lambda kv: kv[1])[:width]
            beam = []
            for Y, v in items:
                I = Nin[0] & Nin[1]
                for x in Y[2:]:
                    I = I & Nin[x]
                beam.append((Y, I))
                if v == 0 and depth == n - 1:
                    return list(Y)
        for Y, I in beam:
            if not I.any():
                return list(Y)
    return None


def main():
    nmax_full = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    pmax_w = int(sys.argv[2]) if len(sys.argv) > 2 else 2500
    t0 = time.time()
    out = {"convention": "x -> y iff y - x is a nonzero square mod p", "full": {}, "witness": {}}
    primes = [p for p in range(3, 20000) if p % 4 == 3 and is_prime(p)]
    for n in range(2, nmax_full + 1):
        fails = {}
        for p in primes:
            if p < 2 * n + 1:
                continue
            Nin = paley_in(p)
            ok, mn, bad, w = exact_Sn(p, n, Nin, stop_at_first=True)
            if not ok:
                assert w is not None and D_size(Nin, w) == 0 and len(set(w)) == n
                fails[p] = w
                continue
            # p is the least prime with S_n: recompute fully for nu_n
            ok2, mn2, bad2, _ = exact_Sn(p, n, Nin, stop_at_first=False)
            assert ok2
            row = {"p_n": p, "nu_n_at_p_n": mn2, "ln2_n2_2n": math.log(2) * n * n * 2 ** n,
                   "ratio_p_over_n2_2n": p / (n * n * 2 ** n), "ratio_p_over_n_2n": p / (n * 2 ** n),
                   "first_moment_threshold": first_moment_threshold(n),
                   "graham_spencer_sufficient": n * n * 2 ** (2 * n - 2),
                   "failing_primes_with_witness": {str(q): v for q, v in fails.items()}}
            out["full"][n] = row
            print(f"n={n}: least Paley p with S_n = {p} (nu_n = {mn2}); p/(n^2 2^n) = {row['ratio_p_over_n2_2n']:.4f}; "
                  f"random first-moment threshold = {row['first_moment_threshold']}; "
                  f"ln2 n^2 2^n = {row['ln2_n2_2n']:.1f}; GS = {row['graham_spencer_sufficient']}  "
                  f"[{time.time() - t0:.0f}s]", flush=True)
            break
    for n in (6, 7):
        fails = {}
        first_open = None
        for p in primes:
            if p < 2 * n + 1:
                continue
            if p > pmax_w:
                break
            Nin = paley_in(p)
            w = beam_witness(p, n, Nin)
            if w is not None:
                assert D_size(Nin, w) == 0 and len(set(w)) == n
                fails[p] = w
            elif first_open is None:
                first_open = p
                if n == 7:
                    break
        out["witness"][n] = {"searched_up_to": pmax_w, "first_p_without_witness": first_open,
                             "all_p_below_fail": first_open, "ln2_n2_2n": math.log(2) * n * n * 2 ** n,
                             "first_moment_threshold": first_moment_threshold(n),
                             "witnesses": {str(q): v for q, v in fails.items()}}
        print(f"n={n}: every Paley p = 3 mod 4 below {first_open} fails S_n (verified witness); "
              f"ln2 n^2 2^n = {math.log(2) * n * n * 2 ** n:.0f}; first-moment = {first_moment_threshold(n)}  "
              f"[{time.time() - t0:.0f}s]", flush=True)
    out["seconds"] = time.time() - t0
    with open(os.path.join(HERE, "r8f_paley.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1)


if __name__ == "__main__":
    main()
