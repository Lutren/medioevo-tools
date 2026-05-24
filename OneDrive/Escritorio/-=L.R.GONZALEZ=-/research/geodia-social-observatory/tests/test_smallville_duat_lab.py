from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from geodia_social_observatory.cli import main as cli_main
from geodia_social_observatory.remote_compute import build_colab_kaggle_notebook, build_remote_compute_plan
from geodia_social_observatory.smallville_lab import (
    falsify_smallville_run,
    run_smallville_duat_lab,
    verify_hash_chain,
)


class SmallvilleDuatLabTests(unittest.TestCase):
    def test_smallville_run_is_deterministic_and_has_25_agents(self) -> None:
        first = run_smallville_duat_lab(seed="proof", days=2, ticks_per_day=4)
        second = run_smallville_duat_lab(seed="proof", days=2, ticks_per_day=4)
        self.assertEqual(first["fingerprints"]["ledger_sha256"], second["fingerprints"]["ledger_sha256"])
        self.assertEqual(first["scenario"]["agent_count"], 25)
        self.assertEqual(first["schema"], "duat.smallville.simulation_run_ledger.v0_1")
        self.assertEqual(first["gates"]["publication_gate"], "BLOCK")
        self.assertFalse(first["external_publication"])

    def test_smallville_hash_chain_and_falsifiers_pass(self) -> None:
        ledger = run_smallville_duat_lab(seed="chain", days=1, ticks_per_day=3)
        report = falsify_smallville_run(ledger)
        self.assertTrue(verify_hash_chain(ledger))
        self.assertTrue(report["passed"])
        self.assertIn("bias_claim_boundary", {check["name"] for check in report["checks"]})
        self.assertEqual(ledger["claims"]["bias"], "AUDITABLE_NOT_ABSENT")
        self.assertEqual(ledger["claims"]["public_prediction"], "NOT_ALLOWED")

    def test_cli_writes_ledger_and_falsifier_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ledger_path = Path(tmp) / "ledger.json"
            falsifier_path = Path(tmp) / "falsifier.json"
            rc_run = cli_main(
                [
                    "smallville-duat",
                    "--seed",
                    "cli-proof",
                    "--days",
                    "1",
                    "--ticks-per-day",
                    "2",
                    "--pretty",
                    "--out",
                    str(ledger_path),
                ]
            )
            rc_falsify = cli_main(
                [
                    "smallville-falsify",
                    "--ledger",
                    str(ledger_path),
                    "--pretty",
                    "--out",
                    str(falsifier_path),
                ]
            )
            ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
            falsifier = json.loads(falsifier_path.read_text(encoding="utf-8"))
        self.assertEqual(rc_run, 0)
        self.assertEqual(rc_falsify, 0)
        self.assertEqual(ledger["scenario"]["agent_count"], 25)
        self.assertTrue(falsifier["passed"])

    def test_remote_compute_plan_keeps_external_runtimes_in_review(self) -> None:
        plan = build_remote_compute_plan(seed="remote-proof")
        gates = {spec["provider"]: spec["action_gate"] for spec in plan["specs"]}
        self.assertEqual(plan["schema"], "duat.remote_compute_plan.v0_1")
        self.assertEqual(gates["local_cpu"], "APPROVE_LOCAL")
        self.assertEqual(gates["colab_notebook"], "REVIEW")
        self.assertEqual(gates["kaggle_kernel"], "REVIEW")
        self.assertEqual(gates["simscale"], "REVIEW")
        self.assertTrue(plan["falsifiers"]["passed"])
        self.assertTrue(all(spec["publication_gate"] == "BLOCK" for spec in plan["specs"]))
        self.assertIn("physical_simulation_only", next(spec for spec in plan["specs"] if spec["provider"] == "simscale")["constraints"])

    def test_remote_compute_cli_outputs_plan(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "remote-plan.json"
            rc = cli_main(["remote-compute-plan", "--pretty", "--out", str(out)])
            plan = json.loads(out.read_text(encoding="utf-8"))
        self.assertEqual(rc, 0)
        self.assertEqual(plan["policy"]["external_execution_default"], "REVIEW")
        self.assertEqual(plan["policy"]["publication_gate"], "BLOCK")

    def test_colab_kaggle_notebook_template_is_exportable_and_blocked(self) -> None:
        notebook = build_colab_kaggle_notebook(seed="notebook-proof")
        self.assertEqual(notebook["nbformat"], 4)
        self.assertEqual(notebook["metadata"]["duat_policy"]["publication_gate"], "BLOCK")
        text = json.dumps(notebook, ensure_ascii=False).lower()
        self.assertIn("run_smallville_duat_lab", text)
        self.assertNotIn("api_key=", text)
        self.assertNotIn("password=", text)

    def test_remote_notebook_cli_writes_ipynb_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "duat-smallville.ipynb"
            rc = cli_main(["remote-notebook-template", "--pretty", "--out", str(out)])
            notebook = json.loads(out.read_text(encoding="utf-8"))
        self.assertEqual(rc, 0)
        self.assertEqual(notebook["metadata"]["duat_policy"]["runtime"], "manual_colab_or_kaggle_only")


if __name__ == "__main__":
    unittest.main()
