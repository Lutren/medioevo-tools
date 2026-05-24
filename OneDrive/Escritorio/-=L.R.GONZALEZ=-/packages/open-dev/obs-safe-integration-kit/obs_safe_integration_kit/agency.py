"""Agency-state helpers for local-first agent gating.

The model is a clean-room runtime contract derived from curated POST insights:
separate metacognition, control, evidence and residue before generation.
"""
from __future__ import annotations

from enum import Enum


class AgencyLevel(str, Enum):
    REACTIVE = "REACTIVE"
    AUTONOMOUS = "AUTONOMOUS"
    OBSERVER = "OBSERVER"
    DELIBERATIVE = "DELIBERATIVE"


PHI_METACOG_THRESHOLD = 0.55
PHI_CONTROL_THRESHOLD = 0.60
R_ALARM_THRESHOLD = 0.40
EVIDENCE_MIN = 2


def classify_agency(
    *,
    phi_eff: float,
    r: float,
    evidence_count: int,
    requires_reality_check: bool = True,
) -> AgencyLevel:
    """Classify an agent state before it generates output.

    `AUTONOMOUS` is allowed only for low-risk contexts that do not require a
    reality check; factual/code/plan work should be `DELIBERATIVE` or blocked.
    """

    if r >= R_ALARM_THRESHOLD:
        return AgencyLevel.OBSERVER

    has_control = phi_eff >= PHI_CONTROL_THRESHOLD
    has_metacognition = phi_eff >= PHI_METACOG_THRESHOLD and evidence_count >= EVIDENCE_MIN

    if has_control and has_metacognition:
        return AgencyLevel.DELIBERATIVE
    if has_control and not has_metacognition:
        return AgencyLevel.OBSERVER if requires_reality_check else AgencyLevel.AUTONOMOUS
    if has_metacognition:
        return AgencyLevel.OBSERVER
    return AgencyLevel.REACTIVE


def can_generate(level: AgencyLevel, *, task_risk: str = "low") -> bool:
    risk = task_risk.lower()
    if level == AgencyLevel.DELIBERATIVE:
        return True
    if level == AgencyLevel.AUTONOMOUS:
        return risk == "low"
    if level == AgencyLevel.REACTIVE:
        return risk == "low"
    return False


def describe_agency(level: AgencyLevel) -> str:
    return {
        AgencyLevel.REACTIVE: "Accion sin planificacion completa; solo tareas de bajo riesgo.",
        AgencyLevel.AUTONOMOUS: "Control sin evidencia suficiente; no usar para realidad/factual/codigo.",
        AgencyLevel.OBSERVER: "Metacognicion o alarma activa; observar y pedir evidencia antes de actuar.",
        AgencyLevel.DELIBERATIVE: "Evidencia, control y gate suficientes para accion local revisada.",
    }[level]

