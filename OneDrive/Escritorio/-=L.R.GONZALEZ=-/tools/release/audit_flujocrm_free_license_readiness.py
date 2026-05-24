from __future__ import annotations

import argparse
import json
from pathlib import Path

from _common import ROOT, ensure_under_root, rel


DEFAULT_TARGET = ROOT / "publish_staging" / "github" / "flujocrm-free-review"
DEFAULT_REPORT = (
    ROOT
    / "qa_artifacts"
    / "release_validation"
    / "flujocrm-free-license-readiness-2026-05-06.json"
)

TEXT_MARKERS = (
    "UNLICENSED",
    "private=true",
    '"private": true',
    "PROPRIETARY",
    "proprietary",
    "All rights reserved",
    "commercial app",
    "does not include the FlujoCRM source code",
)

REQUIRED_FILES = (
    "package.json",
    "package-lock.json",
    "README.md",
    "README_PUBLIC_DRAFT.md",
    "THIRD_PARTY_NOTICES.md",
    "LICENSE_DECISION_REQUIRED.md",
    "PUBLICATION_GATE.md",
    "SOURCE_ALLOWLIST_MANIFEST.json",
)


def read_json(path: Path) -> dict[str, object]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {"_error": str(exc)}
    return value if isinstance(value, dict) else {"_error": "json root is not object"}


def scan_text_markers(path: Path) -> list[dict[str, object]]:
    try:
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    except OSError as exc:
        return [{"line": 0, "marker": "read_error", "text": str(exc)}]
    hits: list[dict[str, object]] = []
    for number, line in enumerate(lines, start=1):
        for marker in TEXT_MARKERS:
            if marker in line:
                hits.append({"line": number, "marker": marker, "text": line.strip()[:180]})
    return hits


def audit(target: Path) -> dict[str, object]:
    target = ensure_under_root(target)
    missing = [name for name in REQUIRED_FILES if not (target / name).is_file()]
    package = read_json(target / "package.json") if (target / "package.json").exists() else {}
    lock = read_json(target / "package-lock.json") if (target / "package-lock.json").exists() else {}
    marker_hits: dict[str, list[dict[str, object]]] = {}
    for path in sorted(target.rglob("*")):
        if not path.is_file() or ".git" in path.parts:
            continue
        if path.suffix.lower() not in {".md", ".json"}:
            continue
        hits = scan_text_markers(path)
        if hits:
            marker_hits[path.relative_to(target).as_posix()] = hits

    blockers: list[str] = []
    if missing:
        blockers.append("missing_required_files")
    if package.get("license") in {None, "", "UNLICENSED"}:
        blockers.append("package_license_not_free")
    if package.get("private") is True:
        blockers.append("package_private_true")
    lock_packages = lock.get("packages") if isinstance(lock, dict) else {}
    if isinstance(lock_packages, dict):
        root_lock = lock_packages.get("")
        if isinstance(root_lock, dict) and root_lock.get("license") in {None, "", "UNLICENSED"}:
            blockers.append("package_lock_root_license_not_free")
    if marker_hits:
        blockers.append("proprietary_markers_present")

    return {
        "schema": "medioevo.flujocrm_free_license_readiness.v1",
        "target": rel(target),
        "publication_ready": not blockers,
        "blockers": sorted(set(blockers)),
        "missing_required_files": missing,
        "package_state": {
            "name": package.get("name"),
            "version": package.get("version"),
            "license": package.get("license"),
            "private": package.get("private"),
        },
        "marker_hits": marker_hits,
        "required_decision": "license_change_review_required" if blockers else "none",
        "recommended_next_step": (
            "Choose MIT, Apache-2.0, AGPL-3.0, source-available/freeware or dual license before editing staging metadata."
            if blockers
            else "Run final ActionGate before external publication."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit FlujoCRM free GitHub staging license readiness.")
    parser.add_argument("--target", default=str(DEFAULT_TARGET), help="staging target under workspace root")
    parser.add_argument("--write", action="store_true", help="write JSON report")
    parser.add_argument("--json", action="store_true", help="print JSON report")
    args = parser.parse_args()
    report = audit(Path(args.target))
    if args.write:
        DEFAULT_REPORT.parent.mkdir(parents=True, exist_ok=True)
        DEFAULT_REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=True), encoding="utf-8")
        report["written"] = rel(DEFAULT_REPORT)
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=True))
    else:
        state = "READY" if report["publication_ready"] else "BLOCKED"
        print(f"flujocrm_free_license_readiness={state} blockers={','.join(report['blockers'])}")
        if args.write:
            print(f"wrote {report['written']}")
    return 0 if report["publication_ready"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
