"""R8-G: exact S_4 checker and tabu search on arc reversals (numpy bitsets).

Convention: A[w, x] = 1 means w -> x (w beats x).  IN[x] is the bitset of
in-neighbours of x, so D(X) = AND_{x in X} IN[x] (members of X never beat
themselves, so they are excluded automatically).

Cost of a tournament = #undominated 4-sets + lam * sum_T max(0, 5 - |D(T)|)
over triples T.  Cost 0 iff the tournament has S_4 (S_4 forces |D(T)| >= 5).

For an arc u -> v, reversing it changes |D(X)| only for
  X containing v but not u: -1 if u dominated X (i.e. u -> X \\ {v});
  X containing u but not v: +1 if v -> X \\ {u}.
Hence the exact change of the cost for every arc is a sum over the critical
4-sets (0 or 1 dominators) and triples (<= 5 dominators); `deltas` computes
it for all arcs at once.
"""
from itertools import combinations
import numpy as np

_DT = np.uint64


def paley(p):
    qr = {(x * x) % p for x in range(1, p)}
    A = np.zeros((p, p), dtype=bool)
    for i in range(p):
        for j in range(p):
            if i != j and ((j - i) % p) in qr:
                A[i, j] = True
    return A


def circulant(n, S):
    S = set(s % n for s in S)
    A = np.zeros((n, n), dtype=bool)
    for i in range(n):
        for s in S:
            A[i, (i + s) % n] = True
    return A


def is_tournament(A):
    A = np.asarray(A, dtype=bool)
    N = len(A)
    return (not A.diagonal().any()) and bool(((A ^ A.T) | np.eye(N, dtype=bool)).all())


def in_bits(A):
    A = np.asarray(A, dtype=bool)
    N = len(A)
    W = (N + 63) // 64
    pad = np.zeros((N, 64 * W), dtype=bool)
    pad[:, :N] = A.T  # row x: who beats x
    by = np.packbits(pad, axis=1, bitorder="little")
    return np.ascontiguousarray(by).view(_DT).reshape(N, W).copy()


def popc(B):
    c = np.bitwise_count(B[:, 0]).astype(np.int32)
    for j in range(1, B.shape[1]):
        c += np.bitwise_count(B[:, j])
    return c


def rows(B, idx):
    """B[idx] for a (k, W) uint64 array, gathered as single 8W-byte items (much faster)."""
    W = B.shape[1]
    return B.view(np.dtype((np.void, 8 * W))).ravel()[idx].view(_DT).reshape(-1, W)


def set_rows(B, idx, X):
    W = B.shape[1]
    B.view(np.dtype((np.void, 8 * W))).ravel()[idx] = \
        np.ascontiguousarray(X).view(np.dtype((np.void, 8 * W))).ravel()


def unpack(B, N):
    B = np.ascontiguousarray(B)
    by = B.view(np.uint8).reshape(len(B), -1)
    return np.unpackbits(by, axis=1, bitorder="little")[:, :N].astype(bool)


def single_bit_index(B):
    """Index of the unique set bit in each row of B (rows must have popcount 1)."""
    W = B.shape[1]
    idx = np.bitwise_count(B[:, 0] - _DT(1)).astype(np.int64)
    if W == 1:
        return idx
    res = np.full(len(B), -1, dtype=np.int64)
    done = np.zeros(len(B), dtype=bool)
    for j in range(W):
        wj = B[:, j]
        hit = (wj != 0) & ~done
        res[hit] = 64 * j + np.bitwise_count(wj[hit] - _DT(1)).astype(np.int64)
        done |= hit
    return res


class Index:
    """Combinatorial index arrays for pairs, triples and 4-sets of range(N)."""

    _cache = {}

    def __new__(cls, N):
        if N in cls._cache:
            return cls._cache[N]
        self = super().__new__(cls)
        self.N = N
        self.pairs = np.array(list(combinations(range(N), 2)), dtype=np.int32)
        self.trip = np.array(list(combinations(range(N), 3)), dtype=np.int32)
        self.quad = np.fromiter((x for c in combinations(range(N), 4) for x in c),
                                dtype=np.int32).reshape(-1, 4)
        pid = np.full((N, N), -1, dtype=np.int32)
        pid[self.pairs[:, 0], self.pairs[:, 1]] = np.arange(len(self.pairs))
        tid = np.full((N, N, N), -1, dtype=np.int32)
        t = self.trip
        tid[t[:, 0], t[:, 1], t[:, 2]] = np.arange(len(t))
        q = self.quad
        # triple (pair-of-first-two, third) decomposition
        self.t_pair = pid[t[:, 0], t[:, 1]]
        self.t_sub = np.stack([pid[t[:, 1], t[:, 2]], pid[t[:, 0], t[:, 2]],
                               pid[t[:, 0], t[:, 1]]], axis=1)  # pair omitting pos i
        self.q_trip = tid[q[:, 0], q[:, 1], q[:, 2]]
        self.q_sub = np.stack([tid[q[:, 1], q[:, 2], q[:, 3]], tid[q[:, 0], q[:, 2], q[:, 3]],
                               tid[q[:, 0], q[:, 1], q[:, 3]], tid[q[:, 0], q[:, 1], q[:, 2]]],
                              axis=1)  # triple omitting pos i
        self.inc = [np.flatnonzero((q == v).any(axis=1)).astype(np.intp) for v in range(N)]
        self.inc_qt = [self.q_trip[s].astype(np.intp) for s in self.inc]
        self.inc_qd = [q[s, 3].astype(np.intp) for s in self.inc]
        self.inc3 = [np.flatnonzero((t == v).any(axis=1)).astype(np.intp) for v in range(N)]
        self.inc3_tp = [self.t_pair[s].astype(np.intp) for s in self.inc3]
        self.inc3_tc = [t[s, 2].astype(np.intp) for s in self.inc3]
        self.inc2 = [np.flatnonzero((self.pairs == v).any(axis=1)).astype(np.intp) for v in range(N)]
        self.q_trip = self.q_trip.astype(np.intp)
        self.t_pair = self.t_pair.astype(np.intp)
        cls._cache[N] = self
        return self


def profile(A):
    """Exact S_4 data: undominated 4-sets, min dominators of pairs/triples/4-sets."""
    A = np.asarray(A, dtype=bool)
    assert is_tournament(A)
    N = len(A)
    ix = Index(N)
    IN = in_bits(A)
    Dp = IN[ix.pairs[:, 0]] & IN[ix.pairs[:, 1]]
    Dt = rows(Dp, ix.t_pair) & IN[ix.trip[:, 2]]
    D4 = rows(Dt, ix.q_trip) & IN[ix.quad[:, 3]]
    c2, c3, c4 = popc(Dp), popc(Dt), popc(D4)
    und = np.flatnonzero(c4 == 0)
    indeg = A.sum(axis=0)
    return {
        "N": N,
        "undominated_4sets": int(len(und)),
        "min_pair_dom": int(c2.min()),
        "min_triple_dom": int(c3.min()),
        "triples_below_5": int((c3 < 5).sum()),
        "triple_deficit": int(np.maximum(0, 5 - c3).sum()),
        "min_4set_dom": int(c4.min()),
        "4sets_with_1_dom": int((c4 == 1).sum()),
        "indeg_min": int(indeg.min()),
        "indeg_max": int(indeg.max()),
        "indeg_hist": {int(k): int(v) for k, v in zip(*np.unique(indeg, return_counts=True))},
        "example_undominated": [int(x) for x in ix.quad[und[0]]] if len(und) else None,
        "S4": bool(len(und) == 0),
    }


class Tabu:
    def __init__(self, A, lam=1.0, rng=None):
        A = np.asarray(A, dtype=bool).copy()
        assert is_tournament(A)
        self.N = N = len(A)
        self.ix = Index(N)
        self.lam = float(lam)
        self.rng = rng if rng is not None else np.random.default_rng()
        self.A = A
        self.full_recompute()

    def full_recompute(self):
        ix = self.ix
        self.IN = in_bits(self.A)
        self.Dp = self.IN[ix.pairs[:, 0]] & self.IN[ix.pairs[:, 1]]
        self.Dt = rows(self.Dp, ix.t_pair) & self.IN[ix.trip[:, 2]]
        self.cnt3 = popc(self.Dt)
        self.D4 = rows(self.Dt, ix.q_trip) & self.IN[ix.quad[:, 3]]
        self.cnt4 = popc(self.D4)
        self.cost = self.cost_from_counts()

    def cost_from_counts(self):
        return float((self.cnt4 == 0).sum()) + self.lam * float(np.maximum(0, 5 - self.cnt3).sum())

    def deltas(self):
        """M[u, v] = exact cost change of reversing the arc u -> v (valid where A[u, v])."""
        N, ix = self.N, self.ix
        idx_parts, w_parts = [], []
        # 4-sets with a unique dominator w: reversing w -> x (x in X) uncovers X.
        s1 = np.flatnonzero(self.cnt4 == 1)
        if len(s1):
            w = single_bit_index(rows(self.D4, s1))
            q = ix.quad[s1]
            for i in range(4):
                idx_parts.append(w * N + q[:, i])
                w_parts.append(np.ones(len(s1)))
        # undominated 4-sets: x in X, v in D(X \ {x}), reversing x -> v covers X.
        s0 = np.flatnonzero(self.cnt4 == 0)
        if len(s0):
            q = ix.quad[s0]
            for i in range(4):
                x = q[:, i]
                bits = unpack(rows(self.Dt, ix.q_sub[s0, i]), N)
                bits[np.arange(len(s0)), x] = False
                r, v = np.nonzero(bits)
                idx_parts.append(x[r].astype(np.int64) * N + v)
                w_parts.append(-np.ones(len(r)))
        if self.lam:
            t5 = np.flatnonzero(self.cnt3 <= 5)
            if len(t5):
                bits = unpack(rows(self.Dt, t5), N)
                r, w = np.nonzero(bits)
                for i in range(3):
                    idx_parts.append(w.astype(np.int64) * N + ix.trip[t5[r], i])
                    w_parts.append(np.full(len(r), self.lam))
            t4 = np.flatnonzero(self.cnt3 <= 4)
            if len(t4):
                for i in range(3):
                    x = ix.trip[t4, i]
                    B = rows(self.Dp, ix.t_sub[t4, i]) & ~self.IN[x]
                    bits = unpack(B, N)
                    bits[np.arange(len(t4)), x] = False
                    r, v = np.nonzero(bits)
                    idx_parts.append(x[r].astype(np.int64) * N + v)
                    w_parts.append(np.full(len(r), -self.lam))
        if not idx_parts:
            return np.zeros((N, N))
        M = np.bincount(np.concatenate(idx_parts), weights=np.concatenate(w_parts),
                        minlength=N * N)
        return M.reshape(N, N)

    def apply(self, u, v):
        """Reverse arc u -> v."""
        assert self.A[u, v]
        self.A[u, v] = False
        self.A[v, u] = True
        wu, bu = divmod(u, 64)
        wv, bv = divmod(v, 64)
        self.IN[v, wu] &= ~_DT(1 << bu)
        self.IN[u, wv] |= _DT(1 << bv)
        ix = self.ix
        for z in (u, v):
            s = ix.inc2[z]
            self.Dp[s] = self.IN[ix.pairs[s, 0]] & self.IN[ix.pairs[s, 1]]
        for z in (u, v):
            s = ix.inc3[z]
            X = rows(self.Dp, ix.inc3_tp[z]) & self.IN[ix.inc3_tc[z]]
            set_rows(self.Dt, s, X)
            self.cnt3[s] = popc(X)
        for z in (u, v):
            s = ix.inc[z]
            X = rows(self.Dt, ix.inc_qt[z]) & self.IN[ix.inc_qd[z]]
            set_rows(self.D4, s, X)
            self.cnt4[s] = popc(X)

    def run(self, time_limit, max_iters=10**9, tenure=(8, 25), stall=2500,
            kick=(4, 12), log_every=0, log=print, t_start=None):
        import time
        t0 = time.time() if t_start is None else t_start
        N = self.N
        tabu = np.zeros((N, N), dtype=np.int64)
        best = self.cost
        bestA = self.A.copy()
        last_imp = 0
        n_kicks = 0
        it = 0
        trace = [(0, best)]
        while it < max_iters and time.time() - t0 < time_limit:
            it += 1
            M = self.deltas()
            allowed = self.A & (tabu < it)
            asp = self.A & (self.cost + M < best - 1e-9)
            cand = np.where(allowed | asp, M, np.inf)
            m = cand.min()
            if not np.isfinite(m):
                tabu[:] = 0
                continue
            choices = np.flatnonzero(cand <= m + 1e-9)
            k = int(self.rng.choice(choices))
            u, v = divmod(k, N)
            self.apply(u, v)
            self.cost += m
            tabu[u, v] = tabu[v, u] = it + int(self.rng.integers(tenure[0], tenure[1] + 1))
            if self.cost < best - 1e-9:
                best = self.cost
                bestA = self.A.copy()
                last_imp = it
                trace.append((it, best))
                if best <= 0:
                    break
            if it - last_imp > stall:
                # kick: restart from the best state with random arc reversals
                self.A = bestA.copy()
                nk = int(self.rng.integers(kick[0], kick[1] + 1))
                for _ in range(nk):
                    a, b = self.rng.choice(N, 2, replace=False)
                    self.A[a, b], self.A[b, a] = self.A[b, a], self.A[a, b]
                self.full_recompute()
                tabu[:] = 0
                last_imp = it
                n_kicks += 1
            if log_every and it % log_every == 0:
                log(f"  it={it} cost={self.cost:.1f} best={best:.1f} t={time.time()-t0:.0f}s")
        return {"best": best, "bestA": bestA, "iters": it, "kicks": n_kicks, "trace": trace}


def save_tournament(path, A, header_lines=()):
    A = np.asarray(A, dtype=bool)
    with open(path, "w", encoding="utf-8") as f:
        for h in header_lines:
            f.write("# " + h + "\n")
        for row in A.astype(int):
            f.write("".join(str(x) for x in row) + "\n")


def load_tournament(path):
    rows = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                rows.append([c == "1" for c in line])
    return np.array(rows, dtype=bool)
