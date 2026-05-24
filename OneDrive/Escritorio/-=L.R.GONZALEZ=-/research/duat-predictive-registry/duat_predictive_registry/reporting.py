"""Report writers for DUAT predictive benchmarks."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


def write_json_report(report: dict[str, Any], path: str | Path, pretty: bool = True) -> str:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(report, ensure_ascii=False, indent=2 if pretty else None)
    target.write_text(text + "\n", encoding="utf-8")
    digest = sha256_file(target)
    report["sha256"] = digest
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2 if pretty else None) + "\n", encoding="utf-8")
    return digest


def write_markdown_report(report: dict[str, Any], path: str | Path) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# DUAT R_before/R_after Benchmark v0.1",
        "",
        "publication_gate: BLOCK",
        f"objective_id: {report.get('objective_id')}",
        f"data_mode: {report.get('data_mode')}",
        f"canonical_indicator_id: {report.get('canonical_indicator_id')}",
        "",
        "## Resultado",
        "",
        f"- R_before: {report.get('r_before')}",
        f"- R_after: {report.get('r_after')}",
        f"- R_delta: {report.get('r_delta')}",
        f"- ForecastGate: {report.get('forecast_gate')}",
        f"- LicenseTermsScan: {report.get('license_terms_scan')}",
        f"- LeakageCheck: {report.get('leakage_check')}",
        "",
        "## Interpretacion",
        "",
        "Este benchmark es retrospectivo y local. No autoriza publicacion, ranking, causalidad ni prediccion publica.",
        "",
        "## Series",
        "",
    ]
    for series in report.get("series", []):
        lines.append(
            f"- {series['series_id']}: comparability={series['comparability_class']}, "
            f"source_quality={series['source_quality']}, folds={len(series['actual'])}"
        )
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")


def sha256_file(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()
