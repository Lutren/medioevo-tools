import pytest

from obs_info_kernel import Source
from obs_info_kernel.math_canon import MATH_CANON_VERSION, R_noisy_or
from obs_info_kernel.operator_profile import OperatorProfiler


def test_operator_profiler_consumes_07b_for_r_and_phi_source():
    source = Source.make(
        "07b active flow fixture",
        "define actualizacion residuo sesgo con prueba local",
        "ia",
        evidence_type="experiment",
    )
    profiler = OperatorProfiler(expected_operators=["actualizacion", "residuo", "sesgo", "jamming"])

    profile = profiler.build(source)

    assert profile.r_source == pytest.approx(R_noisy_or([0.25, 0.0, 0.0]))
    assert 0.0 <= profile.phi_source <= 1.0
    assert profile.phi_source != pytest.approx(1.0 - profile.r_source)
    assert profile.metadata["math_canon"]["version"] == MATH_CANON_VERSION
    assert profile.metadata["math_canon"]["r_source_formula"] == "R_or = 1 - prod_i(1 - r_i)"
    assert profile.metadata["math_canon"]["claim_boundary"] == "operational_proxy_not_science_claim"


def test_operator_atlas_summary_averages_canonical_phi_source():
    source = Source.make(
        "07b atlas fixture",
        "define actualizacion residuo sesgo con prueba local",
        "ia",
        evidence_type="experiment",
    )
    profiler = OperatorProfiler(expected_operators=["actualizacion", "residuo", "sesgo", "jamming"])
    profile = profiler.build(source)
    summary = profiler.atlas_summary([profile])

    assert summary["mean_r_source"] == round(profile.r_source, 4)
    assert summary["mean_phi_source"] == round(profile.phi_source, 4)
