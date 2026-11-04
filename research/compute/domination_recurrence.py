"""Finite check of the tournament recurrence gamma = 1 + min gamma(in-neighbourhood).

gamma is the domination number: a set D dominates when every vertex outside D
is beaten by some vertex of D. The empty tournament has gamma 0.
"""

from __future__ import annotations

import json
from pathlib import Path


def pair_index(i: int, j: int) -> int:
    if i > j:
        i, j = j, i
    return j * (j - 1) // 2 + i


def beats(bits: int, i: int, j: int) -> bool:
    if i < j:
        return (bits >> pair_index(i, j)) & 1 == 1
    return not beats(bits, j, i)


def gamma(n: int, bits: int) -> int:
    if n == 0:
        return 0
    best = n
    for mask in range(1 << n):
        size = mask.bit_count()
        if size >= best:
            continue
        good = True
        for v in range(n):
            if (mask >> v) & 1:
                continue
            if not any((mask >> u) & 1 and beats(bits, u, v) for u in range(n)):
                good = False
                break
        if good:
            best = size
    return best


def induced_in(n: int, bits: int, v: int) -> tuple[int, int]:
    verts = [u for u in range(n) if beats(bits, u, v)]
    m = len(verts)
    out = 0
    for a in range(m):
        for b in range(a + 1, m):
            if beats(bits, verts[a], verts[b]):
                out |= 1 << pair_index(a, b)
    return m, out


def main():
    checked = 0
    mismatches = []
    for n in range(0, 7):
        for bits in range(1 << (n * (n - 1) // 2)):
            g = gamma(n, bits)
            if n == 0:
                checked += 1
                continue
            values = [gamma(*induced_in(n, bits, v)) for v in range(n)]
            checked += 1
            if g != 1 + min(values):
                mismatches.append({"n": n, "bits": bits, "gamma": g, "in": values})
                if len(mismatches) >= 5:
                    break
        if mismatches:
            break
    payload = {"checked": checked, "mismatches": mismatches, "max_order": 6}
    Path(__file__).with_name("domination_recurrence_result.json").write_text(
        json.dumps(payload) + "\n", encoding="utf-8"
    )
    print(payload)
    if mismatches:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
