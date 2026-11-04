# Order 52: every tight pair has J ≥ 6

Written 24 October 2026. Erdős 902 is not solved by this note. It removes the cell J = 5 from the order-52 tight-pair tree and
re-checks J ≤ 4 independently of R1-C, R3-C and R4-C.

Notation is that of `proof/F4_GE_52_HAND_PROOF.md` §2 and `research/AGENT_TASKS/R4-C-tight-s4.report.json`: T has S_4 on 52
vertices, P = {a, b} is tight, R = D(P), O = V \ (P ∪ R) with |O| = 39, Q_y = R ∩ N⁻(y), M_y = R \ Q_y, e_y = |Q_y| − 5,
d⁻(r) = 25 + j_r, J = Σ j_r, V_0 = {r : j_r = 0}, c(u, v) = |N⁻(u) ∩ N⁻(v) ∩ R|, E_both(u, v) = Σ_{y : u, v ∈ M_y} e_y.

## 1. The missing constraint: c(u, v) ≥ 1 for every pair of R

For u, v ∈ R the 4-set {a, b, u, v} has a dominator w. It beats a and b, so w ∈ D(P) = R, and it beats u and v. Hence
**T[R] has S_2 and c(u, v) ≥ 1.** The order-51 proof records this (the 551 classes are the S_2 ones), but the order-52 case
analyses in R1-C, R3-C, R4-C, R5-C and R6-C only use c ≥ 0.

Consequences.
* R4-C's unique survivor at J = 5, s = 4 forces |D({C, D})| = 12, E_both(C, D) = 3 and therefore triple excess
  s(C, D) = 4·12 − c − 45 − 3 = −c, i.e. c(C, D) = 0. That contradicts c ≥ 1. **The cell J = 5, s = 4 is empty.**
* The 11-vertex tournament of R5-C (used again by R6-C) has N⁻(2) = {0, 1, 3, 8, 10} and N⁻(3) = {4, 5, 6, 7, 9}, so
  c(2, 3) = c(C, D) = 0. It is not S_2 and cannot be T[R]. R7-C's search for "another such tournament" is moot: every
  candidate needs c(C, D) = 0. `research/compute/r7c_filter.py` confirms that none of the 551 classes has a labelling
  meeting R4-C's windows.

## 2. J = 5, s = 5 by hand

Here j = 1 on V_+ = {five vertices}, |V_0| = 6, heavy excess 14 − J = 9. Tools (all from R4-C/Lemma A, valid for every J):
heavy vertices miss only V_+; a heavy vertex of excess e misses 6 − e vertices of V_+; for u ∈ V_+ the four pairs into V_+
have dominator counts summing to 53 − τ_u (τ_u = Σ_{y : u ∈ M_y} e_y), because the six pairs into V_0 have 12 each;
s(u, v) = 4|D(u, v)| − c − 45 − E_both ∈ [0, Ex(u)], Ex(u) = 15 − Σ_{y : u ∈ M_y} λ(q_y).
From s ≥ 0 and c ≥ 1: **|D(u, v)| ≥ ⌈(46 + E_both)/4⌉**, so |D| ≥ 13 whenever E_both ≥ 3.

Every |D| ≥ 12 gives τ_u ≤ 5. Among the partitions of 9 into parts 1..6, this and Σ e(6 − e) ≤ 25 leave
6+3, 6+2+1, 6+1+1+1, 5+4, 5+2+2, 4+4+1 (5+3+1, 5+2+1+1, 5+1⁴ put τ ≥ 6 on the vertex missed by the 5; 4+3+2 puts τ ≥ 6 on
some vertex; the rest have Σ e(6 − e) > 25).

* **6+3** (the 3 misses {x₁, x₂, x₃}): pair sums 50, 50, 50, 53, 53. The three pairs inside {x₁, x₂, x₃} have E_both = 3,
  so |D| ≥ 13; summing at x₁, x₂, x₃ forces them to be exactly 13 and all six cross pairs 12. The last pair {w₁, w₂} then
  has 53 − 36 = 17 dominators and s = 23 − c ≥ 19 > Ex = 15.
* **6+2+1**: the four vertices missed by both heavies have pair sums 50 and their six internal pairs have E_both = 3,
  so they sum to at least 78; but summing at those four and subtracting the fifth vertex's sum 52 gives 74.
* **6+1+1+1**: every pair has E_both = 3, so the ten pairs sum to at least 130, but the pair sums give 5·50/2 = 125.
* **5+4**: the vertex missed by the 5 has all four pairs equal to 12; the pair missed by the 4 has E_both = 4, so |D| ≥ 13
  even with c ≥ 0; this forces its four cross pairs to 12 and the remaining pair to 17, with s ≥ 19 > 15.
* **5+2+2**: both 2's miss the four vertices not missed by the 5; those have pair sum 49 with one pair to the 5's vertex
  equal to 12, leaving 37 for three pairs with E_both = 4, each ≥ 13.
* **4+4+1**: a vertex missed by a 4 has pair sum 48, one pair with E_both = 5 (|D| ≥ 13) and three others ≥ 12: 49 > 48.

**So J = 5 is impossible.** With R1-C (J ≥ 5) this gives J ≥ 6. The three 6+x cases are exactly where c ≥ 1 is needed;
`research/compute/n52_s5_patterns.py` checks all 83 heavy patterns up to symmetry and agrees: without c ≥ 1 only those
three survive, with it none do.

## 3. Independent computer check of J ≤ 5

`research/compute/n52_pairlevel.py` encodes, for each partition of J (0 ≤ J ≤ 14) placed on R, the pair-level system:
T[R] as 55 arc variables (5-regular, c ≥ 1), (I1), Lemma I, Lemma A, the pair identity |D| = c + #{y : u, v ∈ M_y},
s(u, v) = 4|D| − c − 45 − E_both with 0 ≤ s ≤ Ex, Σ_v s(u, v) = 2Ex(u), and the light vertices through their pair counts.
Every row is a consequence of S_4. CP-SAT, all instances decided:

| J | partitions | infeasible | feasible |
|---|---|---|---|
| 0–5 | 19 | 19 | 0 |
| 6 | 11 | 8 | 3: (2,2,1,1), (2,1,1,1,1), (1⁶), each with heavy 6+2 |
| 7–14 | 471 | 268 | 203 |

Cross-checks: replacing T[R] by free integers c ∈ [1, 4] with row sums 20 gives the same verdict for J ≤ 6. With c ≥ 0
instead of c ≥ 1 the model reproduces the repository's earlier results exactly: J ≤ 4 infeasible (R1-C), and at J = 5 only
(2,1,1,1) (R4-C's cell) and (1⁵) (the open R8-C cell) survive. Dropping Lemma A does not change any verdict, consistent with
it being derived from the same rows. A full local model (individual outside vertices, all triple and 4-set rows of R, the
U + a and U + b rows) was also written (`n52_full.py`, `n52_tight_local.py`, `n52_tight_cpsat.py`); CP-SAT and HiGHS did not
decide it within 5 minutes per instance, so it adds nothing yet.

## 4. Where this leaves order 52

* Tight-pair branch: J ∈ [6, 14]; 206 j-partitions survive the pair-level system. Corollary 3's spectral step does not
  transfer: at order 52 the off-diagonal row sum of a tight row is 14 − J, which is below the diagonal 6 only when J ≥ 9.
* No-tight branch: untouched. It forces the equality margin of Lemma S1 (every in-degree 25 or 26; each in-degree-25 vertex
  has a 12-regular in-neighbourhood), and R4-B/R5-B show the global moments do not exclude it.
* Bounds unchanged: 52 ≤ f(4) ≤ 67, and (c* − o(1)) n 2ⁿ ≤ f(n) ≤ (ln 2 + o(1)) n² 2ⁿ.
