# Research state

Erdős 902 is open. No resolution is recorded in `FINAL_PROOF.md`.

The published shape of the problem is \(n 2^n \ll f(n) \ll n^2 2^n\), with \(f(1)=3\), \(f(2)=7\), \(f(3)=19\). Inside this workspace, `proof/verify_proof.py` was rerun on 23 October 2026 with 0 failures. That confirms the numerical parts of `proof/ERDOS902_PROOF.md`, including \(c^\ast = 0.7695032191504894326990652683098231346767\), the explicit table through \(n = 12\), \(S_4\) for the Paley tournament of order 67, and the failure of Claim L. It does not confirm the hand argument for \(f(4) \ge 52\).

Lemma S1, Lemma I, and Lemma J are recorded in `LEMMAS.md`. Lemma J is the bound \(J \ge 3\) for every tight pair; the printed every-order paragraph is incomplete, and the replacement argument has been checked on its new steps. The doubly regular order-51 moment argument has been re-derived and stops short of \(f(4) \ge 52\). The Paley tournament of order 47 shows that "at most 3 dominators" is false and that "at most 4" is tight on that example. The next obstacle is the unaudited case split \(J = 3\) and \(J = 4\) at order 52.

## Resume

From the repository root, after a crash or a new session:

```text
python research/orchestrator.py resume
python research/orchestrator.py status
python research/orchestrator.py plan-round
```

`resume` ingests any report file that landed in `research/AGENT_TASKS/` and returns a dispatch older than 45 minutes to the queue. It leaves a younger dispatch alone, so a second process does not duplicate a live agent. The controller is single-writer. Cursor cannot keep Task subagents alive after the IDE or the machine stops; the checkpoint can. A round that hits the daily budget is paused, not declared finished.

`python research/orchestrator.py mock-round` runs the failure drill in a scratch directory and refuses to run against this repository.

## Next actions

1. Audit the \(J = 3\) and \(J = 4\) case split at order 52 (`R1-C-n52-j-le-2`, retargeted after Lemma J).
2. One equivalent formulation of the order-52 problem that is not a known counting barrier (`R1-F-reformulation`).
3. Rank the next round from the reports (`R1-H-strategy`).

<!-- BEGIN GENERATED STATE -->
solved: false
round: 8
rounds_started_today: 4 on 2026-10-24
exhausted_approaches: 7

| id | role | status | attempts | verification |
|---|---|---|---|---|
| R1-A-literature | A | completed | 0 | unreviewed |
| R1-B-theorem5 | B | completed | 0 | arithmetic_agrees |
| R1-C-n52-j-le-2 | C | completed | 0 | case_tree_recomputed |
| R1-D-counterexample | D | completed | 0 | independently_recomputed |
| R1-E-checks | E | completed | 0 | reproduced_by_orchestrator |
| R1-F-reformulation | F | completed | 0 | unreviewed |
| R1-G-audit-every-n | G | completed | 0 | skeleton_checked |
| R1-H-strategy | H | completed | 0 | unreviewed |
| R3-C-four-positive | C | completed | 0 | unreviewed |
| R3-D-case-I | D | completed | 0 | arithmetic_agrees |
| R3-F-order-52 | F | completed | 0 | arithmetic_agrees |
| R3-G-break-52 | G | completed | 0 | line_checked |
| R4-B-no-tight | B | completed | 0 | moments_recomputed |
| R4-C-tight-s4 | C | completed | 0 | unreviewed |
| R4-D-upper | D | completed | 0 | circular_witnesses_recomputed |
| R4-G-degree-24 | G | completed | 0 | weight_minimum_recomputed |
| R5-B-outsets | B | completed | 0 | transitive_sum_recomputed |
| R5-C-pattern | C | completed | 0 | tournament_recomputed |
| R5-F-three | F | completed | 0 | unreviewed |
| R5-G-push | G | completed | 0 | unreviewed |
| R6-B-s4 | B | completed | 0 | four_set_count_recomputed |
| R6-C-heavy | C | completed | 0 | obstruction_recomputed |
| R6-G-nu | G | completed | 0 | unreviewed |
| R6-H-strategy | H | completed | 0 | unreviewed |
| R7-B-cubic | B | pending | 1 |  |
| R7-C-avoid | C | completed | 0 | unreviewed |
| R8-A-audit-j5 | G | dispatched | 0 |  |
| R8-B-no-tight | B | dispatched | 0 |  |
| R8-C-s5 | C | pending | 0 |  |
| R8-D-spectral | F | dispatched | 0 |  |
| R8-E-independent | E | dispatched | 0 |  |
| R8-F-asymptotic | A | dispatched | 0 |  |
| R8-G-construct | D | dispatched | 0 |  |
<!-- END GENERATED STATE -->
