# Ledger

Chronological record. Later entries are appended by `research/orchestrator.py`. An entry labelled "reading" is not a proof.

## 2026-10-23 — baseline inspection

The workspace already contained a long investigation of Erdős 902. Nothing in `proof/` was modified. The zip archives described in `FILE_INDEX.md` are not in the workspace. `proof/swarm/` contains only `BRIEF.md`; the 23 October swarm had been briefed and had not written its reports here.

**Problem.** Exact statement and the source limitation are in `research/PROBLEM.md`. The indexed erdosproblems.com text still asks to estimate \(f(n)\). The indexed proof-claims snippet reports no submitted proof.

**Reproduced computation.** `python proof/verify_proof.py` was rerun from this workspace. Log: `logs/verify_proof_rerun_20261023.out`. Exit 0. "Total time 66s. Failures: 0." That rerun covers V1–V7 of `proof/ERDOS902_PROOF.md`: Paley profiles, the arithmetic of Theorem A, the Theorem B comparison through \(n = 2000\), \(c^\ast\) to 40 digits, the Theorem D table, and the Claim L realisation. It does not read the hand proof of \(f(4) \ge 52\).

**Proved in this baseline, unconditionally for Lemma S1 and under degree hypotheses for Lemma I.** See `research/LEMMAS.md`. Lemma S1: every tournament on 52 vertices has \(\sum |D(P)| \ge 16250\), so some pair has at least 13 dominators. Lemma I: the tight-pair excess identity \(\sum(q_y-5) = 6N-298-J\).

**Open bottleneck.** `proof/F4_GE_52_HAND_PROOF.md` contains a complete-looking argument that \(J \ge 3\) for a tight pair at \(N = 51\), and a short paragraph extending that bound to every order. `proof/N52_TIGHT_PAIRS.md` cites the extension to start its claim \(J \ge 5\) at \(N = 52\). The extension does not re-derive `(R1)` outside Lemma P. That is the first obstacle for \(f(4) \ge 53\). It is not a counterexample to the bound.

**Strong claim versus \(f(4)\).** The 20 October note claims every tournament on at most 51 vertices has a triple with at most 4 dominators. That implies \(f(4) \ge 52\). A tournament on 47–51 vertices with every triple dominated at least five times would kill that proof. It would kill \(f(4) \ge 52\) only if it also had \(S_4\).

**Not settled.** The order of \(f(n)\). The exact value of \(f(4)\). Whether the hand argument for \(f(4) \ge 52\) is correct. Whether an \(S_4\) tournament on 52 vertices exists.

**Exhausted approach keys, not to be reopened:** `claim-L-single-pair-link`, `one-level-counting-past-cstar`, `two-stage-averaging-second-log`, `random-cayley-beat-erdos-upper`, `n51-local-milp-certificates`, `wrong-direction-covering-local48`.

**Next actions.** Run the controller's first round: exact Paley profiles through order 67; an independent reading of the every-order paragraph; a re-derivation of the doubly regular order-51 moment argument; a search for a tournament on 47–51 vertices with minimum triple-dominator count at least 5.

## 2026-10-23 — controller initialised

solved remains false. Seed tasks are pending.

## 2026-10-23T16:36:21.176927+00:00 — R1-E-checks ingested

Source: compute. Result: computed. Verification: reproduced_by_orchestrator.

Claim: Lemma S1 and Lemma I match the arithmetic in LEMMAS.md, the printed numbers in F4_GE_52 section 6 match, and the Paley profiles of orders 7, 19 and 67 match the profiles previously computed by proof/verify_proof.py. In the Paley tournament of order 47 the minimum of |D(Y)| over triples Y is 4, attained, and the minimum over 4-sets is 0. The sentence 'every tournament on at most 51 vertices has a triple with at most 3 dominators' is therefore false. The strong claim with 4 in place of 3 survives this example, and this tournament does not have S_4.

Weakness: All Paley tournaments of orders 7, 11, 19, 23, 31, 43, 47 and 67 were scanned exactly. This is not a search over all tournaments of those orders. Orders below 47 cannot meet the triple condition for S_4, by the Szekeres bound, so a Paley counterexample to the strong claim would have to be order 47.

Next: If a Paley candidate exists, verify that witness by hand. Otherwise use the profiles as negative Paley evidence only.

## 2026-10-23T16:49:51.072337+00:00 — R1-A-literature ingested

Source: file. Result: computed. Verification: unreviewed.

Claim: Bibliographic classification only, checked on 23 October 2026. Erdős problem 902 is not solved. On the opened problem page the stated results stop at f(1)=3, f(2)=7, Erdős's 2^{n+1}-1 ≤ f(n) ≪ n^2 2^n, and Szekeres–Szekeres's f(3)=19 and n 2^n ≪ f(n), with zero proof claims. The finite window 48 ≤ f(4) ≤ 67 is supported by sources opened outside this workspace: Reid, McRae, Hedetniemi, and Hedetniemi (2004) prove that property S_4 requires at least 48 vertices, and Graham–Spencer (1971) state that the Paley tournament on 67 vertices has the property. The claims f(4) ≥ 51, f(4) ≥ 52, and c* ≈ 0.76950321915 were not present in any source opened in this pass. They are written in this workspace. This is not a proof that those three strings occur nowhere else in the literature.

Weakness: ['The full texts of Erdős 1963 and Szekeres–Szekeres 1965 were not opened. Their general bounds are website attributions plus quotations in later papers that were opened.', 'Reid and Brown 1972, cited for the last step of Corollary 7, was not opened. Moon 1968 was not opened. The Er82e target was not opened.', "Graham–Spencer formulas in the Cambridge extraction are OCR-damaged. The prose sentence that T_67 has property P_4 was readable. The strictness of the sign in 'f(4) > 47' was not checked against a clean glyph.", "Jeffries's preprint says the classical bounds remain the best known and have been unimproved for 60 years, while the 2004 paper opened here already has the stronger finite bound of 48. That is a gap in the preprint's survey, not a retraction of Corollary 7.", 'Bozóki attributes the conjecture f(4)=67 to Graham–Spencer. The sentence read in Graham–Spencer is that T_67 might be minimal.', "Web search and the opened corpus did not surface f(4) ≥ 51, f(4) ≥ 52, or 0.76950321915. That does not prove those strings are absent from every unopened paper, repository, or paywalled scan. Semantic Scholar's empty response is not a negative search.", 'The Wilder Lean project was read from the README and one markdown note. It was not rebuilt, so the kernel check claimed there is UNVERIFIED.', 'The cursor-ide-browser server did not register. Page text comes from WebFetch and publisher extractions, not from a rendered browser snapshot.', "OpenAlex's hit for the Szekeres title was Yair Caro and Adriana Hansberg, Directed domination in oriented hypergraphs (2019), not the 1965 paper. It was not used. The broad arXiv tool from the earlier session was not rerun and those unrelated papers are not cited."]

Next: Read the 1963 and 1965 Gazette articles and resolve the tag Er82e before quoting their theorems as checked. Keep f(4) ≥ 51, f(4) ≥ 52, and c* ≈ 0.7695 inside this workspace until a source that actually contains them is opened. Do not describe the opened Wilder files as a proof that f(4) ≥ 49.

## 2026-10-23T16:49:51.095765+00:00 — R1-B-theorem5 ingested

Source: file. Result: proved. Verification: unreviewed.

Claim: Every doubly regular tournament on 51 vertices has some triple with at most 4 dominators. Here doubly regular means that every in-degree and every out-degree is 25, and every two distinct vertices have exactly 12 common in-neighbours.

Weakness: The proved statement stops at the doubly regular parameters. It does not show that every tournament on 51 vertices has a triple with at most 4 dominators, and it does not show f(4)≥52. In the hand proof those conclusions use Theorem 1 and Corollary 4, which were not re-derived. Erdős problem 902 is not solved: the order of f(n) is untouched, and so is the upper bound f(4)≤67. The argument also does not decide whether a tournament with these parameters exists, and it does not name the exact minimum, only that the minimum is at most 4.

Next: Re-derive Theorem 1 and Corollary 4, the reduction from an arbitrary S_4 tournament on 51 vertices to the doubly regular parameters. Until that reduction is checked, the triple bound in Theorem 5 does not give f(4)≥52.

## 2026-10-23T16:49:51.119148+00:00 — R1-D-counterexample ingested

Source: file. Result: disproved. Verification: unreviewed.

Claim: The sentence 'every tournament on at most 51 vertices has a triple with at most 3 dominators' is false. The Paley tournament of order 47 is a counterexample: the minimum of |D(Y)| over its 16215 triples is 4, attained by {0,1,3}, whose dominators are 23, 41, 44 and 46. The strong claim in proof/F4_GE_52_HAND_PROOF.md, whose bound is 4 rather than 3, is consistent with this tournament, because that triple has exactly 4 dominators. The same tournament has undominated 4-sets, including {0,1,3,38}, so it does not have S_4 and does not decide whether f(4) >= 52.

Weakness: This kills the strengthening with 3. It leaves the strong claim with 4 untouched: 4324 triples in this tournament have exactly 4 dominators, so the tournament is not a counterexample to that claim, and a failed search is not evidence that the strong claim is true. The count over all triples is a machine enumeration, repeated with two implementations that agreed; the four dominators of {0,1,3} were also listed by hand from the residues. The Paley profiles of orders 7, 11, 19, 23, 31, 43 and 67 were taken from research/AGENT_TASKS/R1-E-checks.report.json and were not re-enumerated. In that report their minimum numbers of triple dominators are 0, 0, 1, 1, 2, 3 and 6, so none of the orders at most 51 meets the condition that every triple has at least 5 dominators. Orders 48, 49, 50 and 51 have no Paley tournament. No other construction on 47-51 vertices was examined. The optional search for an integer pattern of (q_y) and (j_r) at N = 52 with J <= 2 was not carried out. Claim L was not reopened.

Next: A counterexample to the strong claim would be a tournament on 47, 48, 49, 50 or 51 vertices, other than the Paley tournament of order 47, in which every triple has at least 5 dominators. It would falsify f(4) >= 52 only if that same tournament also had S_4. Paley order 47 is closed for this purpose.

## 2026-10-23T16:49:51.140253+00:00 — R1-G-audit-every-n ingested

Source: file. Result: proved. Verification: unreviewed.

Claim: The paragraph in proof/F4_GE_52_HAND_PROOF.md that begins 'Theorem 1 holds for every N, not only N = 51' is an incomplete proof. Its first unjustified inference is the sentence asserting that (*), (R1)-(R3) and the rounding lemma hold verbatim at every order once gamma_u is redefined as the number of vertices y with q_y >= 9 and u not in Q_y. The conclusion of that paragraph is true by the argument written in this report, which is the auditor's proof and not a repair declared to be the printed text: in every S_4 tournament, on any number of vertices, every tight pair P satisfies J(P) >= 3. This verdict covers that every-order claim. It does not certify the N = 51 write-up of Theorem 1, it does not prove J >= 5 on 52 vertices, and it does not solve Erdős 902.

Weakness: The status proved applies only to the argument written here. The printed paragraph remains incomplete, and the sentence that Steps 3-5 are unchanged is still not a citation of a matching text: Step 3 in the N = 51 write-up names a single vertex y*. The following paragraph of the same note, lines 213-218, claims the in-degree-25 structural fact for an arbitrary tight pair with no bound on J. Its parenthetical proof invokes the rounding lemma as written, which assumes the N = 51 profile, and that paragraph was not given a proof in this report. Sections 3 and 4 of proof/N52_TIGHT_PAIRS.md, which exclude J = 3 and J = 4 at N = 52, were not audited. The lower bound s >= 7 - x is weak once x >= 8; the argument removes every 6-vertex before the final comparison, so that weak range is not where the contradiction is drawn. No enumeration was run.

Next: Audit sections 3 and 4 of proof/N52_TIGHT_PAIRS.md, the exclusions of J = 3 and J = 4 at N = 52 that sit on top of J >= 3. Separately, supply a proof of the in-degree-25 structural statement in the paragraph after the every-order claim, the one that allows q_y in {7, 8} and does not assume J <= 2.

## 2026-10-23 — orchestrator review of round 1

R1-E-checks was reproduced by the controller. R1-D's disproof of the sentence with 3 in place of 4 was recomputed independently: Paley order 47, triple {0,1,3}, dominators 23, 41, 44, 46, minimum 4, undominated 4-set {0,1,3,38}. The histogram in that report was not recomputed.

R1-G is accepted as Lemma J after a check of the steps the printed paragraph skipped. Verification is skeleton_checked, not a second blind write-up. R1-B agrees with the inclusion-exclusion and with p=6375. Neither report proves f(4) >= 52.

R1-C is retargeted from J <= 2 to the J = 3 and J = 4 case split at N = 52. solved remains false.

## 2026-10-23T17:26:36.531341+00:00 — R1-C-n52-j-le-2 ingested

Source: file. Result: proved. Verification: unreviewed.

Claim: In an S_4 tournament on 52 vertices, every tight pair P satisfies J(P) >= 5. Lemma J supplies J >= 3, and the case analysis below excludes J = 3 and J = 4. Sections 3 and 4 of proof/N52_TIGHT_PAIRS.md are not the proof: the first case that does not follow as printed is section 4, s = 3, which treats partitions of 11 and gives no argument for the partition 5+5 of the excess 10. The bound J >= 5 is the conclusion of the corrected analysis in this report. A tight pair with J >= 5 is still open, f(4) >= 52 is not proved, and Erdős problem 902 is not solved.

Weakness: The status proved belongs to the case analysis written here. The printed section 4, s = 3, does not establish its exclusion, and the s = 4 rows 6+4, 5+5 and 4+4+2 do not follow from the reasons printed beside them. Section 3 follows once 17 is replaced by 22 in the inconsistent s = 2 assignment. Lemma J is an input from the G report and from research/LEMMAS.md; that argument is one author and one checker, and this report does not re-prove J >= 3. Lemma A was rechecked because every appeal to 12 dominators on a pair into V_0 uses it. The comparison J >= 5 does not force four vertices of positive excess: a single vertex of excess 5 meets J = 5 with s = 1, and sections 5 and 9, which treat that shape, were not audited. No tournament was enumerated. A tight pair at order 52 remains open, f(4) >= 52 is not proved, and Erdős problem 902 is not solved.

Next: Audit section 5 of proof/N52_TIGHT_PAIRS.md, the claim that J = 5 forces s >= 4, and then section 9, the claim that s <= 3 is impossible for J >= 6. Those two sections are what turn J >= 5 into the stronger statement that at least four dominators have in-degree greater than 25. A second reading of the corrected J = 3 and J = 4 split is the check this report still needs.

## 2026-10-23T17:26:36.552338+00:00 — R1-F-reformulation ingested

Source: file. Result: proved. Verification: unreviewed.

Claim: A tournament on 52 vertices has property S_4 if and only if, for every vertex v, the subtournament induced by the in-neighbourhood of v has property S_3. Equivalently, no tournament on 52 vertices has S_4 if and only if every tournament on 52 vertices has at least one vertex whose induced in-neighbourhood fails S_3. Iterating the same identity, S_4 fails if and only if there is a sequence of m ≤ 4 vertices in which each later vertex beats every earlier one and no vertex beats the whole sequence. The equivalence does not show that either side is true, and it does not solve Erdős problem 902.

Weakness: The status proved applies only to the equivalence. Neither side has been established: the report does not show that every tournament on 52 vertices has a vertex whose in-neighbourhood fails S_3, and it does not show that an S_4 tournament on 52 vertices exists. Erdős problem 902 is not solved. The order of f(n) is untouched, and so is the upper bound f(4) ≤ 67. The identity holds at every order at least 4, so the number 52 plays no special role. Granting the classical theorem f(3) = 19, which is not re-proved here, would dispose only of a vertex of in-degree at most 18. Every remaining case has all in-degrees at least 19, and an in-neighbourhood of that order can carry S_3. The sequence form allows length strictly less than 4. It is not the assertion that some transitive 4-set is undominated; a shorter transitive dominating set need not extend to a transitive dominating 4-set. Lemma S1, the tight-pair bound J ≥ 3, and the case split J = 3, 4 were not used.

Next: Prove that every tournament on 52 vertices has a vertex whose induced in-neighbourhood fails S_3. With the classical bound f(3) = 19 taken as known, any vertex of in-degree at most 18 is already such a vertex, and the remaining case is minimum in-degree at least 19. That case is not treated here.

## 2026-10-23T17:26:36.573340+00:00 — R1-H-strategy ingested

Source: file. Result: inconclusive. Verification: unreviewed.

Claim: The obstacles that block a proof, in the order they should be worked, are: Corollaries 2–4 at order 51, which are what would let the re-derived Theorem 5 forbid an S_4 tournament on 51 vertices; Theorem A, which is what would then exclude orders 49 and 50 and give f(4) ≥ 52; the order-52 branch in which every pair has at least 12 dominators, which is what blocks a proof that no S_4 tournament has 52 vertices; and sections 5 and 9 of the order-52 note, which are what would turn a tight pair into four dominators of in-degree greater than 25. The J = 3 and J = 4 audit is already written in R1-C and stays in progress until an independent check finishes. Erdős problem 902 is not solved.

Weakness: This is a strategy. It proves no bound and it exhibits no tournament. J ≥ 5 remains conditional until someone other than the author of R1-C checks that report, including its Lemma A; the enumeration with 18 and 220 configurations is not that check. The two swarm files under proof/swarm/ are uningested sketches. Tasks R2-F-min-12 and R2-I-four-positive can return inconclusive without touching the order-51 gates. Section 8, the classical unopened papers, and the factor-n gap are left out of this round on purpose: the first is the reserve behind rank 4, and the other two block citation and the asymptotic estimate rather than the written finite implications. Erdős problem 902 is not solved, and f(4) ≥ 52 is not proved.

Next: Dispatch the four round-2 tasks and leave the J = 3 and J = 4 audit in progress. R2-B-n51-reduction, approach key n51-corollaries-2-4-from-lemma-J: re-derive Corollaries 2–4 from Lemma J. This does not repeat rederive-drt51-third-moment, which assumes the doubly regular parameters and never derives them. R2-G-theorem-a, approach key theorem-a-orders-49-and-50: read Theorem A at orders 49 and 50. This does not repeat exact-identities-and-paley-profiles, which matched numbers and did not read that counting. R2-F-min-12, approach key n52-excess-338-minimum-12-pairs: decide the order-52 branch in which every pair has at least 12 dominators. This does not repeat rederive-drt51-third-moment, where k plus the common out-neighbour count is constant. R2-I-four-positive, approach key n52-net-excess-invariant-four-positive: decide the four-positive-dominator claim from the net-excess invariant and sections 5 and 9. This does not repeat the J = 3 and J = 4 partition audit already written in R1-C.

## 2026-10-23 — case tree for J=3 and J=4

research/compute/audit_j34.py enumerated the heavy-vertex placements used in R1-C. J=3: 18 configurations, 0 survivors (pair-sum 1, exceeds-Ex 5, lambda 12). J=4: 220 configurations, 0 survivors (pair-sum 1, exceeds-Ex 19, lambda 181, below-12 19). The enumeration assumes Lemma A, at most 4 common in-neighbours, and the pair and triple identities. It supports J>=5 for a tight pair at order 52. A tight pair with J>=5 remains open. f(4)>=52 remains unproved. solved remains false.

proof/swarm/r1_AUDIT-52-B.md stops in section 3. The uniform proof announced in its introduction is not in the file. proof/swarm/r1_AUDIT-51.md claims the chain through f(4)>=52 and has not been accepted.

## 2026-10-23 — line check before round 3

The printed arc count in Corollary 3 is the right one. Each x in N^-(v) uses one out-arc on v, so sum |D_z| = sum (d^+(x)-1). research/compute/corollary3_count.py checked this on 20 tournaments of order 7 and 5 of order 51. The subtraction equals |A| in every trial.

Theorem A, Corollary 2, the diagonal-dominance step in Corollary 3, Corollary 4, and the arithmetic of Theorem 5 were read line by line. Promotion of f(4) >= 52 is withheld until a hostile pass returns. solved remains false.

## 2026-10-23T17:56:54.548775+00:00 — R3-C-four-positive ingested

Source: file. Result: conditional. Verification: unreviewed.

Claim: Assume J >= 5 for every tight pair in an S_4 tournament on 52 vertices, as proved in research/AGENT_TASKS/R1-C-n52-j-le-2.report.json and not re-proved here. Then every such pair has at least four dominators of in-degree greater than 25. Sections 5 and 9 of proof/N52_TIGHT_PAIRS.md reach that conclusion, but they do not follow as printed. The first gap is section 5, partition 6+3, on the degree shape (2, 2, 1): the pair counts are 18, 13 and 13, so the printed pair with 8 dominators does not occur. Section 9 omits the empty excess at J = 14 and several degree splits, and two printed budgets are wrong. The repaired case analysis below leaves no configuration with s <= 3. A tight pair with s >= 4 remains open, f(4) >= 52 is not proved, and Erdős problem 902 is not solved.

Weakness: The status conditional belongs to the dependence on J >= 5. That bound is the R1-C report, written by the same agent role, and it is unreviewed. This report does not re-prove it, and it does not re-prove Lemma A. Every pair into V_0 is given 12 dominators by Lemma A; if that lemma failed, the pair-sum reduction used here would fail with it. The repaired case analysis is the argument for s >= 4 given those inputs. The printed section 5 does not establish the shape (2, 2, 1) of partition 6+3, and it does not write the placements of partition 5+4. The printed section 9 does not treat J = 14, and the splits and budgets named in the evidence do not follow as written. The introduction of proof/swarm/r1_AUDIT-52-B.md asserts Lemma C and sketches a uniform counting invariant, but the file stops during its section 3, before any such proof. That introduction is not evidence. The labeled enumeration is a check that the same inequalities admit no survivor; it is not a search of tournaments, and it uses the same identities as the case analysis, so it does not insure those identities. A tight pair with four or more positive dominators remains possible. f(4) >= 52 is not proved, and Erdős problem 902 is not solved.

Next: Have a second reader check the repaired placements in section 5, partition 5+4, and the section 9 composition E = 5, j_X = 1, degrees (4, 4), against the pair-sum. The open half of Lemma C is s >= 4: the excess can still sit on four or more dominators, and that regime is what a surviving tight pair at order 52 would have to satisfy.

## 2026-10-23T17:56:54.573810+00:00 — R3-D-case-I ingested

Source: file. Result: proved. Verification: unreviewed.

Claim: At order 51, no integer parameters meet the identities used in Corollary 3 of proof/F4_GE_52_HAND_PROOF.md in case (I) while every tight pair has J at least 3. The identity that blocks the search is sum_z h_z = 26 + |N^-(v) intersect Z| - W(v). Under those hypotheses the right-hand side is at most 25, while the Gram matrix forces at least 26 indices z with h_z at least 1. Erdős problem 902 is not solved, and this comparison does not prove f(4) >= 52.

Weakness: The status proved applies to the emptiness of this integer box under the hypotheses Corollary 3 cites and under J >= 3 on every tight pair. Claim Q, Lemma T, (F1), (F2), and the minimum in-degree 24 are used as constraints, not re-proved. The load-bearing unit is k <= 2 against nullity 26: the excluded point k = 3, W = 3, J = 3 would give sum_z h_z = 26. No tournament was built, and the 551 isomorphism classes of 5-regular tournaments on 11 vertices were not searched. Case (R), the doubly regular moment argument, and orders other than 51 are outside the box. The random check of the arc count covers 8 tournaments of order 51 and 30 of order 7; the identity itself is the double count in the argument. Erdős problem 902 is not solved, and f(4) >= 52 is not a conclusion of this report.

Next: The case (I) integer box is closed under these hypotheses. An independent check can recompute only 26 + k - W at k = 2 and W = 3 against the nullity 50 - 24. The remaining order-51 branch is case (R), which is a different degree pattern.

## 2026-10-23T17:56:54.595848+00:00 — R3-F-order-52 ingested

Source: file. Result: proved. Verification: unreviewed.

Claim: Rerunning at order 52 the argument that an S_4 tournament on 51 vertices is doubly regular, the first bound that becomes inconclusive is Σ_{a in A} e(a) ≤ 2 in Corollary 2 of proof/F4_GE_52_HAND_PROOF.md. At order 51 the arcs from the in-neighbourhood of a vertex of in-degree 23 force that sum to be at most 2, and 2 contradicts J ≥ 3. At order 52 the same count forces the sum to be at most 14, and 14 does not contradict J ≥ 3. The two numbers are 2 and 14. Erdős problem 902 is not solved.

Weakness: The status proved applies to the location of the first transported failure and to the two slack values 2 and 14. It does not disprove minimum in-degree 24 at order 52: the design argument in proof/N52_ATTEMPT.md was left unread beyond its statement that it continues from E ≤ 14, and it was not checked. Lemma J is an input from research/LEMMAS.md and from R1-G; this report does not re-prove J ≥ 3. The comparison with J ≥ 5 uses that bound only as a number, without reopening its case analysis. Corollaries 3 and 4 were not rerun. No tournament was enumerated. Erdős problem 902 is not solved, and f(4) is not evaluated.

Next: Leave the Corollary 2 contradiction at order 52 as inconclusive on the numbers 2 and 14, and do not revive it by the order-23 design count inside this approach. If a separate argument supplies minimum in-degree 24, the next identity to test is the case split Σ_{x not in Z} e(x) = |Z|: at order 51 the sum of e is 0, and at order 52 it is 26, so the transported right side is 26 + |Z|.

## 2026-10-23T17:56:54.618401+00:00 — R3-G-break-52 ingested

Source: file. Result: proved. Verification: unreviewed.

Claim: No tournament on 51 or fewer vertices has S_4, so f(4) >= 52. For A = N^-(v) in Corollary 3, sum_z |D_z| equals sum_{x in A}(d^+(x) - 1). Every inference on the printed path follows. There is no first failing inference and no unfinished block on that path. Erdős problem 902 is not solved.

Weakness: The status proved is the nonexistence of an S_4 tournament on at most 51 vertices, together with the resulting lower bound f(4) >= 52. It is not a solution of Erdős problem 902. The classical upper bound f(4) <= 67 was not re-proved, so this pass does not identify f(4). Order 52 was not considered. Weyl's inequality, Gershgorin's theorem, and Cauchy interlacing are used as standard facts about Hermitian matrices; their hypotheses were checked in the decreasing eigenvalue convention, and they were not re-proved from the characteristic polynomial. The every-order paragraph after Theorem 1 remains an incomplete citation, as previously reported, and the structural sentence about an arbitrary tight dominator of in-degree 25 was not given a separate proof here because Corollary 2, Corollary 3, and Corollary 4 do not use it. No tournament was enumerated.

Next: Leave the bound f(4) >= 52 as checked and unreviewed, and do not record Erdős problem 902 as solved. The next mathematical question is order 52: whether an S_4 tournament there can avoid a tight pair, and whether a tight pair at that order can be excluded. This pass does not start that case.

## 2026-10-23 — f(4) >= 52 recorded, Paley 59 separated

The chain through Theorem 5 was line-checked and rewritten in R3-G-break-52. Case (I) stops because sum h_z = 26 + k - W is at most 25 while the Gram matrix needs 26 positive h_z. The bound f(4) >= 52 is entered in research/LEMMAS.md. Erdős problem 902 stays open. The exact value of f(4) is still only pinned to 52 <= f(4) <= 67.

Paley order 59: quadratic residues give triple minimum 5 on {0,1,7}, dominators 31, 38, 39, 40, 44, and the 4-set {0,1,7,19} is undominated. A triple minimum of 5 does not force S_4.

At order 52 the Corollary 2 slack is 14 rather than 2. The separate counting in proof/N52_ATTEMPT.md section 2, recomputed here, still forbids in-degree 23, using the structural fact for in-degree 25. solved remains false.

## 2026-10-23T19:04:37.699365+00:00 — R4-B-no-tight ingested

Source: file. Result: proved. Verification: unreviewed.

Claim: These hypotheses do not force a triple with fewer than 5 dominators. The handshaking identities admit the integer margin (26, 338, 5): the degree excesses are twenty-six 0s and twenty-six 1s, the pair excesses sum to 338, and every triple in the solution has at least 5 dominators. For this same margin the lower bound is sharp, because the identities also force some triple to have at most 5 dominators. Erdős problem 902 is not solved.

Weakness: The status proved applies to the integer margin (26, 338, 5) and to the sign obstruction that makes 5 sharp for that margin. The solution assigns nonnegative integers to the double-counting equations. It does not construct the arcs of a tournament, so it does not show that a tournament on 52 vertices can have every pair at least 12 dominators and every triple at least 5. The transitive triples were distributed between the two excess classes only so that their number equals 16250; a tournament would have to realise that split inside the out-sets. Other degree sequences, with Σ e^2>26, were not needed: one consistent margin is enough to show that the identities do not force a triple below 5, and it says nothing about those other sequences. The lower bound of 7 dominators on some triple is the balanced-score remark already in proof/N52_TIGHT_PAIRS.md §7; the new comparison is that the same second moment still fits next to a minimum of 5. No appeal is made to a tight pair, to J, or to S_4 beyond the numerical lower bounds in the hypotheses. Erdős problem 902 is not solved, and f(4) is not evaluated. The classical upper bound f(4)≤67 was not re-proved.

Next: Either realise the margin (26, 338, 5) by a tournament, or find a counting identity stricter than the two pair moments and the third-moment symmetry. Those equations allow every triple to have at least 5 dominators and forbid every triple from having at least 6. A pair with 11 dominators is a different branch.

## 2026-10-23T19:04:37.726358+00:00 — R4-C-tight-s4 ingested

Source: file. Result: conditional. Verification: unreviewed.

Claim: Assume a tight pair in an S_4 tournament on 52 vertices with J = 5 and s = 4. Those two bounds are conditional inputs and are not rebuilt. The degree excesses on the four positive dominators are then 2, 1, 1, 1, and the heavy excess is 9. Lemma A, the pair-sum, the triple-excess formula, and c <= 4 exclude every excess partition of 9 other than 6+3. They also exclude 6+3 unless the vertex of q = 8 misses the degree-2 dominator and exactly two of the degree-1 dominators. Name the degree-2 vertex A, the untouched degree-1 vertex B, and the missed degree-1 vertices C and D so that |D({B,C})| = 13. The six dominator counts inside the positive set are then forced: |D({A,B})| = 16, |D({A,D})| = 14, |D({A,C})| = 13, |D({B,C})| = 13, |D({B,D})| = 12, and |D({C,D})| = 12. The same identities force c(A,B) = 4 and c(C,D) = 0, and they admit an explicit common-in-neighbour tuple on the other four pairs. A tight pair with J = 5 and s = 4 remains compatible with these identities. f(4) >= 52 is not proved, and Erdős problem 902 is not solved.

Weakness: The status conditional belongs to the dependence on J >= 5 and s >= 4. The first is the R1-C report and the second is the R3-C report. Both were written in the same agent role, both are unreviewed, and neither is re-proved here. Lemma A is an input from the same source: every pair into V_0 is given 12 dominators and c <= 3 by that lemma. The case analysis excludes the other patterns at J = 5 and s = 4, and it exhibits one pattern that meets the pair-sum, the triple-excess formula, and the per-vertex sum of common-in-neighbour counts. The seven counts from each positive vertex into V_0 were checked only as a list of seven integers at that vertex. They were not realized together inside one 5-regular tournament on 11 vertices. The nonnegative subset counts in the evidence account for the 37 light vertices on V_+ for one common-in-neighbour tuple. They do not assign those vertices inside V_0, and they do not build the tournament. The labeled enumeration is a check that the same inequalities admit no second orbit. It is not a search of tournaments, and it uses the same identities as the case analysis. A tight pair with this pattern, or with J = 5 and s = 5, or with J > 5, remains possible. f(4) >= 52 is not proved, and Erdős problem 902 is not solved.

Next: Test this one pattern against a 5-regular tournament on the eleven dominators, with c(A,B) = 4 and c(C,D) = 0, and against an assignment of the 37 light vertices in O. The same identities at J = 5 and s = 5 have not been run.

## 2026-10-23T19:04:37.754357+00:00 — R4-D-upper ingested

Source: file. Result: computed. Verification: unreviewed.

Claim: For every n from 52 through 66, the forward circular tournaments C_n^+ and C_n^- fail S_4. The undominated 4-set is {0, m, 2m, 3m} with m = floor(n/4). For odd n the two diametral rules define the same tournament; for even n both orientations fail, with this same witness. That half of the claim is a proof. A finite census shows that the Paley tournament of order 67 has no induced subtournament with S_4 on 50 through 66 vertices, the Paley tournament of order 71 has none on 52 through 70 vertices, and the Paley tournament of order 79 has none on 52 through 78 vertices. The Paley tournament of order 83 has none on 52 through 66 vertices. The power-interval tournaments of orders 53, 59, and 61, the cyclotomic tournaments of orders 53 and 61 in each of the two admissible pairs of residue classes, the Jacobi tournaments of orders 55 and 63, thirteen lexicographic products of orders 52 through 66, and all 64 majority products of a tournament on 4 vertices, fail S_4. An undominated 4-set for each of them is recorded in the evidence. The Paley tournament of order 67 has S_4, and this search found no example on fewer vertices, so the upper bound supplied by these families remains f(4) <= 67. Erdős problem 902 remains open.

Weakness: The circular failure is a written proof, and the edge list of each order was checked against it. The argument is special to this connection set. The Paley statements are enumerations. At orders 67, 71, and 79 the independence numbers in the unique-dominator bounds were recomputed by CP-SAT, CBC, CaDiCaL, and a separate backtrack. The equality cases at orders 71 and 79 were rejected by CP-SAT and CaDiCaL, and on one sample set the number of violated clauses equalled a direct count of undominated four-sets. Orders 52 through 60 in QR_79, and orders 52 through 66 in QR_83, are full four-set encodings. Both CP-SAT and CaDiCaL reject them, and the cardinality constraints alone are satisfiable. The independence number 27 at order 83 was not recomputed by the backtrack. The exclusion of orders 52 through 66 in QR_83 does not use that number; the unique-dominator bound there is 68 and does not reach those orders. Orders 67 and 68 inside QR_83 were not searched. The run does not decide whether QR_83 has S_4, because four-sets containing 0 were not part of the empty-dominator count. The caps 49, 51, and 51 at orders 67, 71, and 79 are upper bounds on a proper induced subtournament with S_4. No example of those orders was built. The products C_3[C_13] and C_13[C_3] have order 39, fail S_4, and lie outside the window. Thirty-two of the sixty-four majority bases have a vertex of out-degree 3, and the constant copy of that vertex has in-degree 0 in the product. The other thirty-two bases have maximum out-degree 2 and their products still fail S_4. The abstract at doi 10.5281/zenodo.23269759 describes a Cayley search on the odd-order groups from 47 through 65 and states that the bounds 48 <= f(4) <= 67 are unchanged. That dataset was not executed. The odd-order circular tournaments are single Cayley connection sets, settled here by the gap argument. Even-order circular tournaments and induced Paley subtournaments lie outside that Cayley statement. Paley orders 47 and 59 were not re-censused. One recorded set in each was used to check the edge orientation. The lower bound f(4) >= 52 is an input of the task and is not re-proved. Tournaments outside the families named here were not searched. Re-running the censuses requires a short program; the counts, witnesses, independent sets, and solver outcomes are the record of the run.

Next: Run the same four-set census on subsets of 52 through 66 vertices in the Paley tournament of order 103, the next prime congruent to 3 mod 4 after 83. Orders 67 and 68 inside QR_83 are undecided; both sit at or above the upper bound f(4) <= 67 already given by QR_67.

## 2026-10-23T19:04:37.779372+00:00 — R4-G-degree-24 ingested

Source: file. Result: proved. Verification: unreviewed.

Claim: The no-in-degree-23 lemma is accepted. In a tournament on 52 vertices in which every triple has at least 5 dominators, no in-degree equals 23. A vertex of in-degree 24 need not exist: twenty-six in-degrees 25 and twenty-six in-degrees 26 already sum (in-degree minus 25) to 26. Whether or not an in-degree 24 occurs, some triple has at least 7 dominators. If every triple had at most 6 dominators, the sum of C(|D(Y)|, 2) would equal 5 times the sum of |D(Y)| minus 331500, while the common-out-neighbour count is at least 1158 larger. Erdős problem 902 is not solved.

Weakness: The status proved covers the acceptance of the no-in-degree-23 count and the uniform 7-dominator bound. Step 4 of that count uses J >= 3. That bound is the argument in research/AGENT_TASKS/R1-G-audit-every-n.report.json, used here as an input and not rewritten. (SF) is taken from the completed proof in section 3 of proof/swarm/r1_AUDIT-52-B.md; the introduction of that file claims several later theorems, and those claims are not evidence because the file stops during section 3. Claim Q is an input: the comparison uses z <= 5, and it does not use the stronger sentence that each vertex of Z has at most two in-neighbours in Z. The same arithmetic still forces a 7-dominator triple for every z <= 8, and the formal difference becomes negative at z = 9, so the appeal to Claim Q has room, but without some upper bound on z the comparison does not close. The convex lower bound L uses only the sum of the common-out sizes. Extra constraints can only raise the sum of C(c, 3), so they do not weaken the contradiction, and 1158 is not asserted to be the gap of a realized tournament. No tournament was enumerated, Landau's condition was not needed, and the J = 3, 4 tree was not reopened. A tight pair at order 52 remains possible. Erdős problem 902 is not solved, and f(4) is not evaluated.

Next: Keep the minimum in-degree at 24 and keep both score regimes, z = 0 and z > 0. The slack 1158 is smallest on five in-degrees 24, forty-five in-degrees 25, one in-degree 40 and one in-degree 41; the next counting should test that sequence, and the balanced sequence, against a triple whose dominator count is at least 7. Do not treat an in-degree 24 as known to exist, and do not reopen the J = 3, 4 tree.

## 2026-10-23 — round 4

Under the triple hypothesis at order 52, some triple has at least 7 dominators. The weight minimum and the gap 1158 were recomputed. The handshaking equations still admit every triple at least 5, on the margin (26, 338, 5); those moments were recomputed and do not build a tournament. Forward circular tournaments of orders 52 through 66 are undominated on {0, m, 2m, 3m}. The upper bound remains f(4) <= 67. solved remains false.

## 2026-10-24T02:41:56.857351+00:00 — R5-B-outsets ingested

Source: file. Result: proved. Verification: unreviewed.

Claim: The margin survives the out-neighbourhood count. The out-set of a vertex of out-degree 26 is a tournament on 26 vertices with score sequence thirteen 12s and thirteen 13s, so it contains 1872 transitive triples. With the 12-regular out-sets of the vertices of out-degree 25, the sum of the dominator counts over transitive triples is 91572. The seven recorded rows fall short of that sum by 298. The same degree pattern and pair-excess pattern still admit an integer solution in which every triple has at least 5 dominators and the transitive sum is 91572. Erdős problem 902 stays open.

Weakness: The status proved applies to the counting equations of the margin (26, 338, 5) after the out-neighbourhood sum is imposed. The repaired rows assign nonnegative integers to those equations, and every triple in them has at least 5 dominators. They do not specify the arcs of a tournament, and they do not place a particular set of 1872 transitive triples inside one named out-set. The seven rows of the previous report remain incompatible with the sum 91572; survival uses the replacement above. The sign comparison that forbids minimum 6 is the one already written for this degree pattern and pair-excess pattern. Degree sequences with square-sum greater than 26 stay outside the argument. Erdős problem 902 stays open, and f(4) is not evaluated.

Next: Stop. The out-neighbourhood count is compatible with minimum 5, so it does not remove the margin. An arc realization would still have to carry a tournament of score sequence thirteen 12s and thirteen 13s in each out-set of an out-degree-26 vertex.

## 2026-10-24T02:41:56.895457+00:00 — R5-C-pattern ingested

Source: file. Result: proved. Verification: unreviewed.

Claim: The common-in-neighbour numbers c(A,B) = 4 and c(C,D) = 0 occur in a 5-regular tournament on 11 vertices. The recorded tournament uses vertices 0 through 10, with A = 0, B = 1, C = 2, and D = 3. Its out-sets are in the evidence. The six positive counts, in the order (A,B), (A,D), (A,C), (B,C), (B,D), (C,D), are 4, 3, 2, 2, 3, 0. Those two forced values occur, and the other four lie in the windows compatible with dominator counts 16, 14, 13, 13, 12, 12. Every common-in-neighbour count from {A,B,C,D} into {4,5,6,7,8,9,10} is at most 3. The construction stops at these eleven vertices. f(4) >= 52 is not proved, and Erdős problem 902 is not solved.

Weakness: The result is existence of one tournament, read off its out-sets. The out-sets were located by a constraint search; the proof is the inspection of the lists, and the search is not a step in that inspection. The 551 isomorphism classes of 5-regular tournaments on 11 vertices were not listed, and the report does not claim that the common-in-neighbour tuple is unique. The dominator counts, the excesses E_both, the budgets Ex, and the bound c ≤ 3 on pairs into V_0 are inputs from the R4-C report. That report takes J = 5 and s = 4 from earlier reports in the same agent role. Those bounds are not re-proved here. The two heavy vertices and the 37 light vertices are unassigned, so a tight pair on 52 vertices is neither built nor excluded. f(4) >= 52 is not proved, and Erdős problem 902 is not solved.

Next: Assign the two heavy vertices and the 37 light vertices for this common-in-neighbour pattern on the eleven dominators, or run the same identities at J = 5 and s = 5.

## 2026-10-24T02:41:56.925335+00:00 — R5-F-three ingested

Source: file. Result: proved. Verification: unreviewed.

Claim: Three nested common-in-neighbourhood deletions leave the coefficient of log2 log2 N equal to 1. For stage lengths s1, s2, s3 and out-degree excesses δi, the count produces γ ≤ log2 N + Π − log2(log2 N − s_eff) + C + o(1), where Π ≥ 0 and 0 ≤ s_eff ≤ s1 + s2 + s3. That expression is at least the one-level bound log2 N − log2 log2 N + C + o(1). It never has the shape log2 N − 2 log2 log2 N + O(1), because that would require log2 N − s_eff at least a constant times (log2 N)^2, while log2 N − s_eff is at most log2 N. Inverted, the lower estimate of f(n) stays of the shape (c + o(1)) n 2^n. Erdős problem 902 is not solved.

Weakness: The status proved applies only to this negative statement: three nested deletions do not change the coefficient. The shape of B is taken from the one-level bound and is not re-proved. The o(1) needs the order tending to infinity and each stage length o of the square root of the current order; outside that range the remainder is capped and the count falls back to B. The argument says nothing about a one-step count of every n-set. A tournament with a very small in-neighbourhood can satisfy a stronger numerical bound, and that bound is not available for a regular tournament, so it does not improve f(n). The constant in front of n 2^n is whatever constant B already carries. Erdős problem 902 stays open, and f(4) is not evaluated.

Next: Stop. The third deletion level leaves the coefficient of log2 log2 N equal to 1, for every split of the stage lengths and every out-degree excess. A further deletion of the same kind has the same shape.

## 2026-10-24T02:41:56.957356+00:00 — R5-G-push ingested

Source: file. Result: proved. Verification: unreviewed.

Claim: The weight equations do not force a triple with at most 4 dominators. On the extreme score sequence of five in-degrees 24, forty-five in-degrees 25, one in-degree 40 and one in-degree 41, the handshaking identities admit an explicit integer solution in which every triple level is at least 5 and the dominator counts are 16717 fives, 16 sixes, 2702 sevens and 2665 elevens. The common-out cubic moment is 370727, which is 42677 above the value attainable by counts in {5, 6}, and that excess is carried by the sevens and the elevens. Erdős problem 902 is not solved.

Weakness: The status proved applies to one integer solution of the star sums, the level formula, and the second-moment identity on the extreme score sequence. The common-out numbers are constant on the cuts of a realizable degree pattern. They are not shown to be the intersection sizes of the out-sets, so the solution is not a tournament. The dominated-side moment sum C(nu,2) is required to equal sum C(lambda,3)=388592, and the third-moment symmetry sum C(k,3)=sum C(nu,3) is required as well. Neither identity is solved here. A failure of those two identities would be a later step; it is not a proof that some triple has at most 4 dominators. The convex gap 1158 is used only as the input lower bound. This solution sits 41519 above the convex value 329208, because the stars of the in-degrees 40 and 41 cannot carry common-out counts 12 and 13. The balanced margin (26, 338, 5) is not rebuilt. No appeal is made to a tight pair or to the J=3, 4 tree. Erdős problem 902 is not solved, and f(4) is not evaluated.

Next: On this same pair table, decide whether nonnegative nu=L-k can satisfy sum C(nu,2)=388592 and sum C(k,3)=sum C(nu,3). If they can, record the rows. If they cannot, the obstruction is that identity, not a return to the weight minimum. Do not reopen the J=3, 4 tree, and do not treat the present solution as a tournament.

## 2026-10-23 — round 5

The margin (26, 338, 5) survives the out-neighbourhood count: each out-degree-26 vertex forces 1872 transitive triples, and a replacement integer solution still has every triple at least 5. The transitive sum 91572 was recomputed. On the extreme score sequence the weight equations also still allow every triple level at least 5. Three nested deletions leave the coefficient of the second logarithm equal to 1; that approach key is now exhausted. A 5-regular tournament on 11 vertices with common-in-neighbour counts 4, 3, 2, 2, 3, 0 was recomputed from its out-sets. solved remains false. f(4) stays in the interval from 52 to 67.

## 2026-10-24T03:11:10.074542+00:00 — R6-B-s4 ingested

Source: file. Result: inconclusive. Verification: unreviewed.

Claim: Property S_4 on 52 vertices is not contradicted by the identities recorded in research/LEMMAS.md or the round-4 and round-5 reports. The missing identity is sum_{|X|=4} |D(X)| = sum_v C(d^+(v), 4). Erdős problem 902 is not solved.

Weakness: The status inconclusive belongs to the decision that the recorded identities do not contradict S_4, together with the naming of the missing four-set equation. It is not a construction of an S_4 tournament on 52 vertices, and it is not a proof that no such tournament exists. The comparison 717600 > 270725 uses the double count in the proof of Lemma S1 one binomial degree higher; that four-set sentence is not written in research/LEMMAS.md or the round-4 and round-5 reports. The explicit four-set solution for 730730 assigns nonnegative integers. It does not specify arcs, and it does not use the R5-B rows. The convex lower bound 730730 is the minimum of sum C(μ, 4) for the equality score sequence; other score sequences were checked only at the extreme common-out table of R5-G. The equation sum C(|D(X)|, 3) = sum C(ν(Y), 4) is not decided. R4-C remains conditional on J = 5 and s = 4, and R5-C stops at eleven vertices. R4-D excludes named families only. The upper bound f(4) ≤ 67 was not re-proved. Three-level deletion was not used. Erdős problem 902 is not solved, and f(4) is not evaluated.

Next: Keep the equation sum_{|X|=4} |D(X)| = sum_v C(d^+(v), 4), which is at least 717600 against 270725 four-sets and does not forbid S_4. Impose sum_{|X|=4} C(|D(X)|, 2) = sum_P C(μ(P), 4) on the surviving (k, ν) rows; on the equality margin the right-hand side is at least 730730 and still allows every four-set at least two dominators. The identity that those two comparisons leave open is sum_{|X|=4} C(|D(X)|, 3) = sum_Y C(ν(Y), 4). Do not return to three-level deletion.

## 2026-10-24T03:11:10.100064+00:00 — R6-C-heavy ingested

Source: file. Result: proved. Verification: unreviewed.

Claim: The two heavy vertices of the J = 5, s = 4 pattern cannot sit against the recorded 5-regular tournament on vertices 0 through 10. With A, B, C, D = 0, 1, 2, 3, the zero-excess vertices are 4, 5, 6, 7, 8, 9, 10. Vertices 6 and 9 have exactly four common in-neighbours, namely 2, 4, 7, 8. The vertex of q = 11 beats nobody in the eleven, and the vertex of q = 8 beats only {0, 2, 3}, so both are out-neighbours of 6. The ten pair excesses at 6 then sum to 10 and are at least 14. The same gap holds at 9. The edge between the two heavy vertices is unused. A different tournament on eleven vertices is not excluded. f(4) >= 52 is not proved, and Erdős problem 902 is not solved.

Weakness: The obstruction is special to this edge list. The pair {6, 9} was found by reading the common-in-neighbour counts on the 21 pairs inside {4, 5, 6, 7, 8, 9, 10}; the proof is the reading of the out-sets and the budget arithmetic, and the scan is not a step in that reading. The 551 isomorphism classes of 5-regular tournaments on 11 vertices were not listed. A different tournament with the positive counts 4, 3, 2, 2, 3, 0 and with every zero-excess pair at most 3 may still accept the same two heavy vertices. The degree excesses 2, 1, 1, 1 and the heavy types q = 11 and q = 8 missing {0, 2, 3} are the pattern recorded in the R4-C report. That report depends on J >= 5 and s >= 4 from earlier reports in the same agent role, and those bounds are not rebuilt here. (F1) is derived above from S_4; the rest of the order-52 case tree is not. The 37 light vertices are unassigned because the budget at 6 has already failed. f(4) >= 52 is not proved, and Erdős problem 902 is not solved.

Next: Test another 5-regular tournament on 11 vertices against the same two heavy vertices, with positive common-in-neighbour counts 4, 3, 2, 2, 3, 0 and with every pair that meets the seven zero-excess vertices at most 3. The recorded tournament fails that last condition on {6, 9}.

## 2026-10-24T03:11:10.129062+00:00 — R6-G-nu ingested

Source: file. Result: proved. Verification: unreviewed.

Claim: On the extreme score sequence, with the recorded pair table and the recorded level assignment, nonnegative integers nu = L - k exist with every dominator count at least 5, sum k = 131910, sum C(k, 2) = 370727, sum C(nu, 2) = 388592 and sum C(k, 3) = sum C(nu, 3). Each dominated count in the rows is at most the out-degree room of its triple. The dominator counts 16717, 16, 2702 and 2665 cannot meet the third-moment identity. Erdős problem 902 is not solved.

Weakness: The proved statement is an integer table on one pair table and one cyclic placement: all of GNN, all of NNN, and 20 triples of HNN. The common-out numbers are constant on the cuts of the degree pattern. The table does not identify them with intersection sizes of out-sets. Two classes use a third dominator value on a single triple, one in hHH and one in HHG, and those singles are part of the checked total. The multiplier bound rules out the counts 16717, 16, 2702 and 2665. It leaves other dominator counts open, and the exhibited counts are one point that works. The out-degree room is the most generous orientation bound; a fixed orientation inside a class could be tighter. The weight minimum, the balanced margin and the J = 3, 4 tree are untouched. Erdős problem 902 is not solved, and f(4) is not evaluated.

Next: Keep this pair table and test whether its cut constants are the intersection sizes of the out-sets, with the triple counts restricted to a solution of these binomial equations. The out-degree room is already met by the rows. The missing test is that intersection condition. Do not rebuild the weight minimum, and do not treat the rows as a tournament.

## 2026-10-24T03:11:10.155071+00:00 — R6-H-strategy ingested

Source: file. Result: inconclusive. Verification: unreviewed.

Claim: The next round has two tasks, and the round after it has one. Round 7 decides the four-set cubic identity on the equality margin (26, 338, 5), and it tests one 5-regular tournament on 11 vertices that keeps the J=5, s=4 counts and keeps every pair of zero-excess vertices at most 3 common in-neighbours. Round 8 runs the pair and triple identities at J=5 and s=5. The bound f(4) >= 52 stays checked, the bound f(4) <= 67 stays unchanged, the pair and triple moments stay compatible with every triple having at least 5 dominators, and three-level deletion stays closed. Erdős problem 902 is not solved.

Weakness: This is a strategy. It proves no bound and it exhibits no tournament. The three round-6 reports were read from disk and are not yet ledger entries. J >= 5 and s >= 4 remain conditional on unreviewed reports in the same agent line. A four-set solution on the equality margin leaves the extreme score sequence untouched, and an exclusion on that margin leaves every other score sequence untouched. One 11-vertex tournament can meet the zero-excess condition and still reject the two heavy vertices, and acceptance of those two vertices would leave the 37 light vertices unassigned. A proof that no such tournament exists does not by itself close J=5 and s=4. The s=5 task does not treat J >= 6. Erdős problem 902 is not solved, and these three tasks do not determine f(4).

Next: Dispatch two round-7 tasks and one round-8 task. R7-B-cubic, approach key n52-four-set-cubic-margin: decide the four-set cubic identity on the repaired rows of the equality margin. This does not repeat n52-s4-from-recorded-identities, which left that cubic undecided after the four-set first and second moments still allowed every 4-set a dominator. R7-C-avoid, approach key n52-zero-excess-pairs-c-at-most-3: test one 5-regular tournament on 11 vertices whose pairs inside the seven zero-excess vertices have at most 3 common in-neighbours. This does not repeat n52-two-heavy-vertices, which placed the two heavy vertices on the recorded tournament and stopped at the pair {6, 9}. R8-C-s5, approach key n52-j5-s5-degree-shape: run the pair and triple identities at J=5 and s=5. This does not repeat n52-j5-s4-one-restriction, which ran the identities only for the degree shape 2, 1, 1, 1 and left five excesses equal to 1 unrun.

## 2026-10-23 — round 6

The four-set count sum |D(X)| = sum C(d^+, 4) is at least 717600, and there are 270725 four-sets, so that identity does not force an undominated 4-set. Both numbers were recomputed. The two heavy vertices of the J=5, s=4 pattern cannot sit on the recorded 11-vertex tournament: vertices 6 and 9 have common in-neighbours {2,4,7,8}, and the pair-excess lower bounds sum to 14 against a budget of 10. solved remains false.

## 2026-10-24T04:12:50.370163+00:00 — R7-C-avoid ingested

Source: file. Result: proved. Verification: unreviewed.

Claim: No 5-regular tournament on 11 vertices can carry the J = 5, s = 4 pattern of R4-C, because that pattern forces c(C, D) = 0 while T[R] has property S_2, so every pair of R has at least one common in-neighbour in R. The cell J = 5, s = 4 is empty. The tournament of R5-C has c(2, 3) = 0, is not S_2, and cannot be T[R]. Together with a hand treatment of J = 5, s = 5, every tight pair in an S_4 tournament on 52 vertices has J >= 6. Erdős problem 902 is not solved.

Weakness: J >= 6 uses R1-C (J >= 5) for s <= 3 and the R4-C case tree for s = 4 as hand inputs; both are independently reproduced by the CP-SAT pair-level model, which is one implementation by one author. Lemma A is used; its proof (rounding modulo 4 at a vertex with j = 0) was re-read for N = 52. The CP-SAT verdicts are solver outputs without exported certificates. Tight pairs with 6 <= J <= 14 are not excluded, and the no-tight branch at order 52 is untouched. f(4) >= 53 is not proved and Erdős problem 902 is not solved.

Next: Drop R8-C (J = 5, s = 5 is closed). Attack the three J = 6 survivors, all with heavy pattern 6+2, with the full local model (outside vertices individually, triple and 4-set rows) or by hand, and look for a global argument that turns J >= 6 into a contradiction with the order-52 degree budget.

## 2026-10-24T04:12:50.401846+00:00 — R7-B-cubic failed

Attempt 1 of 3. Status: pending.

dispatch timed out before a report arrived
