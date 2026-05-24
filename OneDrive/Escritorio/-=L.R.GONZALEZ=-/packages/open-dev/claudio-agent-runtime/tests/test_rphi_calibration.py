from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from claudio_agent_runtime.cli import main
from claudio_agent_runtime.rphi_calibration import default_fixture_root, run_calibration, write_calibration_artifacts


FIXTURES = default_fixture_root()


def _episodes_by_name(calibration: dict) -> dict[str, dict]:
    return {episode["episode_name"]: episode for episode in calibration["episodes"]}


def test_calibration_schema_is_stable() -> None:
    calibration = run_calibration(FIXTURES)
    assert set(calibration) == {
        "schema_version",
        "generated_at",
        "fixtures_root",
        "total_episodes",
        "passed_episodes",
        "failed_episodes",
        "calibration_status",
        "weight_review_required",
        "weight_review_note",
        "episodes",
    }
    assert calibration["schema_version"] == "claudio.rphi_calibration.v0.1"
    assert calibration["total_episodes"] == 10
    assert calibration["calibration_status"] == "PASS"


def test_direction_clean_missing_failed() -> None:
    episodes = _episodes_by_name(run_calibration(FIXTURES))
    assert episodes["clean_episode"]["r_total"] < episodes["missing_evidence_episode"]["r_total"]
    assert episodes["clean_episode"]["r_total"] < episodes["failed_command_episode"]["r_total"]
    assert episodes["clean_episode"]["phi_eff"] > episodes["failed_command_episode"]["phi_eff"]


def test_contradiction_component_detected() -> None:
    episode = _episodes_by_name(run_calibration(FIXTURES))["contradiction_episode"]
    assert episode["components"]["contradiction_component"] > 0


def test_missing_evidence_component_detected() -> None:
    episode = _episodes_by_name(run_calibration(FIXTURES))["missing_evidence_episode"]
    assert episode["components"]["missing_evidence_component"] > 0
    assert episode["actiongate_suggestion"] == "REVIEW"


def test_rollback_failure_blocks() -> None:
    episode = _episodes_by_name(run_calibration(FIXTURES))["rollback_failure_episode"]
    assert episode["actiongate_suggestion"] == "BLOCK"


def test_rollback_success_does_not_block() -> None:
    episode = _episodes_by_name(run_calibration(FIXTURES))["rollback_success_episode"]
    assert episode["components"]["rollback_component"] > 0
    assert episode["actiongate_suggestion"] != "BLOCK"


def test_stale_memory_component_detected() -> None:
    episode = _episodes_by_name(run_calibration(FIXTURES))["stale_memory_episode"]
    assert episode["components"]["stale_state_component"] > 0


def test_review_block_component_increases_over_clean() -> None:
    episodes = _episodes_by_name(run_calibration(FIXTURES))
    assert episodes["review_block_episode"]["r_total"] > episodes["clean_episode"]["r_total"]
    assert (
        episodes["review_block_episode"]["components"]["review_block_component"]
        > episodes["clean_episode"]["components"]["review_block_component"]
    )


def test_mixed_realistic_sanitized_episode_is_not_optimo() -> None:
    episode = _episodes_by_name(run_calibration(FIXTURES))["mixed_realistic_sanitized_episode"]
    assert episode["regime"] != "OPTIMO"
    assert episode["actiongate_suggestion"] == "REVIEW"


def test_real_local_publication_matrix_episode_is_bounded_and_sanitized() -> None:
    episode = _episodes_by_name(run_calibration(FIXTURES))["real_local_publication_matrix_episode"]
    assert episode["r_total"] <= 0.25
    assert episode["phi_eff"] >= 0.75
    assert episode["actiongate_suggestion"] == "APPROVE"
    assert episode["raw_counts"]["publication_attempts"] == 0
    assert episode["raw_counts"]["secret_private_path_findings"] == 0


def test_write_calibration_artifacts_and_cli(tmp_path: Path) -> None:
    result = write_calibration_artifacts(FIXTURES, output_root=tmp_path)
    assert Path(result["json_path"]).exists()
    assert Path(result["markdown_report_path"]).exists()
    assert result["calibration"]["calibration_status"] == "PASS"

    cli_out = tmp_path / "cli"
    assert main(["budget", "calibrate", "--fixtures-root", str(FIXTURES), "--output-root", str(cli_out), "--json"]) == 0
    assert (cli_out / "rphi-calibration-latest.json").exists()
    assert (cli_out / "rphi-calibration-report-latest.md").exists()
