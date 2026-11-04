"""R8-G local search driver: tabu search on arc reversals for S_4 at order N.

Seed families
  reg  : random tournament with in-degrees floor((N-1)/2), ceil((N-1)/2) (25/26 at N=52):
         rotational tournament randomised by score-preserving 3-cycle reversals.
  qr   : QR_67 minus 67-N vertices S, S chosen by local search so the remaining
         in-degrees are as equal as possible (25/26 at N=52); best of several S by cost.
  circ : circulant on Z_n (n = N if N odd, else n = N+1 with vertex 0 deleted), connection
         set S chosen by local search to make |S cap (S+x)| as constant as possible
         (doubly-regular-like), excluding the quadratic residues when n = 67.

Usage: python r8g_search.py --N 52 --seeds reg,qr,circ --minutes 27 --seed 1 --tag p1
"""
import argparse
import json
import os
import sys
import time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import r8g_core as C


def seed_reg(N, rng, sweeps=10):
    h = (N - 1) // 2
    A = np.zeros((N, N), dtype=bool)
    for i in range(N):
        for d in range(1, h + 1):
            A[i, (i + d) % N] = True
    if N % 2 == 0:  # diametral pairs: orient i -> i+N/2 for i < N/2
        for i in range(N // 2):
            A[i, i + N // 2] = True
    assert C.is_tournament(A)
    target = sweeps * N * N
    done = 0
    while done < target:
        t = rng.choice(N, 3, replace=False)
        a, b, c = t
        if A[a, b] and A[b, c] and A[c, a]:
            A[a, b], A[b, c], A[c, a] = False, False, False
            A[b, a], A[c, b], A[a, c] = True, True, True
            done += 1
        elif A[b, a] and A[c, b] and A[a, c]:
            A[b, a], A[c, b], A[a, c] = False, False, False
            A[a, b], A[b, c], A[c, a] = True, True, True
            done += 1
        else:
            done += 0.25
    return A


def seed_qr(N, rng, tries=6):
    P = C.paley(67)
    k = 67 - N
    tgt = (N - 1) / 2.0
    best = None
    for _ in range(tries):
        S = set(rng.choice(67, k, replace=False).tolist())

        def obj(S):
            keep = [v for v in range(67) if v not in S]
            sub = P[np.ix_(keep, keep)]
            return float(((sub.sum(axis=0) - tgt) ** 2).sum())

        cur = obj(S)
        for _ in range(400):
            a = int(rng.choice(sorted(S)))
            b = int(rng.integers(67))
            if b in S:
                continue
            S2 = (S - {a}) | {b}
            o = obj(S2)
            if o <= cur:
                S, cur = S2, o
        keep = [v for v in range(67) if v not in S]
        A = P[np.ix_(keep, keep)].copy()
        c = C.Tabu(A).cost
        if best is None or c < best[0]:
            best = (c, A, sorted(S), cur)
    return best[1], {"deleted": best[2], "degree_obj": best[3]}


def seed_qr47(N, rng):
    """QR_47 on vertices 0..46 plus N-47 new vertices with uniformly random arcs."""
    A = np.zeros((N, N), dtype=bool)
    A[:47, :47] = C.paley(47)
    for i in range(47, N):
        for j in range(i):
            if rng.random() < 0.5:
                A[i, j] = True
            else:
                A[j, i] = True
    return A, {"base": "QR_47", "added": N - 47}


def seed_circ(N, rng):
    n = N if N % 2 == 1 else N + 1
    h = (n - 1) // 2
    qr = {(x * x) % n for x in range(1, n)}
    while True:
        S = set()
        for x in range(1, h + 1):
            S.add(x if rng.random() < 0.5 else n - x)

        def obj(S):
            ind = np.zeros(n, dtype=bool)
            ind[list(S)] = True
            lam = np.array([np.sum(ind & np.roll(ind, x)) for x in range(1, n)])
            return float(((lam - lam.mean()) ** 2).sum())

        cur = obj(S)
        for _ in range(1500):
            x = int(rng.integers(1, h + 1))
            S2 = set(S)
            if x in S2:
                S2.remove(x); S2.add(n - x)
            else:
                S2.remove(n - x); S2.add(x)
            o = obj(S2)
            if o <= cur:
                S, cur = S2, o
        if not (n == 67 and S in (qr, {n - s for s in qr})):
            break
    A = C.circulant(n, S)
    if n != N:
        A = A[1:, 1:]
    return A.copy(), {"n": n, "S": sorted(S), "dr_obj": cur}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--N", type=int, required=True)
    ap.add_argument("--seeds", default="reg,qr,circ")
    ap.add_argument("--minutes", type=float, required=True)
    ap.add_argument("--restart_seconds", type=float, default=300)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--tag", default="x")
    ap.add_argument("--lam", type=float, default=1.0)
    ap.add_argument("--stall", type=int, default=1500)
    args = ap.parse_args()
    N = args.N
    rng = np.random.default_rng(args.seed)
    t_global = time.time()
    budget = args.minutes * 60
    logpath = os.path.join(HERE, f"r8g_log_{N}_{args.tag}.json")
    log = {"N": N, "args": vars(args), "runs": []}
    best_all = None
    kinds = args.seeds.split(",")
    r = 0
    while time.time() - t_global < budget - 20:
        kind = kinds[r % len(kinds)]
        r += 1
        if kind == "reg":
            A, meta = seed_reg(N, rng), {}
        elif kind == "qr":
            A, meta = seed_qr(N, rng)
        elif kind == "qr47":
            A, meta = seed_qr47(N, rng)
        else:
            A, meta = seed_circ(N, rng)
        T = C.Tabu(A, lam=args.lam, rng=rng)
        c0 = T.cost
        p0 = C.profile(A)
        remaining = budget - (time.time() - t_global)
        tl = min(args.restart_seconds, remaining - 5)
        t1 = time.time()
        res = T.run(time_limit=tl, stall=args.stall)
        bestA = res["bestA"]
        pr = C.profile(bestA)
        entry = {"run": r, "seed_kind": kind, "seed_meta": meta, "seed_cost": c0,
                 "seed_undominated": p0["undominated_4sets"], "best_cost": res["best"],
                 "iters": res["iters"], "kicks": res["kicks"],
                 "seconds": round(time.time() - t1, 1), "trace": res["trace"][-15:],
                 "profile": pr}
        log["runs"].append(entry)
        print(f"[N={N} {args.tag}] run {r} {kind}: seed cost {c0:.0f} -> best {res['best']:.1f} "
              f"(U4={pr['undominated_4sets']}, min triple dom {pr['min_triple_dom']}, "
              f"min pair dom {pr['min_pair_dom']}, iters {res['iters']})", flush=True)
        key = (pr["undominated_4sets"], res["best"])
        if best_all is None or key < best_all[0]:
            best_all = (key, bestA.copy(), entry)
            C.save_tournament(os.path.join(HERE, f"r8g_best_{N}_{args.tag}.txt"), bestA,
                              [f"R8-G best at N={N} tag={args.tag} run={r} seed={kind}",
                               f"cost(lam={args.lam})={res['best']} undominated_4sets={pr['undominated_4sets']}",
                               f"min_pair_dom={pr['min_pair_dom']} min_triple_dom={pr['min_triple_dom']}",
                               "row w, column x = 1 iff w -> x"])
        if pr["S4"]:
            C.save_tournament(os.path.join(HERE, f"r8g_CANDIDATE_{N}_{args.tag}.txt"), bestA,
                              [f"S_4 CANDIDATE N={N}: verify with r8g_check2.py"])
            print("!!! S_4 candidate found", flush=True)
        log["best"] = {"undominated_4sets": best_all[0][0], "cost": best_all[0][1],
                       "run": best_all[2]["run"], "seed_kind": best_all[2]["seed_kind"],
                       "profile": best_all[2]["profile"]}
        log["elapsed_seconds"] = round(time.time() - t_global, 1)
        with open(logpath, "w", encoding="utf-8") as f:
            json.dump(log, f, indent=1)
        if pr["S4"]:
            break


if __name__ == "__main__":
    main()
