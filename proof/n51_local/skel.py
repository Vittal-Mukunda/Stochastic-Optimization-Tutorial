"""Skeleton split at the root, optionally modulo automorphisms of T[R].

Skeleton = (the unique y* with q >= 9: its set S* and type t*, the vector j).  By Lemma P every integer solution has
exactly one such (S*, t*) with x = 1, j in {0,1,2}^11 with sum <= 2, and j_r >= 1 for r not in S* (row P3).
An automorphism s of T[R] maps configurations to configurations (S -> s(S), types kept, j'_{s(r)} = j_r), so it is
enough to refute one skeleton per orbit.  Tree node:  ['K', perms, [[bigvar, jvec, subtree], ...]].
"""
import itertools, time
from lmodel import popc, N_R
from bnb import Searcher, StrongSearcher, _Abort


def automorphisms(out):
    res = []
    def ext(m, used):
        k = len(m)
        if k == N_R:
            res.append(tuple(m)); return
        for v in range(N_R):
            if v not in used and all(((out[i] >> k) & 1) == ((out[m[i]] >> v) & 1) for i in range(k)):
                m.append(v); used.add(v); ext(m, used); m.pop(); used.discard(v)
    ext([], set())
    return res


def jvectors():
    for j in itertools.product((0, 1, 2), repeat=N_R):
        if sum(j) <= 2:
            yield j


def act(p, S, j):
    S2 = 0
    for r in range(N_R):
        if (S >> r) & 1:
            S2 |= 1 << p[r]
    j2 = [0] * N_R
    for r in range(N_R):
        j2[p[r]] = j[r]
    return S2, tuple(j2)


def skeleton_list(M, perms):
    bigs = [(i, v[1], v[2]) for i, v in enumerate(M.vars) if v[0] == 'x' and popc(v[1]) >= 9]
    byst = {(S, t): i for i, S, t in bigs}
    reps = []
    for i, S, t in bigs:
        for j in jvectors():
            if any(j[r] > M.ub[M.idx[('j', r)]] for r in range(N_R)):
                continue                      # outside the root box (e.g. mode 'reg': j = 0)
            if any(j[r] == 0 for r in range(N_R) if not (S >> r) & 1):
                continue
            key = (S, t, j)
            canon = min((act(p, S, j)[0], t, act(p, S, j)[1]) for p in perms) if perms else key
            if canon == key:
                reps.append((i, j))
    return reps


def run_skeleton(M, perms, strong=0, node_limit=10**6, time_limit=None, verbose=False):
    S = StrongSearcher(M, K=strong, node_limit=node_limit, time_limit=time_limit) if strong else \
        Searcher(M, node_limit=node_limit, time_limit=time_limit)
    reps = skeleton_list(M, perms)
    kids = []
    jidx = [M.idx[('j', r)] for r in range(N_R)]
    t0 = time.time()
    for n, (b, j) in enumerate(reps):
        ch = [(b, 1, S.ub[b])] + [(jidx[r], j[r], j[r]) for r in range(N_R)]
        u1 = S._apply(ch)
        pr = S.propagate()
        if pr is None:
            S._undo(u1); kids.append([b, list(j), ['X']]); continue
        u2 = S._apply(pr)
        try:
            sub = S._node()
        except _Abort as e:
            S._undo(u2); S._undo(u1)
            return e.args[0], (b, j, e.args[1]), S
        S._undo(u2); S._undo(u1)
        kids.append([b, list(j), sub])
        if verbose and n % 50 == 0:
            print('skeleton', n, '/', len(reps), 'nodes', S.nodes, round(time.time() - t0, 1), flush=True)
    return 'INF', ['K', [list(p) for p in perms], kids], S
