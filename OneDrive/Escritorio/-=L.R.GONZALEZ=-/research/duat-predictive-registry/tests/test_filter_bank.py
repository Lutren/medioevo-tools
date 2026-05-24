from duat_predictive_registry.filter_bank import filter_catalog, required_filter_ids


def test_filter_bank_covers_sensitive_and_source_filters():
    catalog = filter_catalog()
    ids = {row["filter_id"] for row in catalog}
    assert "sensitive_boundary_filter" in ids
    assert "source_quality_filter" in ids


def test_required_filter_ids_routes_high_dimensions():
    required = required_filter_ids({"R_sensitive": 0.9, "R_source": 0.4, "R_user_style": 0.01})
    assert "sensitive_boundary_filter" in required
    assert "source_quality_filter" in required
    assert "user_style_adapter" not in required
