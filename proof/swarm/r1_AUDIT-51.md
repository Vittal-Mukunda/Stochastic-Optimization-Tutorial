# AUDIT-51: hostile audit of the f(4) ≥ 52 proof and of the prerequisites it takes from [EP]

*Round 1, lane AUDIT-51, 23 October 2026. Hand derivation only: no script, solver or search was run, and nothing in
the archives was executed. Every number below was computed by hand and re-checked a second time (§11).*

Citations. [52] = `F4_GE_52_HAND_PROOF.md`. [EP] = `ERDOS902_PROOF.md`. [A52] = `N52_ATTEMPT.md`.
[TP] = `N52_TIGHT_PAIRS.md`. "F1-tournament" = a tournament in which every triple has at least 5 dominators.

---

## 0. Verdict

**I found no false statement in [52] or in the audited parts of [EP].** The chain

 Theorem A → Theorem 1 → Corollary 2 → Corollary 3 → Corollary 4 → Theorem 5 → f(4) ≥ 52

is correct, line by line, as a proof that no F1-tournament (hence no S_4 tournament) has at most 51 vertices.

Two proofs in the closing paragraphs of [52] §2 are **incomplete as written**, although the statements are true:

* **G1.** "Theorem 1 holds for every N". The text says that (∗), (R1)–(R3) and the rounding lemma "hold verbatim". They do
  not: Lemma P is a statement about N = 51 only, the proof of (R3) uses the bound c + m ≤ 6 that comes from Lemma P, and the
  step "no 6-vertex" is attributed to Step 1 instead of Step 2. The fill is in §5 (Theorem 1′), and it also gives a
  proof of Theorem 1 at N = 51 that does not use Lemma P.
* **G2.** The structural fact "r ∈ D(P) with d⁻(r) = 25 lies in every Q_y with q_y ≥ 6, c(r, v) ≤ 3, |D({r, v})| = 12".
  The text invokes "the rounding lemma as written", but that lemma is stated under the hypotheses J ≤ 2 and Lemma P.
  The fill is in §4 (Proposition SF): a self-contained proof, for every N and every tight pair, with the 7- and 8-vertices
  included.

Neither gap touches the N = 51 chain (where all hypotheses used are in force). Both are load-bearing for the N = 52
programme ([A52] Lemma 1, [TP] Lemma A, and J ≥ 3 at N = 52). Both are now filled.

### 0.1 Verdict table

| ID | claim | verdict |
|---|---|---|
| E1 | [EP] Lemma 1.1 | correct |
| E2 | [EP] Lemma 1.2 (D(A) undominated, \|D(A)\| ≥ n+1) | correct |
| E3 | [EP] Lemma 1.3 and the regularity statement | correct |
| E4 | (F1), (F2), (F3), "tight ⇒ 5-regular" | correct, and valid for every F1-tournament, every N |
| E5 | [EP] Lemma 2.1 = Lemma T (d⁻ ≥ 25 on a tight dominator set) | correct, every N |
| E6 | [EP] Lemma 2.2 (d⁻(v) = 23 ⇒ N ≥ 51) | correct |
| E7 | [EP] Lemma 2.3 = Claim Q, including "≥ 12 tight partners" | correct, every N |
| E8 | [EP] Theorem A (N ≥ 51) | correct |
| S1 | [52] (2.1), (I1), (I2), (I3) | correct (numerical forms are N = 51; general forms in §3.1) |
| S2 | [52] (∗) and the λ table | correct, N-free |
| S3 | [52] Lemma P | correct, **N = 51 only** |
| S4 | [52] (R1), (R2) | correct |
| S5 | [52] (R3) and "s ≥ 7 − c − m when c + m ≥ 4" | correct; the side remark "c + m ≤ 6" is N = 51 only, the inequality holds for every c + m (fill G3, §3.3) |
| S6 | [52] rounding lemma | correct (as written it is an N = 51 statement) |
| S7 | [52] Steps 1–5, Theorem 1 at N = 51 | correct |
| S8 | [52] "Theorem 1 holds for every N" | **statement true; written proof incomplete; correct after fill G1 (§5)** |
| S9 | [52] structural fact for d⁻(r) = 25 | **statement true; written proof incomplete; correct after fill G2 (§4)** |
| S10 | [52] Corollary 2 | correct |
| S11 | [52] Corollary 3, steps 1–5 (Weyl, interlacing, 26 zero eigenvalues, n_t ≤ 28 − W, Claim Q) | correct; interlacing directions right; an interlacing-free proof of step 4 is in §6.2 |
| S12 | [52] Corollary 4 and the pair count 15300 | correct |
| S13 | [52] (M0)–(M4) | correct |
| S14 | [52] algebra, positivity, counting, Theorem 5 | correct |
| S15 | [52] §5 conclusion and the remarks (variance 0.845 / 0.498, sharpness, QR_19 check, class-0 c-values) | correct (checked); the "1101 computer certificates" remark is not part of the proof and I did not check it |

### 0.2 Ranked list of defects

All are gaps in write-up. None is a false claim.

1. **G1** ([52] §2, "Theorem 1 holds for every N"): proof incomplete as written. Damage to f(4) ≥ 52: none. Damage to N = 52:
   high if unfilled (every result of [TP] uses J ≥ 3 at N = 52), none now.
2. **G2** ([52] §2, the d⁻(r) = 25 structural fact): proof cites a lemma outside its hypotheses. Damage to f(4) ≥ 52: none.
   Damage to N = 52: high if unfilled ([A52] Lemma 1 step 5, [TP] Lemma A, and the whole case analysis rest on it); none now.
   (TP Lemma A contains an independent correct proof of the j = 0 case; see §8.)
3. **G3** ((R3) proof): "Here c + m ≤ 4 + 2 = 6" and "if 4 ≤ c + m ≤ 6, the least non-negative number is 7 − c − m" are valid
   only under Lemma P (m ≤ 2). The stated consequence "s ≥ 7 − c − m when c + m ≥ 4" is true for every c + m (§3.3).
4. **G4** (hazards): Lemma P ("exactly one y* with q ≥ 9") is false in general for N > 51: under J ≤ 2 there are N − 50
   big vertices (§5). Corollaries 2, 3, 4 and Theorem 5 use N = 51 numbers throughout; they must not be cited at N = 52 (§10).
5. **G5** (cosmetic): "With no 6-vertex (Step 1)" should read Step 2; the explicit "no 7-, 8-vertices" step is missing
   from the every-N paragraph.

---

## 1. Conventions, and where N enters

Throughout, T is a tournament on N vertices in which every triple has ≥ 5 dominators ("F1-tournament"). An S_4
tournament is one (Lemma 1.2 of [EP]). I checked that [52] never uses the other half of Lemma 1.2 (that D(Y) is
undominated): every statement below is a statement about F1-tournaments.

For a tight pair P = {a, b} (|D(P)| = 11): R = D(P), O = V ∖ (P ∪ R), |O| = N − 13, Q_y = R ∩ N⁻(y) = D(P ∪ {y}) for
y ∈ O, q_y = |Q_y| ≥ 5, d⁻(r) = 25 + j_r, J = Σ_{r∈R} j_r.

### 1.1 N-ledger

| item | N-dependence |
|---|---|
| (F1)–(F3), Lemma T, Claim Q, Theorem A | none (all N) |
| (2.1), (I3), (∗), λ-table, (R1), (R2) | none (all N) |
| (I1): #{y ∈ O : r ∉ Q_y} = 20 + j_r | none. The companion #{y ∈ O : r ∈ Q_y} = N − 33 − j_r (= 18 − j_r at N = 51) |
| (I2): Σ_y (q_y − 5) = 6N − 298 − J | 8 − J at N = 51; 14 − J at N = 52 |
| Lemma P | **N = 51 only** (uses \|O\| = 38 and 8 − J) |
| rounding lemma | as written: N = 51 (Lemma P structure). Re-derived N-free in §4 and §5 |
| Steps 1–5 of Theorem 1 | as written: N = 51. N-free after §5 |
| Corollaries 2, 3, 4; Theorem 5 | **N = 51 only** |

---

## 2. Audit of [EP] (prerequisites)

### 2.1 Lemmas 1.1–1.3, (F1)–(F3)

**Lemma 1.1.** An S_n tournament has N ≥ n + 1 (an n-set needs an outside dominator). A set X with |X| ≤ n extends to an
n-set X′ ⊇ X; a dominator of X′ is outside X′, hence outside X, and beats X. And X ⊆ X′ gives D(X′) ⊆ D(X) directly. Correct.

**Lemma 1.2.** |A| ≤ n − 1, D(A) ≠ ∅ (Lemma 1.1). Suppose z beats all of D(A).
* z ∉ A, since every vertex of D(A) ≠ ∅ beats every vertex of A, so a member of A cannot beat all of D(A).
* z ∉ D(A), since z cannot beat itself.
* |A ∪ {z}| ≤ n, so A ∪ {z} has a dominator w ∉ A ∪ {z}. Then w beats A, so w ∈ D(A), so z → w. But w beats z.
  Contradiction. So D(A) is undominated, hence |D(A)| > n (a set of ≤ n vertices is dominated). Correct.

With n = 4 and |A| = 3 this is **(F1)**: |D(Y)| ≥ 5 for every triple Y.

**Lemma 1.3.** For y ∉ A and R = D(A): w ∈ D(A ∪ {y}) ⇔ w ∉ A ∪ {y}, w beats A, w → y ⇔ w ∈ R ∩ N⁻(y)
(w ∈ R already gives w ∉ A, and w → y gives w ≠ y). This holds for y ∈ R and for y ∉ R. Correct. The in-degree of y ∈ R
in T[R] is |R ∩ N⁻(y)|, so min in-degree of T[R] ≥ ν_{s+1}. For a tournament on m vertices with min in-degree ≥ δ:
C(m,2) ≥ mδ gives m ≥ 2δ + 1; equality forces all in-degrees to equal δ. Correct.

**(F2)** (s = 2): for a pair P, |D(P ∪ {y})| ≥ 5 by (F1), so T[D(P)] has min in-degree ≥ 5, |D(P)| ≥ 11, and each y ∉ P ∪ D(P) has
q_y ≥ 5. If |D(P)| = 11, T[D(P)] is 5-regular. **(F3)** (s = 1): for a ∈ N⁻(v), the in-degree of a in T[N⁻(v)] is
|N⁻(v) ∩ N⁻(a)| = |D({a, v})| ≥ 11, so d⁻(v) ≥ 2·11 + 1 = 23. All of this uses (F1) only. Correct.

### 2.2 Lemma 2.1 (Lemma T): tight pair ⇒ every dominator has d⁻ ≥ 25

P tight, R = D(P), r ∈ R. Triples U ⊆ R with r ∈ U: C(10,2) = 45. Each has ≥ 5 dominators (F1): at least 225 pairs (U, w).
A dominator w beats r; w ∉ P because r beats both vertices of P; so w ∈ N⁻(r) ∖ P.
* w ∈ R: exactly 5 of them beat r (5-regular). w dominates U ⊆ R only if U ⊆ N⁺(w) ∩ R, a 5-set containing r; U ∖ {r} is a
  2-subset of the other 4: C(4,2) = 6. Total ≤ 5·6 = 30.
* w ∈ O: there are d⁻(r) − 5 of them (N⁻(r) has no vertex in P, 5 in R). Each is beaten by ≥ 5 vertices of R (q_w ≥ 5), so
  N⁺(w) ∩ R has ≤ 6 elements, one of which is r. It contains ≤ C(5,2) = 10 of the 45 triples.

So 225 ≤ 30 + 10(d⁻(r) − 5), d⁻(r) ≥ 5 + 19.5 = 24.5, hence d⁻(r) ≥ 25. **Correct, every N** (no N is used).

### 2.3 Lemma 2.2

d⁻(v) = 23, A = N⁻(v), B = N⁺(v), |B| = N − 24. The in-degrees of T[A] are |D({a, v})| ≥ 11 and sum to C(23,2) = 253 = 23·11,
so T[A] is 11-regular and every {a, v} is tight with D({a, v}) = A ∩ N⁻(a). Each a′ ∈ A beats some a ∈ A (it has 11 out-neighbours
in A), so a′ ∈ D({a, v}) and d⁻(a′) ≥ 25 by Lemma T. Arcs A → B: each b ∈ B is beaten by |D({v, b})| = |A ∩ N⁻(b)| ≥ 11
vertices of A, so ≥ 11(N − 24). Each a ∈ A beats v and 11 vertices of A, and d⁺(a) = N − 1 − d⁻(a) ≤ N − 26, so a beats
≤ N − 26 − 12 = N − 38 vertices of B; total ≤ 23(N − 38). Then 11N − 264 ≤ 23N − 874, 12N ≥ 610, N ≥ 50.83, so N ≥ 51.
**Correct.**

### 2.4 Lemma 2.3 (Claim Q)

Z = {d⁻ = 24}, v ∈ Z, A = N⁻(v) (24 vertices), Z_v = A ∩ Z. In-degrees in T[A] are 11 + f_x, f_x ≥ 0, summing to
C(24,2) = 276 = 24·11 + 12, so Σ f_x = 12. L = {f_x = 0}, ℓ = |L|. At most 12 vertices have f ≥ 1, so **ℓ ≥ 12**.
(For a ∈ L, {a, v} is tight, so L is exactly the set of a ∈ A with {a, v} tight: this is the "≥ 12 tight partners" claim used in
[52] Corollary 3. Correct.)

(a) a ∈ L: D({a, v}) = A ∩ N⁻(a), so every in-neighbour of a inside A has d⁻ ≥ 25 (Lemma T) and is not in Z. Every x ∈ Z_v ∖ {a}
is in A and is not an in-neighbour of a, so a → x. Two members of L ∩ Z would each beat the other: |L ∩ Z| ≤ 1. Correct.

(b) Q = Z_v ∖ L, q = |Q|. For z ∈ Q, all ℓ vertices of L beat z (by (a)), and L ∩ Q = ∅, so the in-degree of z in T[A] satisfies
11 + f_z ≥ ℓ + d⁻_{T[Q]}(z). Summing over Q: Σ_Q f ≥ q(ℓ − 11) + C(q,2). The other 24 − ℓ − q vertices of A ∖ L ∖ Q have f ≥ 1. So
12 ≥ q(ℓ − 11) + C(q,2) + (24 − ℓ − q), i.e. 0 ≥ qℓ − 12q − ℓ + 12 + C(q,2) = (q − 1)(ℓ − 12) + C(q,2).
For q ≥ 2 the left side is ≥ 0 + 1 > 0, a contradiction; so q ≤ 1 and |Z_v| ≤ |L ∩ Z| + q ≤ 2. In T[Z] every in-degree is ≤ 2, so
C(|Z|, 2) ≤ 2|Z|, |Z| ≤ 5. **Correct, every N.**

### 2.5 Theorem A

N ≤ 50. In-degrees ≥ 23 (F3), none equal to 23 (Lemma 2.2 would give N ≥ 51), so all ≥ 24: C(N,2) ≥ 24N, N ≥ 49.
Excess Σ(d⁻ − 24) = N(N − 1)/2 − 24N = N(N − 49)/2 = 0 (N = 49), 25 (N = 50). Each vertex outside Z contributes ≥ 1, so
|Z| ≥ N − (excess) = 49, resp. 25. Contradiction with |Z| ≤ 5. **Correct.**

---

## 3. Audit of [52] §2 (Theorem 1 at N = 51)

### 3.1 Set-up, (2.1), (I1)–(I3)

**(2.1)**: for ∅ ≠ U ⊆ R, D(U) = {w ∈ R ∖ U : U ⊆ N⁺(w)} ∪ {y ∈ O : U ∩ Q_y = ∅}. Proof: a, b are beaten by all of R, so beat nothing in
U; w ∈ R needs U ⊆ N⁺(w); y ∈ O beats u ∈ R iff u ∉ Q_y. Correct.

**(I1)** N⁻(r) ∩ P = ∅, |N⁻(r) ∩ R| = 5, so |N⁻(r) ∩ O| = d⁻(r) − 5 = 20 + j_r, and y ∈ O lies in N⁻(r) iff r ∉ Q_y.
Hence #{y : r ∉ Q_y} = 20 + j_r for **every N**, and #{y : r ∈ Q_y} = (N − 13) − 20 − j_r = N − 33 − j_r (18 − j_r at N = 51). Correct.

**(I2)** Σ_y q_y = Σ_r (N − 33 − j_r) = 11N − 363 − J, so Σ_y (q_y − 5) = 11N − 363 − J − 5(N − 13) = **6N − 298 − J**
(= 8 − J at N = 51; 14 − J at N = 52). Correct.

**(I3)** For u ∈ R, Σ_{v≠u} c(u, v) = Σ_{w∈R, w→u} #{v ≠ u : w → v} = 5·4 = 20. And c(u, v) ≤ 4: if u → v, the 5 in-neighbours
of v in R include u, which is not an in-neighbour of u. Correct.

### 3.2 (∗) and the λ table

For r ∈ R, the 45 triples U ∋ r: w ∈ R beating r contribute exactly 6 each (30 in all); y ∈ O with r ∉ Q_y contributes exactly
C(10 − q_y, 2) (the triples r ∪ {2 vertices of R ∖ Q_y ∖ {r}}, a set of 11 − q_y − 1 = 10 − q_y elements); P contributes 0. Hence
Σ_U |D(U)| = 30 + Σ_{y∌r} C(10 − q_y, 2), and with |D(U)| ≥ 5, 225 ≤ 30 + 10(20 + j_r) − Σ_{y∌r} λ(q_y), where
λ(q) = 10 − C(10 − q, 2): λ(5) = 10 − 10 = 0, λ(6) = 10 − 6 = 4, λ(7) = 10 − 3 = 7, λ(8) = 10 − 1 = 9, λ(9) = λ(10) = 10.
So **Σ_{y∌r} λ(q_y) ≤ 5 + 10 j_r** (∗), and the exact slack is Ex(r) := Σ_{U∋r}(|D(U)| − 5) = 5 + 10 j_r − Σ_{y∌r} λ(q_y) ≥ 0.
Correct, N-free. (All y with r ∉ Q_y have q_y ≤ 10.)

### 3.3 Lemma P (N = 51, J ≤ 2)

* q_y = 7: the 4 vertices r ∉ Q_y have 7 ≤ λ(7) ≤ 5 + 10 j_r, so j_r ≥ 1 each, J ≥ 4. q_y = 8: 3 such r with 9 ≤ 5 + 10 j_r, J ≥ 3.
  Both contradict J ≤ 2. (N-free.)
* Triples of R: Σ_{U⊆R} |D(U)| = 11·C(5,3) + Σ_y C(11 − q_y, 3) = 110 + Σ_y C(11 − q_y, 3) ≥ 5·C(11,3) = 825. With m = #{q ≥ 9},
  n_6 = #{q = 6}, and C(6,3) = 20, C(5,3) = 10, C(2,3) = 0, the 38 vertices of O give 110 + 20(38 − m − n_6) + 10 n_6 ≥ 825, i.e.
  870 − 20m − 10 n_6 ≥ 825, **20m + 10 n_6 ≤ 45**. (General N: 20N − 975 ≥ 20m + 10 n_6.)
* (I2): n_6 + Σ_{q≥9}(q_y − 5) = 8 − J ≥ 6. m = 0 forces n_6 ≥ 6, 60 ≤ 45, false. m ≥ 2 forces m = 2 (20·3 > 45), and then the two
  terms ≥ 4 already give 8, so J = 0 and n_6 = 0, q = 9 for both; a vertex r outside one of them has 10 = λ(9) ≤ 5 + 0, false.
  So m = 1, and 10 n_6 ≤ 25 gives n_6 ≤ 2. **Correct.** It is an N = 51 statement.

### 3.4 (R1), (R2), (R3), the rounding lemma

Let s(u, v) = Σ_{w∈R∖{u,v}} (|D({u, v, w})| − 5) ≥ 0.

**(R1) (general q).** By (2.1) the vertices of R dominating {u, v, w} are the w′ with w′ → u, w′ → v, w′ → w. There are c(u, v) such w′,
each beating exactly 3 vertices w ∈ R ∖ {u, v} (w′ beats 5 vertices of R, two of them u and v). A y ∈ O dominates {u, v, w} iff u, v, w ∉ Q_y; for
y missing both u and v the number of admissible w is |R ∖ Q_y| − 2 = 9 − q_y (4, 3, 2, 1, 0 for q = 5, 6, 7, 8, ≥ 9). So

 s(u, v) = 3c(u, v) + 4k_5 + 3k_6 + 2k_7 + k_8 − 45,

k_q = #{y : q_y = q, u, v ∉ Q_y}. (A y with q ≥ 9 missing both has q = 9 and contributes 0.) Correct.

*Exact aggregate check of (R1).* Sum over all 110 ordered pairs (u, v): Σ c = 11·20 = 220. A vertex y with t = |R ∖ Q_y| = 11 − q_y is missed by t(t − 1)
ordered pairs, each with weight 9 − q_y = t − 2. So Σ s = 3·220 − 45·110 + Σ_y t(t − 1)(t − 2) = 660 − 4950 + 6 Σ_y C(t_y, 3) = −4290 + 6Σ_y C(t_y, 3).
On the other hand every triple U ⊆ R has 6 ordered pairs, so Σ s = 6 S_tot with S_tot = Σ_U (|D(U)| − 5) = 110 + Σ_y C(t_y, 3) − 825 = −715 + Σ_y C(t_y, 3),
and 6·(−715) = −4290. The two agree identically for every profile (q_y). This confirms the coefficients and the constant −45.

**(R2) (N = 51 form).** Under Lemma P, with α_u, β_u, γ_u as in [52], Σ_v k = 5α_u, Σ_v m = 4β_u (a 5-vertex missing u misses 5 more vertices of R; a
6-vertex misses 4 more), α_u + β_u + γ_u = 20 + j_u. So Σ_v s(u, v) = 3·20 + 4·5α + 3·4β − 45·10 = 20α + 12β − 390 =
10 + 20 j_u − 8β_u − 20γ_u. Correct.
General q (needed in §4): Σ_v k_7 = 3β_7, Σ_v k_8 = 2β_8, so
 Σ_v s(u, v) = 10 + 20 j_u − 8β_6 − 14β_7 − 18β_8 − 20γ_u,
where γ_u counts y with q_y ≥ 9, u ∉ Q_y: 60 + 20α + 12β_6 + 6β_7 + 2β_8 − 450 with α = 20 + j − β_6 − β_7 − β_8 − γ; the coefficients are 12 − 20, 6 − 20,
2 − 20, −20. This matches the formula printed in [52]. Correct.
*Aggregate check of (R2), N = 51 under Lemma P:* Σ_u of the right side = 110 + 20J − 8·(5 n_6) − 20 t*, where t* = 11 − q_{y*} (Σ_u β_u = 5n_6, Σ_u γ_u = t*). Counting
incidences (u, y), u ∉ Q_y: 6n_5 + 5n_6 + t* = Σ_u (20 + j_u) = 220 + J, so 120 n_5 = 20(220 + J − 5n_6 − t*). Then 6S_tot = −4290 + 120 n_5 + 60 n_6 = 110 + 20J − 40 n_6 − 20t*. Equal. ✓.

**(R3) and the arithmetic lemma.** Mod 4: 3c ≡ −c, 4k ≡ 0, 3m ≡ −m, −45 ≡ −1 ≡ 3, so s ≡ 3 − c − m. *Lemma Ρ.* Let s ≥ 0 and x ≥ 0 be integers with
s ≡ 3 − x (mod 4). Then s ≥ 3 − x if x ≤ 3, and **s ≥ 7 − x if x ≥ 4, for every x ≥ 4**. Proof: for x ≤ 3, 3 − x ∈ {0, 1, 2, 3} is the least non-negative
representative. For x ≥ 4, s ≡ 7 − x; if 7 − x ≤ 0 the claim is trivial; if x ∈ {4, 5, 6}, 7 − x ∈ {3, 2, 1} is the least non-negative representative. ∎
(For x ≥ 8 the inequality is weak but still true: e.g. x = 8 gives s ≥ 3 > −1. This is **G3**: [52] argues with "c + m ≤ 6", which holds only under Lemma P;
the stated inequality needs no such bound.) Correct.

**Rounding lemma.** Σ_v s(u, v) ≥ Σ_v (3 − c − m) + 4N_4(u) = 30 − 20 − 4β_u + 4N_4(u), and (R2) gives Σ_v s = 10 + 20 j_u − 8β_u − 20γ_u. Hence
 20 j_u − 4β_u − 20γ_u ≥ 4N_4(u), i.e. **β_u + 5γ_u + N_4(u) ≤ 5 j_u.** Correct (under Lemma P).

### 3.5 Steps 1–5 (N = 51)

V_0 = {j = 0}, |V_0| ≥ 11 − J ≥ 9.
* **Step 1.** u ∈ V_0: β_u = γ_u = N_4(u) = 0; m(u, v) = 0 for all v, so c(u, v) ≤ 3. ✓.
* **Step 2.** A 6-vertex y has |R ∖ Q_y| = 5 and R ∖ Q_y ⊆ R ∖ V_0, which has ≤ J ≤ 2 elements. Contradiction, n_6 = 0. Then (I2): q_{y*} − 5 = 8 − J, so q_{y*} = 13 − J ≤ 11,
  so J = 2 and Q_{y*} = R. ✓.
* **Step 3.** u ∈ V_0: Σ_v s(u, v) = 10 (β = γ = j = 0), and s(u, v) ≥ 3 − c(u, v) with Σ_v (3 − c) = 30 − 20 = 10, so s = 3 − c for every v. Then (R1) with m = 0:
  3c + 4k − 45 = 3 − c, k = 12 − c; |D({u, v})| = c + k = 12 (y* misses nothing). ✓.
* **Step 4.** Σ_{v≠s} |D({s, v})| = 20 + 5α_s = 20 + 5(20 + j_s) = 120 + 5 j_s, since every y missing s is a 5-vertex. ✓.
* **Step 5.** (i) j_s = 2, the other 10 vertices in V_0: each |D({s, v})| = 12 by Step 3, total 120 ≠ 130. (ii) j_{s_1} = j_{s_2} = 1: Step 4 at s_1 gives
  125 − 9·12 = 17 = |D({s_1, s_2})|, k = 17 − c, s(s_1, s_2) = 3c + 4(17 − c) − 45 = 23 − c ≥ 19. But the triples through s_1 have total excess ½Σ_v s(s_1, v) =
  ½(10 + 20) = 15 (each triple {s_1, v, w} is counted in s(s_1, v) and in s(s_1, w)), and the triples through both s_1, s_2 are among them: s(s_1, s_2) ≤ 15. ✓.

**Theorem 1 at N = 51: correct.**

---

## 4. Proposition SF (fill G2): the structural fact, any tight pair, any N

**Proposition SF.** Let T be an F1-tournament on N vertices, P tight, and r ∈ R = D(P) with d⁻(r) = 25 (j_r = 0). Then
1. every y ∈ O with y → r (i.e. r ∉ Q_y) has q_y = 5; equivalently r ∈ Q_y whenever q_y ≥ 6;
2. c(r, v) ≤ 3 for every v ∈ R ∖ {r};
3. s(r, v) = 3 − c(r, v) and k(r, v) = 12 − c(r, v), where k(r, v) = #{y ∈ O : r, v ∉ Q_y};
4. |D({r, v})| = 12 for every v ∈ R ∖ {r}.

*Proof.* (a) *No 7-, 8-, 9-, 10-vertex misses r; at most one 6-vertex does.* By (∗) with j_r = 0, Σ_{y: r∉Q_y} λ(q_y) ≤ 5. Here q_y ≤ 10 for these y; λ(q) ≥ 7 for
7 ≤ q ≤ 10, and λ(6) = 4 with 2·4 = 8 > 5. So the 20 vertices of O that beat r are (20 − β) 5-vertices and β ∈ {0, 1} 6-vertices.

(b) *Pair formula at r.* A y contributes to s(r, v) only if it misses r. By (R1) (general-q form of §3.4, valid for every N), with k = k_5(r, v), m = m(r, v) ∈ {0, 1}:
 s(r, v) = 3c(r, v) + 4k + 3m − 45.
(c) *Sum.* Σ_v c(r, v) = 20 (I3). Σ_v k = 5(20 − β) (each 5-vertex missing r misses 5 further vertices of R) and Σ_v m = 4β. Hence
 Σ_v s(r, v) = 60 + 20(20 − β) + 12β − 450 = 10 − 8β.
(d) *Rounding.* s(r, v) ≡ 3 − c − m (mod 4), and c + m ≤ 5. By Lemma Ρ, s ≥ (3 − c − m) + 4·[c + m ≥ 4]. Sum over the 10 vertices v:
 Σ_v s ≥ 30 − 20 − 4β + 4N_4, N_4 := #{v : c(r, v) + m(r, v) ≥ 4}.
(e) Compare (c) and (d): 10 − 8β ≥ 10 − 4β + 4N_4, so 4β + 4N_4 ≤ 0, **β = N_4 = 0**. This gives 1, and c + m = c ≤ 3, giving 2.
(f) Now Σ_v s = 10 = Σ_v (3 − c), and every s(r, v) ≥ 3 − c, so s(r, v) = 3 − c(r, v). From (b): 3c + 4k − 45 = 3 − c, k = 12 − c: 3. By (2.1) with U = {r, v},
|D({r, v})| = c(r, v) + k(r, v) (the y ∈ O that dominate {r, v} miss r, so are 5-vertices): 4. ∎

**Remarks.**
* The 7- and 8-vertices were "included" as the assignment asks: they enter only through (∗) (λ(7) = 7 > 5, λ(8) = 9 > 5), and they cannot enter any pair term (r, v) because
  r misses none of them. The version of (R2) printed in [52], Σ_v s(r, v) = 10 + 20 j_r − 8β_6 − 14β_7 − 18β_8 − 20γ, agrees with §3.4, so the author's shortcut
  "left side ≥ 0 ⇒ β_7 = β_8 = γ = 0, β_6 ≤ 1" is also valid (10 − 14 < 0, 10 − 18 < 0, 10 − 20 < 0).
* The phrase "the rounding lemma as written gives β_6 = 0 and N_4(r) = 0" is the gap G2: the lemma as written assumes Lemma P. The argument above is what is needed.
* [TP] Lemma A is the same statement (restricted to the form used in [TP]) with the same proof. It is correct.

---

## 5. Theorem 1′ (fill G1): J ≥ 3 for every F1-tournament, every N

**Theorem 1′.** If P is a tight pair in an F1-tournament on N vertices, then J(P) ≥ 3.

*Proof.* Assume J ≤ 2. Put V_0 = {j = 0}, V_+ = R ∖ V_0. Then |V_+| ≤ J ≤ 2 and |V_0| ≥ 9. Lemma T gives j ≥ 0.

**A. No 7- or 8-vertex.** If q_y ∈ {7, 8}, the 4 (resp. 3) vertices r ∉ Q_y satisfy λ(q_y) ≤ 5 + 10 j_r, so j_r ≥ 1, J ≥ 3 (resp. 4). ((∗) is N-free.)

**B. No 6-vertex.** If q_y = 6, then |R ∖ Q_y| = 5, and by SF(1) every u ∈ V_0 lies in Q_y; so R ∖ Q_y ⊆ V_+, 5 ≤ 2, false.

So each y ∈ O is a 5-vertex or a *big* vertex (q_y ≥ 9, missing t_y = 11 − q_y ≤ 2 vertices of R, all in V_+ by SF(1)). Let m = #big, γ_u = #{big y : u ∉ Q_y},
Γ = Σ_y t_y = Σ_u γ_u.

**C. γ_u ≤ j_u for every u ∈ R.** By A, B, (R1) and (R2) reduce to s(u, v) = 3c + 4k_5 − 45 (big vertices contribute weight 9 − q ≤ 0, and exactly 0 since they can miss
both u and v only with q = 9) and Σ_v s(u, v) = 10 + 20 j_u − 20γ_u. By Lemma Ρ, s ≥ 3 − c + 4·[c = 4]. Summing over v: 10 + 20 j_u − 20γ_u ≥ 10 + 4·#{v : c(u, v) = 4},
so **γ_u ≤ j_u** (this is the rounding lemma in this setting). Hence Γ ≤ J.

**D. Counting.** (I2): Σ_y (q_y − 5) = 6N − 298 − J, and only big vertices contribute, each 6 − t_y. So 6m − Γ = 6N − 298 − J, i.e.

 6(m − N + 50) = 2 − J + Γ.

Since Γ ≤ J ≤ 2, we have 2 − J + Γ ≤ 2, and 2 − J + Γ ≥ 2 − J ≥ 0. A multiple of 6 in [0, 2] is 0. So **J = 2, Γ = 0, m = N − 50**, and every big vertex has Q_y = R.

**E. Contradiction (Steps 3–5 of [52], now N-free).** For u ∈ V_0, SF(4) gives |D({u, v})| = 12 for all v. For any s ∈ R, all y missing s are 5-vertices (α_s = 20 + j_s),
big vertices miss nothing, so Σ_{v≠s} |D({s, v})| = Σ c + Σ k = 20 + 5(20 + j_s) = 120 + 5 j_s.
* One vertex s with j_s = 2: the other ten pairs {s, v} have 12 dominators, total 120 ≠ 130.
* Two vertices s_1, s_2 with j = 1: |D({s_1, s_2})| = 125 − 9·12 = 17, k = 17 − c, s(s_1, s_2) = 23 − c ≥ 19, but s(s_1, s_2) ≤ ½(10 + 20) = 15. ∎

**Remarks.**
* At N = 51 this reproduces Step 2 (m = 1, q_{y*} = 11, J = 2) and gives a proof of Theorem 1 that does not use Lemma P. At N = 52 it gives m = 2.
* Aggregate sanity check of the extremal scenario (J = 2, any N): 37 five-vertices (|O| − m = N − 13 − (N − 50) = 37, independent of N); incidences 37·6 = 222 = Σ_r (20 + j_r) = 220 + 2.
  Total excess of triples S_tot = −715 + 20·37 = 25, Σ_{u,v} s = 150 = Σ_u (10 + 20 j_u) = 110 + 40. ✓.
* The statement of the every-N paragraph of [52] ("in every S_4 tournament, every tight pair has J ≥ 3") is therefore **true**.

---

## 6. Audit of [52] §3

### 6.1 Corollary 2 (N = 51): min in-degree ≥ 24

d⁻(v) = 23: |A| = 23, |B| = 51 − 24 = 27. As in §2.3, T[A] is 11-regular, every {a, v} is tight, e ≥ 0 on A. Arcs A → B: ≥ 11·27 = 297; exactly 23·13 − Σ_A e (each a ∈ A has
d⁺(a) = 50 − d⁻(a) = 25 − e(a), minus v and 11 inside A: 13 − e(a)); so 297 ≤ 299 − Σ_A e, **Σ_A e ≤ 2**. For any a ∈ A, D({a, v}) ⊆ A, all e ≥ 0, so
J({a, v}) ≤ Σ_A e ≤ 2, contradicting Theorem 1 (N = 51). **Correct.** (At N = 52 this count reads Σ_A e ≤ 14 and Theorem 1 does not finish it: that is why [A52] Lemma 1 needs SF; §8.)

### 6.2 Corollary 3 (N = 51): case (I) is impossible

v ∈ Z, A = N⁻(v), |A| = 24. For z ∈ V ∖ {v} (50 vertices): D_z = D({v, z}) ⊆ N⁻(v) = A, h_z = |D_z| − 11 ≥ 0.
1. **Gram.** G_zz = 11 + h_z. For z ≠ z′: D_z ∩ D_{z′} = D({v, z, z′}) (w beats v, z, z′ implies w ∉ {v, z, z′}), so G_zz′ ≥ 5. G = 5·𝟙𝟙ᵀ + M with
   M_zz = 6 + h_z, M_zz′ = |D({v, z, z′})| − 5 ≥ 0. G = XXᵀ with X a 50 × 24 matrix, so rank G ≤ 24 and G has ≥ 26 zero eigenvalues (indices 25, …, 50 in decreasing order). Since M = G − 5𝟙𝟙ᵀ ≼ G in the
   Loewner order, Courant–Fischer gives λ_i(M) ≤ λ_i(G) (this is the Weyl inequality in the correct direction). So **≥ 26 eigenvalues of M are ≤ 0**. ✓.
2. **Few non-tight z.** x ∈ A lies in D_z iff x beats z and v (v is beaten by x anyway), so for 49 − d⁻(x) values of z (out-degree 50 − d⁻(x) minus the arc to v). Hence
   Σ_z |D_z| = Σ_A (49 − d⁻) = 1176 − Σ_A d⁻ and Σ_z h_z = 1176 − 550 − Σ_A d⁻ = 626 − Σ_A d⁻. For x ∈ A: d⁻ ≥ 24 (Cor. 2); d⁻(x) = 24 iff x ∈ Z; at most 2 vertices of A lie in Z (Claim Q).
   So Σ_A d⁻ = 25·24 − |A ∩ Z| + W ≥ 598 + W, W := Σ_{x∈A∖Z} e(x). Hence n_t := #{h_z ≥ 1} ≤ Σ h_z ≤ **28 − W**. ✓.
3. **Tight z.** h_z = 0: {v, z} tight, R = D_z. Off-diagonal row sum of M at z: Σ_{z′} (|D({v, z, z′})| − 5). For z′ ∈ R: D({v, z, z′}) = R ∩ N⁻(z′) has 5 elements (5-regular), term 0. For z′ ∈ O
   (38 vertices): q_{z′} − 5, total 8 − J({v, z}) ≤ 5 by Theorem 1. M_zz = 6. All off-diagonal entries are ≥ 0, so on the principal submatrix indexed by tight z every row sum of off-diagonals is ≤ 5 < 6; by
   Gershgorin every eigenvalue is ≥ 1. Positive definite. ✓.
4. **Counting.** Cauchy interlacing (λ_i(M) ≥ λ_i(M_S) for a principal submatrix M_S of size |S| = 50 − n_t) gives ≥ 50 − n_t positive eigenvalues of M. With step 1: (50 − n_t) + 26 ≤ 50, n_t ≥ 26. Direction correct.
   *Interlacing-free proof:* K = ker G has dim ≥ 26, and for x ∈ K, xᵀMx = −5(𝟙ᵀx)² ≤ 0, whereas xᵀMx > 0 for 0 ≠ x supported on the tight indices S. So K ∩ E_S = {0}, dim K + |S| ≤ 50. ✓.
   With step 2: 26 ≤ n_t ≤ 28 − W, **W ≤ 2**.
5. Claim Q: some a ∈ A has {a, v} tight (≥ 12 of them). D({a, v}) ⊆ A, e ≥ 0 on it (Lemma T), none of its members lies in Z, so J({a, v}) ≤ W ≤ 2, contradicting Theorem 1. ∎

**Correct.** Note: every use of Theorem 1 is at N = 51 (|O| = 38, 8 − J ≤ 5 < 6).

### 6.3 Corollary 4

Z = ∅ and all d⁻ ≥ 24 with mean 25 give all d⁻ = 25 (case (R)); Corollary 3 excludes (I). A tight pair would have J = Σ (25 − 25) = 0 < 3. So every pair has ≥ 12 dominators, and
Σ_P |D(P)| = Σ_w C(d⁺(w), 2) = 51·C(25, 2) = 51·300 = 15300 = 12·1275 = 12·C(51, 2). Hence every pair has exactly 12. Common out-neighbours: for u → w, the 25 − 1 = 24
in-neighbours of w other than u split into 12 that beat u (the dominators of {u, w}) and 12 that u beats; so u beats 12 vertices (other than w) that beat w, hence 24 − 12 = 12 that w beats: exactly 12 common
out-neighbours (symmetric if w → u). **Correct.**

---

## 7. Audit of [52] §4 (Theorem 5: no DRT(51) has S_4)

**(M0).** Transitive triples = Σ_v C(25, 2) = 51·300 = 15300; C(51, 3) = 51·50·49/6 = 20825; cyclic = 20825 − 15300 = 5525. ✓.

**(M1)** |D(Y)| + |D⁺(Y)| = 12 − σ(Y). The 48 vertices outside Y; inclusion–exclusion over the in-neighbourhoods: |D⁺(Y)| = 48 − Σ_i |N⁻(y_i) ∖ Y| + Σ_{i<j} |D({y_i, y_j}) ∖ Y| − |D(Y)|. Σ_i |N⁻(y_i) ∖ Y| = 75 − 3 = 72
(the three arcs inside Y are in-arcs). D({y_i, y_j}) ∖ Y has 12 − [y_k beats y_i and y_j] elements, and exactly σ(Y) of the three pairs have this (a transitive triple has one source, a cyclic triple none). Middle sum = 36 − σ.
So |D⁺| = 48 − 72 + 36 − σ − |D| = 12 − σ − |D|. ✓. *Independent test in QR_11 (t = 2, the analogue is k + k⁺ = t − σ):* S = {1, 3, 4, 5, 9}, w → x iff x − w ∈ S. Cyclic triple {0, 1, 2}: D = {8}, D⁺ = {5}, sum 2 = 2 − 0 ✓.
Transitive triple {0, 1, 3}: D = ∅, D⁺ = {4}, sum 1 = 2 − 1 ✓.

**(M2).** Σ_{Y transitive} k(Y) = #{(Y, w) : Y ⊆ N⁺(w), Y transitive}. For each w, T[N⁺(w)] has all out-degrees 12 (common out-neighbours of w and x) on 25 vertices, hence all in-degrees 12. Transitive triples inside:
Σ_x C(12, 2) = 25·66 = 1650; cyclic 2300 − 1650 = 650. Times 51: 84150 and 33150. Means 84150/15300 = 5.5 (15300·5.5 = 84150) and 33150/5525 = 6. ✓.

**(M3).** Σ_Y C(k, 2) = Σ_{pairs {w, w′}} C(|N⁺(w) ∩ N⁺(w′)|, 3) = 1275·C(12, 3) = 1275·220 = 280500. ✓.

**(M4).** Both sides count ordered pairs (Y, W) of triples with every vertex of W beating every vertex of Y: for fixed Y, W ⊆ D(Y); for fixed W, Y ⊆ D⁺(W) of size 12 − σ(W) − k(W). ✓.

**Algebra.** f(x) = x³ − x. 6C(k, 3) = (k − 2)(k − 1)k = f(k − 1), k − 1 = u + a with u = k − L/2, a = L/2 − 1. 6C(L − k, 3) = f(L − k − 1) = f(a − u) = −f(u − a). So
C(k, 3) − C(L − k, 3) = [f(u + a) + f(u − a)]/6 = [2u³ + (6a² − 2)u]/6 = (u³ + (3a² − 1)u)/3. ✓. With L = 11 (transitive: a = 9/2, 3a² − 1 = 239/4) and L = 12 (cyclic: a = 5, 74), and Σu = 0 on each class (M2),
(M4) gives Σ_all u³ = 0 (4.1). ✓.

**Positivity.** Transitive u = k − 11/2 ≥ −1/2: u³ − u/4 = (u − 1/2)u(u + 1/2) ≥ 0 with equality iff u = ±1/2 (k ∈ {5, 6}); at u = 3/2 it is 1·(3/2)·2 = 3. Cyclic u = k − 6 ≥ −1: u³ − u = (u − 1)u(u + 1) ≥ 0, equality iff
u ∈ {−1, 0, 1} (k ∈ {5, 6, 7}); at u = 2 it is 6. Since Σ(u³ − u/4) + Σ(u³ − u) = Σu³ − ¼Σ_trans u − Σ_cyc u = 0 and all terms are ≥ 0, all vanish. ✓.

**Counting.** Transitive: n_5 + n_6 = 15300, 5n_5 + 6n_6 = 84150 gives n_6 = 84150 − 76500 = 7650 = n_5. Cyclic with k ∈ {5, 6, 7}: n_5 + n_6 + n_7 = 5525, Σk = 33150 = 6·5525 gives n_7 = n_5 = p, n_6 = 5525 − 2p.
Σ C(k, 2) = 7650(10 + 15) + 10p + 15(5525 − 2p) + 21p = 191250 + 82875 + p = 274125 + p; equal to 280500 gives p = 6375, but 2p = 12750 > 5525. Contradiction. **Theorem 5 correct.** ✓.

*Remarks checked.* Mean k over all triples = 117300/20825 ≈ 5.6327, E[C(k,2)] = 280500/20825 ≈ 13.4694, so Var k = 2·13.4694 + 5.6327 − 5.6327² ≈ 32.5714 − 31.7268 ≈ 0.845. The maximum variance of the confined distribution: within-class 0.25·(15300/20825) + 1·(5525/20825) +
between-class ≈ 0.1837 + 0.2653 + 0.0487 ≈ 0.498. ✓. QR_19 (t = 4): C(19, 3) = 969, transitive 19·36 = 684 (342 + 342), cyclic 285; Σ C(k, 2) = 171·4 = 684 = 342 + (285 − 2p) + 3p gives p = 57. ✓. Class-0 circulant S = {1, 2, 3, 4, 6} in Z_11:
c(d) = |S ∩ (S − d)| for d = 1, …, 10 is 3, 3, 2, 1, 1, 1, 1, 2, 3, 3 (sum 20) ✓, so c ∈ {1, 2, 3}.

---

## 8. Interface with [A52] and [TP] (what the N = 52 programme takes from the audited facts)

Verified at N = 52 (from the general forms above):
* (E) Σ_y (q_y − 5) = 14 − J: from (I2), 6·52 − 298 = 14. ✓.
* (Ex) Ex(r) = 5 + 10 j_r − Σ_{y∌r} λ(q_y): §3.2 (an equality). ✓.
* (PS) Σ_{v≠u} |D({u, v})| = 120 + 5 j_u − τ_u: Σ_v c = 20, and each of the 20 + j_u vertices y missing u misses 10 − q_y = 5 − (q_y − 5) further vertices. ✓.
* (S) s(u, v) = 4|D({u, v})| − c − 45 − E_both: s = 3c + Σ_{y miss u,v} (9 − q_y) − 45, with 9 − q_y = 4 − (q_y − 5) and |D({u, v})| = c + #{y miss u, v}. ✓.
* (B) s(u, v) ≤ Ex(u): the nine triples through {u, v} are among the triples through u. ✓.
* [TP] Lemma A = Proposition SF(1)(2)(4) (proof there: ✓).
* [A52] Lemma 1 (no in-degree 23 at N = 52): T[A] is 11-regular and DRT(23) (5 common in-neighbours, hence 5 common out-neighbours: u → u′, 10 in-neighbours of u′ other than u, 5 beat u, so 5 are beaten by u,
  and of the 10 out-neighbours of u other than u′, 5 beat u′, so 5 are beaten by both). Arcs: 308 ≤ 322 − E, E ≤ 14, |A_0| ≥ 9. Block count: two b with A_b = R_a would give 12 > 11 = 14 − 3 ≥ 14 − J_a, so one b per block (uses Theorem 1′ at N = 52). Key step:
  for r ∈ A_0, b → r, and the 11 vertices a ∈ N⁺_A(r), SF(1) for the tight pair {a, v} gives |R_a ∩ A_b| = 5; Σ_a |R_a ∩ A_b| = Σ_{x∈A_b} |N⁺_A(r) ∩ N⁺_A(x)| = 5|A_b|, so |A_b| = 11; with n_a = |A_b ∩ R_a|, Σ n_a = 121, Σ n_a(n_a − 1) = 11·10·5 = 550,
  Σ (n_a − 5)² = 550 + 121 − 1210 + 575 = 36 = (Σ(n_a − 5))² (Σ(n_a − 5) = 6), so one term is 6: A_b = R_{a_b}; a_b ∈ {r} ∪ N⁻_A(r) (12 elements) for each of the 14 in-neighbours of r in B, distinct. 14 ≤ 12 false. ✓. **[A52] Lemma 1 is correct.**

Not audited here: the case analyses of [TP] §3–§5 and §9 (they use only the identities above, verified).

---

## 9. What would a hostile referee still ask for

* The only unverifiable items are the remarks about the 1101 computer certificates and `verify_proof.py`. Neither is used by the proof.
* The one structural worry: F1 is strictly weaker than S_4, so [52] actually proves that no tournament on ≤ 51 vertices has all triples with ≥ 5 dominators. I checked that nothing is used beyond F1; consistent with the QR_11 / QR_19 / QR_7 sanity
  tests of the identities (M1)–(M4), no contradiction appears.

---

## 10. Dead ends and non-transfers to N = 52 (reasons)

* **Cor 3 (spectral) at N = 52.** With v ∈ Z, G is 51 × 51 of rank ≤ 24: ≥ 27 zero eigenvalues. Σ_z h_z = 639 − Σ_A d⁻ ≤ 41 − W (not 28 − W). For tight z the off-diagonal row sum of M is 14 − J (|O| = 39),
  and diagonal dominance (6 > 14 − J) needs **J ≥ 9**, while [TP] gives only J ≥ 5. The final step would need W ≤ 4 against W ≤ 14 obtained. Both ends fail.
* **Cor 2 at N = 52.** Σ_A e ≤ 14 (not 2); Theorem 1 alone does not finish. [A52] Lemma 1 uses SF and design counting instead.
* **Cor 4 / Theorem 5 at N = 52.** No regular tournament on 52 vertices (Σ d⁻ = 1326); L_Y is not constant (BRIEF §4).
* **Lemma P at N ≥ 52.** Not applicable (under J ≤ 2 there are N − 50 big vertices, §5).

## 11. Hand checks of the numbers

C(10,2) = 45; 5·45 = 225; 30 + 10·19.5 = 225. C(23,2) = 253 = 23·11; 11·27 = 297; 23·13 = 299; 12N ≥ 610. C(24,2) = 276 = 264 + 12.
C(11,3) = 165; 5·165 = 825; 11·C(5,3) = 110; 110 + 20·38 = 870; 870 − 825 = 45. 6·(−715) = −4290; 660 − 4950 = −4290. 60 + 20·20 + ... (R2): 60 + 400 − 450 = 10.
Step 5: 20 + 5·21 = 125; 125 − 108 = 17; 3c + 68 − 4c − 45 = 23 − c. Cor 3: 24·49 = 1176; 1176 − 550 = 626; 25·24 − 2 = 598; 626 − 598 = 28; 50 − 24 = 26.
Thm 5: 51·300 = 15300; 20825 − 15300 = 5525; 25·66 = 1650; 2300 − 1650 = 650; 51·1650 = 84150; 51·650 = 33150; 1275·220 = 280500; 7650·25 = 191250; 15·5525 = 82875; 191250 + 82875 = 274125; 280500 − 274125 = 6375; 2·6375 = 12750 > 5525.
J = 2 scenario: 37·6 = 222 = 220 + 2; −715 + 740 = 25; 110 + 40 = 150 = 6·25. A52 Lemma 1: 121 − 115 = 6; 121 + 550 − 1210 + 575 = 36.
