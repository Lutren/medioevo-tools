"""Minimal indicator harmonization for offline GEODIA fixtures."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


COMPARABILITY_CLASSES = {
    "EXACT",
    "STRONG_PROXY",
    "WEAK_PROXY",
    "NOT_COMPARABLE",
    "REVIEW",
}

REQUIRED_ENTRY_FIELDS = {
    "canonical_indicator_id",
    "source_indicator_id",
    "source_id",
    "country_or_region",
    "year_range",
    "unit_original",
    "unit_canonical",
    "polarity_original",
    "polarity_canonical",
    "frequency",
    "transformation_applied",
    "comparability_class",
    "evidence",
    "caveats",
    "publication_gate",
}


def _is_remote_reference(value: str | Path) -> bool:
    text = str(value).lower()
    return text.startswith(("http://", "https://"))


def _require_local_path(path: str | Path, label: str) -> Path:
    if _is_remote_reference(path):
        raise ValueError(f"{label} must be a local offline path")
    local_path = Path(path)
    if not local_path.exists():
        raise ValueError(f"{label} does not exist: {local_path}")
    return local_path


def _load_json(value: dict[str, Any] | str | Path) -> dict[str, Any]:
    if isinstance(value, dict):
        return value
    path = Path(value)
    return json.loads(path.read_text(encoding="utf-8"))


def _gate_status(value: Any) -> str:
    if isinstance(value, dict):
        return str(value.get("status", ""))
    return str(value)


def validate_publication_gate(record: dict[str, Any]) -> bool:
    if _gate_status(record.get("publication_gate")) != "BLOCK":
        raise ValueError("publication_gate must be BLOCK")
    return True


def load_harmonization_schema(path: str | Path) -> dict[str, Any]:
    schema_path = _require_local_path(path, "schema")
    schema = _load_json(schema_path)
    if schema.get("$id") != "claudio.geodia_indicator_harmonization.v0_1":
        raise ValueError("unexpected harmonization schema id")
    return schema


def validate_crosswalk_against_schema(crosswalk: dict[str, Any], schema: dict[str, Any]) -> bool:
    entry_schema = schema["properties"]["entries"]["items"]
    required = set(entry_schema["required"])
    allowed_classes = set(entry_schema["properties"]["comparability_class"]["enum"])
    if crosswalk.get("schema") != schema["properties"]["schema"]["const"]:
        raise ValueError("crosswalk schema const does not match harmonization schema")
    if crosswalk.get("harmonization_schema") != schema["$id"]:
        raise ValueError("crosswalk harmonization_schema does not match schema id")
    for entry in crosswalk.get("entries", []):
        missing = required.difference(entry)
        if missing:
            raise ValueError(f"crosswalk entry missing schema fields: {sorted(missing)}")
        if entry["comparability_class"] not in allowed_classes:
            raise ValueError(f"invalid comparability_class: {entry['comparability_class']}")
    return True


def load_crosswalk(path: str | Path) -> dict[str, Any]:
    crosswalk_path = _require_local_path(path, "crosswalk")
    crosswalk = _load_json(crosswalk_path)
    validate_publication_gate(crosswalk)
    entries = crosswalk.get("entries")
    if not isinstance(entries, list) or not entries:
        raise ValueError("crosswalk entries must be a non-empty list")
    for entry in entries:
        missing = REQUIRED_ENTRY_FIELDS.difference(entry)
        if missing:
            raise ValueError(f"crosswalk entry missing fields: {sorted(missing)}")
        if entry["comparability_class"] not in COMPARABILITY_CLASSES:
            raise ValueError(f"invalid comparability_class: {entry['comparability_class']}")
        validate_publication_gate(entry)
    return crosswalk


def classify_comparability(indicator_a: dict[str, Any], indicator_b: dict[str, Any]) -> str:
    if indicator_a.get("canonical_indicator_id") != indicator_b.get("canonical_indicator_id"):
        return "NOT_COMPARABLE"
    classes = {
        str(indicator_a.get("comparability_class", "REVIEW")),
        str(indicator_b.get("comparability_class", "REVIEW")),
    }
    if "NOT_COMPARABLE" in classes:
        return "NOT_COMPARABLE"
    if "REVIEW" in classes:
        return "REVIEW"
    if "WEAK_PROXY" in classes:
        return "WEAK_PROXY"
    if "STRONG_PROXY" in classes:
        return "STRONG_PROXY"
    if classes == {"EXACT"}:
        return "EXACT"
    return "REVIEW"


def classify_group_comparability(indicators: list[dict[str, Any]]) -> str:
    if len(indicators) < 2:
        return "REVIEW"
    canonical_ids = {entry.get("canonical_indicator_id") for entry in indicators}
    if len(canonical_ids) != 1:
        return "NOT_COMPARABLE"
    classes = {str(entry.get("comparability_class", "REVIEW")) for entry in indicators}
    if "NOT_COMPARABLE" in classes:
        return "NOT_COMPARABLE"
    if "REVIEW" in classes:
        return "REVIEW"
    if "WEAK_PROXY" in classes:
        return "WEAK_PROXY"
    if "STRONG_PROXY" in classes:
        return "STRONG_PROXY"
    if classes == {"EXACT"}:
        return "EXACT"
    return "REVIEW"


def normalize_polarity(value: float | int, polarity: str) -> float:
    numeric = float(value)
    normalized_polarity = polarity.lower()
    if normalized_polarity == "negative":
        return -numeric
    if normalized_polarity in {"positive", "neutral", "review"}:
        return numeric
    raise ValueError(f"unsupported polarity: {polarity}")


def load_offline_fixture(path: str | Path) -> dict[str, Any]:
    fixture_path = _require_local_path(path, "fixture")
    fixture = _load_json(fixture_path)
    source_url = str(fixture.get("source_url", ""))
    retrieval_mode = str(fixture.get("retrieval_mode", ""))
    if _is_remote_reference(source_url) and not retrieval_mode.startswith("offline_fixture"):
        raise ValueError("offline mode requires a captured fixture, not a live remote source_url")
    if "observations" not in fixture:
        raise ValueError("fixture must contain observations")
    return fixture


def _fixture_country(fixture: dict[str, Any]) -> str:
    return str(fixture.get("country_or_region") or fixture.get("geography") or "UNKNOWN")


def _fixture_year_range(fixture: dict[str, Any]) -> str:
    return str(fixture.get("year_range") or fixture.get("period") or "UNKNOWN")


def _matching_entries(fixture: dict[str, Any], crosswalk: dict[str, Any]) -> list[dict[str, Any]]:
    source_id = str(fixture.get("source_id", ""))
    country = _fixture_country(fixture)
    year_range = _fixture_year_range(fixture)
    return [
        entry
        for entry in crosswalk.get("entries", [])
        if entry["source_id"] == source_id
        and entry["country_or_region"] == country
        and entry["year_range"] == year_range
    ]


def build_harmonized_record(
    fixture: dict[str, Any] | str | Path,
    crosswalk: dict[str, Any] | str | Path,
) -> dict[str, Any]:
    fixture_payload = fixture if isinstance(fixture, dict) else load_offline_fixture(fixture)
    crosswalk_payload = load_crosswalk(crosswalk) if not isinstance(crosswalk, dict) else crosswalk
    validate_publication_gate(crosswalk_payload)

    observations = list(fixture_payload.get("observations", []))
    observations_by_indicator: dict[str, list[dict[str, Any]]] = {}
    for observation in observations:
        source_indicator_id = str(observation.get("source_indicator_id", ""))
        observations_by_indicator.setdefault(source_indicator_id, []).append(observation)

    harmonized_indicators = []
    for entry in _matching_entries(fixture_payload, crosswalk_payload):
        rows = sorted(
            observations_by_indicator.get(entry["source_indicator_id"], []),
            key=lambda row: int(row["year"]),
        )
        if not rows:
            continue
        values = [
            {
                "year": int(row["year"]),
                "value_original": float(row["value"]),
                "value_polarity_normalized": normalize_polarity(
                    float(row["value"]),
                    entry["polarity_canonical"],
                ),
                "unit_original": row.get("unit", entry["unit_original"]),
                "unit_canonical": entry["unit_canonical"],
                "polarity_original": row.get("polarity", entry["polarity_original"]),
                "polarity_canonical": entry["polarity_canonical"],
            }
            for row in rows
        ]
        harmonized_indicators.append(
            {
                **entry,
                "values": values,
                "classification": "INFERENCIA",
            }
        )

    mapped_source_ids = {item["source_indicator_id"] for item in harmonized_indicators}
    source_observation_ids = {str(row.get("source_indicator_id", "")) for row in observations}
    review_indicators = [
        item["source_indicator_id"]
        for item in harmonized_indicators
        if item["comparability_class"] == "REVIEW"
    ]
    not_comparable_indicators = [
        item["source_indicator_id"]
        for item in harmonized_indicators
        if item["comparability_class"] == "NOT_COMPARABLE"
    ]

    record = {
        "schema": "claudio.geodia_harmonized_fixture_record.v0_1",
        "harmonization_schema": crosswalk_payload["harmonization_schema"],
        "source_id": fixture_payload.get("source_id"),
        "country_or_region": _fixture_country(fixture_payload),
        "year_range": _fixture_year_range(fixture_payload),
        "source_card_ref": fixture_payload.get("source_card_ref"),
        "license_status": fixture_payload.get("license_status"),
        "license_review_required": fixture_payload.get("license_review_required", True),
        "raw_source_hash": fixture_payload.get("raw_source_hash"),
        "publication_gate": "BLOCK",
        "ranking": {
            "status": "BLOCKED",
            "reason": "harmonization layer does not rank countries, populations or sources",
        },
        "harmonized_indicators": harmonized_indicators,
        "review_indicators": review_indicators,
        "not_comparable_indicators": not_comparable_indicators,
        "unmapped_source_indicator_ids": sorted(source_observation_ids.difference(mapped_source_ids)),
        "caveats": list(crosswalk_payload.get("caveats", [])) + list(fixture_payload.get("caveats", [])),
        "claims": [
            {
                "classification": "INFERENCIA",
                "text": "This record supports technical fixture compatibility checks only.",
            }
        ],
    }
    validate_publication_gate(record)
    return record


def build_harmonization_report(
    fixture_paths: list[str | Path],
    crosswalk_path: str | Path,
    schema_path: str | Path,
) -> dict[str, Any]:
    schema = load_harmonization_schema(schema_path)
    crosswalk = load_crosswalk(crosswalk_path)
    validate_crosswalk_against_schema(crosswalk, schema)
    records = [build_harmonized_record(path, crosswalk) for path in fixture_paths]

    entries = list(crosswalk["entries"])
    by_canonical: dict[str, list[dict[str, Any]]] = {}
    for entry in entries:
        by_canonical.setdefault(entry["canonical_indicator_id"], []).append(entry)

    indicators_harmonized = []
    for canonical_id, group in sorted(by_canonical.items()):
        if len(group) < 2:
            continue
        indicators_harmonized.append(
            {
                "canonical_indicator_id": canonical_id,
                "source_indicator_ids": [entry["source_indicator_id"] for entry in group],
                "source_ids": [entry["source_id"] for entry in group],
                "comparability_class": classify_group_comparability(group),
                "classification": "INFERENCIA",
            }
        )

    invalid_pair_examples = []
    for left in entries:
        for right in entries:
            if left["source_id"] == right["source_id"]:
                continue
            if classify_comparability(left, right) == "NOT_COMPARABLE":
                invalid_pair_examples.append(
                    {
                        "left": left["source_indicator_id"],
                        "right": right["source_indicator_id"],
                        "reason": "different canonical_indicator_id",
                        "comparability_class": "NOT_COMPARABLE",
                    }
                )
                break
        if invalid_pair_examples:
            break

    review_indicators = [
        {
            "canonical_indicator_id": entry["canonical_indicator_id"],
            "source_indicator_id": entry["source_indicator_id"],
            "source_id": entry["source_id"],
            "reason": "; ".join(entry["caveats"]),
        }
        for entry in entries
        if entry["comparability_class"] == "REVIEW"
    ]
    not_comparable_indicators = [
        {
            "canonical_indicator_id": entry["canonical_indicator_id"],
            "source_indicator_id": entry["source_indicator_id"],
            "source_id": entry["source_id"],
            "reason": "; ".join(entry["caveats"]),
        }
        for entry in entries
        if entry["comparability_class"] == "NOT_COMPARABLE"
    ]

    report = {
        "schema": "claudio.geodia_harmonization_report.v0_1",
        "schema_used": str(Path(schema_path).as_posix()),
        "crosswalk": str(Path(crosswalk_path).as_posix()),
        "generated_at_utc": crosswalk.get("generated_at_utc", "1970-01-01T00:00:00Z"),
        "offline_mode": True,
        "network_used": False,
        "publication_gate": "BLOCK",
        "classification": "INFERENCIA",
        "fixtures_evaluated": [
            {
                "path": str(Path(path).as_posix()),
                "source_id": record["source_id"],
                "country_or_region": record["country_or_region"],
                "year_range": record["year_range"],
                "source_card_ref": record.get("source_card_ref"),
                "license_status": record.get("license_status"),
                "license_review_required": record.get("license_review_required", True),
                "raw_source_hash": record.get("raw_source_hash"),
                "publication_gate": record["publication_gate"],
                "country_ordering": {
                    "status": "BLOCKED",
                    "reason": "not produced by harmonization v0.1",
                },
            }
            for path, record in zip(fixture_paths, records)
        ],
        "indicators_harmonized": indicators_harmonized,
        "indicators_in_review": review_indicators,
        "indicators_not_comparable": not_comparable_indicators,
        "invalid_pair_examples": invalid_pair_examples,
        "harmonized_records": {
            str(record["source_id"]): {
                "indicator_count": len(record["harmonized_indicators"]),
                "review_indicators": record["review_indicators"],
                "not_comparable_indicators": record["not_comparable_indicators"],
                "unmapped_source_indicator_ids": record["unmapped_source_indicator_ids"],
                "source_card_ref": record.get("source_card_ref"),
                "license_status": record.get("license_status"),
                "license_review_required": record.get("license_review_required", True),
                "raw_source_hash": record.get("raw_source_hash"),
                "publication_gate": record["publication_gate"],
            }
            for record in records
        },
        "caveats": [
            "Technical compatibility only; no social conclusion is produced.",
            "Country ordering is blocked.",
            "Economic growth remains REVIEW because provider definitions differ.",
            "License and terms review are required before redistribution.",
        ],
        "claims": [
            {
                "classification": "INFERENCIA",
                "text": "The CLI regenerated a technical harmonization report from local fixtures, crosswalk and schema.",
            }
        ],
        "blocked_actions": [
            "publication",
            "push",
            "deploy",
            "gumroad",
            "social_posting",
            "dns_change",
            "fred_api",
            "credential_use",
            "country_ordering",
            "social_claims_beyond_technical_scope",
        ],
    }
    validate_publication_gate(report)
    return report
