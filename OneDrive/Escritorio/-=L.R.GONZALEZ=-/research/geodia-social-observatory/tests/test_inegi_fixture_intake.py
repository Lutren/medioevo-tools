from __future__ import annotations

import hashlib
import json
import unittest
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures" / "inegi_mexico_social_2018_2023_fixture.json"
SOURCE_CARD = ROOT / "fixtures" / "source_intake" / "inegi" / "INEGI_SOURCE_CARD.md"
MANIFEST = ROOT / "fixtures" / "source_intake" / "inegi" / "INEGI_ENOE_SOURCE_MANIFEST_2026-05-14.json"
RAW_XLSX = ROOT / "fixtures" / "source_intake" / "inegi" / "raw" / "enoe_indicadores_estrategicos_2005_2026_mensual.xlsx"
REVIEW_DOC = ROOT / "fixtures" / "README_THIRD_OFFICIAL_FIXTURE_REVIEW.md"
CROSSWALK = ROOT / "fixtures" / "geodia_indicator_crosswalk_v0_1.json"


NS = {
    "main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "rel": "http://schemas.openxmlformats.org/package/2006/relationships",
    "office_rel": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}


def _column_index(cell_ref: str) -> int:
    letters = "".join(ch for ch in cell_ref if ch.isalpha())
    value = 0
    for letter in letters:
        value = value * 26 + (ord(letter.upper()) - ord("A") + 1)
    return value - 1


def _shared_strings(zf: zipfile.ZipFile) -> list[str]:
    root = ET.fromstring(zf.read("xl/sharedStrings.xml"))
    values: list[str] = []
    for item in root.findall("main:si", NS):
        text = "".join(node.text or "" for node in item.findall(".//main:t", NS))
        values.append(text)
    return values


def _sheet_path(zf: zipfile.ZipFile, sheet_name: str) -> str:
    workbook = ET.fromstring(zf.read("xl/workbook.xml"))
    rels = ET.fromstring(zf.read("xl/_rels/workbook.xml.rels"))
    rel_targets = {rel.attrib["Id"]: rel.attrib["Target"] for rel in rels.findall("rel:Relationship", NS)}
    for sheet in workbook.findall(".//main:sheet", NS):
        if sheet.attrib["name"] == sheet_name:
            rid = sheet.attrib[f"{{{NS['office_rel']}}}id"]
            return "xl/" + rel_targets[rid].lstrip("/")
    raise AssertionError(f"sheet not found: {sheet_name}")


def _sheet_rows(path: Path, sheet_name: str, row_numbers: set[int]) -> dict[int, dict[int, object]]:
    with zipfile.ZipFile(path) as zf:
        strings = _shared_strings(zf)
        sheet = ET.fromstring(zf.read(_sheet_path(zf, sheet_name)))
    rows: dict[int, dict[int, object]] = {}
    for row in sheet.findall(".//main:row", NS):
        row_index = int(row.attrib["r"])
        if row_index not in row_numbers:
            continue
        values: dict[int, object] = {}
        for cell in row.findall("main:c", NS):
            ref = cell.attrib["r"]
            value_node = cell.find("main:v", NS)
            if value_node is None:
                continue
            raw = value_node.text or ""
            if cell.attrib.get("t") == "s":
                values[_column_index(ref)] = strings[int(raw)]
            else:
                try:
                    values[_column_index(ref)] = float(raw)
                except ValueError:
                    values[_column_index(ref)] = raw
        rows[row_index] = values
    return rows


def _annual_mean_from_xlsx(row_number: int) -> dict[str, float]:
    rows = _sheet_rows(RAW_XLSX, "1.2", {5, 7, row_number})
    month_map = {"Ene": 1, "Feb": 2, "Mar": 3, "Abr": 4, "May": 5, "Jun": 6, "Jul": 7, "Ago": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dic": 12}
    values_by_year: dict[int, list[float]] = {year: [] for year in range(2018, 2024)}
    year: int | None = None
    for col in range(5, max(rows[7]) + 1):
        if col in rows[5]:
            year = int(rows[5][col])
        if year in values_by_year and rows[7].get(col) in month_map and col in rows[row_number]:
            values_by_year[year].append(float(rows[row_number][col]))
    return {str(year): round(sum(values) / len(values), 4) for year, values in values_by_year.items()}


class InegiFixtureIntakeTests(unittest.TestCase):
    def test_inegi_source_card_exists(self) -> None:
        text = SOURCE_CARD.read_text(encoding="utf-8")
        self.assertIn("GEODIA-INEGI-ENOE-MEX-2018-2023", text)
        self.assertIn("https://www.inegi.org.mx/", text)
        self.assertIn("publication_gate: `BLOCK`", text)

    def test_inegi_fixture_not_fabricated(self) -> None:
        fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
        digest = hashlib.sha256(RAW_XLSX.read_bytes()).hexdigest()
        self.assertEqual(fixture["raw_source_hash"], f"sha256:{digest}")

        unemployment = next(
            item for item in fixture["indicators"] if item["source_indicator_id"] == "INEGI_ENOE_TASA_DESOCUPACION_ANNUAL_MEAN"
        )
        self.assertEqual(unemployment["source_location"]["workbook_row"], 289)
        self.assertEqual(unemployment["raw_values"], _annual_mean_from_xlsx(289))
        self.assertTrue(all(count == 12 for count in unemployment["monthly_counts"].values()))

    def test_inegi_fixture_has_source_url_and_hash_or_manifest(self) -> None:
        fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(fixture["source_id"], "INEGI")
        self.assertTrue(fixture["source_url"].startswith("https://www.inegi.org.mx/"))
        self.assertEqual(fixture["source_manifest_ref"], "fixtures/source_intake/inegi/INEGI_ENOE_SOURCE_MANIFEST_2026-05-14.json")
        self.assertEqual(fixture["raw_source_hash"], "sha256:" + manifest["sha256"])

    def test_crosswalk_third_source_has_no_unjustified_exact(self) -> None:
        crosswalk = json.loads(CROSSWALK.read_text(encoding="utf-8"))
        inegi_entries = [entry for entry in crosswalk["entries"] if entry["source_id"] == "INEGI"]
        self.assertEqual(len(inegi_entries), 1)
        self.assertEqual(inegi_entries[0]["comparability_class"], "STRONG_PROXY")
        self.assertNotEqual(inegi_entries[0]["comparability_class"], "EXACT")

    def test_license_review_status_present(self) -> None:
        fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(fixture["license_status"], "REVIEW_TERMS_DOCUMENTED")
        self.assertTrue(fixture["license_review_required"])
        self.assertEqual(manifest["license_status"], "REVIEW_TERMS_DOCUMENTED")
        self.assertTrue(manifest["license_review_required"])

    def test_manual_download_scaffold_when_no_download_available(self) -> None:
        text = REVIEW_DOC.read_text(encoding="utf-8")
        self.assertIn("SUPERSEDED_BY_APPROVE_LOCAL_WITH_OFFICIAL_SOURCE", text)
        self.assertIn("fallback manual", text)
        self.assertIn("no se invento el fixture", text.lower())


if __name__ == "__main__":
    unittest.main()
