"""[experiment] (R25): is there a 12-regular tournament on 25 vertices in which every pair has >= 5 common in-neighbours?
SAT encoding with pysat. Symmetry breaking: vertex 0 beats exactly 1..12.
usage: python3 r25_sat.py [solver] [extra]   extra = 'sb2' adds sorted in-degree symmetry breaking inside N-(0)"""
import sys, itertools, time
from pysat.formula import CNF, IDPool
from pysat.card import CardEnc, EncType
from pysat.solvers import Solver
n, out_deg, cmin = 25, 12, 5
pool = IDPool()
def x(i, j): return pool.id(('x', i, j))            # i<j : i -> j
def arc(a, b): return x(a, b) if a < b else -x(b, a)  # literal "a -> b"
cnf = CNF()
for i, j in itertools.combinations(range(n), 2): x(i, j)
for a in range(n):
    lits = [arc(a, b) for b in range(n) if b != a]
    cnf.extend(CardEnc.equals(lits=lits, bound=out_deg, vpool=pool, encoding=EncType.seqcounter).clauses)
for a, b in itertools.combinations(range(n), 2):
    ys = []
    for w in range(n):
        if w in (a, b): continue
        y = pool.id(('y', w, a, b)); ys.append(y)
        cnf.append([-y, arc(w, a)]); cnf.append([-y, arc(w, b)])
    cnf.extend(CardEnc.atleast(lits=ys, bound=cmin, vpool=pool, encoding=EncType.seqcounter).clauses)
for b in range(1, n):
    cnf.append([arc(0, b)] if b <= out_deg else [arc(b, 0)])
print("vars", pool.top, "clauses", len(cnf.clauses), flush=True)
solver_name = sys.argv[1] if len(sys.argv) > 1 else 'cadical153'
t = time.time()
with Solver(name=solver_name, bootstrap_with=cnf.clauses) as s:
    res = s.solve()
    print("result", res, "time %.1f s" % (time.time() - t), flush=True)
    if res:
        m = set(l for l in s.get_model() if l > 0)
        A = [[1 if (b != a and (arc(a, b) in m or (arc(a, b) < 0 and -arc(a, b) not in m))) else 0 for b in range(n)] for a in range(n)]
        for a in range(n): print(a, [b for b in range(n) if A[a][b]])
        In = [set(w for w in range(n) if A[w][v]) for v in range(n)]
        print("min codeg", min(len(In[a] & In[b]) for a, b in itertools.combinations(range(n), 2)),
              "outdeg", sorted(set(sum(r) for r in A)))
