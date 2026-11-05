"""[experiment] Cube-and-conquer for (P25) and its analogues.

Question Q(n, c): is there a regular tournament on n = 2k+1 vertices (out-degree k) in which every pair of vertices has
>= c common in-neighbours (codegree) and every triple has a common dominator (property S_3)?  (P25) is Q(25, 5).

Case split (exhaustive).  Let D_max = c + m be the largest codegree and let vertex 0 be an endpoint of a pair attaining it.
O = N+(0) = {1..k}, R = N-(0) = {k+1..2k}.  For r in R, D(0,r) = in-degree of r inside T[R] = c + alpha_r; for o in O,
D(0,o) = out-degree of o inside T[O] = c + beta_o.  Both alpha and beta are partitions of s = C(k,2) - k*c (padded to k),
the largest part of alpha u beta is m, and every codegree in the tournament is <= c + m.  Relabel R and O so alpha and beta
are non-increasing; inside each block of equal values order the vertices along a Hamiltonian path of the block (every
tournament has one), i.e. arc i -> i+1 for consecutive vertices of a block.  Each (alpha, beta) is one cube.

usage:
  python3 p25_cube.py list  n c                      # print the cubes (index alpha beta m)
  python3 p25_cube.py solve n c index solver [nos3]  # build and solve one cube; prints one JSON line
  python3 p25_cube.py dimacs n c index file          # write the cube CNF in DIMACS
"""
import sys, json, time, itertools
from pysat.formula import CNF, IDPool
from pysat.card import CardEnc, EncType

def partitions(s, maxpart=None, maxlen=None):
    if maxpart is None: maxpart = s
    if s == 0: yield (); return
    if maxlen == 0: return
    for p in range(min(s, maxpart), 0, -1):
        for rest in partitions(s - p, p, None if maxlen is None else maxlen - 1):
            yield (p,) + rest

def cubes(n, c):
    k = (n - 1) // 2; s = k * (k - 1) // 2 - k * c
    assert s >= 0, "no regular tournament with this codegree floor"
    P = [tuple(list(p) + [0] * (k - len(p))) for p in partitions(s, maxlen=k)]
    out = []
    for a in P:
        for b in P:
            out.append((a, b, max(a + b) if s > 0 else 0))
    return out

OPTS = {'enc': 'seqcounter', 'outcodeg': False, 'nohp': False}

def build(n, c, alpha, beta, m, with_s3=True):
    k = (n - 1) // 2
    pool = IDPool(); cnf = CNF()
    def x(i, j): return pool.id(('x', i, j))
    def arc(a, b): return x(a, b) if a < b else -x(b, a)
    for i, j in itertools.combinations(range(n), 2): x(i, j)
    O = list(range(1, k + 1)); R = list(range(k + 1, n))
    def card(lits, lo, hi):
        enc = getattr(EncType, OPTS['enc'])
        if lo > 0: cnf.extend(CardEnc.atleast(lits=lits, bound=lo, vpool=pool, encoding=enc).clauses)
        if hi < len(lits): cnf.extend(CardEnc.atmost(lits=lits, bound=hi, vpool=pool, encoding=enc).clauses)
    for a in range(n):                                   # regular: out-degree exactly k
        card([arc(a, b) for b in range(n) if b != a], k, k)
    for b in O: cnf.append([arc(0, b)])                   # vertex 0 beats O, is beaten by R
    for b in R: cnf.append([arc(b, 0)])
    for i, o in enumerate(O):                             # out-degree of o inside T[O] = c + beta_i
        card([arc(o, p) for p in O if p != o], c + beta[i], c + beta[i])
    for i, r in enumerate(R):                             # in-degree of r inside T[R] = c + alpha_i
        card([arc(p, r) for p in R if p != r], c + alpha[i], c + alpha[i])
    for blockvals, verts in ((beta, O), (alpha, R)):      # Hamiltonian path inside each block of equal values
        if OPTS['nohp']: break
        for i in range(k - 1):
            if blockvals[i] == blockvals[i + 1]: cnf.append([arc(verts[i], verts[i + 1])])
    cap = c + m
    for a, b in itertools.combinations(range(n), 2):      # c <= codegree <= c + m
        ys = []
        for w in range(n):
            if w in (a, b): continue
            y = pool.id(('y', w, a, b)); ys.append(y)
            cnf.append([-y, arc(w, a)]); cnf.append([-y, arc(w, b)]); cnf.append([y, -arc(w, a), -arc(w, b)])
        card(ys, c, min(cap, len(ys)))
        if OPTS['outcodeg']:                              # redundant: common out-neighbours (= codegree when regular)
            ws = []
            for w in range(n):
                if w in (a, b): continue
                v = pool.id(('v', w, a, b)); ws.append(v)
                cnf.append([-v, arc(a, w)]); cnf.append([-v, arc(b, w)]); cnf.append([v, -arc(a, w), -arc(b, w)])
            card(ws, c, min(cap, len(ws)))
    if with_s3:                                           # every triple dominated
        for a, b, d in itertools.combinations(range(n), 3):
            zs = []
            for w in range(n):
                if w in (a, b, d): continue
                z = pool.id(('z', w, a, b, d)); zs.append(z)
                cnf.append([-z, pool.id(('y', w, a, b))]); cnf.append([-z, arc(w, d)])
            cnf.append(zs)
    return cnf, pool, x

def verify(n, c, Out, with_s3=True):
    """independent check of a decoded tournament: returns (ok, message)"""
    k = (n - 1) // 2
    for a in range(n):
        if a in Out[a]: return False, "loop"
        for b in range(a + 1, n):
            if (b in Out[a]) == (a in Out[b]): return False, "not a tournament at %d,%d" % (a, b)
    if any(len(Out[a]) != k for a in range(n)): return False, "not regular"
    In = [set(w for w in range(n) if v in Out[w]) for v in range(n)]
    mc = min(len(In[a] & In[b]) for a, b in itertools.combinations(range(n), 2))
    if mc < c: return False, "codegree %d < %d" % (mc, c)
    if with_s3:
        for a, b, d in itertools.combinations(range(n), 3):
            if not (In[a] & In[b] & In[d]): return False, "undominated triple %s" % ((a, b, d),)
    return True, "min codegree %d" % mc

def main():
    cmd = sys.argv[1]; n = int(sys.argv[2]); c = int(sys.argv[3])
    C = cubes(n, c)
    if cmd == 'list':
        for i, (a, b, m) in enumerate(C): print(i, ''.join(map(str, a)), ''.join(map(str, b)), m)
        return
    idx = int(sys.argv[4]); a, b, m = C[idx]
    if cmd == 'dimacs':
        cnf, pool, x = build(n, c, a, b, m); cnf.to_file(sys.argv[5]); return
    solver = sys.argv[5]; flags = sys.argv[6:]; with_s3 = 'nos3' not in flags
    for f in flags:
        if f.startswith('enc='): OPTS['enc'] = f[4:]
        if f == 'outcodeg': OPTS['outcodeg'] = True
        if f == 'nohp': OPTS['nohp'] = True
    from pysat.solvers import Solver
    t0 = time.time(); cnf, pool, x = build(n, c, a, b, m, with_s3)
    rec = {"n": n, "c": c, "index": idx, "alpha": ''.join(map(str, a)), "beta": ''.join(map(str, b)), "m": m,
           "s3": with_s3, "solver": solver, "opts": dict(OPTS), "vars": pool.top, "clauses": len(cnf.clauses)}
    with Solver(name=solver, bootstrap_with=cnf.clauses) as S:
        res = S.solve(); rec["time"] = round(time.time() - t0, 1)
        if res:
            mdl = set(l for l in S.get_model() if l > 0)
            Out = [set(bb for bb in range(n) if bb != aa and ((x(aa, bb) in mdl) if aa < bb else (x(bb, aa) not in mdl)))
                   for aa in range(n)]
            ok, msg = verify(n, c, Out, with_s3)
            rec.update(result="SAT", verified=ok, check=msg, out=[sorted(o) for o in Out])
        else:
            rec.update(result="UNSAT")
    print(json.dumps(rec), flush=True)

if __name__ == '__main__':
    main()
