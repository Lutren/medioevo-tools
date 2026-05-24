"""Canonical 07b EML operator for local Observacionismo research.

EML is kept as a mathematical operator/proxy only:

    EML(s, c; alpha, beta, theta)
    = sigma(alpha*s - beta*log(1+c) - theta), c >= 0

It is not evidence for physics, consciousness, history, social prediction or
any other strong claim.
"""

from __future__ import annotations

import math


EXPERIMENTAL_OPERATOR_STATUS = "EXPERIMENTAL_OPERATOR_NOT_PROOF"


class EMLDomainError(ValueError):
    """Raised when EML receives non-finite inputs or invalid parameters."""


def _finite_number(value: float | int, name: str) -> float:
    number = float(value)
    if not math.isfinite(number):
        raise EMLDomainError(f"{name} must be finite")
    return number


def eml(
    s: float | int,
    c: float | int,
    *,
    alpha: float | int = 1.0,
    beta: float | int = 1.0,
    theta: float | int = 0.0,
) -> float:
    """Return bounded canonical EML sigmoid from 07b."""

    signal = _finite_number(s, "s")
    cost = _finite_number(c, "c")
    alpha_value = _finite_number(alpha, "alpha")
    beta_value = _finite_number(beta, "beta")
    theta_value = _finite_number(theta, "theta")
    if cost < 0.0:
        raise EMLDomainError("c must be >= 0")
    if alpha_value < 0.0 or beta_value < 0.0 or theta_value < 0.0:
        raise EMLDomainError("alpha, beta and theta must be >= 0")

    z = alpha_value * signal - beta_value * math.log1p(cost) - theta_value
    return _sigmoid(z)


def residue_eml(input_log: float | int, r_norm: float | int) -> float:
    """Operational residue proxy using canonical EML(input_log, max(0, r_norm))."""

    residue = max(0.0, _finite_number(r_norm, "r_norm"))
    return eml(input_log, residue)


def gap_eml(signal_log: float | int, registry_norm: float | int) -> float:
    """Absolute distance from the EML threshold 0.5."""

    registry = max(0.0, _finite_number(registry_norm, "registry_norm"))
    return abs(eml(signal_log, registry) - 0.5)


def operator_contract() -> dict[str, object]:
    """Machine-readable claim boundary for EML integrations."""

    return {
        "schema": "obs_info_kernel.eml_operator_contract.v1",
        "status": EXPERIMENTAL_OPERATOR_STATUS,
        "formula": "EML(s, c; alpha, beta, theta) = sigma(alpha*s - beta*log(1+c) - theta)",
        "sigmoid": "sigma(z) = 1 / (1 + exp(-z))",
        "domain": {
            "s": "finite real",
            "c": "finite real >= 0",
            "alpha": "finite real >= 0",
            "beta": "finite real >= 0",
            "theta": "finite real >= 0",
        },
        "range": "(0, 1)",
        "threshold": {"expand": "> 0.5", "compress": "< 0.5", "boundary": "= 0.5"},
        "public_claim_allowed": False,
        "claim_boundary": [
            "mathematical_proxy_only",
            "not_physics_proof",
            "not_consciousness_proof",
            "not_history_or_social_prediction",
        ],
        "falsifiers": [
            "x is not finite",
            "c is not finite",
            "c < 0",
            "alpha, beta or theta is negative",
            "monotonicity with s or c is broken",
            "operator is promoted as proof outside its mathematical domain",
        ],
    }


def _sigmoid(z: float) -> float:
    if z >= 0.0:
        return 1.0 / (1.0 + math.exp(-z))
    exp_z = math.exp(z)
    return exp_z / (1.0 + exp_z)
