# R2-CASEA: Case A (no tight pair) for F1-tournaments on N = 52

## Status
- Stage: finished for this lane (24 Oct 2026). Verdict: PARTIAL. Case A is NOT shown impossible.
- Proved by hand (W1-W3, W7): Case A basics; head identity (H); tail identity (T) with global check; at an e=0 vertex v, its in-neighbourhood is 12-regular, E_{N+(v)} >= 13; balanced Case A forces f(v) >= 13 on V_0, the mixed x-mass is 13, D1 + D0 = 325 and D1 in [162.5, 318.5] (a score-variance window for T[V_1]).
- Dead ends: H-count and O-count of F1 on triples (W4, W5) give only lower bounds that hold with room; the e=0 vertex degree budget (W6) has large margin.
- Open: balanced Case A (all e in {0,1}, all lambda >= 12) with T[V_1] score sequence in the window of W7 and x-weights as in W7(viii). Non-balanced Case A (some e >= 2) not analysed beyond W1-W3.

## Plan
1. Read BRIEF.md sections 0-10 (rules, notation, proved facts, dead ends).
2. Read r1_NO-Z section 0, r1_DUAL sections 1, 3, 6, r1_MOM-EXACT A.1-A.2, r1_MOM-BALANCED section 4, r1_AUDIT-52-B section 6.2.
3. Re-derive the head identity and the pair-sum identity (sum over pairs of (D_P - 12) = 325 + S2/2) from the definitions.
4. Re-derive the universal triple identities (L_Y, sum C(k,3) = sum C(l,3), sum C(k,2) = sum C(c_P,3)).
5. Attempt a contradiction in Case A: (a) all e(v) >= 0, sum e = 26; (b) all D_P >= 12; (c) identities above.
6. Record every computation, dead end, and the smallest open configuration.

## Working notes

### W1. Case A basics (re-checked from the definitions)
- Case A hypotheses: T is an F1-tournament on 52 vertices with no tight pair. Then lambda_P := |D(P)| >= 12 for every pair (F2 gives >= 11, and 11 is excluded). x_P := lambda_P - 12 >= 0.
- e(v) >= 0 for all v (Lemma B plus Claim Q: e = -1 forces tight pairs). sum e = 26. Let S2 = sum e^2 >= 26 (equality iff all e in {0,1}).
- Head identity (V2), re-derived: for each v, the in-neighbourhood N-(v) has d-(v) = 25 + e(v) vertices. For a in N-(v), the in-degree of a inside T[N-(v)] is |N-(a) cap N-(v)| = lambda_{av}. The in-degrees in a tournament on m vertices sum to C(m,2), so
  sum_{a->v} lambda_{av} = C(25+e,2), i.e. sum_{a->v} x_{av} = C(25+e,2) - 12(25+e) = e(25+e)/2.   (H)
- Summing (H) over v: sum_P x_P = (25*26 + S2)/2 = 325 + S2/2 (= 338 when S2 = 26). Checked: 52 vertices, sum (25 e + e^2) = 650 + S2, halved.

### W2. Tail identity (new in this lane, re-derived)
Let v be any vertex and O := N+(v), |O| = 26 - e(v). For b in O: v -> b, so v is in N-(b). The set N-(b) splits as {v}, N-(b) cap N-(v) (size lambda_{vb}), and N-(b) cap O (size d-(b) - 1 - lambda_{vb}). Summing over b in O, the in-degrees inside T[O] total C(|O|,2):
  sum_{b in O} (d-(b) - 1 - lambda_{vb}) = C(26-e,2).
With d-(b) = 25 + e(b): sum_{b in O} lambda_{vb} = sum_{b in O}(24 + e(b)) - C(26-e,2).
So sum_{b in O} x_{vb} = sum_{b in O} (12 + e(b)) - C(26-e,2) = 12(26-e) + E_O - (26-e)(25-e)/2 = (26-e)(e-1)/2 + E_O,
where E_O := sum_{b in N+(v)} e(b).   (T)
Check with e = 0: 26*12 + E_O - 325 = E_O - 13.  Check with the sum over v: sum_v (T) equals sum_P x_P only if sum_v of sum_{b in N+(v)} x_{vb} equals each pair counted once (it is counted once, from its tail). Consistency: sum_v [(26-e_v)(e_v-1)/2 + E_{N+(v)}] = sum_v (26-e_v)(e_v-1)/2 + sum_b e_b d-(b) = [sum_v (26 e - 26 - e^2 + e)/2] + sum_b e_b(25+e_b) = (27*26 - 26*26... ) -- computed below as a check.
  Hand check: sum_v (26-e)(e-1)/2 = (1/2) sum_v (-26 + 27 e - e^2) = (1/2)(-1352 + 702 - S2) = (-650 - S2)/2 = -325 - S2/2. And sum_b e_b(25+e_b) = 650 + S2. Total = 325 + S2/2 = sum_P x_P. CONFIRMED (so (T) is consistent with (H) globally).

### W3. Consequences for a vertex of excess 0 (Case A)
Let v have e(v)=0. Put H := N-(v) (25 vertices), O := N+(v) (26 vertices), E_H := sum_H e, E_O := sum_O e, so E_H + E_O = 26.
(a) By (H): sum_{a in H} lambda_{av} = 300 and each lambda_{av} >= 12, so lambda_{av} = 12 for all a in H. Hence T[H] has all in-degrees 12: T[H] is a 12-regular tournament on 25 vertices. (Solid.)
(b) By (T) with e=0: sum_{b in O} x_{vb} = E_O - 13 >= 0, hence **E_O >= 13 and E_H <= 13**. (Solid.)
(c) For a in H: d-(a) = 25+e_a = |N-(a) cap H| + |N-(a) cap O| + [v->a] = 12 + |N-(a) cap O| + 0, so |N-(a) cap O| = 13 + e_a and |N+(a) cap O| = 13 - e_a. (Solid.)
(d) Triples {v,a,b}, a,b in H: v is beaten by a and b, so the triple is transitive (sigma = 1). Its dominators are exactly codeg_H(a,b) := |N-(a) cap N-(b) cap H| >= 5 (F1). Its outside-dominated set is N+(a) cap N+(b) cap O, and the universal identity gives L_{vab} = lambda_{ab} - e_a - e_b. Check: lambda_{ab} = codeg_H(a,b) + |N-(a) cap N-(b) cap O|, and with x := |N-a cap N-b cap O|, w := |N+a cap N+b cap O|, the counts x+y = 13+e_a, x+z = 13+e_b, x+y+z+w = 26 give w = x - e_a - e_b. So codeg_H + w = lambda_{ab} - e_a - e_b, matching. (Solid, a consistency check, adds no restriction.)

### W4. Counting inside H (dead end, no contradiction)
Count pairs (Y, w) with Y a triple inside H and w a dominator of Y, i.e. Y in N+(w). Dominators in H contribute sum_{w in H} C(|N+(w) cap H|,3) = 25 * C(12,3) = 5500 (T[H] is 12-regular). Dominator v contributes 0 (v beats nothing in H). A dominator w in O contributes C(g_w,3), g_w := |N+(w) cap H| (sum_O g_w = 351 - E_O, because the arcs from O into H number sum_{a in H} |N-(a) cap O| = 25*13 + E_H = 325 + E_H = 351 - E_O).
F1 on the 2300 triples of H: 5500 + sum_{w in O} C(g_w,3) >= 5*2300 = 11500, i.e. sum_O C(g_w,3) >= 6000.
Hand check: with 26 integers g_w, sum g_w = 351 - E_O >= 325 (since E_O <= 26), the minimum of sum C(g,3) is at the balanced split, 13*C(12,3) + 13*C(13,3) = 13*220 + 13*286 = 6578 when the sum is 325 (and larger otherwise). 6578 >= 6000.
DEAD END: the inequality holds with room (margin 578), so the H-count gives no contradiction. The upper-bound side (which would be needed) is not supplied by this count.

### W5. Counting inside O (dead end)
Triples Y inside O = N+(v): dominators are v (contributes C(26,3) = 2600), vertices a in H (contribute C(|N+(a) cap O|,3) = C(13 - e_a, 3)), and vertices w in O (contribute C(d+_O(w),3), with sum over O of d+_O = 325). F1 gives 2600 + sum_H C(13-e_a,3) + sum_O C(d+_O(w),3) >= 13000. This is again a lower bound; with the balanced minimum 6578 on the O-part it holds with room. DEAD END for the same reason.

### W6. Other exact counts tried (dead ends)
- Vertex-level budget (C9) at a vertex v with e_v=0: sum_{Y contains v} k(Y) = sum_{w in H} C(25-e_w,2) = 7500 - 24.5 E_H + S2_H/2 (S2_H := sum_H e^2). With E_H <= 13 this is always >= 6375 (needed for F1 on the 1275 triples through v). Margin large. DEAD END.
- The pair-sum identity and the L-variance identities of MOM-EXACT/MOM-BALANCED: these need the full balanced data (e in {0,1}) to become rigid, and in Case A with general e they carry the extra term S2. Not closed here.

### W7. Balanced Case A (all e in {0,1}): reduction to a score-sequence window (re-derived, no lambda in {12,13} assumed)
Let V_0 = {e=0}, V_1 = {e=1}, |V_0| = |V_1| = 26. For v in V_i put f(v) := |N+(v) cap V_1|.
(i) Mixed arcs: V_0->V_1 has sum_{V_0} f = 351 arcs, V_1->V_0 has 325 arcs (out-degrees: 26*26 = 676 = 325 + 351).
(ii) By (T): for v in V_0, sum over out-arcs of x = f(v) - 13 >= 0 (Case A), so **f(v) >= 13 for every v in V_0**, and the total x on V_0->V_1 arcs is sum_{V_0}(f-13) = 351 - 338 = 13. By (T) for v in V_1: sum over out-arcs of x = f(v). By (H): every in-arc of a vertex of V_0 has x = 0, so all x lives on arcs with head in V_1.
(iii) Cyclic triples through an arc a->b equal d-(a) - lambda_{ab} = 13 + e_a - x_{ab} (re-derived from |N+(a) cap N+(b)| = 1 + lambda - e_a - e_b). Counting cyclic triples with j vertices of V_1 (j = 1,2 have exactly two mixed arcs): 2(c_1+c_2) = 13*351 + 14*325 - 13 = 9100, so c_1+c_2 = 4550 and c_0+c_3 = 5850 - 4550 = 1300. (Uses only the mixed x-mass 13.)
(iv) Transitive triples inside V_1 = sum_{V_1} C(f,2); inside V_0 = sum_{V_0} C(26-f,2). Hence sum_{V_1} C(f,2) + sum_{V_0} C(26-f,2) = 5200 - 1300 = 3900.
(v) Expanding with sum_{V_1} f = 325 and sum_{V_0}(26-f) = 325 gives sum_{V_1} C(f,2) = D1/2 + 1868.75 and sum_{V_0} C(26-f,2) = D0/2 + 1868.75, where D1 := sum_{V_1}(f-12.5)^2 and D0 := sum_{V_0}(f-13.5)^2. Therefore **D1 + D0 = 325** (general, Case A balanced).
Hand check of (v): F1 + F0 = 2*1868.75 + (D1+D0)/2 = 3737.5 + 162.5 = 3900 when D1 + D0 = 325. Integer minimum check: the balanced split gives 13*66 + 13*78 = 1872 per class, total 3744, and 3900 - 3744 = 156 = (325 - 13)/2, where 13 = 6.5 + 6.5 is the minimum of D1 + D0.
(vi) On V_0: u_v := f(v) - 13 >= 0 (integers) with sum u = 13. Then sum u^2 >= sum u = 13 (since u^2 >= u for integers >= 0), so D0 = sum (u-1/2)^2 = sum u^2 - 6.5 >= 6.5. Also sum u^2 <= (sum u)^2 = 169, so D0 <= 162.5. Hence **D1 in [162.5, 318.5]** (D1 = 325 - D0).
(vii) Score window for T1 := T[V_1] (26-vertex tournament with out-degrees f): sum_{V_1} f^2 = D1 + 4062.5, so **sum f^2 in [4225, 4381]**, versus the regular value 4069. So T1 must have a strongly non-regular score sequence. Its cyclic count c_3 = 2600 - F1 = 731.25 - D1/2 lies in [572, 650].
(viii) Internal weights: write y := x - 1 >= -1 on arcs of T1. Out-sums: sum over out-arcs of y = 0 at every v in V_1 (from (ii)). In-sums: sum over in-arcs of y at w = f(w) - 12 - omega_w, where omega_w := x-mass of mixed in-arcs at w >= 0, sum_w omega_w = 13.
DEAD END so far: (vii) and (viii) are consistent with all counts used; no contradiction yet. This is exactly the open configuration of NT-B (r1_DUAL section 6(e)), now stated with its exact constraints.

### W8. Status of the lane
- Proved (by hand, every step written): W1, W2 (tail identity and its global check), W3 (a) (b) (c) (d), W4 and W5 as valid but non-contradictory counts, W7 (i)-(vii).
- Not proved: that Case A is impossible. The open set is contained in: balanced Case A with D1 in [162.5, 318.5], i.e. T1 has score variance in a window, plus x-weights as in (viii). Non-balanced Case A (some e >= 2) is not analysed in this lane beyond W1-W3.

<!-- END -->
