from __future__ import annotations

import json
from pathlib import Path

from duat_predictive_registry.objectives import load_objective, validate_objective


ROOT = Path(__file__).resolve().parents[1]


def test_predictive_objective_schema_has_required_fields():
    schema = json.loads((ROOT / "schemas" / "duat_predictive_objective_v0_1.schema.json").read_text(encoding="utf-8"))
    required = set(schema["required"])
    assert "objective_id" in required
    assert "canonical_indicator_id" in required
    assert schema["properties"]["data_policy"]["properties"]["publication_gate"]["const"] == "BLOCK"


def test_first_predictive_objective_loads_and_validates():
    objective = load_objective(ROOT / "fixtures" / "duat_first_predictive_objective_v0_1.json")
    errors = validate_objective(objective)
    assert errors == []
    assert objective["synthetic"] is False
    assert objective["data_policy"]["offline_only"] is True
    assert objective["data_policy"]["publication_gate"] == "BLOCK"
