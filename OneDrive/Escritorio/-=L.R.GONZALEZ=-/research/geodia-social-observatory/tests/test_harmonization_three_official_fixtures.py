from __future__ import annotations

import json
import unittest
from pathlib import Path
from unittest import mock

from geodia_social_observatory.harmonization import build_harmonization_report, build_harmonized_record


ROOT = Path(__file__).resolve().parents[1]
CROSSWALK = ROOT / "fixtures" / "geodia_indicator_crosswalk_v0_1.json"
SCHEMA = ROOT / "schemas" / "geodia_indicator_harmonization_v0_1.schema.json"
WORLD_BANK_FIXTURE = ROOT / "fixtures" / "world_bank_mexico_2018_2023_fixture.json"
EUROSTAT_FIXTURE = ROOT / "fixtures" / "eurostat_social_epoch_2018_2023_fixture.json"
INEGI_FIXTURE = ROOT / "fixtures" / "inegi_mexico_social_2018_2023_fixture.json"


def _report() -> dict[str, object]:
    return build_harmonization_report(
        [WORLD_BANK_FIXTURE, EUROSTAT_FIXTURE, INEGI_FIXTURE],
        CROSSWALK,
        SCHEMA,
    )


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


class ThreeOfficialFixtureHarmonizationTests(unittest.TestCase):
    def test_harmonization_accepts_world_bank_eurostat_inegi(self) -> None:
        report = _report()
        self.assertEqual(len(report["fixtures_evaluated"]), 3)
        self.assertIn("INEGI", report["harmonized_records"])
        self.assertEqual(report["harmonized_records"]["INEGI"]["indicator_count"], 1)

    def test_harmonization_runtime_remains_offline(self) -> None:
        with mock.patch("socket.socket", side_effect=AssertionError("network disabled")):
            report = _report()
        self.assertTrue(report["offline_mode"])
        self.assertFalse(report["network_used"])

    def test_publication_gate_remains_blocked(self) -> None:
        report = _report()
        inegi_record = build_harmonized_record(INEGI_FIXTURE, CROSSWALK)
        self.assertEqual(report["publication_gate"], "BLOCK")
        self.assertTrue(all(row["publication_gate"] == "BLOCK" for row in report["fixtures_evaluated"]))
        self.assertEqual(inegi_record["publication_gate"], "BLOCK")

    def test_no_ranking_prediction_causality(self) -> None:
        report = _report()
        text = json.dumps(report, ensure_ascii=False).lower()
        self.assertFalse(any("rank" in key.lower() for key in _all_keys(report)))
        self.assertNotIn("prediction", text)
        self.assertNotIn("predic", text)
        self.assertNotIn("causal", text)

    def test_inegi_unemployment_is_strong_proxy_not_exact(self) -> None:
        report = _report()
        unemployment = next(
            row
            for row in report["indicators_harmonized"]
            if row["canonical_indicator_id"] == "labor_market.unemployment_rate.total"
        )
        self.assertIn("INEGI_ENOE_TASA_DESOCUPACION_ANNUAL_MEAN", unemployment["source_indicator_ids"])
        self.assertEqual(unemployment["comparability_class"], "STRONG_PROXY")
        self.assertNotEqual(unemployment["comparability_class"], "EXACT")


if __name__ == "__main__":
    unittest.main()
