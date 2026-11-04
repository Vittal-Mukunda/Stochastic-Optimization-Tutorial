"""Local model for the claim 'J >= 3' at N = 51 (Erdos #902, case (I)), written from scratch.

Setting.  T has S_4, N = 51, min in-degree >= 24, Z = {d^- = 24}, 1 <= |Z| <= 5, sum_{x not in Z}(d^-(x)-25) = |Z|.
P = {a, b} is a tight pair, a -> b, R = D(P) (11 vertices, T[R] 5-regular S_2: one of the 551 classes).
O = the other 38 vertices.  For y in O:  Q_y = R n N^-(y) = D(P + y);  type 0: y->a, b->y;  type 1: a->y, y->b;
type 2: a->y, b->y   (y->a and y->b is impossible since then y would lie in D(P) = R).
For r in R: d^-(r) = 25 + j_r with j_r >= 0 (Lemma T), and deg_O(r) := |N^+(r) n O| = 18 - j_r.
Mode 'in' : d^-(b) = 24  (b in Z)  <=>  n1 = 12;    a: d^-(a) = 11 + n0 in [24, ..], excess budget n0 + J <= 19.
Mode 'out': d^-(a) = 24  (a in Z)  <=>  n0 = 13;    b: d^-(b) = 12 + n1 in [24, ..], excess budget n1 + J <= 18.
Hypothesis to refute: J = sum_r j_r <= 2.

Variables: x[S,t] (# y in O with Q_y = S, type t), integer >= 0;  j[r] integer in [0, 2].
Rows are (coef dict, sense, rhs, label) with integer data; labels identify each row for the independent checker.
"""
import itertools

N_R = 11
FULL = (1 << N_R) - 1
NU = {1: 23, 2: 11, 3: 5, 4: 1}          # lower bounds on |D(X)| for |X| = 1..4 (only 2,3,4 used for subsets of R)


def popc(x):
    return bin(x).count('1')


def parse_class(line):
    """Upper-triangle string, pairs (i, j) with i < j in lexicographic order; '1' means i -> j.
    Returns out[i] = bitmask of out-neighbours of i inside R."""
    line = line.strip()
    assert len(line) == 55
    out = [0] * N_R
    k = 0
    for i in range(N_R):
        for j in range(i + 1, N_R):
            if line[k] == '1':
                out[i] |= 1 << j
            else:
                out[j] |= 1 << i
            k += 1
    return out


def check_class(out):
    """5-regular and S_2 (every pair of R has a common dominator inside R)."""
    inn = [sum(1 << i for i in range(N_R) if (out[i] >> j) & 1) for j in range(N_R)]
    assert all(popc(o) == 5 for o in out) and all(popc(i) == 5 for i in inn)
    for u, v in itertools.combinations(range(N_R), 2):
        assert inn[u] & inn[v], (u, v)
    return inn


def cR(out, U):
    """number of w in R \\ U with U subset of N^+(w)."""
    return sum(1 for w in range(N_R) if not (U >> w) & 1 and (out[w] & U) == U)


def admissible(out, sizes):
    inn = [sum(1 << i for i in range(N_R) if (out[i] >> j) & 1) for j in range(N_R)]
    res = []
    for S in range(1 << N_R):
        if popc(S) in sizes and all(S & inn[z] for z in range(N_R)):
            res.append(S)
    return res


def lam(q):
    """lambda(q) = 10 - C(10-q, 2)  (weight of a y with |Q_y| = q that beats r)."""
    m = 10 - q
    return 10 - m * (m - 1) // 2


class Model:
    """mode in {'in', 'out', 'free'} ('free' = drop the U+{a}, U+{b} rows and the mode rows: valid for both)."""

    def __init__(self, out, mode, Jmax=2, pattern=True, aux=False):
        self.aux = aux and mode != 'free'
        if mode == 'reg':
            Jmax = 0              # case (R): every in-degree is 25
        self.out = out
        self.mode = mode
        self.Jmax = Jmax
        self.pattern = pattern
        sizes = (5, 6, 9, 10, 11) if pattern else tuple(range(5, 12))
        self.adm = admissible(out, sizes)
        types = (0, 1, 2) if mode != 'free' else (2,)   # 'free': a single generic type
        self.types = types
        self.vars = [('x', S, t) for S in self.adm for t in types] + [('j', r) for r in range(N_R)]
        if self.aux:
            # auxiliary integer variables, each defined by an equality row (labels 'Z', 'N', 'Cc'):
            #   z[S] = sum_t x[S,t] (|S| = 5, 6);  n[t] = sum_S x[S,t];  c[r] = #{y : |Q_y| = 6, r not in Q_y}
            self.vars += [('z', S) for S in self.adm if popc(S) in (5, 6)]
            self.vars += [('n', t) for t in types] + [('c', r) for r in range(N_R)]
        self.idx = {v: i for i, v in enumerate(self.vars)}
        self.lb = [0] * len(self.vars)
        self.ub = [Jmax if v[0] == 'j' else 38 for v in self.vars]
        self.rows = []
        self._build()

    def X(self, pred):
        """coef dict {var index: 1} for x-variables (S, t) with pred(S, t)."""
        return {i: 1 for i, v in enumerate(self.vars) if v[0] == 'x' and pred(v[1], v[2])}

    def J(self, r):
        return self.idx[('j', r)]

    def add(self, co, sense, rhs, label):
        co = {k: v for k, v in co.items() if v != 0}
        self.rows.append((co, sense, rhs, label))

    def _build(self):
        out = self.out
        self.add(self.X(lambda S, t: True), '==', 38, ('C1',))
        for k in (2, 3, 4):
            for U in itertools.combinations(range(N_R), k):
                Um = sum(1 << u for u in U)
                need = NU[k] - cR(out, Um)
                if need > 0:
                    self.add(self.X(lambda S, t: not (S & Um)), '>=', need, ('C3', Um))
        if self.mode != 'free':
            for t, p in ((0, 'a'), (1, 'b')):
                for k in (1, 2, 3):
                    for U in itertools.combinations(range(N_R), k):
                        Um = sum(1 << u for u in U)
                        need = NU[k + 1] - cR(out, Um)
                        if need > 0:
                            self.add(self.X(lambda S, tt: tt == t and not (S & Um)), '>=', need, ('C4', p, Um))
        for r in range(N_R):
            co = self.X(lambda S, t: (S >> r) & 1)
            co[self.J(r)] = 1
            self.add(co, '==', 18, ('C5', r))
        self.add({self.J(r): 1 for r in range(N_R)}, '<=', self.Jmax, ('C6',))
        if self.mode == 'in':
            self.add(self.X(lambda S, t: t == 1), '==', 12, ('M', 'n1=12'))
            self.add(self.X(lambda S, t: t == 0), '>=', 13, ('M', 'n0>=13'))
            co = self.X(lambda S, t: t == 0)
            for r in range(N_R):
                co[self.J(r)] = 1
            self.add(co, '<=', 19, ('M', 'n0+J<=19'))
        elif self.mode == 'reg':
            # case (R): T regular, so d^-(a) = d^-(b) = 25 and J = 0 (use with Jmax = 0)
            self.add(self.X(lambda S, t: t == 0), '==', 14, ('M', 'n0=14'))
            self.add(self.X(lambda S, t: t == 1), '==', 13, ('M', 'n1=13'))
        elif self.mode == 'out':
            self.add(self.X(lambda S, t: t == 0), '==', 13, ('M', 'n0=13'))
            self.add(self.X(lambda S, t: t == 1), '>=', 12, ('M', 'n1>=12'))
            co = self.X(lambda S, t: t == 1)
            for r in range(N_R):
                co[self.J(r)] = 1
            self.add(co, '<=', 18, ('M', 'n1+J<=18'))
        if self.pattern:
            # Lemma P (valid when J <= 2): sets of size 7, 8 already excluded from the variables
            self.add(self.X(lambda S, t: popc(S) >= 9), '==', 1, ('P2',))
            self.add(self.X(lambda S, t: popc(S) == 6), '<=', 2, ('P5',))
            for r in range(N_R):
                co = self.X(lambda S, t: popc(S) in (9, 10) and not (S >> r) & 1)
                co[self.J(r)] = -1
                self.add(co, '<=', 0, ('P3', r))
                co = self.X(lambda S, t: popc(S) in (6, 9, 10) and not (S >> r) & 1)
                co[self.J(r)] = -1
                self.add(co, '<=', 1, ('P4', r))
        if self.aux:
            self._build_aux()

    def _build_aux(self):
        for S in self.adm:
            if popc(S) in (5, 6):
                co = self.X(lambda S2, t: S2 == S)
                co[self.idx[('z', S)]] = -1
                self.add(co, '==', 0, ('Z', S))
        for t in self.types:
            co = self.X(lambda S, tt: tt == t)
            co[self.idx[('n', t)]] = -1
            self.add(co, '==', 0, ('N', t))
        for r in range(N_R):
            co = self.X(lambda S, t: popc(S) == 6 and not (S >> r) & 1)
            co[self.idx[('c', r)]] = -1
            self.add(co, '==', 0, ('Cc', r))

    def sizes(self):
        return len(self.vars), len(self.rows)
