"""[experiment] Same decomposition as p25_dec551.py but one fresh solver per class with T[R] fixed by unit clauses
(for solvers without incremental assumptions, e.g. Kissat).  usage: python3 p25_dec551_units.py beta_string solver class_index"""
import sys, json, time, itertools
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from p25_cube import cubes, build, verify, OPTS
from gen_regular import from_canon
from pysat.solvers import Solver
n, c = 25, 5
beta_s, solver, ci = sys.argv[1], sys.argv[2], int(sys.argv[3])
classes = [l.strip() for l in open(__file__.rsplit('/', 1)[0] + '/reg11_S2_canon.txt')]
idx = [i for i, (a, b, m) in enumerate(cubes(n, c)) if ''.join(map(str, a)) == '600000000000' and ''.join(map(str, b)) == beta_s][0]
alpha, beta, m = cubes(n, c)[idx]; OPTS['nohp_R'] = True; OPTS['lexO'] = len(sys.argv) > 4 and sys.argv[4] == 'lexO'
cnf, pool, x = build(n, c, alpha, beta, m, with_s3=True)
def arc(a, b): return x(a, b) if a < b else -x(b, a)
q, Rq = 13, list(range(14, 25))
T = from_canon(11, tuple(int(ch) for ch in classes[ci])); assert all(len(o) == 5 for o in T)
for r in Rq: cnf.append([arc(r, q)])
for i, j in itertools.combinations(range(11), 2): cnf.append([arc(Rq[i], Rq[j]) if j in T[i] else arc(Rq[j], Rq[i])])
t1 = time.time()
with Solver(name=solver, bootstrap_with=cnf.clauses) as S:
    res = S.solve(); rec = {"cube": idx, "alpha": "600000000000", "beta": beta_s, "class": ci, "solver": solver,
                            "time": round(time.time() - t1, 2), "result": "SAT" if res else "UNSAT"}
    if res:
        mdl = set(l for l in S.get_model() if l > 0)
        Out = [set(bb for bb in range(n) if bb != aa and ((x(aa, bb) in mdl) if aa < bb else (x(bb, aa) not in mdl))) for aa in range(n)]
        ok, msg = verify(n, c, Out, True); rec.update(verified=ok, check=msg, out=[sorted(o) for o in Out])
print(json.dumps(rec), flush=True)
