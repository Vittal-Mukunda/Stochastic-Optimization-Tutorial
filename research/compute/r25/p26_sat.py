"""[experiment] (P26): 26 vertices, every in-degree >= 12, every pair >= 5 common in-neighbours, every triple dominated (S_3).
This is the in-neighbourhood of an in-degree-26 vertex with no tight in-pair in an S_4 tournament on 52 vertices.
Symmetry breaking: in-degrees non-increasing along the vertex order. usage: python3 p26_sat.py [solver] [n] [dmin] [cmin]"""
import sys, itertools, time
from pysat.formula import CNF, IDPool
from pysat.card import CardEnc, EncType
from pysat.solvers import Solver
solver = sys.argv[1] if len(sys.argv) > 1 else 'cadical153'
n = int(sys.argv[2]) if len(sys.argv) > 2 else 26
dmin = int(sys.argv[3]) if len(sys.argv) > 3 else 12
cmin = int(sys.argv[4]) if len(sys.argv) > 4 else 5
pool = IDPool(); cnf = CNF()
def x(i, j): return pool.id(('x', i, j))
def arc(a, b): return x(a, b) if a < b else -x(b, a)
for i, j in itertools.combinations(range(n), 2): x(i, j)
def counter(lits, ub):   # two-directional sequential counter, r[k] <-> sum >= k+1
    T, F = 'T', 'F'; prev = [T] + [F] * ub
    for i, l in enumerate(lits):
        cur = [T]
        for k in range(1, ub + 1):
            a, b = prev[k], prev[k - 1]
            if a == T: cur.append(T); continue
            if a == F and b == F: cur.append(F); continue
            s = pool.id(('s', len(cnf.clauses), i, k))
            if a != F: cnf.append([-a, s])
            if b == T: cnf.append([-l, s])
            elif b != F: cnf.append([-b, -l, s])
            if b != T: cnf.append([-s] + ([a] if a != F else []) + ([b] if b != F else []))
            cnf.append([-s] + ([a] if a != F else []) + [l])
            cur.append(s)
        prev = cur
    out = []
    for k in range(1, ub + 1):
        v = prev[k]
        if v in ('T', 'F'):
            c = pool.id(('const', v)); cnf.append([c] if v == 'T' else [-c]); v = c
        out.append(v)
    return out
indeg = []
for a in range(n):
    r = counter([arc(b, a) for b in range(n) if b != a], n - 1); indeg.append(r)
    cnf.append([r[dmin - 1]])
for a in range(n - 1):
    for k in range(n - 1): cnf.append([-indeg[a + 1][k], indeg[a][k]])
for a, b in itertools.combinations(range(n), 2):
    ys = []
    for w in range(n):
        if w in (a, b): continue
        y = pool.id(('y', w, a, b)); ys.append(y)
        cnf.append([-y, arc(w, a)]); cnf.append([-y, arc(w, b)]); cnf.append([y, -arc(w, a), -arc(w, b)])
    cnf.extend(CardEnc.atleast(lits=ys, bound=cmin, vpool=pool, encoding=EncType.seqcounter).clauses)
for a, b, c in itertools.combinations(range(n), 3):
    zs = []
    for w in range(n):
        if w in (a, b, c): continue
        z = pool.id(('z', w, a, b, c)); zs.append(z)
        cnf.append([-z, pool.id(('y', w, a, b))]); cnf.append([-z, arc(w, c)])
    cnf.append(zs)
print("n", n, "dmin", dmin, "cmin", cmin, "vars", pool.top, "clauses", len(cnf.clauses), flush=True)
t = time.time()
with Solver(name=solver, bootstrap_with=cnf.clauses) as s:
    res = s.solve(); print("result", res, "time %.1f s" % (time.time() - t), flush=True)
    if res:
        mdl = set(l for l in s.get_model() if l > 0)
        beat = lambda a, b: (x(a, b) in mdl) if a < b else (x(b, a) not in mdl)
        In = [set(w for w in range(n) if w != v and beat(w, v)) for v in range(n)]
        print("indeg", [len(I) for I in In])
        print("min codeg", min(len(In[a] & In[b]) for a, b in itertools.combinations(range(n), 2)),
              "min k", min(len(In[a] & In[b] & In[c]) for a, b, c in itertools.combinations(range(n), 3)))
        for a in range(n): print(a, ':', ' '.join(str(b) for b in range(n) if b != a and beat(a, b)))
