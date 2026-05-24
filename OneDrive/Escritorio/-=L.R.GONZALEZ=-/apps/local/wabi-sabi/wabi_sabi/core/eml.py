# ============================================================
# wabi_sabi/core/eml.py — EML Gate Module
#
# CANON v0.3 (2026-05-23, R08):
#   canonical_eml(signal, complexity; alpha, beta, theta)
#   = σ(alpha·signal − beta·log(1+complexity) − theta)
#   epistemic_status = "CANON_v0_3"
#   Referencia: 07b §5, eml_neural.py (EMLClassic), OSIT BDI v0.3
#
# SUPERSEDED (pre-canon):
#   safe_eml(signal_log, residue_norm)
#   = exp(signal_log) − ln(1 + residue_norm)
#   Conservado para compatibilidad hacia atrás. No usar en código nuevo.
#   Enlace: R08 en ROADMAP_MEJORAS_PRIORIZADO_2026-05-23.md
# ============================================================
from __future__ import annotations

import math
from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class EMLResult:
    value: float | None
    domain_ok: bool
    warnings: list[str] = field(default_factory=list)
    epistemic_status: str = "RESEARCH_ONLY"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


# ---------------------------------------------------------------------------
# CANON v0.3 — forma sigmoidal
# ---------------------------------------------------------------------------

def canonical_eml(
    signal: float,
    complexity: float,
    *,
    alpha: float = 1.0,
    beta: float = 1.0,
    theta: float = 0.5,
) -> EMLResult:
    """EML canónico v0.3: σ(alpha·signal − beta·log(1+complexity) − theta).

    Referencia: OSIT BDI canon v0.3, 07b §5.
    Implementación análoga a EMLClassic en Descubrimientos/eml_neural.py.

    Args:
        signal:     Intensidad de señal epistémica s ∈ ℝ.
        complexity: Complejidad / carga residual c ≥ 0.
        alpha:      Peso de la señal (default 1.0).
        beta:       Peso de la complejidad (default 1.0).
        theta:      Umbral de sesgo (default 0.5).

    Returns:
        EMLResult con value ∈ [0, 1] y epistemic_status="CANON_v0_3".
        Un score cercano a 1 indica alta aceptabilidad (bajo residuo esperado).
    """
    warnings: list[str] = []
    if not math.isfinite(signal):
        warnings.append("signal_not_finite")
    if not math.isfinite(complexity):
        warnings.append("complexity_not_finite")
    elif complexity < 0:
        warnings.append("complexity_must_be_gte_zero")
    for name, val in (("alpha", alpha), ("beta", beta), ("theta", theta)):
        if not math.isfinite(val):
            warnings.append(f"{name}_not_finite")
    if warnings:
        return EMLResult(value=None, domain_ok=False, warnings=warnings,
                         epistemic_status="CANON_v0_3")

    # σ(α·s − β·log(1+c) − θ)
    z = alpha * signal - beta * math.log1p(complexity) - theta
    # Clamp z to avoid overflow in exp (same guard as EMLClassic/EMLNeural).
    z_clamped = max(-500.0, min(500.0, z))
    value = 1.0 / (1.0 + math.exp(-z_clamped))
    return EMLResult(value=value, domain_ok=True, warnings=[],
                     epistemic_status="CANON_v0_3")


# ---------------------------------------------------------------------------
# SUPERSEDED — forma pre-canónica (conservada para compatibilidad)
# ---------------------------------------------------------------------------

def safe_eml(signal_log: float, residue_norm: float) -> EMLResult:
    """[SUPERSEDED] EML pre-canónico: exp(signal_log) − ln(1 + residue_norm).

    ESTA FUNCIÓN ESTÁ SUPERSEDED. Para código nuevo usar canonical_eml().
    Conservada para compatibilidad hacia atrás con callers existentes.

    La forma canónica (CANON_v0_3) es sigmoidal:
      canonical_eml(signal, complexity, alpha=1.0, beta=1.0, theta=0.5)
      = σ(alpha·signal − beta·log(1+complexity) − theta)
    """
    warnings: list[str] = []
    if not math.isfinite(signal_log):
        warnings.append("signal_log_not_finite")
    if not math.isfinite(residue_norm):
        warnings.append("residue_norm_not_finite")
    if residue_norm < 0:
        warnings.append("residue_norm_must_be_gte_zero")
    if warnings:
        return EMLResult(value=None, domain_ok=False, warnings=warnings)
    try:
        value = math.exp(signal_log) - math.log1p(residue_norm)
    except (OverflowError, ValueError) as exc:
        return EMLResult(value=None, domain_ok=False, warnings=[f"domain_error:{exc.__class__.__name__}"])
    if not math.isfinite(value):
        return EMLResult(value=None, domain_ok=False, warnings=["eml_value_not_finite"])
    return EMLResult(value=value, domain_ok=True)


# ---------------------------------------------------------------------------
# Auxiliary helpers (unchanged)
# ---------------------------------------------------------------------------

def window_load_eml(*, r_token: float, circularity: float, unresolved_tasks: float) -> EMLResult:
    warnings = _non_negative_inputs(
        {
            "r_token": r_token,
            "circularity": circularity,
            "unresolved_tasks": unresolved_tasks,
        }
    )
    if warnings:
        return EMLResult(value=None, domain_ok=False, warnings=warnings)
    value = math.log1p(r_token) + math.log1p(circularity) + math.log1p(unresolved_tasks)
    return EMLResult(value=value, domain_ok=math.isfinite(value), warnings=[] if math.isfinite(value) else ["value_not_finite"])


def jamming_margin_eml(*, residue_norm: float, phi_log: float) -> EMLResult:
    warnings = _non_negative_inputs({"residue_norm": residue_norm})
    if not math.isfinite(phi_log):
        warnings.append("phi_log_not_finite")
    if warnings:
        return EMLResult(value=None, domain_ok=False, warnings=warnings)
    try:
        value = math.log1p(residue_norm) - math.exp(phi_log)
    except OverflowError:
        return EMLResult(value=None, domain_ok=False, warnings=["phi_exp_overflow"])
    return EMLResult(value=value, domain_ok=math.isfinite(value), warnings=[] if math.isfinite(value) else ["value_not_finite"])


def _non_negative_inputs(values: dict[str, float]) -> list[str]:
    warnings: list[str] = []
    for name, value in values.items():
        if not math.isfinite(value):
            warnings.append(f"{name}_not_finite")
        elif value < 0:
            warnings.append(f"{name}_must_be_gte_zero")
    return warnings
