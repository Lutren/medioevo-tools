from __future__ import annotations

from duat_predictive_registry.predictive_claim_gate import predictive_claim_gate


def test_predictive_claim_gate_approves_only_local_when_metrics_and_gates_pass():
    result = predictive_claim_gate(
        metric_status="IMPROVED",
        r_delta_aligned=-0.01,
        comparability_status="PASS",
        license_terms_scan="PASS",
        leakage_check="PASS",
        data_mode="real_fixture",
    )
    assert result["predictive_claim_gate"] == "APPROVE_LOCAL"
    assert result["publication_gate"] == "BLOCK"
    assert result["claim_allowed_public"] is False


def test_predictive_claim_gate_blocks_leakage():
    result = predictive_claim_gate(
        metric_status="IMPROVED",
        r_delta_aligned=-0.01,
        comparability_status="PASS",
        license_terms_scan="PASS",
        leakage_check="BLOCK",
        data_mode="real_fixture",
    )
    assert result["predictive_claim_gate"] == "BLOCK"


def test_predictive_claim_gate_blocks_synthetic_for_predictive_claims():
    result = predictive_claim_gate(
        metric_status="IMPROVED",
        r_delta_aligned=-0.01,
        comparability_status="PASS",
        license_terms_scan="PASS",
        leakage_check="PASS",
        data_mode="synthetic_fixture",
    )
    assert result["predictive_claim_gate"] == "BLOCK"
    assert result["claim_allowed_internal"] is False


def test_predictive_claim_gate_reviews_metric_or_license_caveats():
    result = predictive_claim_gate(
        metric_status="MIXED",
        r_delta_aligned=-0.01,
        comparability_status="PASS",
        license_terms_scan="REVIEW",
        leakage_check="PASS",
        data_mode="real_fixture",
    )
    assert result["predictive_claim_gate"] == "REVIEW"
    assert result["publication_gate"] == "BLOCK"
