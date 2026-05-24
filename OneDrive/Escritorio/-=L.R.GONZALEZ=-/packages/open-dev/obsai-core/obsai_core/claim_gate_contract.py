"""Canonical claim gate contract for obsai-core.

This module unifies the operational gates used by the MEDIOEVO/OSIT claim
pipeline into one dependency-free, serializable contract:

- TruthGate
- C-GATE
- PhysicsHonestyGate
- ScienceClaimGate

Calibration is DEMO_ONLY. The contract is an engineering control surface, not a
scientific validation claim.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import asdict, dataclass
from typing import Any, Literal

GateDecision = Literal["APPROVE", "REVIEW", "BLOCK"]

CONTRACT_VERSION = "obsai.claim_gate_contract.v1"
CANONICAL_CLAIM_GATES = (
    "TruthGate",
    "C-GATE",
    "PhysicsHonestyGate",
    "ScienceClaimGate",
)
CONTROLLED_DOMAIN_TERMS = (
    "agi",
    "cancer",
    "consciencia",
    "consciousness",
    "cura",
    "cure",
    "fisica",
    "física",
    "ia actual",
    "medical",
    "medicine",
    "new physics",
    "nueva fisica",
    "nueva física",
    "sentient",
)


@dataclass(frozen=True)
class GateOutcome:
    name: str
    status: GateDecision
    reason: str


@dataclass(frozen=True)
class ClaimGateContract:
    schemaVersion: str
    gates: list[GateOutcome]
    final_decision: GateDecision
    calibration: str = "DEMO_ONLY"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_claim_gate_contract(claim: Any, clarity_threshold: float = 0.60) -> dict[str, Any]:
    """Build a serializable unified gate contract for a claim result."""
    label = str(_field(claim, "label", default="INCOGNITA")).upper()
    gate = _normalize_decision(_field(claim, "gate", default="REVIEW"))
    clarity = _float(_field(claim, "clarity", default=0.0))
    r_or = _float(_field(claim, "R_or", default=1.0))
    science_gate_triggered = bool(_field(claim, "science_gate_triggered", default=False))
    text = str(_field(claim, "text", default=""))
    text_lower = text.lower()
    controlled_domain = any(term in text_lower for term in CONTROLLED_DOMAIN_TERMS)

    truth_gate = _truth_gate(label, gate, r_or)
    c_gate = _communication_gate(clarity, clarity_threshold)
    physics_gate = _physics_honesty_gate(label, gate, controlled_domain, science_gate_triggered)
    science_gate = _science_claim_gate(label, controlled_domain, science_gate_triggered)
    gates = [truth_gate, c_gate, physics_gate, science_gate]
    final_decision = _combine([gate, *(item.status for item in gates)])

    return ClaimGateContract(
        schemaVersion=CONTRACT_VERSION,
        gates=gates,
        final_decision=final_decision,
    ).to_dict()


def _truth_gate(label: str, gate: GateDecision, r_or: float) -> GateOutcome:
    if gate == "BLOCK" or label == "BLOQUEO":
        return GateOutcome("TruthGate", "BLOCK", "blocked claim cannot enter canon")
    if label == "INCOGNITA" or r_or >= 0.45:
        return GateOutcome("TruthGate", "REVIEW", "claim needs more evidence before canon")
    return GateOutcome("TruthGate", "APPROVE", "claim has enough operational support")


def _communication_gate(clarity: float, threshold: float) -> GateOutcome:
    if clarity < threshold:
        return GateOutcome("C-GATE", "REVIEW", f"clarity={clarity:.2f} below {threshold:.2f}")
    return GateOutcome("C-GATE", "APPROVE", f"clarity={clarity:.2f} meets threshold")


def _physics_honesty_gate(
    label: str,
    gate: GateDecision,
    controlled_domain: bool,
    science_gate_triggered: bool,
) -> GateOutcome:
    if science_gate_triggered or gate == "BLOCK" or label == "BLOQUEO":
        return GateOutcome("PhysicsHonestyGate", "BLOCK", "strong external claim must not be stated as fact")
    if controlled_domain:
        return GateOutcome("PhysicsHonestyGate", "REVIEW", "controlled domain requires explicit boundary")
    return GateOutcome("PhysicsHonestyGate", "APPROVE", "no controlled physics/AGI/medical domain detected")


def _science_claim_gate(
    label: str,
    controlled_domain: bool,
    science_gate_triggered: bool,
) -> GateOutcome:
    if science_gate_triggered or label == "BLOQUEO":
        return GateOutcome("ScienceClaimGate", "BLOCK", "ScienceClaimGate triggered")
    if controlled_domain:
        return GateOutcome("ScienceClaimGate", "REVIEW", "controlled domain requires verified evidence")
    return GateOutcome("ScienceClaimGate", "APPROVE", "not a controlled external science claim")


def _combine(decisions: list[GateDecision]) -> GateDecision:
    if "BLOCK" in decisions:
        return "BLOCK"
    if "REVIEW" in decisions:
        return "REVIEW"
    return "APPROVE"


def _normalize_decision(value: Any) -> GateDecision:
    text = str(value).upper()
    if text == "APPROVE":
        return "APPROVE"
    if text == "BLOCK":
        return "BLOCK"
    return "REVIEW"


def _field(source: Any, name: str, default: Any) -> Any:
    if isinstance(source, Mapping):
        return source.get(name, default)
    return getattr(source, name, default)


def _float(value: Any) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return 0.0
    if number < 0.0:
        return 0.0
    if number > 1.0:
        return 1.0
    return number
