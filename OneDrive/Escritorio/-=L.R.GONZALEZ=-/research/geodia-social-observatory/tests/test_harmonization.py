from __future__ import annotations

import json
import unittest
from pathlib import Path

from geodia_social_observatory.harmonization import (
    build_harmonized_record,
    classify_comparability,
    load_crosswalk,
    normalize_polarity,
    validate_publication_gate,
)


ROOT = Path(__file__).resolve().parents[1]
CROSSWALK = ROOT / "fixtures" / "geodia_indicator_crosswalk_v0_1.json"
SCHEMA = ROOT / "schemas" / "geodia_indicator_harmonization_v0_1.schema.json"
WORLD_BANK_FIXTURE = ROOT / "fixtures" / "world_bank_mexico_2018_2023_fixture.json"
EUROSTAT_FIXTURE = ROOT / "fixtures" / "eurostat_social_epoch_2018_2023_fixture.json"
INEGI_FIXTURE = ROOT / "fixtures" / "inegi_mexico_social_2018_2023_fixture.json"


class GeodiaHarmonizationTests(unittest.TestCase):
    def test_crosswalk_loads_and_matches_schema_required_fields(self) -> None:
        crosswalk = load_crosswalk(CROSSWALK)
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        required = set(schema["properties"]["entries"]["items"]["required"])
        allowed_classes = set(schema["properties"]["entries"]["items"]["properties"]["comparability_class"]["enum"])

        self.assertEqual(crosswalk["harmonization_schema"], "claudio.geodia_indicator_harmonization.v0_1")
        self.assertEqual(crosswalk["publication_gate"], "BLOCK")
        self.assertEqual(len(crosswalk["entries"]), 7)
        for entry in crosswalk["entries"]:
            self.assertTrue(required.issubset(entry))
            self.assertIn(entry["comparability_class"], allowed_classes)
            self.assertEqual(entry["publication_gate"], "BLOCK")

    def test_no_dubious_indicator_is_exact(self) -> None:
        crosswalk = load_crosswalk(CROSSWALK)
        self.assertFalse(any(entry["comparability_class"] == "EXACT" for entry in crosswalk["entries"]))

    def test_publication_gate_remains_block(self) -> None:
        crosswalk = load_crosswalk(CROSSWALK)
        world_bank = build_harmonized_record(WORLD_BANK_FIXTURE, crosswalk)
        eurostat = build_harmonized_record(EUROSTAT_FIXTURE, crosswalk)
        inegi = build_harmonized_record(INEGI_FIXTURE, crosswalk)
        self.assertTrue(validate_publication_gate(world_bank))
        self.assertTrue(validate_publication_gate(eurostat))
        self.assertTrue(validate_publication_gate(inegi))
        self.assertEqual(world_bank["publication_gate"], "BLOCK")
        self.assertEqual(eurostat["publication_gate"], "BLOCK")
        self.assertEqual(inegi["publication_gate"], "BLOCK")

    def test_negative_unemployment_polarity_is_preserved(self) -> None:
        world_bank = build_harmonized_record(WORLD_BANK_FIXTURE, CROSSWALK)
        unemployment = next(
            item
            for item in world_bank["harmonized_indicators"]
            if item["canonical_indicator_id"] == "labor_market.unemployment_rate.total"
        )
        first_value = unemployment["values"][0]
        self.assertEqual(unemployment["polarity_canonical"], "negative")
        self.assertEqual(first_value["polarity_canonical"], "negative")
        self.assertEqual(first_value["value_polarity_normalized"], -first_value["value_original"])
        self.assertEqual(normalize_polarity(3.2, "negative"), -3.2)

    def test_mexico_world_bank_vs_germany_eurostat_produces_no_ranking(self) -> None:
        world_bank = build_harmonized_record(WORLD_BANK_FIXTURE, CROSSWALK)
        eurostat = build_harmonized_record(EUROSTAT_FIXTURE, CROSSWALK)
        self.assertEqual(world_bank["ranking"]["status"], "BLOCKED")
        self.assertEqual(eurostat["ranking"]["status"], "BLOCKED")
        self.assertNotIn("rank", world_bank)
        self.assertNotIn("rank", eurostat)

    def test_review_and_not_comparable_are_respected(self) -> None:
        entries = load_crosswalk(CROSSWALK)["entries"]
        by_source_indicator = {entry["source_indicator_id"]: entry for entry in entries}

        self.assertEqual(
            classify_comparability(by_source_indicator["NY.GDP.PCAP.KD.ZG"], by_source_indicator["tec00115"]),
            "REVIEW",
        )
        self.assertEqual(
            classify_comparability(by_source_indicator["SL.UEM.TOTL.ZS"], by_source_indicator["demo_mlexpec"]),
            "NOT_COMPARABLE",
        )

        eurostat = build_harmonized_record(EUROSTAT_FIXTURE, CROSSWALK)
        self.assertIn("tec00115", eurostat["review_indicators"])
        self.assertEqual(eurostat["not_comparable_indicators"], [])


if __name__ == "__main__":
    unittest.main()
