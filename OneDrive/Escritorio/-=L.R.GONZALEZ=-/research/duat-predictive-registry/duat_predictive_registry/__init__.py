"""DUAT predictive registry v0.1.

Local-only research utilities for multidimensional residue filtering,
predictive source scoring and forecast gates. This package does not publish,
deploy or claim guaranteed prediction.
"""

from .dual_lane_filter import (
    DualLanePacket,
    ResidueClass,
    compose_agent_ready_output,
    compose_final_output,
    compose_user_adapted_output,
    compute_noise_R,
    compute_structured_residue_score,
    dual_lane_action_gate,
    split_dual_lane,
)
from .forecast_gate import ForecastGateInput, forecast_gate
from .benchmarking import run_benchmark
from .benchmark_matrix import classify_replication, run_benchmark_matrix, validate_matrix_shape
from .domain_calibration import calibrate_benchmark_row, calibrate_matrix, validate_domain_calibration_report
from .domain_weight_calibration import calibrate_domain_weights
from .metric_aligned_r import (
    build_metric_aligned_report,
    compute_metric_aligned_r,
    validate_metric_aligned_report,
)
from .nested_backtest import run_nested_domain_backtest, validate_nested_backtest_report
from .domain_profiles import infer_domain
from .predictive_claim_gate import predictive_claim_gate
from .r_vector import R_DIMENSIONS, compute_r_total
from .source_quality import SourceQualityInputs, compute_r_source, compute_source_quality

__all__ = [
    "DualLanePacket",
    "ForecastGateInput",
    "R_DIMENSIONS",
    "ResidueClass",
    "SourceQualityInputs",
    "compose_agent_ready_output",
    "compose_final_output",
    "compose_user_adapted_output",
    "compute_noise_R",
    "compute_r_source",
    "compute_r_total",
    "compute_source_quality",
    "compute_structured_residue_score",
    "dual_lane_action_gate",
    "forecast_gate",
    "calibrate_benchmark_row",
    "calibrate_matrix",
    "calibrate_domain_weights",
    "classify_replication",
    "build_metric_aligned_report",
    "compute_metric_aligned_r",
    "infer_domain",
    "predictive_claim_gate",
    "run_benchmark",
    "run_benchmark_matrix",
    "run_nested_domain_backtest",
    "validate_domain_calibration_report",
    "validate_metric_aligned_report",
    "validate_matrix_shape",
    "validate_nested_backtest_report",
    "split_dual_lane",
]
