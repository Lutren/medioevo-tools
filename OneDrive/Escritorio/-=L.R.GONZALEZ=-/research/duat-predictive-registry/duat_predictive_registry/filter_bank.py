"""Specialized DUAT filters for R dimensions."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FilterSpec:
    filter_id: str
    r_dimension: str
    purpose: str
    gate_on_high_r: str
    falsifier: str


FILTER_BANK: tuple[FilterSpec, ...] = (
    FilterSpec(
        "cognitive_residue_filter",
        "R_cognitive",
        "Separate nonlinear associations from unresolved ambiguity.",
        "REVIEW",
        "If metaphors cannot be translated into an operational instruction, keep as notes only.",
    ),
    FilterSpec(
        "entertainment_noise_filter",
        "R_entertainment",
        "Detect attention capture, novelty loops and dopamine-shaped distraction.",
        "REVIEW",
        "If entertainment content changes the technical decision, isolate it.",
    ),
    FilterSpec(
        "social_manipulation_filter",
        "R_social_manipulative",
        "Detect propaganda, coercive framing, tribal labels and engagement bait.",
        "BLOCK",
        "If a source urges action without evidence, demote it to manipulation risk.",
    ),
    FilterSpec(
        "temporal_drift_filter",
        "R_temporal",
        "Detect stale data, revision lag, schema drift and mismatch in frequency.",
        "REVIEW",
        "If timestamp, capture date or version is missing, require snapshot review.",
    ),
    FilterSpec(
        "source_quality_filter",
        "R_source",
        "Score provenance, license, coverage, stability and reproducibility.",
        "REVIEW",
        "If source card or terms are missing, integration cannot be approved.",
    ),
    FilterSpec(
        "contradiction_filter",
        "R_contra",
        "Detect conflicting requirements or incompatible claims.",
        "REVIEW",
        "If a critical contradiction remains unresolved, block execution.",
    ),
    FilterSpec(
        "sensitive_boundary_filter",
        "R_sensitive",
        "Detect secrets, PII, private material, legal/political risk and unsafe domains.",
        "BLOCK",
        "Any credential, PII, private RPG/TCG or electoral prediction request blocks.",
    ),
    FilterSpec(
        "model_risk_filter",
        "R_model",
        "Detect overfit, leakage, bad calibration and invalid causal interpretation.",
        "REVIEW",
        "If backtest is worse than baseline or leakage is detected, block production.",
    ),
    FilterSpec(
        "user_style_adapter",
        "R_user_style",
        "Preserve useful user cognitive style without letting it override facts.",
        "APPROVE",
        "If style changes technical content, lower beta or remove adaptation.",
    ),
    FilterSpec(
        "agent_clarity_filter",
        "R_agent_operational",
        "Transform mixed context into clear instructions, schemas and tests for agents.",
        "REVIEW",
        "If an agent cannot identify inputs, outputs and gates, require handoff repair.",
    ),
)


def filter_catalog() -> list[dict[str, str]]:
    return [spec.__dict__.copy() for spec in FILTER_BANK]


def required_filter_ids(r_scores: dict[str, float], threshold: float = 0.15) -> list[str]:
    required = []
    for spec in FILTER_BANK:
        if r_scores.get(spec.r_dimension, 0.0) >= threshold:
            required.append(spec.filter_id)
    return required
