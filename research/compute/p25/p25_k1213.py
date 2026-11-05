"""[experiment] (P25) branch where the codegree-5 graph is triangle-free, hence K_{12,13} (minimum degree >= 12 and
Andrasfai-Erdos-Sos).  A = 0..11 (perfect matching {0,1},{2,3},...,{10,11} of codegree 7), B = 12..24.
Exact codegrees: 5 on A x B, 6 inside B, 6 inside A except 7 on the matching.  Regular (out-degree 12), optional S_3.
usage: python3 p25_k1213.py solver [nos3]"""
import sys, itertools, time, json
from pysat.formula import CNF, IDPool
from pysat.card import CardEnc, EncType
from pysat.solvers import Solver
n = 25; A = list(range(12)); B = list(range(12, 25)); with_s3 = not (len(sys.argv) > 2 and sys.argv[2] == 'nos3')
pool = IDPool(); cnf = CNF()
def x(i, j): return pool.id(('x', i, j))
def arc(a, b): return x(a, b) if a < b else -x(b, a)
for i, j in itertools.combinations(range(n), 2): x(i, j)
def eq(lits, k): cnf.extend(CardEnc.equals(lits=lits, bound=k, vpool=pool, encoding=EncType.seqcounter).clauses)
for a in range(n): eq([arc(a, b) for b in range(n) if b != a], 12)
def target(a, b):
    if (a in A) != (b in A): return 5
    if a in B: return 6
    return 7 if a // 2 == b // 2 else 6
for a, b in itertools.combinations(range(n), 2):
    ys = []
    for w in range(n):
        if w in (a, b): continue
        y = pool.id(('y', w, a, b)); ys.append(y)
        cnf.append([-y, arc(w, a)]); cnf.append([-y, arc(w, b)]); cnf.append([y, -arc(w, a), -arc(w, b)])
    eq(ys, target(a, b))
if with_s3:
    for a, b, d in itertools.combinations(range(n), 3):
        zs = []
        for w in range(n):
            if w in (a, b, d): continue
            z = pool.id(('z', w, a, b, d)); zs.append(z)
            cnf.append([-z, pool.id(('y', w, a, b))]); cnf.append([-z, arc(w, d)])
        cnf.append(zs)
cnf.append([arc(0, 1)])                     # the matching pair {0,1}: WLOG 0 -> 1 (swap labels inside the pair)
t = time.time()
with Solver(name=sys.argv[1], bootstrap_with=cnf.clauses) as S:
    r = S.solve(); print(json.dumps({"branch": "G5=K12,13", "s3": with_s3, "solver": sys.argv[1], "result": "SAT" if r else "UNSAT",
                                     "time": round(time.time() - t, 1), "vars": pool.top, "clauses": len(cnf.clauses)}), flush=True)
    if r:
        mdl = set(l for l in S.get_model() if l > 0)
        Out = [sorted(b for b in range(n) if b != a and ((x(a, b) in mdl) if a < b else (x(b, a) not in mdl))) for a in range(n)]
        print(json.dumps(Out))
