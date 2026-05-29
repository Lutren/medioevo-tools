"""WS2: DUAT predictive registry consumes the canonical obsai-core OSIT ladder."""

from duat_predictive_registry.dual_lane_filter import (
    compose_final_output,
    dual_lane_canonical_state,
    split_dual_lane,
)
from duat_predictive_registry.forecast_gate import (
    ForecastGateInput,
    forecast_gate,
    obsai_forecast_precheck,
)


def test_forecast_gate_annotates_canonical_regime_and_state_without_changing_decision():
    high = forecast_gate(ForecastGateInput(True, True, R_pred=0.7))
    assert high["gate"] == "BLOCK"  # existing decision is unchanged
    assert high["regime"] == "JAMMING"
    assert high["epistemic_state"] == "BLOQUEADO"

    low = forecast_gate(ForecastGateInput(True, True, R_pred=0.1))
    assert low["gate"] == "APPROVE"
    assert low["regime"] == "OPTIMO"
    assert low["epistemic_state"] == "CERTEZA"


def test_obsai_forecast_precheck_blocks_incognita_and_bloqueado():
    assert obsai_forecast_precheck(0.50)["gate"] == "BLOCK"  # INCOGNITA band
    assert obsai_forecast_precheck(0.50)["epistemic_state"] == "INCOGNITA"
    assert obsai_forecast_precheck(0.70)["gate"] == "BLOCK"  # BLOQUEADO band
    assert obsai_forecast_precheck(0.10)["gate"] == "APPROVE"  # CERTEZA band
    assert obsai_forecast_precheck(0.40)["gate"] == "REVIEW"  # INFERENCIA above review band


def test_dual_lane_canonical_state_is_well_formed():
    packet = split_dual_lane("status local listing of safe metadata")
    compose_final_output(packet)
    canon = dual_lane_canonical_state(packet)
    assert canon["epistemic_state"] in {"CERTEZA", "INFERENCIA", "INCOGNITA", "BLOQUEADO"}
    assert canon["gate"] in {"APPROVE", "REVIEW", "BLOCK"}
    assert canon["calibration"] == "DEMO_ONLY"
