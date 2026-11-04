# f(4) ≥ 52: a proof by hand

*Written 20 October 2026. Every step was derived by hand. No computation is used anywhere.
The proof builds on `ERDOS902_PROOF.md` (Theorem A, f(4) ≥ 51, and the lemmas of §1–§2 there).
It replaces every computer-assisted step of `ERDOS902_PROOF.md` §8.1 and of `N51_local_claim.md`.*

---

## 0. Result

**Theorem.** No tournament on 51 vertices has property S_4. Together with Theorem A of `ERDOS902_PROOF.md`,

  **f(4) ≥ 52.**

In fact the proof shows more: **every tournament on at most 51 vertices has a triple with at most 4 dominators.**
Property S_4 is used only through this consequence of it (Lemma 1.2 of `ERDOS902_PROOF.md`).

There are three new ingredients.

1. **Theorem 1 (the local claim, all cases at once).** In an S_4 tournament on 51 vertices, every tight pair P has
   J(P) ≥ 3. The proof is a congruence (rounding) argument modulo 4. It does not depend on the isomorphism class of
   T[D(P)], nor on the in-degrees of the two vertices of P. It replaces the 1101 exact certificates of
   `N51_local_claim.md`, and it settles the case that was left open there (class 0, out-mode).
2. **Corollary 4.** Every S_4 tournament on 51 vertices is a doubly regular tournament DRT(51). This was the reduction of
   `ERDOS902_PROOF.md` §8.1. That reduction used a computer-assisted covering step (minimum in-degree ≥ 24) and the
   local claim. Both are now replaced by short arguments.
3. **Theorem 5.** No DRT(51) has S_4. The proof compares the third moment of the number of dominators of a triple with
   the third moment of the number of vertices that the triple dominates. In a DRT(51) these two numbers add up to a
   constant (11 or 12), and the bound "at least 5 dominators" sits just half a unit below the mean. A double count
   forces the two third moments to be equal. Under S_4 that equality pins the distribution down so tightly that its
   variance becomes too small, but the variance is fixed by the pair counts.

**What remains open.** The upper bound is still f(4) ≤ 67 (QR_67). The next case is N = 52.

---

## 1. Facts used

Notation is as in `ERDOS902_PROOF.md`. T is a tournament on V with |V| = N. D(X) is the set of dominators of X.
N⁻(v) and N⁺(v) are the in- and out-neighbourhoods, d⁻(v) and d⁺(v) their sizes.

Let T have S_4. The following are proved by hand in `ERDOS902_PROOF.md`.

* **(F1)** Every triple Y has |D(Y)| ≥ 5. (Lemma 1.2.)
* **(F2)** For a pair P and a vertex y ∉ P, D(P ∪ {y}) = D(P) ∩ N⁻(y), and this set has at least 5 elements. So
  T[D(P)] has minimum in-degree ≥ 5 and |D(P)| ≥ 11. (Lemma 1.3.)
* **(F3)** For a ∈ N⁻(v), the in-degree of a inside T[N⁻(v)] is |D({a, v})| ≥ 11. So d⁻(v) ≥ 23.
* A pair P is **tight** if |D(P)| = 11. Then T[D(P)] has 11 = 2·5 + 1 vertices and minimum in-degree ≥ 5, so it is
  **5-regular**.
* **Lemma T** (Lemma 2.1). If P is tight, every r ∈ D(P) has d⁻(r) ≥ 25.
* **Claim Q** (Lemma 2.3). Let Z = {v : d⁻(v) = 24}. Every v ∈ Z has at most 2 in-neighbours in Z, so |Z| ≤ 5.
  Its proof also shows: if v ∈ Z, then at least 12 vertices a ∈ N⁻(v) make {a, v} a tight pair.
* **Theorem A.** N ≥ 51.

Each of (F2), (F3), Lemma T and Claim Q is derived from (F1) alone, by counting. So everything below uses S_4 only
through (F1).

---

## 2. Theorem 1: every tight pair at N = 51 has J ≥ 3

**Theorem 1.** Let T be an S_4 tournament on 51 vertices and P a tight pair. Put R = D(P). Then

  J(P) := Σ_{r ∈ R} (d⁻(r) − 25) ≥ 3.

By Lemma T every term of J(P) is ≥ 0.

### 2.1 Set-up and three identities

Let P = {a, b}, R = D(P) with |R| = 11, and O = V \ (P ∪ R), so |O| = 38. For r ∈ R write d⁻(r) = 25 + j_r, so
j_r ≥ 0 and J = Σ_r j_r. For y ∈ O put Q_y = R ∩ N⁻(y) = D(P ∪ {y}) and q_y = |Q_y|. By (F2), **q_y ≥ 5**.

Every vertex of R beats a and b. So a and b beat no vertex of R, and for U ⊆ R:

  **D(U) = { w ∈ R \ U : U ⊆ N⁺(w) } ∪ { y ∈ O : U ∩ Q_y = ∅ }.**  (2.1)

For u ≠ v in R let c(u, v) = |N⁻(u) ∩ N⁻(v) ∩ R|, the number of vertices of R that beat both.

* **(I1)** For r ∈ R, #{y ∈ O : r ∈ Q_y} = #{y ∈ O : r → y} = d⁺(r) − 7 = 18 − j_r, because r beats a, b and exactly 5
  vertices of R, and d⁺(r) = 50 − d⁻(r). Hence **#{y ∈ O : r ∉ Q_y} = 20 + j_r.**
* **(I2)** Σ_{y ∈ O} q_y = Σ_{r ∈ R} (18 − j_r) = 198 − J, so **Σ_{y ∈ O} (q_y − 5) = 8 − J.**
* **(I3)** T[R] is 5-regular. For u ∈ R, Σ_{v ≠ u} c(u, v) = Σ_{w ∈ N⁻(u) ∩ R} (5 − 1) = **20**. Also **c(u, v) ≤ 4**: if
  u → v, then u is one of the 5 in-neighbours of v in R but does not beat itself.

### 2.2 Lemma P (structure when J ≤ 2)

This is Lemma P of `N51_local_claim.md`. The proof is repeated here so that the argument is complete.

For r ∈ R, the 45 triples U ⊆ R with r ∈ U each have at least 5 dominators (F1). By (2.1) the w ∈ R that beat r give
30 incidences (5 vertices, each dominating C(4, 2) = 6 of these triples), and a y ∈ O with r ∉ Q_y gives C(10 − q_y, 2).
With (I1) this gives, for every r ∈ R,

  Σ_{y ∈ O, r ∉ Q_y} λ(q_y) ≤ 5 + 10 j_r,  where λ(q) = 10 − C(10 − q, 2).  (∗)

The values are λ(5) = 0, λ(6) = 4, λ(7) = 7, λ(8) = 9 and λ(9) = λ(10) = 10.

**Lemma P.** If J ≤ 2, then exactly one y* ∈ O has q_{y*} ≥ 9, at most two y ∈ O have q_y = 6, and every other
y ∈ O has q_y = 5.

*Proof.*
* If q_y = 7, each of the 4 vertices r ∉ Q_y has 7 ≤ 5 + 10 j_r by (∗), so j_r ≥ 1 and J ≥ 4. If q_y = 8, the same
  argument with λ(8) = 9 gives J ≥ 3. So no q_y is 7 or 8.
* Count the triples of R with their dominators. By (2.1) and (F1),
  110 + Σ_y C(11 − q_y, 3) ≥ 5·165 = 825. (Each w ∈ R dominates C(5, 3) = 10 triples of R.)
  Let m = #{y : q_y ≥ 9} and n_6 = #{y : q_y = 6}. Since C(6, 3) = 20, C(5, 3) = 10 and C(11 − q, 3) = 0 for q ≥ 9,
  this reads 110 + 20(38 − m − n_6) + 10 n_6 ≥ 825, that is, **20m + 10n_6 ≤ 45**.
* By (I2), n_6 + Σ_{q_y ≥ 9} (q_y − 5) = 8 − J ≥ 6.
  * If m = 0, then n_6 ≥ 6, which contradicts 10 n_6 ≤ 45.
  * If m ≥ 2, then m = 2 (as 20m ≤ 45), and the two terms q_y − 5 ≥ 4 already give 8. So J = 0 and both have
    q_y = 9. A vertex r outside one of them gets λ(9) = 10 ≤ 5 from (∗), which is false.
  * So m = 1, and then 10 n_6 ≤ 25 gives n_6 ≤ 2. ∎

### 2.3 The rounding lemma

Assume J ≤ 2 from now on, and use Lemma P. Call y ∈ O a **5-vertex** or a **6-vertex** according as q_y = 5 or 6.
For u ∈ R put

* α_u = #{5-vertices y with u ∉ Q_y}, β_u = #{6-vertices y with u ∉ Q_y}, γ_u = 1 if u ∉ Q_{y*} and 0 otherwise.

By (I1), **α_u + β_u + γ_u = 20 + j_u.** For u ≠ v in R put

* k(u, v) = #{5-vertices y with u, v ∉ Q_y} and m(u, v) = #{6-vertices y with u, v ∉ Q_y},
* **s(u, v) = Σ_{w ∈ R \ {u, v}} (|D({u, v, w})| − 5)**, the total excess of the 9 triples of R that contain u and v.
  By (F1), s(u, v) ≥ 0.

**(R1)** s(u, v) = 3c(u, v) + 4k(u, v) + 3m(u, v) − 45.

*Proof.* Use (2.1). A vertex w′ ∈ R dominates {u, v, w} only if it beats u and v. There are c(u, v) such w′, and each
dominates the triple for exactly the 3 choices w ∈ (N⁺(w′) ∩ R) \ {u, v}. A vertex y ∈ O dominates {u, v, w} exactly
when u, v, w ∉ Q_y. For a y with u, v ∉ Q_y this happens for |R \ Q_y| − 2 choices of w: 4 for a 5-vertex, 3 for a
6-vertex, and 0 for y*, which misses at most two vertices of R. ∎

**(R2)** Σ_{v ≠ u} s(u, v) = 10 + 20 j_u − 8 β_u − 20 γ_u.

*Proof.* Sum (R1) over the 10 vertices v ≠ u. By (I3), Σ_v c(u, v) = 20. A 5-vertex y with u ∉ Q_y is counted in
k(u, v) for the 5 vertices v ∈ R \ (Q_y ∪ {u}), so Σ_v k(u, v) = 5 α_u. In the same way Σ_v m(u, v) = 4 β_u. So the sum
is 60 + 20 α_u + 12 β_u − 450. Substitute α_u = 20 + j_u − β_u − γ_u. ∎

**(R3)** s(u, v) ≡ 3 − c(u, v) − m(u, v) (mod 4). Consequently

  s(u, v) ≥ 3 − c(u, v) − m(u, v), and s(u, v) ≥ 7 − c(u, v) − m(u, v) when c(u, v) + m(u, v) ≥ 4.

*Proof.* In (R1), 4k ≡ 0, 3 ≡ −1 and −45 ≡ 3 (mod 4). Now s ≥ 0. Here c + m ≤ 4 + 2 = 6. If c + m ≤ 3, the least
non-negative number ≡ 3 − c − m is 3 − c − m itself. If 4 ≤ c + m ≤ 6, it is 7 − c − m. ∎

**Rounding lemma.** For every u ∈ R,

  β_u + 5 γ_u + N_4(u) ≤ 5 j_u,  where N_4(u) = #{v ≠ u : c(u, v) + m(u, v) ≥ 4}.

*Proof.* Sum (R3) over v ≠ u. By (I3) and Σ_v m(u, v) = 4 β_u, the right sides add up to
30 − 20 − 4β_u + 4N_4(u). Compare with (R2): 10 + 20 j_u − 8β_u − 20γ_u ≥ 10 − 4β_u + 4N_4(u). Divide by 4. ∎

The point is the rounding in (R3). Without it, (R1) would only give 4k ≥ 45 − 3c − 3m, and its sum over v would have
slack. The congruence modulo 4 removes exactly that slack.

### 2.4 Proof of Theorem 1

Suppose J ≤ 2. Let V_0 = {u ∈ R : j_u = 0}. Then |V_0| ≥ 11 − J ≥ 9.

**Step 1: every u ∈ V_0 lies in Q_{y*} and in every Q_y with q_y = 6, and c(u, v) ≤ 3 for all v.**
For u ∈ V_0 the rounding lemma gives β_u + 5γ_u + N_4(u) ≤ 0, so β_u = γ_u = N_4(u) = 0.

**Step 2: J = 2, q_{y*} = 11, and every other y ∈ O has q_y = 5.**
Let q_y = 6. Its complement R \ Q_y has 5 elements, and by Step 1 none of them lies in V_0. But R \ V_0 has at most
J ≤ 2 elements. So there is no 6-vertex: n_6 = 0. Then (I2) reads q_{y*} − 5 = 8 − J, that is, q_{y*} = 13 − J.
Since q_{y*} ≤ 11, this forces J = 2 and q_{y*} = 11, so Q_{y*} = R.

**Step 3: |D({u, v})| = 12 whenever u ∈ V_0.**
Let u ∈ V_0. Now β_u = γ_u = 0 and every m(u, v) = 0, so (R2) gives Σ_v s(u, v) = 10. By (R3) and (I3),
Σ_v s(u, v) ≥ Σ_v (3 − c(u, v)) = 30 − 20 = 10. So every term is tight: **s(u, v) = 3 − c(u, v)** for every v ≠ u.
By (R1) with m = 0 this says 4k(u, v) = 48 − 4c(u, v), so k(u, v) = 12 − c(u, v). By (2.1), and because y* beats no
vertex of R, |D({u, v})| = c(u, v) + k(u, v) = 12.

**Step 4: the pair sums.** For every s ∈ R,

  Σ_{v ≠ s} |D({s, v})| = Σ_v c(s, v) + Σ_v k(s, v) = 20 + 5 α_s = 20 + 5(20 + j_s) = 120 + 5 j_s,

since now every y ∈ O with s ∉ Q_y is a 5-vertex.

**Step 5: contradiction.** Since J = 2, either one vertex has j = 2, or two vertices have j = 1.

* *One vertex s with j_s = 2.* All other 10 vertices lie in V_0, so by Step 3 each |D({s, v})| equals 12. The sum in
  Step 4 is then 120, but it must be 130.
* *Two vertices s_1, s_2 with j = 1.* The other 9 vertices lie in V_0. Step 4 at s_1 gives
  |D({s_1, s_2})| = 125 − 9·12 = 17, so k(s_1, s_2) = 17 − c(s_1, s_2). By (R1),
  s(s_1, s_2) = 3c + 4(17 − c) − 45 = 23 − c(s_1, s_2) ≥ 19, by (I3).
  On the other hand s(s_1, s_2) is the total excess of the triples that contain both s_1 and s_2. These are among the
  triples that contain s_1, whose total excess is half of Σ_v s(s_1, v) (each such triple {s_1, v, w} is counted once
  for v and once for w). By (R2) with j = 1 and β = γ = 0, that half is (10 + 20)/2 = 15. So s(s_1, s_2) ≤ 15 < 19.

Both cases are impossible, so J ≥ 3. ∎

**Remarks.**
* Theorem 1 never uses the isomorphism class of T[R], the S_2 property of T[R], the "intersecting" property of the
  sets Q_y, or the types of the vertices of O relative to a and b. It uses (F1), (F2), Lemma T and N = 51.
* So it proves the claim of `N51_local_claim.md` in its strongest ("type-free") form for all 551 classes at once,
  including class 0 in out-mode, which was the case left open there. It agrees with all 1101 certificates found
  by computer.
* It also explains why the computer search found class 0 hard. In the circulant class 0 (x → x + {1, 2, 3, 4, 6} on
  Z_11), c(u, v) takes only the values 1, 2, 3, so N_4(u) = 0 at every vertex, and the rounding lemma is tight at
  every vertex. A linear programming relaxation does not see the rounding in (R3), so a branch-and-bound search
  has to rediscover it one branch at a time.

**Theorem 1 holds for every N, not only N = 51.** For a tight pair in an S_4 tournament on N vertices, the
in-neighbours of r ∈ R outside R ∪ P are exactly the y ∈ O with r ∉ Q_y, so #{y ∈ O : r ∉ Q_y} = d⁻(r) − 5 = 20 + j_r
for every N. Hence (∗), (R1)–(R3) and the rounding lemma hold verbatim, with γ_u now the number of y with q_y ≥ 9 and
u ∉ Q_y. Only Step 2 changes. (I2) becomes Σ_y (q_y − 5) = 6N − 298 − J. With no 6-vertex (Step 1), and with m
vertices of q ≥ 9 missing Γ = Σ_u γ_u ≤ J vertices in all (the rounding lemma gives γ_u ≤ j_u), this reads
6m − Γ = 6N − 298 − J, that is, 6(m − N + 50) = 2 − J + Γ. The right side lies in [0, 2], so it is 0: J = 2, Γ = 0, and
all m = N − 50 big vertices have Q_y = R. Steps 3–5 are then unchanged. So **in every S_4 tournament, every tight pair
has J ≥ 3.** This strengthens Lemma T.

The same rounding also gives a structural fact that holds for every tight pair, whatever J is: if r ∈ D(P) has
d⁻(r) = 25, then r lies in every Q_y with q_y ≥ 6, c(r, v) ≤ 3 for all v ∈ R, and |D({r, v})| = 12 for every other
v ∈ R. (Proof: with the y of q_y ∈ {7, 8} included, (R2) reads Σ_v s(r, v) = 10 + 20 j_r − 8β_6 − 14β_7 − 18β_8 − 20γ,
where β_q counts the y with q_y = q and r ∉ Q_y. For j_r = 0 the left side is ≥ 0, so r misses no Q_y with q_y ≥ 7
and at most one with q_y = 6. Then the rounding lemma as written gives β_6 = 0 and N_4(r) = 0, and Step 3 applies.)
This is the natural starting point for N = 52.

---

## 3. Every S_4 tournament on 51 vertices is doubly regular

Throughout this section T is an S_4 tournament on 51 vertices. The in-degrees add up to C(51, 2) = 51·25, so the
average in-degree is 25. Write e(x) = d⁻(x) − 25.

**Corollary 2. Every vertex has in-degree at least 24.**

*Proof.* By (F3), d⁻ ≥ 23. Suppose d⁻(v) = 23, and put A = N⁻(v) and B = N⁺(v), so |A| = 23 and |B| = 27.
* By (F3) every a ∈ A has in-degree |D({a, v})| ≥ 11 inside T[A]. These in-degrees add up to C(23, 2) = 23·11, so
  each is exactly 11: T[A] is 11-regular and **every pair {a, v} with a ∈ A is tight**, with D({a, v}) = A ∩ N⁻(a).
* Every a′ ∈ A beats some a ∈ A, and then a′ ∈ D({a, v}). By Lemma T, **e(a′) ≥ 0 for every a′ ∈ A**.
* Count the arcs from A to B. Each b ∈ B is beaten by the vertices of A ∩ N⁻(b) = D({v, b}), and there are at least 11
  of them by (F2). So there are at least 11·27 = 297 such arcs. Each a ∈ A beats v and 11 vertices of A, so it beats
  d⁺(a) − 12 = 50 − d⁻(a) − 12 = 13 − e(a) vertices of B. So there are exactly 23·13 − Σ_{a ∈ A} e(a) = 299 − Σ_A e
  such arcs. Hence **Σ_{a ∈ A} e(a) ≤ 2.**
* Take any a ∈ A. The pair {a, v} is tight, its dominator set D({a, v}) lies inside A, and all the terms e(r) are
  ≥ 0. So J({a, v}) ≤ Σ_{a′ ∈ A} e(a′) ≤ 2. This contradicts Theorem 1. ∎

At N = 51 this replaces the computer-assisted covering argument for the two S_3 doubly regular tournaments on 23
vertices (`ERDOS902_PROOF.md` §8.1, first bullet). That argument covered all N ≤ 64; the one here is only for N = 51.

**The two cases.** By Corollary 2 every in-degree is at least 24, and the average is 25. Let Z = {v : d⁻(v) = 24}.
* **(R)** If Z = ∅, every in-degree is 25: T is regular.
* **(I)** Otherwise 1 ≤ |Z| ≤ 5 by Claim Q, and Σ_{x ∉ Z} e(x) = |Z|.

**Corollary 3. Case (I) is impossible.**

*Proof.* This is the spectral lemma of `N51_local_claim.md` §1. It needed the local claim in both "modes", and
Theorem 1 now supplies it without any condition. The argument is repeated here.

Fix v ∈ Z, and let A = N⁻(v), so |A| = 24. For each of the other 50 vertices z let D_z = D({v, z}) ⊆ A and
h_z = |D_z| − 11 ≥ 0 (F2).
1. **Gram matrix.** Let G be the 50 × 50 Gram matrix of the indicator vectors of the sets D_z in ℝ^A. Then
   G_zz = 11 + h_z and, for z ≠ z′, G_zz′ = |D_z ∩ D_z′| = |D({v, z, z′})| ≥ 5 (F1). Write G = 5·𝟙𝟙ᵀ + M. Then
   M_zz = 6 + h_z and M_zz′ = |D({v, z, z′})| − 5 ≥ 0. G is positive semidefinite of rank ≤ 24, so it has at least 26
   zero eigenvalues. Since −5·𝟙𝟙ᵀ is negative semidefinite, Weyl's inequality gives λ_i(M) ≤ λ_i(G) for every i. So
   **M has at least 26 eigenvalues ≤ 0.**
2. **Few non-tight z.** Each x ∈ A beats d⁺(x) − 1 of the 50 vertices z, so Σ_z |D_z| = Σ_{x ∈ A} (49 − d⁻(x)) and
   Σ_z h_z = 626 − Σ_{x ∈ A} d⁻(x). Here d⁻(x) ≥ 24, and at most 2 vertices of A lie in Z (Claim Q). So
   Σ_{x ∈ A} d⁻(x) ≥ 598 + W, where W = Σ_{x ∈ A} max(e(x), 0). Hence **the number n_t of z with h_z ≥ 1 is at most
   28 − W.**
3. **The tight z give a positive definite block.** If h_z = 0, then {v, z} is a tight pair with R = D_z. The 49
   off-diagonal entries of row z of M add up to Σ_{z′} (|D({v, z, z′})| − 5). For z′ ∈ R the term is the in-degree
   of z′ in the 5-regular T[R], minus 5, which is 0. For the 38 other z′ it is q_{z′} − 5. By (I2) the row sum is
   8 − J({v, z}) ≤ 5 < 6 = M_zz, by Theorem 1. So the principal submatrix of M on the tight z is strictly diagonally
   dominant with positive diagonal, hence positive definite (Gershgorin).
4. By Cauchy interlacing, a positive definite principal submatrix of size 50 − n_t forces at least 50 − n_t positive
   eigenvalues of M. With step 1, 26 ≤ n_t ≤ 28 − W, so **W ≤ 2**.
5. By Claim Q there is a ∈ A with {a, v} tight. Its dominator set lies in A, and its terms e(r) are ≥ 0 (Lemma T).
   So J({a, v}) ≤ W ≤ 2, contradicting Theorem 1. ∎

**Corollary 4. T is a doubly regular tournament.**

*Proof.* By Corollary 3, T is regular: every in-degree and out-degree is 25. A tight pair P would have
J(P) = Σ_{r ∈ D(P)} (25 − 25) = 0, contradicting Theorem 1. So every pair has at least 12 dominators. But
Σ_P |D(P)| = Σ_w C(d⁺(w), 2) = 51·C(25, 2) = 15300 = 12·C(51, 2). So **every pair has exactly 12 dominators.** ∎

So T is a DRT(51), the tournament of a skew-Hadamard matrix of order 52. In a DRT(51) every pair also has exactly 12
common out-neighbours: if u → w, the 24 out-neighbours of u other than w split into the 25 − 12 − 1 = 12 that beat w
and the remaining 12 that w beats.

---

## 4. No DRT(51) has S_4

**Theorem 5.** In every doubly regular tournament on 51 vertices some triple has at most 4 dominators. In particular
no DRT(51) has S_4.

Let T be a DRT(51): every in- and out-degree is 25 and every pair has exactly 12 common dominators (and, as noted
after Corollary 4, exactly 12 common out-neighbours). For a triple Y let

* k(Y) = |D(Y)|, the number of vertices that beat all of Y;
* D⁺(Y) = {w ∉ Y : every vertex of Y beats w}, the vertices that Y dominates;
* σ(Y) = 1 if T[Y] is transitive and σ(Y) = 0 if T[Y] is a 3-cycle.

### 4.1 Four identities

**(M0)** There are Σ_v C(d⁺(v), 2) = 51·300 = **15300 transitive** triples, and C(51, 3) − 15300 = 20825 − 15300 =
**5525 cyclic** triples. (Each transitive triple has exactly one vertex that beats the other two.)

**(M1) |D(Y)| + |D⁺(Y)| = 12 − σ(Y),** that is, 11 for a transitive triple and 12 for a cyclic one.

*Proof.* Let Y = {y_1, y_2, y_3}. By inclusion–exclusion over the 48 vertices outside Y,

  |D⁺(Y)| = 48 − Σ_i |N⁻(y_i) \ Y| + Σ_{i<j} |D({y_i, y_j}) \ Y| − |D(Y)|.

Here Σ_i |N⁻(y_i) \ Y| = 3·25 − 3 = 72, because the three arcs inside Y account for 3 in-arcs. The pair {y_i, y_j}
has 12 dominators, and one of them lies in Y exactly when the third vertex of Y beats both; this happens for σ(Y) of
the three pairs. So the middle sum is 36 − σ(Y), and |D⁺(Y)| = 12 − σ(Y) − |D(Y)|. ∎

**(M2) Σ_{Y transitive} k(Y) = 84150 and Σ_{Y cyclic} k(Y) = 33150.** So the mean of k is **11/2 on transitive
triples and 6 on cyclic triples.**

*Proof.* k(Y) counts the w with Y ⊆ N⁺(w). Fix w. Every x ∈ N⁺(w) has exactly 12 out-neighbours inside N⁺(w) (the
common out-neighbours of w and x). So T[N⁺(w)] is a 12-regular tournament on 25 vertices. It has Σ_x C(12, 2) = 1650
transitive triples and C(25, 3) − 1650 = 650 cyclic ones. Multiply by 51. Finally 84150/15300 = 11/2 and
33150/5525 = 6. ∎

**(M3) Σ_Y C(k(Y), 2) = 280500.**

*Proof.* The sum counts pairs (Y, {w, w′}) with w, w′ ∈ D(Y), that is, Y ⊆ N⁺(w) ∩ N⁺(w′). That intersection has 12
vertices for every pair {w, w′}, so the sum is C(51, 2)·C(12, 3) = 1275·220. ∎

**(M4) Σ_Y C(k(Y), 3) = Σ_Y C(12 − σ(Y) − k(Y), 3).**

*Proof.* Both sides count the pairs (Y, W) of triples such that every vertex of W beats every vertex of Y. For fixed
Y this means W ⊆ D(Y). For fixed W it means Y ⊆ D⁺(W), and |D⁺(W)| = 12 − σ(W) − k(W) by (M1). ∎

Identity (M4) is the new ingredient. It holds in every DRT(51), whatever the arcs.

### 4.2 The contradiction

Suppose every triple has k(Y) ≥ 5. Put u(Y) = k(Y) − 11/2 if Y is transitive and u(Y) = k(Y) − 6 if Y is cyclic.
By (M2), **Σ_{transitive} u = 0 and Σ_{cyclic} u = 0.**

*Algebra.* Let L be a constant, u = k − L/2 and a = L/2 − 1, and f(x) = (x − 1)x(x + 1) = x³ − x, an odd function.
Then 6·C(k, 3) = f(k − 1) = f(u + a), and 6·C(L − k, 3) = f(a − u) = −f(u − a). So

  C(k, 3) − C(L − k, 3) = (f(u + a) + f(u − a))/6 = (u³ + (3a² − 1)·u)/3.

For transitive triples L = 11, and for cyclic ones L = 12. Since Σ u = 0 on each class, (M4) becomes

  **Σ_{transitive} u³ + Σ_{cyclic} u³ = 0.**  (4.1)

*Positivity.* On a transitive triple k ≥ 5 gives u ∈ {−1/2, 1/2, 3/2, …}, and
u³ − u/4 = (u − 1/2)·u·(u + 1/2) ≥ 0, with equality only for u = ±1/2. On a cyclic triple u ∈ {−1, 0, 1, 2, …}, and
u³ − u = (u − 1)·u·(u + 1) ≥ 0, with equality only for u ∈ {−1, 0, 1}. By (4.1) and Σ u = 0 on each class,

  Σ_{transitive} (u³ − u/4) + Σ_{cyclic} (u³ − u) = 0.

Every term is ≥ 0, so every term is 0. Hence **every transitive triple has 5 or 6 dominators and every cyclic triple
has 5, 6 or 7.**

*Counting.* By (M2) the transitive mean is 11/2, so exactly 7650 transitive triples have k = 5 and 7650 have k = 6.
The cyclic mean is 6, so the numbers of cyclic triples with k = 5 and with k = 7 are equal, say p each, and
5525 − 2p have k = 6. Then

  Σ_Y C(k(Y), 2) = 7650·10 + 7650·15 + 10p + 15(5525 − 2p) + 21p = 274125 + p.

By (M3) this equals 280500, so p = 6375. But 2p ≤ 5525. This contradiction proves Theorem 5. ∎

**Remarks.**
* (M2) and (M3) fix the variance of k(Y) over all triples at about 0.845. Once (M4) has confined k to {5, 6} on
  transitive and {5, 6, 7} on cyclic triples, the variance can be at most about 0.498. That gap is the whole proof.
* The argument is sharp in the following sense. In a DRT(4t + 3) the same identities hold with 12 replaced by t, the
  transitive mean of k is (t − 1)/2 and the cyclic mean is t/2. For t = 12 the bound k ≥ 5 sits only 1/2 below the
  transitive mean. For QR_67 (t = 16) the means are 15/2 and 8, the bound k ≥ 5 is far below them, and nothing is
  forced. This is consistent with QR_67 having S_4.
* **Sanity check at the level below** (done by hand). In QR_19 (t = 4), which has S_3, the same three identities say:
  if every triple has at least 1 dominator, then transitive triples have k ∈ {1, 2}, half each (342 + 342), and cyclic
  triples have k ∈ {1, 2, 3} with p of each extreme value, where 342·0 + 342·1 + (285 − 2p)·1 + 3p = C(19, 2)·C(4, 3)
  = 684 gives p = 57. This matches the orbit structure of QR_19 under x ↦ ax + b (a a nonzero square): the 114
  cyclic triples fixed by x ↦ 7x + c form two orbits of size 57, and the remaining 171 cyclic triples form one orbit.
  So the identities are consistent with a tournament that is known to exist.

---

## 5. Proof of the Theorem, and what it replaces

**Proof that f(4) ≥ 52.** Theorem A excludes N ≤ 50. Let T be an S_4 tournament on 51 vertices. By Corollary 4 it is
a DRT(51). By Theorem 5 some triple of T has at most 4 dominators, which contradicts (F1). So no S_4 tournament has
51 vertices. ∎

The logical chain for N = 51 is:

| step | statement | ingredients | was |
|---|---|---|---|
| Theorem 1 | every tight pair has J ≥ 3 | (F1), (F2), Lemma T, Lemma P, rounding mod 4 | 1101 computer certificates, 1 case open |
| Corollary 2 | minimum in-degree ≥ 24 | Theorem 1, Lemma T, arc count | computer-assisted covering tables |
| Corollary 3 | case (I) is impossible | spectral lemma, Claim Q, Theorem 1 | needed the open case |
| Corollary 4 | T is a DRT(51) | Theorem 1, pair count | computer certificates for case (R) |
| Theorem 5 | no DRT(51) has S_4 | identities (M0)–(M4) | open |

Nothing in this chain uses a computer. Property S_4 is used only through (F1): every triple has at least 5
dominators. So the proof shows that **every tournament on 51 vertices has a triple with at most 4 dominators**, and
together with Theorem A, the same holds for every tournament on at most 51 vertices.

**Status of the earlier files.**
* `N51_local_claim.md`: its local claim is Theorem 1. The certificates in `n51_local/` remain valid, but they are no
  longer needed. The open case "class 0, out-mode" is covered by Theorem 1.
* `ERDOS902_PROOF.md` §8.1: every bullet is now settled by hand. "DRT(51) with S_4" is Theorem 5. §8.2 (Claim L is
  false) still stands; Theorem 5 does not use pair links at all.

## 6. Hand checks of the numbers

* §2: 45 triples through r, 5·45 = 225; 30 + 10(20 + j) − 225 = 5 + 10j. Triples of R: C(11, 3) = 165, 5·165 = 825,
  11·C(5, 3) = 110. (R2): 60 + 20(20 + j − β − γ) + 12β − 450 = 10 + 20j − 8β − 20γ. Step 5: 20 + 5·21 = 125,
  125 − 108 = 17, 3c + 68 − 4c − 45 = 23 − c.
* §3: 11·27 = 297, 23·13 = 299; Σ_z |D_z| = 24·49 − Σ d⁻ = 1176 − Σ d⁻, minus 50·11 = 550 gives 626 − Σ d⁻;
  24·25 − 2 = 598; 51·C(25, 2) = 15300 = 12·1275.
* §4: C(51, 3) = 20825; 51·C(25, 2) = 15300; C(25, 3) = 2300, 25·C(12, 2) = 1650; 51·1650 = 84150, 51·650 = 33150;
  1275·220 = 280500; 7650·25 = 191250; 15·5525 = 82875; 191250 + 82875 = 274125; 280500 − 274125 = 6375 > 2762.
* §4, algebra: for L = 11, a = 9/2 and 3a² − 1 = 239/4; for L = 12, a = 5 and 3a² − 1 = 74. Spot values:
  C(5, 3) − C(6, 3) = −10 = ((−1/2)³ + (239/4)(−1/2))/3; C(7, 3) − C(5, 3) = 25 = (1 + 74)/3.

