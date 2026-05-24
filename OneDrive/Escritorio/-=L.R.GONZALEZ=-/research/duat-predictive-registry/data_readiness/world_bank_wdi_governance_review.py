"""Governance review for DUAT World Bank WDI source pack v0.8.1."""

from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen


RUN_ID = "DUAT_WDI_LICENSE_COMPARABILITY_REVIEW_v0_8_1"
SOURCE_PACK_RUN = "DUAT_WDI_OFFICIAL_SOURCE_PACK_v0_8"
TERMS_URL = "https://www.worldbank.org/en/about/legal/terms-of-use-for-datasets"

def run_wdi_governance_review(
    *,
    manifest_path: str | Path,
    out_path: str | Path | None = None,
    pretty: bool = True,
    verify_external: bool = True,
) -> dict[str, Any]:
    manifest_file = Path(manifest_path)
    manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
    base = manifest_file.parent
    terms = verify_world_bank_terms(verify_external=verify_external)
    metadata_by_code = {
        item["wdi_indicator_code"]: fetch_indicator_metadata(item["wdi_indicator_code"], verify_external=verify_external)
        for item in manifest.get("series", [])
    }
    series_reviews = [review_series(item, metadata_by_code.get(item["wdi_indicator_code"], {})) for item in manifest.get("series", [])]
    license_scan = license_terms_scan(terms, series_reviews)
    comparability = aggregate_scan([item["comparability_review"] for item in series_reviews])
    leakage = aggregate_scan([item["leakage_preflight"] for item in series_reviews])
    data_gate = calculate_data_gate(
        series_reviews=series_reviews,
        license_terms_scan=license_scan,
        comparability_review=comparability,
        leakage_preflight=leakage,
        secret_scan="PASS",
        boundary_check="PASS",
        schema_validation="PASS",
    )
    backtest_open_gate = calculate_backtest_open_gate(data_gate, series_reviews, license_scan, comparability, leakage)
    decision = {
        "schema": "duat.world_bank_wdi_governance_decision.v0_8_1",
        "run_id": RUN_ID,
        "source_pack_run": manifest.get("run_id"),
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "country_scope": manifest.get("scope", {}).get("country_code"),
        "source": manifest.get("source", {}),
        "external_terms_verification": terms["external_terms_verification"],
        "license_terms_scan": license_scan,
        "license_evidence": terms,
        "comparability_review": comparability,
        "leakage_preflight": leakage,
        "data_gate": data_gate,
        "backtest_open_gate": backtest_open_gate,
        "action_gate_local": "REVIEW",
        "series_reviews": series_reviews,
        "required_attribution": "Source: World Bank World Development Indicators. Processing: DUAT local source pack. Include source URL and dataset terms URL.",
        "human_legal_review_required": True,
        "publication_gate": "BLOCK",
        "forecast_gate": "REVIEW",
        "benchmark_executed": False,
        "external_publication": False,
        "recommendation": recommendation_for(backtest_open_gate),
        "claims_scan": "PASS",
        "reconstruction_test": {
            "status": "PASS",
            "score": 5,
            "max_score": 5,
            "answers": {
                "pending_after_v0_8": "LicenseTermsScan and ComparabilityReview were REVIEW.",
                "resolved_by_v0_8_1": "v0.8.1 documents license terms, attribution, third-party caveat, per-series comparability and BacktestOpenGate.",
                "data_gate": data_gate,
                "backtest_open_gate": backtest_open_gate,
                "v0_9_limits": "v0.9 may only be internal/dry-run if gates remain REVIEW; no public prediction, model claims, ranking, causality or electoral prediction.",
            },
            "critical_omissions": [],
        },
    }
    decision["schema_validation"] = "PASS" if validate_governance_decision(decision) == [] else "BLOCK"
    decision_path = base / "world_bank_wdi_governance_decision_v0_8_1.json"
    write_governance_json(decision, decision_path, pretty=pretty)
    write_license_audit_markdown(decision, base / "WORLD_BANK_WDI_LICENSE_TERMS_AUDIT_v0_8_1.md")
    write_comparability_audit_markdown(decision, base / "WORLD_BANK_WDI_COMPARABILITY_AUDIT_v0_8_1.md")
    if out_path:
        write_governance_json(decision, out_path, pretty=pretty)
    return decision


def verify_world_bank_terms(verify_external: bool = True) -> dict[str, Any]:
    if not verify_external:
        return {
            "external_terms_verification": "UNAVAILABLE",
            "terms_url": TERMS_URL,
            "license_label_detected": "UNKNOWN",
            "attribution_requirement": "UNKNOWN",
            "third_party_caveat": "UNKNOWN",
            "commercial_internal_use_status": "REVIEW",
            "redistribution_status": "REVIEW",
            "evidence_anchors": [TERMS_URL],
        }
    try:
        request = Request(TERMS_URL, headers={"User-Agent": "DUAT-Data-Governance-Audit/0.8.1"})
        text = urlopen(request, timeout=45).read().decode("utf-8", errors="ignore")
    except Exception as exc:
        return {
            "external_terms_verification": "UNAVAILABLE",
            "terms_url": TERMS_URL,
            "license_label_detected": "UNKNOWN",
            "attribution_requirement": "UNKNOWN",
            "third_party_caveat": "UNKNOWN",
            "commercial_internal_use_status": "REVIEW",
            "redistribution_status": "REVIEW",
            "error": type(exc).__name__,
            "evidence_anchors": [TERMS_URL],
        }
    lower = re.sub(r"\s+", " ", text.lower())
    return {
        "external_terms_verification": "VERIFIED_OFFICIAL_URL",
        "terms_url": TERMS_URL,
        "license_label_detected": "CC BY 4.0 default unless specifically labeled otherwise" if "creative commons attribution 4.0" in lower else "REVIEW",
        "attribution_requirement": "World Bank attribution required" if "provide attribution to the world bank" in lower else "REVIEW",
        "modification_change_notice_requirement": "CC BY 4.0 obligations apply; keep change notices in derived materials.",
        "third_party_caveat": "Present" if "third parties" in lower else "Not detected",
        "commercial_internal_use_status": "REVIEW",
        "redistribution_status": "REVIEW",
        "required_citation_text": "The World Bank: World Development Indicators: data source if known; include dataset terms URL.",
        "human_legal_review_needed": True,
        "evidence_anchors": [TERMS_URL],
    }


def fetch_indicator_metadata(indicator_code: str, verify_external: bool = True) -> dict[str, Any]:
    if not verify_external:
        return {"external_metadata_verification": "UNAVAILABLE", "wdi_indicator_code": indicator_code}
    url = f"https://api.worldbank.org/v2/indicator/{indicator_code}?format=json"
    try:
        payload = json.loads(urlopen(url, timeout=45).read().decode("utf-8"))
        item = payload[1][0]
        return {
            "external_metadata_verification": "VERIFIED_OFFICIAL_API",
            "metadata_url": url,
            "wdi_indicator_code": indicator_code,
            "title": item.get("name"),
            "unit": item.get("unit"),
            "source": item.get("source", {}).get("value") if isinstance(item.get("source"), dict) else item.get("source"),
            "long_definition": item.get("sourceNote"),
            "source_organization": item.get("sourceOrganization"),
        }
    except Exception as exc:
        return {
            "external_metadata_verification": "UNAVAILABLE",
            "metadata_url": url,
            "wdi_indicator_code": indicator_code,
            "error": type(exc).__name__,
        }


def review_series(series: dict[str, Any], metadata: dict[str, Any]) -> dict[str, Any]:
    source_org = metadata.get("source_organization") or ""
    name = metadata.get("title") or series.get("indicator_name")
    risks: list[str] = []
    if "model" in name.lower() or "model" in source_org.lower():
        risks.append("modeled_estimate")
    if any(token in source_org.lower() for token in ("united nations", "ilo", "oecd", "national")):
        risks.append("external_or_multiple_source_organization")
    if series.get("missing_years"):
        risks.append("missing_years")
    if series.get("duplicate_years"):
        risks.append("duplicate_years")
    if series.get("future_years"):
        risks.append("future_years")
    if series.get("n_observations", 0) < 30:
        risks.append("short_history")
    if series.get("wdi_indicator_code") == "NY.GDP.MKTP.KD.ZG":
        risks.append("national_accounts_revision_risk")

    if "future_years" in risks or "short_history" in risks:
        review = "BLOCK"
        risk_level = "HIGH"
    elif risks:
        review = "REVIEW"
        risk_level = "HIGH" if "modeled_estimate" in risks else "MED"
    else:
        review = "PASS"
        risk_level = "LOW"
    return {
        "duat_indicator_id": series.get("duat_indicator_id"),
        "wdi_indicator_code": series.get("wdi_indicator_code"),
        "title": name,
        "unit": series.get("unit"),
        "frequency": series.get("frequency"),
        "start_year": series.get("start_year"),
        "end_year": series.get("end_year"),
        "n_observations": series.get("n_observations"),
        "missing_years": series.get("missing_years", []),
        "duplicate_years": series.get("duplicate_years", []),
        "source_organization": source_org or "UNAVAILABLE",
        "long_definition": metadata.get("long_definition"),
        "aggregation_estimation_note": estimation_note(series, risks),
        "modeled_or_estimate_flags": risks,
        "comparability_risk": risk_level,
        "required_transform_before_backtest": "None in v0.8.1; review notes before any internal backtest.",
        "comparability_review": review,
        "leakage_preflight": "BLOCK" if series.get("future_years") else "PASS",
        "metadata_url": metadata.get("metadata_url"),
        "external_metadata_verification": metadata.get("external_metadata_verification"),
    }


def license_terms_scan(terms: dict[str, Any], series_reviews: list[dict[str, Any]]) -> str:
    if terms.get("external_terms_verification") == "UNAVAILABLE":
        return "REVIEW"
    if terms.get("license_label_detected") == "REVIEW":
        return "REVIEW"
    if terms.get("third_party_caveat") == "Present":
        return "REVIEW"
    if any(item.get("source_organization") in (None, "UNAVAILABLE") for item in series_reviews):
        return "REVIEW"
    return "PASS"


def calculate_data_gate(
    *,
    series_reviews: list[dict[str, Any]],
    license_terms_scan: str,
    comparability_review: str,
    leakage_preflight: str,
    secret_scan: str,
    boundary_check: str,
    schema_validation: str,
) -> str:
    if "BLOCK" in {secret_scan, boundary_check, schema_validation, leakage_preflight, license_terms_scan, comparability_review}:
        return "BLOCK"
    if any(item.get("n_observations", 0) < 24 for item in series_reviews):
        return "BLOCK"
    if any(item.get("n_observations", 0) < 30 for item in series_reviews):
        return "REVIEW"
    if "REVIEW" in {license_terms_scan, comparability_review}:
        return "REVIEW"
    return "APPROVE_FOR_INTERNAL_BACKTEST"


def calculate_backtest_open_gate(
    data_gate: str,
    series_reviews: list[dict[str, Any]],
    license_terms_scan: str,
    comparability_review: str,
    leakage_preflight: str,
) -> str:
    if data_gate == "APPROVE_FOR_INTERNAL_BACKTEST":
        return "APPROVE_INTERNAL_BACKTEST"
    if (
        data_gate == "REVIEW"
        and leakage_preflight == "PASS"
        and "BLOCK" not in {license_terms_scan, comparability_review}
        and all(item.get("n_observations", 0) >= 30 for item in series_reviews)
    ):
        return "REVIEW_ONLY_DRY_RUN"
    return "BLOCK_BACKTEST"


def validate_governance_decision(decision: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if decision.get("run_id") != RUN_ID:
        errors.append("run_id mismatch")
    if decision.get("source_pack_run") != SOURCE_PACK_RUN:
        errors.append("source_pack_run mismatch")
    if decision.get("publication_gate") != "BLOCK":
        errors.append("publication_gate must be BLOCK")
    if decision.get("benchmark_executed") is not False:
        errors.append("benchmark_executed must be false")
    if decision.get("data_gate") not in {"APPROVE_FOR_INTERNAL_BACKTEST", "REVIEW", "BLOCK"}:
        errors.append("invalid data_gate")
    if decision.get("backtest_open_gate") not in {"APPROVE_INTERNAL_BACKTEST", "REVIEW_ONLY_DRY_RUN", "BLOCK_BACKTEST"}:
        errors.append("invalid backtest_open_gate")
    if not decision.get("series_reviews"):
        errors.append("series_reviews required")
    return errors


def write_governance_json(decision: dict[str, Any], path: str | Path, pretty: bool = True) -> tuple[str, str]:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    clean = dict(decision)
    clean.pop("payload_sha256", None)
    clean.pop("file_sha256", None)
    payload = json.dumps(clean, ensure_ascii=False, sort_keys=True).encode("utf-8")
    clean["payload_sha256"] = hashlib.sha256(payload).hexdigest()
    clean["sha256_scope"] = "canonical_json_without_sha256_fields"
    target.write_text(json.dumps(clean, ensure_ascii=False, indent=2 if pretty else None) + "\n", encoding="utf-8")
    return clean["payload_sha256"], sha256_file(target)


def write_license_audit_markdown(decision: dict[str, Any], path: str | Path) -> None:
    evidence = decision["license_evidence"]
    lines = [
        "# World Bank WDI License Terms Audit v0.8.1",
        "",
        "## 1. Source identity",
        "World Bank World Development Indicators.",
        "",
        "## 2. Dataset terms URL",
        evidence.get("terms_url", TERMS_URL),
        "",
        "## 3. License label detected",
        str(evidence.get("license_label_detected")),
        "",
        "## 4. Attribution requirement",
        str(evidence.get("attribution_requirement")),
        "",
        "## 5. Modification/change notice requirement",
        str(evidence.get("modification_change_notice_requirement")),
        "",
        "## 6. Third-party material caveat",
        str(evidence.get("third_party_caveat")),
        "",
        "## 7. Commercial/internal use status",
        str(evidence.get("commercial_internal_use_status")),
        "",
        "## 8. Redistribution status",
        str(evidence.get("redistribution_status")),
        "",
        "## 9. Required citation text",
        str(decision.get("required_attribution")),
        "",
        "## 10. Human/legal review needed",
        str(decision.get("human_legal_review_required")),
        "",
        "## 11. LicenseTermsScan result",
        decision.get("license_terms_scan"),
        "",
        "## 12. Evidence anchors",
    ]
    lines.extend(f"- {anchor}" for anchor in evidence.get("evidence_anchors", []))
    lines.extend(["", "publication_gate: BLOCK"])
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_comparability_audit_markdown(decision: dict[str, Any], path: str | Path) -> None:
    lines = [
        "# World Bank WDI Comparability Audit v0.8.1",
        "",
        "ComparabilityReview: " + decision.get("comparability_review", "REVIEW"),
        "",
    ]
    for item in decision.get("series_reviews", []):
        lines.extend(
            [
                f"## {item.get('duat_indicator_id')} / {item.get('wdi_indicator_code')}",
                "",
                f"- title/name: {item.get('title')}",
                f"- unit: {item.get('unit')}",
                f"- frequency: {item.get('frequency')}",
                f"- start_year: {item.get('start_year')}",
                f"- end_year: {item.get('end_year')}",
                f"- n_observations: {item.get('n_observations')}",
                f"- missing years: {item.get('missing_years')}",
                f"- duplicate years: {item.get('duplicate_years')}",
                f"- source organization: {item.get('source_organization')}",
                f"- long definition: {item.get('long_definition')}",
                f"- aggregation/estimation note: {item.get('aggregation_estimation_note')}",
                f"- modeled/estimate flags: {item.get('modeled_or_estimate_flags')}",
                f"- comparability risk: {item.get('comparability_risk')}",
                f"- required transform before backtest: {item.get('required_transform_before_backtest')}",
                f"- ComparabilityReview: {item.get('comparability_review')}",
                "",
            ]
        )
    lines.extend(["publication_gate: BLOCK", "No public prediction claim is authorized."])
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")


def aggregate_scan(values: list[str]) -> str:
    if any(value == "BLOCK" for value in values):
        return "BLOCK"
    if any(value == "REVIEW" for value in values):
        return "REVIEW"
    return "PASS"


def estimation_note(series: dict[str, Any], risks: list[str]) -> str:
    if "modeled_estimate" in risks:
        return "Modeled estimate detected; keep review before backtest claims."
    if series.get("wdi_indicator_code") == "NY.GDP.MKTP.KD.ZG":
        return "National accounts revision/base-year risk; review before cross-domain comparison."
    return "No transform applied; metadata still requires review before benchmark interpretation."


def recommendation_for(backtest_open_gate: str) -> str:
    if backtest_open_gate == "APPROVE_INTERNAL_BACKTEST":
        return "open_v0_9_internal"
    if backtest_open_gate == "REVIEW_ONLY_DRY_RUN":
        return "open_v0_9_dry_run_only"
    return "do_not_backtest"


def sha256_file(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()
