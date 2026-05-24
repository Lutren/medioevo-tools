"""Pre-generation gate for local agent outputs."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Dict, List

from .agency import AgencyLevel, can_generate, classify_agency
from .core import EstadoPSI, clamp
from .gates import GateStatus


REALITY_CHECK_TYPES = {"factual", "code", "plan"}


@dataclass
class GenerationProposal:
    content_type: str = "general"
    requires_sources: bool = False
    is_irreversible: bool = False
    confidence_claimed: float = 0.0
    token_count_estimate: int = 0
    task_risk: str = "low"
    metadata: Dict[str, str] = field(default_factory=dict)


@dataclass
class GenerationGateDecision:
    status: GateStatus
    agency_level: AgencyLevel
    hallucination_risk: float
    reasons: List[str] = field(default_factory=list)

    @property
    def approved(self) -> bool:
        return self.status in {GateStatus.ALLOW, GateStatus.DRY_RUN}

    def to_dict(self) -> dict:
        payload = asdict(self)
        payload["status"] = self.status.value
        payload["agency_level"] = self.agency_level.value
        return payload


def evaluate_generation(
    proposal: GenerationProposal,
    psi: EstadoPSI,
    *,
    evidence_count: int = 0,
) -> GenerationGateDecision:
    content_type = proposal.content_type.lower()
    requires_reality_check = (
        content_type in REALITY_CHECK_TYPES
        or proposal.requires_sources
        or proposal.is_irreversible
    )
    agency = classify_agency(
        phi_eff=psi.Phi_eff,
        r=psi.R,
        evidence_count=evidence_count,
        requires_reality_check=requires_reality_check,
    )
    risk = _hallucination_risk(proposal, psi, evidence_count=evidence_count)
    reasons: list[str] = []

    if psi.R >= psi.J_c:
        reasons.append("psi_jamming")
        return GenerationGateDecision(GateStatus.BLOCK, agency, risk, reasons)

    if proposal.requires_sources and evidence_count == 0:
        reasons.append("sources_required_without_evidence")
    if content_type in REALITY_CHECK_TYPES and agency != AgencyLevel.DELIBERATIVE:
        reasons.append("reality_check_requires_deliberative_agency")
    if proposal.is_irreversible and agency != AgencyLevel.DELIBERATIVE:
        reasons.append("irreversible_generation_requires_deliberative_agency")
    if not can_generate(agency, task_risk=proposal.task_risk):
        reasons.append("agency_level_cannot_generate_for_risk")

    if reasons:
        return GenerationGateDecision(GateStatus.BLOCK, agency, risk, reasons)
    if risk >= 0.55:
        return GenerationGateDecision(GateStatus.HUMAN_REVIEW, agency, risk, ["high_hallucination_risk"])
    return GenerationGateDecision(GateStatus.DRY_RUN, agency, risk, ["pre_generation_gate_passed_dry_run"])


def _hallucination_risk(
    proposal: GenerationProposal,
    psi: EstadoPSI,
    *,
    evidence_count: int,
) -> float:
    base_by_type = {
        "creative": 0.18,
        "general": 0.25,
        "plan": 0.36,
        "code": 0.42,
        "factual": 0.48,
    }
    risk = base_by_type.get(proposal.content_type.lower(), 0.30)
    risk += 0.30 * psi.R
    if proposal.confidence_claimed >= 0.80 and evidence_count == 0:
        risk += 0.20
    if proposal.requires_sources and evidence_count == 0:
        risk += 0.25
    if proposal.token_count_estimate > 4000:
        risk += 0.08
    return round(clamp(risk, 0.0, 1.0), 4)

