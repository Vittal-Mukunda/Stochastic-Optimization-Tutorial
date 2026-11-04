"""R8-F-asymptotic: exhaustive S_6 test of one Paley tournament QR_p.

Run from the project root:  python research/compute/r8f_paley6_exact.py p

Every 6-set is equivalent under x -> a x + b (a a nonzero square) to one containing the arc 0 -> 1,
so it suffices to show |D({0,1,a,b,c,d})| >= 1 for all 2 <= a < b < c < d <= p-1.  For fixed (a, b)
let I = D({0,1,a,b}); then |D({0,1,a,b,c,d})| = sum_{w in I} Nin[c,w] Nin[d,w], i.e. the (c, d) entry
of K K^T with K = Nin[b+1:, I].  Entries are integers < 2^24, exact in float32.
Reports S_6 yes/no, nu_6 = min |D| over 6-sets, and a witness if one exists.
Writes research/compute/r8f_paley6_exact_<p>.json.
"""
from __future__ import annotations

import os

os.environ.setdefault("OMP_NUM_THREADS", "3")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "3")

import json
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from r8f_paley import D_size, paley_in  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    p = int(sys.argv[1])
    Nin = paley_in(p)
    NinF = Nin.astype(np.float32)
    base = Nin[0] & Nin[1]
    t0 = time.time()
    nu6 = None
    witness = None
    count_min = 0
    blocks = 0
    for a in range(2, p):
        Ia = base & Nin[a]
        for b in range(a + 1, p - 1):
            I = Ia & Nin[b]
            cols = np.flatnonzero(I)
            if cols.size == 0:
                witness = [0, 1, a, b]
                break
            K = NinF[b + 1:, cols]
            if K.shape[0] < 2:
                continue
            G = K @ K.T  # G[i, j] = |D({0,1,a,b,c,d})| with c = b+1+i, d = b+1+j (symmetric)
            np.fill_diagonal(G, np.inf)
            mn = int(G.min())
            blocks += 1
            if nu6 is None or mn < nu6:
                nu6, count_min = mn, 0
            if mn == nu6:
                count_min += int((G == mn).sum()) // 2
            if mn == 0:
                i, j = map(int, np.argwhere(G == 0)[0])
                witness = [0, 1, a, b, min(i, j) + b + 1, max(i, j) + b + 1]
                break
        if witness is not None:
            break
        if a % 50 == 0:
            print(f"  a={a}  nu6 so far={nu6}  [{time.time() - t0:.0f}s]", flush=True)
    res = {"p": p, "has_S6": witness is None, "nu_6": 0 if witness else nu6,
           "witness": witness, "pairs_ab_processed": blocks, "seconds": time.time() - t0,
           "number_of_6sets_through_01_attaining_min": None if witness else count_min}
    if witness:
        assert D_size(Nin, witness) == 0
    print(res, flush=True)
    with open(os.path.join(HERE, f"r8f_paley6_exact_{p}.json"), "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=1)


if __name__ == "__main__":
    main()
