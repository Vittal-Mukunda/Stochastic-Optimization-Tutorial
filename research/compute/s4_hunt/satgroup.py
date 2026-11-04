"""SAT search for S_4 tournaments with a prescribed automorphism group (lazy CEGAR).

Group specs (vertices are numbered orbit-block by block, fixed points last):
  cyc:m:k:f        Z_m acting regularly on k blocks of size m, f fixed points.
  aff:p:e:k:f      Z_p x| C_e (x -> a x + b, a in the order-e subgroup of Z_p^*),
                   same action on each of k blocks of size p, f fixed points (e odd).
  aff2:p:e:k:f:s   like aff but the multiplier acts on block i as x -> a^(s^i) x + b ... (unused)

Variables: one per orbit of ordered pairs (u,v); the reverse orbit is its negation.
Aux p(w,{a,b}) -> (w->a & w->b) shared under the group (canonical orbit reps).
Constraints added up front: in-degree >= 23 for every vertex orbit; pair dominators >= 11.
Lazily: triples with < 5 dominators (cardinality), undominated 4-sets (clause).
"""
import argparse, json, os, sys, time, random
from itertools import combinations
import numpy as np
from pysat.solvers import Solver
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import r8g_core as rc  # noqa: E402


def build_group(spec):
    parts = spec.split(":")
    kind = parts[0]
    if kind == "cyc":
        m, k, f = map(int, parts[1:4])
        N = m * k + f
        gen = list(range(N))
        for b in range(k):
            for j in range(m):
                gen[b * m + j] = b * m + (j + 1) % m
        gens = [gen]
    elif kind == "aff":
        p, e, k, f = map(int, parts[1:5])
        N = p * k + f
        # element of order e in Z_p^*
        g = next(x for x in range(2, p) if pow(x, (p - 1), p) == 1 and
                 all(pow(x, d, p) != 1 for d in range(1, p - 1)))
        a = pow(g, (p - 1) // e, p)
        t = list(range(N)); mlt = list(range(N))
        for b in range(k):
            for j in range(p):
                t[b * p + j] = b * p + (j + 1) % p
                mlt[b * p + j] = b * p + (a * j) % p
        gens = [t, mlt]
    else:
        raise ValueError(spec)
    # closure
    ident = tuple(range(N))
    G = {ident}
    frontier = [ident]
    while frontier:
        new = []
        for h in frontier:
            for g in gens:
                c = tuple(g[h[i]] for i in range(N))
                if c not in G:
                    G.add(c); new.append(c)
        frontier = new
    G = np.array(sorted(G), dtype=np.int32)
    assert len(G) % 2 == 1, "group order must be odd"
    return N, G


class Model:
    def __init__(self, N, G, mindeg=23, pairmin=11, tripmin=5, solver="cadical195", seed=0):
        self.N, self.G = N, G
        self.pool = IDPool()
        self.S = Solver(name=solver)
        # arc variables
        self.arc = np.zeros((N, N), dtype=np.int64)
        for u in range(N):
            for v in range(N):
                if u == v or self.arc[u, v] != 0:
                    continue
                x = self.pool.id(("arc", u, v))
                imgs_u, imgs_v = G[:, u], G[:, v]
                for a, b in zip(imgs_u, imgs_v):
                    if self.arc[a, b] not in (0, x):
                        raise RuntimeError("inconsistent arc orbit")
                    self.arc[a, b] = x
                    if self.arc[b, a] not in (0, -x):
                        raise RuntimeError("group order even / reverses arc")
                    self.arc[b, a] = -x
        self.narc = self.pool.top
        self.pvar = {}
        self.added4 = set(); self.added3 = set(); self.nclauses = 0
        self.mindeg, self.pairmin, self.tripmin = mindeg, pairmin, tripmin
        self.build_p()
        # in-degree
        for v in self.orbit_reps_sets(1):
            lits = [int(self.arc[w, v[0]]) for w in range(N) if w != v[0]]
            self.atleast(lits, mindeg)
        # pairs
        for P in (self.orbit_reps_sets(2) if pairmin else []):
            a, b = P
            lits = [self.p(w, a, b) for w in range(N) if w not in P]
            self.atleast(lits, pairmin)
        if seed:
            rng = random.Random(seed)
            self.S.set_phases([v if rng.random() < 0.5 else -v for v in range(1, self.narc + 1)])

    def canon_many(self, Xs):
        """Canonical orbit representatives (sorted tuples) for an array of k-sets."""
        Xs = np.asarray(Xs, dtype=np.int64)
        if Xs.ndim == 1:
            Xs = Xs[None]
        k = Xs.shape[1]; N = self.N
        best = None
        for g in self.G:
            im = np.sort(g[Xs], axis=1)
            code = np.zeros(len(Xs), dtype=np.int64)
            for i in range(k):
                code = code * N + im[:, i]
            best = code if best is None else np.minimum(best, code)
        out = np.zeros((len(Xs), k), dtype=np.int64)
        c = best.copy()
        for i in range(k - 1, -1, -1):
            out[:, i] = c % N; c //= N
        return out

    def canon(self, X):
        return tuple(int(t) for t in self.canon_many([X])[0])

    def orbit_reps_sets(self, k):
        allX = np.array(list(combinations(range(self.N), k)), dtype=np.int64)
        reps = np.unique(self.canon_many(allX), axis=0)
        return [tuple(int(t) for t in r) for r in reps]

    def build_p(self):
        """p(w,a,b) var for every w and pair a<b not containing w (orbit-shared)."""
        N = self.N
        W, Ps = [], []
        for w in range(N):
            for a, b in combinations([x for x in range(N) if x != w], 2):
                W.append(w); Ps.append((a, b))
        W = np.array(W, dtype=np.int64); Ps = np.array(Ps, dtype=np.int64)
        best = None
        for g in self.G:
            w2 = g[W].astype(np.int64); a2 = g[Ps[:, 0]].astype(np.int64); b2 = g[Ps[:, 1]].astype(np.int64)
            code = (w2 * N + np.minimum(a2, b2)) * N + np.maximum(a2, b2)
            best = code if best is None else np.minimum(best, code)
        self.ptab = np.zeros((N, N, N), dtype=np.int64)
        keys, inv = np.unique(best, return_inverse=True)
        ids = np.zeros(len(keys), dtype=np.int64)
        for i, key in enumerate(keys):
            w0, r = divmod(int(key), N * N); a0, b0 = divmod(r, N)
            x = self.pool.id(("p", w0, a0, b0)); ids[i] = x
            self.add([-x, int(self.arc[w0, a0])]); self.add([-x, int(self.arc[w0, b0])])
        v = ids[inv.ravel()]
        self.ptab[W, Ps[:, 0], Ps[:, 1]] = v
        self.ptab[W, Ps[:, 1], Ps[:, 0]] = v

    def p(self, w, a, b):
        return int(self.ptab[w, a, b])

    def add(self, cl):
        self.S.add_clause(cl); self.nclauses += 1

    def atleast(self, lits, k):
        enc = CardEnc.atleast(lits=lits, bound=k, vpool=self.pool, encoding=EncType.seqcounter)
        for cl in enc.clauses:
            self.add(cl)

    def add_triple(self, c):
        c = tuple(int(t) for t in c)
        if c in self.added3:
            return False
        self.added3.add(c)
        a, b, cc = c
        lits = []
        for w in range(self.N):
            if w in c:
                continue
            y = self.pool.id(("t", w) + c)
            self.add([-y, self.p(w, a, b)]); self.add([-y, int(self.arc[w, cc])])
            lits.append(y)
        self.atleast(lits, self.tripmin)
        return True

    def add_quad(self, c):
        c = tuple(int(t) for t in c)
        if c in self.added4:
            return False
        self.added4.add(c)
        a, b, cc, d = c
        cl = []
        for w in range(self.N):
            if w in c:
                continue
            y = self.pool.id(("q", w) + c)
            self.add([-y, self.p(w, a, b)]); self.add([-y, self.p(w, cc, d)])
            cl.append(y)
        self.add(cl)
        return True

    def decode(self, model):
        val = np.zeros(self.pool.top + 1, dtype=bool)
        m = np.array(model[: self.narc])
        val[np.abs(m)] = m > 0
        A = np.where(self.arc > 0, val[np.abs(self.arc)], ~val[np.abs(self.arc)])
        np.fill_diagonal(A, False)
        return A


def violations(A, ix):
    IN = rc.in_bits(A)
    Dp = IN[ix.pairs[:, 0]] & IN[ix.pairs[:, 1]]
    Dt = rc.rows(Dp, ix.t_pair) & IN[ix.trip[:, 2]]
    c3 = rc.popc(Dt)
    D4 = rc.rows(Dt, ix.q_trip) & IN[ix.quad[:, 3]]
    c4 = rc.popc(D4)
    return ix.trip[c3 < 5], ix.quad[c4 == 0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--group", required=True)
    ap.add_argument("--seconds", type=float, default=7000)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--maxadd", type=int, default=20000)
    ap.add_argument("--notrip", action="store_true")
    ap.add_argument("--nopair", action="store_true")
    ap.add_argument("--solver", default="cadical195")
    ap.add_argument("--out", default=os.path.join(HERE, "runs"))
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    tag = f"sat_{args.group.replace(':', '-')}_s{args.seed}"
    logf = open(os.path.join(args.out, tag + ".log"), "a")

    def log(s):
        logf.write(f"[{time.strftime('%H:%M:%S')}] {s}\n"); logf.flush()

    t0 = time.time()
    N, G = build_group(args.group)
    log(f"start N={N} |G|={len(G)}")
    M = Model(N, G, seed=args.seed, pairmin=0 if args.nopair else 11, solver=args.solver)
    ix = rc.Index(N)
    log(f"model built arcvars={M.narc} clauses={M.nclauses} t={time.time()-t0:.0f}s")
    best = None; it = 0; outcome = "timeout"
    rng = np.random.default_rng(args.seed)
    while time.time() - t0 < args.seconds:
        it += 1
        remaining = args.seconds - (time.time() - t0)
        # time-limited solve via interrupt timer
        import threading
        timer = threading.Timer(remaining, M.S.interrupt); timer.start()
        r = M.S.solve_limited(expect_interrupt=True)
        timer.cancel()
        if r is None:
            outcome = "timeout"; break
        if r is False:
            outcome = "UNSAT"; log(f"UNSAT at it={it}"); break
        A = M.decode(M.S.get_model())
        bt, bq = violations(A, ix)
        nq = len(bq)
        if best is None or nq < best:
            best = nq
            rc.save_tournament(os.path.join(args.out, tag + "_best.txt"), A,
                               [f"{args.group} undominated={nq}"])
        log(f"it={it} undom4={nq} triples<5={len(bt)} best={best} q_orbits={len(M.added4)} "
            f"t_orbits={len(M.added3)} vars={M.pool.top} cls={M.nclauses} t={time.time()-t0:.0f}s")
        if nq == 0:
            outcome = "FOUND"
            rc.save_tournament(os.path.join(HERE if N <= 66 else args.out, f"FOUND_N{N}.txt"), A)
            log("FOUND"); break
        if len(bt) > args.maxadd: bt = bt[rng.choice(len(bt), args.maxadd, replace=False)]
        if len(bq) > args.maxadd: bq = bq[rng.choice(len(bq), args.maxadd, replace=False)]
        if len(bt) and not args.notrip:
            for T in np.unique(M.canon_many(bt), axis=0): M.add_triple(T)
        if len(bq):
            for X in np.unique(M.canon_many(bq), axis=0): M.add_quad(X)
        log(f"  added; vars={M.pool.top} cls={M.nclauses} t={time.time()-t0:.0f}s")
    res = {"method": "sat-group", "N": N, "group": args.group, "order": len(G), "seed": args.seed,
           "seconds": round(time.time() - t0), "iters": it, "best_undominated": best,
           "outcome": outcome, "q_orbits": len(M.added4), "t_orbits": len(M.added3)}
    log("RESULT " + json.dumps(res))
    with open(os.path.join(args.out, tag + ".json"), "w") as f:
        json.dump(res, f)


if __name__ == "__main__":
    main()
