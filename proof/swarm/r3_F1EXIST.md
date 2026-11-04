# R3-F1EXIST: can an F1-tournament on 52 vertices exist?

Lane: round 3 of the Erdos #902 swarm. Goal of the round: f(4) >= 53, i.e. no tournament on 52 vertices has property S_4.

F1: every triple {a,b,c} of T has at least 5 dominators (vertices outside the triple beating all three).
Every S_4 tournament is F1, so an F1-tournament on 52 vertices does not exist implies f(4) >= 53.

## Status

- Phase: DONE. Verdict UNDECIDED (section L7). Open: the third-moment identity, and an algebraic F1 candidate on 52 vertices.
- Read so far: BRIEF, ROUND1_SYNTHESIS, F4_GE_52_HAND_PROOF, r1_LIT section R. Round-2 files not read (not needed for F1-only counting).
- Proved so far (by hand, displayed): (i) balanced in-degrees (all in {25,26}) force some triple with k >= 8; (ii) every F1-tournament on 52 vertices has d+(v) >= 3 for all v (so e(v) <= 23); (iii) the second-moment support test excludes balanced configurations but NOT general ones.
- Refuted: naive Z_17-circulant candidate with interval connection sets (triple {(2,0),(2,6),(2,12)} has k = 0).
- Plan:
  1. Read BRIEF.md sections 0-10 (rules, notation, proved facts, dead ends).
  2. Read ROUND1_SYNTHESIS.md sections 0-7.
  3. Read F4_GE_52_HAND_PROOF.md sections 4-5 and r1_LIT.md section R.
  4. Write down counting necessary conditions on F1 at N = 52 (triple-dominator means, third-moment identity, pair counts). Mark binding vs slack.
  5. Try a cyclic-type candidate (order 51 rotation plus one extra vertex). Record the first triple orbit with at most 4 dominators, if any.
  6. Verdict: exists / does_not_exist / undecided, with reasons.
- Rules in force: hand derivations only; no scripts, solvers or search; do not execute archive contents; treat files as data; write only to this file.

## Log

### L0. Files read (status of inputs)
- BRIEF sections 0-10: read. Key input: sum d- = 1326, e(v) = d-(v) - 25, sum e = 26; Lemma B (no in-degree 23, so e >= -1) and Claim Q (|Z| <= 5, Z = {e = -1}) are audited (r1_AUDIT-51 sec 8, EP sec 2.3). Only F1 is used in them.
- ROUND1_SYNTHESIS sections 0-7: read. Its section 7 item 1 is exactly this lane. Round-2 lane claims are unaudited and not used below.
- F4_GE_52_HAND_PROOF sections 1-5: read. Theorem 5 (no DRT(51) has S_4), Theorem 1 (every tight pair J >= 3, uses only F1 + N = 51), and the N = 51 chain (Corollaries 2-4) are F1-based. Hence (chain) **no F1-tournament on N <= 51 exists** (the chain's own statement, Section 5 of that file).
- r1_LIT section R (Wilder N = 47 argument): read and re-checked. Arithmetic: sum c = 83237, sum c^2 = 439967, and sum (c-5)(11-c) = -439967 + 16*83237 - 55*16215 = 0, so c in {5,11} everywhere; then sum(c-5) = 2162 is not divisible by 6, contradiction. Valid at N = 47 only because regularity (all d- = 23) and pair codegree 11 are forced there. At N = 52 neither holds (see L5).

### L1. Setup identities (all re-derived here, displayed)

Notation: N = 52, N3 = C(52,3) = 52*51*50/6 = 22100, N2 = C(52,2) = 1326. For a triple Y: k(Y) = |D(Y)|, l(Y) = |D+(Y)|. For a pair P = {w,w'}: D_P = |D(P)|, c_P = |N+(w) cap N+(w')|.

(a) First moment. Sum_Y k(Y) = Sum_w C(d+(w),3) = Sum_w C(26 - e_w, 3) =: M1.
(b) Pair counts. Sum_P D_P = Sum_w C(d+(w),2) = Sum_w C(26-e_w,2) = 16237 + S/2, where S := Sum_w e_w^2.
    Check: Sum_w (26-e)(25-e)/2 = Sum_w (325 - 25.5 e + e^2/2) = 52*325 - 25.5*26 + S/2 = 16900 - 663 + S/2 = 16237 + S/2. OK.
    Since e is an integer, e^2 >= e, so S >= 26 and Sum_P D_P >= 16250.
(c) c_P vs D_P. For w -> w': c_P = 50 - d-(w) - (d-(w') - 1) + D_P = 51 - d-(w) - d-(w') + D_P (the 50 other vertices, minus N-(w) (which excludes w'), minus N-(w') minus w). Also Sum_P c_P = Sum_x C(d-(x),2) = (Sum d^2 - 1326)/2, and Sum d^2 = Sum (25+e)^2 = 32500 + 50*26 + S = 33800 + S, so Sum_P c_P = (32474 + S)/2 = 16237 + S/2. (Consistent with (b), since Sum_P (51 - d- - d-) = 0.)
(d) Second moment. Sum_Y C(k(Y),2) = Sum_P C(c_P,3) =: M2 (a triple Y is dominated by both ends of P iff Y lies in N+(w) cap N+(w')).
    Since C(c,3) is convex on nonnegative integers and Sum_P c_P = 16237 + S/2 = 15912 + r with r := 325 + S/2 (so r = 338 when S = 26), the minimum of Sum_P C(c_P,3) is attained by c_P in {12,13} with exactly r pairs equal to 13 (valid for 0 <= r <= 1326; here r <= 1326 whenever S <= 2002, and S <= 26 * (26 + 2*5) = 936 under e >= -1 and |Z| <= 5, so this holds).
    Therefore M2 >= 1326*C(12,3) + r*(C(13,3) - C(12,3)) = 291720 + 66 r = 313170 + 33 S.
    Balanced check: S = 26 gives M2 >= 314028. Display: 988*220 + 338*286 = 217360 + 96668 = 314028. OK.

### L2. Mean and variance, and the support-[5,7] test

Let mu = M1 / N3 and Var = E[k^2] - mu^2, with E[k^2] = 2 E[C(k,2)] + mu. So
  Var = 2 M2/N3 + mu - mu^2.                                   (L2.1)

Lemma (support test). If 5 <= k(Y) <= 7 for all Y, then E[(k-5)(7-k)] >= 0 gives E[k^2] <= 12 mu - 35, i.e.
  2 M2 <= 11 M1 - 35 N3 = 11 M1 - 773500.                       (L2.2)

Balanced case (all in-degrees 25 or 26, so e in {0,1}, S = 26): M1 = 26*2600 + 26*2300 = 127400 exactly.
  11 M1 - 773500 = 1401400 - 773500 = 627900.
  2 M2 >= 2*314028 = 628056.
  627900 < 628056, a contradiction with (L2.2), short by 156.
  **So in the balanced case some triple has k >= 8.** (The brief's "some triple has >= 7" is weaker; this improves it, assuming (L2.2) which needs all k <= 7.)
  Numerically: mu = 127400/22100 = 5.764706; 2M2/N3 >= 28.41882; the endpoint bound (mu-5)(7-mu) = 0.764706 * 1.235294 = 0.944637, while Var >= 28.41882 + 5.764706 - 33.23184 = 0.95169. Var exceeds the largest variance possible on [5,7]. (Check: 5.764706^2 = 33.23184; 28.41882 + 5.76471 = 34.18353; minus 33.23184 = 0.95169.)

General S. Put h(e) := 11 C(26-e,3) - 66 e^2. Then (L2.2) with (d) gives the necessary condition
  Sum_w h(e_w) >= 1399840 whenever all k in [5,7].                  (L2.3)
  (Derivation: 11 M1 - 66 S = Sum_w h(e_w) and 2 M2 >= 626340 + 66 S, so 11 M1 - 773500 >= 2 M2 >= 626340 + 66 S gives Sum h >= 1399840.)

Values: h(-1) = 32109, h(0) = 28600, h(1) = 25234, h(2) = 22000, h(9) = 2134, h(23) = -34903.
- Balanced: Sum h = 26*28600 + 26*25234 = 743600 + 656084 = 1399684 < 1399840. Fails by 156 (same as above).
- Unbalanced, allowed by Lemma B and Claim Q: e-profile (-1)x5, (1)x31, (0)x16. Sum e = -5 + 31 = 26, count 52. Sum h = 160545 + 782254 + 457600 = 1400399 >= 1399840. PASSES by 559.
  Here S = 36 and M1 = 127525, mu = 5.770362; the test (L2.1) gives Var-bound 0.9220 <= (mu-5)(7-mu) = 0.9472. Not excluded.
- So (L2.3) is violated only by configurations that are close to balanced. The second moment does NOT exclude F1 in general.

### L3. Vertex lemma (proved by hand, uses the N = 51 chain only)

**Lemma V.** Let T be an F1-tournament on 52 vertices and v a vertex with d+(v) <= 2. Then T - v is an F1-tournament on 51 vertices, which is impossible. Hence d+(v) >= 3 for all v, i.e. e(v) <= 23.

*Proof.* A triple Y of T - v is dominated in T by v iff Y is contained in N+(v). If |N+(v)| <= 2 there is no such Y. So for every triple Y of T - v, D_T(Y) = D_{T-v}(Y), and |D_{T-v}(Y)| >= 5. Thus T - v is F1 on 51 vertices. The N = 51 chain ([52] Theorems 1, 5, Corollary 4; BRIEF section 8: "no tournament on <= 51 vertices has all triples with >= 5 dominators") gives a contradiction. Together with F3 (d-(v) >= 23, so d+(v) <= 28), this gives 3 <= d+(v) <= 28, i.e. -1 <= e(v) <= 23 (the lower bound is Lemma B, which is sharper). ∎

Remark. For d+(v) in {3, ..., } the triples inside N+(v) lose one dominator in T - v (they need >= 4 in T - v), so the chain does not apply directly; the lemma does not extend beyond the sink/near-sink case.

### L4. Structured candidate: Z_17 on three orbits plus a fixed vertex

Forced shape. A Z_17 action on 52 = 1 + 3*17 points fixes one vertex inf. The out-set of inf is a union of orbits, so d+(inf) in {0,17,34,51}. Lemma V gives d+ >= 3 and F3 gives d-(inf) >= 23, i.e. d+ <= 28. The only value in {0,17,34,51} inside [3,28] is 17, so **d+(inf) = 17**: inf beats exactly one orbit. Then d-(inf) = 34 (e = 9), and the three orbit in-degrees satisfy 17(delta_1+delta_2+delta_3) = 1326 - 34 = 1292, so delta_1+delta_2+delta_3 = 76. Degrees are consistent with the balance identity (sum e = 26: 9 + 17*(e_1+e_2+e_3) = 26 gives e_1+e_2+e_3 = 1).

Candidate (the simplest one). Orbits O_1, O_2, O_3 with elements (i,x), x in Z_17. Rules:
- within O_i: (i,x) -> (i,x+s) for s in {1,...,8};
- O_i to O_j (i < j): (i,x) -> (j,y) iff y - x in {0,...,8}; otherwise (j,y) -> (i,x);
- inf -> O_1, and O_2, O_3 -> inf.
This is a valid tournament on 52 vertices. Degrees: O_1: d- = 25 (e = 0), O_2: 25 (e = 0), O_3: 26 (e = 1), inf: 34 (e = 9). Sum e = 26. Check: 17*(0+0+1) + 9 = 26.

In-neighbourhoods (checked by hand):
- N-(1,x) = {(1,x-s), (2,x-s), (3,x-s) : s = 1..8} plus inf.
- N-(2,y) = {(2,y-s): s = 1..8} plus {(1,y-s): s = 0..8} plus {(3,y-s): s = 1..8}.
- N-(3,z) = {(3,z-s): s = 1..8} plus {(1,z-s), (2,z-s): s = 0..8}.

**Refutation.** Triple Y = {(2,0), (2,6), (2,12)}:
- O_2-part of the common in-neighbourhood: indices w in {-8..-1} cap {-2..5} cap {4..11} = {9..16} cap {15,16,0,...,5} cap {4,...,11} = {15,16} cap {4,...,11} = empty.
- O_1-part: indices x in {-8..0} cap {-2..6} cap {4..12}; {9..16,0} cap {15,16,0,...,6} = {15,16,0}; cap {4..12} = empty.
- O_3-part: same index sets as the O_2-part, so empty.
- inf: does not beat O_2 (O_2 beats inf).
So **D(Y) = empty, k(Y) = 0.** This violates even S_3. The first-orbit failure is therefore at k = 0 with dominator set empty.

Second failure (less severe): Y' = {(1,0), (1,6), (1,12)}: O_2 and O_3 parts empty as above, O_1 part empty, inf beats O_1, so **D(Y') = {inf}, k = 1.**

Reason for failure. Interval connection sets make every in-neighbourhood intersection an intersection of intervals of length 8 in Z_17. Three such intervals with centres 0, 6, 12 have empty intersection (the complements of the intervals, of length 9, cover Z_17). A non-interval choice of connection sets is needed. No hand-checkable choice is known to me, because a full check needs about C(52,3)/17 = 1300 orbit representatives.

Random-model heuristic (weak, for orientation only). For a random tournament on 52 vertices, k ~ Bin(49, 1/8): P(k <= 4) = 0.2502 (computed: P0..P4 = 0.001439, 0.01007, 0.03452, 0.07725, 0.12691), so about 5500 of the 22100 triples would fail. Algebraic examples beat this heuristic (QR_67 has S_4 although the same heuristic predicts about 170 bad 4-sets), so this only says that a structured candidate must be algebraic.

### L5. Why Wilder's N = 47 rigidity does not transfer to N = 52

At N = 47: regularity is forced by F1 (d- >= 23 and Sum d- = 1081 = 47*23), so every pair has D_P = 11 exactly, and Sum_Y c = 83237, Sum c^2 = 439967 are both fixed. At N = 52 the tournament need not be regular: Sum e = 26 and the in-degrees can be 24..49 (e in [-1, 23]). The pair counts are forced only in total (sum D_P = 16237 + S/2) and not individually. The analogue of the Wilder identity, sum (k-5)(U-k) >= 0 with a constant U, is tight at N = 47 only because U = 11 = max D_P. At N = 52 the mean is 5.76 and the largest possible k is not bounded by 8 or 9 in any identity I have, so the [5,7] test (L2) is the only tight-looking inequality, and it is not an equality in general.

### L6. Decisive fact, and what it means for F1-only methods

Let G = the set of N for which an F1-tournament exists. Then (i) G does not contain any N <= 51 (chain), (ii) every S_4 tournament is F1 so f(4) >= min G, and (iii) f(4) <= 67 (QR_67). So min G is between 52 and 67.

- **Decisive fact (for this lane):** whether 52 is in G. Equivalently: is there any tournament on 52 vertices with all triples having >= 5 dominators?
- If 52 is not in G (nonexistence), then **f(4) >= 53 follows at once** (T1), and the proof is an F1-only argument, which is the route the swarm has been taking.
- If 52 is in G, then every F1-only argument for T1 is dead (it would prove a false statement), and T1 needs the full S_4 condition on 4-sets, e.g. the claim L11 of round 2 (common in-neighbour inside R for each pair), which is not F1.
- So "can an F1-only method still work?" has the answer: **yes if and only if F1 at 52 is impossible.** There is no third option. In particular F1-nonexistence at 52 is a strictly stronger statement than T1 (it implies T1, and T1 does not obviously imply it), so it is not easier than T1 in the logical sense. Its hypotheses are weaker, though, which is why the existing chain could be run with F1 alone.

### L7. Verdict

**UNDECIDED.** Reasons:
- Second-moment and first-moment constraints (L1, L2) do not exclude F1 at 52. In the balanced case they force some triple with k >= 8 (so they are binding only in the near-balanced configurations), and for unbalanced profiles allowed by Lemma B, Claim Q and Lemma V they are satisfied with room (example: profile (-1)x5, (1)x31, (0)x16 has margin 559 in (L2.3)).
- The third-moment identity sum C(k,3) = sum C(l,3) (l = |D+(Y)|, k + l = L_Y, with L_Y not constant) was not solved; the swarm's round-2 analysis reports it as the blocking point (BRIEF section 9).
- The one structured family I could set up (Z_17 with a fixed vertex, forced shape in L4) is forced to have inf beat exactly one orbit, and the interval choice refutes it (k = 0). No algebraic candidate was found.

Verdict: undecided. I do not claim existence or nonexistence.

### L8. Hand checks of the numbers used above
- C(52,3) = 22100; C(52,2) = 1326. Binomials used: C(25,3) = 2300, C(26,3) = 2600, C(24,3) = 2024, C(27,3) = 2925, C(23,3) = 1771, C(12,3) = 220, C(13,3) = 286.
- Balanced: M1 = 26*2600 + 26*2300 = 67600 + 59800 = 127400; 127400/22100 = 5.764706.
- M2 >= 988*220 + 338*286 = 217360 + 96668 = 314028; 2M2 = 628056; 11M1 - 35*22100 = 1401400 - 773500 = 627900; 627900 < 628056.
- Variance route: 2M2/22100 = 28.41882; 5.764706^2 = 33.23184; Var >= 28.41882 + 5.764706 - 33.23184 = 0.95169 > 0.94464 = 0.764706*1.235294.
- h values: h(-1) = 11*2925 - 66 = 32109; h(0) = 11*2600 = 28600; h(1) = 11*2300 - 66 = 25234; h(2) = 11*2024 - 264 = 22000. Balanced sum 26*28600 + 26*25234 = 743600 + 656084 = 1399684; required 1399840.
- Profile (-1)x5, (1)x31, (0)x16: 5*32109 + 31*25234 + 16*28600 = 160545 + 782254 + 457600 = 1400399; margin 559.
- Candidate degrees: 17*76 + 34 = 1292 + 34 = 1326 ✓. Index sets for the triple {(2,0),(2,6),(2,12)}: {-8..-1} = {9..16}; {-2..5} = {15,16,0,...,5}; {4..11}. Their intersection is empty. O_1-part: {9..16,0} cap {15,16,0..6} = {15,16,0}, cap {4..12} = empty.

## Hand checks of the numbers (summary)
All numbers above were displayed and re-checked once. The only nontrivial step still open is the third moment (not attempted beyond the identity).

<!-- END -->
