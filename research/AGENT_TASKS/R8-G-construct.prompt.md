Task id: R8-G-construct
Role: D
Approach key: upper-local-search-structured-52
Relation to prior work: R4-D excluded named algebraic families. This task runs targeted local search over general tournaments, seeded with the order-52 structure forced by the lower-bound analysis (score sequence 25/26), which no previous task did.

Write one JSON object to:
C:\Users\vitta\OneDrive\Desktop\stochastic optimization\research\AGENT_TASKS\R8-G-construct.report.json

Do not edit files under proof/. Do not edit research/FINAL_PROOF.md.
Do not declare Erdős 902 solved. A status of proved is stored as unreviewed.
Use inconclusive when you have a partial result. Use failed only if you could not start.
Required keys: task_id, agent, claim, status, definitions, argument, evidence, weaknesses, references, next_step, relation_to_prior, novelty.
status is one of proved, disproved, conditional, failed, inconclusive, computed.
task_id must be R8-G-construct. agent must be D.
Exhausted approach keys, which this task must not repeat: claim-L-single-pair-link, one-level-counting-past-cstar, two-stage-averaging-second-log, random-cayley-beat-erdos-upper, n51-local-milp-certificates, wrong-direction-covering-local48, three-level-count-second-log.

Read research/AGENT_TASKS/BRIEF_R8.md first. You try to break the conjecture f(4) >= 53 and to improve f(4) <= 67. Deliverables:
1. Write a fast exact S_4 checker (C compiled with gcc if available, otherwise numpy bitsets) that counts undominated 4-sets and also reports the minimum number of dominators over pairs and triples. Validate it on the Paley tournament QR_67 (S_4) and QR_47, QR_59 (not S_4).
2. Run a local search (simulated annealing or tabu on arc reversals, cost = number of undominated 4-sets plus penalties for triples with < 5 dominators) on N = 52, seeded by (a) random tournaments with in-degrees 25/26, (b) QR_67 minus 15 vertices chosen to keep regularity, (c) doubly-regular-like circulants on Z_52 or Z_53 minus a vertex. Also run N = 60, 63, 66. Budget: at most 3 cores, at most 90 minutes total.
3. Report the best cost found per N with the tournament saved (research/compute/r8g_best_N.txt, adjacency rows), and the profile (min pair dominators, min triple dominators). If any tournament with S_4 on fewer than 67 vertices is found, verify it with a second independent checker and save it; that would be a counterexample candidate. A failure to find one is only weak evidence.
Write research/AGENT_TASKS/R8-G-construct.report.json.
