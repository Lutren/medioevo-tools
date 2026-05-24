from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from geodia_social_observatory.cli import main as cli_main


ROOT = Path(__file__).resolve().parents[1]
CROSSWALK = ROOT / "fixtures" / "geodia_indicator_crosswalk_v0_1.json"
SCHEMA = ROOT / "schemas" / "geodia_indicator_harmonization_v0_1.schema.json"
WORLD_BANK_FIXTURE = ROOT / "fixtures" / "world_bank_mexico_2018_2023_fixture.json"
EUROSTAT_FIXTURE = ROOT / "fixtures" / "eurostat_social_epoch_2018_2023_fixture.json"


def _run_cli(out: Path) -> dict[str, object]:
    rc = cli_main(
        [
            "harmonize",
            "--offline",
            "--fixtures",
            str(WORLD_BANK_FIXTURE),
            str(EUROSTAT_FIXTURE),
            "--crosswalk",
            str(CROSSWALK),
            "--schema",
            str(SCHEMA),
            "--pretty",
            "--out",
            str(out),
        ]
    )
    if rc != 0:
        raise AssertionError(f"unexpected CLI rc: {rc}")
    return json.loads(out.read_text(encoding="utf-8"))


def _all_keys(value: object) -> list[str]:
    keys: list[str] = []
    if isinstance(value, dict):
        for key, nested in value.items():
            keys.append(str(key))
            keys.extend(_all_keys(nested))
    elif isinstance(value, list):
        for item in value:
            keys.extend(_all_keys(item))
    return keys


class GeodiaHarmonizationCliTests(unittest.TestCase):
    def test_cli_runs_without_network_and_generates_valid_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "harmonization.json"
            with mock.patch("socket.socket", side_effect=AssertionError("network disabled")):
                report = _run_cli(out)
        self.assertEqual(report["schema"], "claudio.geodia_harmonization_report.v0_1")
        self.assertTrue(report["offline_mode"])
        self.assertFalse(report["network_used"])

    def test_cli_accepts_offline_fixtures_crosswalk_and_schema(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            report = _run_cli(Path(tmp) / "harmonization.json")
        self.assertEqual(len(report["fixtures_evaluated"]), 2)
        self.assertEqual(report["crosswalk"], str(CROSSWALK.as_posix()))
        self.assertEqual(report["schema_used"], str(SCHEMA.as_posix()))

    def test_report_gate_no_ranking_causality_or_prediction(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            report = _run_cli(Path(tmp) / "harmonization.json")
        self.assertEqual(report["publication_gate"], "BLOCK")
        self.assertFalse(any("rank" in key.lower() for key in _all_keys(report)))
        text = json.dumps(report, ensure_ascii=False).lower()
        self.assertNotIn("causalidad", text)
        self.assertNotIn("prediction", text)
        self.assertNotIn("predic", text)

    def test_economy_review_and_no_unjustified_exact(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            report = _run_cli(Path(tmp) / "harmonization.json")
        classes = {row["canonical_indicator_id"]: row["comparability_class"] for row in report["indicators_harmonized"]}
        self.assertEqual(classes["economy.real_growth_rate"], "REVIEW")
        self.assertEqual(classes["labor_market.unemployment_rate.total"], "STRONG_PROXY")
        self.assertEqual(classes["demography.life_expectancy_at_birth.total"], "STRONG_PROXY")
        self.assertNotIn("EXACT", set(classes.values()))

    def test_invalid_pairs_include_not_comparable(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            report = _run_cli(Path(tmp) / "harmonization.json")
        self.assertTrue(report["invalid_pair_examples"])
        self.assertEqual(report["invalid_pair_examples"][0]["comparability_class"], "NOT_COMPARABLE")

    def test_output_is_reproducible_with_frozen_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            first = Path(tmp) / "first.json"
            second = Path(tmp) / "second.json"
            first_report = _run_cli(first)
            second_report = _run_cli(second)
        self.assertEqual(first_report, second_report)

    def test_missing_crosswalk_fails_safely(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "out.json"
            with self.assertRaises(SystemExit):
                cli_main(
                    [
                        "harmonize",
                        "--offline",
                        "--fixtures",
                        str(WORLD_BANK_FIXTURE),
                        str(EUROSTAT_FIXTURE),
                        "--crosswalk",
                        str(Path(tmp) / "missing.json"),
                        "--schema",
                        str(SCHEMA),
                        "--out",
                        str(out),
                    ]
                )

    def test_missing_schema_fails_safely(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "out.json"
            with self.assertRaises(SystemExit):
                cli_main(
                    [
                        "harmonize",
                        "--offline",
                        "--fixtures",
                        str(WORLD_BANK_FIXTURE),
                        str(EUROSTAT_FIXTURE),
                        "--crosswalk",
                        str(CROSSWALK),
                        "--schema",
                        str(Path(tmp) / "missing.schema.json"),
                        "--out",
                        str(out),
                    ]
                )

    def test_live_remote_fixture_source_fails_safely_in_offline_mode(self) -> None:
        payload = json.loads(WORLD_BANK_FIXTURE.read_text(encoding="utf-8"))
        payload["retrieval_mode"] = "live_api"
        payload["source_url"] = "https://api.worldbank.org/v2/country/MEX/indicator"
        with tempfile.TemporaryDirectory() as tmp:
            bad_fixture = Path(tmp) / "live_fixture.json"
            out = Path(tmp) / "out.json"
            bad_fixture.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaises(SystemExit):
                cli_main(
                    [
                        "harmonize",
                        "--offline",
                        "--fixtures",
                        str(bad_fixture),
                        str(EUROSTAT_FIXTURE),
                        "--crosswalk",
                        str(CROSSWALK),
                        "--schema",
                        str(SCHEMA),
                        "--out",
                        str(out),
                    ]
                )


if __name__ == "__main__":
    unittest.main()
