from __future__ import annotations

import argparse
import json
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from _common import ROOT, print_json


TODAY = "2026-05-06"
SCHEMA = "medioevo.one_universe.unifier.v1"

CANON_ROUTES = {
    "control": [
        ".gitignore",
        "AGENTS.md",
        "README.md",
        "AUDIT_REPO_TREE.md",
        "TREE_PLAN.md",
        "MIGRATION_MAP.md",
        "DELETE_CANDIDATES.md",
        "DELETED_OR_ARCHIVED.md",
        "SOURCE_INTAKE_REGISTER.md",
    ],
    "github_ci": [".github/"],
    "comms": ["COMMS/"],
    "docs": ["docs/"],
    "runtime_state": ["runtime/"],
    "qa_evidence": ["qa_artifacts/", "release_manifests/"],
    "apps": ["apps/"],
    "packages": ["packages/"],
    "books": ["books/"],
    "research": ["research/"],
    "website": ["website/"],
    "tools": ["tools/"],
    "tests": ["tests/"],
    "licenses": ["LICENSES/"],
    "hackathons": ["hackathons/"],
    "publish_staging": ["publish_staging/"],
    "products_staging": ["PRODUCTOS_MEDIOEVO/"],
    "medioevo_core": ["-=MEDIOEVO=-/"],
    "agent_sessions": [".claw/"],
    "private_game": ["game-private/", "-=MEDIOEVO=-/-=LIBROS/metaevo-tcg/", "-=MEDIOEVO=-/-=LIBROS/claudio/tcg/"],
    "archive": ["_archive/", "releases/"],
}

PRIVATE_MARKERS = [
    "game-private/",
    "metaevo-tcg",
    "/tcg/",
    "runtime/game_bridge",
    "04_AUDIOVISUAL_Y_TCG",
]

SECRET_MARKERS = [
    ".env",
    "secret",
    "token",
    "credential",
    "gumroad",
    "stripe",
    "jellyfin_auth",
]

GENERATED_MARKERS = [
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    ".mypy_cache",
    "node_modules",
    "/dist/",
    "/build/",
    "/target/",
]

VENDOR_MARKERS = [
    ".skills/",
    "tools/vendor",
    "tools/pentest_repos",
    "github-modules",
]

EXTERNAL_ACTION_MARKERS = [
    "publish_",
    "publicar_",
    "gumroad",
    "linkedin",
    "sponsors",
    "shopify",
    "stripe",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT.resolve())).replace("\\", "/")
    except ValueError:
        return str(path.resolve()).replace("\\", "/")


def run_git_status() -> list[dict[str, str]]:
    top_proc = subprocess.run(
        ["git", "-C", str(ROOT), "rev-parse", "--show-toplevel"],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    git_root = Path(top_proc.stdout.strip()).resolve() if top_proc.returncode == 0 and top_proc.stdout.strip() else ROOT
    try:
        root_prefix = str(ROOT.resolve().relative_to(git_root)).replace("\\", "/").rstrip("/") + "/"
    except ValueError:
        root_prefix = ""

    proc = subprocess.run(
        ["git", "-C", str(ROOT), "status", "--porcelain=v1", "--untracked-files=normal"],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if proc.returncode != 0:
        return [{"status": "!!", "path": "__GIT_STATUS_FAILED__", "raw": proc.stderr.strip()}]
    rows: list[dict[str, str]] = []
    for line in proc.stdout.splitlines():
        if not line:
            continue
        status = line[:2]
        path = line[3:] if len(line) > 3 else ""
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        path = path.replace("\\", "/")
        if root_prefix and path.startswith(root_prefix):
            path = path[len(root_prefix) :]
        rows.append({"status": status, "path": path, "raw": line})
    return rows


def first_route(path: str) -> tuple[str, str]:
    normalized = path.replace("\\", "/")
    for lane, prefixes in CANON_ROUTES.items():
        for prefix in prefixes:
            if normalized == prefix.rstrip("/") or normalized.startswith(prefix):
                return lane, prefix
    if "/" not in normalized:
        suffix = Path(normalized).suffix.lower()
        if suffix in {".md", ".txt", ".json", ".html"} or normalized in {"LICENSE", "SECURITY.md", "CONTRIBUTING.md"}:
            return "root_registers", "[root]"
        return "root_stray_review", "[root]"
    return "unknown_review", "[unmapped]"


def classify(path: str, status: str) -> dict[str, Any]:
    normalized = path.replace("\\", "/")
    lower = normalized.lower()
    lane, matched_prefix = first_route(normalized)
    flags: list[str] = []

    if lane == "agent_sessions":
        flags.append("agent_session_history")
    if any(marker.lower() in lower for marker in PRIVATE_MARKERS):
        flags.append("private_boundary")
    if any(marker.lower() in lower for marker in SECRET_MARKERS):
        flags.append("secret_or_credential_name")
    if any(marker.lower() in lower for marker in GENERATED_MARKERS):
        flags.append("generated_residue")
    if any(marker.lower() in lower for marker in VENDOR_MARKERS):
        flags.append("vendor_or_imported_tree")
    if any(marker.lower() in lower for marker in EXTERNAL_ACTION_MARKERS):
        flags.append("external_action_surface")
    if status.strip() == "??":
        flags.append("untracked")
    elif status.strip():
        flags.append("tracked_modified")

    if "agent_session_history" in flags:
        gate = "BLOCK"
        decision = "KEEP_LOCAL_AGENT_SESSION_HISTORY_NOT_MAIN_CANON"
    elif "private_boundary" in flags:
        gate = "BLOCK"
        decision = "KEEP_PRIVATE_BOUNDARY_NOT_PUBLIC_CANON"
    elif "secret_or_credential_name" in flags:
        gate = "BLOCK"
        decision = "BLOCK_SECRET_OR_ACCOUNT_SURFACE"
    elif "generated_residue" in flags:
        gate = "APPROVE"
        decision = "DELETE_OR_IGNORE_REGENERABLE_RESIDUE"
    elif "vendor_or_imported_tree" in flags:
        gate = "REVIEW"
        decision = "ARCHIVE_OR_REFERENCE_VENDOR_NOT_MAIN_UNIVERSE"
    elif lane == "unknown_review":
        gate = "REVIEW"
        decision = "ROUTE_TO_CANON_OR_ARCHIVE"
    elif lane == "medioevo_core":
        gate = "REVIEW"
        decision = "KEEP_AS_CORE_SOURCE_UNTIL_EXTRACTED_TO_ROOT_LANES"
    elif lane == "root_stray_review":
        gate = "REVIEW"
        decision = "ROOT_FILE_NEEDS_CANON_ROUTE_OR_DOC_INDEX"
    elif lane == "root_registers":
        gate = "REVIEW"
        decision = "KEEP_ROOT_REGISTER_UNTIL_MERGED_TO_DOCS_INDEX"
    else:
        gate = "REVIEW"
        decision = "KEEP_IN_CANON_LANE_WITH_STATUS_REVIEW"

    return {
        "path": normalized,
        "git_status": status,
        "lane": lane,
        "matched_prefix": matched_prefix,
        "action_gate": gate,
        "decision": decision,
        "flags": flags,
    }


def summarize_rows(rows: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "total_paths": len(rows),
        "by_lane": dict(Counter(str(row["lane"]) for row in rows)),
        "by_decision": dict(Counter(str(row["decision"]) for row in rows)),
        "by_gate": dict(Counter(str(row["action_gate"]) for row in rows)),
        "by_git_status": dict(Counter(str(row["git_status"]) for row in rows)),
        "flag_counts": dict(Counter(flag for row in rows for flag in row.get("flags", []))),
    }


def next_actions(summary: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "order": "1",
            "action": "Root control",
            "decision": "Mantener AGENTS, Atlas, MIGRATION_MAP, DELETE_CANDIDATES y reportes como sistema nervioso del universo.",
            "gate": "REVIEW",
        },
        {
            "order": "2",
            "action": "Regenerable residue",
            "decision": "Borrar o ignorar solo caches/builds regenerables con reporte; no borrar fuentes unicas.",
            "gate": "APPROVE if path-specific cache rule passes",
        },
        {
            "order": "3",
            "action": "MEDIOEVO core extraction",
            "decision": "No mover todo -=MEDIOEVO=- de golpe; extraer a root lanes solo piezas con ficha, hash y destino canonico.",
            "gate": "REVIEW",
        },
        {
            "order": "4",
            "action": "Private boundary",
            "decision": "Juego, TCG, sesiones, secretos y cuentas quedan bloqueados fuera de open/commercial.",
            "gate": "BLOCK",
        },
        {
            "order": "5",
            "action": "Vendor/imported trees",
            "decision": "Referenciar, archivar o excluir; no convertirlos en tecnologia principal salvo modulo minimo extraido.",
            "gate": "REVIEW",
        },
    ]


def build_payload() -> dict[str, Any]:
    git_rows = run_git_status()
    rows = [classify(row["path"], row["status"]) | {"raw": row.get("raw", "")} for row in git_rows]
    summary = summarize_rows(rows)
    return {
        "schema": SCHEMA,
        "generated_at_utc": utc_now(),
        "workspace_root": str(ROOT),
        "status": "MANIFEST_ONLY_NO_MOVE_NO_DELETE",
        "principle": "one universe, many lanes; one canonical map, no orphan trees",
        "canon_routes": CANON_ROUTES,
        "summary": summary,
        "rows": rows,
        "next_actions": next_actions(summary),
        "rules": [
            "One universe does not mean flattening every folder into one directory.",
            "A route is canon only when it has lane, purpose, gate, evidence and owner.",
            "Untracked agent output is production residue until integrated into a lane.",
            "Generated caches can be deleted by rule; unique sources move only with ficha and migration map.",
            "Private, secret-like and external-action surfaces never become public canon by accident.",
        ],
    }


def render_markdown(payload: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append("# One Universe Control - MEDIOEVO")
    lines.append("")
    lines.append(f"Generated UTC: `{payload['generated_at_utc']}`")
    lines.append("")
    lines.append("Principio: un solo universo, varios carriles. Nada queda huerfano; nada entra al canon sin ruta, gate y evidencia.")
    lines.append("")
    lines.append("## Resumen")
    lines.append("")
    lines.append("| metrica | valor |")
    lines.append("|---|---:|")
    for key, value in payload["summary"].items():
        if isinstance(value, dict):
            lines.append(f"| `{key}` | `{len(value)}` grupos |")
        else:
            lines.append(f"| `{key}` | {value} |")
    lines.append("")
    lines.append("## Gates")
    lines.append("")
    lines.append("| gate | rutas |")
    lines.append("|---|---:|")
    for gate, count in sorted(payload["summary"]["by_gate"].items()):
        lines.append(f"| `{gate}` | {count} |")
    lines.append("")
    lines.append("## Carriles Canonicos")
    lines.append("")
    lines.append("| carril | prefijos |")
    lines.append("|---|---|")
    for lane, prefixes in payload["canon_routes"].items():
        lines.append(f"| `{lane}` | `{', '.join(prefixes)}` |")
    lines.append("")
    lines.append("## Decisiones Por Carril")
    lines.append("")
    lines.append("| carril | rutas |")
    lines.append("|---|---:|")
    for lane, count in sorted(payload["summary"]["by_lane"].items()):
        lines.append(f"| `{lane}` | {count} |")
    lines.append("")
    lines.append("## Acciones Siguientes")
    lines.append("")
    lines.append("| orden | accion | gate | decision |")
    lines.append("|---:|---|---|---|")
    for item in payload["next_actions"]:
        lines.append(f"| {item['order']} | {item['action']} | `{item['gate']}` | {item['decision']} |")
    lines.append("")
    lines.append("## Muestra De Rutas")
    lines.append("")
    lines.append("| git | gate | carril | decision | ruta |")
    lines.append("|---|---|---|---|---|")
    for row in payload["rows"][:160]:
        lines.append(
            f"| `{row['git_status']}` | `{row['action_gate']}` | `{row['lane']}` | `{row['decision']}` | `{row['path']}` |"
        )
    lines.append("")
    lines.append("## Reglas")
    lines.append("")
    for rule in payload["rules"]:
        lines.append(f"- {rule}")
    lines.append("")
    return "\n".join(lines)


def write_outputs(payload: dict[str, Any], json_out: Path, report_out: Path) -> None:
    json_out.parent.mkdir(parents=True, exist_ok=True)
    report_out.parent.mkdir(parents=True, exist_ok=True)
    json_out.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    report_out.write_text(render_markdown(payload), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build one-universe routing manifest for MEDIOEVO workspace.")
    parser.add_argument("--json-out", default=f"qa_artifacts/release_validation/one-universe-manifest-{TODAY}.json")
    parser.add_argument("--report-out", default=f"docs/intake/ONE_UNIVERSE_CONTROL_{TODAY}.md")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    payload = build_payload()
    write_outputs(payload, ROOT / args.json_out, ROOT / args.report_out)

    if args.json:
        print_json(
            {
                "schema": payload["schema"],
                "status": payload["status"],
                "summary": payload["summary"],
                "json_out": args.json_out,
                "report_out": args.report_out,
            }
        )
    else:
        print(f"status={payload['status']}")
        print(f"paths={payload['summary']['total_paths']}")
        print(f"json={args.json_out}")
        print(f"report={args.report_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
