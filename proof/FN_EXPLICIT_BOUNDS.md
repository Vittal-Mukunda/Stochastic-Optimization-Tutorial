# An explicit estimate of f(n) for every n ≥ 4

*Hand derivation, 20 October 2026. No computation. The lower bound is Theorem B of `ERDOS902_PROOF.md`, improved at n = 4 by `F4_GE_52_HAND_PROOF.md`. The upper bound below is elementary and holds for every n ≥ 4.*

## 0. What is being estimated

f(n) is the least number of vertices in a tournament in which every set of n vertices is dominated by some vertex outside it. The values f(1) = 3, f(2) = 7 and f(3) = 19 are classical. There is no proved formula that pins f(n) to a single expression for n ≥ 4. The estimate that the counting allows is the following.

**Theorem.** For every integer n ≥ 4,

  (n + 5/2)·2^(n−1) − 1 ≤ f(n) ≤ 2·n²·2^n.

More sharply, f(4) ≤ 67, and f(n) ≤ n²·2^n for every n ≥ 16. Also f(4) ≥ 52, which is one larger than the general lower bound at n = 4.

The two sides differ by a factor of about n. Sections 2 and 3 say why the usual dominator-count does not remove that factor.

## 1. The upper bound

**Lemma.** ln 2 < 7/10.

*Proof.* The series ln 2 = Σ_{k≥1} 1/(k·2^k) comes from integrating Σ_{j≥0} x^j = 1/(1−x) on [0, 1/2]. The sum of the first six terms is

  1/2 + 1/8 + 1/24 + 1/64 + 1/160 + 1/384 = 1327/1920,

and 7/10 − 1327/1920 = 17/1920. The remainder is smaller than the geometric tail starting at the seventh term, divided by 7:

  Σ_{k≥7} 1/(k·2^k) < (1/7)·Σ_{k≥7} 2^(−k) = 1/(7·2^6) = 1/448.

Since 17·448 = 7616 > 1920, one has 17/1920 > 1/448, so the remainder is strictly smaller than 17/1920. ∎

**Proposition.** f(n) ≤ 2·n²·2^n for every n ≥ 1. For every n ≥ 16 the same argument with a smaller target gives f(n) ≤ n²·2^n.

*Proof.* Let N = c·n²·2^n with c = 2, or with c = 1 when n ≥ 16. In a random tournament the expected number of undominated n-sets is

  C(N, n)·(1 − 2^(−n))^(N−n).

The integral comparison Σ_{k=2}^n ln k ≥ ∫_1^n ln x dx = n ln n − n + 1 gives n! ≥ e·(n/e)^n, so C(N, n) < (eN/n)^n. Also 1 − x ≤ e^(−x), so the second factor is at most exp(−(N−n)2^(−n)). The product is therefore smaller than 1 as soon as

  n·ln(eN/n) < (N − n)·2^(−n).

For c = 2 one has eN/n = 2e·n·2^n, and the difference between the two sides is

  n²(2 − ln 2) − n ln n − n(1 + ln 2) − n·2^(−n).

By the lemma this is larger than (13/10)n² − n ln n − (17/10)n − 1. For n ≥ 1 one has ln n < (7/10)n, so the expression is larger than (3/5)n² − (17/10)n − 1. At n = 4 this is 96/10 − 68/10 − 1 = 18/10 > 0, and its derivative 6n/5 − 17/10 is positive for n ≥ 2. Thus the expectation is less than 1, and some tournament on N vertices has no undominated n-set.

For c = 1 and n ≥ 16 the same difference is n²(1 − ln 2) − n ln n − n − n·2^(−n). It is larger than (3/10)n² − n ln n − n − 1, because ln 2 < 7/10 and n·2^(−n) < 1. Here ln n = ln(16·n/16) and, at the bottom of the range, ln 16 = 4 ln 2 < 14/5, so the value at n = 16 is larger than (3/10)·256 − 16·(14/5) − 16 − 1 = 15. The derivative (3/5)n − ln n − 2 is positive at n = 16 and increases, so the difference stays positive. ∎

The Paley tournament on 67 vertices shows the sharper inequality f(4) ≤ 67. The constant 2 in the general upper bound is only a convenient explicit value; Erdős’s original count gives the leading factor ln 2 instead of 2, for all large n.

## 2. The lower bound, and where it stops

Theorem B of `ERDOS902_PROOF.md` is the inequality f(n) ≥ (n + 5/2)·2^(n−1) − 1 for n ≥ 4. It is one step past Szekeres–Szekeres. If some (n−2)-set had only 2n+3 dominators, the cross-level count with k = n−1 would force more than (2n+5)·2^(n−2) vertices. If every (n−2)-set has at least 2n+4 dominators, ordinary doubling from ν_{n−1} ≥ n+1 gives the same number. At n = 4 that dichotomy is too weak, and the separate argument gives f(4) ≥ 52.

Iterating the same count at every level replaces the coefficient 1/2 by the constant c* of Theorem C,

  c* = lim a_j/2^j ≈ 0.7695,

where a_1 = 1 and Φ(a_j, a_{j−1}) = ln 2, with Φ the integral in §5 of that note. The limit exists because 2a_{j−1} < a_j < 2a_{j−1} + 1, so each level contributes about half an extra vertex, on the scale of n, before the set is doubled.

**Saturation.** This count cannot force a lower bound of order n²·2^n. Two comparisons:

* Against the upper bound of §1, ln(n²·2^n)/n = ln 2 + 2(ln n)/n. The extra term tends to 0, so the equation that defines a_j is unchanged: the integral Φ is still being compared with ln 2. The largest liminf the iteration yields is still c*.
* The vertices inside D(A) contribute the second summand of Lemma 3.1. Relative to the outside summand that term is O(2^(−n)) once |D(A)| and its successor dominator-number are both proportional to n and N is proportional to n·2^n. It does not move the limit.

So (c* − o(1))·n·2^n ≤ f(n) ≤ 2·n²·2^n is the estimate these identities give, for every n ≥ 4. Closing the factor n needs a different count.
