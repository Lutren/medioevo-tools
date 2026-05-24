import math

import pytest

from obs_info_kernel.eml import (
    EMLDomainError,
    EXPERIMENTAL_OPERATOR_STATUS,
    eml,
    gap_eml,
    operator_contract,
    residue_eml,
)


def test_eml_returns_finite_for_normal_inputs():
    value = eml(0.25, 1.5)

    assert math.isfinite(value)
    assert 0.0 < value < 1.0
    assert value == pytest.approx(1.0 / (1.0 + math.exp(-(0.25 - math.log1p(1.5)))))


def test_eml_rejects_negative_cost_or_parameters():
    with pytest.raises(EMLDomainError):
        eml(0.0, -1.0)

    with pytest.raises(EMLDomainError):
        eml(0.0, 0.0, alpha=-1.0)

def test_eml_threshold_is_half_when_signal_matches_cost_and_theta():
    cost = 1.75
    theta = 0.25
    signal = math.log1p(cost) + theta

    assert eml(signal, cost, theta=theta) == pytest.approx(0.5)


def test_eml_monotonicity_x_up_y_down():
    assert eml(0.4, 1.25) > eml(0.2, 1.25)
    assert eml(0.4, 1.25) > eml(0.4, 1.75)


def test_residue_and_gap_proxies_keep_domain_guarded():
    assert residue_eml(0.5, -10) == pytest.approx(eml(0.5, 0.0))
    assert gap_eml(0.5, 0.25) == pytest.approx(abs(eml(0.5, 0.25) - 0.5))


def test_adversarial_inputs_do_not_promote_claims():
    contract = operator_contract()

    assert EXPERIMENTAL_OPERATOR_STATUS == "EXPERIMENTAL_OPERATOR_NOT_PROOF"
    assert contract["public_claim_allowed"] is False
    assert contract["range"] == "(0, 1)"
    assert "not_physics_proof" in contract["claim_boundary"]
    with pytest.raises(EMLDomainError):
        eml(float("nan"), 1.0)
    assert eml(1000.0, 1.0) == pytest.approx(1.0)
