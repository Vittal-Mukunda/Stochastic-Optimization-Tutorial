# Lower bounds for Schütte's tournament problem (Erdős Problem #902): complete proofs

*Assembled on 18 October 2026 from everything in this folder: `schutte_902_results.zip`, `schutte_902_all_work.zip`, the debate
transcripts and `ai-debate/`. Every step below was re-derived by hand. Every inequality and every lemma that can be tested
on a real tournament is checked by `proof/verify_proof.py`. Its output is in `proof/verify_proof.out`.*

---

## 0. The problem and what is proved

A **tournament** T has vertex set V, with |V| = N. Each pair of vertices is joined by exactly one arc, and u → v means u beats v.
T has **property S_n** if every set of n vertices is beaten by a single vertex outside the set.
**f(n)** is the least N for which a tournament with S_n exists. Erdős Problem #902 (a question of Schütte) asks for an estimate of f(n).

**Known before this work.**
* f(1) = 3, f(2) = 7 and f(3) = 19 (Szekeres–Szekeres 1965).
* (n + 2)·2^(n−1) − 1 ≤ f(n). This is due to Szekeres–Szekeres (1965).
* f(n) ≤ (ln 2 + o(1))·n²·2^n. This is due to Erdős (1963), by a random tournament.
* 48 ≤ f(4) ≤ 67. The lower bound is Reid–McRae–Hedetniemi–Hedetniemi (2004). The upper bound is the Paley tournament QR_67.
* f(4) ≥ 49 was posted by J. Wilder (GitHub, September 2026) as a computer-assisted candidate.

**Proved here.**

| | statement | type of proof | section |
|---|---|---|---|
| **Theorem A** | **f(4) ≥ 51** | by hand | §2 |
| **Theorem B** | f(n) ≥ (n + 5/2)·2^(n−1) − 1 for every n ≥ 4 | by hand | §4 |
| **Theorem C** | f(n) ≥ (c\* − o(1))·n·2^n, where c\* = 0.76950 32191 50489 43269 90652 68309 82313 46767… | by hand | §5 |
| **Theorem D** | f(5) ≥ 121, f(6) ≥ 281, f(7) ≥ 665, f(8) ≥ 1485, f(9) ≥ 3388, f(10) ≥ 7398, f(11) ≥ 16569, f(12) ≥ 35655 | an explicit recursion, run in exact integers | §6 |

Theorem C raises the leading constant of the lower bound from 1/2 (Szekeres) to about 0.7695. Theorem B is the explicit,
all-n form. It beats Szekeres by 2^(n−2) for every n ≥ 4. In particular the Szekeres bound is never attained for n ≥ 4.

**Not proved.**
* The order of magnitude of f(n), which is still between n·2^n and n²·2^n.
* f(4) ≥ 52. **Update, 20 October 2026: now proved by hand in `F4_GE_52_HAND_PROOF.md`.** That file settles every
  open item of §8.1 without a computer: the local claim (all classes), minimum in-degree ≥ 24, case (I), case (R),
  and "no DRT(51) has S_4".

§8 records exactly where the case N = 51 stands. It includes one proposed reduction, Claim L, that this check shows to be **false**.

**Where the proofs come from.**
* Theorem A is the f4 agent's round-4 "clean proof".
* Theorem B is the verifier agent's argument.
* Theorem C and the cross-level lemma are from round 2. The lemma's sharpened form is from round 3.

This document adds the following:
* A rigorous version of the asymptotic step of Theorem C. Lemmas 5.1–5.3 replace the earlier "−O(1)" estimate.
* A proof of the key inequality of Theorem B for every n ≥ 5. Earlier it had only been checked numerically up to n = 400.
* A uniform statement of the basic lemmas.
* An independent re-implementation of every check.

---

## 1. Notation and three basic lemmas

N⁺(v) and N⁻(v) are the out- and in-neighbourhoods of v, and d⁺(v), d⁻(v) are their sizes. T[Y] is the subtournament induced on Y.
For X ⊆ V, the **dominators** of X are

  D(X) = { w ∈ V \ X : w → x for every x ∈ X }.

So D(∅) = V and D({v}) = N⁻(v). X is *dominated* if D(X) ≠ ∅. For 0 ≤ s ≤ n put ν_s = min{ |D(X)| : |X| = s }.
C(x, k) is the binomial coefficient, with C(x, k) = 0 when x < k.

**Lemma 1.1.** If T has S_n, every set of at most n vertices is dominated. Also D(X′) ⊆ D(X) when X ⊆ X′, so ν_0 ≥ ν_1 ≥ … ≥ ν_n ≥ 1.

*Proof.* Some n-set has a dominator outside it, so N ≥ n + 1. Let |X| ≤ n. Extend X to an n-set X′. A dominator of X′ lies outside X′ ⊇ X and beats X.
The inclusion is immediate from the definition. ∎

**Lemma 1.2 (Szekeres).** Let T have S_n and |A| ≤ n − 1. Then D(A) is not dominated. Hence |D(A)| ≥ n + 1, that is, ν_{n−1} ≥ n + 1.

*Proof.* Suppose z beats every vertex of D(A). D(A) is non-empty (Lemma 1.1).
* Every vertex of D(A) beats every vertex of A, so z ∉ A.
* Also z ∉ D(A), since z cannot beat itself.
* So A ∪ {z} has at most n vertices and has a dominator w ∉ A ∪ {z} (Lemma 1.1).
* Then w beats A and w ∉ A, so w ∈ D(A). Hence z → w. This contradicts w → z.

So D(A) is undominated. By Lemma 1.1 it has more than n vertices. ∎

**Lemma 1.3.** Let T have S_n. Let |A| = s ≤ n − 1 and R = D(A). For every y ∉ A,

  **D(A ∪ {y}) = R ∩ N⁻(y).**  (1)

So |R ∩ N⁻(y)| ≥ ν_{s+1}. This holds whether y lies inside R or outside it.

Consequences:
* T[R] has minimum in-degree at least ν_{s+1}.
* Every y ∉ A ∪ R beats at most |R| − ν_{s+1} vertices of R.
* **|R| ≥ 2ν_{s+1} + 1.**

More generally, a tournament whose minimum in-degree is at least δ has at least 2δ + 1 vertices. If it has exactly 2δ + 1 vertices,
it is regular, with every in-degree and out-degree equal to δ.

*Proof.* A vertex w lies in D(A ∪ {y}) exactly when w ∉ A ∪ {y}, w beats A, and w beats y. That means w ∈ R \ {y} and w ∈ N⁻(y).
Since y ∉ N⁻(y), this is R ∩ N⁻(y). Its size is at least ν_{s+1}, because |A ∪ {y}| = s + 1 ≤ n.

For the general statement, let a tournament on m vertices have every in-degree at least δ. The in-degrees sum to C(m, 2), so
C(m, 2) ≥ mδ, that is, m ≥ 2δ + 1. If m = 2δ + 1, then C(m, 2) = mδ, so every in-degree equals δ. ∎

Iterating Lemma 1.3 gives ν_s + 1 ≥ 2(ν_{s+1} + 1), so

  N + 1 = ν_0 + 1 ≥ 2^(n−j)·(ν_{n−j} + 1)  for every 0 ≤ j ≤ n.  (2)

With j = 1 and Lemma 1.2 this is the Szekeres bound N ≥ (n + 2)·2^(n−1) − 1.

**The case n = 4.** Let T have S_4.
* **(F1)** Every triple Y has |D(Y)| ≥ 5, and D(Y) is undominated (Lemma 1.2).
* **(F2)** For every pair P, T[D(P)] has minimum in-degree ≥ 5. So |D(P)| ≥ 11. Every y ∉ P ∪ D(P) is beaten by ≥ 5 vertices of D(P) (Lemma 1.3 with s = 2).
* **(F3)** For every vertex v, T[N⁻(v)] has minimum in-degree ≥ 11. So d⁻(v) ≥ 23 (Lemma 1.3 with s = 1).

A pair P is **tight** if |D(P)| = 11. Then T[D(P)] has 11 = 2·5 + 1 vertices and minimum in-degree ≥ 5, so it is 5-regular (Lemma 1.3).

One fact is used repeatedly. For a ∈ N⁻(v), (1) with A = {v} gives D({a, v}) = N⁻(v) ∩ N⁻(a). So **the in-degree of a inside T[N⁻(v)] equals |D({a, v})|**.

---

## 2. Theorem A: f(4) ≥ 51

Throughout this section T has S_4 and N vertices.

**Lemma 2.1 (Lemma T).** If P is a tight pair, every r ∈ D(P) has d⁻(r) ≥ 25. This holds for every N.

*Proof.* Let R = D(P), so |R| = 11 and T[R] is 5-regular. Fix r ∈ R. There are C(10, 2) = 45 triples U ⊆ R that contain r.
Count the pairs (U, w) with w ∈ D(U). By (F1) there are at least 5·45 = 225.

Every such w beats r. Also w ∉ P, because r ∈ D(P) beats both vertices of P. So w ∈ N⁻(r). There are two kinds of w:
* **w ∈ R.** Exactly 5 vertices of R beat r. Such a w dominates U only if U ⊆ N⁺(w) ∩ R, which is a 5-set containing r.
  So w dominates at most C(4, 2) = 6 of the 45 triples.
* **w ∉ R.** None of these w lies in P, so there are exactly d⁻(r) − 5 of them. By (F2) each is beaten by at least 5 vertices of R.
  So it beats at most 6 vertices of R, one of which is r. It dominates at most C(5, 2) = 10 of the triples.

Hence 225 ≤ 5·6 + 10·(d⁻(r) − 5), so d⁻(r) ≥ 24.5. ∎

**Lemma 2.2.** If some vertex has in-degree 23, then N ≥ 51.

*Proof.* Let d⁻(v) = 23, A = N⁻(v) and B = N⁺(v), so |B| = N − 24.

*Every pair {a, v} with a ∈ A is tight.* The in-degree of a ∈ A inside T[A] is |D({a, v})| ≥ 11, by (F2). These in-degrees sum to
C(23, 2) = 253 = 23·11. So each equals 11, and T[A] is 11-regular.

*Every a′ ∈ A has d⁻(a′) ≥ 25.* The vertex a′ has 11 out-neighbours in A. Pick one, a. Then a′ ∈ A ∩ N⁻(a) = D({a, v}), which is the
dominator set of a tight pair. Apply Lemma 2.1.

*Double count the arcs from A to B.*
* For b ∈ B, the vertices of A that beat b form A ∩ N⁻(b) = D({v, b}). This set has at least 11 elements by (F2), so there are at least 11(N − 24) arcs.
* Each a ∈ A beats v and 11 vertices of A, and d⁺(a) = N − 1 − d⁻(a) ≤ N − 26. So a beats at most N − 38 vertices of B, and there are at most 23(N − 38) arcs.

Therefore 11(N − 24) ≤ 23(N − 38), which gives 12N ≥ 610 and N ≥ 51. ∎

**Lemma 2.3 (Claim Q).** Let Z = { v : d⁻(v) = 24 }. Every v ∈ Z has at most 2 in-neighbours in Z. Consequently |Z| ≤ 5.

*Proof.* Fix v ∈ Z. Let A = N⁻(v), which has 24 vertices, and Z_v = A ∩ Z. For x ∈ A, write the in-degree of x inside T[A] as
|D({x, v})| = 11 + f_x, with f_x ≥ 0 by (F2). These in-degrees sum to C(24, 2) = 276 = 24·11 + 12, so **Σ_x f_x = 12**.
Let L = { x ∈ A : f_x = 0 } and ℓ = |L|. At most 12 vertices have f_x ≥ 1, so ℓ ≥ 12.

*(a)* For a ∈ L the pair {a, v} is tight, with dominator set A ∩ N⁻(a). By Lemma 2.1 every in-neighbour of a inside A has in-degree
≥ 25, so none of them lies in Z. Hence **a beats every vertex of Z_v \ {a}**. Two vertices of L ∩ Z would each beat the other, so |L ∩ Z| ≤ 1.

*(b)* Let Q = Z_v \ L and q = |Q|. By (a), every z ∈ Q is beaten by all ℓ vertices of L. It is also beaten by its in-neighbours in T[Q].
So 11 + f_z ≥ ℓ + d⁻_{T[Q]}(z). Sum this over Q, and use f ≥ 1 on the other 24 − ℓ − q vertices of A \ L:

  12 = Σ f ≥ q(ℓ − 11) + C(q, 2) + (24 − ℓ − q),  that is,  (q − 1)(ℓ − 12) + C(q, 2) ≤ 0.

Because ℓ ≥ 12, every q ≥ 2 makes the left side at least 1. So q ≤ 1, and |Z_v| = |L ∩ Z| + q ≤ 2.

Finally, every in-degree of T[Z] is at most 2. So C(|Z|, 2) ≤ 2|Z|, which gives |Z| ≤ 5. ∎

**Theorem A.** No tournament with at most 50 vertices has S_4. Hence **f(4) ≥ 51**.

*Proof.* Let T have S_4 with N ≤ 50.
1. By (F3) every in-degree is at least 23. By Lemma 2.2 none equals 23. So every in-degree is at least 24.
2. Then C(N, 2) ≥ 24N, so N ≥ 49.
3. The excess is Σ_v (d⁻(v) − 24) = C(N, 2) − 24N = N(N − 49)/2. This is 0 for N = 49 and 25 for N = 50.
4. Every vertex outside Z contributes at least 1 to the excess. So |Z| ≥ 49 for N = 49, and |Z| ≥ 25 for N = 50.
5. This contradicts |Z| ≤ 5 (Lemma 2.3). ∎

*Remarks.*
1. Property S_4 enters the proof only through (F1)–(F3). Everything else is counting.
2. At N = 51 the average in-degree is exactly 25, so Z may be empty, and the argument stops exactly there (§8).
3. The same count works for S_k. Take a (k − 2)-set with exactly 2k + 3 dominators. The count gives a threshold for the in-degree of each dominator: 3 for k = 2, 9 for k = 3, 25 for k = 4.
   * For k ≤ 3 the threshold adds nothing to (2).
   * QR_7 and QR_19 attain it with equality at every dominator, and they make the incidence identity behind the count exact.
   * Check V2 tests this. It is a test of the counting, not extra evidence for k = 4.
   * Neither available S_4 example has a tight pair, so at k = 4 Lemma 2.1 rests on its proof alone.

---

## 3. The cross-level lemma

**Lemma 3.1.** Let T have S_n. Let A be an s-set with 0 ≤ s ≤ n − 1, R = D(A), m = |R|, and let h ≤ ν_{s+1}. Then for every 1 ≤ k ≤ n,

  ν_k·C(m, k) ≤ Σ_{y ∉ A} C(|N⁺(y) ∩ R|, k) ≤ (N − s − m)·C(m − h, k) + m·C(m − h − 1, k) ≤ (N − s)·C(m − h, k).

*Proof.* Count the pairs (U, y) in which U is a k-subset of R and y ∈ D(U).
* Each U has at least ν_k dominators, because k ≤ n. That gives the left inequality.
* A vertex y dominates U exactly when U ⊆ N⁺(y) ∩ R. So the count equals the middle sum.
* For y ∈ A the term is 0, because every vertex of R beats y.
* For y ∉ A, (1) gives N⁺(y) ∩ R = R \ ({y} ∪ D(A ∪ {y})), and |D(A ∪ {y})| ≥ h. So |N⁺(y) ∩ R| ≤ m − h − 1 if y ∈ R, and ≤ m − h otherwise.
* There are m vertices in R and N − s − m vertices outside A ∪ R. ∎

Lemma 2.1 is the same count made exact at n = 4, s = 2, k = 3, restricted to the triples through one fixed r.

---

## 4. Theorem B: f(n) ≥ (n + 5/2)·2^(n−1) − 1 for n ≥ 4

The right side equals (2n + 5)·2^(n−2) − 1. For n = 4 it is 51, which is Theorem A. Let n ≥ 5 and let T have S_n with N vertices.
Then ν_{n−1} ≥ n + 1 (Lemma 1.2) and ν_{n−2} ≥ 2n + 3 (Lemma 1.3).

**Case 1: some (n − 2)-set A has |D(A)| = 2n + 3.** Apply Lemma 3.1 with s = n − 2, m = 2n + 3, h = n + 1 and k = n − 1, using ν_{n−1} ≥ n + 1:

  (n + 1)·C(2n + 3, n − 1) ≤ (N − n + 2)·C(n + 2, n − 1) = (N − n + 2)·C(n + 2, 3).

*Claim.* Put Λ(n) = (n + 1)·C(2n + 3, n − 1)/C(n + 2, 3) and P(n) = (2n + 5)·2^(n−2). Then Λ(n) > P(n) for all n ≥ 5.

*Proof of the claim.*
* Base case: Λ(5) = 6·715/35 = 858/7 ≈ 122.6 > 120 = P(5).
* A direct computation gives Λ(n+1)/Λ(n) = 2(n + 2)²(2n + 5) / ((n + 1)(n + 3)(n + 5)).
* This ratio is at least 3 for n ≥ 5, because 2(n + 2)²(2n + 5) − 3(n + 1)(n + 3)(n + 5) = n³ − n² − 13n − 5. That is 30 at n = 5, and its derivative 3n² − 2n − 13 is positive for n ≥ 3.
* Meanwhile P(n+1)/P(n) = 2(2n + 7)/(2n + 5) < 3.
* Induction finishes the claim. ∎

So in Case 1, N − n + 2 ≥ Λ(n) > (2n + 5)·2^(n−2), and N > (2n + 5)·2^(n−2).

**Case 2: every (n − 2)-set has at least 2n + 4 dominators.** Then (2) with j = 2 gives N + 1 ≥ 2^(n−2)·(2n + 5).

In both cases N ≥ (2n + 5)·2^(n−2) − 1. ∎

*Remarks.*
* At n = 4 the Case 1 inequality is false: Λ(4) = 41.25 < 52 = P(4). So n = 4 really needs §2.
* At n = 3 the formula would give 21 > f(3) = 19. Indeed, in QR_19 every vertex has exactly 9 = 2·3 + 3 dominators.

---

## 5. Theorem C: f(n) ≥ (c\* − o(1))·n·2^n

For x ≥ 1 let F(x) = x ln x − (x − 1) ln(x − 1), with F(1) = 0. For a − b ≥ 1 and b ≥ 0 let

  Φ(a, b) = ∫₀¹ ln( (a − y)/(a − b − y) ) dy = F(a) − F(a − b).

The closed form uses ∫₀¹ ln(c − y) dy = F(c) − 1 for c ≥ 1. The integrand has only an integrable singularity when a − b = 1.

**Lemma 5.1.**
* F is continuous on [1, ∞), and F′(x) = ln(x/(x − 1)) is positive and strictly decreasing on (1, ∞).
* So on {a − b ≥ 1, b ≥ 0}, Φ is continuous, **strictly decreasing in a** and **strictly increasing in b**.

For b ≥ 1 it also satisfies:
* (i) Φ(b + 1, b) = F(b + 1) ≥ F(2) = 2 ln 2 > ln 2.
* (ii) Φ(2b, b) > ln 2 > Φ(2b + 1, b).
* (iii) Φ(a, b) → 0 as a → ∞.

*Proof.* ∂Φ/∂a = F′(a) − F′(a − b) < 0 and ∂Φ/∂b = F′(a − b) > 0. (i) holds because F is increasing.

(ii): First, Φ(2b, b) = ∫_b^{2b} −ln(1 − 1/x) dx > ∫_b^{2b} dx/x = ln 2. Second,
Φ(2b + 1, b) = ∫_{b+1}^{2b+1} ln(1 + 1/(x − 1)) dx < ∫_{b+1}^{2b+1} dx/(x − 1) = ln 2.

(iii): Φ(a, b) = ∫_{a−b}^{a} F′ ≤ b·F′(a − b) → 0. ∎

**Definition of a_j and c\*.** Put a_1 = 1. For j ≥ 2, let a_j be the unique a ≥ a_{j−1} + 1 with Φ(a, a_{j−1}) = ln 2.
It exists and is unique by (i), (iii), continuity and strict monotonicity in a. By (ii), **2a_{j−1} < a_j < 2a_{j−1} + 1**.

So a_j/2^j is strictly increasing, and a_j/2^j < a_{j−1}/2^(j−1) + 2^(−j). Hence it is bounded by 1, and

  c\* := lim_{j→∞} a_j/2^j = sup_j a_j/2^j = 0.76950 32191 50489 43269 90652 68309 82313 46767…  (check V5).

The first values are a_2 = 2.5622, a_3 = 5.6487, a_4 = 11.8085, a_5 = 24.1224 and a_6 = 48.7474.

**Lemma 5.2.** Let T have S_n on N < n·2^n vertices. Let 2 ≤ i ≤ n, m = ν_{n−i} and h = ν_{n−i+1}. Then m − h ≥ n, and

  Φ((m + 1)/n, h/n) < ln 2 + (ln n)/n.

*Proof.* Take an (n − i)-set A with |D(A)| = m. Lemma 3.1 with s = n − i and k = n, using ν_n ≥ 1, gives C(m, n) ≤ N·C(m − h, n).
Since m ≥ ν_{n−1} ≥ n + 1, C(m, n) > 0. So C(m − h, n) > 0, that is, m − h ≥ n. Taking logarithms,

  G := Σ_{t=0}^{n−1} g(t) = ln[ C(m, n)/C(m − h, n) ] ≤ ln N < n ln 2 + ln n,  where g(x) = ln( (m − x)/(m − h − x) ).

On [−1, n − 1], g is defined and increasing, since m − h − x ≥ 1 and g′(x) = 1/(m − h − x) − 1/(m − x) > 0. So g(t) ≥ ∫_{t−1}^{t} g. Then

  G ≥ ∫_{−1}^{n−1} g(x) dx = n ∫₀¹ g(ny − 1) dy = n·Φ((m + 1)/n, h/n). ∎

This exact comparison replaces the "−O(1)" Riemann estimate of the earlier write-up. It is checked numerically on 27 760 triples (n, m, h) in V5.

**Lemma 5.3.** Fix i ≥ 1 and ε > 0. There is n₀ such that every S_n tournament with n ≥ n₀ and fewer than n·2^n vertices satisfies ν_{n−i} ≥ (a_i − ε)·n.

*Proof.* We use induction on i.

The case i = 1 is ν_{n−1} ≥ n + 1 > a_1·n.

Now let i ≥ 2. We may assume ε < a_i − a_{i−1} − 1, which is positive because a_i > 2a_{i−1} ≥ a_{i−1} + 1.
1. Put a′ = a_i − ε/2. Then Φ(a′, a_{i−1}) > Φ(a_i, a_{i−1}) = ln 2.
2. By continuity, choose 0 < δ < ε/2 with η := Φ(a′, a_{i−1} − δ) − ln 2 > 0. Note a′ − (a_{i−1} − δ) > 1.
3. By the induction hypothesis, h = ν_{n−i+1} ≥ (a_{i−1} − δ)·n for all large n.
4. Suppose m = ν_{n−i} < (a_i − ε)·n with n ≥ 2/ε. Then (m + 1)/n < a′. Lemma 5.2 gives a′ − h/n > (m + 1 − h)/n ≥ 1, so every point used below lies in the domain.
5. Monotonicity in a, then in b, gives Φ((m + 1)/n, h/n) ≥ Φ(a′, h/n) ≥ Φ(a′, a_{i−1} − δ) = ln 2 + η.
6. Lemma 5.2 bounds the same quantity by ln 2 + (ln n)/n. This is a contradiction once (ln n)/n < η. ∎

**Theorem C.** liminf_{n→∞} f(n)/(n·2^n) ≥ c\*. Equivalently, f(n) ≥ (c\* − o(1))·n·2^n.

*Proof.* Fix j ≥ 1 and ε > 0. Let n be large, and let T have S_n on N = f(n) vertices.
* If N ≥ n·2^n, then N/(n·2^n) ≥ 1 > c\*.
* Otherwise Lemma 5.3 gives ν_{n−j} ≥ (a_j − ε)·n, and (2) gives N + 1 ≥ 2^(n−j)·(a_j − ε)·n.

So the liminf is at least (a_j − ε)/2^j. Let ε → 0 and then j → ∞. ∎

*Remarks.*
* Each level of the chain gains about n/2 over plain doubling, since a_j − 2a_{j−1} decreases to 1/2. That gain is why the constant rises from 1/2 to c\*.
* Convergence in n is slow, because of the (ln n)/n term. Earlier floating-point runs of the recursion of §6 give N/(n·2^n) ≈ 0.757 at n = 40 and 0.767 at n = 240.

---

## 6. Theorem D: explicit bounds for 5 ≤ n ≤ 12 (exact computation)

Fix n and N. Define integers L_n ≥ L_{n−1} ≥ … ≥ L_0 as follows.
1. Set L_n = 1.
2. For s = n − 1 down to 0, let L_s be the least m ≥ 2L_{s+1} + 1 such that, for every 1 ≤ k ≤ min(m, n),

  (N − s − m)·C(m − L_{s+1}, k) + m·C(m − L_{s+1} − 1, k) ≥ λ_k·C(m, k).

   Here λ_k = L_k for k > s, and λ_k = 2^(s+1−k)·(L_{s+1} + 1) − 1 for k ≤ s.
3. If no m ≤ N − s qualifies, put L_s = ∞.

**Claim.** If an S_n tournament on N vertices exists, then ν_s ≥ L_s for every s. In particular L_0 ≤ N.

*Proof.* We use downward induction on s. Let A be an s-set with m = |D(A)| = ν_s.
1. Lemma 1.3 gives m ≥ 2ν_{s+1} + 1 ≥ 2L_{s+1} + 1.
2. Each λ_k is a valid lower bound for ν_k. For k > s this is the induction hypothesis. For k ≤ s it follows from (2) applied between levels k and s + 1.
3. Lemma 3.1 with h = L_{s+1} then shows that m satisfies every displayed inequality.

So ν_s ≥ L_s. ∎

Lowering N, or raising any L_t with t > s, only tightens the constraints. So L_0(N) is non-increasing in N.
Consequently, if the recursion rules out N (L_0 > N), it rules out every smaller N too.

**Theorem D.** The recursion rules out N = X − 1 for

| n | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Szekeres (n+2)2^(n−1) − 1 | 7 | 19 | 47 | 111 | 255 | 575 | 1279 | 2815 | 6143 | 13311 | 28671 |
| Theorem B | – | – | 51 | 119 | 271 | 607 | 1343 | 2943 | 6399 | 13823 | 29695 |
| **X (Theorem D)** | 7 | 19 | 49 | **121** | **281** | **665** | **1485** | **3388** | **7398** | **16569** | **35655** |

So f(n) ≥ X for each n in the table. The recursion does not rule out N = X itself, so X is exactly what it proves.
For n = 2 and 3 it returns the true values. For n = 4 it gives only 49, and the structural argument of §2 is what reaches 51.

---

## 7. Verification (`proof/verify_proof.py`, output in `proof/verify_proof.out`)

The script is a fresh implementation. It does not import any of the earlier scripts.

| check | what it does | result |
|---|---|---|
| V1 | Brute force on QR_7 (S_2), QR_19 (S_3), QR_67 (S_4) and `thin_S4_N70` (S_4). For every set A with \|A\| ≤ k − 1 it checks: Lemma 1.2 (D(A) undominated, \|D(A)\| ≥ k + 1); identity (1) for every y; the inner in-degree bound; and all three inequalities of Lemma 3.1 for every k. Where C(m, k) ≤ 3000 it also checks the pair-count identity by listing every U. | all pass. ν-profiles: QR_67 (67, 33, 16, 6, 1); thin_S4_N70 (70, 33, 16, 5, 1). |
| V2 | The S_k version of Lemma 2.1 on every tight (k − 2)-set: regularity of T[R], the outside bound, the exact incidence identity, and the in-degree threshold. | QR_7 and QR_19 attain it **with equality** at every dominator (7 and 171 cases). Neither S_4 example has a tight pair, so at k = 4 the lemma is only checked by the hand proof and V3. |
| V3 | Every inequality of §2 in exact integers. This covers the threshold 25 in Lemma 2.1; the N ≥ 51 threshold of Lemma 2.2, scanned over 24 ≤ N < 2000; the full table of (ℓ, q) for Lemma 2.3 with both forms of the inequality; \|Z\| ≤ 5; and the final count. | all pass |
| V4 | The Theorem B inequality for 5 ≤ n ≤ 2000, the cubic n³ − n² − 13n − 5 > 0, and the failure at n = 4. It also checks the exact ratio formula for Λ(n+1)/Λ(n) and both ratio bounds for n < 400, and the Theorem B row of the §6 table. | all pass |
| V5 | The closed form of Φ against numerical quadrature. For j ≤ 150 it checks the bracket 2a_{j−1} < a_j < 2a_{j−1} + 1, condition (i) and the monotonicity of a_j/2^j. It computes c\* to 40 digits, and checks the comparison G(m, h) ≥ n·Φ((m + 1)/n, h/n) for all n ≤ 20, h ≤ 3n + 1 and n ≤ m − h ≤ 4n + 1. | all pass. c\* = 0.7695032191504894326990652683098231346767. Minimum slack in the comparison is 0.0019. |
| V6 | Runs the §6 recursion for each n in the table at N = X − 1 and N = X, and spot-checks monotonicity at three smaller N. | all pass. Every X in the table is reproduced exactly. |
| V7 | Re-checks the Claim L realisation saved in `ai-debate/` (§8.2). | all pass. The row sizes are 5, 6, 8 and 9. Σ in² + Σ c² = 1596. |

What the script cannot do is check a hand argument in general. The logic of §2, §4 and §5 rests on the proofs above.
The script makes sure that every number in those proofs is right, and that every general lemma holds on the extremal S_2, S_3 and S_4 tournaments that are available.

---

## 8. What is still open

### 8.1 f(4): now 51 ≤ f(4) ≤ 67

The next case is N = 51. These results come from the f4 agent and were **not** re-verified here:
* **Minimum in-degree.** With Lemma 2.1, the budget argument of `RESULTS.md` Lemma 3 drops to Σ_b (|A_b| − 11) ≤ 12N − 610. The covering tables for the two S_3 doubly regular tournaments on 23 vertices then exclude in-degree 23 for all N ≤ 64. This step is computer-assisted and was checked twice.
* **Two cases at N = 51.** Lemma 2.3 leaves (R) T is regular, or (I) 1 ≤ |Z| ≤ 5.
* **Case (R).** LP/MILP models at a tight pair, with exact integer Farkas certificates for all 551 local classes (`round3_agents/f4/vreg51_*.out`, `class0_split.out`), show that no tight pair exists. Then every pair has exactly 12 dominators, and T is a **doubly regular tournament DRT(51)**, equivalently a skew-Hadamard matrix of order 52.
* **Case (I).** A spectral argument reduces it to the *local claim J ≥ 3*. MILP runs support it for 26 of the first 35 of the 551 classes. It is **unfinished**.
* **DRT(51) with S_4.** This is **open**. Every pair-level and triple-level count, and every Gram or spectral identity at a vertex, is forced in every DRT(51), and all of them are consistent with S_4. No classification of skew-Hadamard matrices of order 52 exists.

So **f(4) ≥ 52 would follow from two things: finishing the local claim J ≥ 3, and showing that no DRT(51) has S_4.**

### 8.2 Claim L (the pair-link test for DRT(51)) is false

Round 1 of the 11:44 debate proposed the following test. In a DRT(51), fix a pair {a, b}, let X = D({a, b}), with |X| = 12, and let Y be the other 37 vertices.
For u ∈ Y put N_u = X ∩ N⁻(u). Claim L asserted that no 12-vertex tournament T_X and family (N_u) can satisfy all of the following:
* the exact Gram identities: column sums 12 + in_X(x), and inner products 10 − |N⁺_X(x) ∩ N⁺_X(x′)|;
* (i) T_X is S_2;
* (ii) every in_X ≥ 5;
* (iii) every |N_u| ≥ 5;
* (iv) every N_u meets every N⁻_X(y);
* (v) the N_u pairwise intersect.

Claim L would have reduced f(4) ≥ 52 to a finite search. **It is false.** `ai-debate/claim_l_intersect.py` (HiGHS MILP) found a realisation.
T_X is QR_11 plus a twelfth vertex that beats 6 of the others. There are 37 sets N_u, of sizes 5, 6, 8 and 9 (34 distinct sets).
Check V7 confirms every condition independently, including the exact Gram matrix and the identity Σ in_X² + Σ|N_u|² = 1596.

So **one pair-link on its own cannot exclude a DRT(51) with S_4**. An exclusion has to use how the links of different pairs fit together.
For example, N_u = D({a, b, u}) must agree with what the links of {a, u} and {b, u} say. The realisation does not suggest that such a DRT exists.
It only shows that this local test cannot decide the question.

### 8.3 The asymptotic question

The bounds now read (c\* − o(1))·n·2^n ≤ f(n) ≤ (ln 2 + o(1))·n²·2^n. Two results in the archives explain why the order is hard to settle:
* **The base level is best possible.** For every n there are S_n tournaments with ν_{n−1} = n + 1 (`ROUND3_FINDINGS.md` §4). A bound of the form ν_{n−1} = ω(n) would already give f(n) = ω(n·2^n) through (2), but no such bound holds in general. An improvement of the order must therefore use the fact that N is small.
* **Random symmetric constructions are no better than random.** Random Cayley tournaments, and random G-invariant tournaments for a free action of an odd-order group, cannot beat (ln 2)·n²·2^n asymptotically (`round3_agents/uppertheory/THEOREMS.md`, Theorem A).

---

## References

* P. Erdős, On a problem in graph theory, *Math. Gazette* 47 (1963) 220–223.
* E. Szekeres and G. Szekeres, On a problem of Schütte and Erdős, *Math. Gazette* 49 (1965) 290–293.
* R. L. Graham and J. H. Spencer, A constructive solution to a tournament problem, *Canad. Math. Bull.* 14 (1971) 45–48.
* K. B. Reid, A. A. McRae, S. M. Hedetniemi and S. T. Hedetniemi, Domination and irredundance in tournaments, *Australas. J. Combin.* 29 (2004) 157–172.
* J. W. Moon, *Topics on Tournaments*, Holt, Rinehart and Winston, 1968 (Theorem 16).
* Erdős Problems #902: https://www.erdosproblems.com/902. As of 18 Oct 2026 it lists f(1), f(2), f(3) and the classical bounds, but no bound for f(4).
* J. Wilder, https://github.com/jaredwilder/erdos902 (Lean formalisation of the classical bounds; f(4) ≥ 49 candidate, September 2026).
