from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

KEEP_ROOT_DIRS = {
    "apps",
    "core",
    "tests",
    "tools",
    "docs",
    "runtime",
    "reports",
    "website",
    "products",
    "data",
    "datasets",
    "schemas",
    "library",
    "fixtures",
}

PRIVATE_DIRS = {
    "-=PSI=-",
    "tcg",
    "vault_medioevo",
    "memory_vault",
    "fine_tuned_models",
    "training_datasets",
    "gguf_exports",
}

CACHE_DIRS = {
    "__pycache__",
    ".pytest_cache",
    ".test_research",
    ".test_research_storage",
    ".test_session_storage",
    ".test_sessions",
    "cache",
    "camera_frames",
    "logs",
    "screenshots",
    "_ui_uploads",
}

ARCHIVE_DIRS = {
    "_ARCHIVAR",
    "_archivo_sesiones",
    "_legacy",
    "_local_quarantine",
    "archive",
    "archivo",
}

CONFIG_DIRS = {".agents", ".claude", ".claudio", ".claw", ".skills", ".wrangler", ".venv_api"}

SECRET_MARKERS = ("secret", "token", "credential", "gumroad", ".env", "jellyfin_auth")
LAUNCH_SUFFIXES = {".bat", ".ps1", ".vbs", ".rdp", ".lnk", ".cmd", ".sh"}
DOC_SUFFIXES = {".md", ".txt"}
DATA_SUFFIXES = {".json", ".csv", ".yaml", ".yml"}
DB_SUFFIXES = {".db", ".sqlite"}
MEDIA_SUFFIXES = {".png", ".ico", ".html"}


@dataclass
class RootItem:
    name: str
    kind: str
    size_bytes: int
    category: str
    decision: str
    destination_hint: str
    risk: str
    reason: str


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def classify_item(path: Path) -> tuple[str, str, str, str, str]:
    name = path.name
    lower = name.lower()
    suffix = path.suffix.lower()
    is_dir = path.is_dir()

    if ".git" == name:
        return "git_control", "KEEP", ".git", "HIGH", "repo_control"
    if is_dir and name in KEEP_ROOT_DIRS:
        return "runtime_core_root", "KEEP", name, "LOW", "strong_runtime_route"
    if is_dir and name in PRIVATE_DIRS:
        return "private_blocked", "KEEP_PRIVATE_REVIEW", f"private/{name}", "HIGH", "private_runtime_or_models"
    if is_dir and name in CACHE_DIRS:
        return "cache_regenerable", "CANDIDATE_DELETE_AFTER_GATE", "runtime/cache_or_artifacts", "MEDIUM", "cache_or_generated_runtime"
    if is_dir and name in ARCHIVE_DIRS:
        return "archive_existing", "KEEP_REVIEW_CONSOLIDATE", "runtime/archivo_frio", "MEDIUM", "existing_archive"
    if is_dir and name in CONFIG_DIRS:
        return "local_config_tooling", "KEEP_REVIEW", name, "MEDIUM", "local_tool_config"
    if any(marker in lower for marker in SECRET_MARKERS) or suffix in {".env", ".gumroad"}:
        return "secret_or_sensitive", "BLOCK_MOVE_TO_PRIVATE_CONFIG", "runtime/private_config", "HIGH", "secret_marker"
    if suffix in DB_SUFFIXES:
        return "local_state_db", "KEEP_REVIEW_RETENTION", "runtime/state", "HIGH", "local_state_database"
    if suffix in LAUNCH_SUFFIXES:
        return "launcher_script", "MOVE_CANDIDATE", "tools/launchers", "MEDIUM", "root_launcher_noise"
    if suffix == ".py":
        return "root_python_script", "MOVE_CANDIDATE", "tools/root_scripts_review", "MEDIUM", "root_python_noise"
    if suffix in DOC_SUFFIXES:
        return "root_document", "MOVE_CANDIDATE", "docs/root_notes_review", "LOW", "root_doc_noise"
    if suffix in MEDIA_SUFFIXES:
        return "root_media_or_ui", "MOVE_CANDIDATE", "assets/root_media_review", "LOW", "root_asset_noise"
    if suffix in DATA_SUFFIXES:
        return "root_data_config", "MOVE_CANDIDATE_REVIEW", "data/root_config_review", "MEDIUM", "root_data_noise"
    if is_dir:
        return "domain_module_or_legacy_dir", "REVIEW_DESTINATION", "docs/intake/claudio_root_review", "MEDIUM", "noncanonical_root_dir"
    return "misc_root_item", "REVIEW", "docs/intake/claudio_root_review", "MEDIUM", "fallback"


def get_git_status(root: Path) -> list[str]:
    try:
        result = subprocess.run(
            ["git", "status", "--short"],
            cwd=root,
            text=True,
            encoding="utf-8",
            errors="replace",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            timeout=60,
        )
    except Exception:
        return []
    if result.returncode != 0:
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def build_audit(target_root: Path) -> dict[str, object]:
    records: list[RootItem] = []
    for item in sorted(target_root.iterdir(), key=lambda entry: entry.name.lower()):
        try:
            size = item.stat().st_size if item.is_file() else 0
        except OSError:
            size = 0
        category, decision, destination, risk, reason = classify_item(item)
        records.append(
            RootItem(
                name=item.name,
                kind="directory" if item.is_dir() else "file",
                size_bytes=size,
                category=category,
                decision=decision,
                destination_hint=destination,
                risk=risk,
                reason=reason,
            )
        )

    git_status = get_git_status(target_root)
    category_counts: dict[str, int] = {}
    decision_counts: dict[str, int] = {}
    risk_counts: dict[str, int] = {}
    for record in records:
        category_counts[record.category] = category_counts.get(record.category, 0) + 1
        decision_counts[record.decision] = decision_counts.get(record.decision, 0) + 1
        risk_counts[record.risk] = risk_counts.get(record.risk, 0) + 1

    return {
        "schema": "medioevo.claudio_root_human_audit.v1",
        "generated_at_utc": utc_now(),
        "target_root": str(target_root),
        "summary": {
            "root_items": len(records),
            "root_files": sum(1 for record in records if record.kind == "file"),
            "root_directories": sum(1 for record in records if record.kind == "directory"),
            "git_pending_lines": len(git_status),
            "categories": dict(sorted(category_counts.items())),
            "decisions": dict(sorted(decision_counts.items())),
            "risks": dict(sorted(risk_counts.items())),
        },
        "records": [asdict(record) for record in records],
        "git_status_sample": git_status[:250],
    }


def render_audit(payload: dict[str, object]) -> str:
    summary = payload["summary"]  # type: ignore[assignment]
    records = payload["records"]  # type: ignore[assignment]
    lines = [
        "# Claudio Root Human Audit - 2026-05-06",
        "",
        f"Generated UTC: `{payload['generated_at_utc']}`",
        f"Target: `{payload['target_root']}`",
        "",
        "## Summary",
        "",
        f"- Root items: `{summary['root_items']}`",
        f"- Root files: `{summary['root_files']}`",
        f"- Root directories: `{summary['root_directories']}`",
        f"- Git pending lines: `{summary['git_pending_lines']}`",
        "",
        "## Category Counts",
        "",
        "| category | count |",
        "|---|---:|",
    ]
    for category, count in summary["categories"].items():  # type: ignore[index,union-attr]
        lines.append(f"| `{category}` | {count} |")
    lines.extend(
        [
            "",
            "## Human Diagnosis",
            "",
            "- The root is not human-clean: runtime, docs, launchers, local secrets, device scripts, product scripts and legacy files share one visible level.",
            "- This audit did not move or delete files.",
            "- Immediate safe work is documentation and staged manifests, not broad cleanup.",
            "- Physical moves should be batched by category with rollback manifests.",
            "",
            "## High-Risk Visible Items",
            "",
            "| name | category | decision | risk | destination hint |",
            "|---|---|---|---|---|",
        ]
    )
    for record in records:  # type: ignore[assignment]
        if record["risk"] == "HIGH":
            lines.append(
                f"| `{record['name']}` | `{record['category']}` | `{record['decision']}` | "
                f"`{record['risk']}` | `{record['destination_hint']}` |"
            )
    lines.extend(
        [
            "",
            "## Root Items",
            "",
            "| name | kind | category | decision | destination hint | reason |",
            "|---|---|---|---|---|---|",
        ]
    )
    for record in records:  # type: ignore[assignment]
        lines.append(
            f"| `{record['name']}` | `{record['kind']}` | `{record['category']}` | "
            f"`{record['decision']}` | `{record['destination_hint']}` | `{record['reason']}` |"
        )
    return "\n".join(lines) + "\n"


def render_plan(payload: dict[str, object]) -> str:
    summary = payload["summary"]  # type: ignore[assignment]
    lines = [
        "# Claudio Root Human Migration Plan - 2026-05-06",
        "",
        "Status: `DRY_RUN_NO_MOVES`",
        "",
        "## Objective",
        "",
        "Make Claudio navigable for humans without breaking the runtime or trampling concurrent agent work.",
        "",
        "## Proposed Root Contract",
        "",
        "Keep visible at root only:",
        "",
        "- `00_LEER_PRIMERO.md` or equivalent root README.",
        "- `apps/`, `core/`, `tests/`, `tools/`, `docs/`, `runtime/`, `reports/`.",
        "- `website/`, `products/`, `data/`, `datasets/` when actively used.",
        "- Required repo control files.",
        "",
        "Everything else gets a category-specific move plan before any physical action.",
        "",
        "## Batches",
        "",
        "| order | batch | action | gate |",
        "|---:|---|---|---|",
        "| 1 | secrets and local config | move to private config lane or keep blocked | `BLOCK/REVIEW` |",
        "| 2 | launchers | move to `tools/launchers` with README | `REVIEW` |",
        "| 3 | root docs | move to `docs/root_notes_review` or canon docs | `REVIEW` |",
        "| 4 | root python scripts | move to `tools/root_scripts_review` then classify owners | `REVIEW` |",
        "| 5 | caches/generated | delete only if regenerable and logged | `APPROVE` |",
        "| 6 | legacy/archive dirs | consolidate into one archivo frio lane | `REVIEW` |",
        "",
        "## Current Counts",
        "",
        f"- Root items: `{summary['root_items']}`",
        f"- Root files: `{summary['root_files']}`",
        f"- Root directories: `{summary['root_directories']}`",
        f"- Git pending lines: `{summary['git_pending_lines']}`",
        "",
        "## No-Go",
        "",
        "- Do not delete `.env`, tokens, databases, model files, private RPG/TCG or PSI sources.",
        "- Do not broad-stage the nested repo.",
        "- Do not move files touched by other agents without a rollback manifest.",
        "- Do not publish or deploy from this cleanup pass.",
        "",
        "## Next Safe Command",
        "",
        "Create a move-manifest for one batch at a time, starting with launchers or root docs. Do not start with secrets or runtime code.",
    ]
    return "\n".join(lines) + "\n"


def write_outputs(payload: dict[str, object], output_dir: Path) -> dict[str, str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest = output_dir / "CLAUDIO_ROOT_HUMAN_MANIFEST_2026-05-06.json"
    audit = output_dir / "CLAUDIO_ROOT_HUMAN_AUDIT_2026-05-06.md"
    plan = output_dir / "CLAUDIO_ROOT_HUMAN_MIGRATION_PLAN_2026-05-06.md"
    manifest.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    audit.write_text(render_audit(payload), encoding="utf-8")
    plan.write_text(render_plan(payload), encoding="utf-8")
    return {"manifest": str(manifest), "audit": str(audit), "plan": str(plan)}


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Dry-run human audit for the Claudio root folder.")
    parser.add_argument("--target-root", required=True)
    parser.add_argument("--output-dir", default=str(ROOT / "docs" / "intake"))
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    args = parse_args(argv)
    payload = build_audit(Path(args.target_root).resolve())
    result = {"summary": payload["summary"], "paths": {}}
    if args.write:
        result["paths"] = write_outputs(payload, Path(args.output_dir).resolve())
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(json.dumps(result["summary"], indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
