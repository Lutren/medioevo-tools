from duat_predictive_registry.source_quality import (
    SourceQualityInputs,
    compute_r_source,
    compute_source_quality,
)


def test_source_quality_is_bounded():
    score = compute_source_quality(
        SourceQualityInputs(
            provenance_score=1.0,
            license_score=0.8,
            api_stability_score=0.9,
            granularity_score=0.7,
            coverage_score=0.9,
            traceability_score=1.0,
            reproducibility_score=0.8,
        )
    )
    assert 0.0 <= score <= 1.0
    assert compute_r_source(score) == 1.0 - score


def test_low_license_score_reduces_quality():
    high = compute_source_quality({"provenance_score": 1, "license_score": 1, "api_stability_score": 1, "granularity_score": 1, "coverage_score": 1, "traceability_score": 1, "reproducibility_score": 1})
    low = compute_source_quality({"provenance_score": 1, "license_score": 0, "api_stability_score": 1, "granularity_score": 1, "coverage_score": 1, "traceability_score": 1, "reproducibility_score": 1})
    assert low < high
