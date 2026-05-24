from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from obsai_core.claim_classifier import ClaimClassifier


SCHEMA_PATH = (
    Path(__file__).resolve().parents[1]
    / "obsai_core"
    / "schemas"
    / "observation_envelope_v2_1.schema.json"
)


def test_observation_envelope_schema_file_is_canonical_json_schema() -> None:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))

    assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    assert schema["title"] == "ObservationEnvelope v2.1"
    assert schema["properties"]["schemaVersion"]["const"] == "obsai.observation_envelope.v2.1"
    assert "claimResult" in schema["$defs"]
    assert "claimGateContract" in schema["$defs"]


def test_claim_classifier_output_matches_schema_required_surface() -> None:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    envelope = ClaimClassifier().classify("2 + 2 = 4").to_dict()

    _assert_required_surface(envelope, schema)
    for claim in envelope["claims"]:
        _assert_required_surface(claim, schema["$defs"]["claimResult"])
        _assert_required_surface(claim["gate_contract"], schema["$defs"]["claimGateContract"])
        for gate in claim["gate_contract"]["gates"]:
            _assert_required_surface(gate, schema["$defs"]["gateOutcome"])
        _assert_required_surface(claim["R_components"], schema["$defs"]["claimResult"]["properties"]["R_components"])


def _assert_required_surface(payload: dict[str, Any], schema: dict[str, Any]) -> None:
    for key in schema.get("required", []):
        assert key in payload
    for key in payload:
        assert key in schema.get("properties", {})
