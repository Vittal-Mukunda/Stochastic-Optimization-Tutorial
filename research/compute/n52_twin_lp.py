"""N = 52 session 2026-11-04: how far can exact counting go against the regular twin family?

Run from the project root:   python research/compute/n52_twin_lp.py
Writes research/compute/n52_twin_lp.json (log: n52_twin_lp.log).  Floating-point LP (scipy / HiGHS).

The regular twin family (proof/N52_SESSION_2026-11-04.md, section T1): T' regular on 51 vertices, b0 a vertex,
W = N^-(b0), B = N^+(b0); g_P = |D(P)| - 12 lives on pairs inside B.  Triples of T' are split into regions
  b0  (through b0), W (inside W), B (inside B), WWB, WBB,
and inside a region by sigma (transitive / cyclic) and G (sum of g over the three pairs).  For every class the
LP has one variable per admissible value of k = |D(Y)|: the number of triples of that class with that k.  Then
u = k - L/2, L = 12 - sigma + G.

Model configuration (a pair-level ansatz, NOT a tournament): n pairs of B with g = +1, n with g = -1, the rest 0;
lambda_B = 5 on the -1 pairs (forced, Lemma R of the session file) and lambda_B = lam_plus on the +1 pairs; the
nonzero pairs arranged as alternating 4-cycles, so that every triangle of B meets at most one nonzero pair except
the 4 "couple" triangles per 4-cycle, which are transitive with G = 0 (Theta = Psi_C = 0).  For n > 6 the
4-cycles cannot be vertex-disjoint on 25 vertices, so large n is a formal extrapolation of the class counts.

Exact equalities used (each derived by hand in the session file, section L):
  E1 class sizes;  E2 sum of k in each region: b0 6900, W 12650, B 13300, WWB 43200, WBB 41250;
  E3 sum_T u = sum_C u = 0 globally and inside region b0;  E4 sum of G u per region (b0, WBB, B);
  E5 per-pair sums over WBB: sum_w k(w + P) = 132 + 12 g + lambda_B (aggregated by G-class);
  E6 k fixed on the b0-triples of nonzero pairs (k = omega = 11 + g - lambda_B), and k = 5 on every WBB triple
     through a -1 pair (Lemma R);
  E7 global cubic identity sum (u^3 + c(L) u) = 0;  E8 region b0: sum u^2 = 975 + Gamma2/4;
  E9 local cubic identities at b0: sum_{Y ni b0} C(k,3) = sum_{Z in W} C(l_Z - 1, 2) and
     sum_{Y ni b0} C(l,3) = sum_{Z in B} C(k_Z - 1, 2).
Inequalities: k >= 5 outside B, k >= 4 inside B, 0 <= l = L - k.

The LP maximises sum_Y u^2 (which must equal 16575 - Gamma2/4 + Gamma3/3, Gamma3 = 0 here).  If the maximum is
smaller, the identities exclude the configuration; the difference is the margin.  Lemma C' corresponds to the
subset {E1, E2(B only), E3 global, E7}.
"""
from __future__ import annotations

import json
import os
import sys
from math import comb

import numpy as np
from scipy.optimize import linprog

HERE = os.path.dirname(os.path.abspath(__file__))


def classes(n, lam_plus):
    """Return dict (region, sigma, G) -> (count, fixed_k or None)."""
    c = {}
    c[("b0", 1, 0)] = (900 - 2 * n, None)
    c[("b0", 0, 0)] = (325, None)
    if n:
        c[("b0", 1, 1)] = (n, 12 - lam_plus)
        c[("b0", 1, -1)] = (n, 5)
    c[("W", 1, 0)] = (1650, None)
    c[("W", 0, 0)] = (650, None)
    c[("WWB", 1, 0)] = (5550, None)
    c[("WWB", 0, 0)] = (1950, None)
    c[("WBB", 1, 0)] = (5550 - n * (25 - lam_plus) - 18 * n, None)
    c[("WBB", 0, 0)] = (1950 - n * lam_plus - 7 * n, None)
    if n:
        c[("WBB", 1, 1)] = (n * (25 - lam_plus), None)
        c[("WBB", 0, 1)] = (n * lam_plus, None)
        c[("WBB", 1, -1)] = (18 * n, 5)
        c[("WBB", 0, -1)] = (7 * n, 5)
    c[("B", 1, 0)] = (1650 - n * (9 + lam_plus) - 14 * n, None)
    c[("B", 0, 0)] = (650 - n * (12 - lam_plus) - 7 * n, None)
    if n:
        c[("B", 1, 1)] = (n * (9 + lam_plus), None)
        c[("B", 0, 1)] = (n * (12 - lam_plus), None)
        c[("B", 1, -1)] = (14 * n, None)
        c[("B", 0, -1)] = (7 * n, None)
    for key, (cnt, _) in c.items():
        if cnt < 0:
            raise ValueError(f"negative class size {key}: {cnt}")
    return c


def build(n, lam_plus, use):
    cl = classes(n, lam_plus)
    var = []  # (region, sigma, G, k)
    for (r, s, G), (cnt, fk) in cl.items():
        if cnt == 0:
            continue
        L = 12 - s + G
        kmin = 4 if r == "B" else 5
        kmax = L - 1 if r == "W" else L      # a triple inside W = N^-(b0) dominates b0, so l >= 1
        ks = [fk] if fk is not None else list(range(kmin, kmax + 1))
        for k in ks:
            var.append((r, s, G, k))
    idx = {v: i for i, v in enumerate(var)}
    nv = len(var)
    Aeq, beq, names = [], [], []

    def row(f, rhs, name):
        a = np.zeros(nv)
        for i, (r, s, G, k) in enumerate(var):
            a[i] = f(r, s, G, k)
        Aeq.append(a)
        beq.append(rhs)
        names.append(name)

    def uval(s, G, k):
        return k - (12 - s + G) / 2.0

    G2 = 2 * n
    Lam = n * (lam_plus - 5)
    # E1
    for (r, s, G), (cnt, fk) in cl.items():
        if cnt:
            row(lambda r_, s_, G_, k_, R=r, S=s, GG=G: 1.0 if (r_, s_, G_) == (R, S, GG) else 0.0, cnt, f"E1 {r},{s},{G}")
    # E2
    Ksum = {"b0": 6900, "W": 12650, "B": 13300, "WWB": 43200, "WBB": 41250}
    for reg, val in Ksum.items():
        if reg == "B" or use.get("E2all"):
            row(lambda r_, s_, G_, k_, R=reg: k_ if r_ == R else 0.0, val, f"E2 {reg}")
    # E3 (and the global identity sum G u = 0, which Lemma C' uses through sum L u = 0)
    row(lambda r_, s_, G_, k_: G_ * uval(s_, G_, k_), 0.0, "E3 global sum G u = 0")
    for s in (0, 1):
        row(lambda r_, s_, G_, k_, S=s: uval(s_, G_, k_) if s_ == S else 0.0, 0.0, f"E3 global sigma={s}")
        if use.get("E3b0"):
            row(lambda r_, s_, G_, k_, S=s: uval(s_, G_, k_) if (s_ == S and r_ == "b0") else 0.0, 0.0, f"E3 b0 sigma={s}")
    # E4
    if use.get("E4") and n:
        row(lambda r_, s_, G_, k_: G_ * uval(s_, G_, k_) if r_ == "b0" else 0.0, (G2 - 2 * Lam) / 2.0, "E4 b0")
        row(lambda r_, s_, G_, k_: G_ * uval(s_, G_, k_) if r_ == "WBB" else 0.0, Lam / 2.0, "E4 WBB")
        row(lambda r_, s_, G_, k_: G_ * uval(s_, G_, k_) if r_ == "B" else 0.0, -G2 / 2.0 + Lam / 2.0, "E4 B")
    # E5
    if use.get("E5") and n:
        row(lambda r_, s_, G_, k_: k_ if (r_ == "WBB" and G_ == 1) else 0.0, n * (144 + lam_plus), "E5 WBB G=+1")
        row(lambda r_, s_, G_, k_: k_ if (r_ == "WBB" and G_ == -1) else 0.0, 125 * n, "E5 WBB G=-1")
    # E7
    row(lambda r_, s_, G_, k_: (lambda u, L: u ** 3 + (3 * (L / 2 - 1) ** 2 - 1) * u)(uval(s_, G_, k_), 12 - s_ + G_),
        0.0, "E7 cubic")
    # E8
    if use.get("E8"):
        row(lambda r_, s_, G_, k_: uval(s_, G_, k_) ** 2 if r_ == "b0" else 0.0, 975 + G2 / 4.0, "E8 b0 u^2")
    # E9
    if use.get("E9"):
        row(lambda r_, s_, G_, k_: (comb(k_, 3) if r_ == "b0" else 0.0)
            - (comb(12 - s_ + G_ - k_ - 1, 2) if (r_ == "W" and 12 - s_ + G_ - k_ >= 1) else 0.0), 0.0, "E9 k3 vs W")
        row(lambda r_, s_, G_, k_: (comb(12 - s_ + G_ - k_, 3) if r_ == "b0" else 0.0)
            - (comb(k_ - 1, 2) if r_ == "B" else 0.0), 0.0, "E9 l3 vs B")
    obj = np.array([-(uval(s, G, k) ** 2) for (r, s, G, k) in var])
    return var, np.array(Aeq), np.array(beq), names, obj


def solve(n, lam_plus, use, duals=False):
    var, Aeq, beq, names, obj = build(n, lam_plus, use)
    # drop rows that are identically zero (e.g. G u rows when n = 0)
    keep = [i for i in range(len(beq)) if np.any(Aeq[i] != 0) or beq[i] != 0]
    Aeq, beq, names = Aeq[keep], beq[keep], [names[i] for i in keep]
    res = linprog(obj, A_eq=Aeq, b_eq=beq, bounds=[(0, None)] * len(var), method="highs")
    target = 16575 - (2 * n) / 4.0
    if res.status == 2:
        return {"n": n, "lam_plus": lam_plus, "status": "infeasible even without the u^2 equation",
                "target_sum_u2": target, "excluded": True}
    if res.status != 0:
        return {"n": n, "lam_plus": lam_plus, "status": res.message}
    mx = -res.fun
    out = {"n": n, "lam_plus": lam_plus, "max_sum_u2": round(mx, 4), "target_sum_u2": target,
           "margin": round(target - mx, 4), "excluded": bool(mx < target - 1e-6)}
    if duals:
        out["duals"] = {nm: round(float(y), 6) for nm, y in zip(names, res.eqlin.marginals) if abs(y) > 1e-9}
    return out


FIXED_ROWS = ["E2 B", "E3 global sigma=0", "E3 global sigma=1", "E3 b0 sigma=0", "E3 b0 sigma=1", "E7 cubic",
              "E8 b0 u^2", "E9 l3 vs B", "E9 k3 vs W", "E2 b0", "E2 W", "E2 WWB", "E2 WBB"]


def fixed_multiplier_bound(n, lam_plus, ybar):
    """Best dual bound when the multipliers of the structural rows are frozen at ybar (their n = 0 values) and
    only the class rows (E1), the G u rows (E3 global G u, E4) and the WBB pair rows (E5) are re-optimised.
    This is the bound a hand proof that reuses the Gamma2 = 0 certificate could reach."""
    use = {"E2all": True, "E3b0": True, "E8": True, "E4": True, "E5": True, "E9": True}
    var, Aeq, beq, names, obj = build(n, lam_plus, use)
    fixed = [i for i, nm in enumerate(names) if nm in FIXED_ROWS]
    free = [i for i in range(len(names)) if i not in fixed]
    ys = np.array([ybar.get(names[i], 0.0) for i in fixed])
    c2 = obj - Aeq[fixed].T @ ys
    keep = [i for i in free if np.any(Aeq[i] != 0) or beq[i] != 0]
    res = linprog(c2, A_eq=Aeq[keep], b_eq=beq[keep], bounds=[(0, None)] * len(var), method="highs")
    target = 16575 - (2 * n) / 4.0
    if res.status != 0:
        return {"n": n, "lam_plus": lam_plus, "status": res.message}
    bound = -(res.fun + beq[fixed] @ ys)
    return {"n": n, "lam_plus": lam_plus, "bound": round(bound, 3), "target": target,
            "excluded": bool(bound < target - 1e-6)}


def main():
    out = {}
    sets = {
        "LemmaC' (B-sum, global sigma-sums, sum Gu = 0, cubic)": {},
        "+ all region k-sums": {"E2all": True},
        "+ region b0 sigma-sums and u^2": {"E2all": True, "E3b0": True, "E8": True},
        "+ G u region sums and WBB pair sums": {"E2all": True, "E3b0": True, "E8": True, "E4": True, "E5": True},
        "LemmaC' + local cubic identities at b0 only": {"E9": True},
        "LemmaC' + region k-sums + local cubic at b0": {"E2all": True, "E9": True},
        "all": {"E2all": True, "E3b0": True, "E8": True, "E4": True, "E5": True, "E9": True},
    }
    print("DRT twin (n = 0): maximum of sum u^2 under each constraint set; target 16575")
    out["n0"] = {}
    for name, use in sets.items():
        r = solve(0, 5, use, duals=True)
        out["n0"][name] = r
        print(f"  {name}: max={r.get('max_sum_u2')}, margin={r.get('margin')}, excluded={r.get('excluded')}")
        print(f"      duals: {r.get('duals')}")
    print("Model configurations: first n (Gamma2 = 2n) where the identities stop excluding")
    out["scan"] = {}
    for name in [list(sets)[0], "LemmaC' + local cubic identities at b0 only", "all"]:
        use = sets[name]
        out["scan"][name] = {}
        for lam_plus in (0, 3, 5, 7):
            rows = []
            first_ok = None
            for n in range(0, 61, 1):
                try:
                    r = solve(n, lam_plus, use)
                except ValueError as e:
                    rows.append({"n": n, "status": str(e)})
                    break
                rows.append(r)
                if first_ok is None and r.get("excluded") is False:
                    first_ok = n
            out["scan"][name][lam_plus] = {"first_n_not_excluded": first_ok, "rows": rows}
            last = rows[-1].get("n") if rows else None
            print(f"  [{name}] lam_plus={lam_plus}: first n not excluded = {first_ok} (scan stopped at n = {last})")
    # frozen Gamma2 = 0 multipliers
    ybar = out["n0"]["all"]["duals"]
    print("Frozen Gamma2 = 0 multipliers (structural rows); first n not excluded:")
    out["frozen"] = {}
    for lam_plus in (0, 3, 5, 7):
        rows = []
        first_ok = None
        for n in range(0, 61):
            try:
                r = fixed_multiplier_bound(n, lam_plus, ybar)
            except ValueError as e:
                rows.append({"n": n, "status": str(e)})
                break
            rows.append(r)
            if first_ok is None and r.get("excluded") is False:
                first_ok = n
        out["frozen"][lam_plus] = {"first_n_not_excluded": first_ok, "rows": rows}
        print(f"  lam_plus={lam_plus}: first n not excluded = {first_ok}; rows n=0,4,8..: "
              + ", ".join(f"{r['n']}:{r.get('bound', r.get('status'))}" for r in rows[::4]))
    with open(os.path.join(HERE, "n52_twin_lp.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
