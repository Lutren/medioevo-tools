from duat_predictive_registry.scoring import (
    bayesian_update,
    calibration_score,
    coverage,
    ensemble_weight,
    freshness,
    h_eff_pred,
    r_pred,
    scalar_kalman_gain,
    weighted_ensemble,
)


def test_predictive_formulas_are_bounded():
    assert 0 < freshness(1) <= 1
    assert coverage(8, 10) == 0.8
    assert calibration_score(0.2) == 0.8
    assert 0 <= r_pred(0.2, 0.1, 0.1, 0.0, 0.2) <= 1
    assert 0 <= h_eff_pred(0.8, 0.9, 0.9, 0.9, 0.8, 0.7) <= 1


def test_weighted_ensemble_and_bayes_kalman():
    weights = [ensemble_weight(0.1, 0.2, 1, 0.9), ensemble_weight(0.2, 0.3, 2, 0.8)]
    fused = weighted_ensemble([0.6, 0.8], weights)
    assert 0.6 <= fused <= 0.8
    assert bayesian_update(0.5, 0.8, 0.6) <= 1
    assert scalar_kalman_gain(P=1.0, H=1.0, R=0.5) > 0
