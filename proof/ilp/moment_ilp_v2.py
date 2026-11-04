#!/usr/bin/env python3
"""Stronger moment-ILP for F1 tournaments on N vertices (v2).

F1: every triple has at least 5 dominators. S_4 implies F1, so infeasibility here
proves that no F1 (hence no S_4) tournament on N vertices exists.

Relative to moment_ilp.py (v1) this adds:
  * g_l: histogram of l(W) = |D+(W)|, the number of vertices beaten by all of a
    triple W, with  sum g = C(N,3),  sum l*g = sum_v C(d_v,3),
    sum C(l,2)*g = sum_P C(|D(P)|,3);
  * the universal third-moment identity  sum_Y C(k,3) = sum_W C(l,3)
    (count pairs (Y,W) with W inside D(Y));
  * support constraints for l, tied to real pair classes (l(W) <= E_P for P in W);
  * hand lemmas as cuts: for N = 52, no in-degree 23 (Lemma B), and for every N at
    most five vertices of in-degree 24 (Claim Q, [EP] Lemma 2.3).

Usage:
  python moment_ilp_v2.py --selftest
  python moment_ilp_v2.py N [--time-limit SECONDS]
"""
import argparse
import json
import os
import platform
import random
import sys
import time
from itertools import combinations
from math import comb

import numpy as np
import scipy
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import coo_matrix

OUTDIR = os.path.dirname(os.path.abspath(__file__))
INF = np.inf


def build(N, dmin=None, dlow=11, kmin=5, lmin=0, e_filter=True, claim_q=True):
    """Assemble the integer program. Returns a dict with the sparse matrix and bounds."""
    if dmin is None:
        dmin = 24 if N == 52 else 23
    degs = list(range(dmin, N))          # in-degree d in [dmin, N-1]
    Ds = list(range(dlow, N - 1))        # |D(P)| in [dlow, N-2]
    ks = list(range(kmin, N - 2))        # dominators k in [kmin, N-3]
    ls = list(range(lmin, N - 2))        # dominated count l in [lmin, N-3]
    pairs = []
    for a in degs:
        for b in degs:
            if b < a:
                continue
            for D in Ds:
                E = N - 1 + D - a - b
                if e_filter and (E < 0 or E > N - 2):
                    continue
                pairs.append((a, b, D))

    # E_P values that occur among the pair classes (E_P in [0, N-2] when e_filter is on).
    Es = sorted({N - 1 + P[2] - P[0] - P[1] for P in pairs})

    idx, lo, hi, integ = {}, [], [], []

    def add(key, l, u):
        idx[key] = len(lo)
        lo.append(l)
        hi.append(u)
        integ.append(1)

    N2, N3 = comb(N, 2), comb(N, 3)
    for d in degs:
        add(("n", d), 0, N)
    for P in pairs:
        add(("p",) + P, 0, N2)
    for k in ks:
        add(("h", k), 0, N3)
    for l in ls:
        add(("g", l), 0, N3)
    for D in Ds:
        add(("z", D), 0, 1)
    for E in Es:
        add(("y", E), 0, 1)
    nv = len(lo)

    rows = []  # (coefficient dict, row lower, row upper)

    def eq(c, r):
        rows.append((c, r, r))

    def le(c, r):
        rows.append((c, -INF, r))

    # C1: vertex count and edge count.
    eq({idx[("n", d)]: 1 for d in degs}, N)
    eq({idx[("n", d)]: d for d in degs}, N2)

    # C2: pair count.
    eq({idx[("p",) + P]: 1 for P in pairs}, N2)

    # C3: for each degree a, (N-1) n_a = number of pair endpoints of degree a.
    for a in degs:
        c = {idx[("n", a)]: N - 1}
        for P in pairs:
            m = (P[0] == a) + (P[1] == a)
            if m:
                c[idx[("p",) + P]] = -m
        eq(c, 0)

    # C4: sum over pairs of |D(P)| = sum over vertices of C(out-degree, 2).
    c = {idx[("p",) + P]: P[2] for P in pairs}
    for d in degs:
        c[idx[("n", d)]] = -comb(N - 1 - d, 2)
    eq(c, 0)

    # C5: sum over triples of k = sum over vertices of C(out-degree, 3).
    eq({idx[("h", k)]: 1 for k in ks}, N3)
    c = {idx[("h", k)]: k for k in ks}
    for d in degs:
        c[idx[("n", d)]] = -comb(N - 1 - d, 3)
    eq(c, 0)

    # C5': sum over triples of l = sum over vertices of C(in-degree, 3).
    eq({idx[("g", l)]: 1 for l in ls}, N3)
    c = {idx[("g", l)]: l for l in ls}
    for d in degs:
        c[idx[("n", d)]] = -comb(d, 3)
    eq(c, 0)

    # C6: sum over triples of C(k, 2) = sum over pairs of C(E_P, 3).
    c = {idx[("h", k)]: comb(k, 2) for k in ks}
    for P in pairs:
        E = N - 1 + P[2] - P[0] - P[1]
        cp = comb(E, 3) if E >= 3 else 0
        if cp:
            c[idx[("p",) + P]] = -cp
    eq(c, 0)

    # C6': sum over triples of C(l, 2) = sum over pairs of C(|D(P)|, 3).
    c = {idx[("g", l)]: comb(l, 2) for l in ls}
    for P in pairs:
        cp = comb(P[2], 3) if P[2] >= 3 else 0
        if cp:
            c[idx[("p",) + P]] = -cp
    eq(c, 0)

    # C8: universal third-moment identity sum_Y C(k,3) = sum_W C(l,3).
    c = {idx[("h", k)]: comb(k, 3) for k in ks}
    for l in ls:
        cl = comb(l, 3)
        if cl:
            c[idx[("g", l)]] = -cl
    eq(c, 0)

    # C7a: a pair class with positive count forces its D-value into the support.
    for P in pairs:
        le({idx[("p",) + P]: 1, idx[("z", P[2])]: -N2}, 0)

    # C7b: a triple with k dominators needs some pair with D >= k in the support.
    for k in ks:
        c = {idx[("h", k)]: 1}
        for D in Ds:
            if D >= k:
                c[idx[("z", D)]] = -N3
        le(c, 0)

    # C7c: z_D = 1 only if some pair class has |D(P)| = D.
    for D in Ds:
        c = {idx[("z", D)]: 1}
        for P in pairs:
            if P[2] == D:
                c[idx[("p",) + P]] = -1
        le(c, 0)

    # C7d/e/f: the same support logic for E_P, which bounds l(W).
    for P in pairs:
        E = N - 1 + P[2] - P[0] - P[1]
        le({idx[("p",) + P]: 1, idx[("y", E)]: -N2}, 0)
    for E in Es:
        c = {idx[("y", E)]: 1}
        for P in pairs:
            if N - 1 + P[2] - P[0] - P[1] == E:
                c[idx[("p",) + P]] = -1
        le(c, 0)
    for l in ls:
        c = {idx[("g", l)]: 1}
        for E in Es:
            if E >= l:
                c[idx[("y", E)]] = -N3
        le(c, 0)

    # Hand cut (Claim Q, [EP] Lemma 2.3): at most five vertices of in-degree 24.
    if claim_q and 24 in degs:
        le({idx[("n", 24)]: 1}, 5)

    r, cc, v, rlo, rhi = [], [], [], [], []
    for i, (c, l, u) in enumerate(rows):
        for j, val in c.items():
            if val != 0:
                r.append(i)
                cc.append(j)
                v.append(float(val))
        rlo.append(l)
        rhi.append(u)
    A = coo_matrix((v, (r, cc)), shape=(len(rows), nv)).tocsr()
    return dict(
        N=N, idx=idx, A=A, rlo=np.array(rlo, float), rhi=np.array(rhi, float),
        lo=np.array(lo, float), hi=np.array(hi, float), integ=np.array(integ),
        degs=degs, pairs=pairs, Ds=Ds, ks=ks, ls=ls, Es=Es,
        nrows=len(rows), nvars=nv,
    )


def violation(M, x):
    res = M["A"] @ x
    v_rows = float(np.maximum(np.maximum(M["rlo"] - res, res - M["rhi"]), 0).max()) if len(res) else 0.0
    v_bnd = float(np.maximum(np.maximum(M["lo"] - x, x - M["hi"]), 0).max())
    v_int = float(np.abs(x - np.round(x)).max())
    return v_rows, v_bnd, v_int


def relaxation_point(M, x):
    N = M["N"]
    idx = M["idx"]
    xi = np.round(x).astype(int)
    n_hist = {d: int(xi[idx[("n", d)]]) for d in M["degs"] if xi[idx[("n", d)]]}
    D_hist, p_list = {}, []
    for (a, b, D) in M["pairs"]:
        c = int(xi[idx[("p", a, b, D)]])
        if c:
            p_list.append({"a": a, "b": b, "D": D, "count": c})
            D_hist[D] = D_hist.get(D, 0) + c
    k_hist = {k: int(xi[idx[("h", k)]]) for k in M["ks"] if xi[idx[("h", k)]]}
    l_hist = {l: int(xi[idx[("g", l)]]) for l in M["ls"] if xi[idx[("g", l)]]}
    return dict(N=N, degree_histogram=n_hist, D_histogram=dict(sorted(D_hist.items())),
                triple_dominator_histogram=k_hist, triple_dominated_histogram=l_hist,
                pair_classes=p_list)


def selftest(trials=40, seed=1):
    """The identities must hold exactly for real tournaments (domain-free build)."""
    rng = random.Random(seed)
    worst = 0.0
    for t in range(trials):
        N = rng.randint(6, 11)
        beats = [[False] * N for _ in range(N)]
        for u in range(N):
            for v in range(u + 1, N):
                if rng.random() < 0.5:
                    beats[u][v] = True
                else:
                    beats[v][u] = True
        indeg = [sum(beats[w][v] for w in range(N)) for v in range(N)]
        M = build(N, dmin=0, dlow=0, kmin=0, lmin=0, e_filter=False, claim_q=False)
        x = np.zeros(M["nvars"])
        for v in range(N):
            x[M["idx"][("n", indeg[v])]] += 1
        for u in range(N):
            for v in range(u + 1, N):
                D = sum(1 for w in range(N) if w not in (u, v) and beats[w][u] and beats[w][v])
                a, b = sorted((indeg[u], indeg[v]))
                E = N - 1 + D - a - b
                x[M["idx"][("p", a, b, D)]] += 1
                x[M["idx"][("z", D)]] = 1
                x[M["idx"][("y", E)]] = 1
        for Y in combinations(range(N), 3):
            k = sum(1 for w in range(N) if w not in Y and all(beats[w][y] for y in Y))
            l = sum(1 for w in range(N) if w not in Y and all(beats[y][w] for y in Y))
            x[M["idx"][("h", k)]] += 1
            x[M["idx"][("g", l)]] += 1
        vr, vb, vi = violation(M, x)
        worst = max(worst, vr)
        if vr > 1e-9 or vb > 1e-9 or vi > 1e-9:
            return dict(ok=False, trial=t, N=N, max_row_violation=vr)
    return dict(ok=True, trials=trials, worst_row_violation=worst)


def env_info():
    return dict(python=sys.version.split()[0], numpy=np.__version__, scipy=scipy.__version__,
                platform=platform.platform())


def solve(N, time_limit, e_filter=True):
    M = build(N, e_filter=e_filter)
    t0 = time.time()
    res = milp(
        c=np.zeros(M["nvars"]),
        constraints=LinearConstraint(M["A"], M["rlo"], M["rhi"]),
        integrality=M["integ"],
        bounds=Bounds(M["lo"], M["hi"]),
        options={"time_limit": float(time_limit), "disp": False},
    )
    wall = time.time() - t0
    status_map = {0: "feasible", 1: "time_limit", 2: "infeasible", 3: "unbounded", 4: "other"}
    out = dict(
        N=N, model="v2", status=status_map.get(res.status, f"other({res.status})"),
        scipy_status=int(res.status), message=str(res.message),
        wall_seconds=round(wall, 3), time_limit_seconds=float(time_limit),
        rows=M["nrows"], vars=M["nvars"], n_pair_classes=len(M["pairs"]),
        e_filter=e_filter, env=env_info(),
    )
    if res.status == 1 and res.x is not None:
        out["status"] = "time_limit_with_incumbent"
    if res.x is not None:
        vr, vb, vi = violation(M, res.x)
        out.update(max_row_violation=vr, max_bound_violation=vb, max_integrality_violation=vi)
        if vr <= 1e-6 and vb <= 1e-6 and vi <= 1e-6:
            out["relaxation_point_verified"] = True
            pt = relaxation_point(M, res.x)
            out["relaxation_point_summary"] = {k: pt[k] for k in
                                               ("degree_histogram", "D_histogram",
                                                "triple_dominator_histogram")}
            with open(os.path.join(OUTDIR, f"relaxation_point_v2_N{N}.json"), "w") as f:
                json.dump(pt, f, indent=1)
        else:
            out["relaxation_point_verified"] = False
    with open(os.path.join(OUTDIR, f"result_v2_N{N}.json"), "w") as f:
        json.dump(out, f, indent=1)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("N", type=int, nargs="?")
    ap.add_argument("--time-limit", type=float, default=600.0)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        print(json.dumps(dict(env=env_info(), identity_selftest=selftest()), indent=1))
        return
    if args.N is None:
        ap.error("N required unless --selftest")
    print(json.dumps(solve(args.N, args.time_limit), indent=1))


if __name__ == "__main__":
    main()
