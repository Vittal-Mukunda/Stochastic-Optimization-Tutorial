"""Check Claude's DRT pair-link counting on the Paley tournaments QR_7 and QR_19.

The identity claimed for a doubly regular tournament of order 4t+3 is, for every
pair and X its set of t common in-neighbours:

    sum(in_X(x)^2) + sum(c_u^2) = constant depending only on t.

This script derives that constant the same way and checks it on every pair.
"""

from __future__ import annotations

import itertools


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    return all(n % d for d in range(2, int(n**0.5) + 1))


def paley_beats(order: int) -> list[set[int]]:
    squares = {pow(a, 2, order) for a in range(1, order)}
    return [{(i + s) % order for s in squares} for i in range(order)]


def check(order: int) -> None:
    assert order % 4 == 3 and is_prime(order)
    t = (order - 3) // 4
    beats = paley_beats(order)
    degree = len(beats[0])
    assert degree == 2 * t + 1
    # Closed form from the column-sum / Gram count in the debate.
    # |X| = t, sum of in-degrees in X is C(t, 2), each column sum is t + in_X.
    # sum c = t^2 + C(t, 2)
    # sum c^2 = sum c + 2 * (C(t, 2) * t - sum_y C(in_X(y), 2))
    #         = [that] which simplifies to CONST - sum in^2.
    edges = t * (t - 1) // 2
    sum_c = t * t + edges
    # From the same algebra as the n=51 case:
    # sum c^2 = sum_c + 2 * (edges * (t - 2) - sum C(in, 2))? Wait, recompute generally below
    # and compare to a derived constant.
    mismatches = 0
    constants = set()
    for a, b in itertools.combinations(range(order), 2):
        common_in = [x for x in range(order) if a in beats[x] and b in beats[x]]
        if len(common_in) != t:
            raise SystemExit(f"QR_{order}: pair {(a, b)} has {len(common_in)} common in-neighbours, expected {t}")
        xset = set(common_in)
        yset = [u for u in range(order) if u not in xset and u != a and u != b]
        in_x = []
        for x in common_in:
            in_x.append(sum(1 for z in common_in if z != x and x in beats[z]))
        c = []
        for u in yset:
            c.append(sum(1 for x in common_in if u in beats[x]))
        # r_x should equal t + in_X(x)
        for x, inn in zip(common_in, in_x):
            beaten_in_y = sum(1 for u in yset if u in beats[x])
            if beaten_in_y != t + inn:
                mismatches += 1
        total = sum(v * v for v in in_x) + sum(v * v for v in c)
        constants.add(total)
        if sum(c) != sum_c:
            mismatches += 1
    print(
        f"QR_{order}: t={t}, pairs={order * (order - 1) // 2}, "
        f"sum_c expected {sum_c}, identity constants {sorted(constants)}, mismatches {mismatches}"
    )


if __name__ == "__main__":
    check(7)
    check(19)
