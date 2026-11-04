"""Unit tests of the modelling identities behind the N = 51 local model, on random planted configurations.

A random tournament on 51 vertices is planted with a -> b, R = {2..12} (T[R] = a random class), every r in R beating
a and b, and no outside vertex beating both a and b (so D({a,b}) = R exactly).  All other arcs are random.
For each such tournament the row semantics of check_n51.System (the checker) are evaluated on the actual outside
vertices and compared with brute-force quantities of the tournament:
  C1:  #O = 38
  C3:  cR(U) + #{y: Q_y n U = 0}               = |D(U)|          (U subset R, |U| = 2,3,4)
  C4:  cR(U) + #{y of type p: Q_y n U = 0}     = |D(U + p)|      (p = a, b; |U| = 1,2,3)
  C5:  deg_O(r) + j_r = 18 with j_r := d^-(r) - 25
  M :  n0 = d^-(a) - 11,  n1 = d^-(b) - 12;  |Q_y| = |D({a,b,y})|
  identities used in Lemma P:   sum_{U ni r, |U|=3} (|D(U)| - 5) = 5 + 10 j_r - sum_{y: r not in Q_y} lambda(|Q_y|)
                                sum_y (|Q_y| - 5) = 8 - J ;   sum_{|U|=3} |D(U)| = 110 + sum_y C(11 - |Q_y|, 3)
Also checks that the producer (lmodel.Model) and the checker build identical rows and boxes on several classes,
in every mode, with and without the auxiliary variables.
"""
import random, itertools, sys
from math import comb
import check_n51 as C

lines = open(sys.argv[1] if len(sys.argv) > 1 else 'reg11_S2.txt').read().split()
random.seed(20261018)
N = 51
checks = fails = 0


def ok(cond):
    global checks, fails
    checks += 1
    if not cond:
        fails += 1


class AllSets(C.System):
    """checker semantics, but with the variable universe = all subsets S of R (so any planted Q_y has a variable)."""
    def __init__(self, beats, mode):
        self.beats = beats
        self.mode = mode
        self.adm = [frozenset(S) for k in range(12) for S in itertools.combinations(C.R, k)]
        self.types = (0, 1, 2)
        self.xvars = [(S, t) for S in self.adm for t in self.types]
        self.key = {}
        for (S, t) in self.xvars:
            self.key[('x', S, t)] = len(self.key)
        for r in C.R:
            self.key[('j', r)] = len(self.key)
        self.n = len(self.key)


def lam(q):
    return 10 - comb(10 - q, 2)


for trial in range(int(sys.argv[2]) if len(sys.argv) > 2 else 12):
    cl = random.randrange(551)
    beatsR = C.parse(lines[cl])
    a, b = 0, 1
    Rv = list(range(2, 13))
    Ov = list(range(13, N))
    B = [[False] * N for _ in range(N)]
    for i in range(N):
        for j in range(i + 1, N):
            if random.random() < 0.5:
                B[i][j] = True
            else:
                B[j][i] = True
    B[a][b], B[b][a] = True, False
    for i in range(11):
        for j in range(11):
            if i != j:
                B[Rv[i]][Rv[j]] = beatsR[(i, j)]
    for r in Rv:
        for p in (a, b):
            B[r][p], B[p][r] = True, False
    for y in Ov:
        if B[y][a] and B[y][b]:
            p = random.choice((a, b))
            B[y][p], B[p][y] = False, True
    Dm = lambda X: [w for w in range(N) if w not in X and all(B[w][x] for x in X)]
    assert sorted(Dm([a, b])) == Rv
    din = lambda w: sum(B[x][w] for x in range(N))
    Q = {y: frozenset(i for i in range(11) if B[Rv[i]][y]) for y in Ov}
    typ = {y: (0 if B[y][a] else (1 if B[y][b] else 2)) for y in Ov}
    j = {i: din(Rv[i]) - 25 for i in range(11)}
    J = sum(j.values())
    Sy = AllSets(beatsR, 'in')
    xval = {}
    for y in Ov:
        k = Sy.key[('x', Q[y], typ[y])]
        xval[k] = xval.get(k, 0) + 1
    for i in range(11):
        xval[Sy.key[('j', i)]] = j[i]          # may be negative in a random tournament: identities still hold
    lhs = lambda co: sum(c * xval.get(k, 0) for k, c in co.items())
    co, s, rhs = Sy.row(('C1',)); ok(lhs(co) == 38 and rhs == 38)
    for k in (2, 3, 4):
        for U in itertools.combinations(range(11), k):
            Um = sum(1 << u for u in U)
            co, s, rhs = Sy.row(('C3', Um))
            ok(lhs(co) + Sy.cR(frozenset(U)) == len(Dm([Rv[u] for u in U])))
            ok(rhs == {2: 11, 3: 5, 4: 1}[k] - Sy.cR(frozenset(U)))
    for p, pv in (('a', a), ('b', b)):
        for k in (1, 2, 3):
            for U in itertools.combinations(range(11), k):
                Um = sum(1 << u for u in U)
                co, s, rhs = Sy.row(('C4', p, Um))
                ok(lhs(co) + Sy.cR(frozenset(U)) == len(Dm([Rv[u] for u in U] + [pv])))
                ok(rhs == {1: 11, 2: 5, 3: 1}[k] - Sy.cR(frozenset(U)))
    for r in range(11):
        co, s, rhs = Sy.row(('C5', r))
        ok(lhs(co) == 18 and s == '==' and rhs == 18)
        ok(sum(1 for y in Ov if B[Rv[r]][y]) == 18 - j[r])
    n0 = sum(1 for y in Ov if typ[y] == 0)
    n1 = sum(1 for y in Ov if typ[y] == 1)
    ok(n0 == din(a) - 11)
    ok(n1 == din(b) - 12)
    for y in Ov:
        ok(len(Q[y]) == len(Dm([a, b, y])))
    # Lemma P identities
    trip = list(itertools.combinations(range(11), 3))
    Dsz = {U: len(Dm([Rv[u] for u in U])) for U in trip}
    for r in range(11):
        left = sum(Dsz[U] - 5 for U in trip if r in U)
        right = 5 + 10 * j[r] - sum(lam(len(Q[y])) for y in Ov if r not in Q[y])
        ok(left == right)
    ok(sum(len(Q[y]) - 5 for y in Ov) == 8 - J)
    ok(sum(Dsz.values()) == 110 + sum(comb(11 - len(Q[y]), 3) for y in Ov))

print('planted identity checks', checks, 'failures', fails)

# producer/checker agreement on the row systems
import lmodel
agree = 0
for cl in random.sample(range(551), 6):
    for mode, aux in (('free', False), ('in', False), ('out', False), ('reg', False), ('in', True), ('out', True),
                      ('reg', True)):
        M = lmodel.Model(lmodel.parse_class(lines[cl]), mode, aux=aux)
        Sy = C.System(C.parse(lines[cl]), mode, aux)
        vmap = []
        for v in M.vars:
            if v[0] == 'x':
                vmap.append(Sy.key[('x', C.bits_to_set(v[1]), v[2] if mode != 'free' else 'g')])
            elif v[0] == 'z':
                vmap.append(Sy.key[('z', C.bits_to_set(v[1]))])
            else:
                vmap.append(Sy.key[(v[0], v[1])])
        assert len(set(vmap)) == len(vmap) == Sy.n, 'variable universes differ'
        ok(all(M.ub[k] == (38 if M.vars[k][0] != 'j' else (0 if mode == 'reg' else 2)) and M.lb[k] == 0
               for k in range(len(M.vars))))
        for co, s, rhs, lab in M.rows:
            co2, s2, rhs2 = Sy.row(lab)
            ok({vmap[k]: c for k, c in co.items()} == co2 and s == s2 and rhs == rhs2)
            agree += 1
print('producer/checker row agreement checks', agree, 'total checks', checks, 'failures', fails)
