"""R8-G validation: checker on Paley 47/59/67, both checkers agree, and the
all-arcs delta matrix of the tabu engine equals brute-force recomputation."""
import json
import sys
import time
import numpy as np

sys.path.insert(0, __file__.rsplit("\\", 1)[0])
import r8g_core as C
import r8g_check2 as C2

out = {}
for p in (47, 59, 67):
    A = C.paley(p)
    t = time.time()
    pr = C.profile(A)
    pr["seconds_checker1"] = round(time.time() - t, 3)
    t = time.time()
    pr2 = C2.check(C2.paley_rows(p))
    pr["seconds_checker2"] = round(time.time() - t, 3)
    pr["checker2"] = {k: pr2[k] for k in ("undominated_4sets", "min_pair_dom", "min_triple_dom", "S4")}
    assert pr2["undominated_4sets"] == pr["undominated_4sets"]
    assert pr2["min_pair_dom"] == pr["min_pair_dom"] and pr2["min_triple_dom"] == pr["min_triple_dom"]
    out[f"QR_{p}"] = pr
    print(p, json.dumps(pr))

assert out["QR_67"]["S4"] and not out["QR_47"]["S4"] and not out["QR_59"]["S4"]

# delta-matrix test on random near-regular tournaments and on QR_67 minus vertices
rng = np.random.default_rng(1)
tests = []
for N, lam in ((20, 1.0), (24, 0.5), (66, 1.0)):
    if N == 66:
        A = C.paley(67)[1:, 1:]
    else:
        U = np.triu(rng.random((N, N)) < 0.5, 1)
        A = U | np.triu(~U, 1).T
    assert C.is_tournament(A)
    T = C.Tabu(A, lam=lam, rng=rng)
    M = T.deltas()
    arcs = np.argwhere(T.A)
    pick = arcs[rng.choice(len(arcs), min(40, len(arcs)), replace=False)]
    worst = 0.0
    for u, v in pick:
        B = T.A.copy()
        B[u, v], B[v, u] = False, True
        T2 = C.Tabu(B, lam=lam)
        worst = max(worst, abs((T2.cost - T.cost) - M[u, v]))
    # incremental apply vs full recompute
    for u, v in pick[:10]:
        if T.A[u, v]:
            d = T.deltas()[u, v]
            c0 = T.cost
            T.apply(u, v)
            T.cost = c0 + d
            full = C.Tabu(T.A, lam=lam)
            worst = max(worst, abs(full.cost - T.cost),
                        float(np.abs(full.cnt4 - T.cnt4).max()),
                        float(np.abs(full.cnt3 - T.cnt3).max()),
                        float((full.D4 != T.D4).sum()), float((full.Dp != T.Dp).sum()))
    tests.append({"N": N, "lam": lam, "max_abs_error": worst})
    print("delta test", N, lam, worst)
    assert worst < 1e-9
out["delta_tests"] = tests
with open(__file__.rsplit("\\", 1)[0] + "\\r8g_validate.json", "w") as f:
    json.dump(out, f, indent=1)
