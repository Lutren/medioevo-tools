"""Tests for wabi_sabi.core.eml — both canonical (v0.3) and superseded forms."""

import math

from wabi_sabi.core.eml import (
    canonical_eml,
    jamming_margin_eml,
    safe_eml,
    window_load_eml,
)


# ---------------------------------------------------------------------------
# SUPERSEDED: safe_eml — regresión, no cambiar.
# ---------------------------------------------------------------------------

def test_safe_eml_uses_shifted_residue_domain():
    result = safe_eml(signal_log=0.0, residue_norm=0.0)

    assert result.domain_ok is True
    assert result.epistemic_status == "RESEARCH_ONLY"
    assert result.value == 1.0  # exp(0) - log1p(0) = 1 - 0 = 1


def test_safe_eml_rejects_negative_residue():
    result = safe_eml(signal_log=0.0, residue_norm=-0.1)

    assert result.domain_ok is False
    assert result.value is None
    assert "residue_norm_must_be_gte_zero" in result.warnings


def test_window_load_eml_is_finite_for_non_negative_inputs():
    result = window_load_eml(r_token=1.0, circularity=2.0, unresolved_tasks=3.0)

    assert result.domain_ok is True
    assert result.value == math.log1p(1.0) + math.log1p(2.0) + math.log1p(3.0)


def test_jamming_margin_eml_reports_auxiliary_margin():
    result = jamming_margin_eml(residue_norm=1.0, phi_log=0.0)

    assert result.domain_ok is True
    assert result.value == math.log1p(1.0) - 1.0


# ---------------------------------------------------------------------------
# CANON v0.3: canonical_eml — forma sigmoidal σ(α·s − β·log(1+c) − θ)
# ---------------------------------------------------------------------------

def _sigma(z: float) -> float:
    """Reference sigmoid."""
    return 1.0 / (1.0 + math.exp(-max(-500.0, min(500.0, z))))


def test_canonical_eml_zero_inputs_matches_sigmoid():
    """σ(0·1 − 0·log(1+0) − 0.5) = σ(-0.5)."""
    result = canonical_eml(0.0, 0.0)
    expected = _sigma(1.0 * 0.0 - 1.0 * math.log1p(0.0) - 0.5)
    assert result.domain_ok is True
    assert result.value == pytest_approx(expected)


def test_canonical_eml_output_in_unit_interval():
    """Output must always be in [0, 1]."""
    for signal, complexity in [(-10.0, 0.0), (0.0, 100.0), (5.0, 0.5), (0.0, 0.0)]:
        result = canonical_eml(signal, complexity)
        assert result.domain_ok is True
        assert 0.0 <= result.value <= 1.0


def test_canonical_eml_high_signal_yields_high_score():
    """High signal → score closer to 1."""
    result = canonical_eml(10.0, 0.0)
    assert result.value > 0.9


def test_canonical_eml_high_complexity_yields_low_score():
    """High complexity → score closer to 0."""
    result = canonical_eml(0.0, 1000.0)
    assert result.value < 0.1


def test_canonical_eml_epistemic_status_is_canon():
    result = canonical_eml(1.0, 1.0)
    assert result.epistemic_status == "CANON_v0_3"


def test_canonical_eml_rejects_negative_complexity():
    result = canonical_eml(0.0, -1.0)
    assert result.domain_ok is False
    assert result.value is None
    assert "complexity_must_be_gte_zero" in result.warnings
    assert result.epistemic_status == "CANON_v0_3"


def test_canonical_eml_rejects_nan_signal():
    result = canonical_eml(float("nan"), 0.0)
    assert result.domain_ok is False
    assert "signal_not_finite" in result.warnings


def test_canonical_eml_rejects_inf_complexity():
    result = canonical_eml(0.0, float("inf"))
    assert result.domain_ok is False
    assert "complexity_not_finite" in result.warnings


def test_canonical_eml_custom_params():
    """Custom alpha/beta/theta match manual calculation."""
    alpha, beta, theta = 2.0, 0.5, 0.0
    s, c = 1.0, 2.0
    expected = _sigma(alpha * s - beta * math.log1p(c) - theta)
    result = canonical_eml(s, c, alpha=alpha, beta=beta, theta=theta)
    assert result.domain_ok is True
    assert abs(result.value - expected) < 1e-12


def test_canonical_eml_monotone_in_signal():
    """Higher signal → higher score (complexity fixed)."""
    r1 = canonical_eml(0.0, 1.0)
    r2 = canonical_eml(1.0, 1.0)
    r3 = canonical_eml(2.0, 1.0)
    assert r1.value < r2.value < r3.value


def test_canonical_eml_monotone_in_complexity():
    """Higher complexity → lower score (signal fixed)."""
    r1 = canonical_eml(1.0, 0.0)
    r2 = canonical_eml(1.0, 5.0)
    r3 = canonical_eml(1.0, 50.0)
    assert r1.value > r2.value > r3.value


def test_canonical_eml_matches_emlclassic_defaults():
    """Should match EMLClassic(alpha=1,beta=1,theta=0.5).score(S,C) from eml_neural.py."""
    # EMLClassic uses theta=0.5 as default, same as our canonical_eml default.
    s, c = 0.7, 1.3
    expected = _sigma(1.0 * s - 1.0 * math.log1p(c) - 0.5)
    result = canonical_eml(s, c)
    assert abs(result.value - expected) < 1e-12


def test_canonical_eml_to_dict_has_epistemic_status():
    result = canonical_eml(1.0, 0.5)
    d = result.to_dict()
    assert d["epistemic_status"] == "CANON_v0_3"
    assert "value" in d
    assert "domain_ok" in d


# ---------------------------------------------------------------------------
# Compatibility: safe_eml and canonical_eml coexist without conflict.
# ---------------------------------------------------------------------------

def test_both_functions_importable():
    """Ensure backward compat: both functions importable from the same module."""
    assert callable(safe_eml)
    assert callable(canonical_eml)


def test_safe_eml_still_returns_research_only():
    """Confirm safe_eml epistemic_status unchanged after R08."""
    result = safe_eml(signal_log=1.0, residue_norm=0.5)
    assert result.epistemic_status == "RESEARCH_ONLY"


# Alias for pytest.approx used inline above
import pytest

def pytest_approx(val, rel=1e-9):  # noqa: N802
    return pytest.approx(val, rel=rel)
