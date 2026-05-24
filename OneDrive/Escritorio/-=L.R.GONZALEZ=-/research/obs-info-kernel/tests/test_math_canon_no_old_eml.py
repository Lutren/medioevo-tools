import math

import pytest

from obs_info_kernel.math_canon import EML, MathCanonError, R_noisy_or, classify_claim_math_status, phi_moi, validate_R_bounds


def test_r_noisy_or_is_bounded_and_rejects_unbounded_r():
    assert R_noisy_or([0.9, 0.9]) == pytest.approx(0.99)
    assert 0.0 <= R_noisy_or([1.0, 1.0]) <= 1.0

    with pytest.raises(MathCanonError):
        validate_R_bounds(1.01)


def test_eml_wrapper_stays_inside_open_unit_interval():
    value = EML(0.5, 1.25, alpha=1.0, beta=1.0, theta=0.0)

    assert math.isfinite(value)
    assert 0.0 < value < 1.0


def test_old_exp_minus_log_eml_is_not_allowed_as_active_math():
    status = classify_claim_math_status("EML(x,y) = exp(x)-ln(y)")

    assert status["status"] == "OLD_FORMULA_ACTIVE"
    assert "replace" in status["action"]


def test_phi_moi_uses_fifth_root_not_raw_product():
    canonical = phi_moi(0.8, 0.8, 0.8, 0.8, 0.2)
    raw_product = 0.8 * 0.8 * 0.8 * 0.8 * (1.0 - 0.2)

    assert canonical == pytest.approx(raw_product ** (1.0 / 5.0))
    assert canonical != pytest.approx(raw_product)
