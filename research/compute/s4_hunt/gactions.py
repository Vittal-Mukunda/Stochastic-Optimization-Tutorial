"""Permutation actions of small odd-order groups on unions of coset spaces.

A group is given by generating permutations of a small base set; an action is a list of subgroups
(each given by generators, as words = elements of G); the vertex set is the disjoint union of the
coset spaces G/H_i (left cosets, G acting by left multiplication).
Returns (N, Gperms) with Gperms an array |G| x N, compatible with mkorbits / satgroup.
"""
import numpy as np


def compose(p, q):  # (p*q)(x) = p(q(x))
    return tuple(p[i] for i in q)


def closure(gens):
    n = len(gens[0])
    e = tuple(range(n))
    G = {e}; fr = [e]
    while fr:
        nf = []
        for h in fr:
            for g in gens:
                c = compose(g, h)
                if c not in G:
                    G.add(c); nf.append(c)
        fr = nf
    return sorted(G)


def affine_group(p, e):
    """Z_p x| C_e acting on Z_p (x -> a x + b), plus helper elements."""
    g = next(x for x in range(2, p) if all(pow(x, (p - 1) // q, p) != 1
                                              for q in range(2, p) if (p - 1) % q == 0 and all(q % r for r in range(2, q))))
    a = pow(g, (p - 1) // e, p)
    t = tuple((x + 1) % p for x in range(p))
    m = tuple((a * x) % p for x in range(p))
    return t, m


def cyclic(m):
    return tuple((x + 1) % m for x in range(m))


def power(p, k):
    n = len(p); r = tuple(range(n))
    for _ in range(k):
        r = compose(p, r)
    return r


def direct_product(g1s, n1, g2s, n2):
    """Generators of G1 x G2 acting on disjoint union of base sets (size n1+n2)."""
    gens = []
    for g in g1s:
        gens.append(tuple(list(g) + [n1 + i for i in range(n2)]))
    for g in g2s:
        gens.append(tuple(list(range(n1)) + [n1 + x for x in g]))
    return gens


def action(gens, subgroups):
    """subgroups: list of lists of generator elements (perms); [] means trivial subgroup."""
    G = closure(gens)
    idx = {g: i for i, g in enumerate(G)}
    perms_blocks = []
    offset = 0
    blocks = []
    for H_gens in subgroups:
        H = closure(H_gens) if H_gens else [tuple(range(len(G[0])))]
        Hs = set(H)
        coset_of = {}
        cosets = []
        for g in G:
            if g in coset_of:
                continue
            c = frozenset(compose(g, h) for h in H)
            for x in c:
                coset_of[x] = len(cosets)
            cosets.append(next(iter(c)))
        blocks.append((offset, coset_of, cosets))
        offset += len(cosets)
    N = offset
    P = np.zeros((len(G), N), dtype=np.int32)
    for gi, g in enumerate(G):
        for off, coset_of, cosets in blocks:
            for ci, rep in enumerate(cosets):
                P[gi, off + ci] = off + coset_of[compose(g, rep)]
    assert len(G) % 2 == 1
    return N, P


def n_pair_orbits(N, P):
    seen = np.zeros((N, N), dtype=bool); V = 0
    for u in range(N):
        for v in range(u + 1, N):
            if not seen[u, v]:
                V += 1
                seen[P[:, u], P[:, v]] = True; seen[P[:, v], P[:, u]] = True
    return V
