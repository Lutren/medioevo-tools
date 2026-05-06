from __future__ import annotations

import argparse
import json
import shutil
import sys
import time
from pathlib import Path

from _common import ROOT, add_common_args, rel, validate_root_arg
from publish_free_dev_github import (
    ACTION_GATE_CLI,
    CLAUDIO_ROOT,
    HOST_GATE,
    DEFAULT_OWNER,
    PUBLICATION_EVIDENCE_DIR,
    license_check,
    override_can_release,
    remote_check,
    run,
    run_json,
    scan_claims,
    scan_path_scrub,
)
from stage_public_sanitized_repos import REPOS


STAGING_ROOT = ROOT / "publish_staging" / "github-public-sanitized"
REQUIRED_PUBLIC_FILES = ("README.md", "LICENSE", "CLAIMS.md", "PRIVATE_EXCLUSIONS.md", "SECURITY.md")


def repo_by_name(name: str):
    for spec in REPOS:
        if spec.name == name:
            return spec
    raise KeyError(name)


def gate_decision(repo_name: str, repo_full_name: str, execute: bool) -> tuple[dict[str, object], dict[str, object]]:
    metadata = {
        "receptor_id": "publish_receptor",
        "repo": repo_full_name,
        "staging": rel(STAGING_ROOT / repo_name),
        "mode": "execute" if execute else "dry_run_plan",
        "lane": "github-public-sanitized",
    }
    command = [
        sys.executable,
        str(ACTION_GATE_CLI),
        "public_publish",
        "--target",
        f"github:{repo_full_name}",
        "--external-authorized",
        "--evidence-ref",
        str(ROOT / "qa_artifacts" / "release_validation" / "github-public-sanitized-staging.json"),
        "--metadata-json",
        json.dumps(metadata, ensure_ascii=False),
    ]
    if not execute:
        command.insert(3, "--dry-run")
    return run_json(command, CLAUDIO_ROOT)


def preflight_repo(spec, owner: str, execute: bool, owner_override: bool, override_operator: str) -> dict[str, object]:
    repo_full_name = f"{owner}/{spec.name}"
    staging = STAGING_ROOT / spec.name
    row: dict[str, object] = {
        "repo": spec.name,
        "github_repo": repo_full_name,
        "staging": rel(staging),
        "execute_requested": execute,
    }

    required_paths = [staging, staging / ".git", *(staging / name for name in REQUIRED_PUBLIC_FILES)]
    missing = [rel(path) for path in required_paths if not path.exists()]
    row["missing"] = missing
    commands: list[dict[str, object]] = []
    if missing:
        row["ok"] = False
        row["reason"] = "missing required local artifact"
        row["commands"] = commands
        return row

    status = run(["git", "status", "--short"], staging)
    head = run(["git", "log", "--oneline", "-1"], staging)
    remote = run(["git", "remote", "-v"], staging)
    commands.extend([status, head, remote])
    remote_result = remote_check(remote, repo_full_name)
    license_result = license_check(staging)
    path_scrub = scan_path_scrub(staging)
    claims_scan = scan_claims(staging)

    secret_scan = run(
        [
            sys.executable,
            str(ROOT / "tools" / "release" / "scan_secrets.py"),
            "--path",
            rel(staging),
            "--json",
            "--fail-on-findings",
        ],
        ROOT,
    )
    commands.append(secret_scan)

    gate_command, gate_payload = gate_decision(spec.name, repo_full_name, execute)
    commands.append(gate_command)
    host_payload = gate_payload.get("action_gate", {}).get("host_gate", {})
    override_applied = False
    override_reason = ""
    if owner_override and execute and not bool(gate_payload.get("ok")):
        override_ok, override_reason = override_can_release(gate_payload.get("action_gate", {}), {"gate": host_payload})
        override_applied = bool(override_ok)

    row.update(
        {
            "head": head["stdout_tail"][0] if head["stdout_tail"] else "",
            "staging_clean": status["returncode"] == 0 and not status["stdout_tail"],
            "remote_ok": remote_result,
            "license_check": license_result,
            "path_scrub": path_scrub,
            "claims_scan": claims_scan,
            "action_gate": gate_payload.get("action_gate", {}),
            "owner_override": {
                "requested": owner_override,
                "applied": override_applied,
                "operator": override_operator if owner_override else "",
                "reason": override_reason,
            },
            "commands": commands,
        }
    )
    row["preflight_ok"] = (
        bool(row["staging_clean"])
        and bool(remote_result.get("ok"))
        and bool(license_result.get("ok"))
        and bool(path_scrub.get("ok"))
        and bool(claims_scan.get("ok"))
        and secret_scan["returncode"] == 0
        and (bool(gate_payload.get("ok")) or override_applied)
    )
    if not execute:
        row["ok"] = bool(row["preflight_ok"])
        row["reason"] = "dry-run only; no external action performed"
        return row
    if not row["preflight_ok"]:
        row["ok"] = False
        row["reason"] = "blocked before external action"
        return row
    if shutil.which("gh") is None:
        row["ok"] = False
        row["reason"] = "gh CLI not found"
        return row

    view_before = run(["gh", "repo", "view", repo_full_name], staging)
    external_commands = [view_before]
    if view_before["returncode"] != 0:
        external_commands.append(
            run(
                [
                    "gh",
                    "repo",
                    "create",
                    repo_full_name,
                    "--public",
                    "--source",
                    ".",
                    "--remote",
                    "origin",
                    "--push",
                    "--description",
                    spec.summary[:350],
                ],
                staging,
            )
        )
    else:
        if not remote_result["has_remote"]:
            external_commands.append(run(["git", "remote", "add", "origin", remote_result["expected_remote"]], staging))
        external_commands.append(run(["git", "push", "-u", "origin", "main"], staging))
    external_commands.append(run(["gh", "repo", "view", repo_full_name, "--json", "nameWithOwner,url,isPrivate"], staging))
    row["external_commands"] = external_commands
    row["ok"] = external_commands[-1]["returncode"] == 0 and all(item["returncode"] == 0 for item in external_commands[1:])
    row["reason"] = "external publish verified" if row["ok"] else "external publish command failed"
    return row


def main() -> int:
    parser = argparse.ArgumentParser(description="Gated GitHub publisher for sanitized public staging repos.")
    add_common_args(parser)
    parser.add_argument("--repo", choices=[spec.name for spec in REPOS], action="append")
    parser.add_argument("--owner", default=DEFAULT_OWNER)
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--owner-override-with-evidence", action="store_true")
    parser.add_argument("--override-operator", default="Luis Rene Gonzalez")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    validate_root_arg(args)

    selected = [repo_by_name(name) for name in args.repo] if args.repo else list(REPOS)
    host = run([sys.executable, str(HOST_GATE)], CLAUDIO_ROOT)
    results = [
        preflight_repo(
            spec,
            args.owner,
            args.execute,
            args.owner_override_with_evidence,
            args.override_operator,
        )
        for spec in selected
    ]
    data = {
        "owner": args.owner,
        "execute_requested": args.execute,
        "owner_override_with_evidence": args.owner_override_with_evidence,
        "override_operator": args.override_operator if args.owner_override_with_evidence else "",
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "host_gate_command": host,
        "results": results,
        "ok": all(item.get("ok") for item in results),
        "external_actions_performed": bool(args.execute and any(item.get("external_commands") for item in results)),
    }
    if args.write:
        PUBLICATION_EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
        target = PUBLICATION_EVIDENCE_DIR / ("github-public-sanitized-publish.json" if args.execute else "github-public-sanitized-dry-run.json")
        target.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        data["written"] = rel(target)
    if args.json:
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        for item in results:
            status = "ok" if item.get("ok") else "blocked"
            print(f"{item['repo']}: {status} -> {item['github_repo']} ({item.get('reason', '')})")
        if args.write:
            print(f"wrote {data['written']}")
    return 0 if data["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
