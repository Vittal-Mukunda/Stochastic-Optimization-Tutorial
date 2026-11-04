"""N = 52 session 2026-11-04: checks for the L-adapted certificate (Lemma C') and the regular twin family.

Run from the project root:   python research/compute/n52_twin_certificate.py
Writes research/compute/n52_twin_certificate.json and prints a log (saved as n52_twin_certificate.log).

Notation (proof/N52_SESSION_2026-11-04.md).  T' is a regular tournament on 51 vertices.  For a pair P,
g_P = |D(P)| - 12.  For a triple Y: k = |D(Y)|, l = |D^+(Y)|, L = k + l, sigma = 1 (transitive) / 0 (cyclic),
G = sum of g over the three pairs of Y, u = (k - l)/2, v = k - (12 - sigma)/2.
Gamma2 = sum g^2, Gamma3 = sum g^3, Theta = sum over triangles of g12 g13 g23.
Phi_L(u) = -(2/3) u^3 + u^2 + (2/3 - (L - 12)^2 / 2) u.

Part A  global identities on random regular tournaments on 51 vertices (exact rational arithmetic).
Part B  the one-variable polynomial facts used by Lemma C' (sympy + integer grid).
Part C  the closed form of the survival sum of the regular twin family, on synthetic instances
        (12-regular tournament on 25 vertices, g with zero in- and out-sums supported on its arcs).
"""
from __future__ import annotations

import json
import os
import random
import sys
from fractions import Fraction as F
from itertools import combinations

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = {}


def log(*a):
    print(*a, flush=True)


# ----------------------------------------------------------------------------------------------
# tournaments as adjacency sets
# ----------------------------------------------------------------------------------------------

def rotational(n):
    """i -> i + 1, ..., i + (n-1)/2 (mod n): regular for odd n."""
    m = (n - 1) // 2
    A = [[False] * n for _ in range(n)]
    for i in range(n):
        for s in range(1, m + 1):
            A[i][(i + s) % n] = True
    return A


def scramble(A, steps, rng):
    """Reverse random directed 3-cycles; every in- and out-degree is preserved."""
    n = len(A)
    done = 0
    while done < steps:
        a, b, c = rng.sample(range(n), 3)
        if A[a][b] and A[b][c] and A[c][a]:
            A[a][b] = A[b][c] = A[c][a] = False
            A[b][a] = A[c][b] = A[a][c] = True
            done += 1
        elif A[b][a] and A[c][b] and A[a][c]:
            A[b][a] = A[c][b] = A[a][c] = False
            A[a][b] = A[b][c] = A[c][a] = True
            done += 1
    return A


def masks(A):
    n = len(A)
    IN = [0] * n
    OUTm = [0] * n
    for w in range(n):
        for x in range(n):
            if A[w][x]:
                IN[x] |= 1 << w
                OUTm[w] |= 1 << x
    return IN, OUTm


def pc(x):
    return bin(x).count("1")


def C2(x):
    return F(x) * (x - 1) / 2


def C3(x):
    return F(x) * (x - 1) * (x - 2) / 6


def Phi(L, u):
    return F(-2, 3) * u ** 3 + u ** 2 + (F(2, 3) - F((L - 12) ** 2, 2)) * u


def phiT(v):  # S5 certificate, transitive
    return F(-1, 4) + v ** 2 - F(2, 3) * (v ** 3 - v / 4)


def phiC(v):  # S5 certificate, cyclic
    return -1 + v ** 2 - F(2, 3) * (v ** 3 - v)


def lam_poly(L):
    s = F(L - 10)
    return s ** 3 / 3 - F(3, 4) * s ** 2 + F(2, 3) * s


def pi_poly(L):
    return lam_poly(L) + (L - 10) ** 2 + 3


# ----------------------------------------------------------------------------------------------
# Part A
# ----------------------------------------------------------------------------------------------

def part_A(A, tag):
    n = len(A)
    assert all(sum(A[i]) == (n - 1) // 2 for i in range(n)), "not regular"
    IN, OUTm = masks(A)
    g = {}
    for p, q in combinations(range(n), 2):
        g[(p, q)] = pc(IN[p] & IN[q]) - 12
    G2 = sum(x * x for x in g.values())
    G3 = sum(x ** 3 for x in g.values())
    res = {"tag": tag, "Gamma2": G2, "Gamma3": G3}

    # (I11) zero vertex sums and zero in-sums of g
    ok_vs = all(sum(g[tuple(sorted((v, z)))] for z in range(n) if z != v) == 0 for v in range(n))
    ok_in = all(sum(g[tuple(sorted((a, b)))] for a in range(n) if A[a][b]) == 0 for b in range(n))
    res["zero_vertex_sums"] = ok_vs
    res["zero_in_sums"] = ok_in

    S = {k: F(0) for k in ["uT", "uC", "u2", "Gu", "G2", "G3", "PhiL", "vT", "vC", "v2", "v3",
                           "phi", "Delta", "Gl", "GC2l", "Theta", "cubic_u", "u2G", "GuC"]}
    ok_L = True
    tri = []
    for a, b, c in combinations(range(n), 3):
        k = pc(IN[a] & IN[b] & IN[c])
        l = pc(OUTm[a] & OUTm[b] & OUTm[c])
        cyc = (A[a][b] and A[b][c] and A[c][a]) or (A[b][a] and A[c][b] and A[a][c])
        sig = 0 if cyc else 1
        gab, gac, gbc = g[(a, b)], g[(a, c)], g[(b, c)]
        G = gab + gac + gbc
        L = k + l
        if L != 12 - sig + G:
            ok_L = False
        u = F(k - l, 2)
        v = F(2 * k - 12 + sig, 2)
        if sig:
            S["uT"] += u
            S["vT"] += v
            S["phi"] += phiT(v)
        else:
            S["uC"] += u
            S["vC"] += v
            S["phi"] += phiC(v)
            S["GuC"] += G * u
        S["u2G"] += u * u * G
        S["u2"] += u * u
        S["Gu"] += G * u
        S["G2"] += G * G
        S["G3"] += G ** 3
        S["PhiL"] += Phi(L, u)
        S["v2"] += v * v
        S["v3"] += v ** 3
        S["Delta"] += C3(l) - C3(l - G)
        S["Gl"] += G * l
        S["GC2l"] += G * C2(l)
        S["Theta"] += gab * gac * gbc
        a_ = F(L, 2) - 1
        S["cubic_u"] += u ** 3 + (3 * a_ * a_ - 1) * u
        tri.append((a, b, c, k, l, sig, G))
    Th = S["Theta"]
    # Xi = sum over ordered pairs (P, Q) with P => Q (both vertices of P beat both of Q) of g_P g_Q
    Xi = 0
    pairs = list(g.keys())
    for P in pairs:
        if g[P] == 0:
            continue
        cplus = OUTm[P[0]] & OUTm[P[1]]
        mem = [z for z in range(n) if (cplus >> z) & 1]
        Xi += g[P] * sum(g[tuple(sorted(Q))] for Q in combinations(mem, 2))

    checks = {
        "L = 12 - sigma + G": ok_L,
        "sum_T u = 0": S["uT"] == 0,
        "sum_C u = 0": S["uC"] == 0,
        "sum u^2 = 16575 - G2/4 + G3/3": S["u2"] == 16575 - F(G2, 4) + F(G3, 3),
        "sum G u = 0": S["Gu"] == 0,
        "sum G^2 = 47 G2": S["G2"] == 47 * G2,
        "sum G^3 = 43 G3 + 6 Theta": S["G3"] == 43 * G3 + 6 * Th,
        "sum Phi_L(u) = sum u^2": S["PhiL"] == S["u2"],
        "cubic: sum (u^3 + c(L) u) = 0": S["cubic_u"] == 0,
        "S13: sum_T v = G2/2": S["vT"] == F(G2, 2),
        "S13: sum_C v = -G2/2": S["vC"] == -F(G2, 2),
        "S13: sum v^2 = 16575 + 11.5 G2 + G3/3": S["v2"] == 16575 + F(23, 2) * G2 + F(G3, 3),
        "S13 (R51) first form": S["phi"] == 7225 + F(45, 4) * G2 + F(G3, 3) - F(2, 3) * S["v3"],
        "S13 (R51) second form": S["phi"] == 7225 + F(13, 2) * G2 + F(G3, 3) - 2 * S["Delta"],
        "sum v^3 = 3 sum Delta + 7.125 G2": S["v3"] == 3 * S["Delta"] + F(57, 8) * G2,
        "sum v^3 = (3/2) sum u^2 G - (3/2) sum_C G u + (43 G3 + 6 Theta)/8":
            S["v3"] == F(3, 2) * S["u2G"] - F(3, 2) * S["GuC"] + (43 * G3 + 6 * Th) / F(8),
        "sum G l = 23 G2": S["Gl"] == 23 * G2,
        "sum G C(l,2) = 115 G2 + 5 G3 + Xi": S["GC2l"] == 115 * G2 + 5 * G3 + Xi,
    }
    # local sums at a vertex v (general regular T')
    loc_ok = True
    for v in random.Random(7).sample(range(n), 5):
        Nm = [z for z in range(n) if A[z][v]]
        Np = [z for z in range(n) if A[v][z]]
        sk = sum(t[3] for t in tri if v in t[:3])
        sCk = sum(C2(t[3]) for t in tri if v in t[:3])
        sCl = sum(C2(t[4]) for t in tri if v in t[:3])
        skl = sum(t[3] * t[4] for t in tri if v in t[:3])
        rk = sum(C2(11 + g[tuple(sorted(P))]) for P in combinations(Nm, 2))
        rl = sum(C2(11 + g[tuple(sorted(P))]) for P in combinations(Np, 2))
        rkl = sum(C2(pc(OUTm[a] & IN[b]) - 1) for a in Nm for b in Np)
        loc_ok &= (sk == 6900 and sCk == rk and sCl == rl and skl == rkl)
    checks["local sums at 5 vertices (6900, C(k,2), C(l,2), kl)"] = loc_ok
    # local cubic identities at a vertex v (true in every tournament):
    #   sum_{Y ni v} C(k,3) = sum_{Z in N^-(v)} C(l_Z - 1, 2),  sum_{Y ni v} C(l,3) = sum_{Z in N^+(v)} C(k_Z - 1, 2)
    kl_of = {t[:3]: (t[3], t[4]) for t in tri}
    cub_ok = True
    for v in random.Random(11).sample(range(n), 5):
        Nm = set(z for z in range(n) if A[z][v])
        Np = set(z for z in range(n) if A[v][z])
        lhs1 = sum(C3(t[3]) for t in tri if v in t[:3])
        lhs2 = sum(C3(t[4]) for t in tri if v in t[:3])
        rhs1 = sum(C2(kl_of[Z][1] - 1) for Z in kl_of if set(Z) <= Nm)
        rhs2 = sum(C2(kl_of[Z][0] - 1) for Z in kl_of if set(Z) <= Np)
        cub_ok &= (lhs1 == rhs1 and lhs2 == rhs2)
    checks["local cubic identities at 5 vertices"] = cub_ok
    res["checks"] = checks
    res["sum_v3"] = str(S["v3"])
    res["Theta"] = str(Th)
    res["Xi"] = Xi
    return res


# ----------------------------------------------------------------------------------------------
# Part B
# ----------------------------------------------------------------------------------------------

def part_B():
    res = {}
    Ls, us, ss, j, m = sp.symbols("L u s j m")
    Bsym = sp.Rational(2, 3) - (Ls - 12) ** 2 / 2
    Phis = -sp.Rational(2, 3) * us ** 3 + us ** 2 + Bsym * us
    lam_s = sp.expand(Phis.subs(us, 5 - Ls / 2))
    pi_s = sp.expand(Phis.subs(us, 4 - Ls / 2))
    sL = Ls - 10
    res["lambda(L) = (L-10)^3/3 - 3(L-10)^2/4 + 2(L-10)/3"] = sp.simplify(
        lam_s - (sL ** 3 / 3 - sp.Rational(3, 4) * sL ** 2 + sp.Rational(2, 3) * sL)) == 0
    res["pi(L) - lambda(L) = (L-10)^2 + 3"] = sp.simplify(pi_s - lam_s - ((Ls - 10) ** 2 + 3)) == 0
    res["pi(L) = (L-8)^3/3 - 7(L-8)^2/4 + 11(L-8)/3"] = sp.simplify(
        pi_s - ((Ls - 8) ** 3 / 3 - sp.Rational(7, 4) * (Ls - 8) ** 2 + sp.Rational(11, 3) * (Ls - 8))) == 0
    # hand-proof brackets (L = s + 10)
    f = lambda uu: (-sp.Rational(2, 3) * uu ** 3 + uu ** 2 + (sp.Rational(2, 3) - (ss - 2) ** 2 / 2) * uu)
    u0 = -ss / 2
    br1 = sp.expand(f(u0 + j) - f(u0) - j * (-ss ** 2 + ss * (j + 1) - sp.Rational(2, 3) * j ** 2 + j - sp.Rational(4, 3)))
    res["bracket for k = 5 + j (lambda is attained at k = 5)"] = br1 == 0
    u1 = -1 - ss / 2
    br2 = sp.expand(f(u1 + m) - f(u1) + sp.Rational(4, 3) * m
                    - m * (-ss ** 2 + (m - 1) * ss + 3 * m - sp.Rational(2, 3) * m ** 2 - 4))
    res["bracket for k = 4 + m (ratio 3/4)"] = br2 == 0
    # integer grid: lambda is the max over k >= 5, and Phi + (4/3)(k-4) <= pi
    ok_lam = ok_rat = True
    worst = F(0)
    for L in range(4, 201):
        lamL = lam_poly(L)
        piL = pi_poly(L)
        for k in range(5, L + 40):
            ph = Phi(L, F(2 * k - L, 2))
            if ph > lamL:
                ok_lam = False
            if ph + F(4, 3) * (k - 4) > piL:
                ok_rat = False
            if piL - ph > 0:
                worst = max(worst, F(k - 4) / (piL - ph))
        if Phi(L, F(8 - L, 2)) != piL:
            ok_rat = False
    res["grid L=4..200, k=5..L+39: Phi_L <= lambda(L)"] = ok_lam
    res["grid: Phi_L + (4/3)(k-4) <= pi(L), and Phi_L at k=4 equals pi(L)"] = ok_rat
    res["grid: max of (k-4)/(pi(L) - Phi_L)"] = str(worst)
    # delta expansions
    G = sp.symbols("G")
    # sympify the argument: lamf(11) with a Python int would otherwise produce floats
    lamf = lambda LL: ((sp.sympify(LL) - 10) ** 3 / 3 - sp.Rational(3, 4) * (sp.sympify(LL) - 10) ** 2
                       + sp.Rational(2, 3) * (sp.sympify(LL) - 10))
    pif = lambda LL: lamf(LL) + (sp.sympify(LL) - 10) ** 2 + 3
    res["dlam_1(G) = G/6 + G^2/4 + G^3/3"] = sp.expand(lamf(11 + G) - lamf(11) - (G / 6 + G ** 2 / 4 + G ** 3 / 3)) == 0
    res["dlam_0(G) = 5G/3 + 5G^2/4 + G^3/3"] = sp.expand(lamf(12 + G) - lamf(12) - (sp.Rational(5, 3) * G + sp.Rational(5, 4) * G ** 2 + G ** 3 / 3)) == 0
    res["dpi_1(G) = 13G/6 + 5G^2/4 + G^3/3"] = sp.expand(pif(11 + G) - pif(11) - (sp.Rational(13, 6) * G + sp.Rational(5, 4) * G ** 2 + G ** 3 / 3)) == 0
    res["dpi_0(G) = 17G/3 + 9G^2/4 + G^3/3"] = sp.expand(pif(12 + G) - pif(12) - (sp.Rational(17, 3) * G + sp.Rational(9, 4) * G ** 2 + G ** 3 / 3)) == 0
    # constants
    tab = {L: (str(lam_poly(L)), str(pi_poly(L)), (L - 10) ** 2 + 3) for L in range(8, 17)}
    res["table L: (lambda, pi, e)"] = tab
    T, Cc = sp.symbols("T C")
    # Lemma C' with DRT data: (4/3)(K_S - 4C(s,3)) <= (15300-T)/4 + (5525-C) + (17/4) T + 8 C - 16575
    rhs = sp.expand((15300 - T) * sp.Rational(1, 4) + (5525 - Cc) + sp.Rational(17, 4) * T + 8 * Cc - 16575)
    res["Lemma C' at a DRT: RHS = 4T + 7C - 7225"] = sp.simplify(rhs - (4 * T + 7 * Cc - 7225)) == 0
    base_out = F(15300 - 1650, 4) + (5525 - 650)
    base_in = 1650 * pi_poly(11) + 650 * pi_poly(12)
    res["twin baseline: sum_out lambda + sum_in pi"] = str(base_out + base_in)
    res["twin threshold 16575 + (4/3)*4100 - 20500"] = str(16575 + F(4, 3) * 4100 - (base_out + base_in))
    return res


# ----------------------------------------------------------------------------------------------
# Part C: synthetic regular-twin data
# ----------------------------------------------------------------------------------------------

def part_C(seed, n_cycles, scramble_steps):
    rng = random.Random(seed)
    nB = 25
    A = scramble(rotational(nB), scramble_steps, rng)
    assert all(sum(A[i]) == 12 for i in range(nB))
    lamB = {}
    for b, c in combinations(range(nB), 2):
        lamB[(b, c)] = sum(1 for z in range(nB) if A[z][b] and A[z][c])
    g = {P: 0 for P in lamB}
    placed = 0
    while placed < n_cycles:
        a1, a4, a2, a3 = rng.sample(range(nB), 4)
        if A[a1][a2] and A[a1][a3] and A[a4][a2] and A[a4][a3]:
            for (x, y, s) in [(a1, a2, 1), (a4, a3, 1), (a1, a3, -1), (a4, a2, -1)]:
                g[tuple(sorted((x, y)))] += s
            placed += 1
    # zero in- and out-sums
    for b in range(nB):
        assert sum(g[tuple(sorted((a, b)))] for a in range(nB) if A[a][b]) == 0
        assert sum(g[tuple(sorted((b, c)))] for c in range(nB) if A[b][c]) == 0
    G2 = sum(x * x for x in g.values())
    G3 = sum(x ** 3 for x in g.values())
    lam1 = lambda GG: lam_poly(11 + GG) - lam_poly(11)
    lam0 = lambda GG: lam_poly(12 + GG) - lam_poly(12)
    pi1 = lambda GG: pi_poly(11 + GG) - pi_poly(11)
    pi0 = lambda GG: pi_poly(12 + GG) - pi_poly(12)
    direct = F(G2, 4) - F(G3, 3)
    Lam = sum(g[P] * lamB[P] for P in g)
    for P, gp in g.items():
        if gp == 0:
            continue
        ncyc = 1 - gp + lamB[P]          # cyclic triples {w} u P, w in W (twin structure)
        direct += lam1(gp)               # {b0} u P, transitive
        direct += (25 - ncyc) * lam1(gp) + ncyc * lam0(gp)
    Theta = F(0)
    PsiC = F(0)
    PsiT = F(0)
    PsiTmid = F(0)
    sG2 = sG3 = 0
    for a, b, c in combinations(range(nB), 3):
        gab, gac, gbc = g[(a, b)], g[(a, c)], g[(b, c)]
        GG = gab + gac + gbc
        cyc = (A[a][b] and A[b][c] and A[c][a]) or (A[b][a] and A[c][b] and A[a][c])
        direct += pi0(GG) if cyc else pi1(GG)
        Theta += gab * gac * gbc
        pp = gab * gac + gab * gbc + gac * gbc
        sG2 += GG * GG
        sG3 += GG ** 3
        if cyc:
            PsiC += pp
        else:
            PsiT += pp
            # identify the middle vertex of the transitive triple
            for (x, y, z) in [(a, b, c), (a, c, b), (b, a, c), (b, c, a), (c, a, b), (c, b, a)]:
                if A[x][y] and A[y][z] and A[x][z]:
                    PsiTmid += g[tuple(sorted((x, y)))] * g[tuple(sorted((y, z)))]
    formula = F(89, 2) * G2 + 13 * G3 + 2 * Theta - 2 * Lam + 2 * PsiC
    return {
        "seed": seed, "Gamma2": G2, "Gamma3": G3, "Theta": str(Theta), "Lambda": Lam, "PsiC": str(PsiC),
        "direct survival sum": str(direct), "closed form 44.5G2+13G3+2Theta-2Lambda+2PsiC": str(formula),
        "agree": direct == formula,
        "sum_{Y in B} G^2 = 21 G2": sG2 == 21 * G2,
        "sum_{Y in B} G^3 = 17 G3 + 6 Theta": sG3 == 17 * G3 + 6 * Theta,
        "PsiT + PsiC = -G2": PsiT + PsiC == -G2,
        "PsiC = -PsiT_mid": PsiC == -PsiTmid,
    }


def part_D(rng, n=51, trials=3):
    """Any tournament: sum_Y Phi_{L_Y}(u_Y) = sum u^2 + sum (10 L - 70) u and sum (u^3 + c(L) u) = 0,
    with L = k + l, u = (k - l)/2.  (Starting point for target 2: non-regular T - x.)"""
    out = []
    for t in range(trials):
        A = [[False] * n for _ in range(n)]
        for i, j in combinations(range(n), 2):
            if rng.random() < 0.5:
                A[i][j] = True
            else:
                A[j][i] = True
        IN, OUTm = masks(A)
        s_phi = s_u2 = s_lin = s_cub = F(0)
        for a, b, c in combinations(range(n), 3):
            k = pc(IN[a] & IN[b] & IN[c])
            l = pc(OUTm[a] & OUTm[b] & OUTm[c])
            L = k + l
            u = F(k - l, 2)
            s_phi += Phi(L, u)
            s_u2 += u * u
            s_lin += (10 * L - 70) * u
            a_ = F(L, 2) - 1
            s_cub += u ** 3 + (3 * a_ * a_ - 1) * u
        degs = sorted(sum(A[w]) for w in range(n))
        out.append({"outdeg_range": [degs[0], degs[-1]], "sum Phi = sum u^2 + sum(10L-70)u": s_phi == s_u2 + s_lin,
                    "cubic identity": s_cub == 0})
    return out


def part_E():
    """Strengthened certificate for the twin structure at Gamma2 = 0 (the multipliers found by n52_twin_lp.py,
    rounded to the rationals they print as).  Checks every per-triple inequality exactly and evaluates the bound."""
    a_E2B = F(35, 3)      # weight of k on triples inside B
    a_E9 = F(7, 3)        # weight of C(l,3) on b0-triples, and of -C(k-1,2) on B-triples
    a_E8 = F(14, 3)       # weight of -u^2 on b0-triples
    tilt = {1: F(70, 3), 0: F(262, 9)}   # weight of u on b0-triples (their sigma-sums of u vanish)
    kappa = {("b0", 1): F(409, 12), ("b0", 0): F(440, 9), ("B", 1): F(563, 12), ("B", 0): F(143, 3),
             ("other", 1): F(1, 4), ("other", 0): F(1)}
    counts = {("b0", 1): 900, ("b0", 0): 325, ("B", 1): 1650, ("B", 0): 650,
              ("other", 1): 1650 + 5550 + 5550, ("other", 0): 650 + 1950 + 1950}
    ok = True
    tight = {}
    tables = {}
    for (reg, sig), kap in kappa.items():
        L = 12 - sig
        kmin = 4 if reg == "B" else 5
        rows = []
        for k in range(kmin, L + 1):
            u = F(2 * k - L, 2)
            l = L - k
            val = Phi(L, u)
            if reg == "b0":
                val += -a_E8 * u * u + tilt[sig] * u + a_E9 * C3(l)
            if reg == "B":
                val += a_E2B * k - a_E9 * C2(k - 1)
            rows.append((k, str(val)))
            if val > kap:
                ok = False
            if val == kap:
                tight.setdefault(f"{reg},sigma={sig}", []).append(k)
        tables[f"{reg},sigma={sig}"] = rows
    bound = sum(kappa[c] * counts[c] for c in kappa) - a_E2B * 13300 + a_E8 * 975
    return {"all per-triple inequalities hold": ok, "equality cases (k)": tight, "tables": tables,
            "bound on sum u^2": str(bound), "bound (float)": float(bound), "true value of sum u^2": 16575,
            "margin": str(16575 - bound)}


def main():
    rng = random.Random(20261104)
    log("Part A: random regular tournaments on 51 vertices")
    OUT["A"] = []
    for trial, steps in enumerate([0, 300, 3000, 20000]):
        A = scramble(rotational(51), steps, rng)
        r = part_A(A, f"rotational51 + {steps} 3-cycle reversals")
        OUT["A"].append(r)
        log(f"  {r['tag']}: Gamma2={r['Gamma2']}, Gamma3={r['Gamma3']}, Theta={r['Theta']}, Xi={r['Xi']}")
        log(f"    zero vertex sums: {r['zero_vertex_sums']}, zero in-sums: {r['zero_in_sums']}")
        for k_, v_ in r["checks"].items():
            log(f"    {'OK ' if v_ else 'FAIL'} {k_}")
    log("Part B: polynomial facts")
    OUT["B"] = part_B()
    for k_, v_ in OUT["B"].items():
        log(f"  {k_}: {v_}")
    log("Part C: synthetic regular-twin data")
    OUT["C"] = []
    for seed, nc, st in [(1, 3, 500), (2, 10, 2000), (3, 25, 5000), (4, 60, 5000)]:
        r = part_C(seed, nc, st)
        OUT["C"].append(r)
        log(f"  seed {seed}: " + ", ".join(f"{k_}={v_}" for k_, v_ in r.items() if k_ != "seed"))
    log("Part D: arbitrary (non-regular) tournaments on 51 vertices")
    OUT["D"] = part_D(rng)
    for r in OUT["D"]:
        log("  ", r)
    log("Part E: strengthened certificate for the twin structure at Gamma2 = 0")
    OUT["E"] = part_E()
    for k_, v_ in OUT["E"].items():
        log(f"  {k_}: {v_}")
    allA = all(all(r["checks"].values()) and r["zero_vertex_sums"] and r["zero_in_sums"] for r in OUT["A"])
    allB = all(v for k_, v in OUT["B"].items() if isinstance(v, bool))
    allC = all(r["agree"] and r["sum_{Y in B} G^2 = 21 G2"] and r["sum_{Y in B} G^3 = 17 G3 + 6 Theta"]
               and r["PsiT + PsiC = -G2"] and r["PsiC = -PsiT_mid"] for r in OUT["C"])
    allD = all(r["sum Phi = sum u^2 + sum(10L-70)u"] and r["cubic identity"] for r in OUT["D"])
    allE = OUT["E"]["all per-triple inequalities hold"]
    OUT["summary"] = {"A_all_ok": allA, "B_all_ok": allB, "C_all_ok": allC, "D_all_ok": allD, "E_ok": allE}
    allC = allC and allD and allE
    log("SUMMARY", OUT["summary"])
    with open(os.path.join(HERE, "n52_twin_certificate.json"), "w") as fh:
        json.dump(OUT, fh, indent=1, default=str)
    return 0 if (allA and allB and allC) else 1


if __name__ == "__main__":
    sys.exit(main())
