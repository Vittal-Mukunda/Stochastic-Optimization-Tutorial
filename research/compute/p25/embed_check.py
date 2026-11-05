"""[check] relabel a known tournament into the normal form of its cube and test the cube CNF under those 300 arc values."""
import sys, itertools, json
from pysat.solvers import Solver
sys.path.insert(0, '.')
from p25_cube import cubes, build
def ham_path(verts, Out):
    # insertion construction of a Hamiltonian path in a tournament (Redei)
    path = []
    for v in verts:
        for i in range(len(path) + 1):
            if (i == 0 or v in Out[path[i - 1]]) and (i == len(path) or path[i] in Out[v]):
                path.insert(i, v); break
    assert all(path[i + 1] in Out[path[i]] for i in range(len(path) - 1))
    return path
def normal_form(Out, v0, c):
    n = len(Out); In = [set(w for w in range(n) if v in Out[w]) for v in range(n)]
    D = lambda a, b: len(In[a] & In[b])
    O = sorted(Out[v0], key=lambda o: -D(v0, o)); R = sorted(In[v0], key=lambda r: -D(v0, r))
    def blocks(L):
        res = []; i = 0
        while i < len(L):
            j = i
            while j < len(L) and D(v0, L[j]) == D(v0, L[i]): j += 1
            res += ham_path(L[i:j], Out); i = j
        return res
    order = [v0] + blocks(O) + blocks(R)
    pos = {v: i for i, v in enumerate(order)}
    NewOut = [set() for _ in range(n)]
    for a in range(n):
        for b in Out[a]: NewOut[pos[a]].add(pos[b])
    alpha = tuple(D(v0, r) - c for r in blocks(R)); beta = tuple(D(v0, o) - c for o in blocks(O))
    return NewOut, alpha, beta
f, v0, c, s3 = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4] == 's3'
Out = [set(map(int, l.split(':')[1].split())) for l in open(f)]
n = len(Out); NewOut, alpha, beta = normal_form(Out, v0, c)
C = cubes(n, c); idx = [i for i, (a, b, m) in enumerate(C) if a == alpha and b == beta][0]
a, b, m = C[idx]
print("cube", idx, ''.join(map(str, a)), ''.join(map(str, b)), "m", m)
cnf, pool, x = build(n, c, a, b, m, with_s3=s3)
assum = [x(i, j) if j in NewOut[i] else -x(i, j) for i, j in itertools.combinations(range(n), 2)]
with Solver(name='kissat404' if False else 'cadical153', bootstrap_with=cnf.clauses) as S:
    print("CNF satisfiable with the example's arcs as assumptions:", S.solve(assumptions=assum))
