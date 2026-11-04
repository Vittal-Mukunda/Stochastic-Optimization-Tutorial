# N = 51, case (I): the local claim J ≥ 3

*Written 18 October 2026. Background: `ERDOS902_PROOF.md` §8.1, and the f4 agent's `round3_agents/f4/FINAL.md` §3.3
and `tightJ51.py` in `schutte_902_results.zip`. Everything here was re-implemented from scratch, and no earlier script
is imported. Scripts, data, certificates and logs are in `proof/n51_local/`.*

> **Update, 20 October 2026.** The local claim is now proved by hand for every class and both modes, in its
> type-free form: see Theorem 1 of `F4_GE_52_HAND_PROOF.md` (a rounding argument modulo 4). The open case below
> (class 0, out-mode) is covered by it. The certificates described here remain valid but are no longer needed.

## 0. Result

**Local claim (J ≥ 3).** Let T be an S_4 tournament on 51 vertices with minimum in-degree ≥ 24. Let
Z = {v : d⁻(v) = 24} with 1 ≤ |Z| ≤ 5. Let P = {a, b}, with a → b, be a tight pair (|D(P)| = 11) such that
d⁻(b) = 24 (**in-mode**) or d⁻(a) = 24 (**out-mode**). Then J := Σ_{r ∈ D(P)} (d⁻(r) − 25) ≥ 3.

**Status: proved in 1101 of the 1102 cases (551 classes of T[D(P)], two modes each). One case is still open:
class 0 in out-mode.**
Each proved case has an exact integer certificate: a branch-and-bound tree whose leaves are Farkas certificates. A
separate checker verifies every certificate. It rebuilds every constraint from scratch and imports nothing from the
producer.

* **550 classes** (all except class 0) have a **type-free** certificate. It never uses the in-degrees of a and b, so
  it proves the stronger statement: *in every S_4 tournament on 51 vertices, every tight pair P with T[D(P)] in one
  of these classes has J ≥ 3.*
* **Class 0** (the circulant class, automorphism group of order 11): in-mode is refuted by a single Farkas
  certificate at the root. Out-mode is **not finished**. It is being refuted by a skeleton split over the 75 orbit
  representatives, and 69 of the 75 subtrees are done (§4).
* **Side result.** The type-free certificates refute J = 0 as well. Together with one extra certificate for class 0
  in the regular case ("reg" mode: d⁻(a) = d⁻(b) = 25, J = 0), they **independently re-verify case (R)** of §8.1: a
  regular S_4 tournament on 51 vertices has no tight pair. That result was previously supported only by the f4
  agent's certificates.

**Case (I) is therefore not yet excluded.** The spectral lemma (§1) needs the local claim in both modes. As things
stand, case (I) can only occur through a tight pair P in out-mode with T[D(P)] in class 0. Once that case is certified,
the spectral lemma makes case (I) impossible. Then, granting the computer-assisted minimum-in-degree step of §8.1, every
S_4 tournament on 51 vertices is regular and has no tight pair, so it is a DRT(51).

## 1. Why the claim matters: case (I) reduces to it

At N = 51 the in-degrees sum to 51·25. Assume the minimum in-degree is ≥ 24 (§8.1, computer-assisted). By Claim Q
(Lemma 2.3), either (R) T is regular, or (I) 1 ≤ |Z| ≤ 5 and Σ_{x ∉ Z} (d⁻(x) − 25) = |Z|.

**Spectral lemma** (f4 agent; re-derived here). Assume (I) and the local claim. Fix v ∈ Z, so |N⁻(v)| = 24. For each
of the other 50 vertices z, put D_z = D({v, z}) ⊆ N⁻(v) and h_z = |D_z| − 11 ≥ 0.

* D_z ∩ D_z′ = D({v, z, z′}). So the Gram matrix of the 50 indicator vectors in ℝ^24 is G = 5·𝟙𝟙ᵀ + M, with
  M = diag(6 + h_z) + E and E_zz′ = |D({v, z, z′})| − 5 ≥ 0 by (F1). G is positive semidefinite of rank ≤ 24, so
  λ_i(G) = 0 for i ≥ 25. Subtracting the rank-one positive semidefinite matrix 5·𝟙𝟙ᵀ gives λ_i(M) ≤ λ_i(G). So
  **M has at least 26 eigenvalues ≤ 0**.
* Σ_z |D_z| = Σ_{x ∈ N⁻(v)} (d⁺(x) − 1) = 24·49 − Σ_{x ∈ N⁻(v)} d⁻(x). So Σ_z h_z = 626 − Σ_{x ∈ N⁻(v)} d⁻(x).
  Write d⁻(x) = 25 + (d⁻(x) − 25) and use |N⁻(v) ∩ Z| ≤ 2 (Claim Q). This gives Σ_z h_z ≤ 28 − W⁻(v), where
  W⁻(v) = Σ_{x ∈ N⁻(v)} (d⁻(x) − 25)⁺. So the number n_t of non-tight z is at most 28 − W⁻(v).
* Let z be tight. Then {v, z} is a tight pair with R = D_z, and by the identities of §2.2 the off-diagonal z-row of E
  sums to Σ_{z′ ∈ R} (5 − 5) + Σ_{z′ ∈ O} (q_z′ − 5) = 8 − J_z. By the local claim (in-mode if z → v, out-mode if
  v → z) this is ≤ 5 < 6 = M_zz. So the principal submatrix of M on the tight z is strictly diagonally dominant with
  positive diagonal, hence positive definite.
* By Cauchy interlacing, a positive definite principal submatrix of size 50 − n_t leaves room for at most n_t
  eigenvalues ≤ 0. So 26 ≤ n_t ≤ 28 − W⁻(v), that is, W⁻(v) ≤ 2.
* The proof of Claim Q gives a ∈ N⁻(v) with {a, v} tight (ℓ ≥ 12). Its dominators lie in N⁻(v) and have in-degree
  ≥ 25, so J_a ≤ W⁻(v) ≤ 2. This contradicts the local claim in in-mode. ∎

So **the local claim excludes case (I)**.

## 2. The local model

### 2.1 Setting

T is an S_4 tournament on N = 51 vertices. P = {a, b} is a tight pair with a → b, and R = D(P), so |R| = 11.
O is the set of the other 38 vertices. The facts used all come from `ERDOS902_PROOF.md`:

* (F1): every triple has ≥ 5 dominators. (F2): every pair has ≥ 11. S_4: every 4-set has ≥ 1.
* T[R] is 5-regular (§1, tight pair). It is also S_2: for r, r′ ∈ R, D(P ∪ {r, r′}) = R ∩ N⁻(r) ∩ N⁻(r′) ≠ ∅ by S_4.
  So T[R] is isomorphic to one of the 551 classes of `reg11_S2.txt`. All rows below are defined from T[R] alone, so
  they are invariant under relabelling R, and one representative per class suffices.
* Lemma 2.1 (Lemma T, any N): every r ∈ R has d⁻(r) ≥ 25. Write **d⁻(r) = 25 + j_r, with j_r ≥ 0, and J = Σ_r j_r.**

For y ∈ O put **Q_y = R ∩ N⁻(y)**, the vertices of R that beat y, and q_y = |Q_y|. By (1), Q_y = D(P ∪ {y}).
No y ∈ O beats both a and b, since it would then lie in D(P) = R. So each y has one of three **types**:
* type 0: y → a and b → y;
* type 1: a → y and y → b;
* type 2: a → y and b → y.

Let n_t be the number of type-t vertices.

**Variables.** x[S, t] = #{y ∈ O : Q_y = S, type t}, an integer ≥ 0, and the integers j_r. The **type-free** model
uses x[S] = Σ_t x[S, t] and drops every row that mentions a or b.

### 2.2 Identities

These hold exactly for every tournament with this planted structure. For U ⊆ R, let
cR(U) = #{w ∈ R \ U : w beats every vertex of U}. Then:

* |D(U)| = cR(U) + Σ_{S ∩ U = ∅} x[S, ·]. (a and b beat no vertex of R, and y ∈ O beats u ∈ R iff u ∉ Q_y.)
* For U ≠ ∅: |D(U ∪ {a})| = cR(U) + Σ_{S ∩ U = ∅} x[S, 0] and |D(U ∪ {b})| = cR(U) + Σ_{S ∩ U = ∅} x[S, 1].
* deg_O(r) := |N⁺(r) ∩ O| = Σ_{S ∋ r} x[S, ·] = d⁺(r) − 7 = 18 − j_r. (r beats a, b and 5 vertices of R.)
* d⁻(a) = 11 + n_0 and d⁻(b) = 12 + n_1.
* Σ_y (q_y − 5) = Σ_r deg_O(r) − 190 = 8 − J.
* For r ∈ R: Σ_{U ∋ r, |U| = 3} (|D(U)| − 5) = 5 + 10·j_r − Σ_{y : r ∉ Q_y} λ(q_y), where λ(q) = 10 − C(10 − q, 2).
* Σ_{|U| = 3} |D(U)| = 110 + Σ_y C(11 − q_y, 3).

λ(5), …, λ(10) = 0, 4, 7, 9, 10, 10. The last two identities are the exact form of the count in Lemma 2.1. The 45
triples through r get 30 dominator incidences from the 5 in-neighbours of r in R. They get C(10 − q_y, 2) more from
each y ∈ O that beats r, and there are 38 − deg_O(r) = 20 + j_r such y.

`unit_n51.py` tests every identity on 12 random planted tournaments (25 200 checks, 0 failures).

### 2.3 Rows

| label | row | reason |
|---|---|---|
| C1 | Σ x = 38 | \|O\| = 38 |
| adm | x[S, ·] exists only if \|S\| ≥ 5 and S meets N⁻_R(z) for every z ∈ R | (F1) for P ∪ {y}; S_4 for P ∪ {y, z} |
| C3(U), \|U\| = 2, 3, 4 | cR(U) + Σ_{S∩U=∅} x ≥ 11, 5, 1 | (F2), (F1), S_4 |
| C4(a, U), C4(b, U), \|U\| = 1, 2, 3 | cR(U) + Σ_{S∩U=∅} x[S, 0 or 1] ≥ 11, 5, 1 | (F2), (F1), S_4 for U ∪ {a}, U ∪ {b} |
| C5(r) | Σ_{S∋r} x + j_r = 18 | deg_O identity |
| C6 | Σ_r j_r ≤ 2, 0 ≤ j_r ≤ 2 | the hypothesis being refuted |
| M (in-mode) | n_1 = 12; n_0 ≥ 13; n_0 + J ≤ 19 | d⁻(b) = 24; d⁻(a) ≥ 24; (d⁻(a) − 25)⁺ + J ≤ \|Z\| ≤ 5 |
| M (out-mode) | n_0 = 13; n_1 ≥ 12; n_1 + J ≤ 18 | d⁻(a) = 24; d⁻(b) ≥ 24; (d⁻(b) − 25)⁺ + J ≤ \|Z\| ≤ 5 |
| M (reg, side result) | n_0 = 14; n_1 = 13; j = 0 | case (R): every in-degree is 25 |
| P2, P3, P4, P5, no \|S\| ∈ {7, 8} | see Lemma P | valid when J ≤ 2 |
| intersecting | x[S, ·] ≥ 1 and x[S′, ·] ≥ 1 imply S ∩ S′ ≠ ∅ | S_4 for {a, b, y, y′}: D = Q_y ∩ Q_y′ |

The rows "C4 for U ∪ {a, b}" with |U| ≤ 2 only say cR(U) ≥ 1 (the S_2 property of the class) and cR({u}) = 5, so they
add nothing.

The M rows use the case (I) hypotheses: minimum in-degree ≥ 24, |Z| ≤ 5 (Claim Q), and Σ_{x ∉ Z} (d⁻(x) − 25) = |Z|.
Every term of that sum is ≥ 0, and R together with the endpoint that is not in Z contributes part of it.
**The type-free model uses none of the M rows.** So a type-free certificate needs neither the in-degrees of the
endpoints nor the case (I) hypotheses.

### 2.4 Lemma P (structure when J ≤ 2)

**Lemma P.** If J ≤ 2, then:
1. no y ∈ O has q_y ∈ {7, 8};
2. exactly one y* ∈ O has q_{y*} ≥ 9;
3. at most two y ∈ O have q_y = 6;
4. every r ∉ Q_{y*} has j_r ≥ 1, and every r satisfies c_r + b_r ≤ 1 + j_r. Here c_r = #{y : q_y = 6, r ∉ Q_y} and
   b_r = [q_{y*} ≤ 10 and r ∉ Q_{y*}].

*Proof.* By §2.2 and (F1), every r satisfies

  Σ_{y : r ∉ Q_y} λ(q_y) ≤ 5 + 10 j_r.  (∗)

1. If q_y = 7, each of the 4 vertices r ∉ Q_y has 7 ≤ 5 + 10 j_r. So j_r ≥ 1 for each, and J ≥ 4. If q_y = 8, the
   same argument with λ = 9 gives J ≥ 3.
2–3. Let n_6 = #{q = 6} and m = #{q ≥ 9}. By (F1), Σ_y C(11 − q_y, 3) ≥ 825 − 110 = 715. The left side is
   760 − 10 n_6 − 20 m, since q = 5 contributes 20, q = 6 contributes 10, and q ≥ 9 contributes 0. So
   10 n_6 + 20 m ≤ 45. The deficit identity gives n_6 + Σ_{q_y ≥ 9} (q_y − 5) = 8 − J ≥ 6.
   * If m = 0 then n_6 ≥ 6, contradicting 10 n_6 ≤ 45.
   * If m ≥ 2 the deficit is ≥ 8, so J = 0 and both of these vertices have q = 9. But then (∗) at a vertex outside one
     of them gives 10 ≤ 5.
   So m = 1, and n_6 ≤ 2.
4. If r ∉ Q_{y*}, then λ(q_{y*}) = 10 ≤ 5 + 10 j_r, so j_r ≥ 1. For the inequality, (∗) gives
   4c_r + 10b_r ≤ 5 + 10 j_r.
   * j_r = 0: b_r = 0 and c_r ≤ 1.
   * j_r = 1: if b_r = 1 then c_r ≤ 1; if b_r = 0 then c_r ≤ n_6 ≤ 2.
   * j_r = 2: c_r + b_r ≤ 3. ∎

As linear rows:
* **P2**: Σ_{|S| ≥ 9} x = 1.
* **P5**: Σ_{|S| = 6} x ≤ 2.
* **P3(r)**: Σ_{|S| ∈ {9,10}, r ∉ S} x ≤ j_r.
* **P4(r)**: Σ_{|S| ∈ {6,9,10}, r ∉ S} x ≤ 1 + j_r.
* The variables with |S| ∈ {7, 8} are deleted.

P3 and P4 are valid because exactly one y has q ≥ 9.

### 2.5 Relation to the f4 agent's model (`tightJ51.py`, `runJ.py`, `runJnt.py`, `runJnt2.py`)

These rows are the same as in `tightJ51.py`: C1, adm, C3, C4, C5, the in-mode rows n_1 = 12, n_0 ∈ [13, 19] and
n_0 + J ≤ 19, and the out-mode rows n_0 = 13 and n_1 ∈ [12, 18].

Its cuts #{y → r : 7 ≤ q_y ≤ 10} ≤ 2j_r, #{y → r : q_y = 6} ≤ 1 + 2.5 j_r and #{q ≥ 6} ≤ 4 are integer roundings of
(∗) and of the triple count. The pattern cuts of `runJnt2.py` (no q ∈ {7, 8}, exactly one q ≥ 9, at most two q = 6)
are cited there as "notes Step 17", which is not in `notes.md`; Lemma P proves them.

The differences here:
* the intersecting property is new;
* P3, P4 and the out-mode budget n_1 + J ≤ 18 are new;
* `tightJ51.py` kept the 5-set variables continuous. `runJ.py` and `portfolio_J.py` made them integer, but the earlier
  runs gave HiGHS MILP verdicts without certificates.

## 3. Certification method

**Branch and bound with exact leaves.** For a class c and a mode m ∈ {free, in, out, reg}, a binary tree refutes the
integer program of §2:

* A node is the root box (0 ≤ x ≤ 38, 0 ≤ j_r ≤ 2, or j = 0 in reg mode) plus the branching bounds on the path to
  it, closed under the **intersecting rule**: if some x[S, t] has lower bound ≥ 1, every x[S′, t′] with S′ ∩ S = ∅
  gets upper bound 0.
* A branch on an integer variable v at value k has the two children v ≤ k and v ≥ k + 1, so the children cover the
  node.
* A leaf is an **exact Farkas certificate**. (The format also allows an 'X' leaf, where two disjoint sets are both
  forced ≥ 1. None occurs in the final trees.)

A Farkas certificate is a vector of integers y, one per row, with y ≥ 0 on '≥' rows and y ≤ 0 on '≤' rows, such that

  Σ_i y_i·rhs_i  >  max over the node box of Σ_k (Σ_i y_i·a_ik)·x_k.

Every feasible point satisfies Σ_i y_i (a_i·x) ≥ Σ_i y_i rhs_i. So such a y proves that the node contains no point,
not even a fractional one. The check uses Python integers only, with no floating point.

**Skeleton split.** Some trees start with a 'K' node. By Lemma P, an integer point has exactly one big variable
x[S*, t*] = 1 (with |S*| ≥ 9) and an integer vector j with Σ j ≤ 2, and row P3 forces j_r ≥ 1 for every r ∉ S*.
* The K node has one child per skeleton (S*, t*, j), in which x[S*, t*] ≥ 1 and j is fixed. It may list only one
  skeleton per orbit of the automorphism group of T[R].
* This is enough because relabelling R by an automorphism σ maps a configuration to a configuration (S ↦ σ(S), types
  kept, j_{σ(r)} = j_r).
* The checker verifies that every listed permutation is an automorphism, and that every skeleton allowed by P3 and
  the box is mapped onto a listed one.

**Auxiliary variables** (used only in the class 0 out-mode tree). These are integer variables, each tied to the x by an
equality row:
* z[S] = Σ_t x[S, t] for |S| ∈ {5, 6} (row Z);
* n_t = Σ_S x[S, t] (row N);
* c_r = #{y : q_y = 6, r ∉ Q_y} (row Cc).

They are integers because the x are, so branching on them is valid. The search branches on c, then on z for 6-sets,
then n, then z for 5-sets, and only then on the individual x[S, t]. On the hard class 0 skeletons this cuts the tree
about ninefold (167 nodes against about 1500). The intersecting rule also applies to z[S] ≥ 1. The auxiliary
variables and rows are appended after the base ones, so a subtree computed without them keeps its indices and is still
valid inside the larger system. That lets the class 0 K node combine subtrees from both runs.

**Producer and checker.**
* **Producer.** `lmodel.py` builds the rows. `bnb.py` runs the search with the HiGHS dual simplex, warm-started; it
  rounds dual rays to integers and verifies them. `skel.py` and `run_skel_par.py` add the skeleton split.
  `run_presplit.py` splits the subtree of a hard skeleton further on n_1, into the boxes n_1 ≤ 12, 13, 14, 15 and
  ≥ 16. It refutes each box separately and in parallel, and then joins them as a chain of branch nodes.
  `driver.py` runs all classes, and `recompress.py` shrinks the multipliers.
* **Checker.** `check_n51.py` imports none of these. From the class string it rebuilds the variable universe, every
  row from its label (with its own set arithmetic), every node box and the intersecting rule. It checks the K-node
  coverage and every leaf, exactly. It also checks that the class is 5-regular and S_2.
* **Unit tests.** `unit_n51.py` tests the identities of §2.2 on random planted tournaments (25 200 checks). It also
  checks that the producer and the checker build identical rows and boxes: 47 912 rows on 6 classes, in the free, in,
  out and reg modes, with and without the auxiliary variables. There were 0 failures.
* **Negative tests.** The checker rejects each of these corrupted trees:
  * a tree checked against the wrong class;
  * a tree with the C5 multipliers removed;
  * a tree with a shifted branching value;
  * a tree with relabelled rows;
  * a K node with one child dropped;
  * a K node with a non-automorphism;
  * a K node with the symmetry removed.

## 4. Results

*Status on 18 October 2026, 23:30. The checker was run again on the copies in `certificates.zip`. All 552 trees pass
and nothing fails (`check_partial.out`).*

| classes | mode | certificate | status |
|---|---|---|---|
| 1–550 | type-free (covers in-mode and out-mode) | branch-and-bound tree. Classes 60, 311, 343, 416 and 501 start with a skeleton split (265 skeletons each) | certified, checker OK |
| 0 | in | one Farkas certificate at the root | certified, checker OK |
| 0 | reg (side result, case (R)) | skeleton split, 3 skeletons | certified, checker OK |
| 0 | out | skeleton split, 75 skeletons | **open**: 69 of 75 subtrees done |

The 550 type-free trees have between 1 and 4170 leaves. Class 501 has the most.

**The open case: class 0, out-mode.** The K node has 75 skeleton representatives under the automorphism group of
order 11. 69 subtrees are finished: 48 from the base model and 21 from the model with auxiliary variables. They are
stored in `skelcache.zip`. They have **not** yet been joined into a K-node tree, so the checker has not seen them.

The six open skeletons are indices 62, 63, 64, 65, 66 and 70 of `skel.skeleton_list`. In all six, the big set is
S* = R (q_{y*} = 11) and J = 2:

| index | big variable | j | n_1 boxes done | n_1 boxes open |
|---|---|---|---|---|
| 62 | x[R, 1] | j_9 = j_10 = 1 | ≤ 12, 13, 14 | 15, ≥ 16 |
| 63 | x[R, 1] | j_8 = j_10 = 1 | ≤ 12, 13, 14, 15 | ≥ 16 |
| 64 | x[R, 1] | j_7 = j_10 = 1 | ≤ 12, 13, 14, 15 | ≥ 16 |
| 65 | x[R, 1] | j_6 = j_10 = 1 | ≤ 12, 13, 14, 15 | ≥ 16 |
| 66 | x[R, 1] | j_5 = j_10 = 1 | ≤ 12, 13, 14 | 15, ≥ 16 |
| 70 | x[R, 2] | j_9 = j_10 = 1 | ≤ 12 | 13, 14, 15, ≥ 16 |

Here r is the position of the vertex in the class string, from 0 to 10. Since J = 2, the out-mode rows n_1 ≥ 12 and
n_1 + J ≤ 18 leave n_1 ∈ {12, …, 16}. So the box "≥ 16" is n_1 = 16. That leaves 11 boxes in all. Each finished
n_1 = 15 box took 25–36 minutes.

**Comparison with the earlier runs.** `portfolio_J.py` left classes 0, 1, 7, 8, 17, 18, 21, 29 and 32 undecided, and
never ran classes 35–550. All of these are now certified except class 0 in out-mode.
* Classes 1, 7, 8, 17, 18, 21, 29 and 32 need only the type-free model, with 87 to 1325 branch-and-bound nodes.
* Class 0 is the circulant class with automorphism group of order 11, the same class that needed a split in case (R).
  Its in-mode certificate uses only n_1 = 12 and the rows C4(b, U) with |U| = 2. Its out-mode needs the skeleton
  split, and that split is not finished.

**One case is left open: class 0 in out-mode.**

## 5. What the certificates rest on

The certificates are exact, and the checker is independent of the producer. What they mean rests on the following.
Each item is proved by hand above or in `ERDOS902_PROOF.md`, or checked as stated.

1. (F1), (F2), S_4 and Lemma 1.3 (§1 of the proof file), and Lemma 2.1 (Lemma T, which gives j_r ≥ 0).
2. The identities of §2.2, which are exact counts and are also tested on planted tournaments, and Lemma P (§2.4).
3. The intersecting property (S_4 for {a, b, y, y′}).
4. **The class list.** T[D(P)] is a 5-regular S_2 tournament on 11 vertices, and `reg11_S2.txt` must list every one
   of them exactly once. `verify_classes.py` now checks this independently:
   * An exact recursion counts 48 251 508 480 labelled regular tournaments on 11 vertices.
   * The 1223 lines of `reg11.txt` are pairwise non-isomorphic (canonical forms), and Σ 11!/|Aut| over them equals
     that count. So `reg11.txt` contains every regular tournament on 11 vertices.
   * Its S_2 members are exactly the 551 classes of `reg11_S2.txt`: the same canonical forms, with no repeats.
   * The output is in `n51_local/verify_classes.out`.
5. The in-mode and out-mode certificates use the M rows, and only those certificates need the case (I) hypotheses.
   Only class 0 has in-mode or out-mode certificates: the in-mode one now, and the out-mode one once it is finished.
   The hypotheses are:
   * minimum in-degree ≥ 24 at N = 51 (computer-assisted, §8.1 of the proof file, not re-verified here);
   * Claim Q (|Z| ≤ 5, proved by hand);
   * the excess identity Σ_{x ∉ Z} (d⁻(x) − 25) = |Z|.

The type-free certificates use only items 1–4 and N = 51.

**Sanity check.** Without the hypothesis J ≤ 2, the model has integer solutions. `sanity_minJ.py` minimises J with
the Lemma P rows removed and all set sizes allowed, then re-checks the solution against every row exactly.
**Not run yet:** there is no `sanity_minJ.out`.

## 6. Files (`proof/n51_local/`)

| file | role |
|---|---|
| `lmodel.py`, `lpcert.py`, `bnb.py`, `skel.py` | producer: rows, LP and certificate rounding, branch and bound, skeleton split |
| `driver.py`, `run_skel.py`, `run_skel_par.py` | runs: plain search per class, skeleton split, parallel skeleton split with a per-skeleton cache |
| `run_presplit.py`, `skel_status.py` | class 0 out-mode: split hard skeletons on n_1; show which skeletons are cached and which are open |
| `select_final.py` | pick one tree per needed (class, mode) and write `certificates.zip` (it stops if class 0 out-mode is missing) |
| `add_labels.py`, `recompress.py`, `recompress_all.py` | post-processing: attach label tables to early trees; shrink the multipliers (re-verified exactly) |
| `check_n51.py` | the independent checker; it imports nothing from the producer |
| `unit_n51.py`, `unit_n51.out` | planted-configuration identity tests, and producer/checker agreement on rows and boxes |
| `verify_classes.py`, `verify_classes.out` | completeness of the class list |
| `sanity_minJ.py` | the model is satisfiable once J > 2 is allowed (not run yet) |
| `summarize.py`, `stats.py` | tables and statistics from the checker output |
| `reg11.txt`, `reg11_S2.txt` | the 1223 regular and the 551 regular S_2 tournaments on 11 vertices (copied from the results zip) |
| `certificates.zip` | the 552 finished trees, one per certified (class, mode): `<class>_<mode>[_skel].json.gz`. That is 550 type-free trees (classes 1–550), `0_in` and `0_reg_skel`. The class 0 out-mode tree is missing. |
| `check_partial.out` | the checker's output on the 552 trees in `certificates.zip`: 552 OK, 0 failures |
| `skelcache.zip` | the finished pieces of the class 0 out-mode split: 69 skeleton subtrees and 20 n_1 boxes. Unzip into `skelcache/` to resume. |
| `logs/` | search logs |

`check_all.out` (the checker's output on every certificate) and `results.tsv` (per class: status of in-mode and
out-mode, and the certificate used) will be written once class 0 out-mode is finished.

To re-check the finished certificates, unzip `certificates.zip` into `certs/` inside `n51_local/`, then run

```bash
python check_n51.py reg11_S2.txt certs/*.json.gz > check_partial.out
```

To finish class 0 out-mode, work inside `n51_local/`:
1. Unzip `skelcache.zip` into `skelcache/`. Make empty `trees/` and `ctrees/` folders.
2. Refute the open boxes with `python run_presplit.py 0 out <nproc> 62,63,64,65,66,70`. Pieces already in the cache
   are skipped.
3. Join the K-node tree from the cache with `python run_skel_par.py 0 out <nproc> 0 100000 skelaux`. Shrink it with
   `python recompress.py trees/0_out_skelaux.json.gz ctrees/0_out_skelaux.json.gz`.
4. Unzip `certificates.zip` into `ctrees/` as well. Rebuild the zip with `python select_final.py certificates.zip`.
5. Run the checker on every tree and write `check_all.out`. Then run `python summarize.py check_all.out results.tsv`.

Requirements: Python 3, numpy, scipy and highspy for the producer. The checker needs only the Python standard library.
