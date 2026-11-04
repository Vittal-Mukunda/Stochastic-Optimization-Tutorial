# Tight pairs in an S_4 tournament on 52 vertices

*Derived by hand, 20 October 2026. No computation. Builds on `F4_GE_52_HAND_PROOF.md`, whose Theorem 1 already gives J ≥ 3 for a tight pair at every order.*

## 0. Result

**Theorem.** Let T be an S_4 tournament on 52 vertices.

1. Every in-degree is at least 24.
2. Every tight pair P has J(P) ≥ 5, and at least four vertices of D(P) have in-degree greater than 25.

Property S_4 is used only through (F1): every triple has at least 5 dominators. The isomorphism type of T[D(P)] is not used.

What this does not do: it does not yet exclude a tight pair, and it does not exclude an S_4 tournament on 52 vertices. A tight pair that remains must put its excess in-degree on at least four dominators. In-degree 24 is still open; Claim Q still bounds that set by 5.

## 1. Set-up

N = 52, P = {a, b} tight, R = D(P), |R| = 11, O = V \ (P ∪ R), so |O| = 39. T[R] is 5-regular. Write d⁻(r) = 25 + j_r with j_r ≥ 0 and J = Σ j_r. For y ∈ O write q_y = |R ∩ N⁻(y)| ≥ 5. The identities of `F4_GE_52_HAND_PROOF.md` §2 that do not use N = 51 remain valid, and the order enters only through

  Σ_{y ∈ O} (q_y − 5) = 6·52 − 298 − J = 14 − J.  (E)

In particular J ≤ 14. Theorem 1 of that note gives J ≥ 3, so the right side is an integer in {0, …, 11}.

For r ∈ R the exact triple count (the equality behind (∗) there) is

  Ex(r) := Σ_{U ∋ r, |U| = 3} (|D(U)| − 5) = 5 + 10 j_r − Σ_{y ∌ r} λ(q_y),  (Ex)

where λ(5) = 0, λ(6) = 4, λ(7) = 7, λ(8) = 9, λ(9) = λ(10) = λ(11) = 10, and the sum runs over y ∈ O with r ∉ Q_y. Since Ex(r) ≥ 0,

  Σ_{y ∌ r} λ(q_y) ≤ 5 + 10 j_r.  (∗)

**Pair-sum formula.** For u ∈ R let τ_u = Σ_{y ∌ u} (q_y − 5). Then

  Σ_{v ≠ u} |D({u, v})| = 120 + 5 j_u − τ_u.  (PS)

*Proof.* Σ_{v ≠ u} c(u, v) = 20, where c(u, v) is the number of vertices of R that beat both. A vertex y that misses u misses 10 − q_y further vertices of R. There are 20 + j_u such y, and 10 − q_y = 5 − (q_y − 5), so they contribute 5(20 + j_u) − τ_u. ∎

**Outside contribution to a pair.** For a pair {u, v} let E_both be the sum of (q_y − 5) over those y that miss both u and v, and let c = c(u, v). Every y satisfies t_y := 11 − q_y = 6 − (q_y − 5). Counting the dominators of the nine triples through the pair as in (R1) of the 51-vertex note gives

  s(u, v) := Σ_{w ≠ u, v} (|D({u, v, w})| − 5) = 4 |D({u, v})| − c − 45 − E_both.  (S)

Since c ≤ 4 and s(u, v) ≥ 0, and since the nine triples are among the triples through u,

  s(u, v) ≤ Ex(u).  (B)

(The same bound holds with v in place of u.)

## 2. Vertices of in-degree 25

**Lemma A.** If j_u = 0, then u lies in every Q_y with q_y ≥ 6, c(u, v) ≤ 3 for every v ≠ u, and |D({u, v})| = 12 for every v ≠ u.

*Proof.* By (Ex), Σ λ ≤ 5. Any y with q_y ≥ 7 that misses u contributes λ ≥ 7. Two vertices with q_y = 6 contribute at least 8. So u misses no y with q ≥ 7, and at most one y with q = 6.

Let β ∈ {0, 1} record that one possible 6-vertex, and write m(v) = 1 when that 6-vertex misses both u and v. Then Σ_{v ≠ u} m(v) = 4β. The same congruence as (R3) in the 51-vertex note still holds, because a 6-vertex contributes a multiple of the same residue: s(u, v) ≡ 3 − c(u, v) − m(v) (mod 4). Hence

  Σ_v s(u, v) ≥ Σ_v (3 − c − m) + 4 N_4 = 10 − 4β + 4 N_4,

where N_4 is the number of v with c + m ≥ 4. On the other hand Σ_v s(u, v) = 2 Ex(u) = 2(5 − 4β) = 10 − 8β. Therefore N_4 + β ≤ 0, so β = N_4 = 0.

Now every y that misses u is a 5-vertex, there are 20 of them, and Σ_v s = 10 = Σ_v (3 − c). So s(u, v) = 3 − c(u, v) for every v, which forces c ≤ 3, and (S) with E_both = 0 and |D| = c + k gives k = 12 − c. Thus |D({u, v})| = 12. ∎

Let V_0 = {r ∈ R : j_r = 0} and V_+ = R \ V_0. Lemma A says that every y with q_y ≥ 6 misses only vertices of V_+. If s = |V_+|, such a y misses t ≤ s vertices, so q_y ≥ 11 − s and its excess q_y − 5 = 6 − t lies in {6 − s, …, 6}. Also Σ_{V_+} j_r = J and s ≤ J.

## 3. The case J = 3

Then (E) gives total excess 11, and s ≤ 3. A heavy vertex misses at most s ≤ 3 vertices of R, so its excess lies in {3, 4, 5, 6}.

**s = 1.** One vertex s_* with j = 3. Excesses lie in {5, 6}, and 11 = 6 + 5 is the only such partition: one vertex of q = 11 and one of q = 10, the latter missing s_*. Then τ_{s_*} = 5, and (PS) says the ten pairs from s_* to V_0 sum to 120 + 15 − 5 = 130. Lemma A says each equals 12, so the sum is 120. Contradiction.

**s = 2.** Vertices s_1, s_2, with {j} = {2, 1} in some order. Excesses lie in {4, 5, 6}, and the only partition of 11 is 6 + 5: one q = 11 and one q = 10, the latter missing exactly one of s_1, s_2. Let τ_i be the excess of the heavy vertices that miss s_i, so one of τ_1, τ_2 is 5 and the other is 0. The unique pair between them has, by (PS) and the nine pairs into V_0,

  |D({s_1, s_2})| = 12 + 5 j_i − τ_i

for both i. The assignment τ = 5 on the vertex with j = 1 gives 17 on one side and 12 on the other. The assignment τ = 5 on the vertex with j = 2 gives 17 from both sides. So j(s_1) = 2, the q = 10 vertex misses s_1 only, and |D({s_1, s_2})| = 17.

No heavy vertex misses both endpoints, so E_both = 0 and (S) gives s(s_1, s_2) = 4·17 − c − 45 = 23 − c ≥ 19. But Ex(s_1) = 5 + 20 − λ(10) = 15. This contradicts (B).

**s = 3.** Three vertices, each necessarily with j = 1. Excesses lie in {3, 4, 5, 6}. The partitions of 11 are 6 + 5, 5 + 3 + 3 and 4 + 4 + 3.

* 5 + 3 + 3 is one q = 10 and two q = 8. Each q = 8 misses all three vertices of V_+, so each of them has λ ≥ 9 + 9 = 18 > 15, contradicting (∗).
* 4 + 4 + 3 is two q = 9 and one q = 8. The q = 8 already contributes λ = 9 at every vertex of V_+, and a q = 9 contributes 10 more at two of them, so those two have λ ≥ 19 > 15.
* 6 + 5 is one q = 11 and one q = 10, the latter missing a single vertex s_1. The other two vertices s_2, s_3 of V_+ have τ = 0, and τ_{s_1} = 5. Writing D_{ij} = |D({s_i, s_j})| and applying (PS) against the eight vertices of V_0,

  D_{12} + D_{13} = 24,  D_{12} + D_{23} = 29,  D_{13} + D_{23} = 29.

  Hence D_{12} = D_{13} = 12 and D_{23} = 17. The heavy vertices do not miss both s_2 and s_3, so s(s_2, s_3) = 23 − c ≥ 19. But Ex(s_2) = 5 + 10 − 0 = 15.

All three partitions fail. So J ≠ 3.

## 4. The case J = 4

Total excess 10, and s ≤ 4.

**s = 1.** Excesses lie in {5, 6}. The only partition of 10 is 5 + 5: two vertices of q = 10, both missing the unique positive vertex s_*. Then τ = 10 and (PS) gives sum 120 + 20 − 10 = 130, while Lemma A gives 10 · 12 = 120.

**s = 2.** Excesses in {4, 5, 6}. The partitions of 10 are 6 + 4 and 5 + 5. The j-values are (3, 1) or (2, 2). (PS) forces

  5 j_1 − τ_1 = 5 j_2 − τ_2,  |D| = 12 + 5 j_1 − τ_1.

* (6, 4), both j = 2. The q = 9 misses both, so τ_1 = τ_2 = 4 and |D| = 18. That vertex contributes nothing to the nine triples (it misses no third vertex of R), and s = 23 − c ≥ 19, while Ex = 5 + 20 − 10 = 15.
* (5, 5), both j = 2. Equality of the τ's forces each endpoint to be missed by one q = 10. Then |D| = 17, E_both = 0, s ≥ 19, and Ex = 15 again.
* (5, 5), j = (3, 1). Then τ on the j = 3 vertex is 10 and τ on the other is 0: both q = 10 miss the j = 3 vertex. |D| = 17, E_both = 0, s ≥ 19, Ex at the j = 3 vertex is 5 + 30 − 20 = 15.
* (6, 4) cannot put τ = 0 on either vertex, so it is incompatible with j = (3, 1).

**s = 3.** Excesses in {3, 4, 5, 6}, j-values (2, 1, 1). The partitions of 10 are 6 + 4, 5 + 5 and 4 + 3 + 3.

* 5 + 3 + 3: two vertices of q = 8 miss all three positive vertices, so λ ≥ 18 > 15 at each j = 1 vertex.
* 4 + 3 + 3: the q = 8 misses all three, and each q = 9 misses two. Any vertex missed by the q = 8 and a q = 9 has λ ≥ 19 > 15, but every vertex is missed by the q = 8.
* 6 + 4: one q = 9, missing two of the three positive vertices. If it misses the two vertices of j = 1, (PS) gives a pair-dominator count 8 < 11 between them. If it misses the j = 2 vertex and one j = 1 vertex, the pair from the j = 2 vertex to the untouched j = 1 vertex has 17 dominators, E_both = 0 and s ≥ 19, while the untouched vertex has Ex = 15.

**s = 4.** Four vertices of j = 1. Excesses in {2, 3, 4, 5, 6}. For each positive vertex the three pairs into V_+ sum to 41 − τ_i, and summing over the four vertices counts every pair twice:

  Σ |D| = 82 − (Σ τ)/2,  Σ τ = Σ_y (q_y − 5)(11 − q_y).

The value (q − 5)(11 − q) is 0, 5, 8, 9, 8, 5 for excesses 6, 5, 4, 3, 2, 1 respectively. Combined with (∗) at j = 1, which allows λ-sum at most 15, every partition of 10 fails:

| partition of the excess | why it fails |
|---|---|
| 6 + 4 | the untouched pair has 17 dominators and s ≥ 19, but Ex = 15 there |
| 5 + 5 | the pair of untouched vertices has 11 dominators, so s < 0 |
| 6 + 2 + 2 | every pair is missed by both q = 7 vertices, so E_both ≥ 4, and the total 74 forces some pair with only 12 dominators, for which s < 0 |
| 5 + 3 + 2 | the q = 7 and the q = 8 together put λ ≥ 16 on three of the four vertices |
| 4 + 4 + 2 | each q = 7 contributes λ = 7 everywhere and each q = 9 contributes 10 on two vertices; pigeonhole puts both on some vertex |
| 4 + 3 + 3 | two vertices of q = 8 share at least two missed vertices, and those have λ ≥ 18 |
| 4 + 2 + 2 + 2 | three vertices of q = 7 give λ ≥ 21 everywhere |
| 3 + 3 + 2 + 2 | a vertex missed by both q = 8 has λ ≥ 18 |
| 2 + 2 + 2 + 2 + 2 | λ ≥ 35 |

(The same pigeonhole kills every partition that contains two or more vertices of q ≤ 8 together with a vertex whose miss-set is forced to meet them.) So J ≠ 4.

## 5. The boundary J = 5 forces s ≥ 4

Total excess is now 9.

**s ≤ 2.** For s = 1 the excesses lie in {5, 6} and cannot add to 9. For s = 2 they lie in {4, 5, 6} and the only partition is 5 + 4. The q = 9 misses both positive vertices and the q = 10 misses one of them. Comparing (PS) at the two vertices forces the j-values to be 3 and 2, with the q = 10 missing the vertex of j = 3, and gives |D| = 18 on the pair between them. As in §3, s(pair) ≥ 19, while the vertex of j = 2 has Ex = 5 + 20 − 10 = 15.

**s = 3.** Excesses lie in {3, 4, 5, 6}. The partitions of 9 are 6 + 3, 5 + 4 and 3 + 3 + 3.

* 3 + 3 + 3: three vertices of q = 8 miss all three positive vertices, so λ ≥ 27 at the vertex with j = 1 (every composition of 5 into three positive parts has a part equal to 1).
* 6 + 3: the q = 8 misses all three, each τ equals 3, and (PS) produces a pair with 8 dominators.
* 5 + 4: one q = 10 and one q = 9. For both j-shapes (3, 1, 1) and (2, 2, 1), every choice of which vertices are missed leads to one of: λ > 5 + 10 j at a vertex, a pair with fewer than 11 dominators, or a pair with s ≥ 19 whose endpoint has Ex ≤ 15.

Thus s ≥ 4 whenever J = 5. Since s ≤ J, the case J = 5 has s ∈ {4, 5}.

## 6. Proof of the theorem

J ≤ 2 is Theorem 1 of `F4_GE_52_HAND_PROOF.md`, valid at every order. Sections 3 and 4 exclude J = 3 and J = 4 at N = 52. Section 5 is the second sentence. ∎

## 7. A remark on the balanced score sequence

Separately, if every in-degree is 25 or 26, then exactly 26 vertices have each value, because the in-degrees sum to 52 · 25 + 26. In that case

  Σ_Y C(k(Y), 2) = Σ_{w ≠ w′} C(|N⁺(w) ∩ N⁺(w′)|, 3) ≥ 314028,

the minimum being taken when 338 pairs have 13 common out-neighbours and the other 988 have 12. If every triple had only 5 or 6 dominators, the same sum would be at most 305500. So some triple would have at least 7 dominators. This is consistent with (F1) and is recorded only as a constraint; the degree sequence at N = 52 need not be balanced.

## 8. No in-degree equals 23

**Lemma B.** In an S_4 tournament on 52 vertices every in-degree is at least 24.

*Proof.* By (F3), d⁻ ≥ 23. Suppose d⁻(v) = 23, and put A = N⁻(v), B = N⁺(v), so |A| = 23 and |B| = 28.

As in Corollary 2 of `F4_GE_52_HAND_PROOF.md`, T[A] is 11-regular, every pair {a, v} is tight with dominator set R_a = N⁻_A(a), and e ≥ 0 on A. The same count that gives |D({v, a, a′})| ≥ 5, summed over pairs of A, equals Σ_x C(11, 2) = 1265 = 5·C(23, 2). So every pair in A has exactly 5 common in-neighbours in A. In an 11-regular tournament that forces every pair to have exactly 5 common out-neighbours as well: if u → u′, the usual split of the other 21 vertices gives λ⁺ = λ⁻. Thus T[A] is a DRT(23), and the sets R_a are the blocks of a symmetric 2-(23, 11, 5) design.

Each a ∈ A beats 14 − e(a) vertices of B, and each b ∈ B is beaten by at least 11 vertices of A, so Σ_A e ≤ 322 − 308 = 14. At least 9 vertices of A have e = 0. Call that set A_0.

For the tight pair {a, v}, the identity (E) says the excess Σ (q − 5) is at most 11. A vertex b with A ∩ N⁻(b) = R_a contributes 6, so at most one vertex of B meets A in the block R_a.

Now fix r ∈ A_0 and b ∈ B with b → r. For every a ∈ N⁺_A(r) one has r ∈ R_a and e(r) = 0, so Lemma A gives |R_a ∩ A_b| = 5. There are 11 such a, and

  Σ_a |R_a ∩ A_b| = Σ_{x ∈ A_b} |N⁺_A(r) ∩ N⁺_A(x)| = 5 |A_b|,

since r ∉ A_b and every other pair has 5 common out-neighbours. Thus |A_b| = 11. The 23 numbers x_a = |A_b ∩ R_a| − 5 are nonnegative and sum to 11·11 − 5·23 = 6. Their squares sum to

  11·11 + 11·10·5 − 10·121 + 25·23 = 36 = (Σ x_a)²,

by the usual design count of pairs inside A_b. For nonnegative numbers, Σ x² = (Σ x)² forces a single nonzero term. So A_b equals one block R_{a_b}. Since r ∉ A_b, the vertex a_b lies in the 12-set {r} ∪ N⁻_A(r).

But d⁻(r) = 25 and r already has 11 in-neighbours in A, and r → v, so r has 14 in-neighbours in B. Each of them produces a different a_b in that 12-set, because distinct vertices of B cannot meet A in the same block. 14 ≤ 12 is false. ∎

## 9. The excess on a tight pair meets at least four dominators

**Lemma C.** If P is tight in an S_4 tournament on 52 vertices, then at least four vertices of D(P) have in-degree greater than 25.

Sections 3–5 already give this when J ≤ 5. The remaining cases are J ≥ 6 with s = |V_+| ≤ 3. A heavy vertex misses at most s vertices of R, so its excess q − 5 lies in {6 − s, …, 6}. Write D_ij = |D({s_i, s_j})| for the vertices of V_+. By (PS) and Lemma A,

  Σ_{j ≠ i} D_ij = 12(s − 1) + 5 j_i − τ_i,

and a pair with E_both = 0 and D ≥ 17 has s(pair) ≥ 19.

**s = 1.** The single positive vertex is missed by every heavy vertex, and its ten pairs into V_0 all have 12 dominators, so (PS) reads 120 = 120 + 5J − τ. The only partitions of E = 14 − J into parts in {5, 6} are E = 5 and E = 6, giving τ = 5 and τ = 0. Neither satisfies the equation. No other E is a sum of such parts.

**s = 2.** Parts lie in {4, 5, 6}, so E ∈ {4, 5, 6, 8} (E = 7 and E ≤ 3 cannot be built, and E ≥ 9 is J ≤ 5, already done). In each surviving partition the two expressions for the single pair agree only for one degree pattern, and that pattern has at least 19 triple-excess against a budget of at most 15:

| E | partition | degrees | |D| of the pair | why it fails |
|---|---|---|---|---|
| 8 | 4 + 4 | 3, 3 | 19 | E_both = 8, excess ≥ 19, budget 15 |
| 6 | 6 | 4, 4 | 32 | excess ≥ 79, budget 45 |
| 5 | 5 | 5, 4 | 32 | excess ≥ 79, budget 45 |
| 4 | 4 | 5, 5 | 33 | excess ≥ 79, budget 45 |

**s = 3.** Parts lie in {3, 4, 5, 6}, and J ≥ 6 forces E ≤ 8, so there are at most two heavy vertices. Throughout, Ex(i) = 5 + 10 j_i − Σ λ on the heavy vertices that miss i, and a pair with E_both = 0 and D dominators has triple-excess at least 4D − 49. The three pair-dominator counts are written D, D′, D″.

* *E = 8, both heavy vertices of excess 4, missing the same pair.* The untouched vertex Z has j_Z = 1 and the opposite pair has 14 dominators; one of the other two degrees is then 3 and its pair with Z has 17 dominators. That pair has E_both = 0, so triple-excess at least 19, while Z has Ex = 15.
* *E = 8, the two excesses 4 miss different pairs.* Their common vertex X has λ = 20, so j_X ∈ {2, 3}. If j_X = 2 the opposite pair has 17 dominators and triple-excess at least 19, against Ex ≤ 15 at a degree-2 endpoint. If j_X = 3 the opposite pair has 12 dominators and one of the other two degrees is 2, whose pair with X has 18 dominators; E_both = 4 there, so triple-excess at least 19 against Ex = 15.
* *E = 8, excesses 5 and 3.* The excess-3 vertex misses all three. The vertex X missed by the excess-5 vertex has j_X ∈ {2, 3}. If j_X = 2 the opposite pair has 18 dominators and, with E_both = 3, triple-excess at least 20, while the two endpoints share degree-excess 4 and cannot both have Ex ≥ 20. If j_X = 3 the opposite pair has 13 dominators and one endpoint has degree excess 2, giving a pair of 18 dominators and triple-excess at least 20 against Ex = 16.
* *E = 7, excesses 4 and 3.* The untouched vertex Z has j_Z ∈ {1, 2}, because j_Z ≥ 3 makes the opposite pair have fewer than 11 dominators. If j_Z = 1 that pair has 19 dominators and E_both = 7, so triple-excess at least 20, forcing both endpoints to have degree excess at least 4 and total degree excess at least 9. If j_Z = 2 the pair has 14 dominators and one endpoint has degree excess 3, whose link to Z has 18 dominators and triple-excess at least 20 against Ex(Z) = 16.
* *E = 6, one vertex of excess 6.* It misses nobody, so every pair has E_both = 0. No degree exceeds 4, or the opposite pair has fewer than 11 dominators. The compositions of 8 are then (4, 3, 1), (4, 2, 2) and (3, 3, 2). Opposite the part 1 the pair has 27 dominators and triple-excess at least 59, against Ex ≤ 45. Opposite a part 2 the pair has 22 dominators and triple-excess at least 39, against Ex = 25 when the parts are (4, 2, 2) and against Ex = 35 when they are (3, 3, 2).
* *E = 6, two vertices of excess 3.* Both miss all three positive vertices, so every degree is at least 2 and every pair has E_both = 6. A part 4 makes the opposite pair have fewer than 11 dominators, leaving (3, 3, 2). Opposite the part 2 the pair has 19 dominators and triple-excess at least 21, against Ex = 17.
* *E = 5, one vertex of excess 5, missing X.* No degree exceeds 5. If j_X ≤ 3 the opposite pair has at least 22 dominators and triple-excess at least 39, against Ex ≤ 35. If j_X = 4 the two other degrees are 2 and 3, and the pair from X to the degree-3 vertex has 22 dominators and triple-excess at least 39 against Ex = 35. If j_X = 5 every split of the remaining 4 puts at least 19 of triple-excess on an endpoint of degree excess 1, whose budget is 15, or at least 39 on an endpoint of degree excess 2, whose budget is 25.
* *E = 4, one vertex of excess 4, missing X and Y and not Z.* If j_Z = 1 the missed pair has 28 dominators and triple-excess at least 59; if j_Z = 2 it has 23 dominators and triple-excess at least 39. Either way both missed vertices would need degree excess at least 5, and the remaining excess is at most 8. If j_Z = 3 the missed pair has 18 dominators and one of X, Y has degree excess at least 4; that vertex’s pair with Z has 22 dominators and triple-excess at least 39, against Ex = 35 at the degree-4 end and Ex = 45 at Z. If j_Z = 4 the splits (3, 3), (4, 2) and (5, 1) produce a pair with 22, 27 and 32 dominators, hence triple-excess at least 39, 59 and 79, against budgets 25, 35 and 45. If j_Z ≥ 5 the missed pair has fewer than 11 dominators.
* *E = 3, one vertex of excess 3, missing all three.* Every pair has E_both = 3, and some degree is at most 3. Opposite a part 1, 2 or 3 the pair has 33, 28 or 23 dominators, and the triple-excess is at least 80, 60 or 40. The endpoints would need degree excess at least 9, 7 or 5 respectively, which does not fit in the remaining degree excess.

E ≤ 2 is not a sum of integers ≥ 3. So s ≤ 3 is impossible, which is Lemma C. ∎
