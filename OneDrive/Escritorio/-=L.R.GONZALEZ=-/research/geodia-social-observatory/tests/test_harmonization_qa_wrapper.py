from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
WRAPPER = ROOT / "scripts" / "run_harmonization_qa.py"
WORLD_BANK_FIXTURE = ROOT / "fixtures" / "world_bank_mexico_2018_2023_fixture.json"
EUROSTAT_FIXTURE = ROOT / "fixtures" / "eurostat_social_epoch_2018_2023_fixture.json"
INEGI_FIXTURE = ROOT / "fixtures" / "inegi_mexico_social_2018_2023_fixture.json"


def _load_wrapper():
    spec = importlib.util.spec_from_file_location("run_harmonization_qa", WRAPPER)
    if spec is None or spec.loader is None:
        raise AssertionError("could not load QA wrapper module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class GeodiaHarmonizationQaWrapperTests(unittest.TestCase):
    def test_third_fixture_source_discovery_or_review(self) -> None:
        module = _load_wrapper()
        discovery = module.discover_third_fixture_source()
        self.assertEqual(discovery["candidate_source"], "INEGI / Mexico official social indicators")
        self.assertEqual(discovery["source_status"], "FOUND_LOCAL")
        self.assertIn("research/geodia-social-observatory/fixtures/inegi_mexico_social_2018_2023_fixture.json", discovery["fixture_candidates"])
        self.assertIn("INEGI_SOURCE_CARD.md", discovery["source_card"])

    def test_harmonization_accepts_three_fixtures_when_fixture_exists(self) -> None:
        module = _load_wrapper()
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            report = module.build_report(
                output_report=tmp_path / "harmonization.json",
                qa_report=tmp_path / "qa-wrapper.json",
                fixtures=[WORLD_BANK_FIXTURE, EUROSTAT_FIXTURE, INEGI_FIXTURE],
                run_secret_scans=False,
                run_pending_review=False,
            )
            harmonization = json.loads((tmp_path / "harmonization.json").read_text(encoding="utf-8"))
        self.assertEqual(len(report["input_fixtures"]), 3)
        self.assertEqual(len(harmonization["fixtures_evaluated"]), 3)
        self.assertEqual(harmonization["publication_gate"], "BLOCK")

    def test_no_network_for_third_fixture(self) -> None:
        module = _load_wrapper()
        with mock.patch("socket.socket", side_effect=AssertionError("network disabled")):
            discovery = module.discover_third_fixture_source()
        self.assertEqual(discovery["source_status"], "FOUND_LOCAL")

    def test_publication_gate_remains_blocked(self) -> None:
        module = _load_wrapper()
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            report = module.build_report(
                output_report=tmp_path / "harmonization.json",
                qa_report=tmp_path / "qa-wrapper.json",
                run_secret_scans=False,
                run_pending_review=False,
            )
            third = module.build_third_fixture_readiness_report(out=tmp_path / "third.json")
        self.assertEqual(report["publication_gate"], "BLOCK")
        self.assertEqual(third["publication_gate"], "BLOCK")
        self.assertEqual(third["action_gate"], "APPROVE_LOCAL_ONLY")
        self.assertTrue(third["fixture_created"])

    def test_no_ranking_prediction_causality_with_third_fixture(self) -> None:
        module = _load_wrapper()
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            report = module.build_report(
                output_report=tmp_path / "harmonization.json",
                qa_report=tmp_path / "qa-wrapper.json",
                fixtures=[WORLD_BANK_FIXTURE, EUROSTAT_FIXTURE, INEGI_FIXTURE],
                run_secret_scans=False,
                run_pending_review=False,
            )
        scan = module.forbidden_publication_scan(report)
        self.assertEqual(scan["status"], "PASS")
        self.assertFalse(scan["comparative_ordering_produced"])
        self.assertFalse(scan["future_claims_produced"])
        self.assertFalse(scan["cause_effect_claims_produced"])

    def test_qa_wrapper_dry_or_offline_runs(self) -> None:
        module = _load_wrapper()
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            report = module.build_report(
                pretty=True,
                output_report=tmp_path / "harmonization.json",
                qa_report=tmp_path / "qa-wrapper.json",
                run_secret_scans=False,
                run_pending_review=False,
            )
        self.assertTrue(report["offline_mode"])
        self.assertFalse(report["network_used"])

    def test_qa_wrapper_report_contains_required_fields(self) -> None:
        module = _load_wrapper()
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            out = tmp_path / "qa-wrapper.json"
            report = module.build_report(
                output_report=tmp_path / "harmonization.json",
                qa_report=out,
                run_secret_scans=False,
                run_pending_review=False,
            )
            parsed = json.loads(out.read_text(encoding="utf-8"))
        for key in [
            "timestamp",
            "command_run",
            "input_fixtures",
            "output_report",
            "json_validation",
            "scan_results",
            "pending_review",
            "tests_summary",
            "publication_gate",
            "action_gate",
        ]:
            self.assertIn(key, report)
            self.assertIn(key, parsed)

    def test_qa_wrapper_blocks_publication_gate(self) -> None:
        module = _load_wrapper()
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            report = module.build_report(
                output_report=tmp_path / "harmonization.json",
                qa_report=tmp_path / "qa-wrapper.json",
                run_secret_scans=False,
                run_pending_review=False,
            )
        self.assertEqual(report["publication_gate"], "BLOCK")
        self.assertEqual(report["action_gate"], "APPROVE_LOCAL_ONLY")

    def test_qa_wrapper_rejects_ranking_prediction_causality_fields(self) -> None:
        module = _load_wrapper()
        bad_payload = {
            "country_rank": 1,
            "prediction": "not allowed",
            "causal_claim": "not allowed",
        }
        scan = module.forbidden_publication_scan(bad_payload)
        self.assertEqual(scan["status"], "FAIL")
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            report = module.build_report(
                output_report=tmp_path / "harmonization.json",
                qa_report=tmp_path / "qa-wrapper.json",
                run_secret_scans=False,
                run_pending_review=False,
            )
        clean_scan = module.forbidden_publication_scan(report)
        self.assertEqual(clean_scan["status"], "PASS")

    def test_qa_wrapper_pending_review_shape(self) -> None:
        module = _load_wrapper()
        fake_pending = {"status": "PASS", "active_dedup": 0, "claudio_open": 0, "command": "python tools/release/pending_review.py --write --quiet"}
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(module, "pending_review_scan", return_value=fake_pending):
            tmp_path = Path(tmp)
            report = module.build_report(
                output_report=tmp_path / "harmonization.json",
                qa_report=tmp_path / "qa-wrapper.json",
                run_secret_scans=False,
                run_pending_review=True,
            )
        self.assertEqual(report["pending_review"]["active_dedup"], 0)
        self.assertEqual(report["pending_review"]["claudio_open"], 0)
        self.assertEqual(report["pending_review"]["status"], "PASS")


if __name__ == "__main__":
    unittest.main()
