from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

from _common import PRODUCTS, ROOT, add_common_args, product_by_name, rel, sha256_file, validate_root_arg


STAGING_ROOT = ROOT / "publish_staging" / "open-dev"
ZIP_ROOT = ROOT / "releases" / "free-dev"
CLAUDIO_ROOT = ROOT / "-=MEDIOEVO=-" / "-=LIBROS" / "claudio"
ACTION_GATE_CLI = CLAUDIO_ROOT / "tools" / "action_gate_cli.py"
HOST_GATE = CLAUDIO_ROOT / "tools" / "host_observacionista.py"
DEFAULT_OWNER = "Lutren"
PUBLICATION_EVIDENCE_DIR = ROOT / "qa_artifacts" / "release_validation"
TEXT_SUFFIXES = {
    ".cfg",
    ".csv",
    ".ini",
    ".js",
    ".json",
    ".md",
    ".py",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}
ABSOLUTE_PATH_PATTERN = re.compile(r"\b[A-Za-z]:[\\/][^\s`'\"\)\]]+")
PRIVATE_PATH_MARKERS = (
    "metaevo-tcg",
    "runtime/game_bridge",
    "runtime\\game_bridge",
    "vault_medioevo",
    "tcg/",
    "tcg\\",
)
CLAIM_PATTERNS = (
    re.compile(r"\bproof of consciousness\b", re.I),
    re.compile(r"\bnew physics\b", re.I),
    re.compile(r"\bguaranteed safety\b", re.I),
    re.compile(r"\bmedical diagnosis\b", re.I),
    re.compile(r"\bcognitive diagnosis\b", re.I),
    re.compile(r"\bautonomous hacking\b", re.I),
    re.compile(r"\bcontrol(ar)?\s+(r|reality|la realidad)\b", re.I),
)
NEGATION_MARKERS = ("no ", "not ", "sin ", "without ")


def run(command: list[str], cwd: Path) -> dict[str, object]:
    result = subprocess.run(command, cwd=cwd, text=True, capture_output=True)
    return {
        "command": command,
        "cwd": rel(cwd),
        "returncode": result.returncode,
        "stdout_tail": result.stdout.splitlines()[-20:],
        "stderr_tail": result.stderr.splitlines()[-20:],
    }


def run_json(command: list[str], cwd: Path) -> tuple[dict[str, object], dict[str, object]]:
    completed = subprocess.run(command, cwd=cwd, text=True, capture_output=True)
    result = {
        "command": command,
        "cwd": rel(cwd),
        "returncode": completed.returncode,
        "stdout_tail": completed.stdout.splitlines()[-20:],
        "stderr_tail": completed.stderr.splitlines()[-20:],
    }
    try:
        parsed = json.loads(completed.stdout)
    except json.JSONDecodeError:
        parsed = {}
    return result, parsed


def iter_public_text_files(path: Path) -> list[Path]:
    files: list[Path] = []
    for child in path.rglob("*"):
        if child.is_dir():
            continue
        parts = {part.lower() for part in child.parts}
        if parts.intersection({".git", "__pycache__", ".pytest_cache", "build", "dist", "release", "node_modules"}):
            continue
        if any(part.endswith(".egg-info") for part in parts):
            continue
        if child.suffix.lower() in TEXT_SUFFIXES:
            files.append(child)
    return files


def scan_path_scrub(path: Path) -> dict[str, object]:
    findings: list[dict[str, object]] = []
    for child in iter_public_text_files(path):
        try:
            lines = child.read_text(encoding="utf-8", errors="ignore").splitlines()
        except OSError:
            continue
        for line_no, line in enumerate(lines, start=1):
            markers: list[str] = []
            if ABSOLUTE_PATH_PATTERN.search(line):
                markers.append("absolute_local_path")
            lower = line.lower()
            for marker in PRIVATE_PATH_MARKERS:
                if marker in lower:
                    markers.append(f"private_marker:{marker}")
            if markers:
                findings.append({"path": rel(child), "line": line_no, "markers": sorted(set(markers))})
    return {"ok": not findings, "findings": findings}


def has_negation_near(line: str, start: int) -> bool:
    stripped = line.strip().lower()
    if stripped.startswith(("- no ", "* no ", "no ", "- not ", "* not ", "not ")):
        return True
    guard_prefix = stripped[: max(0, start)]
    if any(marker in guard_prefix for marker in ("must not", "do not", "blocks ", "blocked ", "prohibited ", "forbidden ")):
        return True
    prefix = line[max(0, start - 24) : start].lower()
    return any(marker in prefix for marker in NEGATION_MARKERS)


def scan_claims(path: Path) -> dict[str, object]:
    findings: list[dict[str, object]] = []
    for child in iter_public_text_files(path):
        try:
            lines = child.read_text(encoding="utf-8", errors="ignore").splitlines()
        except OSError:
            continue
        for line_no, line in enumerate(lines, start=1):
            for pattern in CLAIM_PATTERNS:
                match = pattern.search(line)
                if match and not has_negation_near(line, match.start()):
                    findings.append(
                        {
                            "path": rel(child),
                            "line": line_no,
                            "pattern": pattern.pattern,
                        }
                    )
    return {"ok": not findings, "findings": findings}


def license_check(path: Path) -> dict[str, object]:
    license_path = path / "LICENSE"
    if not license_path.exists():
        return {"ok": False, "reason": "missing LICENSE"}
    try:
        text = license_path.read_text(encoding="utf-8", errors="ignore")
    except OSError as exc:
        return {"ok": False, "reason": f"cannot read LICENSE: {exc}"}
    blocked_markers = ("LEGAL_REVIEW_REQUIRED", "LICENSE STATUS", "not public-release-ready")
    blocked = [marker for marker in blocked_markers if marker.lower() in text.lower()]
    return {"ok": not blocked, "reason": "ok" if not blocked else "blocked license marker", "blocked_markers": blocked}


def remote_check(remote_result: dict[str, object], repo_full_name: str) -> dict[str, object]:
    expected = f"https://github.com/{repo_full_name}.git"
    lines = list(remote_result.get("stdout_tail") or [])
    return {
        "ok": not lines or all(expected in line for line in lines),
        "has_remote": bool(lines),
        "expected_remote": expected,
        "lines": lines,
    }


def override_can_release(action_gate: dict[str, object], host_payload: dict[str, object]) -> tuple[bool, str]:
    host_gate = (host_payload.get("gate") or {}) if isinstance(host_payload, dict) else {}
    gate_value = str(host_gate.get("gate") or action_gate.get("host_gate", {}).get("gate") or "").upper()
    host_status = str(host_gate.get("status") or action_gate.get("host_gate", {}).get("status") or "").upper()
    reason = str(action_gate.get("reason") or "")
    if gate_value == "BLOCK" or host_status == "JAMMING":
        return False, f"host not overrideable: {host_status}/{gate_value}"
    if gate_value == "REVIEW" and "requiere host APPROVE" in reason:
        return True, "owner override accepted for host REVIEW only"
    return False, f"not an overrideable ActionGate state: {reason}"


def gate_decision(product_name: str, repo_full_name: str, zip_path: Path, execute: bool) -> tuple[dict[str, object], dict[str, object]]:
    metadata = {
        "receptor_id": "publish_receptor",
        "product": product_name,
        "repo": repo_full_name,
        "artifact": rel(zip_path),
        "sha256": sha256_file(zip_path) if zip_path.exists() else "",
        "mode": "execute" if execute else "dry_run_plan",
    }
    command = [
        sys.executable,
        str(ACTION_GATE_CLI),
        "public_publish",
        "--target",
        f"github:{repo_full_name}",
        "--external-authorized",
        "--evidence-ref",
        str(ROOT / "qa_artifacts" / "release_validation" / "free-dev-staging-smoke.json"),
        "--evidence-ref",
        str(ROOT / "release_manifests" / f"{product_name}.json"),
        "--metadata-json",
        json.dumps(metadata, ensure_ascii=False),
    ]
    if not execute:
        command.insert(3, "--dry-run")
    return run_json(command, CLAUDIO_ROOT)


def preflight_product(product, owner: str, execute: bool, owner_override: bool, override_operator: str) -> dict[str, object]:
    repo_full_name = f"{owner}/{product.name}"
    staging = STAGING_ROOT / product.name
    zip_path = ZIP_ROOT / f"{product.name}.zip"
    row: dict[str, object] = {
        "product": product.name,
        "repo": repo_full_name,
        "staging": rel(staging),
        "zip": rel(zip_path),
        "execute_requested": execute,
    }

    required_paths = [staging, staging / ".git", zip_path, ROOT / "release_manifests" / f"{product.name}.json"]
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

    zip_scan = run(
        [
            sys.executable,
            str(ROOT / "tools" / "release" / "scan_secrets.py"),
            "--artifact",
            rel(zip_path),
            "--json",
            "--fail-on-findings",
        ],
        ROOT,
    )
    commands.append(zip_scan)

    gate_command, gate_payload = gate_decision(product.name, repo_full_name, zip_path, execute)
    commands.append(gate_command)
    remote_result = remote_check(remote, repo_full_name)
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
            "has_remote": bool(remote["stdout_tail"]),
            "remote_ok": remote_result,
            "zip_sha256": sha256_file(zip_path),
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
        and zip_scan["returncode"] == 0
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

    repo_url = f"https://github.com/{repo_full_name}.git"
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
                    product.notes[:350],
                ],
                staging,
            )
        )
    else:
        if not remote["stdout_tail"]:
            external_commands.append(run(["git", "remote", "add", "origin", repo_url], staging))
        external_commands.append(run(["git", "push", "-u", "origin", "main"], staging))
    external_commands.append(run(["gh", "repo", "view", repo_full_name, "--json", "nameWithOwner,url,isPrivate"], staging))
    row["external_commands"] = external_commands
    row["ok"] = external_commands[-1]["returncode"] == 0 and all(item["returncode"] == 0 for item in external_commands[1:])
    row["reason"] = "external publish verified" if row["ok"] else "external publish command failed"
    return row


def main() -> int:
    parser = argparse.ArgumentParser(description="Gated GitHub publisher for free-dev staging repos.")
    add_common_args(parser)
    parser.add_argument("--product", choices=[p.name for p in PRODUCTS if p.lane == "free-dev"], action="append")
    parser.add_argument("--owner", default=DEFAULT_OWNER)
    parser.add_argument("--execute", action="store_true", help="perform gh/git external commands only after ActionGate passes")
    parser.add_argument("--owner-override-with-evidence", action="store_true", help="allow explicit owner override only for host REVIEW after all local evidence passes")
    parser.add_argument("--override-operator", default="Luis Rene Gonzalez")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    validate_root_arg(args)

    selected = [product_by_name(name) for name in args.product] if args.product else [p for p in PRODUCTS if p.lane == "free-dev"]
    host = run([sys.executable, str(HOST_GATE)], CLAUDIO_ROOT)
    results = [
        preflight_product(
            product,
            args.owner,
            args.execute,
            args.owner_override_with_evidence,
            args.override_operator,
        )
        for product in selected
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
        out_dir = PUBLICATION_EVIDENCE_DIR
        out_dir.mkdir(parents=True, exist_ok=True)
        target = out_dir / ("free-dev-github-publish.json" if args.execute else "free-dev-github-dry-run.json")
        target.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        data["written"] = rel(target)
    if args.json:
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        for item in results:
            status = "ok" if item.get("ok") else "blocked"
            print(f"{item['product']}: {status} -> {item['repo']} ({item.get('reason', '')})")
        if args.write:
            print(f"wrote {data['written']}")
    return 0 if data["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
