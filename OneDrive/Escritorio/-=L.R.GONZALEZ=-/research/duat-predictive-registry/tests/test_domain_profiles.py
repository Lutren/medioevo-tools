from __future__ import annotations

from duat_predictive_registry.domain_profiles import get_domain_profile, infer_domain, validate_domain_profiles


def test_domain_profiles_validate():
    assert validate_domain_profiles() == []
    assert get_domain_profile("labor_market")["claim_threshold"] == "internal_only"


def test_infer_domain_from_indicator():
    assert infer_domain("economy.real_growth_rate") == "economy"
    assert infer_domain("labor_market.unemployment_rate.total") == "labor_market"
    assert infer_domain("demography.life_expectancy_at_birth.total") == "demography"
    assert infer_domain("health.life_expectancy") == "health"
    assert infer_domain("education.school_enrollment") == "education"
    assert infer_domain("unknown.indicator") == "unknown"
