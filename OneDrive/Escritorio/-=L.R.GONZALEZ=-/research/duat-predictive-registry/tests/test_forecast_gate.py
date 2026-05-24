from duat_predictive_registry.forecast_gate import ForecastGateInput, forecast_gate


def test_forecast_gate_requires_source_card():
    result = forecast_gate(ForecastGateInput(has_source_card=False, has_backtest=True, R_pred=0.1))
    assert result["gate"] == "REVIEW"


def test_forecast_gate_requires_backtest_before_approval():
    result = forecast_gate(ForecastGateInput(has_source_card=True, has_backtest=False, R_pred=0.1))
    assert result["gate"] == "REVIEW"


def test_forecast_gate_blocks_leakage_and_forbidden_claims():
    assert forecast_gate(ForecastGateInput(True, True, data_leakage_detected=True, R_pred=0.1))["gate"] == "BLOCK"
    assert forecast_gate(ForecastGateInput(True, True, forbidden_domain_claim=True, R_pred=0.1))["gate"] == "BLOCK"


def test_forecast_gate_blocks_worse_than_baseline_and_high_r():
    assert forecast_gate(ForecastGateInput(True, True, brier_score=0.4, baseline_brier=0.3, R_pred=0.1))["gate"] == "BLOCK_PRODUCTION"
    assert forecast_gate(ForecastGateInput(True, True, R_pred=0.7))["gate"] == "BLOCK"
    assert forecast_gate(ForecastGateInput(True, True, R_pred=0.2))["gate"] == "APPROVE"
