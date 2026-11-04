# Lemmas

Curated statements only. A generated list of ingested agent claims follows the marker at the bottom. An ingested claim is not a theorem until its verification line says it was checked independently of the writer.

## Lemma S1 (every tournament on 52 vertices)

**Statement.** Let \(T\) be any tournament on 52 vertices. Then

\[
\sum_{\{u,v\}} |D(\{u,v\})| \ge 16250,
\]

with equality if and only if the in-degrees are twenty-six 25s and twenty-six 26s. In particular some pair has at least 13 dominators, and

\[
\sum_{\{u,v\}} \big(|D(\{u,v\})| - 12\big) \ge 338.
\]

No appeal to \(S_4\) is used. The identity \(\sum |D(P)| = 16237 + \tfrac12\sum e(v)^2\), with \(e(v) = d^-(v)-25\), is the one quoted in `proof/N52_ATTEMPT.md` and `proof/swarm/BRIEF.md`. The lower bound and the equality case are unconditional.

**Proof.** \(d^+(v) = 51 - d^-(v)\). Set \(e(v) = d^-(v) - 25\), so \(d^+(v) = 26 - e(v)\). The handshaking lemma gives \(\sum d^- = \binom{52}{2} = 1326\), hence \(\sum e = 1326 - 25\cdot 52 = 26\).

\[
\sum_v (26-e(v))(25-e(v)) = 52\cdot 650 - 51\cdot 26 + \sum e^2 = 32474 + \sum e^2.
\]

The left side is twice \(\sum \binom{d^+(v)}{2}\), so

\[
\sum_v \binom{d^+(v)}{2} = 16237 + \tfrac12\sum e(v)^2.
\]

A vertex \(w\) dominates a pair if and only if that pair lies in \(N^+(w)\). Therefore \(\sum_P |D(P)| = \sum_v \binom{d^+(v)}{2}\).

It remains to show that an integer vector of length 52 summing to 26 has square-sum at least 26, with equality exactly at twenty-six 1s and twenty-six 0s. If two coordinates \(a\) and \(b\) satisfy \(b \ge a+2\), replace them by \(a+1\) and \(b-1\). The sum is unchanged and the square-sum changes by

\[
(a+1)^2 + (b-1)^2 - a^2 - b^2 = 2(a-b+1) \le -2.
\]

Each such move decreases the square-sum by at least 2, so the process stops at a vector whose coordinates differ by at most 1. The only vector of length 52, sum 26, with coordinates in \(\{m,m+1\}\) is twenty-six 0s and twenty-six 1s: if \(m \ge 1\) the sum is at least 52, and if \(m \le -1\) then \(m+1 \le 0\) and the sum is at most 0. Its square-sum is 26. Every other integer vector can be moved to this one, strictly decreasing the square-sum, so its square-sum is at least 28.

Thus \(\sum |D(P)| \ge 16237 + 13 = 16250\), with equality exactly for that in-degree sequence. If every pair had at most 12 dominators the sum would be at most \(12\cdot 1326 = 15912 < 16250\). So some pair has at least 13 dominators, and the displayed excess over 12 is at least 338. ∎

**Verification.** The arithmetic, the decrease identity, the Landau-free equality case, and the pair-dominator identity were checked on the transitive tournament and on one seeded random tournament by `research/compute/exact_checks.py`. This does not say that a tournament attaining 16250 realises the excess as 338 pairs of size 13 and 988 pairs of size 12. That distribution is only one integer solution of the sum.

**Status.** Proved above. Independent of the Schütte property.

## Lemma I (tight-pair counting, every order)

**Hypotheses.** \(N \ge 13\). \(P\) is a pair, \(R\) is an 11-set disjoint from \(P\), every vertex of \(R\) beats both vertices of \(P\), and \(T[R]\) is 5-regular. Let \(O = V \setminus (P \cup R)\), \(q_y = |R \cap N^-(y)|\) for \(y \in O\), and \(j_r = d^-(r) - 25\) for \(r \in R\), \(J = \sum_{r \in R} j_r\).

**Statement.** For each \(r \in R\), the number of \(y \in O\) with \(r \notin Q_y\) is \(20 + j_r\). And

\[
\sum_{y \in O} (q_y - 5) = 6N - 298 - J.
\]

In particular the right side is \(8 - J\) when \(N = 51\) and \(14 - J\) when \(N = 52\).

**Proof.** \(d^+(r) = N - 1 - d^-(r) = N - 26 - j_r\). The out-neighbourhood of \(r\) already contains both vertices of \(P\) and exactly five vertices of \(R\), and these seven vertices lie outside \(O\). So \(r\) has \(N - 33 - j_r\) out-neighbours in \(O\). Since \(|O| = N - 13\),

\[
|O| - (N - 33 - j_r) = 20 + j_r
\]

vertices of \(O\) are not beaten by \(r\). Those are exactly the \(y\) with \(r \notin Q_y\).

Double counting the pairs \((r,y)\) with \(r \to y\) gives \(\sum_y q_y = \sum_r (N - 33 - j_r) = 11N - 363 - J\). Subtract \(5|O| = 5N - 65\):

\[
\sum_y (q_y - 5) = 6N - 298 - J. \qed
\]

**Status.** Proved under the stated degree hypotheses. Property \(S_4\) is not an extra hypothesis: a tight pair in an \(S_4\) tournament satisfies the hypotheses, by `(F2)` and the definition of tightness in `proof/ERDOS902_PROOF.md`. The identity does not by itself force \(J \ge 3\).

## Lemma J (every tight pair has \(J \ge 3\))

**Statement.** In every tournament with property \(S_4\), on any number of vertices, every tight pair \(P\) satisfies \(J(P) \ge 3\).

**Status.** The paragraph in `proof/F4_GE_52_HAND_PROOF.md` that asserts this for every order is incomplete: it invokes `(R1)`–`(R3)` outside the hypotheses of Lemma P. A replacement argument is written in `research/AGENT_TASKS/R1-G-audit-every-n.report.json`. The orchestrator rechecked the steps that paragraph had skipped: under \(J \le 2\), `(*)` excludes \(q_y \in \{7,8\}\); a 6-vertex would beat five vertices of positive excess and force \(J \ge 5\); the excess identity then forces \(J = 2\), no missed vertex inside a heavy block, and \(N-50\) blocks equal to \(R\); both integer shapes of \(J = 2\) contradict the pair-sum \(120 + 5j\). Those steps hold. This is one author and one checker, not a blind second write-up. It does not by itself prove \(J \ge 5\) at order 52, and it does not prove \(f(4) \ge 52\).

## Doubly regular tournaments of order 51

**Statement.** Every tournament on 51 vertices in which every in-degree and every out-degree is 25, and every pair has exactly 12 common in-neighbours, has a triple with at most 4 dominators.

**Status.** Re-derived in `research/AGENT_TASKS/R1-B-theorem5.report.json`. The inclusion-exclusion \(k+\nu = 12-\sigma\) and the numerical contradiction \(p = 6375 > 2762\) agree with a direct check of those identities.

## Theorem. \(f(4) \ge 52\)

**Statement.** No tournament on 51 or fewer vertices has property \(S_4\). Every tournament on 51 or fewer vertices has some triple with at most 4 dominators. Hence \(f(4) \ge 52\). The Paley tournament of order 47 shows that 4 is attained.

**Status.** Checked. The pieces are Theorem A in `proof/ERDOS902_PROOF.md` §2, Theorem 1 and Corollaries 2–4 and Theorem 5 in `proof/F4_GE_52_HAND_PROOF.md`, with the triple lower bound as the only use of \(S_4\). The orchestrator recomputed the arc identity, the slack \(12N-610\), the case-(I) excess \(26+k-W\), and the third-moment value \(p=6375\). `research/AGENT_TASKS/R3-G-break-52.report.json` rewrote the same path and found no break. `research/AGENT_TASKS/R3-D-case-I.report.json` found that the integer box for case (I) stops at \(\sum h_z \le 25\) against a Gram nullity of 26. This is a bound on \(f(4)\). It is not a determination of \(f(4)\), and it is not a solution of Erdős problem 902.

The Paley tournament of order 59 has triple minimum 5, on \(\{0,1,7\}\), and the 4-set \(\{0,1,7,19\}\) is undominated. A direct quadratic-residue scan agrees. So a triple minimum of 5 does not force \(S_4\). The upper bound in force remains \(f(4) \le 67\).

## Lemma. No in-degree 23 at order 52

**Statement.** In a tournament on 52 vertices in which every triple has at least 5 dominators, no in-degree equals 23.

**Status.** The counting in `proof/N52_ATTEMPT.md` §2 was recomputed: the slack is \(E \le 14\), the block intersection squares sum to 36, and 14 in-neighbours in the out-set cannot land in a 12-set. The step uses the structural fact (SF) for a dominator of in-degree 25. That fact is written in `proof/swarm/r1_AUDIT-52-B.md` §3. The file stops before the uniform argument announced in its introduction.

## Order 52: some triple has at least 7 dominators

**Statement.** In a tournament on 52 vertices in which every triple has at least 5 dominators, some triple has at least 7 dominators.

**Status.** The no-in-degree-23 count and the weight minimum are the argument in `research/AGENT_TASKS/R4-G-degree-24.report.json`. Dynamic programming confirmed that the positive excess \(26+z\) is lightest on two nearly equal parts, for each \(z \le 5\). On the extreme score sequence the second-moment gap is 1158, matching \((55640 + \sum f(e))/6\). The bound does not forbid the triple hypothesis, and it does not decide whether an \(S_4\) tournament on 52 vertices exists.

## Circular tournaments of order 52 through 66

**Statement.** For each \(n\) from 52 through 66, the forward circular tournament, and both diametral orientations when \(n\) is even, has an undominated 4-set \(\{0, m, 2m, 3m\}\) with \(m = \lfloor n/4 \rfloor\).

**Status.** The gap comparison was read, and a direct scan found no dominator of that 4-set for every such order and both orientations. These tournaments do not improve the upper bound \(f(4) \le 67\).

## What is not a lemma yet

### The every-order extension of Theorem 1

`proof/F4_GE_52_HAND_PROOF.md` proves, at order 51, that a tight pair has \(J \ge 3\). The paragraph beginning "Theorem 1 holds for every \(N\), not only \(N = 51\)" then asserts the same bound at every order, and says that `(R1)`–`(R3)` and steps 3–5 survive with only Step 2 rewritten.

That paragraph is the citation `proof/N52_TIGHT_PAIRS.md` uses for \(J \ge 3\) on 52 vertices, and therefore for its theorem that \(J \ge 5\). The \(N = 51\) case analysis does not automatically transfer:

- `(R1)` is derived under Lemma P, which forbids \(q_y \in \{7,8\}\) and leaves a single heavy vertex. Lemma P uses \(|O| = 38\).
- The sentence "\((R1)\)–\((R3)\) hold verbatim, with \(\gamma_u\) redefined" does not re-derive `(R1)` when several vertices have \(q_y \ge 9\), nor does it write the exclusion of \(q_y \in \{7,8\}\).
- "Steps 3–5 are then unchanged" is stated for a situation that, at \(N = 52\), would have \(m = N - 50 = 2\) heavy vertices rather than one.

The mod-4 arithmetic inside the \(N = 51\) argument was recomputed while reading it (the identity \((R2)\) and the division by 4 that produces \(\beta + 5\gamma + N_4 \le 5j\)). That check is not an audit of the every-order paragraph, and it is not an audit of the whole \(N = 51\) write-up.

**Status.** Open. The extension is an unresolved bottleneck, not a disproof.

### Repository claims awaiting an independent reading

| claim | where | status on 23 October 2026 |
|---|---|---|
| \(f(4) \ge 51\) (Theorem A) | `proof/ERDOS902_PROOF.md` §2 | Hand argument present. Every numerical inequality in it was checked again by `proof/verify_proof.py` (V3), rerun this session. The logic has not been re-read line by line in this session. |
| \(f(n) \ge (n+5/2)2^{n-1}-1\) for \(n \ge 4\) | same, §4 | Hand argument. V4 checked the binomial comparison for \(5 \le n \le 2000\). |
| \(f(n) \ge (c^\ast - o(1)) n 2^n\) with \(c^\ast = 0.7695032191504894326990652683098231346767\) | same, §5 | Hand argument. V5 reproduced \(c^\ast\) and the integral comparison. |
| Explicit table, \(f(5) \ge 121\), …, \(f(12) \ge 35655\) | same, §6 | The recursion was rerun (V6) and reproduced the table. This is a finite computation, not a determination of \(f(n)\). |
| \(f(4) \ge 52\), and the strong claim that every tournament on at most 51 vertices has a triple with at most 4 dominators | `proof/F4_GE_52_HAND_PROOF.md` | Hand argument. Not covered by `verify_proof.py`. The strong claim implies \(f(4) \ge 52\), because \(S_4\) implies the triple condition. A tournament on \(\le 51\) vertices in which every triple has at least 5 dominators would falsify the strong claim and this proof, and would falsify \(f(4) \ge 52\) only if that tournament also has \(S_4\). |
| No in-degree 23 at \(N = 52\), and \(J \ge 5\) for a tight pair | `proof/N52_TIGHT_PAIRS.md` | Hand argument, unaudited. The \(J \ge 5\) theorem cites the every-order extension above for the case \(J \le 2\). |
| Claim L is false | `proof/ERDOS902_PROOF.md` §8.2 | The saved realisation was rechecked by V7 this session. See `COUNTEREXAMPLES.md`. |

## Published anchors used as inputs

These are not re-proved here. They are the classical statements named in `PROBLEM.md`: \(f(1)=3\), \(f(2)=7\), \(f(3)=19\), the Szekeres lower bound \((n+2)2^{n-1}-1\), and Erdős's upper bound of shape \(n^2 2^n\). Today's rerun of `verify_proof.py` checked that the Paley tournament of order 7 has \(S_2\) and the Paley tournament of order 19 has \(S_3\).

<!-- BEGIN GENERATED LEMMAS -->
<!-- task:R1-E-checks -->
### R1-E-checks — computed (reproduced_by_orchestrator)

Lemma S1 and Lemma I match the arithmetic in LEMMAS.md, the printed numbers in F4_GE_52 section 6 match, and the Paley profiles of orders 7, 19 and 67 match the profiles previously computed by proof/verify_proof.py. In the Paley tournament of order 47 the minimum of |D(Y)| over triples Y is 4, attained, and the minimum over 4-sets is 0. The sentence 'every tournament on at most 51 vertices has a triple with at most 3 dominators' is therefore false. The strong claim with 4 in place of 3 survives this example, and this tournament does not have S_4.

Weakness: All Paley tournaments of orders 7, 11, 19, 23, 31, 43, 47 and 67 were scanned exactly. This is not a search over all tournaments of those orders. Orders below 47 cannot meet the triple condition for S_4, by the Szekeres bound, so a Paley counterexample to the strong claim would have to be order 47.

<!-- task:R1-A-literature -->
### R1-A-literature — computed (unreviewed)

Bibliographic classification only, checked on 23 October 2026. Erdős problem 902 is not solved. On the opened problem page the stated results stop at f(1)=3, f(2)=7, Erdős's 2^{n+1}-1 ≤ f(n) ≪ n^2 2^n, and Szekeres–Szekeres's f(3)=19 and n 2^n ≪ f(n), with zero proof claims. The finite window 48 ≤ f(4) ≤ 67 is supported by sources opened outside this workspace: Reid, McRae, Hedetniemi, and Hedetniemi (2004) prove that property S_4 requires at least 48 vertices, and Graham–Spencer (1971) state that the Paley tournament on 67 vertices has the property. The claims f(4) ≥ 51, f(4) ≥ 52, and c* ≈ 0.76950321915 were not present in any source opened in this pass. They are written in this workspace. This is not a proof that those three strings occur nowhere else in the literature.

Weakness: ['The full texts of Erdős 1963 and Szekeres–Szekeres 1965 were not opened. Their general bounds are website attributions plus quotations in later papers that were opened.', 'Reid and Brown 1972, cited for the last step of Corollary 7, was not opened. Moon 1968 was not opened. The Er82e target was not opened.', "Graham–Spencer formulas in the Cambridge extraction are OCR-damaged. The prose sentence that T_67 has property P_4 was readable. The strictness of the sign in 'f(4) > 47' was not checked against a clean glyph.", "Jeffries's preprint says the classical bounds remain the best known and have been unimproved for 60 years, while the 2004 paper opened here already has the stronger finite bound of 48. That is a gap in the preprint's survey, not a retraction of Corollary 7.", 'Bozóki attributes the conjecture f(4)=67 to Graham–Spencer. The sentence read in Graham–Spencer is that T_67 might be minimal.', "Web search and the opened corpus did not surface f(4) ≥ 51, f(4) ≥ 52, or 0.76950321915. That does not prove those strings are absent from every unopened paper, repository, or paywalled scan. Semantic Scholar's empty response is not a negative search.", 'The Wilder Lean project was read from the README and one markdown note. It was not rebuilt, so the kernel check claimed there is UNVERIFIED.', 'The cursor-ide-browser server did not register. Page text comes from WebFetch and publisher extractions, not from a rendered browser snapshot.', "OpenAlex's hit for the Szekeres title was Yair Caro and Adriana Hansberg, Directed domination in oriented hypergraphs (2019), not the 1965 paper. It was not used. The broad arXiv tool from the earlier session was not rerun and those unrelated papers are not cited."]

<!-- task:R1-B-theorem5 -->
### R1-B-theorem5 — proved (unreviewed)

Every doubly regular tournament on 51 vertices has some triple with at most 4 dominators. Here doubly regular means that every in-degree and every out-degree is 25, and every two distinct vertices have exactly 12 common in-neighbours.

Weakness: The proved statement stops at the doubly regular parameters. It does not show that every tournament on 51 vertices has a triple with at most 4 dominators, and it does not show f(4)≥52. In the hand proof those conclusions use Theorem 1 and Corollary 4, which were not re-derived. Erdős problem 902 is not solved: the order of f(n) is untouched, and so is the upper bound f(4)≤67. The argument also does not decide whether a tournament with these parameters exists, and it does not name the exact minimum, only that the minimum is at most 4.

<!-- task:R1-G-audit-every-n -->
### R1-G-audit-every-n — proved (unreviewed)

The paragraph in proof/F4_GE_52_HAND_PROOF.md that begins 'Theorem 1 holds for every N, not only N = 51' is an incomplete proof. Its first unjustified inference is the sentence asserting that (*), (R1)-(R3) and the rounding lemma hold verbatim at every order once gamma_u is redefined as the number of vertices y with q_y >= 9 and u not in Q_y. The conclusion of that paragraph is true by the argument written in this report, which is the auditor's proof and not a repair declared to be the printed text: in every S_4 tournament, on any number of vertices, every tight pair P satisfies J(P) >= 3. This verdict covers that every-order claim. It does not certify the N = 51 write-up of Theorem 1, it does not prove J >= 5 on 52 vertices, and it does not solve Erdős 902.

Weakness: The status proved applies only to the argument written here. The printed paragraph remains incomplete, and the sentence that Steps 3-5 are unchanged is still not a citation of a matching text: Step 3 in the N = 51 write-up names a single vertex y*. The following paragraph of the same note, lines 213-218, claims the in-degree-25 structural fact for an arbitrary tight pair with no bound on J. Its parenthetical proof invokes the rounding lemma as written, which assumes the N = 51 profile, and that paragraph was not given a proof in this report. Sections 3 and 4 of proof/N52_TIGHT_PAIRS.md, which exclude J = 3 and J = 4 at N = 52, were not audited. The lower bound s >= 7 - x is weak once x >= 8; the argument removes every 6-vertex before the final comparison, so that weak range is not where the contradiction is drawn. No enumeration was run.

<!-- task:R1-C-n52-j-le-2 -->
### R1-C-n52-j-le-2 — proved (unreviewed)

In an S_4 tournament on 52 vertices, every tight pair P satisfies J(P) >= 5. Lemma J supplies J >= 3, and the case analysis below excludes J = 3 and J = 4. Sections 3 and 4 of proof/N52_TIGHT_PAIRS.md are not the proof: the first case that does not follow as printed is section 4, s = 3, which treats partitions of 11 and gives no argument for the partition 5+5 of the excess 10. The bound J >= 5 is the conclusion of the corrected analysis in this report. A tight pair with J >= 5 is still open, f(4) >= 52 is not proved, and Erdős problem 902 is not solved.

Weakness: The status proved belongs to the case analysis written here. The printed section 4, s = 3, does not establish its exclusion, and the s = 4 rows 6+4, 5+5 and 4+4+2 do not follow from the reasons printed beside them. Section 3 follows once 17 is replaced by 22 in the inconsistent s = 2 assignment. Lemma J is an input from the G report and from research/LEMMAS.md; that argument is one author and one checker, and this report does not re-prove J >= 3. Lemma A was rechecked because every appeal to 12 dominators on a pair into V_0 uses it. The comparison J >= 5 does not force four vertices of positive excess: a single vertex of excess 5 meets J = 5 with s = 1, and sections 5 and 9, which treat that shape, were not audited. No tournament was enumerated. A tight pair at order 52 remains open, f(4) >= 52 is not proved, and Erdős problem 902 is not solved.

<!-- task:R1-F-reformulation -->
### R1-F-reformulation — proved (unreviewed)

A tournament on 52 vertices has property S_4 if and only if, for every vertex v, the subtournament induced by the in-neighbourhood of v has property S_3. Equivalently, no tournament on 52 vertices has S_4 if and only if every tournament on 52 vertices has at least one vertex whose induced in-neighbourhood fails S_3. Iterating the same identity, S_4 fails if and only if there is a sequence of m ≤ 4 vertices in which each later vertex beats every earlier one and no vertex beats the whole sequence. The equivalence does not show that either side is true, and it does not solve Erdős problem 902.

Weakness: The status proved applies only to the equivalence. Neither side has been established: the report does not show that every tournament on 52 vertices has a vertex whose in-neighbourhood fails S_3, and it does not show that an S_4 tournament on 52 vertices exists. Erdős problem 902 is not solved. The order of f(n) is untouched, and so is the upper bound f(4) ≤ 67. The identity holds at every order at least 4, so the number 52 plays no special role. Granting the classical theorem f(3) = 19, which is not re-proved here, would dispose only of a vertex of in-degree at most 18. Every remaining case has all in-degrees at least 19, and an in-neighbourhood of that order can carry S_3. The sequence form allows length strictly less than 4. It is not the assertion that some transitive 4-set is undominated; a shorter transitive dominating set need not extend to a transitive dominating 4-set. Lemma S1, the tight-pair bound J ≥ 3, and the case split J = 3, 4 were not used.

<!-- task:R1-H-strategy -->
### R1-H-strategy — inconclusive (unreviewed)

The obstacles that block a proof, in the order they should be worked, are: Corollaries 2–4 at order 51, which are what would let the re-derived Theorem 5 forbid an S_4 tournament on 51 vertices; Theorem A, which is what would then exclude orders 49 and 50 and give f(4) ≥ 52; the order-52 branch in which every pair has at least 12 dominators, which is what blocks a proof that no S_4 tournament has 52 vertices; and sections 5 and 9 of the order-52 note, which are what would turn a tight pair into four dominators of in-degree greater than 25. The J = 3 and J = 4 audit is already written in R1-C and stays in progress until an independent check finishes. Erdős problem 902 is not solved.

Weakness: This is a strategy. It proves no bound and it exhibits no tournament. J ≥ 5 remains conditional until someone other than the author of R1-C checks that report, including its Lemma A; the enumeration with 18 and 220 configurations is not that check. The two swarm files under proof/swarm/ are uningested sketches. Tasks R2-F-min-12 and R2-I-four-positive can return inconclusive without touching the order-51 gates. Section 8, the classical unopened papers, and the factor-n gap are left out of this round on purpose: the first is the reserve behind rank 4, and the other two block citation and the asymptotic estimate rather than the written finite implications. Erdős problem 902 is not solved, and f(4) ≥ 52 is not proved.

<!-- task:R3-C-four-positive -->
### R3-C-four-positive — conditional (unreviewed)

Assume J >= 5 for every tight pair in an S_4 tournament on 52 vertices, as proved in research/AGENT_TASKS/R1-C-n52-j-le-2.report.json and not re-proved here. Then every such pair has at least four dominators of in-degree greater than 25. Sections 5 and 9 of proof/N52_TIGHT_PAIRS.md reach that conclusion, but they do not follow as printed. The first gap is section 5, partition 6+3, on the degree shape (2, 2, 1): the pair counts are 18, 13 and 13, so the printed pair with 8 dominators does not occur. Section 9 omits the empty excess at J = 14 and several degree splits, and two printed budgets are wrong. The repaired case analysis below leaves no configuration with s <= 3. A tight pair with s >= 4 remains open, f(4) >= 52 is not proved, and Erdős problem 902 is not solved.

Weakness: The status conditional belongs to the dependence on J >= 5. That bound is the R1-C report, written by the same agent role, and it is unreviewed. This report does not re-prove it, and it does not re-prove Lemma A. Every pair into V_0 is given 12 dominators by Lemma A; if that lemma failed, the pair-sum reduction used here would fail with it. The repaired case analysis is the argument for s >= 4 given those inputs. The printed section 5 does not establish the shape (2, 2, 1) of partition 6+3, and it does not write the placements of partition 5+4. The printed section 9 does not treat J = 14, and the splits and budgets named in the evidence do not follow as written. The introduction of proof/swarm/r1_AUDIT-52-B.md asserts Lemma C and sketches a uniform counting invariant, but the file stops during its section 3, before any such proof. That introduction is not evidence. The labeled enumeration is a check that the same inequalities admit no survivor; it is not a search of tournaments, and it uses the same identities as the case analysis, so it does not insure those identities. A tight pair with four or more positive dominators remains possible. f(4) >= 52 is not proved, and Erdős problem 902 is not solved.

<!-- task:R3-D-case-I -->
### R3-D-case-I — proved (unreviewed)

At order 51, no integer parameters meet the identities used in Corollary 3 of proof/F4_GE_52_HAND_PROOF.md in case (I) while every tight pair has J at least 3. The identity that blocks the search is sum_z h_z = 26 + |N^-(v) intersect Z| - W(v). Under those hypotheses the right-hand side is at most 25, while the Gram matrix forces at least 26 indices z with h_z at least 1. Erdős problem 902 is not solved, and this comparison does not prove f(4) >= 52.

Weakness: The status proved applies to the emptiness of this integer box under the hypotheses Corollary 3 cites and under J >= 3 on every tight pair. Claim Q, Lemma T, (F1), (F2), and the minimum in-degree 24 are used as constraints, not re-proved. The load-bearing unit is k <= 2 against nullity 26: the excluded point k = 3, W = 3, J = 3 would give sum_z h_z = 26. No tournament was built, and the 551 isomorphism classes of 5-regular tournaments on 11 vertices were not searched. Case (R), the doubly regular moment argument, and orders other than 51 are outside the box. The random check of the arc count covers 8 tournaments of order 51 and 30 of order 7; the identity itself is the double count in the argument. Erdős problem 902 is not solved, and f(4) >= 52 is not a conclusion of this report.

<!-- task:R3-F-order-52 -->
### R3-F-order-52 — proved (unreviewed)

Rerunning at order 52 the argument that an S_4 tournament on 51 vertices is doubly regular, the first bound that becomes inconclusive is Σ_{a in A} e(a) ≤ 2 in Corollary 2 of proof/F4_GE_52_HAND_PROOF.md. At order 51 the arcs from the in-neighbourhood of a vertex of in-degree 23 force that sum to be at most 2, and 2 contradicts J ≥ 3. At order 52 the same count forces the sum to be at most 14, and 14 does not contradict J ≥ 3. The two numbers are 2 and 14. Erdős problem 902 is not solved.

Weakness: The status proved applies to the location of the first transported failure and to the two slack values 2 and 14. It does not disprove minimum in-degree 24 at order 52: the design argument in proof/N52_ATTEMPT.md was left unread beyond its statement that it continues from E ≤ 14, and it was not checked. Lemma J is an input from research/LEMMAS.md and from R1-G; this report does not re-prove J ≥ 3. The comparison with J ≥ 5 uses that bound only as a number, without reopening its case analysis. Corollaries 3 and 4 were not rerun. No tournament was enumerated. Erdős problem 902 is not solved, and f(4) is not evaluated.

<!-- task:R3-G-break-52 -->
### R3-G-break-52 — proved (unreviewed)

No tournament on 51 or fewer vertices has S_4, so f(4) >= 52. For A = N^-(v) in Corollary 3, sum_z |D_z| equals sum_{x in A}(d^+(x) - 1). Every inference on the printed path follows. There is no first failing inference and no unfinished block on that path. Erdős problem 902 is not solved.

Weakness: The status proved is the nonexistence of an S_4 tournament on at most 51 vertices, together with the resulting lower bound f(4) >= 52. It is not a solution of Erdős problem 902. The classical upper bound f(4) <= 67 was not re-proved, so this pass does not identify f(4). Order 52 was not considered. Weyl's inequality, Gershgorin's theorem, and Cauchy interlacing are used as standard facts about Hermitian matrices; their hypotheses were checked in the decreasing eigenvalue convention, and they were not re-proved from the characteristic polynomial. The every-order paragraph after Theorem 1 remains an incomplete citation, as previously reported, and the structural sentence about an arbitrary tight dominator of in-degree 25 was not given a separate proof here because Corollary 2, Corollary 3, and Corollary 4 do not use it. No tournament was enumerated.

<!-- task:R4-B-no-tight -->
### R4-B-no-tight — proved (unreviewed)

These hypotheses do not force a triple with fewer than 5 dominators. The handshaking identities admit the integer margin (26, 338, 5): the degree excesses are twenty-six 0s and twenty-six 1s, the pair excesses sum to 338, and every triple in the solution has at least 5 dominators. For this same margin the lower bound is sharp, because the identities also force some triple to have at most 5 dominators. Erdős problem 902 is not solved.

Weakness: The status proved applies to the integer margin (26, 338, 5) and to the sign obstruction that makes 5 sharp for that margin. The solution assigns nonnegative integers to the double-counting equations. It does not construct the arcs of a tournament, so it does not show that a tournament on 52 vertices can have every pair at least 12 dominators and every triple at least 5. The transitive triples were distributed between the two excess classes only so that their number equals 16250; a tournament would have to realise that split inside the out-sets. Other degree sequences, with Σ e^2>26, were not needed: one consistent margin is enough to show that the identities do not force a triple below 5, and it says nothing about those other sequences. The lower bound of 7 dominators on some triple is the balanced-score remark already in proof/N52_TIGHT_PAIRS.md §7; the new comparison is that the same second moment still fits next to a minimum of 5. No appeal is made to a tight pair, to J, or to S_4 beyond the numerical lower bounds in the hypotheses. Erdős problem 902 is not solved, and f(4) is not evaluated. The classical upper bound f(4)≤67 was not re-proved.

<!-- task:R4-C-tight-s4 -->
### R4-C-tight-s4 — conditional (unreviewed)

Assume a tight pair in an S_4 tournament on 52 vertices with J = 5 and s = 4. Those two bounds are conditional inputs and are not rebuilt. The degree excesses on the four positive dominators are then 2, 1, 1, 1, and the heavy excess is 9. Lemma A, the pair-sum, the triple-excess formula, and c <= 4 exclude every excess partition of 9 other than 6+3. They also exclude 6+3 unless the vertex of q = 8 misses the degree-2 dominator and exactly two of the degree-1 dominators. Name the degree-2 vertex A, the untouched degree-1 vertex B, and the missed degree-1 vertices C and D so that |D({B,C})| = 13. The six dominator counts inside the positive set are then forced: |D({A,B})| = 16, |D({A,D})| = 14, |D({A,C})| = 13, |D({B,C})| = 13, |D({B,D})| = 12, and |D({C,D})| = 12. The same identities force c(A,B) = 4 and c(C,D) = 0, and they admit an explicit common-in-neighbour tuple on the other four pairs. A tight pair with J = 5 and s = 4 remains compatible with these identities. f(4) >= 52 is not proved, and Erdős problem 902 is not solved.

Weakness: The status conditional belongs to the dependence on J >= 5 and s >= 4. The first is the R1-C report and the second is the R3-C report. Both were written in the same agent role, both are unreviewed, and neither is re-proved here. Lemma A is an input from the same source: every pair into V_0 is given 12 dominators and c <= 3 by that lemma. The case analysis excludes the other patterns at J = 5 and s = 4, and it exhibits one pattern that meets the pair-sum, the triple-excess formula, and the per-vertex sum of common-in-neighbour counts. The seven counts from each positive vertex into V_0 were checked only as a list of seven integers at that vertex. They were not realized together inside one 5-regular tournament on 11 vertices. The nonnegative subset counts in the evidence account for the 37 light vertices on V_+ for one common-in-neighbour tuple. They do not assign those vertices inside V_0, and they do not build the tournament. The labeled enumeration is a check that the same inequalities admit no second orbit. It is not a search of tournaments, and it uses the same identities as the case analysis. A tight pair with this pattern, or with J = 5 and s = 5, or with J > 5, remains possible. f(4) >= 52 is not proved, and Erdős problem 902 is not solved.

<!-- task:R4-D-upper -->
### R4-D-upper — computed (unreviewed)

For every n from 52 through 66, the forward circular tournaments C_n^+ and C_n^- fail S_4. The undominated 4-set is {0, m, 2m, 3m} with m = floor(n/4). For odd n the two diametral rules define the same tournament; for even n both orientations fail, with this same witness. That half of the claim is a proof. A finite census shows that the Paley tournament of order 67 has no induced subtournament with S_4 on 50 through 66 vertices, the Paley tournament of order 71 has none on 52 through 70 vertices, and the Paley tournament of order 79 has none on 52 through 78 vertices. The Paley tournament of order 83 has none on 52 through 66 vertices. The power-interval tournaments of orders 53, 59, and 61, the cyclotomic tournaments of orders 53 and 61 in each of the two admissible pairs of residue classes, the Jacobi tournaments of orders 55 and 63, thirteen lexicographic products of orders 52 through 66, and all 64 majority products of a tournament on 4 vertices, fail S_4. An undominated 4-set for each of them is recorded in the evidence. The Paley tournament of order 67 has S_4, and this search found no example on fewer vertices, so the upper bound supplied by these families remains f(4) <= 67. Erdős problem 902 remains open.

Weakness: The circular failure is a written proof, and the edge list of each order was checked against it. The argument is special to this connection set. The Paley statements are enumerations. At orders 67, 71, and 79 the independence numbers in the unique-dominator bounds were recomputed by CP-SAT, CBC, CaDiCaL, and a separate backtrack. The equality cases at orders 71 and 79 were rejected by CP-SAT and CaDiCaL, and on one sample set the number of violated clauses equalled a direct count of undominated four-sets. Orders 52 through 60 in QR_79, and orders 52 through 66 in QR_83, are full four-set encodings. Both CP-SAT and CaDiCaL reject them, and the cardinality constraints alone are satisfiable. The independence number 27 at order 83 was not recomputed by the backtrack. The exclusion of orders 52 through 66 in QR_83 does not use that number; the unique-dominator bound there is 68 and does not reach those orders. Orders 67 and 68 inside QR_83 were not searched. The run does not decide whether QR_83 has S_4, because four-sets containing 0 were not part of the empty-dominator count. The caps 49, 51, and 51 at orders 67, 71, and 79 are upper bounds on a proper induced subtournament with S_4. No example of those orders was built. The products C_3[C_13] and C_13[C_3] have order 39, fail S_4, and lie outside the window. Thirty-two of the sixty-four majority bases have a vertex of out-degree 3, and the constant copy of that vertex has in-degree 0 in the product. The other thirty-two bases have maximum out-degree 2 and their products still fail S_4. The abstract at doi 10.5281/zenodo.23269759 describes a Cayley search on the odd-order groups from 47 through 65 and states that the bounds 48 <= f(4) <= 67 are unchanged. That dataset was not executed. The odd-order circular tournaments are single Cayley connection sets, settled here by the gap argument. Even-order circular tournaments and induced Paley subtournaments lie outside that Cayley statement. Paley orders 47 and 59 were not re-censused. One recorded set in each was used to check the edge orientation. The lower bound f(4) >= 52 is an input of the task and is not re-proved. Tournaments outside the families named here were not searched. Re-running the censuses requires a short program; the counts, witnesses, independent sets, and solver outcomes are the record of the run.

<!-- task:R4-G-degree-24 -->
### R4-G-degree-24 — proved (unreviewed)

The no-in-degree-23 lemma is accepted. In a tournament on 52 vertices in which every triple has at least 5 dominators, no in-degree equals 23. A vertex of in-degree 24 need not exist: twenty-six in-degrees 25 and twenty-six in-degrees 26 already sum (in-degree minus 25) to 26. Whether or not an in-degree 24 occurs, some triple has at least 7 dominators. If every triple had at most 6 dominators, the sum of C(|D(Y)|, 2) would equal 5 times the sum of |D(Y)| minus 331500, while the common-out-neighbour count is at least 1158 larger. Erdős problem 902 is not solved.

Weakness: The status proved covers the acceptance of the no-in-degree-23 count and the uniform 7-dominator bound. Step 4 of that count uses J >= 3. That bound is the argument in research/AGENT_TASKS/R1-G-audit-every-n.report.json, used here as an input and not rewritten. (SF) is taken from the completed proof in section 3 of proof/swarm/r1_AUDIT-52-B.md; the introduction of that file claims several later theorems, and those claims are not evidence because the file stops during section 3. Claim Q is an input: the comparison uses z <= 5, and it does not use the stronger sentence that each vertex of Z has at most two in-neighbours in Z. The same arithmetic still forces a 7-dominator triple for every z <= 8, and the formal difference becomes negative at z = 9, so the appeal to Claim Q has room, but without some upper bound on z the comparison does not close. The convex lower bound L uses only the sum of the common-out sizes. Extra constraints can only raise the sum of C(c, 3), so they do not weaken the contradiction, and 1158 is not asserted to be the gap of a realized tournament. No tournament was enumerated, Landau's condition was not needed, and the J = 3, 4 tree was not reopened. A tight pair at order 52 remains possible. Erdős problem 902 is not solved, and f(4) is not evaluated.

<!-- task:R5-B-outsets -->
### R5-B-outsets — proved (unreviewed)

The margin survives the out-neighbourhood count. The out-set of a vertex of out-degree 26 is a tournament on 26 vertices with score sequence thirteen 12s and thirteen 13s, so it contains 1872 transitive triples. With the 12-regular out-sets of the vertices of out-degree 25, the sum of the dominator counts over transitive triples is 91572. The seven recorded rows fall short of that sum by 298. The same degree pattern and pair-excess pattern still admit an integer solution in which every triple has at least 5 dominators and the transitive sum is 91572. Erdős problem 902 stays open.

Weakness: The status proved applies to the counting equations of the margin (26, 338, 5) after the out-neighbourhood sum is imposed. The repaired rows assign nonnegative integers to those equations, and every triple in them has at least 5 dominators. They do not specify the arcs of a tournament, and they do not place a particular set of 1872 transitive triples inside one named out-set. The seven rows of the previous report remain incompatible with the sum 91572; survival uses the replacement above. The sign comparison that forbids minimum 6 is the one already written for this degree pattern and pair-excess pattern. Degree sequences with square-sum greater than 26 stay outside the argument. Erdős problem 902 stays open, and f(4) is not evaluated.

<!-- task:R5-C-pattern -->
### R5-C-pattern — proved (unreviewed)

The common-in-neighbour numbers c(A,B) = 4 and c(C,D) = 0 occur in a 5-regular tournament on 11 vertices. The recorded tournament uses vertices 0 through 10, with A = 0, B = 1, C = 2, and D = 3. Its out-sets are in the evidence. The six positive counts, in the order (A,B), (A,D), (A,C), (B,C), (B,D), (C,D), are 4, 3, 2, 2, 3, 0. Those two forced values occur, and the other four lie in the windows compatible with dominator counts 16, 14, 13, 13, 12, 12. Every common-in-neighbour count from {A,B,C,D} into {4,5,6,7,8,9,10} is at most 3. The construction stops at these eleven vertices. f(4) >= 52 is not proved, and Erdős problem 902 is not solved.

Weakness: The result is existence of one tournament, read off its out-sets. The out-sets were located by a constraint search; the proof is the inspection of the lists, and the search is not a step in that inspection. The 551 isomorphism classes of 5-regular tournaments on 11 vertices were not listed, and the report does not claim that the common-in-neighbour tuple is unique. The dominator counts, the excesses E_both, the budgets Ex, and the bound c ≤ 3 on pairs into V_0 are inputs from the R4-C report. That report takes J = 5 and s = 4 from earlier reports in the same agent role. Those bounds are not re-proved here. The two heavy vertices and the 37 light vertices are unassigned, so a tight pair on 52 vertices is neither built nor excluded. f(4) >= 52 is not proved, and Erdős problem 902 is not solved.

<!-- task:R5-F-three -->
### R5-F-three — proved (unreviewed)

Three nested common-in-neighbourhood deletions leave the coefficient of log2 log2 N equal to 1. For stage lengths s1, s2, s3 and out-degree excesses δi, the count produces γ ≤ log2 N + Π − log2(log2 N − s_eff) + C + o(1), where Π ≥ 0 and 0 ≤ s_eff ≤ s1 + s2 + s3. That expression is at least the one-level bound log2 N − log2 log2 N + C + o(1). It never has the shape log2 N − 2 log2 log2 N + O(1), because that would require log2 N − s_eff at least a constant times (log2 N)^2, while log2 N − s_eff is at most log2 N. Inverted, the lower estimate of f(n) stays of the shape (c + o(1)) n 2^n. Erdős problem 902 is not solved.

Weakness: The status proved applies only to this negative statement: three nested deletions do not change the coefficient. The shape of B is taken from the one-level bound and is not re-proved. The o(1) needs the order tending to infinity and each stage length o of the square root of the current order; outside that range the remainder is capped and the count falls back to B. The argument says nothing about a one-step count of every n-set. A tournament with a very small in-neighbourhood can satisfy a stronger numerical bound, and that bound is not available for a regular tournament, so it does not improve f(n). The constant in front of n 2^n is whatever constant B already carries. Erdős problem 902 stays open, and f(4) is not evaluated.

<!-- task:R5-G-push -->
### R5-G-push — proved (unreviewed)

The weight equations do not force a triple with at most 4 dominators. On the extreme score sequence of five in-degrees 24, forty-five in-degrees 25, one in-degree 40 and one in-degree 41, the handshaking identities admit an explicit integer solution in which every triple level is at least 5 and the dominator counts are 16717 fives, 16 sixes, 2702 sevens and 2665 elevens. The common-out cubic moment is 370727, which is 42677 above the value attainable by counts in {5, 6}, and that excess is carried by the sevens and the elevens. Erdős problem 902 is not solved.

Weakness: The status proved applies to one integer solution of the star sums, the level formula, and the second-moment identity on the extreme score sequence. The common-out numbers are constant on the cuts of a realizable degree pattern. They are not shown to be the intersection sizes of the out-sets, so the solution is not a tournament. The dominated-side moment sum C(nu,2) is required to equal sum C(lambda,3)=388592, and the third-moment symmetry sum C(k,3)=sum C(nu,3) is required as well. Neither identity is solved here. A failure of those two identities would be a later step; it is not a proof that some triple has at most 4 dominators. The convex gap 1158 is used only as the input lower bound. This solution sits 41519 above the convex value 329208, because the stars of the in-degrees 40 and 41 cannot carry common-out counts 12 and 13. The balanced margin (26, 338, 5) is not rebuilt. No appeal is made to a tight pair or to the J=3, 4 tree. Erdős problem 902 is not solved, and f(4) is not evaluated.

<!-- task:R6-B-s4 -->
### R6-B-s4 — inconclusive (unreviewed)

Property S_4 on 52 vertices is not contradicted by the identities recorded in research/LEMMAS.md or the round-4 and round-5 reports. The missing identity is sum_{|X|=4} |D(X)| = sum_v C(d^+(v), 4). Erdős problem 902 is not solved.

Weakness: The status inconclusive belongs to the decision that the recorded identities do not contradict S_4, together with the naming of the missing four-set equation. It is not a construction of an S_4 tournament on 52 vertices, and it is not a proof that no such tournament exists. The comparison 717600 > 270725 uses the double count in the proof of Lemma S1 one binomial degree higher; that four-set sentence is not written in research/LEMMAS.md or the round-4 and round-5 reports. The explicit four-set solution for 730730 assigns nonnegative integers. It does not specify arcs, and it does not use the R5-B rows. The convex lower bound 730730 is the minimum of sum C(μ, 4) for the equality score sequence; other score sequences were checked only at the extreme common-out table of R5-G. The equation sum C(|D(X)|, 3) = sum C(ν(Y), 4) is not decided. R4-C remains conditional on J = 5 and s = 4, and R5-C stops at eleven vertices. R4-D excludes named families only. The upper bound f(4) ≤ 67 was not re-proved. Three-level deletion was not used. Erdős problem 902 is not solved, and f(4) is not evaluated.

<!-- task:R6-C-heavy -->
### R6-C-heavy — proved (unreviewed)

The two heavy vertices of the J = 5, s = 4 pattern cannot sit against the recorded 5-regular tournament on vertices 0 through 10. With A, B, C, D = 0, 1, 2, 3, the zero-excess vertices are 4, 5, 6, 7, 8, 9, 10. Vertices 6 and 9 have exactly four common in-neighbours, namely 2, 4, 7, 8. The vertex of q = 11 beats nobody in the eleven, and the vertex of q = 8 beats only {0, 2, 3}, so both are out-neighbours of 6. The ten pair excesses at 6 then sum to 10 and are at least 14. The same gap holds at 9. The edge between the two heavy vertices is unused. A different tournament on eleven vertices is not excluded. f(4) >= 52 is not proved, and Erdős problem 902 is not solved.

Weakness: The obstruction is special to this edge list. The pair {6, 9} was found by reading the common-in-neighbour counts on the 21 pairs inside {4, 5, 6, 7, 8, 9, 10}; the proof is the reading of the out-sets and the budget arithmetic, and the scan is not a step in that reading. The 551 isomorphism classes of 5-regular tournaments on 11 vertices were not listed. A different tournament with the positive counts 4, 3, 2, 2, 3, 0 and with every zero-excess pair at most 3 may still accept the same two heavy vertices. The degree excesses 2, 1, 1, 1 and the heavy types q = 11 and q = 8 missing {0, 2, 3} are the pattern recorded in the R4-C report. That report depends on J >= 5 and s >= 4 from earlier reports in the same agent role, and those bounds are not rebuilt here. (F1) is derived above from S_4; the rest of the order-52 case tree is not. The 37 light vertices are unassigned because the budget at 6 has already failed. f(4) >= 52 is not proved, and Erdős problem 902 is not solved.

<!-- task:R6-G-nu -->
### R6-G-nu — proved (unreviewed)

On the extreme score sequence, with the recorded pair table and the recorded level assignment, nonnegative integers nu = L - k exist with every dominator count at least 5, sum k = 131910, sum C(k, 2) = 370727, sum C(nu, 2) = 388592 and sum C(k, 3) = sum C(nu, 3). Each dominated count in the rows is at most the out-degree room of its triple. The dominator counts 16717, 16, 2702 and 2665 cannot meet the third-moment identity. Erdős problem 902 is not solved.

Weakness: The proved statement is an integer table on one pair table and one cyclic placement: all of GNN, all of NNN, and 20 triples of HNN. The common-out numbers are constant on the cuts of the degree pattern. The table does not identify them with intersection sizes of out-sets. Two classes use a third dominator value on a single triple, one in hHH and one in HHG, and those singles are part of the checked total. The multiplier bound rules out the counts 16717, 16, 2702 and 2665. It leaves other dominator counts open, and the exhibited counts are one point that works. The out-degree room is the most generous orientation bound; a fixed orientation inside a class could be tighter. The weight minimum, the balanced margin and the J = 3, 4 tree are untouched. Erdős problem 902 is not solved, and f(4) is not evaluated.

<!-- task:R6-H-strategy -->
### R6-H-strategy — inconclusive (unreviewed)

The next round has two tasks, and the round after it has one. Round 7 decides the four-set cubic identity on the equality margin (26, 338, 5), and it tests one 5-regular tournament on 11 vertices that keeps the J=5, s=4 counts and keeps every pair of zero-excess vertices at most 3 common in-neighbours. Round 8 runs the pair and triple identities at J=5 and s=5. The bound f(4) >= 52 stays checked, the bound f(4) <= 67 stays unchanged, the pair and triple moments stay compatible with every triple having at least 5 dominators, and three-level deletion stays closed. Erdős problem 902 is not solved.

Weakness: This is a strategy. It proves no bound and it exhibits no tournament. The three round-6 reports were read from disk and are not yet ledger entries. J >= 5 and s >= 4 remain conditional on unreviewed reports in the same agent line. A four-set solution on the equality margin leaves the extreme score sequence untouched, and an exclusion on that margin leaves every other score sequence untouched. One 11-vertex tournament can meet the zero-excess condition and still reject the two heavy vertices, and acceptance of those two vertices would leave the 37 light vertices unassigned. A proof that no such tournament exists does not by itself close J=5 and s=4. The s=5 task does not treat J >= 6. Erdős problem 902 is not solved, and these three tasks do not determine f(4).

<!-- task:R7-C-avoid -->
### R7-C-avoid — proved (unreviewed)

No 5-regular tournament on 11 vertices can carry the J = 5, s = 4 pattern of R4-C, because that pattern forces c(C, D) = 0 while T[R] has property S_2, so every pair of R has at least one common in-neighbour in R. The cell J = 5, s = 4 is empty. The tournament of R5-C has c(2, 3) = 0, is not S_2, and cannot be T[R]. Together with a hand treatment of J = 5, s = 5, every tight pair in an S_4 tournament on 52 vertices has J >= 6. Erdős problem 902 is not solved.

Weakness: J >= 6 uses R1-C (J >= 5) for s <= 3 and the R4-C case tree for s = 4 as hand inputs; both are independently reproduced by the CP-SAT pair-level model, which is one implementation by one author. Lemma A is used; its proof (rounding modulo 4 at a vertex with j = 0) was re-read for N = 52. The CP-SAT verdicts are solver outputs without exported certificates. Tight pairs with 6 <= J <= 14 are not excluded, and the no-tight branch at order 52 is untouched. f(4) >= 53 is not proved and Erdős problem 902 is not solved.
<!-- END GENERATED LEMMAS -->
