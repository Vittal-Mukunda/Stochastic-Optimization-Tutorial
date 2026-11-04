#!/usr/bin/env python3
"""Moment-ILP relaxation for Erdos #902 (F1 tournaments on N vertices).

Usage:
    python moment_ilp.py N [--time-limit SECONDS] [--no-e-filter]
    python moment_ilp.py --selftest

Writes result_N{N}.json next to this file and, when the model is feasible,
witness_N{N}.json. The solver status is reported as returned by
scipy.optimize.milp; nothing is inferred beyond that.

Notation. T is a tournament on N vertices, d(v) is the in-degree of v, and for a
pair P = {w, w2}, D(P) is the set of vertices outside P beating both endpoints.
For P with in-degrees a, b and |D(P)| = D, the number of vertices outside P
beaten by both endpoints is E_P = N - 1 + D - a - b.
For a triple Y, k(Y) is the number of dominators of Y (vertices outside Y beating
all of Y).

Domain restrictions (from the task, supported by Lemmas F2/F3 of
proof/F4_GE_52_HAND_PROOF.md, not re-derived here):
    d(v) >= 23, |D(P)| >= 11, k(Y) >= 5 (the last is the F1 hypothesis itself).
"""
import argparse
import json
import os
import platform
import random
import sys
import time
from math import comb

import numpy as np
import scipy
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import coo_matrix

OUTDIR = os.path.dirname(os.path.abspath(__file__))
DMIN, DLOW, KMIN = 23, 11, 5
INF = np.inf


def build(N, dmin=DMIN, dlow=DLOW, kmin=KMIN, e_filter=True, support_exact=True):
    """Assemble the integer program. Returns a dict with the sparse matrix and bounds.

    e_filter=True drops pair classes (a, b, D) with E = N-1-a-b+D < 0. Such a class
    cannot occur in any tournament, because E is a count of vertices, so the
    restriction is exact.

    support_exact=True adds C7c: z_D <= sum over (a, b) of p_{a,b,D}. Without it z_D
    is only an upper-bound indicator (C7a), so the solver may set z_D = 1 with no pair
    of that D-value, which makes C7b vacuous. C7c makes z the support indicator the
    task describes. support_exact=False reproduces the task's C1-C7 literally.
    """
    degs = list(range(dmin, N))          # d in [dmin, N-1]
    Ds = list(range(dlow, N - 1))        # D in [dlow, N-2]
    ks = list(range(kmin, N - 2))        # k in [kmin, N-3]
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

    idx = {}
    lo, hi, integ = [], [], []

    def add(key, l, u):
        idx[key] = len(lo)
        lo.append(l)
        hi.append(u)
        integ.append(1)

    for d in degs:
        add(("n", d), 0, N)
    for P in pairs:
        add(("p",) + P, 0, comb(N, 2))
    for k in ks:
        add(("h", k), 0, comb(N, 3))
    for D in Ds:
        add(("z", D), 0, 1)
    nv = len(lo)

    rows = []  # (coefficient dict, row lower, row upper)

    def eq(c, r):
        rows.append((c, r, r))

    def le(c, r):
        rows.append((c, -INF, r))

    N2, N3 = comb(N, 2), comb(N, 3)

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

    # C5: sum of k(Y) over triples = sum over vertices of C(out-degree, 3).
    eq({idx[("h", k)]: 1 for k in ks}, N3)
    c = {idx[("h", k)]: k for k in ks}
    for d in degs:
        c[idx[("n", d)]] = -comb(N - 1 - d, 3)
    eq(c, 0)

    # C6: sum over triples of C(k, 2) = sum over pairs of C(E_P, 3).
    c = {idx[("h", k)]: comb(k, 2) for k in ks}
    for P in pairs:
        E = N - 1 + P[2] - P[0] - P[1]
        coef = comb(E, 3) if E >= 3 else 0
        if coef:
            c[idx[("p",) + P]] = -coef
    eq(c, 0)

    # C7a: a pair class with positive count forces its D-value to be in the support.
    for P in pairs:
        le({idx[("p",) + P]: 1, idx[("z", P[2])]: -N2}, 0)

    # C7b: a triple with k dominators needs some pair with D >= k in the support.
    for k in ks:
        c = {idx[("h", k)]: 1}
        for D in Ds:
            if D >= k:
                c[idx[("z", D)]] = -N3
        le(c, 0)

    # C7c (fix, see build docstring): z_D = 1 only if some pair class has |D(P)| = D.
    if support_exact:
        for D in Ds:
            c = {idx[("z", D)]: 1}
            for P in pairs:
                if P[2] == D:
                    c[idx[("p",) + P]] = -1
            le(c, 0)

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
        degs=degs, pairs=pairs, Ds=Ds, ks=ks, nrows=len(rows), nvars=nv,
    )


def violation(M, x):
    res = M["A"] @ x
    v_rows = np.maximum(np.maximum(M["rlo"] - res, res - M["rhi"]), 0).max() if len(res) else 0.0
    v_bnd = np.maximum(np.maximum(M["lo"] - x, x - M["hi"]), 0).max()
    v_int = np.abs(x - np.round(x)).max()
    return float(v_rows), float(v_bnd), float(v_int)


def witness(M, x):
    N = M["N"]
    idx = M["idx"]
    xi = np.round(x).astype(int)
    n = {d: int(xi[idx[("n", d)]]) for d in M["degs"]}
    p = [
        {"a": a, "b": b, "D": D, "count": int(xi[idx[("p", a, b, D)]])}
        for (a, b, D) in M["pairs"] if xi[idx[("p", a, b, D)]] > 0
    ]
    h = {k: int(xi[idx[("h", k)]]) for k in M["ks"]}
    z = {D: int(xi[idx[("z", D)]]) for D in M["Ds"]}
    deg_hist = {d: c for d, c in n.items() if c}
    D_hist = {}
    for q in p:
        D_hist[q["D"]] = D_hist.get(q["D"], 0) + q["count"]
    tri_hist = {k: c for k, c in h.items() if c}
    return dict(N=N, n_d=deg_hist, p=p, h_k=tri_hist, z_D={D: c for D, c in z.items() if c},
                degree_histogram=deg_hist, D_histogram=dict(sorted(D_hist.items())),
                triple_count_histogram=tri_hist)


def solve(N, time_limit, e_filter=True, support_exact=True):
    tag = ("" if support_exact else "_specLiteral") + ("" if e_filter else "_noEfilter")
    M = build(N, e_filter=e_filter, support_exact=support_exact)
    t0 = time.time()
    res = milp(
        c=np.zeros(M["nvars"]),
        constraints=LinearConstraint(M["A"], M["rlo"], M["rhi"]),
        integrality=M["integ"],
        bounds=Bounds(M["lo"], M["hi"]),
        options={"time_limit": float(time_limit), "disp": False},
    )
    wall = time.time() - t0
    status_map = {0: "feasible", 2: "infeasible", 1: "time_limit", 3: "unbounded", 4: "other"}
    status = status_map.get(res.status, f"other({res.status})")
    out = dict(
        N=N, status=status, scipy_status=int(res.status), message=str(res.message),
        wall_seconds=round(wall, 3), time_limit_seconds=time_limit,
        rows=M["nrows"], vars=M["nvars"], e_filter=e_filter,
        support_exact=support_exact, tag=tag or "main",
        n_pair_classes=len(M["pairs"]),
    )
    if res.status == 1 and res.x is not None:
        out["status"] = "time_limit_with_incumbent"
    if res.x is not None:
        x = res.x
        vr, vb, vi = violation(M, x)
        out["max_row_violation"] = vr
        out["max_bound_violation"] = vb
        out["max_integrality_violation"] = vi
        if vr <= 1e-6 and vb <= 1e-6 and vi <= 1e-6:
            out["witness_verified_against_constraints"] = True
            w = witness(M, x)
            out["witness_summary"] = {k: w[k] for k in
                                      ("degree_histogram", "D_histogram", "triple_count_histogram")}
            with open(os.path.join(OUTDIR, f"witness_N{N}{tag}.json"), "w") as f:
                json.dump(w, f, indent=1)
        else:
            out["witness_verified_against_constraints"] = False
    with open(os.path.join(OUTDIR, f"result_N{N}{tag}.json"), "w") as f:
        json.dump(dict(out, env=env_info()), f, indent=1)
    return out


def selftest(trials=40, seed=1):
    """Check that the identities in C1-C7 hold exactly for real tournaments.

    Uses the domain-free build (all degrees, D and k values allowed, no E filter) and
    assigns the actual counts of a random tournament to the variables. Every
    residual must be zero (C1-C6) or nonpositive (C7).
    """
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
        M = build(N, dmin=0, dlow=0, kmin=0, e_filter=False)
        x = np.zeros(M["nvars"])
        for v in range(N):
            x[M["idx"][("n", indeg[v])]] += 1
        Dval = {}
        for u in range(N):
            for v in range(u + 1, N):
                D = sum(1 for w in range(N) if w not in (u, v) and beats[w][u] and beats[w][v])
                Dval[(u, v)] = D
                a, b = sorted((indeg[u], indeg[v]))
                key = ("p", a, b, D)
                x[M["idx"][key]] += 1
                x[M["idx"][("z", D)]] = 1
        from itertools import combinations
        for Y in combinations(range(N), 3):
            k = sum(1 for w in range(N) if w not in Y and all(beats[w][y] for y in Y))
            x[M["idx"][("h", k)]] += 1
        vr, vb, vi = violation(M, x)
        worst = max(worst, vr)
        if vr > 1e-9 or vb > 1e-9 or vi > 1e-9:
            return dict(ok=False, trial=t, N=N, max_row_violation=vr)
    return dict(ok=True, trials=trials, worst_row_violation=worst)


def env_info():
    return dict(python=sys.version.split()[0], numpy=np.__version__, scipy=scipy.__version__,
                platform=platform.platform())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("N", type=int, nargs="?")
    ap.add_argument("--time-limit", type=float, default=600.0)
    ap.add_argument("--no-e-filter", action="store_true")
    ap.add_argument("--spec-literal", action="store_true",
                    help="omit C7c (the support-exact fix); tagged _specLiteral")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        print(json.dumps(dict(env=env_info(), identity_selftest=selftest()), indent=1))
        return
    if args.N is None:
        ap.error("N required unless --selftest")
    out = solve(args.N, args.time_limit, e_filter=not args.no_e_filter,
                support_exact=not args.spec_literal)
    out["env"] = env_info()
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
