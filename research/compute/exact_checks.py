"""Exact checks for the Erdős 902 baseline.

Independent of proof/verify_proof.py. Prints a JSON object on stdout.
The proofs of Lemma S1 and Lemma I are in research/LEMMAS.md; this file
checks the arithmetic and evaluates Paley tournaments.
"""

from __future__ import annotations

import itertools
import json
import random
import sys
import time
from math import comb


def check(failures: list[str], cond: bool, msg: str) -> None:
    if not cond:
        failures.append(msg)


def paley_out(p: int) -> list[int]:
    residues = {pow(a, 2, p) for a in range(1, p)}
    out = [0] * p
    for i in range(p):
        for s in residues:
            out[i] |= 1 << ((i + s) % p)
    return out


def in_neighbourhoods(out: list[int]) -> list[int]:
    n = len(out)
    inn = [0] * n
    for v, bits in enumerate(out):
        while bits:
            low = bits & -bits
            u = low.bit_length() - 1
            inn[u] |= 1 << v
            bits ^= low
    return inn


def assert_tournament(failures: list[str], out: list[int], name: str) -> None:
    n = len(out)
    for i in range(n):
        check(failures, ((out[i] >> i) & 1) == 0, f"{name}: loop at {i}")
        for j in range(i + 1, n):
            arc = ((out[i] >> j) & 1) + ((out[j] >> i) & 1)
            check(failures, arc == 1, f"{name}: pair {i},{j} has {arc} arcs")


def score_and_pair_sum(out: list[int]) -> tuple[int, int, list[int]]:
    """Return (sum |D(pair)|, sum C(d+, 2), in-degrees)."""
    n = len(out)
    inn = in_neighbourhoods(out)
    indeg = [bits.bit_count() for bits in inn]
    sum_c = 0
    for v in range(n):
        outdeg = n - 1 - indeg[v]
        sum_c += comb(outdeg, 2)
    sum_d = 0
    for u, v in itertools.combinations(range(n), 2):
        sum_d += (inn[u] & inn[v]).bit_count()
    return sum_d, sum_c, indeg


def min_dominators(inn: list[int], s: int) -> tuple[int, tuple[int, ...] | None]:
    n = len(inn)
    best = n + 1
    witness = None
    for subset in itertools.combinations(range(n), s):
        mask = inn[subset[0]]
        for v in subset[1:]:
            mask &= inn[v]
        k = mask.bit_count()
        if k < best:
            best = k
            witness = subset
            if best == 0 and s >= 3:
                # The minimum cannot go below 0. Keep scanning only when a
                # positive minimum is still possible; a zero already decides
                # S_s and the strong triple claim for s = 3.
                break
    return best, witness


def profile(out: list[int], max_s: int, stop_triple_at_zero: bool = True) -> dict:
    inn = in_neighbourhoods(out)
    n = len(out)
    mins = [n]
    witnesses: list[tuple[int, ...] | None] = [()]
    for s in range(1, max_s + 1):
        if s == 3 and stop_triple_at_zero:
            best, witness = min_dominators(inn, s)
        else:
            # For s = 4 a zero still has to be a true minimum, and 0 is the
            # minimum, so the same early exit is correct.
            best, witness = min_dominators(inn, s)
        mins.append(best)
        witnesses.append(witness)
    return {"min": mins, "witness": [list(w) if w else [] for w in witnesses]}


def recompute_dominators(out: list[int], subset: list[int]) -> int:
    inn = in_neighbourhoods(out)
    mask = (1 << len(out)) - 1
    for v in subset:
        mask &= inn[v]
    return mask.bit_count()


def transitive_52() -> list[int]:
    out = [0] * 52
    for i in range(52):
        for j in range(i + 1, 52):
            out[i] |= 1 << j
    return out


def random_52(seed: int) -> list[int]:
    rng = random.Random(seed)
    out = [0] * 52
    for i in range(52):
        for j in range(i + 1, 52):
            if rng.randrange(2) == 0:
                out[i] |= 1 << j
            else:
                out[j] |= 1 << i
    return out


def check_lemma_s1(failures: list[str]) -> dict:
    check(failures, comb(52, 2) == 1326, "C(52,2)")
    check(failures, 1326 - 25 * 52 == 26, "sum e")
    check(failures, (52 * 650 - 51 * 26) // 2 == 16237, "constant term")
    check(failures, 26 * comb(26, 2) + 26 * comb(25, 2) == 16250, "balanced sum")
    check(failures, 16237 + 13 == 16250, "half of 26")
    check(failures, 12 * 1326 == 15912, "twelve times pairs")
    check(failures, 16250 - 15912 == 338, "excess 338")
    check(failures, 2 * (0 - 2 + 1) == -2, "equalization decrease")
    # Integer vectors that are not the equality case.
    spread = [1] * 25 + [2, 0] + [0] * 25
    # sum = 25 + 2 = 27, fix: 24 ones, one 2, one 0, and 26 zeros is 52? 
    # 24 ones + one 2 + 27 zeros = 52 vertices, sum = 26, square sum = 24 + 4 = 28.
    spread = [1] * 24 + [2] + [0] * 27
    check(failures, len(spread) == 52 and sum(spread) == 26, "spread shape")
    check(failures, sum(x * x for x in spread) == 28, "spread squares")
    balanced = [1] * 26 + [0] * 26
    check(failures, sum(balanced) == 26 and sum(x * x for x in balanced) == 26, "balanced squares")

    for name, out in (("transitive52", transitive_52()), ("random52-seed20261023", random_52(20261023))):
        assert_tournament(failures, out, name)
        sum_d, sum_c, indeg = score_and_pair_sum(out)
        check(failures, sum_d == sum_c, f"{name}: pair sum identity {sum_d} != {sum_c}")
        e = [d - 25 for d in indeg]
        check(failures, sum(e) == 26, f"{name}: sum e")
        predicted = 16237 + sum(x * x for x in e) // 2
        check(failures, sum_d == predicted, f"{name}: closed form {sum_d} != {predicted}")
        check(failures, sum_d >= 16250, f"{name}: lower bound")
    return {"lower_bound": 16250, "excess_over_12": 338}


def check_lemma_i(failures: list[str]) -> None:
    for n in range(13, 81):
        for j in range(0, 11):
            outs = n - 33 - j
            misses = (n - 13) - outs
            check(failures, misses == 20 + j, f"I1 N={n} j={j}")
        # J = 0 algebra of the excess
        excess = 11 * n - 363 - 5 * (n - 13)
        check(failures, excess == 6 * n - 298, f"I2 N={n}")
    check(failures, 6 * 51 - 298 == 8, "N=51 excess constant")
    check(failures, 6 * 52 - 298 == 14, "N=52 excess constant")


def check_document_arithmetic(failures: list[str]) -> None:
    """Numbers printed in proof/F4_GE_52_HAND_PROOF.md section 6."""
    pairs = [
        (5 * 45, 225),
        (comb(11, 3), 165),
        (5 * 165, 825),
        (11 * comb(5, 3), 110),
        (11 * 27, 297),
        (23 * 13, 299),
        (24 * 49, 1176),
        (50 * 11, 550),
        (1176 - 550, 626),
        (24 * 25 - 2, 598),
        (51 * comb(25, 2), 15300),
        (12 * comb(51, 2), 15300),
        (comb(51, 3), 20825),
        (comb(51, 3) - 15300, 5525),
        (comb(25, 3), 2300),
        (25 * comb(12, 2), 1650),
        (51 * 1650, 84150),
        (51 * 650, 33150),
        (comb(51, 2) * comb(12, 3), 280500),
        (7650 * 25, 191250),
        (15 * 5525, 82875),
        (191250 + 82875, 274125),
        (280500 - 274125, 6375),
        (comb(5, 3) - comb(6, 3), -10),
        (comb(7, 3) - comb(5, 3), 25),
    ]
    for got, expect in pairs:
        check(failures, got == expect, f"document arithmetic {got} != {expect}")
    # (R2) substitution: 60 + 20*alpha + 12*beta - 450 with alpha = 20+j-beta-gamma
    for j, beta, gamma in itertools.product(range(0, 4), range(0, 4), range(0, 3)):
        alpha = 20 + j - beta - gamma
        raw = 60 + 20 * alpha + 12 * beta - 450
        closed = 10 + 20 * j - 8 * beta - 20 * gamma
        check(failures, raw == closed, f"R2 j={j} beta={beta} gamma={gamma}")
        lower = 10 - 4 * beta
        # The paper then adds 4*N4 outside this identity. The difference without N4:
        diff = closed - lower
        check(failures, diff == 20 * j - 4 * beta - 20 * gamma, f"rounding diff {j}")


def check_paley(failures: list[str]) -> dict:
    expected = {
        7: [7, 3, 1, 0],
        19: [19, 9, 4, 1, 0],
        67: [67, 33, 16, 6, 1],
    }
    # max set size recorded. Order 67 stops at 4. Smaller orders too.
    orders = [7, 11, 19, 23, 31, 43, 47, 67]
    out_data = {}
    candidates = []
    for p in orders:
        print(f"paley {p}", file=sys.stderr, flush=True)
        out = paley_out(p)
        assert_tournament(failures, out, f"QR_{p}")
        inn = in_neighbourhoods(out)
        degrees = {bits.bit_count() for bits in inn}
        check(failures, degrees == {(p - 1) // 2}, f"QR_{p} not regular: {degrees}")
        max_s = 4 if p >= 19 else 3
        prof = profile(out, max_s)
        # Fill s=0 which profile() includes.
        if p in expected:
            got = prof["min"]
            exp = expected[p]
            check(failures, got[: len(exp)] == exp, f"QR_{p} profile {got} != {exp}")
        witness = prof["witness"][3] if len(prof["witness"]) > 3 else []
        if witness:
            again = recompute_dominators(out, witness)
            check(failures, again == prof["min"][3], f"QR_{p} witness recompute")
        record = {
            "min_dominators_by_set_size": prof["min"],
            "witness_for_minimum_triple": witness,
            "has_S4": prof["min"][4] >= 1 if len(prof["min"]) > 4 else None,
        }
        out_data[str(p)] = record
        if p <= 51 and prof["min"][3] >= 5:
            candidates.append({"order": p, "witness": witness, "min_triple_dominators": prof["min"][3], "min_4": prof["min"][4] if len(prof["min"]) > 4 else None})
    return {"profiles": out_data, "strong_claim_paley_candidates": candidates}


def run_checks() -> dict:
    t0 = time.perf_counter()
    failures: list[str] = []
    try:
        lemma_s1 = check_lemma_s1(failures)
        check_lemma_i(failures)
        check_document_arithmetic(failures)
        paley = check_paley(failures)
    except Exception as exc:  # noqa: BLE001 — report the crash as a failed check
        failures.append(f"exception: {type(exc).__name__}: {exc}")
        lemma_s1 = {}
        paley = {}
    runtime = round(time.perf_counter() - t0, 3)
    candidates = paley.get("strong_claim_paley_candidates", []) if paley else []
    profiles = (paley or {}).get("profiles") or {}
    qr47 = profiles.get("47")
    finite = None
    if qr47 is not None:
        mins = qr47["min_dominators_by_set_size"]
        finite = {
            "statement": (
                "In the Paley tournament of order 47 the minimum of |D(Y)| over triples Y is 4, "
                "attained, and the minimum over 4-sets is 0. The sentence 'every tournament on "
                "at most 51 vertices has a triple with at most 3 dominators' is therefore false. "
                "The strong claim with 4 in place of 3 survives this example, and this tournament does not have S_4."
            ),
            "min_dominators_by_set_size": mins,
            "witness_triple": qr47["witness_for_minimum_triple"],
        }
        check(failures, mins[3] == 4 and mins[4] == 0, f"QR_47 unexpected profile {mins}")
    claim = (
        "Lemma S1 and Lemma I match the arithmetic in LEMMAS.md, the printed "
        "numbers in F4_GE_52 section 6 match, and the Paley profiles of orders "
        "7, 19 and 67 match the profiles previously computed by proof/verify_proof.py."
    )
    if finite is not None and not failures:
        claim += " " + finite["statement"]
    if candidates:
        claim += " A Paley tournament on at most 51 vertices has every triple dominated at least five times."
    return {
        "ok": not failures,
        "claim": claim,
        "failures": failures,
        "lemma_s1": lemma_s1,
        "paley": paley,
        "counterexample_candidate": candidates[0] if candidates else None,
        "finite_theorem": finite,
        "runtime_seconds": runtime,
        "coverage": (
            "All Paley tournaments of orders 7, 11, 19, 23, 31, 43, 47 and 67 "
            "were scanned exactly. This is not a search over all tournaments of those orders. "
            "Orders below 47 cannot meet the triple condition for S_4, by the Szekeres bound, "
            "so a Paley counterexample to the strong claim would have to be order 47."
        ),
    }


def main() -> int:
    report = run_checks()
    json.dump(report, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
