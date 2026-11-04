"""R8-F-asymptotic: targeted search for undominated 6-sets in Paley tournaments QR_p.

Run from the project root:  python research/compute/r8f_paley6.py p1 p2 ... [--budget SECONDS]

For each p: order the 4-sets {0,1,a,b} by |D({0,1,a,b})| (smallest first) and, for each, compute
|D({0,1,a,b,c,d})| for ALL pairs (c,d) at once by one matrix product.  Stops at the first
undominated 6-set (re-verified) or when the time budget is spent; reports how many 4-sets were
completed exhaustively.  A found set proves that QR_p fails S_6.  No witness is NOT a proof of S_6.
Appends to research/compute/r8f_paley6.json.
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


def search(p, budget):
    Nin = paley_in(p)
    NinF = Nin.astype(np.float32)
    base = Nin[0] & Nin[1]
    c3 = NinF @ base.astype(np.float32)  # |D({0,1,a})|
    t0 = time.time()
    # candidate 4-sets ordered by |D|
    A = [a for a in np.argsort(c3) if a >= 2][: 200]
    pairs = []
    for a in A:
        Ia = base & Nin[a]
        c4 = NinF @ Ia.astype(np.float32)
        for b in np.argsort(c4)[:60]:
            if b >= 2 and b != a:
                pairs.append((int(c4[b]), int(min(a, b)), int(max(a, b))))
    pairs = sorted(set(pairs))
    done = 0
    for size, a, b in pairs:
        if time.time() - t0 > budget:
            break
        I = base & Nin[a] & Nin[b]
        M = (Nin & I[None, :]).astype(np.float32)
        cnt = M @ NinF.T
        excl = [0, 1, a, b]
        cnt[excl, :] = 1
        cnt[:, excl] = 1
        np.fill_diagonal(cnt, 1)
        z = np.argwhere(cnt == 0)
        done += 1
        if len(z):
            c, d = map(int, z[0])
            X = [0, 1, a, b, c, d]
            assert D_size(Nin, X) == 0 and len(set(X)) == 6
            return {"p": p, "witness": X, "four_sets_completed": done, "seconds": time.time() - t0}
    return {"p": p, "witness": None, "four_sets_completed": done, "seconds": time.time() - t0,
            "min_D_of_4set_tried": pairs[0][0] if pairs else None}


def main():
    args = sys.argv[1:]
    budget = 60.0
    if "--budget" in args:
        i = args.index("--budget")
        budget = float(args[i + 1])
        args = args[:i] + args[i + 2:]
    path = os.path.join(HERE, "r8f_paley6.json")
    res = json.load(open(path)) if os.path.exists(path) else {}
    for p in map(int, args):
        r = search(p, budget)
        res[str(p)] = r
        print(r, flush=True)
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(res, fh, indent=1)


if __name__ == "__main__":
    main()
