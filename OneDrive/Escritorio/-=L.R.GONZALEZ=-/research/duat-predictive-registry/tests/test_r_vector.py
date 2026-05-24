from duat_predictive_registry.r_vector import R_DIMENSIONS, compute_r_total


def test_r_vector_has_expected_dimensions():
    assert "R_cognitive" in R_DIMENSIONS
    assert "R_sensitive" in R_DIMENSIONS
    assert "R_agent_operational" in R_DIMENSIONS


def test_sensitive_r_partially_dominates_total():
    value = compute_r_total({"R_sensitive": 0.9, "R_source": 0.1}, task_type="technical")
    assert value >= 0.75
