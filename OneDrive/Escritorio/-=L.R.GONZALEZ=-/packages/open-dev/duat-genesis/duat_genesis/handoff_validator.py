from __future__ import annotations

from dataclasses import dataclass


REQUIRED_HANDOFF_SECTIONS = (
    "ESTADO",
    "CERTEZA",
    "INFERENCIA",
    "INCOGNITA",
    "ACCION",
    "ARTEFACTO",
    "HANDOFF",
)


@dataclass(frozen=True)
class HandoffValidationResult:
    ok: bool
    missing_sections: tuple[str, ...]
    reasons: tuple[str, ...]


def validate_handoff_text(text: str) -> HandoffValidationResult:
    normalized = text.upper()
    missing = tuple(section for section in REQUIRED_HANDOFF_SECTIONS if section not in normalized)
    reasons: list[str] = []
    if missing:
        reasons.append("handoff is missing required sections")
    if "NEXT" not in normalized and "PROXIMA" not in normalized and "SIGUIENTE" not in normalized:
        reasons.append("handoff does not expose a next action")
    if "FINGERPRINT" not in normalized:
        reasons.append("handoff does not expose a fingerprint")
    return HandoffValidationResult(ok=not missing and not reasons, missing_sections=missing, reasons=tuple(reasons))
