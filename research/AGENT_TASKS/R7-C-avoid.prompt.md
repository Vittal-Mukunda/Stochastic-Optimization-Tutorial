Task id: R7-C-avoid
Role: C
Approach key: n52-zero-excess-pairs-c-at-most-3
Relation to prior work: The recorded 11-vertex tournament fails on the pair {6,9}. This asks for a tournament that avoids that pair.

Write one JSON object to:
C:\Users\vitta\OneDrive\Desktop\stochastic optimization\research\AGENT_TASKS\R7-C-avoid.report.json

Do not edit files under proof/. Do not edit research/FINAL_PROOF.md.
Do not declare Erdős 902 solved. A status of proved is stored as unreviewed.
Use inconclusive when you have a partial result. Use failed only if you could not start.
Required keys: task_id, agent, claim, status, definitions, argument, evidence, weaknesses, references, next_step, relation_to_prior, novelty.
status is one of proved, disproved, conditional, failed, inconclusive, computed.
task_id must be R7-C-avoid. agent must be C.
Exhausted approach keys, which this task must not repeat: claim-L-single-pair-link, one-level-counting-past-cstar, two-stage-averaging-second-log, random-cayley-beat-erdos-upper, n51-local-milp-certificates, wrong-direction-covering-local48, three-level-count-second-log.

You are the combinatorial researcher. Keep the six positive common-in-neighbour counts 4, 3, 2, 2, 3, 0 and the bound 3 on counts from {A,B,C,D} into the seven zero-excess vertices.
Find one 5-regular tournament on 11 vertices in which every pair inside those seven vertices also has at most 3 common in-neighbours, then apply the heavy-vertex budget: the ten pair excesses at a zero-excess vertex sum to 10, and a pair with c=4 inside that seven forces a lower bound summing to 14.
The recorded tournament fails on {6,9}. The orchestrator recomputed that count. If no tournament meets the condition, a counting obstruction is the claim. Do not list isomorphism classes. Do not declare Erdős problem 902 solved.
