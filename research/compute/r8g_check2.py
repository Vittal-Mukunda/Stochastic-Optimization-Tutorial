"""R8-G second, independent S_4 checker (pure Python integers, no numpy, no shared code).

Reads a tournament as 0/1 adjacency rows (row w, column x is 1 iff w -> x; lines
starting with '#' are ignored), or builds a Paley tournament with --paley p.
For each 4-set {a,b,c,d} it scans dominators via Python-int bitmasks of
out-neighbourhoods taken from the rows directly (bit w of beats_all[x] set iff
row w has a 1 in column x).

Usage: python r8g_check2.py FILE      or      python r8g_check2.py --paley 67
"""
import sys
from itertools import combinations


def read_rows(path):
    rows = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            s = line.strip()
            if s and not s.startswith("#"):
                rows.append(s)
    return rows


def paley_rows(p):
    qr = set()
    for x in range(1, p):
        qr.add(x * x % p)
    return ["".join("1" if (i != j and (j - i) % p in qr) else "0" for j in range(p))
            for i in range(p)]


def check(rows):
    n = len(rows)
    for i in range(n):
        assert len(rows[i]) == n and rows[i][i] == "0", "bad row %d" % i
        for j in range(i + 1, n):
            assert (rows[i][j] == "1") != (rows[j][i] == "1"), "not a tournament at %d,%d" % (i, j)
    # beaten_by[x] = set of w with w -> x, as an int bitmask
    beaten_by = [0] * n
    for w in range(n):
        for x in range(n):
            if rows[w][x] == "1":
                beaten_by[x] |= 1 << w
    minp = min(bin(beaten_by[a] & beaten_by[b]).count("1") for a, b in combinations(range(n), 2))
    mint = min(bin(beaten_by[a] & beaten_by[b] & beaten_by[c]).count("1")
               for a, b, c in combinations(range(n), 3))
    bad = 0
    first = None
    for a, b, c, d in combinations(range(n), 4):
        if beaten_by[a] & beaten_by[b] & beaten_by[c] & beaten_by[d] == 0:
            bad += 1
            if first is None:
                first = (a, b, c, d)
    return {"n": n, "undominated_4sets": bad, "first_undominated": first,
            "min_pair_dom": minp, "min_triple_dom": mint, "S4": bad == 0}


if __name__ == "__main__":
    if sys.argv[1] == "--paley":
        print(check(paley_rows(int(sys.argv[2]))))
    else:
        print(check(read_rows(sys.argv[1])))
