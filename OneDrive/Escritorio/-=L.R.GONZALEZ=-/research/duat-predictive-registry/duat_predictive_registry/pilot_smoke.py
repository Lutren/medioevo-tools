"""Offline-safe pilot smoke utilities."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from .forecast_gate import ForecastGateInput, forecast_gate
from .scoring import coverage, freshness, h_eff_pred, r_pred
from .source_quality import SourceQualityInputs, compute_r_source, compute_source_quality


def pilot_source_scores() -> list[dict[str, Any]]:
    """Return offline source scores for the no-key pilot.

    The report is synthetic smoke evidence: it verifies formulas and gates but
    does not claim live data retrieval or forecast validity.
    """

    specs = [
        ("open_meteo", "geophysical_weather", SourceQualityInputs(0.85, 0.70, 0.80, 0.85, 0.80, 0.85, 0.75)),
        ("world_bank", "macroeconomic", SourceQualityInputs(0.90, 0.75, 0.85, 0.70, 0.85, 0.90, 0.85)),
        ("gdelt", "media_events", SourceQualityInputs(0.72, 0.65, 0.75, 0.75, 0.82, 0.70, 0.72)),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, domain, inputs in specs:
        source_quality = compute_source_quality(inputs)
        source_r = compute_r_source(source_quality)
        R_pred = r_pred(source_r, R_missing=0.10, R_temporal=0.12, R_contra=0.05, R_model=0.20)
        gate = forecast_gate(
            ForecastGateInput(
                has_source_card=True,
                has_backtest=False,
                R_pred=R_pred,
            )
        )
        rows.append(
            {
                "source_id": source_id,
                "domain": domain,
                "synthetic_smoke_test": True,
                "source_quality": round(source_quality, 4),
                "R_source": round(source_r, 4),
                "R_pred": round(R_pred, 4),
                "H_eff_pred_demo": round(
                    h_eff_pred(
                        H_raw=0.70,
                        SourceQuality=source_quality,
                        Freshness=freshness(1),
                        Coverage=coverage(95, 100),
                        Phi_eff=0.85,
                        CalibrationScore=0.70,
                        FilterFit=0.90,
                    ),
                    4,
                ),
                "forecast_gate": gate,
            }
        )
    return rows


def build_pilot_smoke_report() -> dict[str, Any]:
    rows = pilot_source_scores()
    return {
        "schema": "duat.pilot_smoke_report.v0_1",
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "publication_gate": "BLOCK",
        "external_publication": False,
        "network_used": False,
        "sources": rows,
        "claims": [
            {
                "classification": "INFERENCIA",
                "text": "Pilot smoke verifies formula plumbing, not real forecast validity.",
            }
        ],
    }
