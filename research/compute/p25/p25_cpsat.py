"""[experiment] CP-SAT model of one (P25)-type cube; same case split and constraints as p25_cube.py.
usage: python3 p25_cpsat.py n c index time_limit workers [nos3]   -> one JSON line"""
import sys, json, time, itertools
from ortools.sat.python import cp_model
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from p25_cube import cubes, verify

def main():
    n, c, idx = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    tl, workers = float(sys.argv[4]), int(sys.argv[5]); with_s3 = not (len(sys.argv) > 6 and sys.argv[6] == 'nos3')
    alpha, beta, m = cubes(n, c)[idx]; k = (n - 1) // 2
    M = cp_model.CpModel()
    X = {(i, j): M.NewBoolVar(f"x{i}_{j}") for i, j in itertools.combinations(range(n), 2)}
    def arc(a, b): return X[(a, b)] if a < b else X[(b, a)].Not()
    for a in range(n): M.Add(sum(arc(a, b) for b in range(n) if b != a) == k)
    O = list(range(1, k + 1)); R = list(range(k + 1, n))
    for b in O: M.Add(arc(0, b) == 1)
    for b in R: M.Add(arc(b, 0) == 1)
    for i, o in enumerate(O): M.Add(sum(arc(o, p) for p in O if p != o) == c + beta[i])
    for i, r in enumerate(R): M.Add(sum(arc(p, r) for p in R if p != r) == c + alpha[i])
    for vals, verts in ((beta, O), (alpha, R)):
        for i in range(k - 1):
            if vals[i] == vals[i + 1]: M.Add(arc(verts[i], verts[i + 1]) == 1)
    Y = {}
    for a, b in itertools.combinations(range(n), 2):
        ys = []
        for w in range(n):
            if w in (a, b): continue
            y = M.NewBoolVar(""); Y[(w, a, b)] = y; ys.append(y)
            M.AddBoolAnd([arc(w, a), arc(w, b)]).OnlyEnforceIf(y)
            M.AddBoolOr([arc(w, a).Not(), arc(w, b).Not()]).OnlyEnforceIf(y.Not())
        M.Add(sum(ys) >= c); M.Add(sum(ys) <= c + m)
    if with_s3:
        for a, b, d in itertools.combinations(range(n), 3):
            zs = []
            for w in range(n):
                if w in (a, b, d): continue
                z = M.NewBoolVar(""); zs.append(z)
                M.AddImplication(z, Y[(w, a, b)]); M.AddImplication(z, arc(w, d))
            M.AddBoolOr(zs)
    S = cp_model.CpSolver(); S.parameters.max_time_in_seconds = tl; S.parameters.num_workers = workers
    t0 = time.time(); st = S.Solve(M)
    rec = {"n": n, "c": c, "index": idx, "alpha": ''.join(map(str, alpha)), "beta": ''.join(map(str, beta)), "m": m,
           "s3": with_s3, "solver": "cpsat", "workers": workers, "time": round(time.time() - t0, 1), "status": S.StatusName(st)}
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        Out = [set(b for b in range(n) if b != a and S.Value(arc(a, b))) for a in range(n)]
        ok, msg = verify(n, c, Out, with_s3); rec.update(result="SAT", verified=ok, check=msg, out=[sorted(o) for o in Out])
    elif st == cp_model.INFEASIBLE: rec["result"] = "UNSAT"
    else: rec["result"] = "TIMEOUT"
    print(json.dumps(rec), flush=True)

if __name__ == '__main__': main()
