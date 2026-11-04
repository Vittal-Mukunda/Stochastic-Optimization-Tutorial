"""Identity check for the arc count in Corollary 3.

For a vertex v and A = N^-(v), the sets D_z = A intersect N^-(z) for z != v
satisfy sum_z |D_z| = sum_{x in A} d^+(x). On 51 vertices, d^+ = 50 - d^-.
"""

from __future__ import annotations

import json
import random
from pathlib import Path


def tournament(n: int, rng: random.Random):
    beats = [[False] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if rng.randrange(2):
                beats[i][j] = True
            else:
                beats[j][i] = True
    return beats


def check(beats):
    n = len(beats)
    gaps = []
    for v in range(n):
        indeg = [sum(beats[y][x] for y in range(n)) for x in range(n)]
        A = [x for x in range(n) if beats[x][v]]
        total = 0
        for z in range(n):
            if z == v:
                continue
            total += sum(1 for x in A if beats[x][z])
        by_out = sum((n - 1) - indeg[x] for x in A)
        by_printed = sum((n - 2) - indeg[x] for x in A)
        gaps.append(by_out - total)
        if total != by_printed or by_out - total != len(A):
            return None
    return gaps


def main():
    rng = random.Random(20261023)
    runs = []
    ok = True
    for n, samples in ((7, 20), (51, 5)):
        gaps = []
        for _ in range(samples):
            found = check(tournament(n, rng))
            if found is None:
                ok = False
                break
            gaps.extend(found)
        runs.append({
            "n": n,
            "samples": samples,
            "min_gap_versus_printed": min(gaps) if gaps else None,
            "max_gap_versus_printed": max(gaps) if gaps else None,
        })
    payload = {
        "ok": ok,
        "runs": runs,
        "claim": "Each x in N^-(v) spends one out-arc on v, so sum_z |D_z| = sum_x (d^+(x)-1) = sum_x ((n-2)-d^-(x)). On 51 vertices this is the printed 49-count.",
    }
    Path(__file__).with_name("corollary3_count_result.json").write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload))
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
