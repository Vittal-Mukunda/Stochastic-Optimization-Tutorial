"""R8-F-asymptotic: in-degree information does not separate the barrier profile (exact check).

Run from the project root:  python research/compute/r8f_regular_check.py

Lemma 3.1' (degree form, proved in the report): for |A| = s, R = D(A), m = |R|, h <= nu_{s+1}, 1 <= k <= n,
    nu_k C(m, k) <= C(m - h, k) / (m - h) * sum_{r in R} d^-(r),
because C(x,k)/x is non-decreasing in x and sum_{y not in A} |N^+(y) cap R| = sum_{r in R} d^-(r).
For a near-regular T (every d^- <= ceil((N-1)/2)) this gives
    nu_k C(m, k) (m - h) <= C(m - h, k) m ceil((N-1)/2).
The script checks this inequality, in exact integers, for every level and every k on the barrier
profiles of r8f_barrier.py, i.e. the barrier is consistent with T being (near-)regular as well.
Writes research/compute/r8f_regular_check.json.
"""
from __future__ import annotations

import json
import os
import sys
from math import comb

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import r8f_barrier as B  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))


def check(m, n):
    N = m[0]
    dmax = N // 2  # = ceil((N-1)/2)
    for t in range(n):
        mt, h = m[t], m[t + 1]
        for k in range(1, n + 1):
            lhs = m[k] * comb(mt, k) * (mt - h)
            rhs = comb(mt - h, k) * mt * dmax
            if lhs > rhs:
                return False, (t, k)
    return True, None


def main():
    res = {}
    for n in (16, 24, 32, 48, 64, 100, 128, 200, 256):
        m = B.profile(n, B.IMAX)
        ok, v = check(m, n)
        res[n] = {"ok": ok, "violation": v, "N_over_n2n": m[0] / (n * 2 ** n)}
        print(n, ok, v, flush=True)
    with open(os.path.join(HERE, "r8f_regular_check.json"), "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=1)


if __name__ == "__main__":
    main()
