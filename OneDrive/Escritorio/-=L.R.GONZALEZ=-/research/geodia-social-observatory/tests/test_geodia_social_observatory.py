from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from geodia_social_observatory.cli import main as cli_main
from geodia_social_observatory.contracts import (
    EPOCH_MODEL_SCHEMA,
    SCENARIO_REPORT_SCHEMA,
    SOURCE_SNAPSHOT_SCHEMA,
)
from geodia_social_observatory.model import build_epoch_model, build_scenario_report, run_backtest
from geodia_social_observatory.snapshot import create_snapshot_from_fixture
from geodia_social_observatory.sources import SourcePolicyError, source_catalog


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures" / "social_epoch_fixture.json"
EUROSTAT_FIXTURE = ROOT / "fixtures" / "eurostat_social_epoch_2018_2023_fixture.json"


class GeodiaSocialObservatoryTests(unittest.TestCase):
    def test_rejects_source_outside_allowlist(self) -> None:
        payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
        payload["source_id"] = "random_blog"
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaises(SourcePolicyError):
                create_snapshot_from_fixture(path)

    def test_snapshot_hash_is_stable(self) -> None:
        first = create_snapshot_from_fixture(FIXTURE)
        second = create_snapshot_from_fixture(FIXTURE)
        self.assertEqual(first["schema"], SOURCE_SNAPSHOT_SCHEMA)
        self.assertEqual(first["content_sha256"], second["content_sha256"])
        self.assertEqual(first["classification"], "CERTEZA")

    def test_epoch_model_contains_duat_and_conway(self) -> None:
        snapshot = create_snapshot_from_fixture(FIXTURE)
        model = build_epoch_model(snapshot)
        self.assertEqual(model["schema"], EPOCH_MODEL_SCHEMA)
        self.assertIn("duat", model)
        self.assertGreaterEqual(len(model["conway_specialists"]), 3)
        self.assertTrue(model["epoch_label"])

    def test_report_has_claim_evidence_and_uncertainty(self) -> None:
        snapshot = create_snapshot_from_fixture(FIXTURE)
        report = build_scenario_report(snapshot, run_backtest(FIXTURE))
        self.assertEqual(report["schema"], SCENARIO_REPORT_SCHEMA)
        self.assertEqual(report["publication_gate"]["status"], "BLOCK")
        self.assertTrue(report["claims"])
        self.assertTrue(all(claim["evidence"] for claim in report["claims"]))
        self.assertTrue(any(item["classification"] == "INCOGNITA" for item in report["uncertainties"]))

    def test_gdelt_is_media_signal_only(self) -> None:
        payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
        payload["source_id"] = "gdelt_doc_2"
        payload["source_url"] = "https://api.gdeltproject.org/api/v2/doc/doc"
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "gdelt.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            snapshot = create_snapshot_from_fixture(path)
        self.assertEqual(snapshot["source"]["role"], "media_narrative_signal_only")
        self.assertEqual(snapshot["classification"], "INFERENCIA")

    def test_awesomedata_is_catalog_index_only(self) -> None:
        catalog = {row["source_id"]: row for row in source_catalog()}
        source = catalog["awesomedata_public_datasets"]
        self.assertEqual(source["role"], "dataset_catalog_index_only")
        self.assertEqual(source["classification_floor"], "INFERENCIA")
        self.assertIn("license", str(source["license_notice"]).lower())
        self.assertIn("catalog", str(source["special_notice"]).lower())

    def test_backtest_uses_holdout(self) -> None:
        result = run_backtest(FIXTURE, holdout_year=2023)
        self.assertEqual(result["status"], "evaluated")
        self.assertEqual(result["holdout_year"], 2023)
        self.assertIn(result["classification"], ("INFERENCIA", "INCOGNITA"))

    def test_cli_offline_run_writes_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "report.json"
            rc = cli_main(["run", "--offline", "--fixture", str(FIXTURE), "--out", str(out)])
            data = json.loads(out.read_text(encoding="utf-8"))
        self.assertEqual(rc, 0)
        self.assertEqual(data["schema"], SCENARIO_REPORT_SCHEMA)
        self.assertEqual(data["publication_gate"]["status"], "BLOCK")

    def test_eurostat_fixture_shape_and_gate(self) -> None:
        payload = json.loads(EUROSTAT_FIXTURE.read_text(encoding="utf-8"))
        self.assertEqual(payload["source_id"], "eurostat_sdmx")
        self.assertEqual(payload["publication_gate"], "BLOCK")
        self.assertEqual(payload["country_or_region"], "DE")
        self.assertEqual(payload["year_range"], "2018-2023")
        self.assertEqual(len(payload["indicators"]), 3)
        self.assertTrue(all("raw_values" in row for row in payload["indicators"]))
        self.assertTrue(all("normalized_values" in row for row in payload["indicators"]))

        snapshot = create_snapshot_from_fixture(EUROSTAT_FIXTURE)
        report = build_scenario_report(snapshot, run_backtest(EUROSTAT_FIXTURE))
        self.assertEqual(snapshot["schema"], SOURCE_SNAPSHOT_SCHEMA)
        self.assertEqual(snapshot["source"]["source_id"], "eurostat_sdmx")
        self.assertEqual(snapshot["classification"], "CERTEZA")
        self.assertEqual(report["schema"], SCENARIO_REPORT_SCHEMA)
        self.assertEqual(report["publication_gate"]["status"], "BLOCK")
        self.assertTrue(all(claim["classification"] in ("CERTEZA", "INFERENCIA") for claim in report["claims"]))


if __name__ == "__main__":
    unittest.main()
