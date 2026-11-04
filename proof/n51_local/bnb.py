"""Certified branch-and-bound for the local model (lmodel.Model).

Every node = root box + branching bounds + 'intersecting' propagation:
   if lb(x[S,t]) >= 1 for some (S,t), then ub(x[S',t']) = 0 for every S' disjoint from S  (S_4 on {a,b,y,y'}).
Branching: on one integer variable v with LP value f fractional:  (v <= floor f) | (v >= floor f + 1).
Leaves: exact integer Farkas certificate for (rows, node box).
Tree format (JSON-able):  ['B', var, k, left, right] | ['L', {row: y_int}] | ['X'] (two disjoint sets forced >= 1).
"""
import math, time
import numpy as np
import highspy
from lpcert import to_highs, exact_value, round_ray, cert_lp

INF = highspy.kHighsInf


class Searcher:
    def __init__(self, M, node_limit=200000, time_limit=None, priority=None):
        self.M = M
        self.nv = len(M.vars)
        self.rows = [(co, s, b) for co, s, b, l in M.rows]
        self.root_lb = list(M.lb)
        self.root_ub = list(M.ub)
        h = highspy.Highs()
        h.setOptionValue('output_flag', False)
        h.setOptionValue('presolve', 'off')
        h.setOptionValue('threads', 1)
        h.passModel(to_highs(self.nv, self.rows, self.root_lb, self.root_ub))
        self.h = h
        self.lb = list(self.root_lb)
        self.ub = list(self.root_ub)
        self.nodes = 0
        self.leaves = 0
        self.node_limit = node_limit
        self.time_limit = time_limit
        self.t0 = time.time()
        self.found = None
        # disjointness lists among x variables
        xs = [(i, v[1]) for i, v in enumerate(M.vars) if v[0] in ('x', 'z')]
        self.xidx = [i for i, _ in xs]
        self.setof = {i: S for i, S in xs}
        bysets = {}
        for i, S in xs:
            bysets.setdefault(S, []).append(i)
        self.disj = {}
        sets = list(bysets)
        for S in sets:
            lst = []
            for S2 in sets:
                if not (S & S2):
                    lst += bysets[S2]
            self.disj[S] = lst
        def prio_of(v):
            # big sets, j, c, z6, n, z5, x6, x5
            if v[0] == 'j': return 1
            if v[0] == 'c': return 2
            if v[0] == 'n': return 4
            p = bin(v[1]).count('1')
            if v[0] == 'z': return 3 if p == 6 else 5
            if p >= 9: return 0
            if getattr(M, 'aux', False): return 6 if p == 6 else 7
            return 2 if p == 6 else 3
        self.prio = [prio_of(v) for v in M.vars]
        if priority is not None:
            self.prio = priority

    # ---- bound management -------------------------------------------------
    def _apply(self, changes):
        """changes: list of (j, lo, hi); returns undo list."""
        undo = []
        for j, lo, hi in changes:
            undo.append((j, self.lb[j], self.ub[j]))
            self.lb[j], self.ub[j] = lo, hi
            self.h.changeColBounds(j, float(lo), float(hi))
        return undo

    def _undo(self, undo):
        for j, lo, hi in reversed(undo):
            self.lb[j], self.ub[j] = lo, hi
            self.h.changeColBounds(j, float(lo), float(hi))

    def propagate(self):
        """intersecting propagation; returns list of changes (j, lo, hi) or None if empty box."""
        ch = []
        seen = set()
        for i in self.xidx:
            if self.lb[i] >= 1:
                S = self.setof[i]
                if S in seen:
                    continue
                seen.add(S)
                for k in self.disj[S]:
                    if self.ub[k] > 0:
                        if self.lb[k] > 0:
                            return None
                        ch.append((k, self.lb[k], 0))
        return ch

    # ---- search ------------------------------------------------------------
    def leaf_cert(self):
        st = self.h.getModelStatus()
        cands = []
        try:
            _st, has, vals = self.h.getDualRay()
            if has:
                r = np.array(vals)
                cands += [r, -r]
        except Exception:
            pass
        for c in cands:
            y = round_ray(self.rows, c)
            v = exact_value(self.rows, self.lb, self.ub, y)
            if v is not None and v > 0:
                return y
        yr = cert_lp(self.nv, self.rows, self.lb, self.ub)
        if yr is not None:
            y = round_ray(self.rows, yr)
            v = exact_value(self.rows, self.lb, self.ub, y)
            if v is not None and v > 0:
                return y
        return None

    def choose(self, x):
        best = None
        for j in range(self.nv):
            f = x[j] - math.floor(x[j] + 1e-9)
            if 1e-6 < f < 1 - 1e-6:
                key = (self.prio[j], -min(f, 1 - f) if self.prio[j] >= 2 else -x[j])
                if best is None or key < best[0]:
                    best = (key, j)
        return None if best is None else best[1]

    def run(self):
        """returns ('INF', tree) or ('FEAS', x) or ('LIMIT', None)."""
        try:
            tree = self._node()
        except _Abort as e:
            return e.args[0], e.args[1]
        return 'INF', tree

    def _node(self):
        self.nodes += 1
        if self.nodes > self.node_limit or (self.time_limit and time.time() - self.t0 > self.time_limit):
            raise _Abort('LIMIT', None)
        self.h.run()
        st = self.h.getModelStatus()
        if st == highspy.HighsModelStatus.kInfeasible:
            y = self.leaf_cert()
            if y is None:
                raise _Abort('NOCERT', None)
            self.leaves += 1
            return ['L', {i: v for i, v in enumerate(y) if v}]
        if st != highspy.HighsModelStatus.kOptimal:
            raise _Abort('LPFAIL:' + str(st), None)
        x = np.array(self.h.getSolution().col_value)
        j = self.choose(x)
        if j is None:
            raise _Abort('FEAS', x)
        k = math.floor(x[j] + 1e-9)
        kids = []
        for lo, hi in ((self.lb[j], k), (k + 1, self.ub[j])):
            if lo > hi:
                kids.append(None)
                continue
            u1 = self._apply([(j, lo, hi)])
            ch = self.propagate()
            if ch is None:
                # two disjoint sets both forced >= 1: contradicts the intersecting property directly
                self._undo(u1)
                self.leaves += 1
                kids.append(['X'])
                continue
            u2 = self._apply(ch)
            kids.append(self._node())
            self._undo(u2)
            self._undo(u1)
        return ['B', j, k, kids[0], kids[1]]


class _Abort(Exception):
    pass


def tree_stats(t):
    if t is None:
        return 0, 0
    if t[0] == 'L':
        return 1, 1
    a, b = tree_stats(t[3]), tree_stats(t[4])
    return a[0] + b[0] + 1, a[1] + b[1]


class StrongSearcher(Searcher):
    """Same proof format; the branching variable is picked by probing both children of up to `K` candidates."""

    def __init__(self, M, K=10, **kw):
        super().__init__(M, **kw)
        self.K = K
        self.probes = 0

    def _probe(self, j, lo, hi):
        u1 = self._apply([(j, lo, hi)])
        ch = self.propagate()
        if ch is None:
            self._undo(u1)
            return True
        u2 = self._apply(ch)
        self.h.run()
        self.probes += 1
        inf = self.h.getModelStatus() == highspy.HighsModelStatus.kInfeasible
        self._undo(u2)
        self._undo(u1)
        return inf

    def choose(self, x):
        cand = []
        for j in range(self.nv):
            f = x[j] - math.floor(x[j] + 1e-9)
            if 1e-6 < f < 1 - 1e-6:
                cand.append((self.prio[j], -min(f, 1 - f), j))
        if not cand:
            return None
        cand.sort()
        top = cand[0][0]
        pool = [c for c in cand if c[0] == top][:self.K]
        if len(pool) < self.K:
            pool += [c for c in cand if c[0] != top][:self.K - len(pool)]
        best = None
        for _, negf, j in pool:
            k = math.floor(x[j] + 1e-9)
            a = self._probe(j, self.lb[j], k)
            b = self._probe(j, k + 1, self.ub[j])
            score = (a + b, -negf)
            if a and b:
                best = (score, j)
                break
            if best is None or score > best[0]:
                best = (score, j)
        # restore the node LP solution state (basis) for consistency
        self.h.run()
        return best[1]
