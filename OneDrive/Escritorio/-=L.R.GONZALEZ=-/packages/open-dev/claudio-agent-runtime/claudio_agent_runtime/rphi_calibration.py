from __future__ import annotations

import json
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .jsonutil import write_json
from .rphi_budget import calculate_rphi_budget


EPISODE_ORDER = [
    "clean_episode",
    "missing_evidence_episode",
    "contradiction_episode",
    "failed_command_episode",
    "review_block_episode",
    "rollback_success_episode",
    "rollback_failure_episode",
    "stale_memory_episode",
    "mixed_realistic_sanitized_episode",
    "real_local_publication_matrix_episode",
]

EXPECTED = {
    "clean_episode": {
        "expected_direction": "low R, high Phi",
        "expected_gate": "APPROVE",
    },
    "missing_evidence_episode": {
        "expected_direction": "R higher than clean; missing_evidence_component > 0",
        "expected_gate": "REVIEW",
    },
    "contradiction_episode": {
        "expected_direction": "contradiction_component > 0; R higher than clean",
        "expected_gate": "REVIEW",
    },
    "failed_command_episode": {
        "expected_direction": "failure_component > 0; R higher than clean; Phi lower than clean",
        "expected_gate": "REVIEW",
    },
    "review_block_episode": {
        "expected_direction": "review_block_component higher than clean; R higher than clean; Phi lower than clean",
        "expected_gate": "REVIEW",
    },
    "rollback_success_episode": {
        "expected_direction": "rollback_component > 0; no BLOCK",
        "expected_gate": "APPROVE_OR_REVIEW",
    },
    "rollback_failure_episode": {
        "expected_direction": "rollback failure triggers BLOCK",
        "expected_gate": "BLOCK",
    },
    "stale_memory_episode": {
        "expected_direction": "stale_state_component > 0; R higher than clean",
        "expected_gate": "REVIEW",
    },
    "mixed_realistic_sanitized_episode": {
        "expected_direction": "mixed residue should not be OPTIMO",
        "expected_gate": "REVIEW",
    },
    "real_local_publication_matrix_episode": {
        "expected_direction": "real sanitized local book-control work: low R, adequate Phi, no external action",
        "expected_gate": "APPROVE",
    },
}


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def default_fixture_root() -> Path:
    return Path(__file__).resolve().parents[1] / "tests" / "fixtures" / "rphi_episodes"


def _read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(item, dict):
            rows.append(item)
    return rows


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n")


def _memory_records(episode_dir: Path) -> list[dict[str, Any]]:
    data = _read_json(episode_dir / "memory.json", {"records": []})
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]
    if isinstance(data, dict) and isinstance(data.get("records"), list):
        return [item for item in data["records"] if isinstance(item, dict)]
    return []


def _command_events(episode_dir: Path) -> list[dict[str, Any]]:
    data = _read_json(episode_dir / "command_outcomes.json", {"commands": []})
    commands = data.get("commands") if isinstance(data, dict) else []
    if not isinstance(commands, list):
        return []
    events: list[dict[str, Any]] = []
    for index, command in enumerate(commands):
        if not isinstance(command, dict):
            continue
        events.append(
            {
                "schema_version": "claudio.witness_log.v0.1",
                "event_id": command.get("event_id") or f"evt-command-{index:03d}",
                "created_at": command.get("created_at") or "2026-05-15T00:00:00Z",
                "command": command.get("command") or "local command",
                "status": command.get("status") or "ok",
                "actiongate": command.get("actiongate") or "APPROVE",
                "target": command.get("target"),
                "reason": command.get("reason"),
                "result_summary": {
                    "kind": "dict",
                    "redacted": True,
                    "evidence": command.get("evidence"),
                    "decision": command.get("decision"),
                },
            }
        )
    return events


def _rollback_manifests(episode_dir: Path) -> list[dict[str, Any]]:
    data = _read_json(episode_dir / "rollback_manifest.json", {"rollbacks": []})
    if isinstance(data, dict) and isinstance(data.get("rollbacks"), list):
        return [item for item in data["rollbacks"] if isinstance(item, dict)]
    if isinstance(data, dict) and data.get("rollback_id"):
        return [data]
    return []


def materialize_episode_state(episode_dir: str | Path, state_root: str | Path) -> Path:
    episode = Path(episode_dir)
    state = Path(state_root)
    state.mkdir(parents=True, exist_ok=True)

    task_source = episode / "task_board.json"
    task_target = state / "tasks" / "task_board.json"
    task_target.parent.mkdir(parents=True, exist_ok=True)
    if task_source.exists():
        shutil.copy2(task_source, task_target)
    else:
        write_json(task_target, {"schema_version": "claudio.task_board.v0.1", "tasks": []})

    memory_rows = _memory_records(episode)
    _write_jsonl(state / "memory" / "memory_lite.jsonl", memory_rows)

    witness_rows = _read_jsonl(episode / "witnesslog.jsonl")
    witness_rows.extend(_command_events(episode))
    _write_jsonl(state / "witness" / "witness_log.jsonl", witness_rows)

    for index, manifest in enumerate(_rollback_manifests(episode)):
        rollback_id = str(manifest.get("rollback_id") or f"rollback-fixture-{index:03d}")
        rollback_dir = state / "runtime" / "rollback" / rollback_id
        write_json(rollback_dir / "manifest.json", manifest | {"rollback_id": rollback_id})

    return state


def _episode_dirs(fixtures_root: Path) -> list[Path]:
    dirs = [fixtures_root / name for name in EPISODE_ORDER if (fixtures_root / name).exists()]
    extras = sorted(path for path in fixtures_root.iterdir() if path.is_dir() and path.name not in EPISODE_ORDER) if fixtures_root.exists() else []
    return dirs + extras


def _evaluate_episode(name: str, budget: dict[str, Any], clean: dict[str, Any] | None) -> tuple[bool, list[str]]:
    checks: list[tuple[bool, str]] = []
    gate = budget["actiongate_suggestion"]
    components = budget["components"]

    if name == "clean_episode":
        checks.append((budget["regime"] != "JAMMING", "clean is not JAMMING"))
        checks.append((gate == "APPROVE", "clean gate is APPROVE"))
    elif name == "missing_evidence_episode":
        checks.append((clean is not None and budget["r_total"] > clean["r_total"], "R higher than clean"))
        checks.append((components["missing_evidence_component"] > 0, "missing evidence detected"))
        checks.append((gate == "REVIEW", "gate is REVIEW"))
    elif name == "contradiction_episode":
        checks.append((components["contradiction_component"] > 0, "contradiction detected"))
        checks.append((clean is not None and budget["r_total"] > clean["r_total"], "R higher than clean"))
    elif name == "failed_command_episode":
        checks.append((components["failure_component"] > 0, "failure detected"))
        checks.append((clean is not None and budget["r_total"] > clean["r_total"], "R higher than clean"))
        checks.append((clean is not None and budget["phi_eff"] < clean["phi_eff"], "Phi lower than clean"))
    elif name == "review_block_episode":
        clean_component = clean["components"]["review_block_component"] if clean else 0
        checks.append((components["review_block_component"] > clean_component, "review/block component higher than clean"))
        checks.append((clean is not None and budget["r_total"] > clean["r_total"], "R higher than clean"))
        checks.append((clean is not None and budget["phi_eff"] < clean["phi_eff"], "Phi lower than clean"))
    elif name == "rollback_success_episode":
        checks.append((components["rollback_component"] > 0, "rollback component detected"))
        checks.append((gate != "BLOCK", "gate is not BLOCK"))
    elif name == "rollback_failure_episode":
        checks.append((gate == "BLOCK", "rollback failure triggers BLOCK"))
    elif name == "stale_memory_episode":
        checks.append((components["stale_state_component"] > 0, "stale state detected"))
        checks.append((clean is not None and budget["r_total"] > clean["r_total"], "R higher than clean"))
    elif name == "mixed_realistic_sanitized_episode":
        checks.append((budget["regime"] != "OPTIMO", "mixed episode is not OPTIMO"))
        checks.append((gate == "REVIEW", "mixed gate is REVIEW"))
    elif name == "real_local_publication_matrix_episode":
        checks.append((budget["r_total"] <= 0.25, "real sanitized local episode keeps R <= 0.25"))
        checks.append((budget["phi_eff"] >= 0.75, "real sanitized local episode keeps Phi >= 0.75"))
        checks.append((gate == "APPROVE", "gate is APPROVE for local reversible inventory work"))
        checks.append((budget["raw_counts"]["publication_attempts"] == 0, "no external-release attempt detected"))
        checks.append((budget["raw_counts"]["secret_private_path_findings"] == 0, "no sensitive-path marker detected"))
    else:
        checks.append((True, "no explicit expectation"))

    return all(item[0] for item in checks), [f"{'PASS' if ok else 'FAIL'}: {message}" for ok, message in checks]


def run_calibration(fixtures_root: str | Path | None = None) -> dict[str, Any]:
    root = Path(fixtures_root) if fixtures_root is not None else default_fixture_root()
    episodes: list[dict[str, Any]] = []

    with tempfile.TemporaryDirectory(prefix="claudio-rphi-calibration-") as tmp:
        temp_root = Path(tmp)
        budgets: dict[str, dict[str, Any]] = {}
        for episode_dir in _episode_dirs(root):
            state_root = materialize_episode_state(episode_dir, temp_root / episode_dir.name)
            budgets[episode_dir.name] = calculate_rphi_budget(state_root)

        clean = budgets.get("clean_episode")
        for episode_name in [name for name in EPISODE_ORDER if name in budgets] + sorted(
            name for name in budgets if name not in EPISODE_ORDER
        ):
            budget = budgets[episode_name]
            passed, explanation = _evaluate_episode(episode_name, budget, clean)
            expected = EXPECTED.get(episode_name, {"expected_direction": "not specified", "expected_gate": "not specified"})
            episodes.append(
                {
                    "episode_name": episode_name,
                    "r_total": budget["r_total"],
                    "phi_eff": budget["phi_eff"],
                    "regime": budget["regime"],
                    "actiongate_suggestion": budget["actiongate_suggestion"],
                    "components": budget["components"],
                    "raw_counts": budget["raw_counts"],
                    "expected_direction": expected["expected_direction"],
                    "expected_gate": expected["expected_gate"],
                    "pass": passed,
                    "explanation": explanation,
                }
            )

    failed = [episode for episode in episodes if not episode["pass"]]
    critical_failures = [
        episode
        for episode in episodes
        if (
            episode["episode_name"] == "rollback_failure_episode"
            and episode["actiongate_suggestion"] != "BLOCK"
        )
        or (
            episode["episode_name"] == "clean_episode"
            and episode["regime"] == "JAMMING"
        )
    ]
    if critical_failures:
        status = "BLOCK"
    elif failed:
        status = "REVIEW"
    else:
        status = "PASS"

    return {
        "schema_version": "claudio.rphi_calibration.v0.1",
        "generated_at": _utc_now(),
        "fixtures_root": "tests/fixtures/rphi_episodes",
        "total_episodes": len(episodes),
        "passed_episodes": len(episodes) - len(failed),
        "failed_episodes": len(failed),
        "calibration_status": status,
        "weight_review_required": status != "PASS",
        "weight_review_note": (
            "WEIGHT_REVIEW_REQUIRED: inspect failed directional expectations before changing weights."
            if status != "PASS"
            else "No weight review required from this synthetic calibration pass."
        ),
        "episodes": episodes,
    }


def render_calibration_report(calibration: dict[str, Any]) -> str:
    lines = [
        "# RPHI Calibration Report",
        "",
        "Status: `LOCAL_ONLY`",
        "",
        f"calibration_status: `{calibration['calibration_status']}`",
        f"total_episodes: {calibration['total_episodes']}",
        f"passed_episodes: {calibration['passed_episodes']}",
        f"failed_episodes: {calibration['failed_episodes']}",
        f"weight_review_required: {str(calibration['weight_review_required']).lower()}",
        "",
        "## Matrix",
        "",
        "| episode | R | Phi_eff | regime | gate | pass | expected |",
        "|---|---:|---:|---|---|---|---|",
    ]
    for episode in calibration["episodes"]:
        lines.append(
            "| {episode_name} | {r_total:.4f} | {phi_eff:.4f} | {regime} | {actiongate_suggestion} | {status} | {expected_direction} |".format(
                status="PASS" if episode["pass"] else "FAIL",
                **episode,
            )
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- PASS means the synthetic directional expectations moved as intended.",
            "- REVIEW means at least one weak expectation failed and should be inspected before changing weights.",
            "- BLOCK means rollback failure did not block or clean work was classified as JAMMING.",
            "",
            "## WEIGHT_REVIEW_REQUIRED",
            "",
            calibration["weight_review_note"],
        ]
    )
    return "\n".join(lines) + "\n"


def write_calibration_artifacts(
    fixtures_root: str | Path | None = None,
    output_root: str | Path | None = None,
) -> dict[str, Any]:
    calibration = run_calibration(fixtures_root)
    artifact_root = Path(output_root) if output_root is not None else Path.cwd() / "qa_artifacts"
    json_path = artifact_root / "rphi-calibration-latest.json"
    report_path = artifact_root / "rphi-calibration-report-latest.md"
    write_json(json_path, calibration)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(render_calibration_report(calibration), encoding="utf-8")
    return {
        "calibration": calibration,
        "json_path": str(json_path),
        "markdown_report_path": str(report_path),
    }


def latest_calibration_status(root: str | Path = ".") -> dict[str, Any]:
    base = Path(root)
    candidates = [
        base / "qa_artifacts" / "rphi-calibration-latest.json",
        base.parent / "qa_artifacts" / "rphi-calibration-latest.json",
        base.parent.parent / "qa_artifacts" / "rphi-calibration-latest.json",
    ]
    for path in candidates:
        data = _read_json(path, None)
        if isinstance(data, dict):
            return {
                "exists": True,
                "path": "qa_artifacts/rphi-calibration-latest.json",
                "calibration_status": data.get("calibration_status"),
                "total_episodes": data.get("total_episodes"),
                "passed_episodes": data.get("passed_episodes"),
                "failed_episodes": data.get("failed_episodes"),
                "generated_at": data.get("generated_at"),
            }
    return {
        "exists": False,
        "path": "qa_artifacts/rphi-calibration-latest.json",
    }
