"""Unit & behavioural smoke tests for Phase 2 Kimi-k3 Swarm & Single-Pass Review."""
from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))

from jev import (
    SwarmBatchReport,
    SwarmConfig,
    SwarmResult,
    SwarmTask,
    execute_kimi_swarm,
    load_queue_tasks,
    register_provider,
    run_two_phase_pipeline,
    save_task_spec,
    single_pass_batch_verify,
)


@register_provider("swarm_test_provider")
def test_provider(state, questions, model, timeout):
    answers = {}
    for key in questions:
        if "fail" in key:
            score = 0.60
        else:
            score = 0.95
        answers[key] = {"type": "noul", "noul": score}
    return {
        "model": "test-verifier",
        "answers": answers,
        "usage": {"input_tokens": 10, "output_tokens": 0},
    }


class SwarmTests(unittest.TestCase):
    def test_config_defaults(self):
        cfg = SwarmConfig()
        self.assertEqual(cfg.max_concurrency, 300)
        self.assertEqual(cfg.model_name, "kimi-k3")
        self.assertEqual(cfg.tau_verify, 0.85)
        self.assertEqual(cfg.resolved_base_url(), "https://api.opencode.ai/v1")

        old_url = os.environ.get("OPENCODE_API_URL")
        try:
            os.environ["OPENCODE_API_URL"] = "http://localhost:8080/v1"
            self.assertEqual(cfg.resolved_base_url(), "http://localhost:8080/v1")
        finally:
            if old_url is not None:
                os.environ["OPENCODE_API_URL"] = old_url
            else:
                os.environ.pop("OPENCODE_API_URL", None)

    def test_task_serialization_roundtrip(self):
        task = SwarmTask(
            task_id="TSK-001",
            clean_goal="Analyze renal clearance kinetics",
            assigned_worker="researcher",
            filtered_context=("GFR: 30",),
            constraints=("Traditional Chinese",),
            outputs=("report.md",),
            confidence=0.98,
        )
        data = task.to_spec_dict()
        self.assertEqual(data["handoff_version"], "2.1.0")
        self.assertEqual(data["phase2_routing"]["status"], "ready_for_opencode")
        self.assertEqual(data["phase2_routing"]["tau_action"], "execute")

        restored = SwarmTask.from_dict(data)
        self.assertEqual(restored.task_id, "TSK-001")
        self.assertEqual(restored.clean_goal, "Analyze renal clearance kinetics")
        self.assertEqual(restored.assigned_worker, "researcher")
        self.assertEqual(restored.confidence, 0.98)
        self.assertEqual(restored.filtered_context, ("GFR: 30",))

    def test_queue_save_and_load(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            qdir = Path(tmpdir) / "queue"
            t1 = SwarmTask(task_id="T1", clean_goal="Goal 1", confidence=0.95)
            t2 = SwarmTask(task_id="T2", clean_goal="Goal 2", confidence=0.92)
            # Low confidence task should be skipped by loader
            t3_dict = {
                "task_id": "T3",
                "clean_goal": "Goal 3",
                "confidence": 0.75,
                "phase2_routing": {"status": "ready_for_opencode", "tau_action": "execute"},
            }

            save_task_spec(t1, qdir)
            save_task_spec(t2, qdir)
            (qdir / "T3.json").write_text(json.dumps(t3_dict), encoding="utf-8")

            loaded = load_queue_tasks(qdir)
            loaded_ids = {t.task_id for t in loaded}
            self.assertEqual(loaded_ids, {"T1", "T2"})

    def test_execute_swarm_parallel_workers(self):
        tasks = [SwarmTask(task_id=f"PAR-{i}", clean_goal=f"Subtask {i}") for i in range(12)]
        cfg = SwarmConfig(max_concurrency=16)

        results = execute_kimi_swarm(tasks, cfg)
        self.assertEqual(len(results), 12)
        for r in results:
            self.assertEqual(r.status, "completed")
            self.assertIn("PAR-", r.output)

    def test_single_pass_batch_verify_pass_and_requeue(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            qdir = Path(tmpdir) / "queue"
            t_pass = SwarmTask(task_id="task_pass", clean_goal="Passing goal")
            t_fail = SwarmTask(task_id="task_fail", clean_goal="Failing goal")

            p_pass = save_task_spec(t_pass, qdir)
            p_fail = save_task_spec(t_fail, qdir)

            r_pass = SwarmResult(task_id="task_pass", output="Valid evidence", status="completed",
                                 task_ref=SwarmTask.from_dict(t_pass.to_spec_dict(), source_file=str(p_pass)))
            r_fail = SwarmResult(task_id="task_fail", output="Incomplete output", status="completed",
                                 task_ref=SwarmTask.from_dict(t_fail.to_spec_dict(), source_file=str(p_fail)))

            cfg = SwarmConfig(tau_verify=0.85)
            passed, requeued, scores = single_pass_batch_verify([r_pass, r_fail], cfg, provider="swarm_test_provider")

            self.assertEqual(len(passed), 1)
            self.assertEqual(passed[0].task_id, "task_pass")
            self.assertEqual(len(requeued), 1)
            self.assertEqual(requeued[0].task_id, "task_fail")

            # Check queue cleanup: pass is deleted, fail remains
            self.assertFalse(p_pass.exists())
            self.assertTrue(p_fail.exists())

    def test_run_two_phase_pipeline_end_to_end(self):
        tasks = [
            SwarmTask(task_id="pipeline_1", clean_goal="Compute eigenvalues"),
            SwarmTask(task_id="pipeline_2", clean_goal="Plot phase portrait"),
        ]
        cfg = SwarmConfig(max_concurrency=10, tau_verify=0.85)
        report = run_two_phase_pipeline(tasks, config=cfg, provider="swarm_test_provider")

        self.assertIsInstance(report, SwarmBatchReport)
        self.assertEqual(report.total_tasks, 2)
        self.assertEqual(report.passed_count, 2)
        self.assertEqual(report.requeue_count, 0)
        self.assertEqual(report.status, "completed")
        self.assertGreater(report.wall_clock_s, 0.0)


if __name__ == "__main__":
    unittest.main()
