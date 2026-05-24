"""Stable contract names for GEODIA Social Observatory."""

SOURCE_SNAPSHOT_SCHEMA = "claudio.social_source_snapshot.v1"
EPOCH_MODEL_SCHEMA = "claudio.social_epoch_model.v1"
SCENARIO_REPORT_SCHEMA = "claudio.social_scenario_report.v1"
LOCAL_SOURCE_INTAKE_SCHEMA = "motor.local_source_intake.v1"
OBSERVATION_EVENT_SCHEMA = "motor.observation_event.v1"
ARTIFACT_RECORD_SCHEMA = "motor.artifact_record.v1"
ROUTE_DECISION_SCHEMA = "motor.route_decision.v1"
BEHAVIOR_SIGNATURE_SCHEMA = "motor.behavior_signature.v1"
DUAT_HEALTH_WINDOW_SCHEMA = "motor.duat_health_window.v1"
DUAT_CONWAY_SIMULATION_SCHEMA = "motor.duat_conway_simulation.v1"
DUAT_V2_INTAKE_SCHEMA = "motor.duat_v2_intake.v1"
DUAT_SMALLVILLE_SCENARIO_SCHEMA = "duat.smallville.simulation_scenario.v0_1"
DUAT_SMALLVILLE_LEDGER_SCHEMA = "duat.smallville.simulation_run_ledger.v0_1"
DUAT_SMALLVILLE_FALSIFIER_SCHEMA = "duat.smallville.falsifier_report.v0_1"
DUAT_SIGNAL_SOURCE_PACK_SCHEMA = "duat.smallville.signal_source_pack.v0_2"
DUAT_SMALLVILLE_INTERVENTION_SCHEMA = "duat.smallville.intervention_run.v0_2"
DUAT_SMALLVILLE_REPLAY_SCHEMA = "duat.smallville.replay_verification.v0_2"
DUAT_SMALLVILLE_METRICS_SCHEMA = "duat.smallville.metrics.v0_2"
DUAT_SMALLVILLE_FALSIFIER_V0_2_SCHEMA = "duat.smallville.falsifier_report.v0_2"
DUAT_REMOTE_COMPUTE_PLAN_SCHEMA = "duat.remote_compute_plan.v0_1"
DUAT_REMOTE_RUN_SPEC_SCHEMA = "duat.remote_run_spec.v0_1"

CLASSIFICATIONS = ("CERTEZA", "INFERENCIA", "INCOGNITA")


def claim(classification: str, statement: str, evidence: list[dict[str, str]]) -> dict[str, object]:
    if classification not in CLASSIFICATIONS:
        raise ValueError(f"invalid classification: {classification}")
    return {
        "classification": classification,
        "statement": statement,
        "evidence": evidence,
    }
