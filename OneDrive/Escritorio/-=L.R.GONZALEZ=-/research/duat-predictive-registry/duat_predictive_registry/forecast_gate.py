"""ForecastGate rules for DUAT predictive registry."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ForecastGateInput:
    has_source_card: bool
    has_backtest: bool
    data_leakage_detected: bool = False
    unsupported_causality_claim: bool = False
    forbidden_domain_claim: bool = False
    brier_score: float | None = None
    baseline_brier: float | None = None
    R_pred: float = 1.0


def forecast_gate(gate_input: ForecastGateInput | dict[str, object]) -> dict[str, str]:
    if isinstance(gate_input, ForecastGateInput):
        item = gate_input
    else:
        item = ForecastGateInput(**gate_input)

    if not item.has_source_card:
        return {"gate": "REVIEW", "reason": "missing_source_card"}
    if not item.has_backtest:
        return {"gate": "REVIEW", "reason": "missing_backtest"}
    if item.data_leakage_detected:
        return {"gate": "BLOCK", "reason": "data_leakage_detected"}
    if item.unsupported_causality_claim:
        return {"gate": "BLOCK", "reason": "unsupported_causality_claim"}
    if item.forbidden_domain_claim:
        return {"gate": "BLOCK", "reason": "forbidden_domain_claim"}
    if (
        item.brier_score is not None
        and item.baseline_brier is not None
        and item.brier_score > item.baseline_brier
    ):
        return {"gate": "BLOCK_PRODUCTION", "reason": "worse_than_baseline_brier"}
    if item.R_pred >= 0.60:
        return {"gate": "BLOCK", "reason": "r_pred_high"}
    if item.R_pred >= 0.35:
        return {"gate": "REVIEW", "reason": "r_pred_review"}
    return {"gate": "APPROVE", "reason": "forecast_gate_passed"}
