# AUDIT-52-B: hostile audit of the N = 52 notes, back to front (Lemma C focus)

*Round 1 of the swarm, 23 October 2026. Hand derivations only; no scripts, no search. Nothing outside this file was edited.*
*Files read: BRIEF.md, N52_TIGHT_PAIRS.md = [TP] (all of it), N52_ATTEMPT.md = [A52], F4_GE_52_HAND_PROOF.md = [52], ERDOS902_PROOF.md = [EP] sections 1-2.*

## Status (kept current; round 2 continuation, 24 Oct 2026)

* DONE and proved by hand (sections 4-8 below were written by the continuing agent AUDIT-52-B2; sections 0-3 by the interrupted earlier agent):
  * **Theorem 4.3 (Lemma C, uniform proof): s = |V_+| >= 4.** Invariant nu_u = j_u - (#heavy y beating u), sum over V_+ of nu_u = 14 - 6h; s = 0, 1, 2 done by the identity plus rho_u and the pair inequality; s = 3 forces nu_1 = nu_2 = nu_3, then 3x = 14 - 6h is impossible mod 3.
  * J = 4 excluded (5.2, complete nine-partition case list); hence **J >= 5** (part 2 of the [TP] theorem), without Theorem 1 of [52].
  * Audit of [TP] sections 3-5 (5.1): conclusions all correct; one genuine omitted case (J=4, s=3, partition 5+5), one stray bullet, one garbled bullet, one misstated row (J=4, s=4, 5+5 says 11, true 17), one under-justified row (6+4), one single-shape argument (J=5, s=3, 6+3).
  * [TP] section 7 (314028, 305500) re-derived correct, plus a sharper form sum_Y C(k-5,2) >= 8528 (6.1). Lemma B re-derived correct (6.2).
  * Lead's inequality tau_i <= 5 j_i verified (7.1); new consequences: slack identity, (G), nu bounds (7.2).
  * Theorem S (8.1): necessary structure of a surviving tight pair; complete J = 5 analysis (8.2): four configurations survive the counting tools, all with a q = 11 vertex.
* OPEN / not claimed: no tight pair is excluded; the counting tools cannot exclude J = 14 with h = 0 (8.3). f(4) >= 53 is NOT proved by this file.
* Not re-audited line by line: [TP] section 9 s = 3 bullets (superseded by Theorem 4.3; spot-checks in section 9.2 found no error; the case E = 0 is missing in [TP] s = 1).

## 0. Bottom line

1. **Lemma C is true.** Every tight pair P of an F1-tournament on 52 vertices has at least four dominators of in-degree > 25.
2. The proof of Lemma C written in [TP] section 9 is **correct after gaps that I fill** (list in section 3). No case is false. Gaps: the case E = 0 (J = 14) is never treated; several "the other two degrees are ..." sub-splits are incomplete; two numeric slips; one wrong case label.
3. [TP] sections 3-5 (J = 3, 4, 5) are right in conclusion but **contain garbled passages** (section 4, s = 3 bullets belong to J = 3; the 5 + 5 row of the s = 4 table states "11 dominators", the true value is 17; the 6 + 4 row needs a rounding step that is not written; section 5 "6 + 3" covers only one degree shape). All are repaired in section 5 below.
4. **New: a uniform two-page proof of Lemma C** (section 4). It uses only Lemma A, the pair-sum formula (PS), the pair-excess formula (S), the budget (B), c <= 4 and the count (E). It does not use Theorem 1 of [52], does not use J >= 3, and has no case list. The key invariant is
   nu_u := j_u - (number of heavy outside vertices missing u),  with  **sum over V_+ of nu_u = 14 - 6h**  (h = number of heavy outside vertices).
   For s = |V_+| <= 3 it forces all nu_u equal, and then sum nu = 14 - 6h has no solution (14 is 2 mod 3 and 2 mod 6).
5. **Lemma B (no in-degree 23) is correct** as written, and so is [A52] Lemma 1 (same proof). [TP] section 7 (balanced degrees) is correct; I add a sharper form of its conclusion.
6. [A52] section 1 (SF) and [TP] Lemma A are **correct at N = 52**, including the case where outside vertices with q = 7 or 8 exist (they cannot miss a vertex of in-degree 25) and the mod-4 rounding.
7. This does **not** prove f(4) >= 53. It does not exclude a tight pair: s >= 4 remains. Section 8 records what a surviving tight pair must look like.

## 1. Notation (as in [TP])

N = 52, P = {a, b} tight, R = D(P), |R| = 11, T[R] 5-regular, O = V minus (P union R), |O| = 39. For y in O: Q_y = R inter N^-(y), q_y = |Q_y| >= 5, M_y = R minus Q_y (the vertices of R that y beats), |M_y| = 11 - q_y. For r in R: d^-(r) = 25 + j_r, J = sum j_r, V_0 = {j = 0}, V_+ = {j > 0}, s = |V_+|. A y is **heavy** if q_y >= 6, a **5-vertex** if q_y = 5. For u, v in R: c(u,v) = number of vertices of R beating both; D_uv = |D({u,v})|; s(u,v) = sum over w in R minus {u,v} of (|D({u,v,w})| - 5) (this is [TP]'s s(u, v); I write it s(u,v) to separate it from s = |V_+|).

Everything below that is called "proved" has every step written out. Verdicts: **OK** = correct as written; **OK+gap** = correct after the gap I fill; **WRONG** = false as written (and what is true).

## 2. Re-derivation of the base identities at N = 52

**(I1)** r in R beats a, b and exactly 5 vertices of R, and d^+(r) = 51 - d^-(r) = 26 - j_r. So r beats 26 - j_r - 7 = 19 - j_r vertices of O. Hence #{y in O : r in Q_y} = 19 - j_r and **#{y in O : r not in Q_y} = 39 - 19 + j_r = 20 + j_r.** (Equivalently: the in-neighbours of r are 5 in R, none in P, and 20 + j_r in O, total 25 + j_r.) Verdict: OK.

**(E)** Sum_y q_y = sum_r (19 - j_r) = 209 - J. Sum_y (q_y - 5) = 209 - J - 5*39 = 209 - 195 - J = **14 - J.** [TP] (E) says 6N - 298 - J = 312 - 298 - J = 14 - J. OK. Since each term is >= 0, J <= 14.

**(2.1)** For U a subset of R: D(U) = {w in R minus U : U inside N^+(w)} union {y in O : U inter Q_y = empty}. (a, b are beaten by every vertex of R, so they dominate nothing in R.) y in O dominates U iff y beats every vertex of U iff U inter Q_y = empty.

**(Ex) and (*)** For r in R there are C(10,2) = 45 triples U inside R with r in U. Dominators of these triples: (i) the 5 vertices w in R that beat r: w dominates U iff U inside N^+(w) inter R (a 5-set containing r), so C(4,2) = 6 triples each, 30 in all; (ii) the 20 + j_r vertices y in O with r not in Q_y: y dominates U iff U inside R minus Q_y (size 11 - q_y, contains r), so C(10 - q_y, 2) triples. Hence
sum_U (|D(U)| - 5) = 30 + sum_{y: r not in Q_y} C(10 - q_y, 2) - 225.
Write C(10 - q, 2) = 10 - lambda(q), lambda(q) = 10 - C(10-q, 2): lambda(5) = 10 - 10 = 0, lambda(6) = 10 - 6 = 4, lambda(7) = 10 - 3 = 7, lambda(8) = 10 - 1 = 9, lambda(9) = lambda(10) = 10 - 0 = 10. Then 30 + 10(20 + j_r) - 225 = 5 + 10 j_r, so
**Ex(r) := sum over triples U inside R containing r of (|D(U)| - 5) = 5 + 10 j_r - sum_{y: r not in Q_y} lambda(q_y) >= 0.**
Verdict: OK+gap. The gap is notation: [TP] writes the sum over "U containing r, |U| = 3", which read literally is all triples of V; it must be **triples U inside R**. The table entry lambda(11) is vacuous (q = 11 means r is in Q_y). Both are harmless.

**(R1) (generalised)** For u != v in R:
s(u,v) = 3c(u,v) + 4k_5 + 3k_6 + 2k_7 + k_8 - 45, where k_q = #{y : q_y = q, u,v not in Q_y}.
Proof. A vertex w' in R that beats u and v (there are c(u,v)) dominates {u,v,w} for each of the 3 vertices w in (N^+(w') inter R) minus {u,v}: w' beats exactly 5 vertices of R, two of which are u and v. A y in O with u,v not in Q_y dominates {u,v,w} for each w in R minus Q_y minus {u,v}: 11 - q_y - 2 = 9 - q_y vertices (4, 3, 2, 1, 0 for q = 5,...,9, and 0 for q >= 9). Total: 3c + sum (9 - q_y)^+ - 9*5. OK.

**(R2) (generalised)** Sum_{v != u} s(u,v) = 10 + 20 j_u - 8 beta_6 - 14 beta_7 - 18 beta_8 - 20 gamma, where beta_q(u) = #{y : q_y = q, u not in Q_y} and gamma(u) = #{y : q_y >= 9, u not in Q_y}.
Proof. Sum (R1) over the 10 vertices v. Sum_v c(u,v) = 5 * 4 = 20 (each of the 5 in-neighbours of u in R beats 4 other vertices of R besides u). A y with u not in Q_y and q_y = q has 10 - q vertices v in R minus {u} outside Q_y, so sum_v k_5 = 5 alpha_u, sum_v k_6 = 4 beta_6, sum_v k_7 = 3 beta_7, sum_v k_8 = 2 beta_8, with alpha_u = 20 + j_u - beta_6 - beta_7 - beta_8 - gamma (by (I1)). So the sum is 60 + 20 alpha + 12 beta_6 + 6 beta_7 + 2 beta_8 - 450 = 10 + 20 j - 8 beta_6 - 14 beta_7 - 18 beta_8 - 20 gamma. Same as 2 Ex(u) = 2(5 + 10 j - 4 beta_6 - 7 beta_7 - 9 beta_8 - 10 gamma): consistent. OK. This is the formula quoted in [A52] section 1 and in [52] end of section 2. Verdict: OK.

**(PS)** For u in R let tau_u = sum over y in O with u not in Q_y of (q_y - 5). Then sum_{v != u} D_uv = 120 + 5 j_u - tau_u.
Proof. D_uv = c(u,v) + #{y in O : u, v not in Q_y}. Sum_v c = 20. Sum_v #{...} = sum over the 20 + j_u vertices y with u not in Q_y of (11 - q_y - 1) = (10 - q_y) = 5 - (q_y - 5). So 20 + 5(20 + j_u) - tau_u = 120 + 5 j_u - tau_u. Verdict: OK.

**(S)** s(u,v) = 4 D_uv - c(u,v) - 45 - E_both(u,v), with E_both(u,v) = sum of (q_y - 5) over y missing both u and v.
Proof. s = 3c + sum_{y missing u,v} (9 - q_y)^+ - 45. A y missing both u and v has q_y <= 9, since it misses at least two vertices, so (9 - q_y)^+ = 9 - q_y = 4 - (q_y - 5). With K = #{y missing u,v} = D_uv - c: s = 3c + 4K - E_both - 45 = 4 D_uv - c - 45 - E_both. Verdict: OK (the remark q_y <= 9 is the point that [TP] leaves unsaid; q = 10, 11 vertices miss at most one vertex of R).

**(B)** The nine triples {u,v,w} are among the triples inside R containing u, all excesses are >= 0, so s(u,v) <= Ex(u); symmetrically s(u,v) <= Ex(v). OK.

**Consequences used repeatedly.**
(a) c <= 4 (if u -> v then u is one of the 5 in-neighbours of v in R but u does not beat itself, so at most 4 common beaters; symmetric if v -> u). So s(u,v) >= 4 D_uv - 49 - E_both. The phrase in [TP] "a pair with E_both = 0 and D dominators has triple-excess at least 4D - 49" is correct; it is **only** valid with E_both = 0 (in general subtract E_both).
(b) s(u,v) >= 0 and (S) give D_uv >= (45 + c + E_both)/4 >= 45/4, so **D_uv >= 12 for every pair inside R** (even 11 is excluded: a tight pair inside D(P) would give s = -1 - c - E_both < 0). [TP] only uses D >= 11 ("fewer than 11 dominators"); this is weaker than available but valid.

## 3. Lemma A and (SF) at N = 52

**Statement (Lemma A of [TP]; (SF) of [A52]).** If j_u = 0 then (i) u lies in Q_y for every y in O with q_y >= 6 (equivalently every y -> u is a 5-vertex), (ii) c(u,v) <= 3 for all v in R, (iii) D_uv = 12 and s(u,v) = 3 - c(u,v) for all v != u.

**Proof (from scratch).** j_u = 0 gives, by (Ex) and (*), sum over y missing u of lambda(q_y) <= 5.
* lambda(q) >= 7 for q = 7, 8, 9, 10, so no y with q_y >= 7 misses u. Two 6-vertices missing u would give 8 > 5. So beta_7 = beta_8 = gamma = 0 and beta_6 =: beta in {0, 1}. (Equivalently from (R2): 10 - 8 beta_6 - 14 beta_7 - 18 beta_8 - 20 gamma >= 0.)
* Outside vertices with q = 7, 8 may well exist elsewhere in O; they simply do not miss u, so k_7(u,v) = k_8(u,v) = 0 for every v. Hence (R1) reads s(u,v) = 3c + 4k_5 + 3k_6 - 45 with k_6(u,v) =: m(v) in {0,1}, and sum_v m(v) = 4 beta (the unique 6-vertex y_6 missing u misses 4 more vertices of R).
* Mod 4: 3c - 45 + 3m = 3c + 3m - 48 + 3 and 3 = -1 (mod 4), so s(u,v) = 3 - c - m (mod 4), with s >= 0 and c + m <= 4 + 1 = 5. If c + m <= 3 the least admissible value is 3 - c - m; if c + m in {4, 5} it is 7 - c - m (3 and 2 respectively). So s(u,v) >= 3 - c - m + 4*[c + m >= 4].
* Sum over the ten v: sum_v s(u,v) >= 30 - 20 - 4 beta + 4 N_4 = 10 - 4 beta + 4 N_4, where N_4 = #{v : c + m >= 4}. But sum_v s(u,v) = 2 Ex(u) = 2(5 - 4 beta) = 10 - 8 beta. So -4 beta >= 4 N_4, i.e. **beta = N_4 = 0**.
* Now every y missing u is a 5-vertex, m = 0, and sum_v s(u,v) = 10 = sum_v (3 - c(u,v)) with termwise s >= 3 - c >= 0 (as c <= 3 because N_4 = 0). So s(u,v) = 3 - c(u,v) for every v, c <= 3, and (R1) gives 4 k_5 = 48 - 4c, k_5 = 12 - c. All y missing both u and v are 5-vertices, so D_uv = c + k_5 = 12. QED.

Verdict: **OK** (both [TP] Lemma A and [A52] (SF)). One small slip in [TP]: it says m(v) = 1 "when that 6-vertex misses both u and v" and writes the congruence with "a multiple of the same residue"; the precise reason is the one above (3k_6 = -k_6 mod 4 with k_7 = k_8 = 0). The "N = 52" never enters the proof of Lemma A except through (I1) (20 + j_u) and (I3); it holds at every order.

**Corollary A'. (net-zero vertices)** The same proof gives a generalisation I use later: if all outside vertices of q >= 6 missing u have q >= 9 (no 6-, 7-, 8-vertex misses u) and Ex(u) = 5 (that is, j_u equals the number of q >= 9 vertices missing u), then s(u,v) = 3 - c(u,v), c(u,v) <= 3 and D_uv = 12 + (number of q = 9 vertices missing both u and v) for all v. Proof: with beta_6 = beta_7 = beta_8 = 0, s(u,v) = 3 - c (mod 4); sum_v s(u,v) = 2 Ex(u) = 10 = sum_v (3 - c); equality forces s = 3 - c termwise; then (S) gives 4 D_uv = 48 + E_both and E_both = 4 * #(q = 9 missing both u, v). (Used in sections 5 and 8.)

## 4. A uniform proof of Lemma C (round 2 continuation, 24 Oct 2026)

*Written by the continuing agent (AUDIT-52-B2). Everything here is re-derived from scratch from the base identities of section 2 and Lemma A of section 3; the earlier agent's reasoning was lost, so nothing is taken on trust except the verified items of sections 2-3.*

**4.0 Notation and the facts used.** N = 52, P tight, R = D(P), O the 39 outside vertices, V_0, V_+, s = |V_+|, j_u, J as in section 1. For y in O write M_y = R minus Q_y (the vertices of R that y beats), t_y = |M_y| = 11 - q_y, e_y = q_y - 5 = 6 - t_y >= 0. "y beats u" means u is in M_y. H = set of heavy y (q_y >= 6, i.e. e_y >= 1, i.e. t_y <= 5), h = |H|. A 5-vertex has e_y = 0, t_y = 6. m_u = number of heavy y beating u. Also delta_uv := D_uv - 12 for u, v in R.

Facts (each proved in sections 2-3):
* (E) sum over y in O of e_y = 14 - J, hence sum over H of e_y = 14 - J.
* (A-i) [Lemma A (i)] if j_u = 0 then no heavy y beats u. So M_y is inside V_+ for every y in H, and t_y <= s.
* (A-iii) if j_u = 0 then D_uv = 12 for all v.
* (PS) for u in R: sum over v != u of D_uv = 120 + 5 j_u - tau_u, tau_u = sum over y beating u of e_y.
* (D12) D_uv >= 12 for every pair inside R (section 2, consequence (b)).
* (S) s(u,v) = 4 D_uv - c(u,v) - 45 - E_both(u,v) >= 0, c <= 4, E_both(u,v) = sum of e_y over y beating both.
* (B) s(u,v) <= Ex(u) and <= Ex(v); (Ex) Ex(u) = 5 + 10 j_u - sum over y beating u of lambda(q_y).

**4.1 Proposition (the invariant).** Put nu_u := j_u - m_u for u in V_+ (an integer). Then

  **sum over u in V_+ of nu_u = 14 - 6h.**

*Proof.* By (A-i) each y in H beats exactly t_y vertices of R and all of them lie in V_+, so sum over V_+ of m_u = sum over H of t_y = sum over H of (6 - e_y) = 6h - (14 - J), using (E) and e_y = 0 off H. Hence sum nu_u = J - 6h + 14 - J = 14 - 6h. Check of the two kinds of special vertices: a y with q_y = 11 has t_y = 0, e_y = 6; it is heavy, it adds 1 to h and nothing to any m_u, and it contributes its 6 to (E): the identity holds because 6h counts exactly the 6 = t_y + e_y of each heavy vertex. A y with q_y = 10 has t_y = 1, e_y = 5, beats one vertex of V_+. A 5-vertex is not in H: it beats 6 vertices of R, is invisible to h, m_u and (E), and it is the reason nu_u is defined with heavy vertices only. QED. (Only (E), (A-i) are used; N = 52 enters through the constant 14.)

**4.2 Proposition (two reformulations).** For u in V_+, with Phi_u := sum over heavy y beating u of (t_y - 1) >= 0 and g_u := sum over heavy y beating u of C(t_y - 1, 2):

 (a) sum over v in V_+ minus {u} of delta_uv = rho_u := 5 nu_u + Phi_u.   (b) Ex(u) = 5 + 10 nu_u + g_u.

*Proof.* (a) Split (PS) over v in V_0 (there are 11 - s of them; D_uv = 12 by (A-iii) applied at v) and v in V_+ minus {u} (s - 1 of them): sum_{v in V_+ \ u} D_uv = 120 + 5 j_u - tau_u - 12(11 - s) = 12(s - 1) + 5 j_u - tau_u, so sum delta_uv = 5 j_u - tau_u. Now tau_u = sum over heavy y beating u of (6 - t_y) (5-vertices have e = 0), and m_u = number of such y, so 5 j_u - tau_u = 5(j_u - m_u) + sum (5 - 6 + t_y) = 5 nu_u + Phi_u. (b) For q in {5,...,10}, lambda(q) = 10 - C(10 - q, 2) (check: q = 5,...,10 gives 0, 4, 7, 9, 10, 10 as in section 2). A heavy y beating u has 6 <= q_y <= 10 and 10 - q_y = t_y - 1, so lambda(q_y) = 10 - C(t_y - 1, 2). A 5-vertex has lambda = 0. So sum over y beating u of lambda = 10 m_u - g_u and Ex(u) = 5 + 10 j_u - 10 m_u + g_u. QED.

By (D12) every delta_uv >= 0, so **rho_u >= 0** for every u in V_+ (this is the lead's inequality tau_u <= 5 j_u, see section 7).

**4.3 Theorem (Lemma C, uniform proof).** s >= 4. That is, at least four dominators of a tight pair have in-degree > 25.

*Proof.* Suppose s <= 3. Throughout, nu's are integers and the pair inequality is: for u != v in V_+,
  0 <= s(u,v) = 4 delta_uv + 3 - c(u,v) - E_both(u,v) <= min(Ex(u), Ex(v)), with 0 <= c <= 4,   (P)
which is (S) and (B) with 4 D = 48 + 4 delta.

*s = 0.* The sum in 4.1 is empty: 0 = 14 - 6h. But 14 is not divisible by 6.

*s = 1.* V_+ = {u}. A heavy y beating u has t_y = 1, so Phi_u = 0, and there is no v in V_+ minus {u}, so rho_u = 0 (empty sum). Thus nu_u = 0 and 4.1 gives 0 = 14 - 6h, impossible.

*s = 2.* V_+ = {u, v}; let n be the number of y with M_y = {u, v} (those have e_y = 4); other heavy y beating u or v have t = 1. Phi_u = Phi_v = n (only the t = 2 vertices contribute, 1 each); g_u = g_v = 0. With delta = delta_uv, 4.2(a) at u and at v gives delta = 5 nu_u + n = 5 nu_v + n, so nu_u = nu_v =: x and delta = 5x + n. E_both(u,v) = 4n. Then (P) reads
  s(u,v) = 4(5x + n) + 3 - c - 4n = 20 x + 3 - c, and 20x + 3 - c >= 0, and 20 x + 3 - c <= Ex(u) = 5 + 10 x.
The first gives 20 x >= c - 3 >= -3, so x >= 0 (x integer). The second gives 10 x <= 2 + c <= 6, so x <= 0. Hence x = 0 and 4.1 gives 0 = 14 - 6h, impossible.

*s = 3.* V_+ = {1, 2, 3}, x_i := nu_i. Heavy y are of types M_y = empty (n_0 of them, e = 6), {i} (n_i, e = 5), {i,k} (n_ik, e = 4), {1,2,3} (n of them, e = 3). Then Phi_1 = n_12 + n_13 + 2n, g_1 = n (a t = 3 vertex gives C(2,2) = 1, a t = 2 vertex gives C(1,2) = 0), and cyclically. 4.2(a) gives rho_i = 5 x_i + Phi_i, and the three equations delta_12 + delta_13 = rho_1 etc. solve to
  delta_12 = (rho_1 + rho_2 - rho_3)/2 = (5/2)(x_1 + x_2 - x_3) + n_12 + n
(the Phi's combine as (n_12 + n_13 + 2n) + (n_12 + n_23 + 2n) - (n_13 + n_23 + 2n) = 2 n_12 + 2n). Also E_both(1,2) = 4 n_12 + 3n. So
  s(1,2) = 10 (x_1 + x_2 - x_3) + 4 n_12 + 4n + 3 - c_12 - 4 n_12 - 3n = 10 (x_1 + x_2 - x_3) + n + 3 - c_12.
Now s(1,2) <= Ex(1) = 5 + 10 x_1 + n gives 10 (x_2 - x_3) <= 2 + c_12 <= 6, hence x_2 <= x_3. And s(1,2) <= Ex(2) gives x_1 <= x_3. Applying the same to the pair {1,3} gives x_3 <= x_2 and x_1 <= x_2; to {2,3} gives x_3 <= x_1 and x_2 <= x_1. Therefore x_1 = x_2 = x_3 =: x and 4.1 reads 3x = 14 - 6h. The left side is a multiple of 3, 14 - 6h is 2 mod 3. Impossible.

So s <= 3 is impossible. QED.

**What the proof used and did not use.** It uses: (E), Lemma A, (PS), (S), (B), c <= 4, D >= 12 inside R (which came from s >= 0). It does NOT use Theorem 1 of [52], not J >= 3, not any case list on E = 14 - J, and no discussion of excess partitions. Every step was written above; the only place numbers appear is 14 (mod 6 and mod 3) and the inequalities 10 (x_2 - x_3) <= 6 and 10x <= 6. Verdict on [TP] Lemma C: **true**; this section is a complete proof (status proved_by_hand).

**4.4 Check of the invariant on a toy configuration (to see that nothing is vacuous).** Take s = 4 with all j = 1 (J = 4), heavy vertices of types e = 6 (t = 0) and e = 4 (t = 2 beating vertices 1, 2): h = 2, E = 10 = 14 - 4. Then m_1 = m_2 = 1, m_3 = m_4 = 0, nu = (0, 0, 1, 1), sum = 2 = 14 - 12. The identity holds. (This configuration is the 6 + 4 row of [TP] section 4, killed in section 5 below.)

## 5. [TP] sections 3-5 (J = 3, 4, 5): audit, repairs, and the complete J = 4 case

**5.0 What Theorem 4.3 does to these sections.** Theorem 4.3 gives s >= 4, and s <= J always (each vertex of V_+ has j >= 1). Hence:
* J = 3 is impossible at once (s <= 3 contradicts Theorem 4.3); so is J <= 3 in general. This reproves [TP] section 3 and, with Theorem 1' of the earlier audit, is independent of it.
* J = 5 forces s in {4, 5}: this is exactly the claim of [TP] section 5, and it needs no case work.
* J = 4 forces s = 4 and j = (1,1,1,1). That one case remains and is done in 5.2 below.
I nevertheless audited the old case lists, as the assignment asked; results are in 5.1.

**5.1 Line-by-line verdicts on the old text** (each case recomputed with the pair formula A_i = 12(s-1) + 5 j_i - tau_i, D_ij = (A_i + A_j - A_k)/2 for s = 3, delta = D - 12).
* [TP] section 3, s = 1, 2, 3 (J = 3): **correct**. Partitions of E = 11 into allowed parts: s = 1: {5,6} gives 6 + 5 only; s = 2: parts {4,5,6}, 6 + 5 only; s = 3: parts {3,...,6}: 6 + 5, 5 + 3 + 3, 4 + 4 + 3 (complete: two parts need 11 = 6 + 5; three parts from {3,...,6} summing to 11 are 3 + 3 + 5 and 3 + 4 + 4; four parts would sum to at least 12). Numbers re-done: s = 2: (PS) equality 5 j_1 - tau_1 = 5 j_2 - tau_2 with tau in {5, 0}; the pairing tau = 5 on the j = 1 vertex gives 0 versus 10, on the j = 2 vertex gives 5 versus 5, so D = 17, E_both = 0, s(pair) = 68 - c - 45 = 23 - c >= 19 > Ex = 5 + 20 - 10 = 15. s = 3 with 6 + 5: A = (24, 29, 29), D_12 = (24 + 29 - 29)/2 = 12, D_13 = 12, D_23 = (29 + 29 - 24)/2 = 17, E_both(2,3) = 0, s >= 19 > Ex(2) = 15. The 5 + 3 + 3 and 4 + 4 + 3 rows are right (lambda(q = 8) = 9, lambda(q = 9) = 10 against the budget 15 at j = 1). No error found.
* [TP] section 4, s = 1, 2 (J = 4): **correct** (all numbers re-done: s = 2, (6,4), j = (2,2): tau = (4,4), D = 12 + 10 - 4 = 18, E_both = 4, s(pair) = 72 - c - 45 - 4 = 23 - c >= 19 > 15. The text says the q = 9 vertex "contributes nothing to the nine triples"; that is true, and the 4 in E_both is what produces 23 - c, so the conclusion is right although the sentence suggests E_both = 0.)
* [TP] section 4, s = 3 (j = (2,1,1)): **correct in conclusion, but one stray bullet, one garbled bullet and one MISSING case.** (i) The first bullet "5 + 3 + 3" has sum 11, it belongs to J = 3 (E = 11) and is a stray copy; the partitions of E = 10 into parts in {3,...,6} are 6 + 4, 5 + 5, 4 + 3 + 3. (ii) **The partition 5 + 5 is announced in the list but never treated** (this is the one genuine gap in [TP] sections 3-5). It dies: two q = 10 vertices, tau_u = 5 (number beating u). Both beat vertex 1 (j = 2): tau = (10,0,0), A = 24 + 5j - tau = (24, 29, 29), D_12 + D_13 = 24 forces both 12, D_23 = (29 + 29 - 24)/2 = 17, E_both(2,3) = 0, s >= 19 > Ex(2) = 15. They beat vertices 1 and 2: tau = (5,5,0), A = (29, 24, 29), D_13 = (29 + 29 - 24)/2 = 17, E_both(1,3) = 0, s >= 19 > Ex(3) = 15. They beat 2 and 3: tau = (0,5,5), A = (34, 24, 24), D_23 = (24 + 24 - 34)/2 = 7 < 12. They both beat 2 (or both beat 3): tau_2 = 10 > 5 j_2 = 5, so rho_2 < 0. All dead (and Theorem 4.3 covers it anyway). (iii) The bullet "4 + 3 + 3 ... each q = 9 misses two" should read: one q = 9 (misses two of the three) and two q = 8 (each misses all three); then every vertex of V_+ has lambda >= 9 + 9 = 18, and the two missed by the q = 9 have lambda >= 28 > 25 >= Ex budget. 6 + 4: both sub-cases re-done (vertex 1 has j = 2, vertices 2, 3 have j = 1; the q = 9 vertex beats two of the three): if it beats the two j = 1 vertices 2, 3: A = (34, 25, 25), D_23 = (25 + 25 - 34)/2 = 8 < 12, impossible. q = 9 missing the j = 2 vertex 1 and the j = 1 vertex 2: tau = (4,4,0), A = (30, 25, 29), D_13 = (30 + 29 - 25)/2 = 17, E_both(1,3) = 0, s >= 19 > Ex(3) = 15. Both fine.
* [TP] section 4, s = 4: the table has the right nine partitions (checked in 5.2) and the right conclusion for every row, but **two rows are misstated**: (i) the 5 + 5 row says the untouched pair "has 11 dominators, so s < 0". The true count is 17 (5.2, case 5 + 5); the conclusion survives only through the other route s >= 19 > Ex = 15. (ii) The 6 + 4 row asserts "the untouched pair has 17 dominators" without the step that forces it (it is forced by s(1,2) >= 0 on the doubly beaten pair; see 5.2). Other rows are valid but use different (correct) reasons than my 5.2.
* [TP] section 5 (J = 5): s = 1: parts {5,6} cannot sum to 9, ok. s = 2: only 5 + 4; (PS): the q = 10 beats u_1, the q = 9 beats both; tau = (9, 4), 5 j_1 - 9 = 5 j_2 - 4 gives j_1 = j_2 + 1, so (3,2), delta = 6, D = 18, E_both = 4, s(pair) = 72 - c - 45 - 4 = 23 - c >= 19 > Ex(u_2) = 5 + 20 - 10 = 15 (and Ex(u_1) = 5 + 30 - 20 = 15). **Correct.** s = 3: 6 + 3: the q = 11 vertex beats nothing, the q = 8 beats all three, tau_i = 3, A_i = 21 + 5 j_i, D_12 = 23 - 5 j_3. The text says "(PS) produces a pair with 8 dominators": that is true only for the shape (3,1,1) (j_3 = 3 gives 8). **For the shape (2,2,1) the pair opposite the vertex with j = 1 has D = 18, E_both = 3, s(pair) = 72 - c - 45 - 3 = 24 - c >= 20, against Ex(j = 2 vertex) = 5 + 20 - 9 = 16.** So the conclusion holds but the text covers one shape. 3 + 3 + 3: lambda 27 at a j = 1 vertex: right. 5 + 4 (q = 10, q = 9): "every choice ... leads to one of ..." is not displayed in [TP]; it is subsumed by Theorem 4.3 and by the s = 3 case of its proof, which handles all of them with no case list.

**5.2 The complete case J = 4, s = 4.** (This is the only J < 5 case not yet excluded by Theorem 4.3.) Then V_+ = {1,2,3,4}, j = (1,1,1,1), E = 14 - 4 = 10, every heavy y has M_y inside V_+, so t_y <= 4 and e_y = 6 - t_y >= 2. For every u: **tau_u <= 5** (from rho_u = 5 j_u - tau_u >= 0, Proposition 4.2) and Ex(u) = 15 - sum over y beating u of lambda(q_y) >= 0, lambda = 10, 10, 9, 7 for t = 1, 2, 3, 4.

*All partitions of 10 into parts e in {2,...,6}:* h = 2: 6 + 4, 5 + 5. h = 3: 6 + 2 + 2, 5 + 3 + 2, 4 + 4 + 2, 4 + 3 + 3. h = 4: 4 + 2 + 2 + 2, 3 + 3 + 2 + 2. h = 5: 2 + 2 + 2 + 2 + 2. (No h = 1: 10 > 6. For h = 3: the largest part is 6, 5, 4 and the rest sums to 4 (2+2), 5 (3+2), 6 (4+2, 3+3) with parts >= 2, and largest part 3 would give at most 9. For h = 4: parts >= 2 sum 10 leaves 2 to distribute: 4+2+2+2 and 3+3+2+2. h = 5 forces all 2.) Nine partitions, those of the [TP] table.

*Step 1 (a global inequality).* sum over u of tau_u = sum over y in H of e_y t_y = sum e (6 - e) <= 4 * 5 = 20 (the t_y copies of e_y: each heavy y adds e_y to tau_u of each of the t_y vertices it beats). Values of e(6 - e): e = 6: 0; 5: 5; 4: 8; 3: 9; 2: 8. So:
 5 + 3 + 2: 5 + 9 + 8 = 22 > 20. 4 + 4 + 2: 8 + 8 + 8 = 24 > 20. 4 + 3 + 3: 8 + 9 + 9 = 26 > 20. 4 + 2 + 2 + 2: 8 + 24 = 32 > 20. 3 + 3 + 2 + 2: 9 + 9 + 8 + 8 = 34 > 20. 2 x 5: 40 > 20. **These six are impossible** (this is the lead's inequality, section 7; [TP] used instead lambda-sums, also valid).
 Remaining: 6 + 4 (sum 8), 5 + 5 (sum 10), 6 + 2 + 2 (sum 16).

*Case 6 + 2 + 2.* One y_0 with q = 11, two y_1, y_2 with q = 7 (t = 4), so M = V_+ for both. tau_u = 2 + 2 = 4 for every u, rho_u = 1, sum of delta over the 6 pairs = (4 * 1)/2 = 2. Hence at least four pairs have delta = 0 (D = 12). For every pair E_both = 2 + 2 = 4. For a pair with delta = 0: s = 4 * 0 + 3 - c - 4 = -1 - c < 0, contradicting s >= 0. Impossible.

*Case 5 + 5.* Two y's with q = 10, each beats exactly one vertex of V_+. If both beat the same u then tau_u = 10 > 5, so they beat distinct u_1, u_2: tau = (5, 5, 0, 0), rho = (0, 0, 5, 5). As delta >= 0, rho_{u_1} = 0 gives delta_{u_1 v} = 0 for all v; same for u_2; the remaining pair {u_3, u_4} then carries rho_{u_3} = delta_{u_3 u_4} = 5. So D_{34} = 17 (not 11 as in [TP]). No heavy y beats u_3 or u_4, E_both = 0, s(u_3, u_4) = 68 - c - 45 = 23 - c >= 19 while Ex(u_3) = 15 - 0 = 15 (nothing heavy beats u_3). Contradiction with (B).

*Case 6 + 4.* One y_0 with q = 11, one y_1 with q = 9 beating two vertices, say 1, 2. tau = (4, 4, 0, 0), rho = (1, 1, 5, 5). The doubly beaten pair {1, 2} has E_both = 4, so s(1,2) = 4 delta_12 + 3 - c - 4 = 4 delta_12 - 1 - c >= 0 forces delta_12 >= 1 (since 1 + c >= 1). With rho_1 = rho_2 = 1 this makes delta_12 = 1 and delta_{1v} = delta_{2v} = 0 for v = 3, 4. Then rho_3 = delta_34 = 5, D_34 = 17, E_both(3,4) = 0 and s(3,4) = 68 - c - 45 = 23 - c >= 19 > Ex(3) = 15 (nothing heavy beats 3). Contradiction.

All nine partitions fail. **So J = 4 is impossible, and (with Theorem 4.3 and s <= J) J >= 5.** This proves part 2 of the [TP] Theorem (J >= 5 and at least four dominators of in-degree > 25) in full, with Theorem 4.3 and 5.2 and no use of Theorem 1 of [52]. Status: proved_by_hand.

## 6. Audit of [TP] section 7 (balanced degrees) and of Lemma B (no in-degree 23)

**6.1 [TP] section 7: correct, numbers re-derived.**
* Degrees. If every in-degree is 25 or 26 and a vertices have 26: 25*52 + a = 1326 gives a = 26. So 26 vertices of each kind. d^+ = 51 - d^-: 26 vertices with d^+ = 26 (in-degree 25) and 26 with d^+ = 25.
* Identity. A triple Y is counted by a pair {w, w'} of its dominators iff Y lies in N^+(w) inter N^+(w'); so sum_Y C(k(Y), 2) = sum over unordered pairs {w,w'} of C(a_{ww'}, 3) with a_{ww'} = |N^+(w) inter N^+(w')|.
* a_{ww'} = D_{ww'} + 51 - d^-(w) - d^-(w'). Proof: say w -> w'. Of the 50 other vertices let D beat both, x beat w only, y' beat w' only, a beat neither (these are the common out-neighbours). d^-(w) = D + x (w' is beaten by w), d^-(w') = D + y' + 1. So a = 50 - D - x - y' = 50 - D - (d^-(w) - D) - (d^-(w') - 1 - D) = 51 - d^-(w) - d^-(w') + D. OK.
* Sum of a. Sum over pairs of (51 - d^-(w) - d^-(w')) = 51*1326 - 51 * sum d^- = 0, since each vertex is in 51 pairs and sum d^- = 1326. And sum over pairs of D_{ww'} = number of (vertex z, pair of its out-neighbours) = sum_z C(d^+(z), 2) = 26*C(26,2) + 26*C(25,2) = 26*325 + 26*300 = 8450 + 7800 = 16250 (this agrees with 16237 + (sum e^2)/2 = 16237 + 13 in the brief). So sum_pairs a = 16250.
* Minimum of sum C(a,3). C(a+1,3) - C(a,3) = C(a,2) is nondecreasing in a >= 0, so C(a,3) is convex on integers, and for a fixed sum over 1326 integers the sum of C(a,3) is minimal when all a are in {12, 13}. 16250 - 12*1326 = 16250 - 15912 = 338 pairs have 13, 988 have 12. C(13,3) = 286, C(12,3) = 220: 338*286 = 96668, 988*220 = 217360, total **314028**. OK.
* Upper bound if all k in {5,6}. sum_Y k = sum_w C(d^+(w), 3) = 26*C(26,3) + 26*C(25,3) = 26*2600 + 26*2300 = 67600 + 59800 = 127400. With 22100 triples, 5*22100 = 110500, so exactly 127400 - 110500 = 16900 triples would have k = 6 and 5200 would have k = 5; sum C(k,2) = 5200*10 + 16900*15 = 52000 + 253500 = **305500** (it would be equal, not just at most). 314028 > 305500, so some triple has k >= 7. OK.
* **Sharper form (new).** With u_Y := k(Y) - 5 >= 0: C(5 + u, 2) = 10 + 5u + C(u, 2). Hence sum_Y C(k,2) = 22100*10 + 5*(127400 - 110500) + sum_Y C(u_Y, 2) = 221000 + 84500 + sum C(u_Y, 2) = 305500 + sum_Y C(u_Y, 2). So in the balanced case **sum_Y C(k(Y) - 5, 2) >= 314028 - 305500 = 8528.** In particular at least 8528 / C(u_max, 2) triples have k >= 7; if k <= 7 throughout then at least 8528 triples have exactly 7 dominators (that is 38.6% of all triples).
Verdict: [TP] section 7 **OK**; also consistent with the remark in BRIEF section 3.

**6.2 Lemma B (no in-degree 23): correct, every step re-derived.** Suppose d^-(v) = 23, A = N^-(v) (23 vertices), B = N^+(v) (28 vertices).
1. For a in A, D({a,v}) = N^-(a) inter A (a vertex beating v lies in A), so |D({a,v})| = d^-_A(a) >= 11 by (F2). The sum over A of d^-_A(a) is C(23,2) = 253 = 23*11, so all equal 11: T[A] is a regular tournament with degrees 11, every {a,v} is tight with R_a := N^-_A(a), and (Lemma T) every vertex of A is a dominator of some tight pair (x in R_a for the 11 vertices a that x beats in A), so e(x) >= 0 on A. OK.
2. For a, a' in A: D({v,a,a'}) = common in-neighbours of a, a' inside A. Summing over the C(23,2) = 253 pairs: sum_{x in A} C(d^+_A(x), 2) = 23*C(11,2) = 23*55 = 1265 = 5*253. Each term is >= 5 (F1), so each equals 5. OK.
3. If a -> a', the 21 other vertices of A split: a has in-degree 11 and a' is not an in-neighbour, so 11 in-neighbours of a among the 21, 5 of them also beat a' and 6 do not; a' has in-degree 11, one of which is a, so 10 in-neighbours of a' among the 21, 5 also beat a, 5 do not. The rest: 21 - 5 - 6 - 5 = 5 are common out-neighbours. So T[A] is a doubly regular tournament DRT(23) and the R_a are the blocks of a symmetric 2-(23,11,5) design (a, a' lie together in R_x iff x is a common out-neighbour: 5). OK.
4. a in A beats v and 11 vertices of A, so it beats 26 - e(a) - 12 = 14 - e(a) vertices of B. Each b in B has |D({v,b})| >= 11 and D({v,b}) is inside A, so at least 11 vertices of A beat b. Hence sum_A (14 - e) >= 28*11 = 308, i.e. 322 - sum_A e >= 308, sum_A e <= 14, and since e >= 0 on A at least 23 - 14 = 9 vertices of A have e = 0. OK.
5. For the tight pair {a,v}: b in B has Q_b = R_a inter N^-(b) = R_a inter A_b where A_b := A inter N^-(b). Exactly one b can have q_b = 11 (excess 6) because the total excess is 14 - J <= 11 (J >= 3, Theorem 1'; indeed even <= 10 by section 5 above). OK.
6. Fix r in A_0 (e(r) = 0) and b in B with b -> r. For each of the 11 vertices a that r beats in A, r is in R_a, j_r = 0, and b beats r, so Lemma A (i) (b is a 5-vertex) gives |R_a inter A_b| = 5. Count: sum over a in N^+_A(r) of |R_a inter A_b| = sum_{x in A_b} |N^+_A(r) inter N^+_A(x)| = 5|A_b| (r is not in A_b because b -> r, and any two distinct vertices of the DRT(23) have 5 common out-neighbours). So 55 = 5|A_b|, |A_b| = 11. OK.
7. z_a := |A_b inter R_a| >= 5 for all 23 a (q_b >= 5), sum_a z_a = sum_{x in A_b} d^+_A(x) = 11*11 = 121, sum_a z_a^2 = sum over ordered pairs (x,x') of A_b of #{a : x, x' in R_a} = 11*11 + 11*10*5 = 121 + 550 = 671. With x_a = z_a - 5 >= 0: sum x_a = 121 - 115 = 6 and sum x_a^2 = 671 - 10*121 + 25*23 = 671 - 1210 + 575 = 36 = (sum x_a)^2. So all cross terms x_a x_a' vanish: exactly one a = a_b has x = 6, z = 11, A_b = R_{a_b}. OK.
8. r is not in A_b = R_{a_b}, so r does not beat a_b: a_b is in {r} union N^-_A(r), a set of 1 + 11 = 12 vertices. r has d^-(r) = 25, with 11 in-neighbours in A, none is v (r -> v), so 14 in B. Each such b gives a_b in the 12-set; two different b, b' cannot have the same a_b since then both would have q = 11 for the pair {a_b, v} (item 5). 14 distinct elements in a 12-set: contradiction. OK.
Verdict: **Lemma B correct** (also [A52] Lemma 1). The only external inputs: (F1), (F2), Lemma T, Lemma A (valid for any tight pair at N = 52, regardless of the degrees of the two vertices of the pair), and J >= 3 (only through the weak bound excess <= 11 < 12).

## 7. The lead's inequality tau_i <= 5 j_i (BRIEF section 8): verified, with consequences

**7.1 Statement and proof.** For a tight pair at N = 52 and every u in V_+: sum over v in V_+ minus {u} of D_uv = 12(s-1) + 5 j_u - tau_u, hence **tau_u <= 5 j_u**, with equality iff D_uv = 12 for all v in V_+ minus {u}.
*Proof.* (PS) gives sum over the ten v of D_uv = 120 + 5 j_u - tau_u. For the 11 - s vertices v of V_0, D_uv = 12 by Lemma A (applied at v). So the s - 1 others sum to 120 + 5 j_u - tau_u - 12(11 - s) = 12(s-1) + 5 j_u - tau_u [120 - 132 + 12 s = 12 s - 12 ok]. Each D_uv >= 12 (section 2 (b)), so the sum is >= 12(s-1), i.e. 5 j_u - tau_u >= 0. QED. This is the lead's formula and inequality, exactly. (It is Proposition 4.2(a): rho_u = 5 j_u - tau_u = 5 nu_u + Phi_u >= 0.)

**7.2 Consequences (all proved).**
(a) Summing over V_+: sum over heavy y of e_y t_y <= 5J, i.e. sum over H of t_y (6 - t_y) <= 5J, which is the lead's second statement. The slack is exact: **5J - sum_H e_y t_y = 2 * sum over pairs {u,v} in V_+ of delta_uv.** (Each heavy y adds e_y to tau_u for the t_y vertices it beats, all in V_+; and sum_u rho_u counts each pair twice.)
(b) With sum_H e = 14 - J: sum_H e(6 - e) <= 5(14 - sum_H e), i.e. **sum_{y in H} e_y (11 - e_y) <= 70**, equivalently sum e^2 >= 11E - 70 with E = 14 - J. For E <= 7 (J >= 7) this is empty (sum e^2 >= sum e = E >= ... in fact 11E - 70 <= E iff E <= 7). It bites only for J = 5 (E = 9: sum e^2 >= 29) and J = 6 (E = 8: sum e^2 >= 18). So the lead's inequality cannot by itself exclude J >= 7.
(c) **Equality/slack lemma (new).** If delta_uv = 0 then s(u,v) = 3 - c - E_both >= 0, so E_both(u,v) + c(u,v) <= 3. More generally 4 delta_uv >= E_both(u,v) + c(u,v) - 3, so delta_uv >= ceil((E_both(u,v) - 3)/4) and **any pair jointly beaten by heavy vertices of total excess >= 4 has delta >= 1** (E_both >= 8 gives delta >= 2, and so on). Therefore the number of such pairs is at most sum of delta = (5J - sum_H e t)/2.
(d) **Global inequality (G) (new).** Summing 4 delta_uv >= E_both + c - 3 over the C(s,2) pairs of V_+ (sum of E_both over pairs = sum_H e_y C(t_y, 2)) and using 4 sum delta = 2(5J - sum e t), with J = 14 - sum e:
   **sum over y in H of w(t_y) + C_+ <= 140 + 3 C(s,2),**  where C_+ = sum over pairs in V_+ of c(u,v) >= 0 and w(t) = e (10 + t(t+3)/2) with e = 6 - t, i.e.
   w(0) = 6*10 = 60, w(1) = 5*12 = 60, w(2) = 4*15 = 60, w(3) = 3*19 = 57, w(4) = 2*24 = 48, w(5) = 1*30 = 30.
   (Derivation: 10J + 3C(s,2) >= sum e t [2 + (t-1)/2] + C_+ = sum e t (t+3)/2 + C_+; substitute 10J = 140 - 10 sum e.) For s = 4: bound 158; s = 5: 170; s = 6: 185; s = 11: 305. E.g. at most two heavy vertices with t <= 2 when s <= 5.
(e) **nu bounds (new).** From Ex(u) = 5 + 10 nu_u + g_u >= 0: nu_u >= -floor((5 + g_u)/10). So nu_u >= 0 unless u is beaten by heavy vertices of total g_u = (#t=3) + 3(#t=4) + 6(#t=5) >= 5. Together with 4.1 (sum nu = 14 - 6h): **either every nu_u >= 0 and h <= 2, or some u is "deep" (nu_u <= -1, g_u >= 5).** For s = 4 the pair-lower-bound sum gives the stronger nu_u >= -floor((9 + 2 g_u)/20) (derived by summing 4 delta_uv >= E_both + c - 3 over v in V_+ minus {u}, giving 20 nu_u >= -2 g_u - 3(s-1)); deep needs g_u >= 6 when s = 4.
(f) For u in V_+ with nu_u = 0 and g_u = 0 ("net-zero"), Corollary A' of section 3 holds: s(u,v) = 3 - c(u,v), c <= 3, and delta_uv = #{heavy y with M_y inside ... containing u, v and t = 2} (the number of q = 9 vertices beating both). This agrees with Proposition 4.2(a): rho_u = Phi_u = number of t = 2 vertices beating u.

**7.3 Verdict on tau_i <= 5 j_i:** correct, proved_by_hand. It is the entire content of "D >= 12 inside R" summed. It is weak for J >= 7.

## 8. What a surviving tight pair must look like (input for the lane that tries to kill tight pairs)

All statements in 8.1 are proved in sections 2-7 above (N = 52, F1 only). A "tight pair" below means a pair P with |D(P)| = 11 in an F1-tournament on 52 vertices.

**8.1 Theorem S (necessary structure).** Let P be a tight pair, R = D(P), O = V minus (P union R), and use the notation of section 4.0. Then:
1. **Order data.** |O| = 39; for r in R: d^-(r) = 25 + j_r, r beats exactly 19 - j_r vertices of O, and exactly 20 + j_r vertices of O beat r. J = sum j_r <= 14 and **J >= 5**; sum over y in O of (q_y - 5) = 14 - J.
2. **Positive vertices.** s = |V_+| satisfies **4 <= s <= min(J, 11)**. (J = 4 forces s = 4 and is excluded in 5.2; s <= 3 is excluded by Theorem 4.3.)
3. **Heavy vertices.** The heavy outside vertices H (q_y >= 6; h = |H|) beat only vertices of V_+; each has t_y = 11 - q_y <= s, e_y = 6 - t_y; the other 39 - h outside vertices have q = 5 (they beat 6 vertices of R, possibly in V_0). sum_H e_y = 14 - J, i.e. sum_H t_y = 6h - 14 + J.
4. **V_0 vertices** (in-degree 25): for u in V_0 and every v in R minus {u}: D_uv = 12, c(u,v) <= 3, s(u,v) = 3 - c(u,v), sum_v c(u,v) = 20, Ex(u) = 5.
5. **Pairs inside V_+.** D_uv = 12 + delta_uv with delta_uv >= 0; sum over v in V_+ minus {u} of delta_uv = rho_u = 5 j_u - tau_u = 5 nu_u + Phi_u >= 0 (Prop 4.2); for each pair 0 <= 4 delta_uv + 3 - c(u,v) - E_both(u,v) <= min(Ex(u), Ex(v)), where Ex(u) = 5 + 10 nu_u + g_u.
6. **Global.** sum_{u in V_+} nu_u = 14 - 6h (4.1); sum_H e_y(11 - e_y) <= 70; (G) of 7.2(d); the slack identity 5J - sum_H e t = 2 sum_pairs delta.
7. **Branches.** Either (I) nu_u >= 0 for all u in V_+, and then h <= 2, with sum nu = 14 (h = 0), 8 (h = 1) or 2 (h = 2); or (II) some u has nu_u <= -1, which needs g_u = (#t=3) + 3(#t=4) + 6(#t=5) among the heavy vertices beating u to be >= 5 (>= 6 if s = 4).
   In branch I: h = 0 means J = 14 and all 39 outside vertices are 5-vertices; h = 1 means J = 8 + t_y; h = 2 means J = 2 + t_1 + t_2.

**8.2 The boundary J = 5 completely (excess E = 9; s in {4, 5}).** Tools: K1 = [sum e t <= 25 and tau_u <= 5], K2 = slack lemma 7.2(c)/(d), K3 = Ex(u) >= 0 with nu_u = j_u - m_u, K4 = solve the rho-system for delta and test pairs. Writing parts as e (so t = 6 - e).

*s = 4, j = (2,1,1,1)* (parts e >= 2 since t <= 4; partitions of E = 9 into parts in {2,...,6}: exactly six): 6+3, 5+4, 5+2+2, 4+3+2, 3+3+3, 3+2+2+2.
| partition | sum e t | verdict |
|---|---|---|
| 3+3+3 | 27 > 25 | dead (K1) |
| 3+2+2+2 | 33 > 25 | dead (K1) |
| 4+3+2 | 25 (slack 0, all delta = 0) | dead: all pairs need E_both + c <= 3, but a pair inside the t = 3 set also lies in the t = 4 set (which is all of V_+), E_both >= 3 + 2 = 5 |
| 5+2+2 | 21 (sum delta = 2) | dead: both t = 4 vertices beat all of V_+, so every one of the 6 pairs has E_both >= 4, delta >= 1, sum delta >= 6 > 2 |
| 5+4 | 13 | dead: y_1 (t=1) beats x, y_2 (t=2) beats {p,q}; if x in {p,q} then Ex(x) = 5 + 10(j_x - 2) >= 0 forces j_x = 2, rho = (1,1,5,5) on (p,q,r_1,r_2), delta_pq >= 1 exhausts rho_p, rho_q, so delta_{r1 r2} = 5; if x not in {p,q} and j_r = 2 then rho = (1,1,0,10) impossible, j_x = 2 gives rho = (1,1,5,5) and delta_{x r} = 5, j_p = 2 gives rho = (6,1,0,5), delta_{pr} = 5. Every time a pair (r_1, r_2 / x, r / p, r) with no heavy vertex beating either end has D = 17, E_both = 0, s(pair) = 68 - c - 45 = 23 - c >= 19 > Ex = 15 at an end with nu = 1 |
| **6+3** | 9 | **not excluded**: y_0 (q = 11) and y_1 (q = 8, beats three vertices a, b, c, not d). j_d = 2 is dead (rho_d = 10 > rho_a + rho_b + rho_c = 6); j_a = 2: nu = (1,0,0,1), g = (1,1,1,0), Ex = (16, 6, 6, 15), rho = (7,2,2,5), and the system forces delta_ad = 4 (with c(a,d) = 4), delta_bc = 0 (c(b,c) = 0), {delta_bd, delta_cd} = {1, 0}, e.g. delta_bd = 1, delta_ab = 1, delta_ac = 2 (c(a,c) >= 2, c(b,d) >= 1) |

*s = 5, j = (1,1,1,1,1)*: all ten partitions with sum e^2 >= 29 (K1); the other 16 partitions of 9 (4+3+1+1, 4+2+2+1, 4+2+1^3, 4+1^5, 3+3+3, 3+3+2+1, 3+3+1^3, 3+2+2+2, 3+2+2+1+1, 3+2+1^4, 3+1^6, 2^4+1, 2^3+1^3, 2^2+1^5, 2+1^7, 1^9, with sum e^2 = 27, 25, 23, 21, 27, 23, 21, 21, 19, 17, 15, 17, 15, 13, 11, 9) are dead by K1.
| partition | sum e t | verdict |
|---|---|---|
| 5+1+1+1+1 | 25, slack 0 | dead: the four t = 5 vertices beat all of V_+, E_both >= 4 on every pair but delta = 0 needs E_both <= 3 |
| 4+3+2 | 25, slack 0 | dead: the t = 3 and t = 4 vertices beat sets of size 3 and 4 in a 5-set, which meet in >= 2 vertices; a pair there has E_both >= 3 + 2 = 5 > 3 |
| 5+2+1+1 | 23 (sum delta = 1) | dead: the t = 4 vertex beats a 4-set; each of its 6 pairs has E_both >= 2+1+1 = 4, delta >= 1 |
| 5+2+2 | 21 (sum delta = 2) | dead: two 4-sets in a 5-set share >= 3 vertices, >= 3 pairs with E_both >= 4, sum delta >= 3 |
| 4+4+1 | 21 | dead: y_a, y_b (t = 2, e = 4) and y_c (t = 5, e = 1). Same pair beaten by both, or two beaten pairs sharing a vertex u: m_u = 3, nu_u = -2, Ex(u) = 5 - 20 + g_u, g_u = 6 (only the t=5 vertex) < 15, dead. Disjoint pairs {1,2}, {3,4}: nu = (-1,-1,-1,-1,0), Phi_1 = (2-1) + (5-1) = 5, rho_1 = -5 + 5 = 0, but delta_12 >= ceil((4+1-3)/4) = 1, contradiction |
| 5+3+1 | 19 | dead: y_1 (t=1, beats x), y_2 (t=3, set M_2), y_3 (t=5, all). If x in M_2: m_x = 3, nu_x = -2, Ex(x) = 5 - 20 + g_x, g_x = C(2,2) + C(4,2) = 7: negative. If x not in M_2: tau_x = 5 + 1 = 6 > 5 = 5 j_x |
| 5+4 | 13 | dead: x in {p,q} gives m_x = 2, Ex(x) = 5 - 10 < 0; x outside gives rho = (1,1,0,5,5) on (p,q,x,r_1,r_2), delta_pq = 1, delta_{r1r2} = 5, D = 17, s >= 19 > Ex(r_1) = 15 |
| **6+3** | 9 (slack 16, sum delta = 8) | **not excluded**: y_0 (q = 11) and y_1 (q = 8, beats {1,2,3}); nu = (0,0,0,1,1), Ex = (6,6,6,15,15), rho = (2,2,2,5,5); a solution of the delta-system: delta_45 = 2, delta_{i4} = delta_{i5} = 1 (i = 1,2,3), delta_ij = 0 inside {1,2,3} (needs c(i,j) = 0 inside, c(i,4), c(i,5) >= 1) |
| **6+2+1** | 13 (sum delta = 6) | **not excluded**: y_0 (q = 11), y_a (e = 2, q = 7, t = 4, beats {1,2,3,4}), y_b (e = 1, q = 6, t = 5, beats all); nu = (-1,-1,-1,-1,0), Ex = (4,4,4,4,11), rho = (2,2,2,2,4); forced: delta_{i5} = 1 (c(i,5) >= 2) for i <= 4, and a perfect matching of delta = 1 inside {1,2,3,4}, the other four inside pairs have delta = 0 and c = 0 |
| **6+1+1+1** | 15 (sum delta = 5) | **not excluded**: y_0 and three q = 6 vertices each beating all of V_+; nu = (-2,...,-2), Ex = 3 each, rho = 2 each, E_both = 3 on every pair; forced: delta in {0,1}, the delta = 1 pairs form a 5-cycle (c >= 1 there), the five delta = 0 pairs have c = 0 |

So for J = 5 exactly four configurations survive these counting tools: (s=4) 6+3 with j = 2 on a vertex beaten by the q = 8 vertex; (s=5) 6+3, 6+2+1, 6+1+1+1. In all four there is a vertex with q = 11 (excess 6): no survivor has its 6 absent. Status: the eliminations are proved_by_hand; the four survivors are only "not excluded by counting" (I exhibit a delta-assignment but make no claim about T[R]).

**8.3 What cannot be excluded by these tools.** For J >= 7 the lead's inequality is empty, and branch I with h = 0 (J = 14, every outside vertex a 5-vertex, nu_u = j_u, rho_u = 5 j_u, Ex(u) = 5 + 10 j_u) gives pair constraints 0 <= 4 delta + 3 - c <= 5 + 10 min(j_u, j_v) that are satisfiable (for instance s = 11, j = (2,2,2,1,...,1): rho_u = 10 or 5, bound delta <= (2 + 10 j + c)/4 >= 4 allows). So **counting inside R and O at this level cannot kill all tight pairs**. The remaining information is the internal structure of the 5-regular tournament T[R] (the numbers c(u,v)) and the 5-vertices' behaviour (which vertices of R each 5-vertex beats: it beats 6, and for u in V_0 exactly 20 of them beat u). Recorded demands on c from the survivors: c = 0 on prescribed pairs, c = 4 on a pair, c >= 2 on others; globally sum over pairs of c = 110, sum_v c(u,v) = 20 for every u, c(u,v) <= 4, <= 3 if u or v in V_0.

## 9. Remaining audit items, interpretation of the invariant, dead ends, hand checks

**9.1 Meaning of nu_u (new remark).** Let f_u be the number of 5-vertices of O that beat u (u in R). By (I1) exactly 20 + j_u vertices of O beat u; of these m_u are heavy, so **f_u = 20 + j_u - m_u = 20 + nu_u for u in V_+, and f_u = 20 for u in V_0.** Each 5-vertex beats exactly 6 vertices of R and there are 39 - h of them, so sum_{u in R} f_u = 6(39 - h) = 234 - 6h, i.e. sum_u (f_u - 20) = 234 - 6h - 220 = 14 - 6h. So Proposition 4.1 is the double count of the incidences between the 39 - h five-vertices and R; "nu_u = surplus of five-vertex losses at u". This also explains why nothing else is needed: Lemma A says V_0 vertices have no surplus. In this language Ex(u) = 5 + 10 (f_u - 20) + g_u, and the s <= 3 proof shows that the surpluses are forced to be equal and then 3 | 14 fails.

**9.2 [TP] section 9 (the old proof of Lemma C).** Superseded by Theorem 4.3. Spot checks (recomputed with A_i = 24 + 5 j_i - tau_i, D_YZ = (A_Y + A_Z - A_X)/2): s = 1 and s = 2 table: correct except that E = 0 (no heavy vertex, J = 14) is silently omitted in s = 1 ("no other E is a sum of such parts"): for s = 1, E = 0 gives (PS) 120 = 120 + 5*14 - 0, false, so the case is dead. s = 3 bullets: E = 8 same pair: opposite pair 14, (3,2) splits give 17 with E_both = 0 vs Ex(Z) = 15, (4,1) gives D_23 = 7; OK. E = 8 different pairs: j_X = 2: D_YZ = 17 for every split of the remaining 4, E_both = 0, min(Ex(Y), Ex(Z)) <= 15; j_X = 3: D_YZ = 12, D_XZ = 18, E_both = 4, 23 - c vs 15; j_X = 4: D_YZ = 7: OK. E = 8 (5, 3): j_X = 2 gives D = 18, s >= 20, min Ex <= 16; j_X = 3 gives D = 13, D_XZ = 18, s >= 20 vs 16; j_X = 4 gives D_YZ = 8: OK (j_X = 4 is not mentioned in [TP]). E = 6 single excess 6: D_opposite = 32 - 5 j_X, so j_X <= 4 and compositions (4,3,1), (4,2,2), (3,3,2): OK as in [TP]. E = 6 two excess-3 vertices: OK (computed above: (3,3,2) gives D = 19, s >= 25 - c >= 21 vs Ex(j = 3) = 17). E = 3: D = 38 - 5 j_X = 33, 28, 23, s >= 4D - 52 = 80, 60, 40: OK. I found no error; the gaps are (a) E = 0, (b) j_X = 4 sub-splits unstated, (c) the 5 + 3 table entries phrased as "endpoints share degree excess 4" without displaying min Ex. None changes a conclusion. I did not re-verify every sub-bullet (E = 7, E = 5, E = 4 bullets), since Theorem 4.3 replaces them.

**9.3 Dead ends recorded.**
* Extending the nu-method to s = 4: the rho-system has 4 equations in 6 unknowns delta_uv; only sum delta and the three "matching differences" delta_12 - delta_34 etc. are determined. Summing the lower and upper pair bounds over v only gives nu_u >= -(5 + g_u)/10 (from Ex >= 0) and nu_u >= -(9 + 2 g_u)/20 (s = 4); no parity obstruction appears (14 - 6h is not constrained mod anything once four or more nu's are free). Survivors exist (8.2).
* The tau-sum inequality (7.2(b)) is vacuous for J >= 7; the inequality (G) is vacuous for small h.
* [TP]-style per-J case lists do not scale (J = 5 alone has 16 + 10 partitions for s = 5); the invariant plus slack-lemma method of 5.2 and 8.2 is the economical replacement.
* Lemma-A analogues for vertices with j = 1: only the "net-zero" vertices (nu_u = 0, g_u = 0) behave like V_0 (D_uv = 12 + n_uv, Corollary A'); a general j = 1 vertex is not controlled.

**9.4 Hand checks of the numbers (second pass).**
1. 14 = 2*6 + 2, so 14 - 6h is 2 mod 6 for every integer h, in particular never 0; 14 = 3*4 + 2, so never divisible by 3. Hence 4.1 contradicts s = 0, 1 (value 0) and s = 3 (value 3x).
2. s = 2: 20x + 3 - c >= 0 gives 20 x >= c - 3 >= -3 (as c >= 0); x integer so x >= 0 (x = -1 would need c - 3 <= -20, impossible). And 10x <= 2 + c <= 6 (as c <= 4); x integer so x <= 0 (x = 1 would need c >= 8, impossible). Good.
3. s = 3: s(1,2) = 10(x_1 + x_2 - x_3) + n + 3 - c_12 and Ex(1) = 5 + 10 x_1 + n; difference Ex(1) - s(1,2) = 2 + c_12 - 10 (x_2 - x_3) >= 0 gives 10(x_2 - x_3) <= 2 + c_12 <= 6. OK. Check by example: x = (0,0,0), n = 0: s(1,2) = 3 - c, Ex = 5, fine (this is the net-zero situation, delta = n_12 = 0, D = 12).
4. delta_12 for s = 3: rho_1 + rho_2 - rho_3 = 5(x_1 + x_2 - x_3) + (n_12 + n_13 + 2n) + (n_12 + n_23 + 2n) - (n_13 + n_23 + 2n) = 5(...) + 2 n_12 + 2n. Half of it: (5/2)(...) + n_12 + n. The half-integrality is fine because rho_1 + rho_2 - rho_3 = 2 delta_12 is even automatically.
5. J = 4 case: e(6 - e) for e = 6, 5, 4, 3, 2, 1 is 6*0 = 0, 5*1 = 5, 4*2 = 8, 3*3 = 9, 2*4 = 8, 1*5 = 5. Totals: 6+4: 0 + 8 = 8. 5+5: 10. 6+2+2: 16. 5+3+2: 5 + 9 + 8 = 22. 4+4+2: 24. 4+3+3: 8 + 9 + 9 = 26. 4+2+2+2: 8 + 24 = 32. 3+3+2+2: 18 + 16 = 34. 2*5: 40. Threshold 5J = 20. OK.
6. J = 5, s = 5 partitions with sum e^2 >= 29: 6+3: 36+9 = 45; 6+2+1: 36+4+1 = 41; 6+1+1+1: 39; 5+4: 41; 5+3+1: 35; 5+2+2: 33; 5+2+1+1: 25+4+2 = 31; 5+1^4: 29; 4+4+1: 33; 4+3+2: 16+9+4 = 29. Condition: sum e^2 >= 11*9 - 70 = 29. OK.
7. (G) weights: w(t) = e (10 + t(t+3)/2): t = 0: 6*10 = 60; t = 1: 5*(10 + 2) = 60; t = 2: 4*(10 + 5) = 60; t = 3: 3*(10 + 9) = 57; t = 4: 2*(10 + 14) = 48; t = 5: 1*(10 + 20) = 30. RHS 140 + 3 C(s,2): s = 4: 140 + 18 = 158; s = 5: 140 + 30 = 170. (Used only as a screen; every elimination in 8.2 was also done directly.)
8. 6.1: 338*286: 300*286 = 85800, 38*286 = 10868, total 96668. 988*220 = 217360. Sum 314028. 26*325 = 8450, 26*300 = 7800, sum 16250. 26*2600 = 67600, 26*2300 = 59800, sum 127400. 5*22100 = 110500; 127400 - 110500 = 16900; 5200*10 = 52000; 16900*15 = 253500; sum 305500; 314028 - 305500 = 8528. OK.
9. 6.2: 23*55 = 1265 (20*55 = 1100, 3*55 = 165). 5*253 = 1265. 11*11 + 11*10*5 = 121 + 550 = 671; 671 - 1210 + 575 = 36.

**9.5 Suggested next steps for the swarm.**
* To kill a tight pair one must use the internal structure of T[R] (the pair numbers c(u,v), with sum 110 over the 55 pairs, sum_v c(u,v) = 20, c <= 4), or the individual neighbourhoods of the 5-vertices (each beats exactly 6 vertices of R; f_u = 20 + nu_u of them beat u), because counting at the level of (E), (PS), (S), (B) leaves at least the four J = 5 configurations of 8.2 and the whole branch h = 0, J = 14.
* In the survivors the c-demands are sharp (c = 4 on a pair; c = 0 on prescribed pairs of V_+; c >= 2 on others). A lane could try to realise or refute these inside a 5-regular tournament on 11 vertices.
* A cheaper target: extend 8.2 to J = 6 (E = 8) with the same method (s in {4,5,6}); the lead's inequality still has bite there (sum e^2 >= 18).

<!-- END -->
