"""Failure-isolation and checkpoint tests for the Erdős 902 controller.

Run from anywhere:

    python research/tests/test_orchestrator.py
"""

from __future__ import annotations

import importlib.util
import json
import tempfile
import time
from pathlib import Path


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ROOT = Path(__file__).resolve().parents[1]
ORCH = load_module(ROOT / "orchestrator.py", "erdos902_orchestrator")
CHECKS = load_module(ROOT / "compute" / "exact_checks.py", "erdos902_checks")


def write_config(root: Path, **overrides) -> None:
    research = root / "research"
    research.mkdir(parents=True, exist_ok=True)
    cfg = dict(ORCH.DEFAULT_CONFIG)
    cfg.update(overrides)
    (research / "config.json").write_text(json.dumps(cfg), encoding="utf-8")


def test_mock_isolation_and_no_duplicate() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        write_config(root, backoff_seconds_base=0, max_rounds_per_day=20)
        first = ORCH.mock_round(root)
        data = ORCH.load_checkpoint(root)
        tasks = data["tasks"]
        assert tasks["MOCK-ok"]["status"] == "completed", tasks["MOCK-ok"]
        assert tasks["MOCK-ok"]["ingest_count"] == 1
        assert tasks["MOCK-bad"]["attempts"] == 1
        assert tasks["MOCK-boom"]["attempts"] == 1
        assert tasks["MOCK-slow"]["attempts"] == 1
        assert data["solved"] is False
        assert "exception" in first["outcomes"]
        assert "malformed" in first["outcomes"]
        assert "timeout" in first["outcomes"]
        assert "ingested" in first["outcomes"]
        second = ORCH.mock_round(root)
        again = ORCH.load_checkpoint(root)
        assert again["tasks"]["MOCK-ok"]["ingest_count"] == 1
        assert "skipped_completed" in second["outcomes"]
        # A failed sibling does not erase the successful report.
        assert again["tasks"]["MOCK-ok"]["status"] == "completed"


def test_resolution_claim_does_not_solve() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        write_config(root)
        ORCH.init_workspace(root, seeds=False)
        added = ORCH.add_task(root, {
            "id": "FAKE-PROOF",
            "role": "B",
            "title": "pretend",
            "approach_key": "fake-full-proof",
            "kind": "agent",
            "priority": 1,
            "depends_on": [],
            "relation_to_prior": "test",
            "prompt_name": "R1_theorem5",
            "max_attempts": 2,
        })
        assert added["added"]
        report = ORCH.blank_report("FAKE-PROOF", "B")
        report["status"] = "proved"
        report["claim"] = "f(n) is completely determined."
        report["claim_scope"] = "full_problem_resolution"
        outcome = ORCH.ingest(root, report, source="test")
        assert outcome["ok"]
        data = ORCH.load_checkpoint(root)
        assert data["solved"] is False
        assert data["tasks"]["FAKE-PROOF"]["verification"] == "unreviewed"
        assert data["tasks"]["FAKE-PROOF"]["status"] == "completed"


def test_exhaustion_and_backoff() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        write_config(root, backoff_seconds_base=1000, max_attempts_per_task=2)
        ORCH.init_workspace(root, seeds=False)
        ORCH.add_task(root, {
            "id": "RETRY",
            "role": "D",
            "title": "retry me",
            "approach_key": "retry-key",
            "kind": "agent",
            "priority": 1,
            "depends_on": [],
            "relation_to_prior": "test",
            "prompt_name": "R1_counterexample",
            "max_attempts": 2,
        })
        rejected = ORCH.add_task(root, {
            "id": "CLAIM-L-AGAIN",
            "role": "D",
            "title": "reopen Claim L",
            "approach_key": "claim-L-single-pair-link",
            "kind": "agent",
            "priority": 1,
            "depends_on": [],
            "relation_to_prior": "already dead",
            "prompt_name": "R1_counterexample",
        })
        assert rejected["added"] is False
        assert rejected["reason"] == "exhausted"
        now = time.time()
        ORCH.record_failure(root, "RETRY", "first", now=now)
        data = ORCH.load_checkpoint(root)
        assert data["tasks"]["RETRY"]["status"] == "pending"
        assert "RETRY" not in ORCH.due_task_ids(root, now=now + 1)
        ORCH.record_failure(root, "RETRY", "second", now=now + 10)
        data = ORCH.load_checkpoint(root)
        assert data["tasks"]["RETRY"]["status"] == "exhausted"
        again = ORCH.add_task(root, {
            "id": "RETRY-2",
            "role": "D",
            "title": "same idea",
            "approach_key": "retry-key",
            "kind": "agent",
            "priority": 1,
            "depends_on": [],
            "relation_to_prior": "same",
            "prompt_name": "R1_counterexample",
        })
        assert again["reason"] == "exhausted"


def test_resume_keeps_live_dispatch_and_recovers_stale() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        write_config(root, agent_timeout_seconds=50)
        ORCH.init_workspace(root, seeds=False)
        ORCH.add_task(root, {
            "id": "LIVE",
            "role": "A",
            "title": "live",
            "approach_key": "live-key",
            "kind": "agent",
            "priority": 1,
            "depends_on": [],
            "relation_to_prior": "test",
            "prompt_name": "R1_literature",
        })
        now = time.time()
        data = ORCH.load_checkpoint(root)
        data["tasks"]["LIVE"]["status"] = "dispatched"
        data["tasks"]["LIVE"]["dispatched_at"] = now
        ORCH.save_checkpoint(root, data)
        ORCH.resume(root, now=now + 5)
        assert ORCH.load_checkpoint(root)["tasks"]["LIVE"]["status"] == "dispatched"
        data = ORCH.load_checkpoint(root)
        data["tasks"]["LIVE"]["dispatched_at"] = now - 1000
        ORCH.save_checkpoint(root, data)
        ORCH.resume(root, now=now)
        task = ORCH.load_checkpoint(root)["tasks"]["LIVE"]
        assert task["status"] == "pending"
        assert task["attempts"] == 1


def test_corrupt_checkpoint_recovers() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        write_config(root)
        ORCH.init_workspace(root, seeds=False)
        data = ORCH.load_checkpoint(root)
        data["marker"] = 2
        ORCH.save_checkpoint(root, data)
        path = root / "research" / "CHECKPOINT.json"
        path.write_text("{not json", encoding="utf-8")
        loaded = ORCH.load_checkpoint(root)
        assert loaded["marker"] == 2
        assert loaded["solved"] is False


def test_plan_isolates_missing_compute_and_skips_completed() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        write_config(root, max_concurrent_agents=4, backoff_seconds_base=0)
        narrative = root / "research"
        narrative.mkdir(parents=True, exist_ok=True)
        (narrative / "STATE.md").write_text(
            "# State\n\nNarrative stays.\n\n<!-- BEGIN GENERATED STATE -->\nold\n<!-- END GENERATED STATE -->\n",
            encoding="utf-8",
        )
        ORCH.init_workspace(root, seeds=False)
        text = (narrative / "STATE.md").read_text(encoding="utf-8")
        assert "Narrative stays." in text
        assert "old" not in text.split("BEGIN GENERATED")[1]
        ORCH.add_task(root, {
            "id": "COMPUTE-MISSING",
            "role": "E",
            "title": "missing script",
            "approach_key": "missing-script",
            "kind": "compute",
            "priority": 0,
            "depends_on": [],
            "relation_to_prior": "test",
            "prompt_name": "R1_compute",
            "script": str(root / "no-such-script.py"),
            "max_attempts": 2,
        })
        ORCH.add_task(root, {
            "id": "AGENT",
            "role": "A",
            "title": "still goes",
            "approach_key": "agent-goes",
            "kind": "agent",
            "priority": 1,
            "depends_on": [],
            "relation_to_prior": "test",
            "prompt_name": "R1_literature",
        })
        ORCH.add_task(root, {
            "id": "LATER",
            "role": "H",
            "title": "after agent",
            "approach_key": "later-key",
            "kind": "agent",
            "priority": 3,
            "depends_on": ["AGENT"],
            "relation_to_prior": "test",
            "prompt_name": "R1_strategy",
        })
        result = ORCH.plan_round(root)
        assert "AGENT" in result["dispatched"]
        assert "LATER" not in result["dispatched"]
        data = ORCH.load_checkpoint(root)
        assert data["tasks"]["COMPUTE-MISSING"]["attempts"] == 1
        assert data["tasks"]["AGENT"]["status"] == "dispatched"
        second = ORCH.plan_round(root)
        assert "AGENT" not in second["dispatched"]


def test_exact_checks() -> dict:
    from math import comb
    assert comb(52, 2) == 1326
    assert 26 * comb(26, 2) + 26 * comb(25, 2) == 16250
    assert 16250 - 12 * 1326 == 338
    report = CHECKS.run_checks()
    assert report["ok"], report["failures"]
    assert report["lemma_s1"]["lower_bound"] == 16250
    profiles = report["paley"]["profiles"]
    assert profiles["7"]["min_dominators_by_set_size"][:4] == [7, 3, 1, 0]
    assert profiles["19"]["min_dominators_by_set_size"] == [19, 9, 4, 1, 0]
    assert profiles["67"]["min_dominators_by_set_size"] == [67, 33, 16, 6, 1]
    return report


def main() -> None:
    tests = [
        test_mock_isolation_and_no_duplicate,
        test_resolution_claim_does_not_solve,
        test_exhaustion_and_backoff,
        test_resume_keeps_live_dispatch_and_recovers_stale,
        test_corrupt_checkpoint_recovers,
        test_plan_isolates_missing_compute_and_skips_completed,
        test_exact_checks,
    ]
    for test in tests:
        print(f"RUN {test.__name__}", flush=True)
        result = test()
        print(f"OK  {test.__name__}", flush=True)
        if test is test_exact_checks:
            paley = result["paley"]["profiles"]
            for order, row in paley.items():
                print(f"  QR_{order} min |D| by set size {row['min_dominators_by_set_size']}", flush=True)
            print("  candidates", result["counterexample_candidate"], flush=True)
            print("  runtime", result["runtime_seconds"], flush=True)
    print("ALL TESTS PASSED", flush=True)


if __name__ == "__main__":
    main()
