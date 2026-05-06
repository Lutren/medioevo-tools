"""Public-safe predictive method catalog for DUAT-style labs.

The catalog is a gate contract, not an inference engine. It helps DUAT decide
which forecasting or scenario method is allowed for a local research run.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Sequence


@dataclass(frozen=True)
class PredictiveMethod:
    method_id: str
    label: str
    family: str
    duat_role: str
    base_gate: str
    claim_boundary: str
    strengths: tuple[str, ...]
    limits: tuple[str, ...]
    required_evidence: tuple[str, ...]
    external_dependency: bool = False
    private_or_heavy: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "methodId": self.method_id,
            "label": self.label,
            "family": self.family,
            "duatRole": self.duat_role,
            "baseGate": self.base_gate,
            "claimBoundary": self.claim_boundary,
            "strengths": list(self.strengths),
            "limits": list(self.limits),
            "requiredEvidence": list(self.required_evidence),
            "externalDependency": self.external_dependency,
            "privateOrHeavy": self.private_or_heavy,
        }


def duat_predictive_catalog() -> list[PredictiveMethod]:
    """Return public-safe method specs for DUAT scenario work."""

    return [
        PredictiveMethod(
            method_id="local_baseline_forecast",
            label="Local baseline forecast",
            family="classical_time_series",
            duat_role="cheap falsifier and benchmark floor",
            base_gate="APPROVE",
            claim_boundary="scenario_only",
            strengths=("fast", "dependency_free", "easy_to_backtest"),
            limits=("weak_on_regime_shift", "no_deep_covariate_learning"),
            required_evidence=("holdout_backtest", "residual_report"),
        ),
        PredictiveMethod(
            method_id="chronos_foundation_forecast",
            label="Chronos / Chronos-2 time-series foundation model",
            family="foundation_time_series",
            duat_role="probabilistic scenario generator for measured time series",
            base_gate="REVIEW",
            claim_boundary="probabilistic_forecast_not_oracle",
            strengths=("zero_shot_candidate", "quantile_forecasts", "covariate_support_in_chronos_2"),
            limits=("requires_model_dependency", "needs_data_provenance", "no_social_certainty"),
            required_evidence=("model_license_review", "offline_fixture", "holdout_backtest", "calibration_error"),
            external_dependency=True,
            private_or_heavy=True,
        ),
        PredictiveMethod(
            method_id="state_space_kalman",
            label="State-space / Kalman-style tracker",
            family="state_space",
            duat_role="latent-state smoothing and uncertainty tracking",
            base_gate="APPROVE",
            claim_boundary="state_estimate_only",
            strengths=("interpretable_state", "online_updates", "uncertainty_tracking"),
            limits=("linear_assumptions", "requires_measurement_model"),
            required_evidence=("measurement_model", "innovation_residuals"),
        ),
        PredictiveMethod(
            method_id="agent_based_counterfactual",
            label="Agent-based counterfactual simulation",
            family="simulation",
            duat_role="synthetic what-if lab for policy and social cells",
            base_gate="APPROVE",
            claim_boundary="synthetic_counterfactual_only",
            strengths=("local", "explainable_rules", "pairs_well_with_conway"),
            limits=("fixture_quality_bound", "not_real_world_prediction"),
            required_evidence=("seed", "ruleset_hash", "scenario_report"),
        ),
        PredictiveMethod(
            method_id="causal_impact_synthetic_control",
            label="Causal impact / synthetic control",
            family="causal_inference",
            duat_role="event impact hypothesis under strict assumptions",
            base_gate="REVIEW",
            claim_boundary="causal_hypothesis_not_proof",
            strengths=("counterfactual_baseline", "useful_for_interventions"),
            limits=("assumption_sensitive", "confounding_risk"),
            required_evidence=("pre_period_fit", "assumption_register", "negative_controls"),
        ),
        PredictiveMethod(
            method_id="early_warning_anomaly",
            label="Early-warning anomaly detector",
            family="anomaly_detection",
            duat_role="risk signal for review queues",
            base_gate="APPROVE",
            claim_boundary="review_signal_only",
            strengths=("local", "good_for_alerts", "pairs_with_actiongate"),
            limits=("false_positives", "threshold_calibration_needed"),
            required_evidence=("threshold_record", "false_positive_log"),
        ),
        PredictiveMethod(
            method_id="ensemble_scenario_gate",
            label="Ensemble scenario gate",
            family="governance",
            duat_role="combine methods into APPROVE/REVIEW/BLOCK evidence",
            base_gate="APPROVE",
            claim_boundary="decision_support_only",
            strengths=("residue_aware", "method_disagreement_visible", "fits_witnesslog"),
            limits=("depends_on_inputs", "must_not_hide_disagreement"),
            required_evidence=("method_votes", "disagreement_residue", "witness_event"),
        ),
    ]


def evaluate_predictive_method(
    method: PredictiveMethod,
    *,
    external_models_allowed: bool = False,
    real_world_action: bool = False,
    social_prediction_claim: bool = False,
) -> dict[str, Any]:
    """Return the effective gate for a DUAT method in the current run."""

    gate = method.base_gate
    reasons: list[str] = []
    if method.external_dependency and not external_models_allowed:
        gate = "REVIEW"
        reasons.append("external_model_or_dependency_not_approved")
    if method.private_or_heavy and not external_models_allowed:
        reasons.append("heavy_or_private_model_route_requires_gate")
    if real_world_action:
        gate = "BLOCK"
        reasons.append("predictive_methods_may_not_execute_real_world_action")
    if social_prediction_claim:
        gate = "BLOCK"
        reasons.append("social_prediction_claim_is_blocked_without_professional_validation")
    if not reasons:
        reasons.append("method_within_current_local_research_boundary")
    payload = method.to_dict()
    payload.update({"effectiveGate": gate, "reasons": reasons})
    return payload


def select_duat_predictive_methods(
    *,
    goal: str = "scenario_lab",
    external_models_allowed: bool = False,
    real_world_action: bool = False,
    social_prediction_claim: bool = False,
) -> dict[str, Any]:
    """Build a gate-aware method list for a DUAT run."""

    evaluations = [
        evaluate_predictive_method(
            method,
            external_models_allowed=external_models_allowed,
            real_world_action=real_world_action,
            social_prediction_claim=social_prediction_claim,
        )
        for method in duat_predictive_catalog()
    ]
    return {
        "schemaVersion": "obsai.duat_predictive_method_selection.v1",
        "goal": goal,
        "claimBoundary": "scenario_generation_not_guaranteed_prediction",
        "methods": evaluations,
        "allowedMethodIds": [
            item["methodId"] for item in evaluations if item["effectiveGate"] == "APPROVE"
        ],
        "reviewMethodIds": [
            item["methodId"] for item in evaluations if item["effectiveGate"] == "REVIEW"
        ],
        "blockedMethodIds": [
            item["methodId"] for item in evaluations if item["effectiveGate"] == "BLOCK"
        ],
    }


def method_ids(methods: Sequence[PredictiveMethod]) -> tuple[str, ...]:
    return tuple(method.method_id for method in methods)
