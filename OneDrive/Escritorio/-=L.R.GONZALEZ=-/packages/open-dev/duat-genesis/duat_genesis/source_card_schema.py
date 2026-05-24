from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class SourceCard:
    id: str
    title: str
    source_type: str
    boundary: str
    claims: tuple[str, ...]
    evidence: tuple[str, ...]
    risks: tuple[str, ...] = field(default_factory=tuple)
    next_action: str = ""


def validate_source_card(card: SourceCard) -> list[str]:
    errors: list[str] = []
    if not card.id:
        errors.append("missing id")
    if not card.title:
        errors.append("missing title")
    if card.boundary not in {"public", "private", "protected", "unknown_review"}:
        errors.append("invalid boundary")
    if not card.claims:
        errors.append("missing claims")
    if not card.evidence:
        errors.append("missing evidence")
    if not card.next_action:
        errors.append("missing next_action")
    return errors
