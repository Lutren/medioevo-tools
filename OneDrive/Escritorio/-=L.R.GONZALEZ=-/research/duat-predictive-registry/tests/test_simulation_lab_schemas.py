from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _schema(name: str) -> dict[str, object]:
    return json.loads((ROOT / "schemas" / name).read_text(encoding="utf-8"))


def test_simulation_scenario_schema_locks_synthetic_smallville_boundary():
    schema = _schema("duat_simulation_scenario_v0_1.schema.json")
    assert schema["properties"]["schema"]["const"] == "duat.smallville.simulation_scenario.v0_1"
    assert schema["properties"]["agent_count"]["const"] == 25
    assert schema["properties"]["source_policy"]["properties"]["publication_gate"]["const"] == "BLOCK"
    assert schema["properties"]["source_policy"]["properties"]["fixtures"]["const"] == "SYNTHETIC_ONLY"


def test_signal_source_pack_schema_requires_hash_and_blocks_publication():
    schema = _schema("duat_signal_source_pack_v0_1.schema.json")
    required = set(schema["required"])
    assert "payload_sha256" in required
    assert "license_status" in required
    assert "comparability_status" in required
    assert schema["properties"]["publication_gate"]["const"] == "BLOCK"


def test_remote_run_spec_schema_keeps_external_publish_disabled():
    schema = _schema("duat_remote_run_spec_v0_1.schema.json")
    assert "simscale" in schema["properties"]["provider"]["enum"]
    assert "colab_notebook" in schema["properties"]["provider"]["enum"]
    assert "kaggle_kernel" in schema["properties"]["provider"]["enum"]
    assert schema["properties"]["publication_gate"]["const"] == "BLOCK"
    assert schema["properties"]["external_publication"]["const"] is False


def test_simulation_ledger_schema_blocks_public_prediction_claims():
    schema = _schema("duat_simulation_run_ledger_v0_1.schema.json")
    claims = schema["properties"]["claims"]["properties"]
    gates = schema["properties"]["gates"]["properties"]
    assert claims["public_prediction"]["const"] == "NOT_ALLOWED"
    assert claims["bias"]["const"] == "AUDITABLE_NOT_ABSENT"
    assert gates["RemoteComputeGate"]["const"] == "REVIEW_FOR_EXTERNAL_RUNTIME"
    assert gates["publication_gate"]["const"] == "BLOCK"
