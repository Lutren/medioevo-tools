from duat_predictive_registry.pilot_smoke import build_pilot_smoke_report


def test_pilot_smoke_is_offline_and_blocked_for_publication():
    report = build_pilot_smoke_report()
    assert report["network_used"] is False
    assert report["publication_gate"] == "BLOCK"
    assert len(report["sources"]) == 3
    assert all(row["synthetic_smoke_test"] is True for row in report["sources"])
    assert all(row["forecast_gate"]["gate"] == "REVIEW" for row in report["sources"])
