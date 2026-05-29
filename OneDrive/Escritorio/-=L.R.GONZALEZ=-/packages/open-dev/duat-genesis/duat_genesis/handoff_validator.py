from __future__ import annotations

from dataclasses import dataclass
from typing import Any

try:  # Canonical stable fingerprint from obsai-core (single source of truth).
    from obsai_core import stable_fingerprint as _obsai_stable_fingerprint
except Exception:  # pragma: no cover - hashlib fallback if obsai-core is absent.
    _obsai_stable_fingerprint = None


HANDOFF_FINGERPRINT_SCHEMA = "duat.genesis.handoff.v1"

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


def fingerprint_handoff(text: str) -> str:
    """Stable SHA-256 fingerprint of a handoff (obsai-core canonical, hashlib fallback)."""
    payload = {"schema": HANDOFF_FINGERPRINT_SCHEMA, "handoff": str(text or "")}
    if _obsai_stable_fingerprint is not None:
        return _obsai_stable_fingerprint(payload)
    import hashlib
    import json

    canonical = json.dumps(payload, sort_keys=True, ensure_ascii=True)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def validate_and_fingerprint(text: str) -> dict[str, Any]:
    """Validate a handoff and stamp it with a canonical fingerprint over the validated text."""
    result = validate_handoff_text(text)
    return {
        "schema": HANDOFF_FINGERPRINT_SCHEMA,
        "ok": result.ok,
        "missing_sections": list(result.missing_sections),
        "reasons": list(result.reasons),
        "fingerprint": fingerprint_handoff(text),
    }
