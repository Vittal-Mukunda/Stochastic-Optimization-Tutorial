"""Plain-Python S_4 checker written from the definition (no bit tricks).
Usage: python check_a.py MATRIX_FILE   (N lines of N chars 0/1; A[w][x]=1 iff w->x)"""
import sys
from itertools import combinations


def load(path):
    rows = [ln.strip() for ln in open(path) if ln.strip() and not ln.startswith("#")]
    return [[int(c) for c in r] for r in rows]


def check(A):
    N = len(A)
    assert all(len(r) == N for r in A), "matrix not square"
    for i in range(N):
        assert A[i][i] == 0, f"A[{i}][{i}] != 0"
        for j in range(N):
            if i != j:
                assert A[i][j] + A[j][i] == 1, f"pair ({i},{j}) not a tournament arc"
    checked = 0
    undominated = []
    for X in combinations(range(N), 4):
        checked += 1
        ok = False
        for w in range(N):
            if w in X:
                continue
            if all(A[w][x] == 1 for x in X):
                ok = True
                break
        if not ok:
            undominated.append(X)
    return N, checked, undominated


if __name__ == "__main__":
    N, checked, und = check(load(sys.argv[1]))
    print(f"checker_a: N={N} tournament=OK 4-sets checked={checked} undominated={len(und)}"
          + (f" first={und[0]}" if und else ""))
    print("checker_a: S_4 " + ("HOLDS" if not und else "FAILS"))
