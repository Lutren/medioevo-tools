"""DUAT benchmark matrix v0.3."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .benchmarking import run_benchmark
from .comparability import build_comparability_review
from .license_review import build_license_review
from .objectives import find_workspace_root, load_objective, resolve_workspace_path


RUN_ID = "DUAT_PREDICTIVE_BENCHMARK_MATRIX_v0_3"
RUN_ID_V0_4 = "DUAT_BENCHMARK_MATRIX_v0_4"


def run_benchmark_matrix(
    objective_paths: list[str | Path],
    workspace_root: str | Path | None = None,
    run_id: str = RUN_ID,
    schema: str = "duat.benchmark_matrix.v0_3",
) -> dict[str, Any]:
    root = Path(workspace_root or find_workspace_root()).resolve()
    objectives = [load_objective(resolve_workspace_path(path, root)) for path in objective_paths]
    benchmark_reports = [run_benchmark(resolve_workspace_path(path, root), root) for path in objective_paths]
    rows = [matrix_row(report) for report in benchmark_reports]
    replication_status = classify_replication(rows)
    metric_caveats = metric_caveats_for_rows(rows)
    license_review = build_license_review(objectives, root)
    comparability_review = build_comparability_review(objectives, root)
    return {
        "schema": schema,
        "run_id": run_id,
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "publication_gate": "BLOCK",
        "action_gate_local": "REVIEW" if license_review["license_terms_scan"] == "REVIEW" else _action_gate_from_rows(rows),
        "objectives": rows,
        "matrix_interpretation": {
            "replication_status": replication_status,
            "claim_level": "internal_technical_evidence_only",
            "public_claim_allowed": False,
            "interpretation_note": _interpretation_note(replication_status, metric_caveats),
            "metric_caveats": metric_caveats,
        },
        "license_review": license_review,
        "comparability_review": comparability_review,
        "raw_reports": benchmark_reports,
        "scans": {
            "LicenseTermsScan": license_review["license_terms_scan"],
            "LeakageCheck": "PASS" if all(row["leakage_check"] == "PASS" for row in rows) else "BLOCK",
            "PublicationGateScan": "PASS",
        },
    }


def matrix_row(report: dict[str, Any]) -> dict[str, Any]:
    return {
        "objective_id": report.get("objective_id"),
        "indicator": report.get("canonical_indicator_id"),
        "data_mode": report.get("data_mode"),
        "r_before": report.get("r_before"),
        "r_after": report.get("r_after"),
        "r_delta": report.get("r_delta"),
        "forecast_gate": report.get("forecast_gate"),
        "publication_gate": report.get("publication_gate", "BLOCK"),
        "license_terms_scan": report.get("license_terms_scan"),
        "leakage_check": report.get("leakage_check"),
        "n_observations": len(report.get("actual", [])),
        "n_splits": report.get("timeseries_split", {}).get("fold_count"),
        "coverage": 1.0 if report.get("actual") else 0.0,
        "source_quality": report.get("source_quality", {}).get("enhanced_average"),
        "baseline_metrics": report.get("baseline_metrics", {}).get("selected", {}),
        "enhanced_metrics": report.get("enhanced_metrics", {}),
    }


def classify_replication(rows: list[dict[str, Any]]) -> str:
    if not rows or any(row.get("data_mode") != "real_fixture" for row in rows):
        return "BLOCKED_NO_DATA"
    if any(row.get("leakage_check") != "PASS" for row in rows):
        return "BLOCKED_NO_DATA"
    deltas = [row.get("r_delta") for row in rows]
    if any(delta is None for delta in deltas):
        return "BLOCKED_NO_DATA"
    labor_rows = [row for row in rows if row.get("indicator") == "labor_market.unemployment_rate.total"]
    if labor_rows and any(row["r_delta"] >= 0 for row in labor_rows):
        return "NOT_REPLICATED"
    if all(delta < 0 for delta in deltas):
        if any(abs(delta) < 0.01 for delta in deltas):
            return "MIXED_LOCAL"
        return "REPLICATED_LOCAL"
    if any(delta < 0 for delta in deltas):
        return "MIXED_LOCAL"
    return "NOT_REPLICATED"


def metric_caveats_for_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    caveats: list[dict[str, Any]] = []
    for row in rows:
        baseline_mae = row.get("baseline_metrics", {}).get("MAE")
        enhanced_mae = row.get("enhanced_metrics", {}).get("MAE")
        if baseline_mae is not None and enhanced_mae is not None and enhanced_mae > baseline_mae:
            caveats.append(
                {
                    "indicator": row.get("indicator"),
                    "status": "ENHANCED_MAE_WORSE_THAN_SELECTED_BASELINE",
                    "baseline_mae": baseline_mae,
                    "enhanced_mae": enhanced_mae,
                    "note": "R_delta improved through SourceQuality/R components, but raw MAE worsened; do not treat as robust predictive accuracy gain.",
                }
            )
    return caveats


def validate_matrix_shape(matrix: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if matrix.get("run_id") not in {RUN_ID, RUN_ID_V0_4}:
        errors.append("run_id mismatch")
    if matrix.get("publication_gate") != "BLOCK":
        errors.append("publication_gate must be BLOCK")
    if not isinstance(matrix.get("objectives"), list) or not matrix["objectives"]:
        errors.append("objectives must be a non-empty list")
    interpretation = matrix.get("matrix_interpretation", {})
    if interpretation.get("public_claim_allowed") is not False:
        errors.append("public_claim_allowed must be false")
    return errors


def write_matrix_json(matrix: dict[str, Any], path: str | Path, pretty: bool = True) -> str:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(matrix, ensure_ascii=False, indent=2 if pretty else None) + "\n", encoding="utf-8")
    import hashlib

    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    matrix["sha256"] = digest
    target.write_text(json.dumps(matrix, ensure_ascii=False, indent=2 if pretty else None) + "\n", encoding="utf-8")
    return digest


def write_matrix_markdown(matrix: dict[str, Any], path: str | Path) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    title = "DUAT Benchmark Matrix v0.4" if matrix.get("run_id") == RUN_ID_V0_4 else "DUAT Benchmark Matrix v0.3"
    lines = [
        f"# {title}",
        "",
        "publication_gate: BLOCK",
        f"run_id: {matrix.get('run_id')}",
        f"replication_status: {matrix.get('matrix_interpretation', {}).get('replication_status')}",
        "",
        "## Matrix",
        "",
        "| indicator | data_mode | R_before | R_after | R_delta | ForecastGate |",
        "|---|---|---:|---:|---:|---|",
    ]
    for row in matrix.get("objectives", []):
        lines.append(
            f"| {row.get('indicator')} | {row.get('data_mode')} | {row.get('r_before')} | "
            f"{row.get('r_after')} | {row.get('r_delta')} | {row.get('forecast_gate')} |"
        )
    lines.extend(
        [
            "",
            "## Claim Boundary",
            "",
            "Internal local benchmark only. Not public validation, not a public predictive claim, no ranking and no causal assertion.",
            "R reduction does not equal predictive validation; metric deltas require domain calibration.",
        ]
    )
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_license_comparability_markdown(matrix: dict[str, Any], path: str | Path) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    license_review = matrix["license_review"]
    comparability_review = matrix["comparability_review"]
    lines = [
        "# DUAT License And Comparability Review v0.1",
        "",
        "publication_gate: BLOCK",
        "",
        "LicenseTermsScan remains REVIEW pending human/legal review.",
        "",
        "## Sources And Fixtures",
        "",
    ]
    for fixture in license_review.get("fixtures", []):
        lines.extend(
            [
                f"- Fixture: `{fixture.get('fixture')}`",
                f"  - Source: {fixture.get('source_id')}",
                f"  - URL: {fixture.get('source_url')}",
                f"  - Geography: {fixture.get('geography')}",
                f"  - Period: {fixture.get('period')}",
                f"  - License status: {fixture.get('license_status')}",
                f"  - Publication gate: {fixture.get('publication_gate')}",
            ]
        )
    lines.extend(["", "## Comparability", ""])
    for review in comparability_review.get("reviews", []):
        lines.append(f"### {review.get('indicator')}")
        lines.append(f"- Objective: {review.get('objective_id')}")
        lines.append(f"- Review status: {review.get('review_status')}")
        for entry in review.get("entries", []):
            lines.extend(
                [
                    f"- {entry.get('source_id')} / {entry.get('source_indicator_id')} / {entry.get('country_or_region')}",
                    f"  - Frequency: {entry.get('frequency')}",
                    f"  - Years: {entry.get('year_range')}",
                    f"  - Units: {entry.get('unit_original')} -> {entry.get('unit_canonical')}",
                    f"  - Transformation: {entry.get('transformation_applied')}",
                    f"  - Comparability: {entry.get('comparability_class')}",
                    f"  - Missing values: none observed in fixture benchmark rows",
                    f"  - Caveats: {'; '.join(entry.get('caveats') or [])}",
                ]
            )
    lines.extend(
        [
            "",
            "## What Is Missing For PASS",
            "",
            "- Human/legal review of source-specific redistribution terms.",
            "- Approved public-safe attribution text per source.",
            "- Explicit decision that derived fixture redistribution is allowed.",
            "- More historical folds before any stronger public-facing language.",
        ]
    )
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _action_gate_from_rows(rows: list[dict[str, Any]]) -> str:
    if any(row.get("forecast_gate") == "BLOCK" for row in rows):
        return "BLOCK"
    if any(row.get("forecast_gate") == "REVIEW" for row in rows):
        return "REVIEW"
    return "APPROVE_LOCAL"


def _interpretation_note(status: str, metric_caveats: list[dict[str, Any]] | None = None) -> str:
    caveat_suffix = ""
    if metric_caveats:
        caveat_suffix = " Metric caveats exist; report them before any stronger interpretation."
    if status == "REPLICATED_LOCAL":
        return "R_delta is negative for all real-fixture objectives; this is internal technical evidence only." + caveat_suffix
    if status == "NOT_REPLICATED":
        return "The second real-fixture objective did not improve; report as boundary evidence." + caveat_suffix
    if status == "BLOCKED_NO_DATA":
        return "Real fixture evidence was insufficient; synthetic data cannot count as predictive evidence."
    return "Evidence is mixed or too small for stronger claims." + caveat_suffix
