# R2-AUDIT: Independent hostile audit of round-1 claims

Lane: R2-AUDIT (round 2 of the Erdos #902 swarm, goal f(4) >= 53).
Target: check round-1 claims by hand, line by line. Do not trust the lane's arithmetic.
Each item gets VERIFIED, FLAWED (with error and correct statement), or UNCHECKED (with reason).

## Status

- COMPLETE. All six items were checked by hand. Each derivation was re-done, not trusted.
- Verdicts: item 1 VERIFIED; item 2 VERIFIED with 2 FLAWED sub-claims (N^- >= 9 and S2 >= 346) and 1 typo; item 3 VERIFIED with 1 FLAWED inference (Lemma 6.4 last paragraph); item 4 VERIFIED; item 5 VERIFIED; item 6 VERIFIED conditional on upstream section 2 of r1_AUDIT-52-B.
- None of this proves f(4) >= 53. The audit only certifies which round-1 statements round 2 can use.

## Verdict table

| # | Item | Verdict | One-line reason | Safe consequence for round 2 | Withdraw / correct |
|---|---|---|---|---|---|
| 1 | r1_DUAL s.6 Thm NT-B01 (no tournament on 52 vertices with all in-degrees in {25,26} and all lambda in {12,13}) | VERIFIED | Steps 0-7 re-derived: V2 forces lambda=12 on V_0 in-pairs; V2' gives excess f(v); cyclic count c_0+c_3 = 1300; sum C(f,2) identity gives S = 338; but S <= 13*14 = 182. | An F1 tournament on 52 vertices with all in-degrees in {25,26} has a pair with lambda = 11 (tight) or lambda >= 14. | none |
| 2a | r1_MOM-BALANCED s.2 Lemma 2.1 (in-nbhds) | VERIFIED | v in G: 300 = 25*12 forces x=0 on in-pairs; v in H: 325 = 26*12+13. | Under H1+H2: sum over in-nbrs of x is 0 (G) or 13 (H). | none |
| 2b | Lemma 2.2 (out-nbhds) | VERIFIED | Common out-degree m = 51 - d- - d- + lambda re-derived; gives g+ + X+ = 13 (G) and X+ = h+ (H). | Under H1+H2: sum_{v in G} d_v = 13 with d_v = 13 - g+(v) >= 0; T[G] transitive count >= 1872. | none |
| 2c | STAR identity sum_H o^2 + sum_G d^2 = 4394 (sec 3.2) | VERIFIED | Cyclic count 3c_0 + c_1 = 4225 with c_0, c_1 from transitive counts; sum omega^2 = sum o^2 since sum o = 325. | Under H1+H2: sum_H o_w^2 + sum_G d_v^2 = 4394; sum (o-12.5)^2 = 331.5 - sum d^2 in [162.5, 318.5]. | none |
| 2d | Prop 4.1 (a) | VERIFIED | Algebra of sum (o-12.5)^2 re-done (sum o^2 - 4062.5). | As stated. | none |
| 2e | Prop 4.1 (b) | VERIFIED | x <= 1 forces all HH arcs x=1, s_h = gamma_h, sum s^2 = sum d^2 = 169, so x(v0,h0) = 13 > 1. | Under H1+H2 some pair has D >= 14. | none |
| 2f | Prop 4.1 (c) | VERIFIED | eta >= Z >= B >= N^-; N^- >= (169 - sum d^2)/25 from sum s^2 = 338 - sum d^2. | eta >= N^-, N^- >= (169 - sum d^2)/25. | none |
| 2g | Prop 4.2 (structure with g+(v0) = 0) | VERIFIED | o_h = 12 + x(v0,h) from |G cap N-(h)| = 1 + o_h; forces x(v0,h0)=13, x(h0,h)=1. | As stated. | none |
| 2h | Prop 4.3 (family impossible up to HH defects) | VERIFIED (conditional on (3.3), (3.4b), (3.6), all re-checked) | 2450 + 2 ex_H <= 147 eta + E; defect-free case contradicted by 17050 < 19500. | If all HH x = 1 (eta = 0), the Prop 4.2 family is impossible; in general eta >= 17 or E >= 2450 - 147 eta. | none (see 2j, 2i for the flawed sub-claims) |
| 2i | Sec 5 bullet 2 | FLAWED | 'S2 >= 346 with eta = ex = 0' is impossible: eta = ex = 0 forces S2 = 338. | The correct form is 520 + 2 ex <= 147 eta + 69 G + E, with G = sum over G->H arcs of x(x-1). | Withdraw 'S2 >= 346 (take eta = ex = 0)'. |
| 2j | Sec 4 'e.g.' sub-claim | FLAWED | 'sum d^2 = 13 forces N^- >= 9, hence eta >= 9' is not derived: the stated bound gives N^- >= 156/25, so N^- >= 7. | eta >= 7 when sum d^2 = 13. | Withdraw 'N^- >= 9, eta >= 9'; replace by N^- >= 7, eta >= 7. |
| 2k | Sec 3.6 certificate values lambda(9..18) | VERIFIED (typo) | Values recomputed: -7/4, 0, 1/4, 1, 17/4, 12, 105/4, 49, 82.25 (L=17), 128 (L=18). | As stated. | Fix the sign in the L=11 and L=12 factorizations (g - 1/4 = -(2/3)(...), g - 1 = -(1/3)(...)). |
| 3a | r1_NO-Z s.2 Lemma Delta (i) | VERIFIED | Arc count R -> N+ = 66 - F; sum X_a = 6 - F; F <= 6. | F_x <= 6 for x in L. | none |
| 3b | Lemma Delta (ii) | VERIFIED | Double count gives 550 + 2 Delta = 514 + 11F + sum X^2; so sum X^2 = 36 - 11F + 2 Delta. | As stated. | none |
| 3c | Lemma Delta (iii) | VERIFIED | Case analysis on partitions of 4 (F=2 needs Delta=1, one X=4). | F = 0 gives one X_a = 6; F = 1 gives one X_a = 5; F = 2 gives one X_a = 4. | none |
| 3d | Lemma Sigma (a) | VERIFIED | sum_a X_a = 12 s - g - 120. | As stated. | none |
| 3e | Lemma Sigma (b) and closed form sum X^2 = 6s^2 - 114s + 600 + (11-2s)g + 2 Delta_S | VERIFIED | Term-by-term check of c+ = 1 + c- - f - f', pair sums and the -10 and +25*24 terms. | As stated. | none |
| 3f | Sec 3 'f(A_b) >= J_b - 2 >= 3' for b in B_0 | VERIFIED (conditional) | Algebra and the F1 nonnegativity give g >= J - 2. The J >= 5 input is supplied by r1_AUDIT-52-B 4.3 and 5.2 (item 6). Using only the verified J >= 3, the conclusion is f >= 1. | f(A_b) >= 3 conditional on J >= 5. | none (cite the dependency) |
| 3g | Lemma 6.4 last paragraph ('at least 78 - 12E pairs of A in no common tight set') | FLAWED (general case) | Uncovered >= 276 - Theta, and Theta >= 198 + 12E is a LOWER bound; the inequality needs an upper bound on Theta. Holds only for 0/1-valued f and m. | Only the identity sum (D - 11) = 178.5 + 12.5E + (sum f^2 + sum m^2)/2 and Theta >= 198 + 12E. | Withdraw the general 'at least 78 - 12E uncovered' claim; keep only the 0/1-valued case. |
| 4 | r1_DUAL s.3 Lemma Theta: r_L, M(L), Theta(L) for L = 10..16, identity Theta = 20 + 5z + C(z,2) + 2C(z,3), and summed inequality A3 <= sum Theta - 10 a2 + 70 a1 | VERIFIED | Each M(L) recomputed (L=10: 0; 11: 3/8; 12: 3/2; 13: 51/8; 14: 18; 15: 315/8; 16: 73.5); cubic checked at z = -5..8; sum algebra via (G4) and s_L - (3L^2/4 - 3L + 2) = -15L + 105 re-done. | A3 <= sum over Y of Theta(L_Y) - 10 a2 + 70 a1 holds for every F1-tournament on 52 vertices (pointwise certificate). | none (the QR_67 sanity figure was not checked) |
| 5a | r1_MOM-EXACT A.3 expansions 6C(26-e,3) = 15600 - 1874e + 75e^2 - e^3 and 6C(25+e,3) = 13800 + 1727e + 72e^2 + e^3 | VERIFIED | Term-by-term expansion re-done; sums with sum e = 26 give 762476 + 75 S2 - S3 and 762502 + 72 S2 + S3. | As stated. | none |
| 5b | Totals sum (k + k+) = 254163 + 24.5 S2 | VERIFIED | 1524978/6 = 254163; independent route -541450 + 49 Theta agrees. | sum_Y L_Y = 254163 + 24.5 S2 for every F1 tournament on 52 vertices. | none |
| 5c | Vertex pair identity V1 (sum_u D_wu = 25 d-(w) - eps^-(w)) | VERIFIED | Double count re-done; global check gives 650 + S2 on both sides. | sum_u x_wu = 13 + 25 e(w) - eps^-(w) for every vertex. | none |
| 6 | r1_AUDIT-52-B s.4.3 (s >= 4) and s.5.2 (J = 4 killed, so J >= 5) | VERIFIED (conditional on upstream sec 2 formulas E, PS, S, B, Ex, A-i, D12) | (P) rewrite, invariant 4.1, cases s = 0..3, and the nine partitions of 10 in 5.2 all re-checked. | s >= 4 and J >= 5 (the TP Lemma C and J >= 5 claims) can be used by round 2, conditional on sec 2 of that file. | Earlier '5+5 never treated' remarks in 5.1 are superseded by 4.3, not in the record as a flaw. |

## Statements that must be withdrawn or corrected in the record

1. r1_MOM-BALANCED s.4 'e.g.' and s.5: 'sum d^2 = 13 forces N^- >= 9, hence eta >= 9' is wrong as derived. Correct: N^- >= 7, eta >= 7.
2. r1_MOM-BALANCED s.5 bullet 2: '(5.1) forces E_tail > 0 or S2 >= 346 (take eta = ex = 0)' is wrong. With eta = ex = 0 the value S2 is forced to 338. Correct: 520 + 2 ex <= 147 eta + 69 G + E_tail.
3. r1_MOM-BALANCED s.3.6: the L=11 and L=12 factorizations have the wrong sign (values are right).
4. r1_NO-Z s.6 Lemma 6.4 last paragraph: 'at least 78 - 12E pairs in no common tight set' does not follow in general. Keep only the 0/1-valued case.
5. Dependency, not a withdrawal: r1_NO-Z s.3 (f(A_b) >= 3) and s.6 (Lambda_a <= 15) need J >= 5, now supplied by r1_AUDIT-52-B s.4.3 and s.5.2. Cite them, not the older [TP] section 5.

## Items NOT verified (UNCHECKED)

- r1_DUAL.md: sections 1, 2, 4, 5, 7 (other than NT-B01 and Lemma Theta). The IB-min impossibility (sec 5, 'no tournament has the IB-min pair data') and the n_13 / 1625 bound in the status line are UNCHECKED.
- r1_MOM-BALANCED.md: sections 1, 5 (beyond the bullets above), 6 are UNCHECKED except the parts listed in item 2.
- r1_NO-Z.md: sections 4-5 beyond the Bridge lemma and Lemma 5.1-5.4, 6.1-6.3, were checked, but Proposition SF and Claim Q are taken from the brief (audited in round 1), not re-derived.
- r1_AUDIT-52-B.md: sections 6.1-6.2, 7 and 8 are UNCHECKED here.
- Upstream formulas (E), (PS), (S), (B), (Ex), (A-i), (D12), c <= 4 are not re-derived; they are taken from round-1 audit section 2 as the brief records them.

## Log

(entries appended below as checks are completed)

### Item 1: NT-B01 (r1_DUAL.md s.6) -- VERIFIED

Hand re-check, step by step:
- Step 0: sum d- = 1326 = 52*25 + 26 gives |V_1| = 26, |V_0| = 26. Arcs: inside V_0 = C(26,2) = 325; V_1->V_0 = 26*25 - 325 = 325; V_0->V_1 = 676 - 325 = 351. Checked.
- Step 1 (V2): sum_{a->v} lambda_av = C(d-(v),2) holds (in-degree of a inside T[N-(v)] equals lambda_av). v in V_0: 300 = 25*12 forces all 12 (since lambda in {12,13}). v in V_1: 325 = 26*12 + 13 gives exactly 13 in-nbrs with lambda 13. Checked.
- Step 2 (V2'): sum_{b in N+(v)} (d-(b)-1-lambda_vb) = C(d+(v),2). v in V_1: 600 + f - 300 = 300 + f, so excess sum = f. v in V_0: 624 + f - 325 = 299 + f, excess sum = f - 13. Both checked.
- Step 3: out-nbrs in V_0 have head in V_0 so lambda = 12; excess f(v) spread over f(v) V_1-out-nbrs each <= 1, so all equal 1: every V_1-internal pair has lambda = 13. w_v = f - 12, t_v = f - 13. sum_{V_0} t = 351 - 338 = 13 = sum_{V_1} w = 325 - 312. Checked.
- Step 4: cyclic triples through a->b = d-(a) - lambda_ab (Checked). Only the 13 lambda-13 pairs are V_0->V_1 arcs (V_1->V_0 arcs have head in V_0, so lambda = 12). Sum over mixed arcs = 351*25 - 4225 + 325*14 = 8775 - 4225 + 4550 = 9100; c_1 + c_2 = 4550. Total cyclic = 22100 - 16250 = 5850, so c_0 + c_3 = 1300. Checked.
- Step 5: transitive triples inside V_1 counted by source: sum_{V_1} C(f,2); c_3 = 2600 - that. Inside V_0 transitive by source with out-degree inside V_0 = 26 - f. Sum = 3900. Checked.
- Step 6: sum_{V_1} C(12+w,2) = 1716 + 11.5*13 + (sum w^2)/2 = 1865.5 + ..., sum_{V_0} C(13-t,2) = 2028 - 162.5 + ... = 1865.5 + ... Total 3731 + S/2 = 3900 gives S = 338. Checked.
- Step 7: S = sum over G-edges (t_v + w_b) since deg_G(v) = t_v, deg_G(b) = w_b. Edge vb: deg v + deg b - 1 <= |E(G)| = 13, so t_v + w_b <= 14 and S <= 13*14 = 182 < 338. Contradiction. Checked.
- Cross-check (a) of the file (S = 26 for the spread choice) also re-checked: 13*78 + 13*66 = 1872 per class.
- Only the 'generalisation' paragraph was not part of the target; its sub-claim sum_{V_0}(f-13) = 13 holds in all cases (it is 351 - 338), so it is fine.
Conclusion: NT-B01 holds as stated (hypothesis: all in-degrees in {25,26}, all lambda in {12,13}). The proof does not use F1. Safe consequence for round 2: an F1 tournament on 52 vertices with all in-degrees in {25,26} has a pair P with lambda_P = 11 (tight) or lambda_P >= 14 (F2 gives lambda >= 11 for every pair, so these are the only other values).

### Item 4: Lemma Theta (r1_DUAL.md s.3) -- VERIFIED

- s_L = (3/4)(L-12)^2 - 1 = (3/4)L^2 - 18L + 107: checked for L = 10..16 (2, -1/4, -1, -1/4, 2, 23/4, 11).
- Allowed u: u in Z + L/2 with u >= 5 - L/2. Values rechecked:
  - L=10: u in Z, u>=0, f(0)=0 (f increasing since f' = 3u^2-3u+2 > 0). M=0. Theta = 20. OK.
  - L=11: u in Z+1/2, u>=-1/2. f(-1/2)=f(1/2)=f(3/2)=-3/8, f(5/2)=5.625. M=3/8. r_11=(u^2-1/4)(u-3/2) (expanded, checked). Theta = 1/4 + 99/4 = 25. OK.
  - L=12: u in Z, u>=-1. f(-1)=f(1)=-3/2, f(0)=0, f(2)=0. M=3/2. r_12=(u^2-1)(u-3/2) (expanded, checked). Theta = 1 + 30 = 31. OK.
  - L=13: u in Z+1/2, u>=-3/2. f(-3/2) = -3.375 - 3.375 + 0.375 = -51/8. f(-1/2)=f(1/2)=-3/8. M = 51/8. Theta = 17/4*... (2/3)(51/8) = 17/4 = 4.25; plus 143/4 = 35.75; sum 40. OK.
  - L=14: u in Z, u>=-2; f(-2) = -8-6-4 = -18, M=18, Theta = 12 + 42 = 54. OK.
  - L=15: u in Z+1/2, u>=-5/2; f(-5/2) = -15.625 - 9.375 - 14.375 = -39.375, M = 39.375, Theta = 26.25 + 48.75 = 75. OK.
  - L=16: u in Z, u>=-3; f(-3) = -27-13.5-33 = -73.5, M=73.5, Theta = 49 + 56 = 105. OK.
  - Extra values rechecked: L=5..9 and L=17,18 give -60,-30,-9,5,14,146,200 as stated. OK.
- Cubic identity Theta(L) = 20 + 5z + C(z,2) + 2C(z,3), z=L-10: checked at z = -5..8 (all 14 values match). Also Theta(z) = z^3/3 - z^2/2 + (37/6)z + 20 as a polynomial.
- Pointwise part: (G4) rewritten as sum u^3 = -sum(3L^2/4 - 3L + 2)u was re-derived: C(k,3) - C(m,3) = (u^3 + (3a^2 - 1)u)/3 with a = L/2 - 1 (derived via x^3 - x identity). Check: 3a^2 - 1 = 3L^2/4 - 3L + 2. OK.
- Algebra: s_L - (3L^2/4 - 3L + 2) = -15L + 105. So sum(u^3 + s_L u) = -15 a2 + 105 a1. OK.
- Summed inequality: 0 <= -15a2 + 105a1 - (3/2) sum u^2 + sum M gives sum u^2 <= -10 a2 + 70 a1 + (2/3) sum M. With sum u^2 = A3 - sum L(L-2)/4 (from C(k,2)+C(m,2) = L^2/4 - L/2 + u^2, checked), this gives A3 <= sum Theta(L_Y) - 10 a2 + 70 a1. OK.
- Note the moment-form Taylor expansion: Theta''/2 = z - 1/2, cubic term delta^3/3. Checked. Numerical check N*Theta(zbar) = 22100*27.925 approx 617,150 also rechecked (zbar = 254800/22100 - 10 = 1.5294).
Conclusion: Lemma Theta is correct as stated, for all L (pointwise on the lattice), and the summed inequality follows. Round 2 may use it. Only caveat: it depends on (G3) and (G4), which rest on (C5) and (C6); both were re-derived here and are correct. Its use at N = 52 also depends on the definitions of x_P = lambda_P + 1 - e_a - e_b (checked).

### Item 2: r1_MOM-BALANCED.md sections 2-4

Lemma 2.1 -- VERIFIED. v in G: C(25,2) = 300 = 25*12 with each term >= 12 (H2), so all in-pairs have x = 0. v in H: C(26,2) = 325 = 26*12 + 13, so sum of x over in-nbrs = 13. (In-degree of a inside T[N-(v)] equals lambda_av: checked.)

Lemma 2.2 -- VERIFIED. Common out-nbrs m(a,v) = 51 - d-(a) - d-(v) + lambda_av (re-derived). v in G: 13 g+ + 12 h+ + X+ = 325 gives g+ + X+ = 13 (checked with h+ = 26 - g+). v in H: 12(25 - h+) + 11 h+ + X+ = 300 gives X+ = h+ (checked). Consequences (i)-(iii) checked; in particular T[G] transitive count = (3731 + sum d^2)/2 >= 1872 (sum d = 13, d >= 0 integers).

STAR identity (3.2) -- VERIFIED. cyc(a->b) = d+(b) - m_P re-derived; per arc-type values 13 / 14 / 13-x / 14-x re-derived; arc totals 4225 + 4550 + 4550 + 4225 = 17550 = 3*5850 (checked). t_1 = 4394 - sum d^2 + (sum omega^2 - 325)/2 re-derived (transitive triples with one H-vertex, counted by source). Solving 3c_0 + c_1 = 4225 with c_0 = (1469 - sum d^2)/2 gives 12844 - sum d^2 - sum omega^2 = 8450, and sum omega^2 = sum o^2 because sum o = 325. So sum o^2 + sum d^2 = 4394 (checked).

Prop 4.1 -- (a) VERIFIED: sum (o - 12.5)^2 = sum o^2 - 4062.5 = 331.5 - sum d^2 (checked). (b) VERIFIED: x <= 1 forces every HH arc to have x = 1 (out-mass of w = number of HH out-arcs), so in-mass = in-degree gives s_h = gamma_h, then sum s^2 = sum d^2 = 169 forces d_{v0} = 13 and gamma_{h0} = 13, so x(v0,h0) = 13 > 1. Contradiction (checked). (c) VERIFIED: y = x - 1, sum of y over out-arcs = 0 and over in-arcs = b_h (checked); eta >= Z >= B >= N^- (checked each inequality); N^- >= (169 - sum d^2)/25 (checked: sum s^2 = 338 - sum d^2 identically, and the bound 169 + 25 N^-).

Prop 4.2 -- VERIFIED. g+(v0) = 0 gives N+(v0) = H, N-(v0) = G'. o_h = 12 + x(v0,h) re-derived via |G cap N-(h)| = 1 + o_h. Sum s^2 = 169 forces s_{h0} = 13 (o_{h0} = 25), x(v0,h0) = 13, x(v0,h) = 0 on H', x(h0,h) = 1 on H' (lambda = 1 + o_h = 13). All checked.

Prop 4.3 -- VERIFIED, conditional only on the inputs (3.3), (3.4b), (3.6), which were also checked here:
- (3.3) sum L^2 = 2,930,876 + 46 S2: re-derived from L0 = 13 - a - sigma + X, sum L0^2 = 2,581,150 (checked from sum a = 33150, sum a^2 = 65650, sum sigma = 16250, sum sigma a = 24375), sum L0 X = 166244 - S2 (checked: sum X = 16900, sum aX = 41275, sum sigma X = 12181 + S2), sum X^2 = 48 S2 + sum xi^2 with sum xi^2 = 17238 (checked).
- (3.4b) sum u^2 = 22737 + 2ex - 11.5 S2 + eta: re-derived via A3 = 628056 + 2ex + eta (f_G, f_H decomposition checked; F - ex = eta checked) and sum L = 254800.
- Special triples: L = 24, u = 0 (checked on both y in G' and y in H').
- S2 = 494 + 2 eta for the family (checked). Non-special sums: sum (L-12) = -11000, sum (L-12)^2 = 46 S2 - 9124 (checked).
- Majorant sum Lambda_q = 731,614 + 69 S2 (checked) and sum_ns lambda <= -11,355 + 57.5 S2 + E (checked).
- Final: 36,536 + 2 ex_H <= 69 S2 + 9 eta + E, i.e. 2450 + 2 ex_H <= 147 eta + E (checked arithmetic).
- Defect-free check: sum L^2 = 2,953,600 (checked), and sum_ns u^2 <= 17,050 < 19,500 (checked; L counts 12300 / 8450 / 1300 / 50 re-derived from the a-classes).

Section 3.6 (certificate lambda(L)) -- values VERIFIED for L = 9..18 (lambda = -7/4, 0, 1/4, 1, 17/4, 12, 105/4, 49, 82.25 at 17, 128 at 18; the e(14..18) = 2, 8, 20, 40, 70 are correct). Minor FLAW (typo, value unaffected): the factorizations have the wrong sign: g(u) - 1/4 = -(2/3)(u+1/2)(u-1/2)(u-3/2) for L = 11, and g(u) - 1 = -(1/3)(u-1)(u+1)(2u-3) for L = 12. The text's "+" should be "-". Also "zero at u=-3/2, min >= 0" for L = 13 is garbled; the value 17/4 at u = -3/2 is correct.

FLAW (sub-claim, Section 4 'e.g.' and Section 5): "sum d^2 = 13 forces N^- >= 9, hence eta >= 9". The stated inequality N^- >= (169 - sum d^2)/25 gives N^- >= 156/25 = 6.24, so N^- >= 7 and eta >= 7. The bound 9 is not derived. Correct statement: N^- >= 7, eta >= 7 (no sharper bound is shown here).

FLAW (sub-claim, Section 5, bullet 2): "(5.1) forces either E_tail > 0 or S2 >= 346 (take eta = ex = 0 as best case)". With eta = ex = 0 the pair counts are forced: S2_HH = 325 + 2 eta and S2_GH = 13 + G (G := sum over G->H arcs of x(x-1)), so S2 = 338 + 2 eta + G, and ex = 0 forces G = 0 (f_G(2) = 12 > 0). So eta = ex = 0 gives S2 = 338 exactly, not S2 >= 346. The correct form of the inequality is 520 + 2 ex <= 147 eta + 69 G + E_tail. The conclusion (defects or tail are needed) is still correct.

### Item 3: r1_NO-Z.md section 2 (Lemma Delta) and section 3 (Lemma Sigma)

Setup checked: d-(v) = 24, A = N-(v) (24 vertices), B = N+(v) (27), E + E_B = 27, A_x = A cap N-(x), a_x >= 11 (F2). Sum over A of f = 12 (sum of in-degrees inside T[A] = C(24,2) = 276 = 24*11 + 12): VERIFIED. |L| >= 12: VERIFIED. (S4) sum_b m_b = 27 - E: VERIFIED (324 - E - 297). (S5) |B_0| >= E: VERIFIED. (S6): VERIFIED.

Lemma Delta -- VERIFIED.
- Setup: R = A_x for x in L is 11-element and T[R] 5-regular (sum of in-degrees C(11,2) = 55 = 11*5 with min in-degree 5). Out-degree of r in A is 12 - f_r; out-nbrs of r in A are 5 (inside R) + x + (6 - f_r) in N+. Arc count R -> N+ = 66 - F_x, and so sum X_a = 6 - F_x (checked, including 12 * 5 = 60).
- (ii) Double count of sum over s<s' in R of |D({v,s,s'})| = sum over w in A of C(n_w,2), n_w = |N+(w) cap R|: n_w = 5 on R (11 vertices, contributing 110), n_x = 0, n_a = 6 - X_a on N+. LHS 275 + Delta_x. Algebra (x2): 550 + 2 Delta = 514 + 11 F + sum X^2, so sum X^2 = 36 - 11F + 2 Delta. Re-derived: CHECKED.
- (iii) F = 0: sum X^2 = 36 + 2 Delta <= (sum X)^2 = 36, so Delta = 0 and one X = 6. F = 1: sum X^2 = 25 + 2 Delta <= 25, one X = 5. F = 2: sum X^2 = 14 + 2 Delta, must be <= 16 and partitions of 4 give squares in {16,10,8,6,4}; 14 is not among them, so Delta = 1, sum X^2 = 16, one X = 4. CHECKED.
- Budget split: the B-part 8 - J_x + F_x re-derived from sum_{r in R}(13 - e_r + f_r) = 143 - J + F (out-nbrs of r in B: 26 - e - 1 - (12 - f)) minus 135. CHECKED. The (E) identity it relies on: sum over the 50 vertices y outside P of k({a,b,y}) = sum_{r in R}(24 - e_r), giving 14 - J (CHECKED in r1_DUAL section 1, (C8)).

Lemma Sigma (a) -- VERIFIED: sum_a X_a = sum_{w in S} d+_A(w) - 120 = 12 s - g - 120.

Lemma Sigma (b) and the closed form -- VERIFIED.
- sum_a |S cap R_a|^2 = sum_{w in S}(12 - f_w) + 2 sum_{w<w'} c+(w,w'), with c+(w,w') = 1 + c-(w,w') - f_w - f_w' for w -> w' (re-derived from |N-_A(w) cup N-_A(w')| minus {w,w'}: 21 + f_w + f_w' - c-; 22 - that).
- Sum over pairs: sum c- = 5 C(s,2) + Delta_S, so sum_{w<w'} c+ = 6 C(s,2) + Delta_S - (s-1) g.
- Total: 12 s + 6 s(s-1) - (2s-1) g + 2 Delta_S. Then sum X^2 = (that) - 10(12 s - g) + 600 = 6 s^2 - 114 s + 600 + (11 - 2s) g + 2 Delta_S. CHECKED term by term.
- s = 11: sum X = 12 - g, sum X^2 = 72 - 11 g + 2 Delta_S (726 - 1254 + 600 = 72). CHECKED.
- Near-twin table (max X >= 6, 6, 5, 5, 4, 3, 1 for g = 0..6): CHECKED (61/11 = 5.55, 50/10 = 5, 39/9 = 4.33, 28/8 = 3.5, 17/7 = 2.43, 6/6 = 1).
- Pair excess eps_z = 6 + 11 f_z - f(R_z) and Gamma = 66 + sum f^2 / 2: CHECKED (sum_z eps_z = 132 + sum f^2 = 2 Gamma).

Lemma Sigma, consequence 'f(A_b) >= J_b - 2' (section 3, tight pairs {v,b}, b in B_0): the algebra is CHECKED: sum over A\S of X = 12 - g, sum over B\{b} of (|S cap A_b'| - 5) = 2 - J + g, total 14 - J, and each part is >= 0 (F1), so g >= J - 2. The derivation is VERIFIED.
- DEPENDENCY: the conclusion f(A_b) >= 3 uses J_b >= 5. Brief section 8 recorded only J >= 3 (Theorem 1') as verified. The later round-1 sections of r1_AUDIT-52-B (sections 4.3 and 5.2: s >= 4, then J = 4 killed, so J >= 5) were checked in Item 6 below and hold, conditional on that file's section 2 formulas. So f(A_b) >= 3 is usable conditionally on those sections. Without them only f(A_b) >= 1 follows from the verified J >= 3. Same dependency for Lemma 6.3 (Lambda_a <= 20 - J_a <= 15).

Section 4 Bridge Lemma -- VERIFIED given Proposition SF (which the brief section 8 records as audited). Checked: y in N-(r) is neither x nor v; the two cases (y outside D(P): q_y = |A_x cap A_y|; y in A_x: in-degree 5 by 5-regularity). Counting d-_B(r) = 14 - f_r: CHECKED.

Section 5: Lemma 5.1 (a), (b), (c): VERIFIED. Lemma 5.2 (clusters): VERIFIED given Bridge. Lemma 5.3 (skew identity): VERIFIED: RHS = (11-i)^2 + 2(5i - C(i,2)) - 10(11-i) = 11 - i, checked term by term. Use claim (x in L, b in B_0 with x -> b, forcing |R_x cap A_b| = 5): VERIFIED.
Lemma 5.4 (moment identity): VERIFIED: sum t^2 = 5 tau^2 + 6 tau + 2 Xi; variance form 6 tau - tau^2/24 + 2 Xi checked (5 - 121/24 = -1/24). Z-vertex bounds tau <= 23 + 7.67 Xi/tau and tau <= 12 + 4 Xi/tau: CHECKED (121/23 - 5 = 6/23; 121/22 - 5 = 1/2).

Lemma 6.1 (xi_S <= 14 - J_x): VERIFIED (sub-sum of the (E) budget; y in R_x contribute 0).
Lemma 6.2 (Fisher-type, |T'| <= 24): VERIFIED. Gram = 6I + 5J + C', C' >= 0 with zero diagonal and row sums < 6; Gershgorin gives positive definiteness; J_x >= 9 gives xi <= 5 < 6. Conditional on J_x >= 9 being a usable hypothesis (not an issue here).
Lemma 6.3 (popularity window): identity Lambda_a = 6 tau - t_a - sum_{N+(a)} t_w: VERIFIED. Bounds 6 <= Lambda_a <= 20 - J_a: VERIFIED given Lemma 6.1 and 5.1(c); the value 15 uses the J >= 5 dependency above.

Lemma 6.4 (pair-coverage identity): the identity sum over the 276 pairs of (D - 11) = 178.5 + 12.5 E + (sum f^2 + sum m^2)/2 is VERIFIED (u in A contributes C(12 - f_u, 2), u in B contributes C(13 - m_u, 2), v contributes 0; totals 1446 + sum f^2/2 and 1768.5 + 12.5 E + sum m^2/2, minus 3036). Lower bound Theta >= 198 + 12E: VERIFIED (sum f^2 >= 12, sum m^2 >= 27 - E).
FLAW (inference, Lemma 6.4 last paragraph): 'at least 78 - 12E pairs of A lie in no common tight set'. From cov <= Theta, the number of uncovered pairs is >= 276 - Theta, and this is >= 78 - 12E only if Theta <= 198 + 12E. Theta is bounded BELOW by 198 + 12E, so the inequality goes the wrong way in general. It holds exactly only when f and m are 0/1-valued (then Theta = 198 + 12E). The text's parenthesis says so, but the general sentence should be dropped. Also the step 'D >= 12 for pairs inside a tight set' depends on the r1_AUDIT-52-B section 2 claim, which is recorded as only partially audited.

Minor typo/garble: section 2 'Interpretation' is fine. Nothing else in section 2-3 is wrong.

### Item 5: r1_MOM-EXACT.md section A.3 and section B (V1)

A.3 expansions -- VERIFIED.
- (26-x)(25-x)(24-x) = 15600 - 1874x + 75x^2 - x^3 (expanded term by term: 650*24 = 15600; 650x + 1224x = 1874x; 51*24 + 24 = 75x^2 term; -x^3). CHECKED.
- (25+x)(24+x)(23+x) = 13800 + 1727x + 72x^2 + x^3 (600*23 = 13800; 600x + 1127x = 1727x; 49*23 + 23... i.e. 49x^2 + 23x^2 = 72x^2). CHECKED.
- Sum over 52 vertices with sum e = 26: 52*15600 = 811200, 1874*26 = 48724, so 6 sum k = 762476 + 75 S2 - S3 (CHECKED). 52*13800 = 717600, 1727*26 = 44902, so 6 sum k+ = 762502 + 72 S2 + S3 (CHECKED).
- sum (k + k+) = (1524978 + 147 S2)/6 = 254163 + 24.5 S2 (1524978/6 = 254163 exactly). CHECKED.
- sum (k - k+) = (3 S2 - 2 S3 - 26)/6. CHECKED.
- Balanced check (S2 = S3 = 26): sum k = 127400, sum (k-k+) = 0. CHECKED.
- Independent route for sum L (A1' with Theta = 16237 + S2/2, sum sigma = Theta, sum E_Y = 33150): -541450 + 49 Theta = 254163 + 24.5 S2 (795613 = 49*16237). CHECKED.
- A.1 (formula (A1) and N = 52 form (A1')): re-derived from n_0..n_3 (n_2 = B - 3k, n_1 = A - 2B + 3k, n_0 = N - 3 - A + B - k). CHECKED.
- (A2) c_P = 1 + D_P - e(w) - e(w'), (A3) m(w,w') = 25 + e(w') - [w->w'] - D_P: CHECKED.
- Cubic identity A.4: 24[C(k,3) - C(k+,3)] = delta (delta^2 + 3L^2 - 12L + 8). Re-derived from k(k-1)(k-2) = (x+1)x(x-1) with x = k-1. Spot checks at (L,k,k+) = (13,5,8) (gives -1104 both sides) and (11,6,5) (gives 240 both sides). CHECKED. g(10..13) = 188, 239, 296, 359: CHECKED.
- (I6), (I7) (class-refined first moments): VERIFIED by the source/sink counting in T[N+(w)], T[N-(w)]; DRT(51) check 1275*66 = 84150 CHECKED.

Vertex pair identity V1 -- VERIFIED. sum_{u != w} D_wu = 25 d-(w) - eps^-(w): re-derived by swapping the count (each z in N-(w) has d+(z) - 1 = 25 - e(z) out-nbrs other than w). Then sum_u x_wu = 13 + 25 e(w) - eps^-(w) (625 + 25e - eps^- - 612). CHECKED. Global check: sum over w gives 650 + S2 on both sides (CHECKED). The c-version (ii) is consistent with V1 (reduces to eps^+ + eps^- = 26 - e(w)), CHECKED.
- V2 (e(w) = -1 gives sum_u x = -12 - eps^-(w), hence >= 10 tight pairs at w given eps^- >= -2 from Claim Q and no in-degree 23): VERIFIED given Claim Q and A52 Lemma 1 (both recorded as audited in the brief section 8).
- V3 (balanced): the three equations 2X_UU + X_UW = 663, 2X_WW + X_UW = 13, hence X_UU - X_WW = 325, X_UU + X_WW + X_UW = 338, and the no-tight consequences X_WW <= 6, X_UW <= 13, X_UU >= 325: VERIFIED (arcs inside U = 325 and arcs U->W = 325 re-counted). Sanity claim (a_w = 13 for all w in U impossible since sum a_w = 325): VERIFIED.

No FLAWED items in section A.3 or B.

### Item 6: r1_AUDIT-52-B section 4.3 (uniform proof of Lemma C) and section 5.2 (J = 4 case) -- VERIFIED (conditional)

The 'step 4 rewrite of the pair formula' is read as the (P) line of section 4.3, which is the rewrite of (S) and (B) with 4D = 48 + 4 delta. Both (S), (B), (E), (PS), (Ex), (A-i), (D12) are upstream formulas from section 2 of that file (not reproduced here). The brief section 8 records them as verified, and I did not re-derive them. Everything downstream was checked.

- (P) rewrite: s = 4D - c - 45 - E_both with D = 12 + delta gives 3 + 4 delta - c - E_both. CHECKED.
- 4.1 invariant sum_{V_+} nu_u = 14 - 6h: CHECKED (sum_{V_+} j = J; sum_{V_+} m = sum_H t_y = 6h - (14 - J) using (E) and (A-i)). Gives 14 mod 6 and 14 mod 3 obstructions. CHECKED.
- 4.2 (a): rho_u = 5 nu_u + Phi_u: CHECKED (Phi_u = sum (t-1), tau_u = sum (6 - t)). 4.2 (b) Ex(u) = 5 + 10 nu_u + g_u: CHECKED (lambda(q) = 10 - C(10-q,2) gives 0,4,7,9,10,10 for q = 5..10; checked).
- s = 0, 1: CHECKED. s = 2: delta = 5x + n, E_both = 4n, s(u,v) = 20x + 3 - c, bounds give 10x <= 2 + c <= 6 and 20x >= c - 3 >= -3, so x = 0, contradiction with 14 = 6h. CHECKED.
- s = 3: Phi_1 = n_12 + n_13 + 2n, g_1 = n, delta_12 = (5/2)(nu_1 + nu_2 - nu_3) + n_12 + n, E_both(1,2) = 4 n_12 + 3n, s(1,2) = 10(nu_1 + nu_2 - nu_3) + n + 3 - c_12 (all re-derived). Bounds force nu_1 = nu_2 = nu_3 = x, so 3x = 14 - 6h, impossible mod 3. CHECKED.
- 5.2 (J = 4, s = 4, all j = 1, E = 10): partition list of 10 into parts in {2..6} is complete (9 partitions, CHECKED). Step 1: sum tau = sum e(6-e) <= 20 and the six values 22, 24, 26, 32, 34, 40 exceed 20 (CHECKED). Remaining 6+4, 5+5, 6+2+2: each dies (CHECKED: 6+2+2 gives delta sum 2 with E_both = 4 so s < 0 on a delta = 0 pair; 5+5 gives D_34 = 17 and s(3,4) = 23 - c >= 19 > 15 = Ex; 6+4 forces delta_12 = 1, delta_34 = 5, same contradiction).
- Conclusion: s >= 4 (4.3) and J >= 5 (4.3 + 5.2) are established, conditional on section 2 of that file. Note the file's own earlier [TP] remarks (5.1, 5.2 'partition 5+5 never treated' etc.) are superseded by 4.3, and I did not audit the case lists in 5.1.
- Not checked here (UNCHECKED): sections 6.1-6.2, 7, 8 and 8.2 onward of r1_AUDIT-52-B. I read section 6.1 but did not verify its arithmetic line by line. The 314028 minimum it uses is the same value as in item 1 and item 2, which I did verify.

<!-- END -->
