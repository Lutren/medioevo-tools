"""Canonical 07b/07d math adapter for local operational flows.

This module exposes bounded operators for scoring and gates. The functions are
operational proxies only; they do not validate physics, consciousness,
biology, history, prediction, or universal compression claims.
"""

from __future__ import annotations

import json
import math
import re
from collections.abc import Iterable, Mapping
from typing import Any

from .eml import eml as _eml


MATH_CANON_VERSION = "07b/07d-2026-05-20"
SCIENCE_CLAIM_GATE = "BLOCK_STRONG_CLAIMS_UNTIL_F1_F6"


class MathCanonError(ValueError):
    """Raised when a canonical operator receives invalid numeric input."""


def validate_R_bounds(R: float | int) -> float:
    """Return R as float when it is finite and inside [0, 1]."""

    value = float(R)
    if not math.isfinite(value):
        raise MathCanonError("R must be finite")
    if value < 0.0 or value > 1.0:
        raise MathCanonError("R must be in [0, 1]")
    return value


def R_noisy_or(rs: Iterable[float | int]) -> float:
    """Canonical bounded aggregate residue: R_or = 1 - prod_i(1 - r_i)."""

    complement_product = 1.0
    count = 0
    for r in rs:
        value = validate_R_bounds(r)
        complement_product *= 1.0 - value
        count += 1
    if count == 0:
        return 0.0
    return validate_R_bounds(1.0 - complement_product)


def phi_moi(T: float | int, S: float | int, C: float | int, K: float | int, R: float | int) -> float:
    """Canonical Phi_moi geometric mean: (T*S*C*K*(1-R))^(1/5)."""

    factors = [
        validate_R_bounds(T),
        validate_R_bounds(S),
        validate_R_bounds(C),
        validate_R_bounds(K),
        1.0 - validate_R_bounds(R),
    ]
    product = 1.0
    for factor in factors:
        product *= factor
    return validate_R_bounds(product ** (1.0 / 5.0))


def EML(
    s: float | int,
    c: float | int,
    alpha: float | int = 1.0,
    beta: float | int = 1.0,
    theta: float | int = 0.0,
) -> float:
    """Canonical 07b EML wrapper over the bounded sigmoid implementation."""

    return _eml(s, c, alpha=alpha, beta=beta, theta=theta)


def classify_claim_math_status(claim_or_config: Any) -> dict[str, str]:
    """Classify whether a math claim/config stays inside 07b/07d boundaries."""

    text = _text_from_claim(claim_or_config)
    lowered = text.lower()

    if _contains_old_eml(text):
        return {
            "status": "OLD_FORMULA_ACTIVE",
            "reason": "old EML exp(x)-ln(y) form detected",
            "action": "replace with EML(s,c;alpha,beta,theta) sigmoid and mark historical text deprecated",
        }

    if _contains_blocked_science_claim(lowered):
        return {
            "status": "BLOCKED_CLAIM",
            "reason": "strong physical/consciousness/utility claim is not closed by 07b/07d",
            "action": "keep as BLOQUEO COMO HECHO until falsifiers and datasets exist",
        }

    if _contains_unearned_f5_closure(lowered):
        return {
            "status": "ACTIVE_NEEDS_REVIEW",
            "reason": "F5 is described as closed without explicit dataset evidence",
            "action": "downgrade to INCOGNITA until F1-F6 benchmark evidence exists",
        }

    if _contains_canonical_math(text):
        return {
            "status": "CANON_07B",
            "reason": "canonical 07b/07d operators or boundary language detected",
            "action": "allowed as local operational math proxy",
        }

    return {
        "status": "DOC_ONLY",
        "reason": "no active canonical or deprecated math operator detected",
        "action": "no runtime action",
    }


def _text_from_claim(claim_or_config: Any) -> str:
    if isinstance(claim_or_config, str):
        return claim_or_config
    if isinstance(claim_or_config, Mapping):
        return json.dumps(claim_or_config, sort_keys=True, ensure_ascii=False, default=str)
    return str(claim_or_config)


def _contains_old_eml(text: str) -> bool:
    return bool(
        re.search(
            r"eml\s*\(\s*x\s*,\s*y\s*\).*exp\s*\(\s*x\s*\)\s*(?:[-\u2212]|\s{2,})\s*ln\s*\(\s*y\s*\)",
            text,
            flags=re.IGNORECASE,
        )
        or re.search(
            r"exp\s*\(\s*x\s*\)\s*(?:[-\u2212]|\s{2,})\s*ln\s*\(\s*y\s*\)",
            text,
            flags=re.IGNORECASE,
        )
    )


def _contains_blocked_science_claim(lowered: str) -> bool:
    blocked_fragments = [
        "física validada",
        "fisica validada",
        "nueva física validada",
        "nueva fisica validada",
        "consciencia demostrada",
        "conciencia demostrada",
        "agi demostrada",
        "superior a shannon",
        "superior a kolmogorov",
        "compresión universal demostrada",
        "compresion universal demostrada",
        "propiedad demostrada algorítmicamente",
        "propiedad demostrada algoritmicamente",
        "extraer el noúmeno",
        "extraer el noumeno",
        "\u03bc_f extrae",
        "mu_f extrae",
    ]
    return any(fragment in lowered for fragment in blocked_fragments)


def _contains_unearned_f5_closure(lowered: str) -> bool:
    if "f5" not in lowered:
        return False
    closure_terms = ["queda cerrado", "cerrado", "closed", "validado", "validated", "pass", "passed"]
    evidence_terms = ["dataset", "datasets", "fixture", "benchmark", "evidencia", "evidence"]
    return any(term in lowered for term in closure_terms) and not any(term in lowered for term in evidence_terms)


def _contains_canonical_math(text: str) -> bool:
    lowered = text.lower()
    canonical_fragments = [
        "r_or",
        "r_noisy_or",
        "phi_moi",
        "\u03c6_moi",
        "eml(s,c",
        "eml(s, c",
        "u(x; r)",
        "\u03bc_f",
        "mu_f",
        "f1-f6",
        "mathematical_proxy_only",
        "not_physics_proof",
    ]
    return any(fragment in lowered for fragment in canonical_fragments)
