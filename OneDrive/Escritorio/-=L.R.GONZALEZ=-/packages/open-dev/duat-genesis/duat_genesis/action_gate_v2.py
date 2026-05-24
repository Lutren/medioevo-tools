from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


GateDecision = Literal["APPROVE", "REVIEW", "BLOCK"]


@dataclass(frozen=True)
class ActionGateInput:
    evidence: float
    risk: float
    reversibility: float
    authorization: float
    phi_eff: float
    r_delta_expected: float
    touches_secrets: bool
    external_publish: bool
    destructive: bool
    permanent_delete: bool = False
    value_absorbed: bool = False
    manifest_created: bool = False


@dataclass(frozen=True)
class ActionGateResult:
    decision: GateDecision
    score: float
    reasons: tuple[str, ...]
    next_action: str


def _bounded(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def action_gate_v2(input: ActionGateInput) -> ActionGateResult:
    evidence = _bounded(input.evidence)
    risk = _bounded(input.risk)
    reversibility = _bounded(input.reversibility)
    authorization = _bounded(input.authorization)
    phi_eff = _bounded(input.phi_eff)
    reasons: list[str] = []

    if input.touches_secrets:
        reasons.append("Touches secrets or credentials.")
    if input.destructive and not input.permanent_delete:
        reasons.append("Destructive action.")
    if input.permanent_delete and not input.value_absorbed:
        reasons.append("Permanent delete requested before value absorption.")
    if input.permanent_delete and not input.manifest_created:
        reasons.append("Permanent delete requested before manifest.")
    if authorization < 0.5:
        reasons.append("Insufficient authorization.")
    if evidence < 0.55 and risk > 0.3:
        reasons.append("Evidence too low for risk level.")
    if phi_eff < 0.6:
        reasons.append("Phi_eff below operational threshold.")
    if input.external_publish and risk > 0.6:
        reasons.append("External publication risk too high.")

    if input.touches_secrets or (input.destructive and not input.permanent_delete):
        return ActionGateResult(
            decision="BLOCK",
            score=0.0,
            reasons=tuple(reasons),
            next_action="Remove secret/destructive path or create a reviewed plan.",
        )

    if input.permanent_delete and (not input.value_absorbed or not input.manifest_created):
        return ActionGateResult(
            decision="REVIEW",
            score=0.4,
            reasons=tuple(reasons),
            next_action="Absorb useful value, create manifest, then delete only approved residue.",
        )

    score = (
        evidence * 0.25
        + (1.0 - risk) * 0.2
        + reversibility * 0.15
        + authorization * 0.2
        + phi_eff * 0.1
        + (0.1 if input.r_delta_expected <= 0 else -0.05)
    )
    score = round(max(0.0, min(1.0, score)), 6)

    if score >= 0.72 and not reasons:
        return ActionGateResult(
            decision="APPROVE",
            score=score,
            reasons=("Sufficient evidence, authorization, documentation and acceptable risk.",),
            next_action="Execute and write WitnessLog.",
        )

    return ActionGateResult(
        decision="REVIEW",
        score=score,
        reasons=tuple(reasons),
        next_action="Complete missing evidence, reduce risk, or isolate action behind documented procedure.",
    )
