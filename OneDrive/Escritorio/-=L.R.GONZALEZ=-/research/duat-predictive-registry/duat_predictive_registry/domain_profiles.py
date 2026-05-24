"""Domain profiles for DUAT predictive benchmark calibration."""

from __future__ import annotations

from copy import deepcopy
from typing import Any


DOMAIN_PROFILES: dict[str, dict[str, Any]] = {
    "economy": {
        "minimum_observations": 5,
        "preferred_metrics": ["MAE", "RMSE"],
        "mape_allowed": "if_positive_nonzero",
        "claim_threshold": "internal_only",
    },
    "labor_market": {
        "minimum_observations": 5,
        "preferred_metrics": ["MAE", "RMSE"],
        "mape_allowed": "if_positive_nonzero",
        "claim_threshold": "internal_only",
        "caveat": "labor indicators can improve R while worsening direct forecast metrics due to smoothing/lag/proxy mismatch",
    },
    "demography": {
        "minimum_observations": 5,
        "preferred_metrics": ["MAE", "RMSE"],
        "mape_allowed": "if_positive_nonzero",
        "claim_threshold": "internal_only",
    },
    "health": {
        "minimum_observations": 5,
        "preferred_metrics": ["MAE", "RMSE"],
        "mape_allowed": "if_positive_nonzero",
        "claim_threshold": "internal_only",
        "extra_gate": "high_stakes_claim_review",
    },
    "life": {
        "minimum_observations": 5,
        "preferred_metrics": ["MAE", "RMSE"],
        "mape_allowed": "if_positive_nonzero",
        "claim_threshold": "internal_only",
    },
    "education": {
        "minimum_observations": 5,
        "preferred_metrics": ["MAE", "RMSE"],
        "mape_allowed": "if_positive_nonzero",
        "claim_threshold": "internal_only",
    },
    "unknown": {
        "minimum_observations": 5,
        "preferred_metrics": ["MAE", "RMSE"],
        "mape_allowed": "if_positive_nonzero",
        "claim_threshold": "internal_only",
    },
}


def infer_domain(indicator: str | None) -> str:
    """Infer a benchmark domain from a canonical indicator id."""

    value = (indicator or "").lower()
    if value.startswith("economy.") or "gdp" in value or "growth" in value:
        return "economy"
    if value.startswith("labor_market.") or "unemployment" in value or "labor" in value:
        return "labor_market"
    if value.startswith("demography.") or "population" in value:
        return "demography"
    if value.startswith("health."):
        return "health"
    if value.startswith("life.") or "life_expectancy" in value or "expectancy" in value:
        return "life"
    if value.startswith("education.") or "school" in value:
        return "education"
    return "unknown"


def get_domain_profile(domain: str | None) -> dict[str, Any]:
    """Return a defensive copy of the profile for the requested domain."""

    key = domain if domain in DOMAIN_PROFILES else "unknown"
    return deepcopy(DOMAIN_PROFILES[key])


def validate_domain_profiles() -> list[str]:
    """Validate profile shape without requiring external schema packages."""

    errors: list[str] = []
    for domain, profile in DOMAIN_PROFILES.items():
        if profile.get("minimum_observations", 0) < 1:
            errors.append(f"{domain}.minimum_observations must be positive")
        if not profile.get("preferred_metrics"):
            errors.append(f"{domain}.preferred_metrics must not be empty")
        if profile.get("claim_threshold") != "internal_only":
            errors.append(f"{domain}.claim_threshold must be internal_only")
    return errors
