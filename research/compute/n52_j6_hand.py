"""Solver-free enumeration of J = 6 pair-level configurations, then class-by-class
S_2 placement of the 6+2 survivors.

This is not a rerun of n52_pairlevel.py. T[R] is taken from the 551 stored S_2
classes (c-matrix is an input, not a variable). The experiment asks: does any
actual 5-regular S_2 tournament on 11 vertices carry a 6+2 heavy pattern at J = 6?
"""
from __future__ import annotations

import itertools
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "proof" / "n51_local"))
from lmodel import N_R, check_class, parse_class  # noqa: E402

LAM = {6: 4, 7: 7, 8: 9, 9: 10, 10: 10, 11: 10}


def partitions(n, maxpart, maxlen):
    if n == 0:
        yield ()
        return
    if maxlen == 0:
        return
    for p in range(min(n, maxpart), 0, -1):
        for rest in partitions(n - p, p, maxlen - 1):
            yield (p,) + rest


def pair_ok(jvec, heavy, cmin=1):
    """Integer pair-level feasibility with free c in [cmin, 4] (or [cmin, 3] at V_0)."""
    J = sum(jvec)
    pos = [r for r in range(11) if jvec[r] > 0]
    zero = [r for r in range(11) if jvec[r] == 0]
    nlight = 39 - len(heavy)
    L, Ex, tau = {}, {}, {}
    for u in range(11):
        hs = [M for M in heavy if u in M]
        tau[u] = sum(6 - len(M) for M in hs)
        L[u] = 20 + jvec[u] - len(hs)
        Ex[u] = 5 + 10 * jvec[u] - sum(LAM[11 - len(M)] for M in hs)
        if L[u] < 0 or Ex[u] < 0:
            return False
    if sum(L.values()) != 6 * nlight:
        return False
    # V_+ pair integers D
    pairs = list(itertools.combinations(pos, 2)) if pos else []
    # bounds
    bounds = {}
    for u, v in pairs:
        hs = [M for M in heavy if u in M and v in M]
        eb = sum(6 - len(M) for M in hs)
        # 4D - c - 45 - eb in [0, min Ex], c in [cmin, 4]
        lo, hi = 12, 43
        ok_c = []
        for D in range(12, 44):
            for c in range(cmin, 5):
                s = 4 * D - c - 45 - eb
                if 0 <= s <= min(Ex[u], Ex[v]):
                    ok_c.append((D, c, s))
                    break
        if not ok_c:
            return False
        # store D range
        Ds = [D for D, _, _ in
              ((D, c, 4 * D - c - 45 - eb)
               for D in range(12, 44) for c in range(cmin, 5)
               if 0 <= 4 * D - c - 45 - eb <= min(Ex[u], Ex[v]))]
        bounds[(u, v)] = (min(Ds), max(Ds), eb)
    # pair-sum check as necessary condition
    for u in pos:
        need = 12 * (len(pos) - 1) + 5 * jvec[u] - tau[u]
        lo = sum(bounds[tuple(sorted((u, v)))][0] for v in pos if v != u)
        hi = sum(bounds[tuple(sorted((u, v)))][1] for v in pos if v != u)
        if not (lo <= need <= hi):
            return False
    # brute D assignment when s <= 5 (small)
    if len(pairs) > 10:
        return True  # only report the necessary filter
    keys = pairs
    ranges = {k: range(bounds[k][0], bounds[k][1] + 1) for k in keys}

    def rec(i, D):
        if i == len(keys):
            for u in pos:
                need = 12 * (len(pos) - 1) + 5 * jvec[u] - tau[u]
                got = sum(D[tuple(sorted((u, v)))] for v in pos if v != u)
                if got != need:
                    return False
            # c-windows exist?
            for u, v in keys:
                eb = bounds[(u, v)][2]
                Dv = D[(u, v)]
                if not any(0 <= 4 * Dv - c - 45 - eb <= min(Ex[u], Ex[v])
                           for c in range(cmin, 5)):
                    return False
            return True
        k = keys[i]
        for d in ranges[k]:
            D[k] = d
            if rec(i + 1, D):
                return True
        return False

    return rec(0, {})


def enum_j6(cmin=1):
    rows = []
    for part in partitions(6, 6, 11):
        jvec = list(part) + [0] * (11 - len(part))
        pos = [r for r in range(11) if jvec[r] > 0]
        seen = set()
        n_ok = 0
        survivors = []
        for epart in partitions(8, 6, 8):
            choices = [list(itertools.combinations(pos, 6 - e)) for e in epart]
            if any(len(ch) == 0 and e < 6 for e, ch in zip(epart, choices)):
                # e=6 has empty miss-set, combinations of 0
                pass
            choices = []
            for e in epart:
                sz = 6 - e
                if sz == 0:
                    choices.append([()])
                elif sz > len(pos):
                    choices.append([])
                else:
                    choices.append(list(itertools.combinations(pos, sz)))
            if any(len(ch) == 0 for ch in choices):
                continue
            for combo in itertools.product(*choices):
                heavy = [frozenset(M) for M in combo]
                key = tuple(sorted(tuple(sorted(M)) for M in heavy))
                if key in seen:
                    continue
                seen.add(key)
                if pair_ok(jvec, heavy, cmin=cmin):
                    n_ok += 1
                    survivors.append(([6 - len(M) for M in heavy], [sorted(M) for M in heavy]))
        rows.append({"j": list(part), "patterns_up_to_label": len(seen),
                     "survivors": n_ok, "examples": survivors[:5]})
    return rows


def cmat(out):
    inn = [sum(1 << i for i in range(N_R) if (out[i] >> j) & 1) for j in range(N_R)]
    return [[bin(inn[u] & inn[v]).count("1") if u != v else 0 for v in range(N_R)]
            for u in range(N_R)]


def class_carries(out, j_pattern, miss_size=4):
    """Does this S_2 class admit a labelling of V_+ and a 4-miss-set inside it
    meeting Lemma A (c<=3 at V_0) plus the pair-sum / Ex windows for 6+2?"""
    c = cmat(out)
    s = len(j_pattern)
    hits = []
    # Choose the set V_+, then assign the j-pattern up to equal-j symmetry.
    groups = []
    i = 0
    while i < s:
        j = i
        while j < s and j_pattern[j] == j_pattern[i]:
            j += 1
        groups.append((j_pattern[i], j - i))
        i = j
    for Vset in itertools.combinations(range(11), s):
        remaining = list(Vset)
        assignments = [None] * s
        def assign_groups(g, pool, slot):
            if g == len(groups):
                yield list(assignments)
                return
            val, cnt = groups[g]
            for chosen in itertools.combinations(pool, cnt):
                for k, v in enumerate(chosen):
                    assignments[slot + k] = v
                rest = [x for x in pool if x not in chosen]
                yield from assign_groups(g + 1, rest, slot + cnt)
        for Vplus in assign_groups(0, remaining, 0):
            pos = list(Vplus)
            zero = [r for r in range(11) if r not in pos]
            if any(c[u][v] > 3 for u in zero for v in range(11) if v != u):
                continue
            jvec = [0] * 11
            for ii, u in enumerate(pos):
                jvec[u] = j_pattern[ii]
            for M in itertools.combinations(pos, miss_size):
                Ex = {u: 5 + 10 * jvec[u] - (7 if u in M else 0) for u in range(11)}
                if any(Ex[u] < 0 for u in range(11)):
                    continue
                tau = {u: (2 if u in M else 0) for u in pos}
                Dneed = {u: 12 * (s - 1) + 5 * jvec[u] - tau[u] for u in pos}
                ranges = {}
                good = True
                for u, v in itertools.combinations(pos, 2):
                    eb = 2 if (u in M and v in M) else 0
                    cuv = c[u][v]
                    both = (u in M and v in M)
                    vals = []
                    for k in range(0, 40):
                        Dv = cuv + k + (1 if both else 0)
                        sv = 4 * Dv - cuv - 45 - eb
                        if 0 <= sv <= min(Ex[u], Ex[v]) and Dv >= 12:
                            vals.append(Dv)
                    ranges[tuple(sorted((u, v)))] = vals
                    if not vals:
                        good = False
                        break
                if not good:
                    continue
                keys = list(ranges)

                def rec(i, cur):
                    if i == len(keys):
                        for u in pos:
                            got = sum(cur[tuple(sorted((u, v)))] for v in pos if v != u)
                            if got != Dneed[u]:
                                return False
                        return True
                    for d in ranges[keys[i]]:
                        cur[keys[i]] = d
                        if rec(i + 1, cur):
                            return True
                    return False

                if rec(0, {}):
                    hits.append((list(pos), list(M)))
                    return hits
    return hits


def main():
    outp = Path(__file__).parent / "n52_j6_hand.json"
    payload = {}
    print("=== class-by-class 6+2 placement on 551 S_2 tournaments ===", flush=True)
    lines = (ROOT / "proof" / "n51_local" / "reg11_S2.txt").read_text().split()
    class_hits = {}
    pats = ([2, 2, 1, 1], [2, 1, 1, 1, 1]) if "--all" not in sys.argv else (
        [2, 2, 1, 1], [2, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1])
    for pat in pats:
        n = 0
        examples = []
        for ci, line in enumerate(lines):
            out = parse_class(line)
            check_class(out)
            hits = class_carries(out, pat)
            if hits:
                n += 1
                if len(examples) < 3:
                    examples.append({"class": ci, "labelling": hits[0]})
        class_hits[str(pat)] = {"classes_with_a_labelling": n, "examples": examples}
        print(pat, "classes", n, "examples", examples, flush=True)
    payload["class_hits"] = class_hits
    outp.write_text(json.dumps(payload, indent=1))
    print("wrote", outp)


if __name__ == "__main__":
    main()
