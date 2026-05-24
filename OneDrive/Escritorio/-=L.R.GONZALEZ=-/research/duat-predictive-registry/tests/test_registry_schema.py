from pathlib import Path

from duat_predictive_registry.registry_loader import (
    load_json,
    validate_methods_catalog,
    validate_source_catalog,
)


ROOT = Path(__file__).resolve().parents[1]


def test_source_catalog_shape_and_key_gates():
    catalog = load_json(ROOT / "DUAT_FREE_SIGNAL_SOURCES_CATALOG_v0_1.json")
    errors = validate_source_catalog(catalog)
    assert errors == []
    assert catalog["publication_gate"] == "BLOCK"
    assert len(catalog["sources"]) >= 20
    fred = next(row for row in catalog["sources"] if row["source_id"] == "fred_api")
    assert fred["integration_gate"] == "REVIEW_KEY_REQUIRED"


def test_methods_catalog_shape():
    catalog = load_json(ROOT / "DUAT_PREDICTIVE_METHODS_CATALOG_v0_1.json")
    errors = validate_methods_catalog(catalog)
    assert errors == []
    method_ids = {row["method_id"] for row in catalog["methods"]}
    assert "kalman_state_space" in method_ids
    assert "conformal_mapie" in method_ids
    assert "dowhy_econml_causalnex" in method_ids
