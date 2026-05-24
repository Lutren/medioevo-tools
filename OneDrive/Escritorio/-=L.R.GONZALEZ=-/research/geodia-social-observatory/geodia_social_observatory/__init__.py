"""GEODIA Social Observatory local research MVP."""

from .behavior import analyze_behavior_signature
from .contracts import (
    ARTIFACT_RECORD_SCHEMA,
    BEHAVIOR_SIGNATURE_SCHEMA,
    DUAT_CONWAY_SIMULATION_SCHEMA,
    DUAT_HEALTH_WINDOW_SCHEMA,
    DUAT_REMOTE_COMPUTE_PLAN_SCHEMA,
    DUAT_REMOTE_RUN_SPEC_SCHEMA,
    DUAT_SIGNAL_SOURCE_PACK_SCHEMA,
    DUAT_SMALLVILLE_FALSIFIER_SCHEMA,
    DUAT_SMALLVILLE_FALSIFIER_V0_2_SCHEMA,
    DUAT_SMALLVILLE_INTERVENTION_SCHEMA,
    DUAT_SMALLVILLE_LEDGER_SCHEMA,
    DUAT_SMALLVILLE_METRICS_SCHEMA,
    DUAT_SMALLVILLE_REPLAY_SCHEMA,
    DUAT_SMALLVILLE_SCENARIO_SCHEMA,
    DUAT_V2_INTAKE_SCHEMA,
    EPOCH_MODEL_SCHEMA,
    LOCAL_SOURCE_INTAKE_SCHEMA,
    OBSERVATION_EVENT_SCHEMA,
    ROUTE_DECISION_SCHEMA,
    SCENARIO_REPORT_SCHEMA,
    SOURCE_SNAPSHOT_SCHEMA,
)
from .duat_sim import run_duat_conway_simulation
from .duat_v2_intake import build_duat_v2_intake
from .harmonization import (
    build_harmonized_record,
    build_harmonization_report,
    classify_comparability,
    load_crosswalk,
    normalize_polarity,
    validate_publication_gate,
)
from .intervention_engine import build_baseline_intervention_pair, run_smallville_v0_2
from .metrics_v0_2 import build_metrics_v0_2, falsify_v0_2
from .model import build_epoch_model, build_scenario_report, run_backtest
from .remote_compute import build_colab_kaggle_notebook, build_remote_compute_plan
from .replay_verifier import verify_replay
from .router import RequestFeatures, decide_route
from .signal_source_pack import build_signal_source_pack
from .smallville_lab import (
    build_smallville_scenario,
    falsify_smallville_run,
    run_smallville_duat_lab,
    verify_hash_chain,
)
from .smallville_v02_release import build_release_artifacts
from .snapshot import create_snapshot_from_fixture
from .source_registry import build_local_source_intake

__all__ = [
    "ARTIFACT_RECORD_SCHEMA",
    "BEHAVIOR_SIGNATURE_SCHEMA",
    "DUAT_CONWAY_SIMULATION_SCHEMA",
    "DUAT_HEALTH_WINDOW_SCHEMA",
    "DUAT_REMOTE_COMPUTE_PLAN_SCHEMA",
    "DUAT_REMOTE_RUN_SPEC_SCHEMA",
    "DUAT_SIGNAL_SOURCE_PACK_SCHEMA",
    "DUAT_SMALLVILLE_FALSIFIER_SCHEMA",
    "DUAT_SMALLVILLE_FALSIFIER_V0_2_SCHEMA",
    "DUAT_SMALLVILLE_INTERVENTION_SCHEMA",
    "DUAT_SMALLVILLE_LEDGER_SCHEMA",
    "DUAT_SMALLVILLE_METRICS_SCHEMA",
    "DUAT_SMALLVILLE_REPLAY_SCHEMA",
    "DUAT_SMALLVILLE_SCENARIO_SCHEMA",
    "DUAT_V2_INTAKE_SCHEMA",
    "EPOCH_MODEL_SCHEMA",
    "LOCAL_SOURCE_INTAKE_SCHEMA",
    "OBSERVATION_EVENT_SCHEMA",
    "ROUTE_DECISION_SCHEMA",
    "SCENARIO_REPORT_SCHEMA",
    "SOURCE_SNAPSHOT_SCHEMA",
    "RequestFeatures",
    "analyze_behavior_signature",
    "build_baseline_intervention_pair",
    "build_colab_kaggle_notebook",
    "build_duat_v2_intake",
    "build_epoch_model",
    "build_harmonization_report",
    "build_harmonized_record",
    "build_local_source_intake",
    "build_metrics_v0_2",
    "build_release_artifacts",
    "build_remote_compute_plan",
    "build_scenario_report",
    "build_signal_source_pack",
    "build_smallville_scenario",
    "classify_comparability",
    "create_snapshot_from_fixture",
    "decide_route",
    "falsify_smallville_run",
    "falsify_v0_2",
    "load_crosswalk",
    "normalize_polarity",
    "run_backtest",
    "run_duat_conway_simulation",
    "run_smallville_duat_lab",
    "run_smallville_v0_2",
    "validate_publication_gate",
    "verify_hash_chain",
    "verify_replay",
]
