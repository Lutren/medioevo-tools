from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

from _common import ROOT, ensure_under_root, rel


SOURCE = ROOT / "apps" / "commercial" / "flujocrm"
TARGET = ROOT / "publish_staging" / "github" / "flujocrm-free-review"
REPORT = ROOT / "qa_artifacts" / "release_validation" / "flujocrm-free-github-review-staging-2026-05-06.json"

ALLOWLIST = (
    ".gitignore",
    "README.md",
    "BUSINESS.md",
    "CUSTOMER_INSTALL_NOTES.md",
    "THIRD_PARTY_NOTICES.md",
    "index.html",
    "main.js",
    "mockup.html",
    "preload.js",
    "package.json",
    "package-lock.json",
    "assets/README.md",
    "scripts/smoke-main.cjs",
    "scripts/smoke-preload.cjs",
    "scripts/smoke-renderer.cjs",
    "scripts/e2e-storage-smoke.cjs",
)

DENY_MARKERS = (
    "dist",
    "node_modules",
    ".env",
    "secret",
    "token",
    "credential",
    "gumroad",
    "stripe",
    ".wrangler",
    ".claw",
    ".claude",
)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def run(command: list[str], cwd: Path) -> dict[str, object]:
    result = subprocess.run(command, cwd=cwd, text=True, capture_output=True)
    return {
        "command": command,
        "cwd": rel(cwd),
        "returncode": result.returncode,
        "stdout_tail": result.stdout.splitlines()[-12:],
        "stderr_tail": result.stderr.splitlines()[-12:],
    }


def blocked_name(relative: str) -> str | None:
    value = relative.replace("\\", "/").lower()
    parts = value.split("/")
    for marker in DENY_MARKERS:
        if marker in parts or marker in value:
            return marker
    return None


def copy_allowlist(target: Path) -> list[dict[str, object]]:
    copied: list[dict[str, object]] = []
    for relative in ALLOWLIST:
        reason = blocked_name(relative)
        if reason:
            raise RuntimeError(f"blocked allowlist entry {relative}: {reason}")
        source = ensure_under_root(SOURCE / relative)
        if not source.exists():
            raise FileNotFoundError(source)
        destination = ensure_under_root(target / relative)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        copied.append(
            {
                "path": relative,
                "bytes": destination.stat().st_size,
                "sha256": sha256_file(destination),
            }
        )
    return copied


def write_review_docs(target: Path, copied: list[dict[str, object]]) -> list[dict[str, object]]:
    docs = {
        "PUBLICATION_GATE.md": """# FlujoCRM Free GitHub Review Gate

Status: `STAGING_LOCAL_REVIEW_ONLY`

This folder is a local review candidate for the owner's direction to make
FlujoCRM free on GitHub. It is not a public release and must not be pushed until
the gates below pass.

## Required Before GitHub

- License decision for the free source release.
- `package.json` license/private fields updated only after that decision.
- Source secret scan reports `count_reported=0`.
- Path scrub confirms no local/private paths.
- Claims copy stays local-first and low-claim.
- No `dist`, `node_modules`, installers, runtime databases, secrets, Gumroad,
  Stripe, private game/TCG, book vault or account state.
- ActionGate target `github-flujocrm-free-release` allows publication.

## Current License Truth

The active product is still proprietary in `apps/commercial/flujocrm`.
This candidate intentionally preserves that blocker instead of pretending the
license has already changed.
""",
        "README_PUBLIC_DRAFT.md": """# FlujoCRM

FlujoCRM is a local-first CRM candidate for freelancers, small teams and
operators who want contacts, pipeline stages and follow-up notes without a
hosted SaaS account.

This draft is prepared for a future free GitHub lane after license review,
clean staging and QA. Support, setup help, templates and polished installers may
remain paid services around the free source.

## Scope

- Local contact management.
- Simple pipeline stages.
- Follow-up notes and activity history.
- Electron desktop shell.
- SQLite storage in installed builds.
- Browser localStorage fallback for standalone preview.

## Boundaries

- No cloud service claim.
- No team sync claim.
- No compliance, legal or revenue guarantees.
- No private MEDIOEVO runtime, books, RPG/TCG material, credentials or account
  state.
""",
        "LICENSE_DECISION_REQUIRED.md": """# License Decision Required

The owner requested a free GitHub direction for FlujoCRM. The active product is
currently `UNLICENSED`, `private=true` and covered by a proprietary commercial
license.

Do not push or publish this staging folder until one option is chosen and
recorded:

| option | effect | tradeoff |
|---|---|---|
| MIT | simple permissive open source | competitors can reuse commercially |
| Apache-2.0 | permissive plus patent terms | slightly heavier text |
| AGPL-3.0 | forces network-service source sharing | higher adoption friction |
| Source-available/freeware | free access without OSI open source | less open-source trust |
| Dual license | free core plus paid commercial/support lane | needs clearer legal docs |

Until this is decided, the staging state is `LEGAL_REVIEW_REQUIRED`.
""",
    }
    written: list[dict[str, object]] = []
    manifest = {
        "schema": "medioevo.flujocrm_free_review_manifest.v1",
        "status": "STAGING_LOCAL_REVIEW_ONLY",
        "source": rel(SOURCE),
        "file_count": len(copied),
        "files": copied,
        "blocked_external_publication": True,
        "license_state": "LEGAL_REVIEW_REQUIRED",
    }
    docs["SOURCE_ALLOWLIST_MANIFEST.json"] = json.dumps(manifest, indent=2, ensure_ascii=True) + "\n"
    for name, content in docs.items():
        path = ensure_under_root(target / name)
        path.write_text(content, encoding="utf-8")
        written.append({"path": name, "bytes": path.stat().st_size, "sha256": sha256_file(path)})
    return written


def iter_staged_files(target: Path) -> list[dict[str, object]]:
    files: list[dict[str, object]] = []
    for path in sorted(target.rglob("*")):
        if not path.is_file() or ".git" in path.parts:
            continue
        relative = path.relative_to(target).as_posix()
        files.append({"path": relative, "bytes": path.stat().st_size, "sha256": sha256_file(path)})
    return files


def staging_license_state(target: Path) -> dict[str, object]:
    package_path = target / "package.json"
    state: dict[str, object] = {"license": None, "private": None, "ready": False}
    try:
        package = json.loads(package_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        state["error"] = str(exc)
        return state
    if isinstance(package, dict):
        state["license"] = package.get("license")
        state["private"] = package.get("private")
        state["ready"] = package.get("license") == "MIT" and package.get("private") is False
    return state


def publication_blockers_for_existing(target: Path) -> list[str]:
    blockers = ["host_actiongate_block", "external_actiongate_required"]
    license_state = staging_license_state(target)
    if not license_state.get("ready"):
        blockers.append("license_decision_required")
    return blockers


def verify_existing(target: Path, args: argparse.Namespace) -> dict[str, object]:
    ensure_under_root(target)
    if not target.exists():
        raise SystemExit(f"target does not exist: {target}")
    commands = [
        run(["git", "status", "--short"], target),
        run(["git", "log", "--oneline", "-1"], target),
        run(["git", "remote", "-v"], target),
        run(["git", "diff", "--check"], target),
    ]
    status = commands[0]
    report = {
        "ok": all(item["returncode"] == 0 for item in commands) and not status["stdout_tail"],
        "target": rel(target),
        "source": rel(SOURCE),
        "files": iter_staged_files(target),
        "commands": commands,
        "license_state": staging_license_state(target),
        "publication_allowed": False,
        "publication_blockers": publication_blockers_for_existing(target),
    }
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=True), encoding="utf-8")
        report["written"] = rel(REPORT)
    return report


def build(args: argparse.Namespace) -> dict[str, object]:
    ensure_under_root(SOURCE)
    target = ensure_under_root(Path(args.target) if args.target else TARGET)
    if args.verify_existing:
        return verify_existing(target, args)
    if target.exists() and any(target.iterdir()):
        raise SystemExit(f"target exists and is not empty: {target}")
    target.mkdir(parents=True, exist_ok=True)
    copied = copy_allowlist(target)
    generated = write_review_docs(target, copied)
    commands = [
        run(["git", "init", "-b", "main"], target),
        run(["git", "config", "user.name", "L.R. Gonzalez"], target),
        run(["git", "config", "user.email", "lutren@users.noreply.github.com"], target),
        run(["git", "add", "--", "."], target),
        run(["git", "diff", "--cached", "--check"], target),
    ]
    if all(item["returncode"] == 0 for item in commands):
        commands.append(run(["git", "commit", "-m", "Initial FlujoCRM free GitHub review staging"], target))
    status = run(["git", "status", "--short"], target)
    commands.append(status)
    report = {
        "ok": all(item["returncode"] == 0 for item in commands) and not status["stdout_tail"],
        "target": rel(target),
        "source": rel(SOURCE),
        "copied": copied,
        "generated": generated,
        "commands": commands,
        "publication_allowed": False,
        "publication_blockers": [
            "host_actiongate_block",
            "license_decision_required",
            "post_staging_secret_scan_required",
            "path_scrub_required",
            "human_or_owner_release_gate_required",
        ],
    }
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=True), encoding="utf-8")
        report["written"] = rel(REPORT)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Stage a local FlujoCRM free-GitHub review candidate.")
    parser.add_argument("--target", default="", help="optional target under workspace root")
    parser.add_argument("--verify-existing", action="store_true", help="verify an existing staging folder instead of creating it")
    parser.add_argument("--write", action="store_true", help="write qa report")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = build(args)
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=True))
    else:
        print(f"staged {report['target']} files={len(report['copied'])} generated={len(report['generated'])}")
        if report.get("written"):
            print(f"wrote {report['written']}")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
