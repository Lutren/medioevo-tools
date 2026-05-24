"""Heuristic residue classifier for local DUAT filtering."""

from __future__ import annotations

import re
from collections import Counter

from .r_vector import empty_r_vector

SENSITIVE_PATTERNS = (
    r"\bapi[_-]?key\b",
    r"\btoken\b\s*[:=]",
    r"\bpassword\b\s*[:=]",
    r"\bsecret\b\s*[:=]",
    r"\bcredencial",
    r"\bssn\b",
    r"\bcurp\b",
    r"\.env\b",
)

FORBIDDEN_DOMAIN_PATTERNS = (
    r"predic(?:e|cion|ción).*(eleccion|elección|voto|votante)",
    r"rankea\s+votantes",
    r"prueba\s+causalidad",
)

STRUCTURED_PATTERNS = (
    r"\bcomo\b",
    r"\bmetafor",
    r"\bintuici",
    r"\basociaci",
    r"\bbacteria",
    r"\bneurona",
    r"\bluz\b",
    r"\bgravedad\b",
    r"\bsonido\b",
    r"\bresiduo\b",
)

CLEAN_PATTERNS = (
    r"\bcrear\b",
    r"\bimplementar\b",
    r"\barchivo\b",
    r"\btest\b",
    r"\bschema\b",
    r"\bobjetivo\b",
    r"\baccion\b",
    r"\bsource\b",
    r"\bgate\b",
)

ENTERTAINMENT_PATTERNS = (
    r"\bmeme\b",
    r"\bviral\b",
    r"\btendencia\b",
    r"\bclickbait\b",
    r"\bengagement\b",
)

SOCIAL_MANIPULATION_PATTERNS = (
    r"\bpropaganda\b",
    r"\bmanipul",
    r"\btribal",
    r"\bframing\b",
    r"\bpresion social\b",
    r"\bpresión social\b",
)


def _hits(patterns: tuple[str, ...], text: str) -> list[str]:
    return [pattern for pattern in patterns if re.search(pattern, text, re.IGNORECASE)]


def _repetition_score(text: str) -> float:
    words = re.findall(r"[A-Za-zÁÉÍÓÚáéíóúÑñ0-9_]+", text.lower())
    if not words:
        return 0.0
    counts = Counter(words)
    repeated = sum(count for word, count in counts.items() if count >= 4 and len(word) > 2)
    return min(1.0, repeated / max(8, len(words)))


def classify_residue(input_text: str) -> dict[str, object]:
    """Classify text into R dimensions and residue buckets.

    This is deliberately conservative and local. It is a routing aid, not a
    truth engine.
    """

    text = input_text or ""
    r_vector = empty_r_vector()
    sensitive = _hits(SENSITIVE_PATTERNS, text)
    forbidden = _hits(FORBIDDEN_DOMAIN_PATTERNS, text)
    structured = _hits(STRUCTURED_PATTERNS, text)
    clean = _hits(CLEAN_PATTERNS, text)
    entertainment = _hits(ENTERTAINMENT_PATTERNS, text)
    social = _hits(SOCIAL_MANIPULATION_PATTERNS, text)
    repetition = _repetition_score(text)
    contradiction = bool(
        re.search(r"\bpublica\b", text, re.IGNORECASE)
        and re.search(r"\bno\s+public", text, re.IGNORECASE)
    )

    r_vector["R_sensitive"] = min(1.0, 0.45 * bool(sensitive) + 0.55 * bool(forbidden))
    r_vector["R_cognitive"] = 0.18 if structured else 0.0
    r_vector["R_entertainment"] = 0.35 if entertainment else 0.0
    r_vector["R_social_manipulative"] = 0.45 if social else 0.0
    r_vector["R_contra"] = 0.55 if contradiction else 0.0
    r_vector["R_agent_operational"] = 0.0 if clean else 0.22
    r_vector["R_user_style"] = 0.20 if structured else 0.05

    true_noise_score = max(repetition, 0.25 if "???" in text or "!!!" in text else 0.0)
    r_vector["R_cognitive"] = min(1.0, r_vector["R_cognitive"] + true_noise_score * 0.5)

    return {
        "clean_signal": bool(clean) and not forbidden,
        "structured_residue": bool(structured),
        "true_noise_score": true_noise_score,
        "sensitive_hits": sensitive + forbidden,
        "contradiction": contradiction,
        "r_vector": r_vector,
        "matched_patterns": {
            "clean": clean,
            "structured": structured,
            "entertainment": entertainment,
            "social_manipulative": social,
        },
    }
