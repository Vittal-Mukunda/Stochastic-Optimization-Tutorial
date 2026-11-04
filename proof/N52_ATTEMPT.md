# N = 52: towards f(4) ≥ 53 (hand work, in progress)

*Started 20 October 2026. Hand derivations only. Builds on `F4_GE_52_HAND_PROOF.md` (cited as [52]) and
`ERDOS902_PROOF.md` (cited as [EP]). Notation as there: e(x) = d⁻(x) − 25, λ(P) = |D(P)|.*

Throughout, T is a tournament on N = 52 vertices in which every triple has at least 5 dominators (F1).
Σ_v d⁻(v) = C(52, 2) = 1326 = 52·25.5, so **Σ_v e(v) = 26**.

## 1. Tools from [52] used here (valid for every N)

* **(TH1)** Every tight pair P has J(P) = Σ_{r ∈ D(P)} e(r) ≥ 3 (all terms ≥ 0 by Lemma T).
* **(SF)** Let P be tight, R = D(P), O = V \ (P ∪ R), Q_y = R ∩ N⁻(y), and let r ∈ R have d⁻(r) = 25. Then every
  y ∈ O with y → r has q_y = 5; also c(r, w) ≤ 3 and |D({r, w})| = 12 for all w ∈ R \ {r}.
  (Re-derived: with k_q(u, w) = #{y : q_y = q, u, w ∉ Q_y}, s(u, w) = 3c + 4k_5 + 3k_6 + 2k_7 + k_8 − 45 and
  Σ_w s(r, w) = 10 + 20 j_r − 8β_6 − 14β_7 − 18β_8 − 20γ; at j_r = 0 this forces β_{≥7} = 0, β_6 ≤ 1, then the
  mod-4 rounding forces β_6 = N_4 = 0 and s(r, w) = 3 − c(r, w), k_5 = 12 − c.)
* **(I2) at N = 52.** For a tight pair, Σ_{y ∈ O} (q_y − 5) = 6N − 298 − J = **14 − J ≤ 11**.

## 2. Lemma 1: no vertex has in-degree 23 (N = 52)

Let d⁻(v) = 23, A = N⁻(v), B = N⁺(v), |B| = 28.

1. As in [52] Cor. 2: T[A] is 11-regular, each {a, v} (a ∈ A) is tight with R_a := D({a, v}) = N⁻_A(a), and
   e ≥ 0 on A (Lemma T).
2. **T[A] is a DRT(23).** For a ≠ a′ in A, D({v, a, a′}) = N⁻_A(a) ∩ N⁻_A(a′) has ≥ 5 elements (F1), and these
   numbers add up to Σ_x C(11, 2) = 23·55 = 1265 = 5·C(23, 2). So all equal 5, and (regularity) every pair of A
   also has exactly 5 common out-neighbours in A. The sets R_a form a symmetric 2-(23, 11, 5) design.
3. **Arc count.** a ∈ A beats 51 − d⁻(a) − 12 = 14 − e(a) vertices of B; each b ∈ B is beaten by
   |A_b| = |D({v, b})| ≥ 11 vertices of A (A_b := A ∩ N⁻(b)). So 308 ≤ 322 − E with E = Σ_A e, i.e. E ≤ 14.
   Hence A_0 := {r ∈ A : e(r) = 0} has at least 23 − 14 = 9 elements.
4. **At most one b per block.** For a ∈ A, b ∈ B with A_b = R_a has q_b = 11 for the tight pair {a, v}, so it
   contributes 6 to Σ_{y}(q_y − 5) = 14 − J_a ≤ 11 (TH1). So at most one b ∈ B has A_b = R_a.
5. **Key step.** Let r ∈ A_0 and b ∈ B with b → r. For each of the 11 vertices a ∈ N⁺_A(r) we have r ∈ R_a, and
   (SF) for the tight pair {a, v} gives |R_a ∩ A_b| = 5. Summing,
   55 = Σ_{a ∈ N⁺_A(r)} |R_a ∩ A_b| = Σ_{x ∈ A_b} |N⁺_A(r) ∩ N⁺_A(x)| = 5|A_b| (r ∉ A_b, design property).
   So |A_b| = 11. Then over all 23 blocks, with x_a := |A_b ∩ R_a| − 5 ≥ 0:
   Σ_a x_a = 11·11 − 115 = 6 and Σ_a x_a² = (11·11 + 11·10·5) − 10·121 + 25·23 = 36 = (Σ x_a)².
   So exactly one a_b has x = 6, i.e. **A_b = R_{a_b}**. As r ∉ A_b = N⁻_A(a_b), a_b ∈ {r} ∪ N⁻_A(r).
6. **Contradiction.** r has 25 − 11 = 14 in-neighbours in B. By step 5 each gives an a_b in the 12-set
   {r} ∪ N⁻_A(r), and by step 4 distinct b give distinct a_b. So 14 ≤ 12. ∎

So **every in-degree is at least 24**, and by Claim Q ([EP] Lemma 2.3, valid for all N) Z = {v : d⁻(v) = 24} has
|Z| ≤ 5 and every v ∈ Z has at most 2 in-neighbours in Z.
