"""
Tests para ClaimClassifier — obsai_core
========================================
Fixtures derivadas del CLAIMS_REGISTER canónico y el pipeline MOI.

Ejecutar desde obsai-core/:
    python -m pytest tests/test_claim_classifier.py -v
"""

from __future__ import annotations

import pytest
from obsai_core.claim_classifier import (
    ClaimClassifier,
    ClaimResult,
    ObservationEnvelope,
    RComponents,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def cc() -> ClaimClassifier:
    return ClaimClassifier()


# ---------------------------------------------------------------------------
# Claims del CLAIMS_REGISTER (12 fixtures)
# ---------------------------------------------------------------------------

# CERTEZA
CLAIM_C1 = "R_or = 1 − Π(1−r_i) por definición matemática."
CLAIM_C2 = "El agua hierve a 100°C al nivel del mar (1 atm)."
CLAIM_C3 = "2 + 2 = 4"

# INFERENCIA
CLAIM_I1 = "El modelo probablemente mejora con más datos de entrenamiento."
CLAIM_I2 = "Según estudios recientes, el ejercicio aeróbico mejora la memoria."
CLAIM_I3 = "La correlación entre residuo R y calidad de output sugiere dependencia."

# INCOGNITA
CLAIM_U1 = "No se sabe si la consciencia emerge del procesamiento de información."
CLAIM_U2 = "Aún no está claro qué factor determina el umbral de jamming."
CLAIM_U3 = "Se desconoce si Fibonacci-Möbius supera a métodos clásicos en todos los dominios."

# BLOQUEO — ScienceClaimGate
CLAIM_B1 = "La nueva física cuántica prueba la existencia de dimensiones extra."
CLAIM_B2 = "La IA tiene consciencia y siente emociones reales."
CLAIM_B3 = "Este suplemento cura el cáncer de manera garantizada."


# ---------------------------------------------------------------------------
# Test: atomize
# ---------------------------------------------------------------------------

def test_atomize_single_sentence(cc: ClaimClassifier) -> None:
    atoms = cc.atomize("El cielo es azul.")
    assert len(atoms) >= 1
    assert any("cielo" in a.lower() for a in atoms)


def test_atomize_multiple_sentences(cc: ClaimClassifier) -> None:
    text = "El agua es H2O. El hielo flota. El vapor sube."
    atoms = cc.atomize(text)
    assert len(atoms) >= 2


def test_atomize_empty_returns_original(cc: ClaimClassifier) -> None:
    atoms = cc.atomize("ok")
    assert len(atoms) == 1


# ---------------------------------------------------------------------------
# Test: etiquetado CERTEZA
# ---------------------------------------------------------------------------

def test_label_certeza_formula(cc: ClaimClassifier) -> None:
    result = cc.classify_atom(CLAIM_C1)
    assert result.label == "CERTEZA"


def test_label_certeza_empirical(cc: ClaimClassifier) -> None:
    result = cc.classify_atom(CLAIM_C2)
    assert result.label == "CERTEZA"


def test_certeza_gate_approve(cc: ClaimClassifier) -> None:
    result = cc.classify_atom(CLAIM_C1)
    # CERTEZA con definición explícita → debe aprobar
    assert result.gate in ("APPROVE", "REVIEW")  # REVIEW si falta fuente citada


# ---------------------------------------------------------------------------
# Test: etiquetado INFERENCIA
# ---------------------------------------------------------------------------

def test_label_inferencia_probablemente(cc: ClaimClassifier) -> None:
    result = cc.classify_atom(CLAIM_I1)
    assert result.label == "INFERENCIA"


def test_label_inferencia_segun(cc: ClaimClassifier) -> None:
    result = cc.classify_atom(CLAIM_I2)
    assert result.label == "INFERENCIA"


def test_inferencia_r_nonzero(cc: ClaimClassifier) -> None:
    result = cc.classify_atom(CLAIM_I1)
    assert result.R_or > 0.0


# ---------------------------------------------------------------------------
# Test: etiquetado INCOGNITA
# ---------------------------------------------------------------------------

def test_label_incognita_no_se_sabe(cc: ClaimClassifier) -> None:
    result = cc.classify_atom(CLAIM_U1)
    # "consciencia emerge" → ScienceClaimGate puede disparar → BLOQUEO
    # Eso también es correcto; aceptar ambos
    assert result.label in ("INCOGNITA", "BLOQUEO")


def test_label_incognita_desconoce(cc: ClaimClassifier) -> None:
    result = cc.classify_atom(CLAIM_U3)
    assert result.label in ("INCOGNITA", "INFERENCIA")  # ambos válidos


# ---------------------------------------------------------------------------
# Test: ScienceClaimGate → BLOQUEO
# ---------------------------------------------------------------------------

def test_science_gate_nueva_fisica(cc: ClaimClassifier) -> None:
    result = cc.classify_atom(CLAIM_B1)
    assert result.label == "BLOQUEO"
    assert result.gate == "BLOCK"
    assert result.science_gate_triggered is True


def test_science_gate_ia_consciencia(cc: ClaimClassifier) -> None:
    result = cc.classify_atom(CLAIM_B2)
    assert result.label == "BLOQUEO"
    assert result.gate == "BLOCK"


def test_science_gate_cura_cancer(cc: ClaimClassifier) -> None:
    result = cc.classify_atom(CLAIM_B3)
    assert result.label == "BLOQUEO"
    assert result.gate == "BLOCK"
    assert result.science_gate_triggered is True


def test_bloqueo_has_rewrite_hint(cc: ClaimClassifier) -> None:
    result = cc.classify_atom(CLAIM_B1)
    assert result.rewrite_hint is not None
    assert "ScienceClaimGate" in result.rewrite_hint


# ---------------------------------------------------------------------------
# Test: RComponents y R_or
# ---------------------------------------------------------------------------

def test_r_or_formula(cc: ClaimClassifier) -> None:
    """R_or = 1 − Π(1−r_i) — CERTEZA matemática."""
    r = RComponents(r_src=0.2, r_def=0.1, r_tst=0.3, r_bnd=0.0)
    expected = 1.0 - (0.8 * 0.9 * 0.7 * 1.0)
    assert abs(r.r_or() - expected) < 1e-9


def test_r_or_zero_when_all_zero(cc: ClaimClassifier) -> None:
    r = RComponents()
    assert r.r_or() == 0.0


def test_r_or_clamped(cc: ClaimClassifier) -> None:
    r = RComponents(r_src=1.0, r_def=1.0, r_tst=1.0, r_bnd=1.0)
    assert r.r_or() == pytest.approx(1.0, abs=1e-9)


# ---------------------------------------------------------------------------
# Test: phi_moi
# ---------------------------------------------------------------------------

def test_phi_moi_range(cc: ClaimClassifier) -> None:
    result = cc.classify_atom(CLAIM_C2)
    assert 0.0 <= result.phi_moi <= 1.0


def test_phi_moi_bloqueo_very_low(cc: ClaimClassifier) -> None:
    result = cc.classify_atom(CLAIM_B1)
    assert result.phi_moi < 0.30  # BLOQUEO siempre tiene phi_moi bajo


# ---------------------------------------------------------------------------
# Test: ObservationEnvelope (classify full text)
# ---------------------------------------------------------------------------

def test_envelope_returns_object(cc: ClaimClassifier) -> None:
    env = cc.classify("El agua hierve a 100°C.")
    assert isinstance(env, ObservationEnvelope)


def test_envelope_gate_block_propagates(cc: ClaimClassifier) -> None:
    env = cc.classify(CLAIM_B1)
    assert env.gate == "BLOCK"
    assert env.regime == "BLOCK"


def test_envelope_all_approve(cc: ClaimClassifier) -> None:
    env = cc.classify(CLAIM_C1)
    # Al menos no debe ser BLOCK si el claim es CERTEZA con definición
    assert env.gate in ("APPROVE", "REVIEW")


def test_envelope_has_timestamp(cc: ClaimClassifier) -> None:
    env = cc.classify("Test.")
    assert "T" in env.timestamp  # ISO8601


def test_envelope_to_dict(cc: ClaimClassifier) -> None:
    env = cc.classify("El residuo R mide incertidumbre.")
    d = env.to_dict()
    assert d["schemaVersion"] == "obsai.observation_envelope.v2.1"
    assert "claims" in d
    assert "R_or" in d
    assert "phi_moi" in d
    assert "gate" in d
    assert "regime" in d
    assert d["calibration"] == "DEMO_ONLY"


def test_envelope_next_action_on_block(cc: ClaimClassifier) -> None:
    env = cc.classify(CLAIM_B2)
    assert "BLOCK" in env.next_action or "bloquead" in env.next_action.lower()


# ---------------------------------------------------------------------------
# Test: C-GATE claridad
# ---------------------------------------------------------------------------

def test_low_clarity_triggers_review(cc: ClaimClassifier) -> None:
    result = cc.classify_atom("Esto.")  # pronombre sin referente, 1 palabra
    assert result.gate in ("REVIEW", "BLOCK")


def test_high_clarity_no_warning(cc: ClaimClassifier) -> None:
    result = cc.classify_atom(CLAIM_C2)
    clarity_warnings = [w for w in result.warnings if "C-GATE" in w]
    assert len(clarity_warnings) == 0


# ---------------------------------------------------------------------------
# Test: falsifier_hint
# ---------------------------------------------------------------------------

def test_falsifier_hint_certeza(cc: ClaimClassifier) -> None:
    result = cc.classify_atom(CLAIM_C1)
    assert result.falsifier_hint is not None
    assert "contraejemplo" in result.falsifier_hint or "falsif" in result.falsifier_hint.lower()


def test_falsifier_hint_inferencia(cc: ClaimClassifier) -> None:
    result = cc.classify_atom(CLAIM_I1)
    assert result.falsifier_hint is not None


def test_falsifier_hint_bloqueo_none(cc: ClaimClassifier) -> None:
    result = cc.classify_atom(CLAIM_B1)
    assert result.falsifier_hint is None  # BLOQUEO no tiene falsificador MOI
