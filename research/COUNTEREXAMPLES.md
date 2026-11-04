# Counterexamples and failed claims

A construction is entered here only when it meets every hypothesis of the claim it is supposed to kill and violates the conclusion. A search that found nothing is a search record in `LEDGER.md`, not a counterexample.

## Claim L is false

**Claim (false).** In a doubly regular tournament of order 51, fix one pair and its 12 common in-neighbours \(X\). The claim asserted that no 12-vertex tournament on \(X\) and no family of 37 subsets \(N_u \subseteq X\) can satisfy the Gram identities together with the local \(S_4\) conditions (i)–(v) listed in `proof/ERDOS902_PROOF.md` §8.2.

**Counterexample.** The realisation constructed by `ai-debate/claim_l_intersect.py`: the tournament on \(X\) is the Paley tournament of order 11 plus a twelfth vertex that beats 6 of the others. There are 37 sets \(N_u\), of sizes 5, 6, 8 and 9.

**Check.** `proof/verify_proof.py` check V7 confirms the Gram matrix and (i)–(v). It was rerun on 23 October 2026 from this workspace: `logs/verify_proof_rerun_20261023.out`, exit 0, "Failures: 0", row sizes `[5, 6, 8, 9]`, identity total 1596. Runtime of the whole script 66 seconds.

**What it does not say.** It does not say that a doubly regular tournament of order 51 with \(S_4\) exists. It says that a test which looks at a single pair, and not at how the links of different pairs fit together, cannot decide the question.

## "At most 3" is too strong

**False sentence.** Every tournament on at most 51 vertices has a triple with at most 3 dominators.

**Counterexample.** The Paley tournament of order 47: vertices are residues modulo 47, and \(i \to j\) when \(j-i\) is a nonzero quadratic residue. The triple \(\{0,1,3\}\) has exactly four dominators, \(23, 41, 44, 46\). An enumeration of all \(\binom{47}{3}\) triples finds no triple with fewer than 4 dominators. The 4-set \(\{0,1,3,38\}\) has no dominator, so this tournament does not have \(S_4\).

**Checks.** `research/compute/exact_checks.py` (bit masks) and a separate residue-by-residue enumeration both give minimum 4 on \(\{0,1,3\}\) and the same four dominators, and both find the undominated 4-set. The report `research/AGENT_TASKS/R1-D-counterexample.report.json` lists the same dominators from the residues. The histogram in that report was not recomputed here.

**What it does not say.** The strong claim with 4 in place of 3 is compatible with this tournament, because the minimum is exactly 4. It does not decide \(f(4)\).

## Approaches exhausted before this controller existed

These are recorded so later tasks cannot reopen them under the same approach key. Detail is in `LEDGER.md`.

| approach key | outcome |
|---|---|
| `claim-L-single-pair-link` | Disproved by the realisation above. |
| `one-level-counting-past-cstar` | The dominator double count stops at the constant \(c^\ast\). See `proof/FN_EXPLICIT_BOUNDS.md`. |
| `two-stage-averaging-second-log` | Does not change the coefficient of the second logarithm. See `proof/FN_GAP_ATTEMPT.md`. |
| `random-cayley-beat-erdos-upper` | Treated in this repository as a barrier for random symmetric constructions. The source note cited by `FILE_INDEX.md` is not in the workspace; the key stays closed until a new construction is specified. |
| `n51-local-milp-certificates` | Superseded, for the \(N=51\) local claim, by the hand argument in `proof/F4_GE_52_HAND_PROOF.md`. Re-running the 551-class MILP is not a new approach. |
| `wrong-direction-covering-local48` | `FILE_INDEX.md` marks `local48.c` and its siblings as using the wrong covering direction. |

<!-- BEGIN GENERATED COUNTEREXAMPLES -->
<!-- task:R1-D-counterexample -->
### R1-D-counterexample — disproved (unreviewed)

The sentence 'every tournament on at most 51 vertices has a triple with at most 3 dominators' is false. The Paley tournament of order 47 is a counterexample: the minimum of |D(Y)| over its 16215 triples is 4, attained by {0,1,3}, whose dominators are 23, 41, 44 and 46. The strong claim in proof/F4_GE_52_HAND_PROOF.md, whose bound is 4 rather than 3, is consistent with this tournament, because that triple has exactly 4 dominators. The same tournament has undominated 4-sets, including {0,1,3,38}, so it does not have S_4 and does not decide whether f(4) >= 52.

Weakness: This kills the strengthening with 3. It leaves the strong claim with 4 untouched: 4324 triples in this tournament have exactly 4 dominators, so the tournament is not a counterexample to that claim, and a failed search is not evidence that the strong claim is true. The count over all triples is a machine enumeration, repeated with two implementations that agreed; the four dominators of {0,1,3} were also listed by hand from the residues. The Paley profiles of orders 7, 11, 19, 23, 31, 43 and 67 were taken from research/AGENT_TASKS/R1-E-checks.report.json and were not re-enumerated. In that report their minimum numbers of triple dominators are 0, 0, 1, 1, 2, 3 and 6, so none of the orders at most 51 meets the condition that every triple has at least 5 dominators. Orders 48, 49, 50 and 51 have no Paley tournament. No other construction on 47-51 vertices was examined. The optional search for an integer pattern of (q_y) and (j_r) at N = 52 with J <= 2 was not carried out. Claim L was not reopened.
<!-- END GENERATED COUNTEREXAMPLES -->
