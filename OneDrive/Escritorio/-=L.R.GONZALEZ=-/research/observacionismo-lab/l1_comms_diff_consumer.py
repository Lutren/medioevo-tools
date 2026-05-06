#!/usr/bin/env python3
"""Read L1 workpack COMMS inbox messages and build dry diff plans.

The consumer is read-only with respect to the repository. It may write a plan
JSON only when --out is supplied. It never applies patches.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from l1_programmer_workpack import FORBIDDEN_OPERATIONS, WORKPACK_SCHEMA, validate_programmer_workpack
from l1_to_envelope import canonical_json, fingerprint


DIFF_PLAN_SCHEMA = "observacionismo.l1_comms_diff_plan.v0_1"
COMMS_MESSAGE_SCHEMA = "observacionismo.l1_programmer_workpack.comms_message.v0_1"

PRIVATE_PATH_MARKERS = (
    "metaevo-tcg",
    "/tcg/",
    "\\tcg\\",
    "runtime/game_bridge",
    "runtime\\game_bridge",
    "game-private",
)

SECRET_PATH_MARKERS = (
    ".env",
    "secret",
    "token",
    "credential",
    "settings.local.json",
    ".claw",
    ".claude",
    ".wrangler",
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def is_relative_safe(raw_path: str) -> bool:
    path = Path(str(raw_path or ""))
    return bool(raw_path) and not path.is_absolute() and ".." not in path.parts


def is_within_path(base_path: Path, candidate_path: Path) -> bool:
    try:
        candidate_path.resolve().relative_to(base_path.resolve())
    except ValueError:
        return False
    return True


def has_marker(path: str, markers: tuple[str, ...]) -> bool:
    lower = path.lower().replace("/", "\\")
    lower_slash = path.lower().replace("\\", "/")
    return any(marker.lower() in lower or marker.lower() in lower_slash for marker in markers)


def observe_target(repo_root: Path, raw_path: str) -> dict[str, Any]:
    repo = repo_root.resolve()
    safe_relative = is_relative_safe(raw_path)
    resolved = (repo / raw_path).resolve() if safe_relative else repo
    within_repo = safe_relative and is_within_path(repo, resolved)
    private_boundary = has_marker(raw_path, PRIVATE_PATH_MARKERS)
    secret_like_path = has_marker(raw_path, SECRET_PATH_MARKERS)
    exists = bool(within_repo and resolved.exists())
    is_file = bool(exists and resolved.is_file())
    return {
        "path": raw_path,
        "safe_relative": safe_relative,
        "within_repo": within_repo,
        "exists": exists,
        "is_file": is_file,
        "private_boundary": private_boundary,
        "secret_like_path": secret_like_path,
        "sha256": sha256_file(resolved) if is_file else "",
        "read_allowed": bool(is_file and not private_boundary and not secret_like_path),
    }


def iter_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        value = json.loads(line)
        if isinstance(value, dict):
            rows.append(value)
    return rows


def extract_workpack_message(row: dict[str, Any]) -> dict[str, Any] | None:
    if row.get("schema") != COMMS_MESSAGE_SCHEMA:
        return None
    workpack = row.get("workpack")
    if not isinstance(workpack, dict):
        return None
    return row


def build_diff_plan_from_message(message: dict[str, Any], *, repo_root: str | Path) -> dict[str, Any]:
    repo = Path(repo_root).resolve()
    workpack = message.get("workpack", {})
    patch_policy = workpack.get("patch_policy", {})
    proposed_scope = workpack.get("proposed_scope", {})
    risk_flags = list(workpack.get("risk_flags") or [])
    target_paths = [str(path) for path in proposed_scope.get("target_paths", [])]
    target_observations = [observe_target(repo, path) for path in target_paths]
    validation = validate_embedded_workpack(workpack)

    blockers: list[str] = []
    if not validation["ok"]:
        blockers.extend(validation["errors"])
    if workpack.get("status") == "BLOCKED_BY_ACTION_GATE" or "blocked_external_action" in risk_flags:
        blockers.append("blocked_by_action_gate")
    if patch_policy.get("may_apply_patch") is not False:
        blockers.append("embedded_workpack_allows_apply")
    if workpack.get("status") == "REVIEW_MISSING_EVIDENCE":
        blockers.append("missing_evidence")
    if not target_paths and workpack.get("status") == "REVIEW_PATCH_PLAN_ONLY":
        blockers.append("missing_target_paths")
    unsafe_targets = [
        item["path"]
        for item in target_observations
        if not item["safe_relative"] or not item["within_repo"] or item["private_boundary"] or item["secret_like_path"]
    ]
    if unsafe_targets:
        blockers.append("unsafe_target_path")
    missing_targets = [item["path"] for item in target_observations if not item["exists"]]
    if missing_targets:
        blockers.append("target_missing")
    not_file_targets = [item["path"] for item in target_observations if item["exists"] and not item["is_file"]]
    if not_file_targets:
        blockers.append("target_not_file")

    if "blocked_by_action_gate" in blockers:
        status = "BLOCKED_BY_ACTION_GATE"
    elif blockers:
        status = "REVIEW_NOT_DIFFABLE"
    elif workpack.get("status") == "REVIEW_PATCH_PLAN_ONLY" and target_observations:
        status = "DIFF_PLAN_READY"
    elif workpack.get("status") == "READY_READ_ONLY":
        status = "READ_ONLY_NO_DIFF"
    else:
        status = "REVIEW_NOT_DIFFABLE"

    proposals = []
    if status == "DIFF_PLAN_READY":
        proposals = [
            {
                "path": item["path"],
                "operation": "prepare_manual_diff",
                "before_sha256": item["sha256"],
                "reason": "L1 workpack requested patch planning only; no patch is applied by this consumer.",
            }
            for item in target_observations
            if item["read_allowed"]
        ]

    plan = {
        "schema": DIFF_PLAN_SCHEMA,
        "source_message_id": message.get("message_id", ""),
        "source_workpack_id": workpack.get("workpack_id", ""),
        "repo_root": str(repo),
        "status": status,
        "blockers": sorted(set(blockers)),
        "target_observations": target_observations,
        "proposal_count": len(proposals),
        "proposals": proposals,
        "application_gate": {
            "status": "REVIEW",
            "reasons": [
                "diff_plan_requires_human_review",
                "consumer_is_read_only",
                "separate_ActionGate_APPROVE_required_before_apply",
            ],
        },
        "dry_run": True,
        "applied": False,
        "may_apply_patch": False,
        "forbidden_operations": FORBIDDEN_OPERATIONS,
        "validation_required": [
            "review target path",
            "prepare concrete unified diff in a separate gated step",
            "run module-specific tests after any future approved write",
            "record rollback before any future approved write",
        ],
    }
    plan["plan_id"] = fingerprint(plan, prefix="OBS_L1_COMMS_DIFF_PLAN_V01_2026-05-06")
    plan["validation"] = validate_diff_plan(plan)
    return plan


def validate_embedded_workpack(workpack: dict[str, Any]) -> dict[str, Any]:
    if workpack.get("schema") != WORKPACK_SCHEMA:
        return {"ok": False, "errors": ["embedded workpack schema mismatch"]}
    return validate_programmer_workpack(
        {
            **workpack,
            "intent": "",
            "observation_envelope": {},
            "action_gate": {},
            "evidence_refs": [],
            "risk_flags": workpack.get("risk_flags", []),
            "validation_required": [],
            "handoff": {},
            "falsifiers": [],
        }
    )


def validate_diff_plan(plan: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    if plan.get("schema") != DIFF_PLAN_SCHEMA:
        errors.append("schema mismatch")
    if plan.get("dry_run") is not True:
        errors.append("dry_run must be true")
    if plan.get("applied") is not False:
        errors.append("applied must be false")
    if plan.get("may_apply_patch") is not False:
        errors.append("may_apply_patch must be false")
    if plan.get("application_gate", {}).get("status") != "REVIEW":
        errors.append("application_gate must remain REVIEW")
    forbidden = set(plan.get("forbidden_operations", []))
    for operation in ("apply_patch", "delete", "external_network", "publish", "run_shell"):
        if operation not in forbidden:
            errors.append(f"missing forbidden operation: {operation}")
    if plan.get("status") == "DIFF_PLAN_READY" and not plan.get("proposals"):
        errors.append("DIFF_PLAN_READY requires proposals")
    return {
        "schema": "observacionismo.l1_comms_diff_plan.validation.v0_1",
        "ok": not errors,
        "errors": errors,
        "plan_id": plan.get("plan_id", ""),
        "status": plan.get("status", "UNKNOWN"),
    }


def consume_inbox(inbox_path: str | Path, *, repo_root: str | Path, limit: int = 20) -> dict[str, Any]:
    inbox = Path(inbox_path)
    rows = iter_jsonl(inbox)
    messages = [row for row in rows if extract_workpack_message(row)]
    selected = messages[-max(1, int(limit)) :]
    plans = [build_diff_plan_from_message(message, repo_root=repo_root) for message in selected]
    status_counts: dict[str, int] = {}
    for plan in plans:
        status_counts[plan["status"]] = status_counts.get(plan["status"], 0) + 1
    result = {
        "schema": "observacionismo.l1_comms_diff_consumer_result.v0_1",
        "inbox_path": str(inbox),
        "repo_root": str(Path(repo_root).resolve()),
        "message_count": len(messages),
        "plan_count": len(plans),
        "status_counts": status_counts,
        "plans": plans,
        "dry_run": True,
        "applied": False,
    }
    result["result_id"] = fingerprint(result, prefix="OBS_L1_COMMS_DIFF_CONSUMER_V01_2026-05-06")
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Consume L1 workpack COMMS inbox into dry diff plans.")
    parser.add_argument("inbox", type=Path)
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args(argv)
    result = consume_inbox(args.inbox, repo_root=args.repo_root, limit=args.limit)
    text = json.dumps(result, ensure_ascii=True, indent=2 if args.pretty else None, sort_keys=bool(args.pretty))
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
