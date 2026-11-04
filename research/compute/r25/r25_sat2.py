"""[experiment] (R25) with stronger encoding. Vertex 0 beats exactly O = 1..12 and is beaten by R = 13..24.
Symmetry breaking: out-degree inside T[O] non-increasing along 1..12; in-degree inside T[R] non-increasing along 13..24
(relabelling inside O and inside R preserves the vertex-0 normalisation). Totalizer encodings.
usage: python3 r25_sat2.py [solver] [cmin] [n]"""
import sys, itertools, time
from pysat.formula import CNF, IDPool
from pysat.card import CardEnc, EncType, ITotalizer
from pysat.solvers import Solver
solver_name = sys.argv[1] if len(sys.argv) > 1 else 'cadical153'
cmin = int(sys.argv[2]) if len(sys.argv) > 2 else 5
n = int(sys.argv[3]) if len(sys.argv) > 3 else 25
m = (n - 1) // 2
pool = IDPool(); cnf = CNF()
def x(i, j): return pool.id(('x', i, j))
def arc(a, b): return x(a, b) if a < b else -x(b, a)
for i, j in itertools.combinations(range(n), 2): x(i, j)
def tot(lits, ub):
    """two-directional sequential counter: returns r with r[k] <-> (sum lits >= k+1), k = 0..ub-1"""
    prev = [None] * (ub + 1)          # prev[k] literal for 'sum of first i >= k'; None = constant
    TRUE, FALSE = 'T', 'F'
    prev = [TRUE] + [FALSE] * ub
    for i, l in enumerate(lits):
        cur = [TRUE]
        for k in range(1, ub + 1):
            a, b = prev[k], prev[k - 1]      # s_{i,k} <-> a or (b and l)
            if a == TRUE: cur.append(TRUE); continue
            if a == FALSE and b == FALSE: cur.append(FALSE); continue
            s = pool.id(('s', id(lits), i, k, len(cnf.clauses)))
            if a != FALSE: cnf.append([-a, s]); 
            if b == TRUE: cnf.append([-l, s])
            elif b != FALSE: cnf.append([-b, -l, s])
            # s -> a or b ; s -> a or l
            c1 = [-s] + ([a] if a != FALSE else []) + ([b] if b not in (FALSE,) and b != TRUE else ([] if b == FALSE else None or []))
            if b == TRUE: c1 = None
            if c1 is not None: cnf.append(c1)
            cnf.append([-s] + ([a] if a != FALSE else []) + [l])
            cur.append(s)
        prev = cur
    out = []
    for k in range(1, ub + 1):
        v = prev[k]
        if v == TRUE: v = pool.id(('const', 'T')); cnf.append([v])
        elif v == FALSE: v = pool.id(('const', 'F')); cnf.append([-v])
        out.append(v)
    return out
for a in range(n):
    r = tot([arc(a, b) for b in range(n) if b != a], m + 1)
    cnf.append([r[m - 1]]); cnf.append([-r[m]])   # out-degree exactly m
for a, b in itertools.combinations(range(n), 2):
    ys = []
    for w in range(n):
        if w in (a, b): continue
        y = pool.id(('y', w, a, b)); ys.append(y)
        cnf.append([-y, arc(w, a)]); cnf.append([-y, arc(w, b)]); cnf.append([y, -arc(w, a), -arc(w, b)])
    r = tot(ys, cmin); cnf.append([r[cmin - 1]])
O = list(range(1, m + 1)); R = list(range(m + 1, n))
for b in O: cnf.append([arc(0, b)])
for b in R: cnf.append([arc(b, 0)])
outO = [tot([arc(o, p) for p in O if p != o], m - 1) for o in O]
inR = [tot([arc(p, q) for p in R if p != q], m - 1) for q in R]
for seq in (outO, inR):
    for i in range(len(seq) - 1):
        for k in range(m - 1): cnf.append([-seq[i + 1][k], seq[i][k]])   # deg(i+1) >= k+1 -> deg(i) >= k+1
print("n", n, "cmin", cmin, "vars", pool.top, "clauses", len(cnf.clauses), flush=True)
t = time.time()
with Solver(name=solver_name, bootstrap_with=cnf.clauses) as s:
    res = s.solve(); print("result", res, "time %.1f s" % (time.time() - t), flush=True)
    if res:
        mdl = set(l for l in s.get_model() if l > 0)
        beat = lambda a, b: (x(a, b) in mdl) if a < b else (x(b, a) not in mdl)
        In = [set(w for w in range(n) if w != v and beat(w, v)) for v in range(n)]
        for a in range(n): print(a, sorted(b for b in range(n) if b != a and beat(a, b)))
        print("min codeg", min(len(In[a] & In[b]) for a, b in itertools.combinations(range(n), 2)))
