Task id: R8-A-audit-j5
Role: G
Approach key: n52-audit-j-le-5-chain
Relation to prior work: Audits research/N52_TIGHT_J_GE_6.md, R1-C and R3-C, and the soundness of research/compute/n52_pairlevel.py. None of these has had a second reader.

Write one JSON object to:
C:\Users\vitta\OneDrive\Desktop\stochastic optimization\research\AGENT_TASKS\R8-A-audit-j5.report.json

Do not edit files under proof/. Do not edit research/FINAL_PROOF.md.
Do not declare Erdős 902 solved. A status of proved is stored as unreviewed.
Use inconclusive when you have a partial result. Use failed only if you could not start.
Required keys: task_id, agent, claim, status, definitions, argument, evidence, weaknesses, references, next_step, relation_to_prior, novelty.
status is one of proved, disproved, conditional, failed, inconclusive, computed.
task_id must be R8-A-audit-j5. agent must be G.
Exhausted approach keys, which this task must not repeat: claim-L-single-pair-link, one-level-counting-past-cstar, two-stage-averaging-second-log, random-cayley-beat-erdos-upper, n51-local-milp-certificates, wrong-direction-covering-local48, three-level-count-second-log.

Read research/AGENT_TASKS/BRIEF_R8.md first. You are the adversarial auditor (Track 6). Deliverables, each with a verdict justified / gap / false and the exact line at fault:
1. Re-derive from the definitions, at N = 52: the identities (I1), Sum e_y = 14 - J, |D(u,v)| = c + #{y : u,v in M_y}, s(u,v) = 4|D| - c - 45 - E_both, Ex(u) formula, Sum_v s(u,v) = 2Ex(u). Then re-prove Lemma A at N = 52 (rounding modulo 4 at a vertex with j = 0, including the case of y with q_y in {7,8,9,10,11}). Then re-prove c(u,v) >= 1, stating every arc direction.
2. Audit research/N52_TIGHT_J_GE_6.md sections 1 and 2 line by line (the R4-C survivor kill and the J = 5, s = 5 hand proof, including the partition filter for heavy excess 9).
3. Audit the J <= 4 and s <= 3 parts: research/AGENT_TASKS/R1-C-n52-j-le-2.report.json (excluding J = 3 and J = 4) and research/AGENT_TASKS/R3-C-four-positive.report.json (s <= 3 at J >= 5). Either confirm each case or write a corrected argument for the case you find broken.
4. Read research/compute/n52_pairlevel.py and check that every constraint is a valid consequence of S_4 at N = 52 (variable domains included), and that the restriction of heavy miss-sets to V_+ is justified by Lemma A. List any row that is not justified.
Report status proved if the full chain J <= 5 impossible survives with your corrections, otherwise inconclusive with the precise gap. Write research/AGENT_TASKS/R8-A-audit-j5.report.json.
