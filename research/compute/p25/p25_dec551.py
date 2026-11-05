"""[experiment] 551-class decomposition of the (P25) cubes with alpha = (6).
In such a cube q = 13 is a sink of T[R] and T[R \\ {q}] (vertices 14..24) is a 5-regular tournament on 11 vertices with S_2,
i.e. one of the 551 classes in reg11_S2_canon.txt.  For a given beta the cube formula (with the R-side Hamiltonian-path
symmetry breaking removed) is built once, and each class is solved incrementally under the 66 assumptions that fix T[R].
usage: python3 p25_dec551.py beta_string solver outfile [first last]"""
import sys, json, time, itertools
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import p25_cube
from p25_cube import cubes, build, verify, OPTS
from gen_regular import from_canon
from pysat.solvers import Solver
n, c = 25, 5
beta_s, solver, outfile = sys.argv[1], sys.argv[2], sys.argv[3]
classes = [l.strip() for l in open(__file__.rsplit('/', 1)[0] + '/reg11_S2_canon.txt')]
first, last = (int(sys.argv[4]), int(sys.argv[5])) if len(sys.argv) > 5 else (0, len(classes))
idx = [i for i, (a, b, m) in enumerate(cubes(n, c)) if ''.join(map(str, a)) == '600000000000' and ''.join(map(str, b)) == beta_s][0]
alpha, beta, m = cubes(n, c)[idx]
OPTS['nohp_R'] = True
t0 = time.time(); cnf, pool, x = build(n, c, alpha, beta, m, with_s3=True); tb = time.time() - t0
def arc(a, b): return x(a, b) if a < b else -x(b, a)
q, Rq = 13, list(range(14, 25))
with Solver(name=solver, bootstrap_with=cnf.clauses) as S, open(outfile, 'a') as f:
    for ci in range(first, min(last, len(classes))):
        T = from_canon(11, tuple(int(ch) for ch in classes[ci]))
        assert all(len(o) == 5 for o in T), 'class decoding is not 5-regular'
        assum = [arc(r, q) for r in Rq]
        for i, j in itertools.combinations(range(11), 2):
            assum.append(arc(Rq[i], Rq[j]) if j in T[i] else arc(Rq[j], Rq[i]))
        t1 = time.time(); res = S.solve(assumptions=assum); dt = round(time.time() - t1, 2)
        rec = {"cube": idx, "alpha": "600000000000", "beta": beta_s, "class": ci, "solver": solver, "time": dt,
               "result": "SAT" if res else "UNSAT", "build": round(tb, 1)}
        if res:
            mdl = set(l for l in S.get_model() if l > 0)
            Out = [set(bb for bb in range(n) if bb != aa and ((x(aa, bb) in mdl) if aa < bb else (x(bb, aa) not in mdl))) for aa in range(n)]
            ok, msg = verify(n, c, Out, True); rec.update(verified=ok, check=msg, out=[sorted(o) for o in Out])
        f.write(json.dumps(rec) + '\n'); f.flush()
