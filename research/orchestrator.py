"""Persistent controller for the Erdős 902 research record.

The checkpoint is the source of truth. Agent transcripts are not.
A proved claim is stored as unreviewed and does not close the problem.

    python research/orchestrator.py init
    python research/orchestrator.py status
    python research/orchestrator.py plan-round
    python research/orchestrator.py resume
    python research/orchestrator.py mock-round
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import time
from datetime import date, datetime, timezone
from pathlib import Path

DEFAULT_ROOT = Path(__file__).resolve().parents[1]
BEGIN_STATE = "<!-- BEGIN GENERATED STATE -->"
END_STATE = "<!-- END GENERATED STATE -->"
BEGIN_LEMMAS = "<!-- BEGIN GENERATED LEMMAS -->"
END_LEMMAS = "<!-- END GENERATED LEMMAS -->"
BEGIN_COUNTER = "<!-- BEGIN GENERATED COUNTEREXAMPLES -->"
END_COUNTER = "<!-- END GENERATED COUNTEREXAMPLES -->"

DEFAULT_CONFIG = {
    "problem_id": "erdos-902",
    "max_concurrent_agents": 4,
    "max_attempts_per_task": 3,
    "backoff_seconds_base": 30,
    "agent_timeout_seconds": 2700,
    "max_rounds_per_day": 8,
    "max_compute_seconds": 180,
    "max_checkpoint_backups": 100,
}

EXHAUSTED_PRIORS = [
    "claim-L-single-pair-link",
    "one-level-counting-past-cstar",
    "two-stage-averaging-second-log",
    "random-cayley-beat-erdos-upper",
    "n51-local-milp-certificates",
    "wrong-direction-covering-local48",
]

ALLOWED_STATUS = {"proved", "disproved", "conditional", "failed", "inconclusive", "computed"}
NONEMPTY_FIELDS = (
    "task_id", "agent", "claim", "status", "definitions", "argument",
    "evidence", "weaknesses", "next_step", "relation_to_prior", "novelty",
)

PROMPTS = {
    "R1_literature": """
You are the literature researcher. Read research/PROBLEM.md and research/LITERATURE.md.
Establish the published state of Erdős problem 902 (Schütte's tournament problem).
Check Erdős 1963, Szekeres–Szekeres 1965, Graham–Spencer 1971, Reid–McRae–Hedetniemi–Hedetniemi 2004, the current page https://www.erdosproblems.com/902, and its proof-claims thread.
Separate four classes: published theorem, website commentary, preprint or code repository, and a claim that exists only in this workspace.
In particular locate whether f(4) >= 51, f(4) >= 52, and the constant c* ≈ 0.7695 appear outside this workspace.
If a source cannot be opened, mark that item UNVERIFIED. Do not fill the gap from memory and call it checked.
This is new relative to research/LITERATURE.md because that file records a timed-out page fetch and an empty Semantic Scholar response.
""".strip(),
    "R1_audit_every_n": """
You are the independent proof auditor. Read proof/F4_GE_52_HAND_PROOF.md, section 2, especially the paragraph that begins "Theorem 1 holds for every N, not only N = 51."
The N = 52 notes in proof/N52_TIGHT_PAIRS.md cite that paragraph for J >= 3 at every order, and then claim J >= 5.
Decide whether the paragraph is a complete proof, an incomplete proof, or a false proof. Name the first inference that is not justified, if there is one.
Re-derive the counting yourself. research/LEMMAS.md Lemma I and Lemma S1 are available as inputs only after you check that their hypotheses match the step where you use them.
Do not repair the paragraph and then declare the original text a proof. A repair is your own argument: write it in full and mark it proved or conditional.
The N = 51 argument and the every-order paragraph are different tasks. Say which one your verdict covers.
Do not use a computer. This audit is new because the paragraph has not been audited; the earlier verifier only checks proof/ERDOS902_PROOF.md.
""".strip(),
    "R1_theorem5": """
You are the pure mathematician. Re-derive the claim that every doubly regular tournament on 51 vertices has some triple with at most 4 dominators.
Definition you must use: every in-degree and out-degree is 25, and every two distinct vertices have exactly 12 common in-neighbours.
Write the identities you need before relying on proof/F4_GE_52_HAND_PROOF.md section 4. Then read that section and mark every step you cannot justify.
The third-moment comparison has to be complete. This task is not the N = 52 question and it is not a request to rerun the superseded MILP certificates.
""".strip(),
    "R1_counterexample": """
You are the counterexample researcher. The strong claim in proof/F4_GE_52_HAND_PROOF.md says every tournament on at most 51 vertices has a triple with at most 4 dominators. That claim implies f(4) >= 52. A tournament on 47, 48, 49, 50 or 51 vertices in which every triple has at least 5 dominators falsifies the strong claim and that proof. It falsifies f(4) >= 52 only if the same tournament has S_4.
Orders below 47 are impossible for the triple condition, by the Szekeres bound, so do not search them.
Read the Paley profiles produced by research/compute/exact_checks.py. If one of them is a candidate, recompute the witness. If none is, state the exact orders and constructions you checked and stop. A failed search is not evidence the claim is true.
You may also look for an integer pattern of (q_y) and (j_r) at N = 52 with J <= 2 that meets the identities you can prove and avoids a contradiction. Record it if you find one.
Do not repeat approach key claim-L-single-pair-link. That counterexample is already in research/COUNTEREXAMPLES.md.
""".strip(),
    "R1_n52_j_le_2": """
You are the combinatorial researcher. Do not try to prove J <= 2. Agent G's report
research/AGENT_TASKS/R1-G-audit-every-n.report.json gives an argument that every tight pair in every S_4 tournament has J >= 3. Treat that bound as an input you may use, and do not rewrite it.
Your target is sections 3 and 4 of proof/N52_TIGHT_PAIRS.md, the case analysis that excludes J = 3 and J = 4 at N = 52 and concludes J >= 5. Audit it. Either write a complete proof of J >= 5 at N = 52, or name the first case in those sections that does not follow.
This is new relative to G's audit: G stopped before sections 3 and 4. It is also not the exhausted MILP classification.
""".strip(),
    "R1_reformulation": """
You are the alternative-formulation researcher. Give one equivalent formulation of "no tournament on 52 vertices has S_4" that is different from the dominator-minimum sentence and different from the counting barriers in proof/FN_GAP_ATTEMPT.md and proof/FN_EXPLICIT_BOUNDS.md.
State the hypotheses the equivalence uses. If you only find a relaxation, label it a relaxation and say what it drops.
Do not propose another one-level counting argument past c*, and do not propose a single-pair link test.
""".strip(),
    "R1_strategy": """
You are the research strategist. Read research/LEDGER.md, research/LEMMAS.md, research/STATE.md and the report files in research/AGENT_TASKS/.
Rank the unresolved obstacles by how directly they block a proof or a counterexample.
Propose the next round's tasks. Each task needs a new approach key and a sentence saying which previous failure it is not repeating.
Do not propose Claim L, one-level counting past c*, two-stage averaging, a random Cayley upper bound, or another classification of the 551 regular tournaments on 11 vertices.
Do not recommend stopping because the problem is hard.
""".strip(),
    "R3_break_52": """
You are the hostile auditor. The target sentence is: no tournament on 51 or fewer vertices has S_4, so f(4) >= 52.
Read proof/ERDOS902_PROOF.md section 2 and proof/F4_GE_52_HAND_PROOF.md sections 2 and 3, and the Lemma J argument in research/AGENT_TASKS/R1-G-audit-every-n.report.json.
Do not open any file under proof/swarm/.
Check the arc count in Corollary 3 yourself: for A = N^-(v), is sum_z |D_z| equal to sum_{x in A}(d^+(x) - 1)?
Name the first inference on the path to f(4) >= 52 that does not follow. If every inference you checked follows, say which block you did not finish.
A status of proved requires a complete argument in your own words. Do not declare Erdős problem 902 solved.
""".strip(),
    "R3_case_I": """
You are the counterexample researcher. At order 51, case (I) is the case 1 <= |Z| <= 5, where Z is the set of vertices of in-degree 24 and every other in-degree is at least 25.
Try to satisfy the hypotheses used in Corollary 3 of proof/F4_GE_52_HAND_PROOF.md while keeping J >= 3 on every tight pair. Either exhibit integer parameters that meet every cited identity and avoid the contradiction, or prove that the identities themselves forbid those parameters.
Do not open proof/swarm/. A failed search must name the identity that blocked it.
""".strip(),
    "R3_four_positive": """
You are the combinatorial researcher. Decide whether every tight pair in an S_4 tournament on 52 vertices has at least four dominators of in-degree greater than 25.
Audit sections 5 and 9 of proof/N52_TIGHT_PAIRS.md. You may use J >= 5 as a conditional input from research/AGENT_TASKS/R1-C-n52-j-le-2.report.json; do not rebuild the J = 3 and J = 4 tree.
proof/swarm/r1_AUDIT-52-B.md stops during section 3. Do not treat its introduction as a proof.
If a printed case fails, name it. Do not declare Erdős problem 902 solved.
""".strip(),
    "R3_order_52": """
You are the alternative-formulation researcher. Take the argument that an S_4 tournament on 51 vertices is doubly regular, and replace 51 by 52.
Find the first identity, corollary, or numerical bound that becomes false or inconclusive at order 52.
The useful output is that first failure, with the two numbers side by side. Do not repeat the exhausted counting arguments, and do not declare Erdős problem 902 solved.
""".strip(),
    "R4_degree_24": """
You are the hostile auditor. Lemma: in a tournament on 52 vertices where every triple has at least 5 dominators, no in-degree equals 23. The counting is proof/N52_ATTEMPT.md section 2, and the structural fact it uses is proof/swarm/r1_AUDIT-52-B.md section 3 only. The file ends during section 3; ignore the introduction's later claims.
Either name the first step of the no-in-degree-23 lemma that fails, or accept it. The sum of (in-degree minus 25) is 26, so a vertex of in-degree 24 need not exist: twenty-six 25s and twenty-six 26s already sum to 26. Derive one restriction that covers both the presence and the absence of in-degree 24, and that the existing notes do not already contain. Do not rebuild the J=3,4 tree. Do not declare Erdős problem 902 solved.
""".strip(),
    "R4_no_tight": """
You are the pure mathematician. Assume a tournament on 52 vertices in which every triple has at least 5 dominators and every pair has at least 12 dominators. The sum of (in-degree minus 25) is 26. Lemma S1 in research/LEMMAS.md gives sum (|D(P)|-12) >= 338.
Decide whether these hypotheses force some triple below 5 dominators. If they do not, give an integer margin: a triple of numbers (degree pattern, pair-excess pattern, triple-dominator lower bound) consistent with the handshaking identities. Do not assume every degree equals 25. That is the order-51 case already settled. Do not declare Erdős problem 902 solved.
""".strip(),
    "R4_tight_s4": """
You are the combinatorial researcher. At order 52, assume a tight pair with J >= 5 and at least four dominators of in-degree greater than 25. Those two inputs are conditional. Do not rebuild them.
Prove one new restriction on such a pair, or show that the identities still permit J = 5 and s = 4. A single surviving integer pattern, or a single contradiction that covers that pattern, is enough. Sections 5 and 9 of proof/N52_TIGHT_PAIRS.md are already the source of the conditional input; do not repeat their printed gaps. Do not declare Erdős problem 902 solved.
""".strip(),
    "R4_upper": """
You are the counterexample researcher. The checked lower bound is f(4) >= 52. The Paley tournament of order 67 has S_4. The Paley tournament of order 59 has triple minimum 5 and an undominated 4-set {0,1,7,19}, so it does not have S_4. That scan is in research/compute/paley59_result.json and was repeated from the quadratic residues.
Look for a tournament of order 52, 53, ..., 66 with S_4, or prove that one explicit family in that range fails S_4. A failed search must name the family and the witness. Do not repeat the order-47 Paley calculation. Do not declare Erdős problem 902 solved.
""".strip(),
    "R5_outsets": """
You are the pure mathematician. research/AGENT_TASKS/R4-B-no-tight.report.json gives an integer solution of the handshaking equations on 52 vertices in which every pair has at least 12 dominators and every triple has at least 5, with degree excesses twenty-six 0s and twenty-six 1s. The orchestrator checked that those seven (k, nu) rows reproduce the moments. The solution is not a tournament.
Use the out-neighbourhood of one vertex of out-degree 26. It is a tournament on 26 vertices. Derive a count inside that subtournament that the global solution does not have to satisfy, and decide whether the margin survives that count. If it survives, say so and stop. If it dies, name the count. Do not declare Erdős problem 902 solved.
""".strip(),
    "R5_push": """
You are the hostile auditor. At order 52, under the hypothesis that every triple has at least 5 dominators, the weight argument in research/AGENT_TASKS/R4-G-degree-24.report.json says some triple has at least 7 dominators. The orchestrator checked the weight minimum by dynamic programming and checked the gap 1158 on the extreme score sequence.
Push exactly one step past that statement. Either force some triple to have at most 4 dominators, or give an explicit integer solution of the same moment equations in which every triple has at least 5 dominators. Do not rebuild the weight minimum. Do not declare Erdős problem 902 solved.
""".strip(),
    "R5_pattern": """
You are the combinatorial researcher. research/AGENT_TASKS/R4-C-tight-s4.report.json leaves one pattern at J = 5 and s = 4: dominator counts 16, 14, 13, 13, 12, 12 on the positive vertices, with c(A,B) = 4 and c(C,D) = 0.
Decide whether those common-in-neighbour numbers can occur in a 5-regular tournament on 11 vertices. This is one numerical pattern, not a classification of the regular tournaments on 11 vertices. If the pattern is impossible, the obstruction is the claim. If it is possible, record one tournament on those 11 vertices. Do not declare Erdős problem 902 solved.
""".strip(),
    "R5_three": """
You are the alternative-formulation researcher. Read proof/FN_GAP_ATTEMPT.md only far enough to see the one-level bound and the two-stage bound.
Attempt a three-level count for f(n). If the coefficient of the second logarithm is unchanged, that negative result is the claim, and you should stop. Do not repeat a one-level count past c* and do not repeat two-stage averaging. Do not declare Erdős problem 902 solved.
""".strip(),
    "R6_nu": """
You are the hostile auditor. In research/AGENT_TASKS/R5-G-push.report.json the extreme score sequence has an integer solution with every triple level at least 5, and the report says sum C(nu, 2) was not matched to sum C(lambda, 3) = 388592.
Decide that one identity. Either give nonnegative nu = L - k meeting both sum C(nu, 2) = 388592 and sum C(k, 3) = sum C(nu, 3), or prove no such integers exist. Do not rebuild the weight minimum. Do not declare Erdős problem 902 solved.
""".strip(),
    "R6_heavy": """
You are the combinatorial researcher. The tournament in research/AGENT_TASKS/R5-C-pattern.report.json is 5-regular on vertices 0..10, with A,B,C,D = 0,1,2,3 and common-in-neighbour counts 4,3,2,2,3,0. The orchestrator recomputed those counts.
Place the two heavy vertices of the J=5, s=4 pattern, one of q=11 and one of q=8 missing {A,C,D}, or prove they cannot sit against this tournament. This is two vertices, not a search of all 52. Do not declare Erdős problem 902 solved.
""".strip(),
    "R6_s4": """
You are the pure mathematician. The equations under the triple hypothesis at order 52 still allow every triple at least 5 dominators. Property S_4 asks for a dominator of every 4-set, which is a stronger demand.
Using only identities already recorded in research/LEMMAS.md and the round-4 and round-5 reports, decide whether S_4 at order 52 is already contradicted. If it is not, name the missing identity in one sentence. Do not repeat the three-level deletion; that approach is exhausted. Do not declare Erdős problem 902 solved.
""".strip(),
    "R6_strategy": """
You are the research strategist. Read research/LEDGER.md, research/LEMMAS.md, and research/STATE.md.
f(4) >= 52 is checked. f(4) <= 67 is unchanged. The moment equations at order 52 do not force a triple below 5. Three-level deletion is exhausted.
Propose exactly two tasks for the next round and one task for the round after that. Each needs a new approach key and a sentence naming the previous failure it does not repeat. Do not propose Claim L, one-level counting, two-stage averaging, three-level deletion, a random Cayley upper bound, or another classification of regular tournaments on 11 vertices. Do not recommend stopping because the problem is hard. Status must be inconclusive.
""".strip(),
    "R7_cubic": """
You are the pure mathematician. Use the repaired (k, nu) rows in research/AGENT_TASKS/R5-B-outsets.report.json. They meet every triple at least 5 dominators on the equality margin.
research/AGENT_TASKS/R6-B-s4.report.json records that the four-set first moment is at least 717600 against 270725 four-sets, and that the four-set second moment is at least 730730 and still allows every 4-set two dominators. The orchestrator recomputed 717600 and 270725.
Decide the four-set cubic identity sum_X C(|D(X)|, 3) = sum_Y C(nu(Y), 4) on those rows. Either give nonnegative four-set counts with every |D(X)| at least 1 meeting the three four-set equations, or prove that no such counts exist. Do not declare Erdős problem 902 solved.
""".strip(),
    "R7_avoid": """
You are the combinatorial researcher. Keep the six positive common-in-neighbour counts 4, 3, 2, 2, 3, 0 and the bound 3 on counts from {A,B,C,D} into the seven zero-excess vertices.
Find one 5-regular tournament on 11 vertices in which every pair inside those seven vertices also has at most 3 common in-neighbours, then apply the heavy-vertex budget: the ten pair excesses at a zero-excess vertex sum to 10, and a pair with c=4 inside that seven forces a lower bound summing to 14.
The recorded tournament fails on {6,9}. The orchestrator recomputed that count. If no tournament meets the condition, a counting obstruction is the claim. Do not list isomorphism classes. Do not declare Erdős problem 902 solved.
""".strip(),
    "R8_s5": """
You are the combinatorial researcher. Assume a tight pair on 52 vertices with J=5 and s=5. Those bounds are conditional inputs. The five positive excesses are 1,1,1,1,1 and the heavy excess is 9.
Using Lemma A, the pair-sum, and the triple-excess formula, either exclude this degree shape or write the one integer pattern that survives. Stop there. Do not build an 11-vertex tournament. Do not declare Erdős problem 902 solved.
""".strip(),
    "R1_compute": "Run research/compute/exact_checks.py and ingest its JSON.",
}


def checkpoint_path(root: Path) -> Path:
    return root / "research" / "CHECKPOINT.json"


def load_config(root: Path) -> dict:
    cfg = dict(DEFAULT_CONFIG)
    path = root / "research" / "config.json"
    if path.exists():
        cfg.update(json.loads(path.read_text(encoding="utf-8")))
    return cfg


def ensure_dirs(root: Path) -> None:
    for rel in ("research", "research/AGENT_TASKS", "research/checkpoints", "logs"):
        (root / rel).mkdir(parents=True, exist_ok=True)


def _now_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%f")


def save_checkpoint(root: Path, data: dict) -> None:
    ensure_dirs(root)
    path = checkpoint_path(root)
    new = json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    bak = path.parent / "checkpoints"
    bak.mkdir(parents=True, exist_ok=True)
    if path.exists():
        old = path.read_text(encoding="utf-8")
        if old != new:
            (bak / f"CHECKPOINT_{_now_stamp()}.json").write_text(old, encoding="utf-8")
            _prune_backups(root)
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(new, encoding="utf-8")
    os.replace(tmp, path)
    (bak / "CHECKPOINT_good.json").write_text(new, encoding="utf-8")


def _prune_backups(root: Path) -> None:
    limit = int(load_config(root).get("max_checkpoint_backups", 100))
    bak = root / "research" / "checkpoints"
    files = sorted(p for p in bak.glob("CHECKPOINT_2*.json"))
    extra = len(files) - limit
    for path in files[: max(0, extra)]:
        path.unlink(missing_ok=True)


def load_checkpoint(root: Path) -> dict:
    path = checkpoint_path(root)
    bak = path.parent / "checkpoints"
    candidates = [path, bak / "CHECKPOINT_good.json"]
    if bak.exists():
        candidates.extend(reversed(sorted(bak.glob("CHECKPOINT_2*.json"))))
    seen = set()
    for candidate in candidates:
        if candidate in seen or not candidate.exists():
            continue
        seen.add(candidate)
        try:
            return json.loads(candidate.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
    raise RuntimeError(f"no valid checkpoint under {path}")


def append_log(root: Path, event: dict) -> None:
    ensure_dirs(root)
    event = dict(event)
    event["time"] = datetime.now(timezone.utc).isoformat()
    with (root / "logs" / "orchestrator.jsonl").open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False) + "\n")


def append_ledger(root: Path, text: str) -> None:
    ensure_dirs(root)
    path = root / "research" / "LEDGER.md"
    if not path.exists():
        path.write_text("# Ledger\n", encoding="utf-8")
    with path.open("a", encoding="utf-8") as handle:
        handle.write("\n" + text.strip() + "\n")


def replace_block(text: str, begin: str, end: str, inner: str) -> str:
    block = begin + "\n" + inner.strip() + "\n" + end + "\n"
    if begin in text and end in text:
        pre = text.split(begin, 1)[0]
        post = text.split(end, 1)[1]
        if post.startswith("\n"):
            post = post[1:]
        return pre + block + post
    return text.rstrip() + "\n\n" + block


def render_state(root: Path, data: dict | None = None) -> None:
    if data is None:
        data = load_checkpoint(root)
    lines = [
        f"solved: {str(data['solved']).lower()}",
        f"round: {data['round']}",
        f"rounds_started_today: {data['usage']['rounds_started']} on {data['usage']['date']}",
        f"exhausted_approaches: {len(data['exhausted_approaches'])}",
        "",
        "| id | role | status | attempts | verification |",
        "|---|---|---|---|---|",
    ]
    if not data["tasks"]:
        lines.append("| (none) | | | | |")
    for tid in sorted(data["tasks"]):
        task = data["tasks"][tid]
        lines.append(
            f"| {tid} | {task['role']} | {task['status']} | {task['attempts']} | {task.get('verification') or ''} |"
        )
    path = root / "research" / "STATE.md"
    current = path.read_text(encoding="utf-8") if path.exists() else "# State\n\n"
    path.write_text(replace_block(current, BEGIN_STATE, END_STATE, "\n".join(lines)), encoding="utf-8")


def fresh_checkpoint() -> dict:
    return {
        "version": 1,
        "problem_id": "erdos-902",
        "solved": False,
        "round": 0,
        "usage": {"date": date.today().isoformat(), "rounds_started": 0},
        "exhausted_approaches": list(EXHAUSTED_PRIORS),
        "tasks": {},
        "events": [],
        "candidate_counterexample": None,
    }


def init_workspace(root: Path, seeds: bool = True) -> None:
    ensure_dirs(root)
    cfg_path = root / "research" / "config.json"
    if not cfg_path.exists():
        cfg_path.write_text(json.dumps(DEFAULT_CONFIG, indent=2) + "\n", encoding="utf-8")
    created = False
    if not checkpoint_path(root).exists():
        save_checkpoint(root, fresh_checkpoint())
        created = True
        append_ledger(root, f"## {date.today().isoformat()} — controller initialised\n\nsolved remains false. Seed tasks are pending.")
        append_log(root, {"event": "init"})
    if seeds:
        for spec in seed_tasks():
            add_task(root, spec)
    render_state(root)
    if created:
        append_log(root, {"event": "init-complete", "seeds": seeds})


def seed_tasks() -> list[dict]:
    return [
        {
            "id": "R1-E-checks",
            "role": "E",
            "title": "Exact identities and Paley profiles",
            "approach_key": "exact-identities-and-paley-profiles",
            "kind": "compute",
            "priority": 0,
            "depends_on": [],
            "relation_to_prior": "Recomputes Lemma S1, Lemma I, the printed arithmetic of the 20 October note, and Paley profiles, independently of proof/verify_proof.py.",
            "prompt_name": "R1_compute",
            "max_attempts": 2,
        },
        {
            "id": "R1-A-literature",
            "role": "A",
            "title": "Published versus local claims",
            "approach_key": "literature-published-versus-local-2026-10-23",
            "kind": "agent",
            "priority": 1,
            "depends_on": [],
            "relation_to_prior": "The baseline literature file records a timed-out fetch. This task opens the sources.",
            "prompt_name": "R1_literature",
        },
        {
            "id": "R1-G-audit-every-n",
            "role": "G",
            "title": "Audit the every-order J>=3 paragraph",
            "approach_key": "audit-theorem1-every-order-paragraph",
            "kind": "agent",
            "priority": 1,
            "depends_on": [],
            "relation_to_prior": "The N=52 notes cite this paragraph. It has not been audited. This is not the MILP certificate search.",
            "prompt_name": "R1_audit_every_n",
        },
        {
            "id": "R1-B-theorem5",
            "role": "B",
            "title": "Re-derive the DRT(51) moment argument",
            "approach_key": "rederive-drt51-third-moment",
            "kind": "agent",
            "priority": 1,
            "depends_on": [],
            "relation_to_prior": "Theorem 5 is the step that turns a doubly regular tournament of order 51 into the strong claim. The verifier does not read it.",
            "prompt_name": "R1_theorem5",
        },
        {
            "id": "R1-D-counterexample",
            "role": "D",
            "title": "Strong-claim search on orders 47-51",
            "approach_key": "strong-claim-search-orders-47-51",
            "kind": "agent",
            "priority": 1,
            "depends_on": [],
            "relation_to_prior": "Claim L is already dead. This searches the strong triple claim, which is a different statement.",
            "prompt_name": "R1_counterexample",
        },
        {
            "id": "R1-C-n52-j-le-2",
            "role": "C",
            "title": "Direct J<=2 argument at N=52",
            "approach_key": "n52-tight-pair-j-at-most-2-direct",
            "kind": "agent",
            "priority": 2,
            "depends_on": [],
            "relation_to_prior": "Does not cite the every-order paragraph and does not repeat the J=3,4 case split.",
            "prompt_name": "R1_n52_j_le_2",
        },
        {
            "id": "R1-F-reformulation",
            "role": "F",
            "title": "An equivalent formulation for N=52",
            "approach_key": "n52-equivalent-formulation",
            "kind": "agent",
            "priority": 2,
            "depends_on": [],
            "relation_to_prior": "Avoids the exhausted one-level counting and single-pair-link keys.",
            "prompt_name": "R1_reformulation",
        },
        {
            "id": "R1-H-strategy",
            "role": "H",
            "title": "Rank obstacles and set the next round",
            "approach_key": "strategy-after-round1-batch",
            "kind": "agent",
            "priority": 3,
            "depends_on": [
                "R1-E-checks",
                "R1-A-literature",
                "R1-G-audit-every-n",
                "R1-B-theorem5",
                "R1-D-counterexample",
            ],
            "relation_to_prior": "Runs only after the first batch has finished or exhausted, and may not repeat its approach keys.",
            "prompt_name": "R1_strategy",
        },
    ]


def add_task(root: Path, spec: dict) -> dict:
    data = load_checkpoint(root)
    key = spec["approach_key"]
    if key in data["exhausted_approaches"]:
        return {"added": False, "reason": "exhausted"}
    if spec["id"] in data["tasks"]:
        return {"added": False, "reason": "duplicate"}
    for task in data["tasks"].values():
        if task["approach_key"] == key and task["status"] in ("pending", "dispatched", "completed", "blocked"):
            return {"added": False, "reason": "duplicate"}
    cfg = load_config(root)
    task = {
        "id": spec["id"],
        "role": spec["role"],
        "title": spec["title"],
        "approach_key": key,
        "kind": spec.get("kind", "agent"),
        "priority": spec.get("priority", 1),
        "depends_on": list(spec.get("depends_on") or []),
        "status": "pending",
        "attempts": 0,
        "max_attempts": spec.get("max_attempts") or cfg["max_attempts_per_task"],
        "relation_to_prior": spec.get("relation_to_prior", ""),
        "prompt_name": spec.get("prompt_name", ""),
        "body": spec.get("body", ""),
        "script": spec.get("script"),
        "dispatched_at": None,
        "report_hash": None,
        "result_status": None,
        "verification": None,
        "last_error": None,
        "next_retry_after": None,
        "ingest_count": 0,
    }
    data["tasks"][task["id"]] = task
    save_checkpoint(root, data)
    render_state(root, data)
    return {"added": True, "reason": "added"}


def is_due(data: dict, task: dict, now: float) -> bool:
    if task["status"] != "pending":
        return False
    nxt = task.get("next_retry_after")
    if nxt is not None and nxt > now:
        return False
    for dep in task.get("depends_on") or []:
        other = data["tasks"].get(dep)
        if other is None or other["status"] not in ("completed", "exhausted"):
            return False
    return True


def due_task_ids(root: Path, now: float | None = None, kind: str | None = None) -> list[str]:
    now = time.time() if now is None else now
    data = load_checkpoint(root)
    found = []
    for task in data["tasks"].values():
        if kind is not None and task["kind"] != kind:
            continue
        if is_due(data, task, now):
            found.append(task)
    found.sort(key=lambda task: (task["priority"], task["id"]))
    return [task["id"] for task in found]


def record_failure(root: Path, task_id: str, error: str, now: float | None = None) -> dict:
    now = time.time() if now is None else now
    data = load_checkpoint(root)
    task = data["tasks"][task_id]
    if task["status"] in ("completed", "exhausted"):
        return data
    task["attempts"] += 1
    task["last_error"] = error
    task["dispatched_at"] = None
    if task["attempts"] >= task["max_attempts"]:
        task["status"] = "exhausted"
        if task["approach_key"] not in data["exhausted_approaches"]:
            data["exhausted_approaches"].append(task["approach_key"])
    else:
        task["status"] = "pending"
        delay = load_config(root)["backoff_seconds_base"] * (2 ** (task["attempts"] - 1))
        task["next_retry_after"] = now + delay
    save_checkpoint(root, data)
    render_state(root, data)
    append_ledger(
        root,
        f"## {datetime.now(timezone.utc).isoformat()} — {task_id} failed\n\n"
        f"Attempt {task['attempts']} of {task['max_attempts']}. Status: {task['status']}.\n\n{error}",
    )
    append_log(root, {"event": "failure", "task": task_id, "status": task["status"], "error": error})
    return data


def blank_report(task_id: str, agent: str) -> dict:
    return {
        "task_id": task_id,
        "agent": agent,
        "claim": "placeholder",
        "status": "inconclusive",
        "definitions": "As in research/PROBLEM.md.",
        "argument": "placeholder argument",
        "evidence": "placeholder evidence",
        "weaknesses": "placeholder weakness",
        "references": [],
        "next_step": "placeholder next step",
        "relation_to_prior": "placeholder relation",
        "novelty": "placeholder novelty",
    }


def _empty(value) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return not value.strip()
    if isinstance(value, (list, dict)):
        return len(value) == 0
    return False


def _report_hash(report: dict) -> str:
    payload = {key: report.get(key) for key in NONEMPTY_FIELDS}
    payload["references"] = report.get("references")
    raw = json.dumps(payload, sort_keys=True, ensure_ascii=False, default=str)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _upsert_marked_section(root: Path, filename: str, begin: str, end: str, task_id: str, section: str) -> None:
    path = root / "research" / filename
    if not path.exists():
        path.write_text(f"# {filename}\n\n{begin}\n{end}\n", encoding="utf-8")
    text = path.read_text(encoding="utf-8")
    marker = f"<!-- task:{task_id} -->"
    if marker in text:
        return
    if begin not in text or end not in text:
        text = text.rstrip() + f"\n\n{begin}\n{end}\n"
    inner = text.split(begin, 1)[1].split(end, 1)[0]
    inner = inner.replace("(none yet)", "").strip()
    piece = f"{marker}\n{section.strip()}"
    inner = piece if not inner else inner + "\n\n" + piece
    path.write_text(replace_block(text, begin, end, inner), encoding="utf-8")


def ingest(root: Path, report: dict, source: str = "agent") -> dict:
    task_id = report.get("task_id")
    missing = [key for key in NONEMPTY_FIELDS if _empty(report.get(key))]
    if "references" not in report:
        missing.append("references")
    status = report.get("status")
    if status not in ALLOWED_STATUS:
        missing.append("status")
    data = load_checkpoint(root)
    if missing:
        if task_id in data["tasks"]:
            record_failure(root, task_id, "malformed report, missing " + ", ".join(missing))
        else:
            append_ledger(root, f"## orphan malformed report\n\n{missing}")
        return {"ok": False, "error": "malformed", "missing": missing}
    task = data["tasks"].get(task_id)
    if task is None:
        append_ledger(root, f"## orphan report {task_id}\n\nNo such task.")
        return {"ok": False, "error": "unknown-task"}
    if task["status"] == "exhausted":
        append_ledger(root, f"## {task_id} late report refused\n\nThe approach is exhausted.")
        return {"ok": False, "error": "exhausted"}
    if status == "failed":
        record_failure(root, task_id, str(report.get("weaknesses")))
        return {"ok": False, "error": "reported-failure"}
    digest = _report_hash(report)
    if task["status"] == "completed" and task.get("report_hash") == digest:
        return {"ok": True, "duplicate": True}
    if task["status"] == "completed" and task.get("report_hash") not in (None, digest):
        append_ledger(root, f"## {task_id} conflicting report preserved the earlier one\n\nNew hash {digest}.")
        append_log(root, {"event": "conflict", "task": task_id})
        return {"ok": False, "error": "conflict"}
    verification = "reproduced_by_orchestrator" if source == "compute" and status == "computed" else "unreviewed"
    task["status"] = "completed"
    task["result_status"] = status
    task["verification"] = verification
    task["report_hash"] = digest
    task["ingest_count"] = int(task.get("ingest_count") or 0) + 1
    task["dispatched_at"] = None
    task["last_error"] = None
    evidence = report.get("evidence")
    if isinstance(evidence, dict) and evidence.get("counterexample_candidate"):
        data["candidate_counterexample"] = evidence["counterexample_candidate"]
    # Ingest never closes the problem. Promotion into FINAL_PROOF.md is a separate act.
    data["solved"] = False
    save_checkpoint(root, data)
    report_path = root / "research" / "AGENT_TASKS" / f"{task_id}.report.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    stored = dict(report)
    stored["verification"] = verification
    stored["source"] = source
    report_path.write_text(json.dumps(stored, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    section = (
        f"### {task_id} — {status} ({verification})\n\n"
        f"{report['claim']}\n\nWeakness: {report['weaknesses']}\n"
    )
    if status == "disproved":
        _upsert_marked_section(root, "COUNTEREXAMPLES.md", BEGIN_COUNTER, END_COUNTER, task_id, section)
    else:
        _upsert_marked_section(root, "LEMMAS.md", BEGIN_LEMMAS, END_LEMMAS, task_id, section)
    append_ledger(
        root,
        f"## {datetime.now(timezone.utc).isoformat()} — {task_id} ingested\n\n"
        f"Source: {source}. Result: {status}. Verification: {verification}.\n\n"
        f"Claim: {report['claim']}\n\n"
        f"Weakness: {report['weaknesses']}\n\n"
        f"Next: {report['next_step']}",
    )
    append_log(root, {"event": "ingest", "task": task_id, "status": status, "verification": verification})
    render_state(root)
    return {"ok": True, "duplicate": False, "verification": verification}


def render_prompt(root: Path, task: dict, data: dict) -> str:
    body = task.get("body") or PROMPTS.get(task["prompt_name"], task["title"])
    out = root / "research" / "AGENT_TASKS" / f"{task['id']}.report.json"
    closed = ", ".join(data["exhausted_approaches"])
    return (
        f"Task id: {task['id']}\n"
        f"Role: {task['role']}\n"
        f"Approach key: {task['approach_key']}\n"
        f"Relation to prior work: {task['relation_to_prior']}\n\n"
        f"Write one JSON object to:\n{out}\n\n"
        "Do not edit files under proof/. Do not edit research/FINAL_PROOF.md.\n"
        "Do not declare Erdős 902 solved. A status of proved is stored as unreviewed.\n"
        "Use inconclusive when you have a partial result. Use failed only if you could not start.\n"
        "Required keys: task_id, agent, claim, status, definitions, argument, evidence, "
        "weaknesses, references, next_step, relation_to_prior, novelty.\n"
        "status is one of proved, disproved, conditional, failed, inconclusive, computed.\n"
        f"task_id must be {task['id']}. agent must be {task['role']}.\n"
        f"Exhausted approach keys, which this task must not repeat: {closed}.\n\n"
        f"{body}\n"
    )


def collect_reports(root: Path) -> list[str]:
    if not checkpoint_path(root).exists():
        return []
    data = load_checkpoint(root)
    ingested = []
    for task in data["tasks"].values():
        if task["status"] in ("completed", "exhausted"):
            continue
        path = root / "research" / "AGENT_TASKS" / f"{task['id']}.report.json"
        if not path.exists():
            continue
        try:
            report = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            record_failure(root, task["id"], f"unreadable report {path}")
            continue
        outcome = ingest(root, report, source="file")
        if outcome.get("ok"):
            ingested.append(task["id"])
    return ingested


def run_one_compute(root: Path, task_id: str, now: float | None = None) -> dict:
    now = time.time() if now is None else now
    data = load_checkpoint(root)
    task = data["tasks"][task_id]
    script = Path(task["script"]) if task.get("script") else root / "research" / "compute" / "exact_checks.py"
    if not script.exists():
        record_failure(root, task_id, f"missing script {script}", now=now)
        return {"ok": False, "error": "missing-script"}
    cfg = load_config(root)
    try:
        proc = subprocess.run(
            [sys.executable, str(script)],
            cwd=str(root),
            capture_output=True,
            text=True,
            timeout=int(cfg["max_compute_seconds"]),
            encoding="utf-8",
            errors="replace",
        )
    except subprocess.TimeoutExpired:
        record_failure(root, task_id, "compute timed out", now=now)
        return {"ok": False, "error": "timeout"}
    raw_path = root / "research" / "AGENT_TASKS" / f"{task_id}.stdout.json"
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    raw_path.write_text(proc.stdout or "", encoding="utf-8")
    if proc.returncode != 0:
        record_failure(root, task_id, (proc.stderr or proc.stdout or "nonzero exit")[-800], now=now)
        return {"ok": False, "error": "nonzero"}
    try:
        payload = json.loads(proc.stdout)
    except json.JSONDecodeError:
        record_failure(root, task_id, "compute stdout was not JSON", now=now)
        return {"ok": False, "error": "json"}
    if not payload.get("ok"):
        record_failure(root, task_id, "; ".join(payload.get("failures") or ["ok is false"]), now=now)
        return {"ok": False, "error": "checks-failed"}
    weaknesses = payload.get("coverage") or "Finite check."
    if payload.get("counterexample_candidate"):
        weaknesses = "A Paley candidate contradicts the strong claim. It is not yet an independent check, and it is not yet an S_4 tournament. " + weaknesses
    report = blank_report(task_id, task["role"])
    report.update({
        "claim": payload.get("claim") or "Exact checks passed.",
        "status": "computed",
        "definitions": "Tournament, dominator set, and Paley quadratic-residue tournament, as in research/PROBLEM.md.",
        "argument": "The script checks Lemma S1, Lemma I, the printed arithmetic, and exact Paley scans. The proofs of S1 and I are in research/LEMMAS.md; the script does not replace those proofs.",
        "evidence": payload,
        "weaknesses": weaknesses,
        "references": ["research/compute/exact_checks.py", "research/LEMMAS.md"],
        "next_step": "If a Paley candidate exists, verify that witness by hand. Otherwise use the profiles as negative Paley evidence only.",
        "relation_to_prior": task["relation_to_prior"],
        "novelty": "Independent of proof/verify_proof.py, and it records orders 43 and 47, which that script does not profile.",
    })
    return ingest(root, report, source="compute")


def _roll_usage(data: dict) -> None:
    today = date.today().isoformat()
    if data["usage"]["date"] != today:
        data["usage"] = {"date": today, "rounds_started": 0}


def plan_round(root: Path, now: float | None = None, dispatch_limit: int | None = None) -> dict:
    collect_reports(root)
    now = time.time() if now is None else now
    cfg = load_config(root)
    data = load_checkpoint(root)
    _roll_usage(data)
    if data["usage"]["rounds_started"] >= int(cfg["max_rounds_per_day"]):
        save_checkpoint(root, data)
        append_log(root, {"event": "paused", "reason": "daily round budget"})
        return {"paused": True, "dispatched": [], "reason": "daily round budget"}
    save_checkpoint(root, data)
    compute_ids = due_task_ids(root, now=now, kind="compute")
    for task_id in compute_ids:
        run_one_compute(root, task_id, now=now)
    data = load_checkpoint(root)
    inflight = sum(1 for task in data["tasks"].values() if task["status"] == "dispatched")
    slots = int(dispatch_limit if dispatch_limit is not None else cfg["max_concurrent_agents"]) - inflight
    dispatched = []
    for task_id in due_task_ids(root, now=now, kind="agent"):
        if slots <= 0:
            break
        task = data["tasks"][task_id]
        prompt_path = root / "research" / "AGENT_TASKS" / f"{task_id}.prompt.md"
        prompt_path.write_text(render_prompt(root, task, data), encoding="utf-8")
        task["status"] = "dispatched"
        task["dispatched_at"] = now
        dispatched.append(task_id)
        slots -= 1
    if compute_ids or dispatched:
        data["round"] = int(data["round"]) + 1
        data["usage"]["rounds_started"] = int(data["usage"]["rounds_started"]) + 1
    save_checkpoint(root, data)
    render_state(root, data)
    append_log(root, {"event": "plan", "dispatched": dispatched, "compute": compute_ids, "round": data["round"]})
    return {"paused": False, "dispatched": dispatched, "compute": compute_ids, "round": data["round"]}


def resume(root: Path, now: float | None = None) -> list[str]:
    collect_reports(root)
    now = time.time() if now is None else now
    timeout = int(load_config(root)["agent_timeout_seconds"])
    data = load_checkpoint(root)
    stale = []
    for task_id, task in data["tasks"].items():
        if task["status"] != "dispatched":
            continue
        started = task.get("dispatched_at") or 0
        if now - started > timeout:
            stale.append(task_id)
    for task_id in stale:
        record_failure(root, task_id, "dispatch timed out before a report arrived", now=now)
    append_log(root, {"event": "resume", "expired": stale})
    return stale


def mock_round(root: Path) -> dict:
    if not checkpoint_path(root).exists():
        init_workspace(root, seeds=False)
    specs = [
        ("MOCK-ok", "success", "E"),
        ("MOCK-bad", "malformed", "D"),
        ("MOCK-boom", "exception", "B"),
        ("MOCK-slow", "timeout", "G"),
    ]
    outcomes = []
    for task_id, behavior, role in specs:
        data = load_checkpoint(root)
        if task_id not in data["tasks"]:
            add_task(root, {
                "id": task_id,
                "role": role,
                "title": behavior,
                "approach_key": f"mock-{behavior}",
                "kind": "agent",
                "priority": 1,
                "depends_on": [],
                "relation_to_prior": "mock drill",
                "prompt_name": "R1_compute",
                "max_attempts": 3,
            })
            data = load_checkpoint(root)
        status = data["tasks"][task_id]["status"]
        if status == "completed":
            outcomes.append("skipped_completed")
            continue
        if status == "exhausted":
            outcomes.append("skipped_exhausted")
            continue
        if behavior == "exception":
            try:
                raise RuntimeError("simulated agent crash")
            except RuntimeError as exc:
                record_failure(root, task_id, str(exc))
            outcomes.append("exception")
        elif behavior == "timeout":
            record_failure(root, task_id, "timeout")
            outcomes.append("timeout")
        elif behavior == "malformed":
            ingest(root, {"task_id": task_id, "agent": role}, source="mock")
            outcomes.append("malformed")
        else:
            report = blank_report(task_id, role)
            report["claim"] = "Mock finite check only: 2 + 2 = 4."
            report["status"] = "computed"
            report["argument"] = "Arithmetic in the integers. This mock does not speak about tournaments."
            ingest(root, report, source="mock")
            outcomes.append("ingested")
    return {"outcomes": outcomes}


def status_text(root: Path) -> str:
    data = load_checkpoint(root)
    lines = [
        f"solved={data['solved']} round={data['round']} "
        f"today={data['usage']['rounds_started']}/{load_config(root)['max_rounds_per_day']}",
    ]
    for task_id in sorted(data["tasks"]):
        task = data["tasks"][task_id]
        err = f" error={task['last_error']}" if task.get("last_error") else ""
        lines.append(f"{task_id} {task['status']} attempts={task['attempts']} verification={task.get('verification')}{err}")
    if data.get("candidate_counterexample"):
        lines.append(f"candidate_counterexample={data['candidate_counterexample']}")
    return "\n".join(lines)


def heartbeat(root: Path) -> dict:
    expired = resume(root)
    planned = plan_round(root)
    text = status_text(root)
    append_log(root, {"event": "heartbeat", "expired": expired, "dispatched": planned.get("dispatched", [])})
    return {"expired": expired, "plan": planned, "status": text}


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Erdős 902 research controller")
    parser.add_argument("command", choices=["init", "status", "plan-round", "mock-round", "run-compute", "ingest", "resume", "heartbeat", "add-task"])
    parser.add_argument("--root", default=None)
    parser.add_argument("--report", default=None)
    parser.add_argument("--spec", default=None, help="JSON file holding one task spec or a list of specs (add-task)")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--dispatch", type=int, default=None)
    args = parser.parse_args(argv)
    root = Path(args.root).resolve() if args.root else DEFAULT_ROOT
    if args.command == "mock-round":
        problem = root / "research" / "PROBLEM.md"
        if problem.exists() and not args.force:
            print("refusing mock-round on the research repository; omit --root to use a scratch directory")
            if args.root is None:
                scratch = Path(tempfile.mkdtemp(prefix="erdos902-mock-"))
                print(mock_round(scratch))
                print(scratch)
                return 0
            return 2
        print(mock_round(root))
        return 0
    if args.command == "init":
        init_workspace(root, seeds=True)
        print(status_text(root))
        return 0
    if args.command == "status":
        print(status_text(root))
        return 0
    if args.command == "resume":
        print(resume(root))
        print(status_text(root))
        return 0
    if args.command == "plan-round":
        print(json.dumps(plan_round(root, dispatch_limit=args.dispatch), indent=2))
        print(status_text(root))
        return 0
    if args.command == "run-compute":
        ids = due_task_ids(root, kind="compute")
        print(json.dumps([run_one_compute(root, task_id) for task_id in ids], indent=2, default=str))
        return 0
    if args.command == "ingest":
        if not args.report:
            print("--report is required")
            return 2
        report = json.loads(Path(args.report).read_text(encoding="utf-8"))
        print(ingest(root, report, source="file"))
        return 0
    if args.command == "add-task":
        if not args.spec:
            print("--spec is required")
            return 2
        specs = json.loads(Path(args.spec).read_text(encoding="utf-8"))
        specs = specs if isinstance(specs, list) else [specs]
        for spec in specs:
            print(spec["id"], add_task(root, spec))
        return 0
    if args.command == "heartbeat":
        result = heartbeat(root)
        print(result["status"])
        print(json.dumps({"expired": result["expired"], "dispatched": result["plan"].get("dispatched")}, indent=2))
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main())
