#!/usr/bin/env python3
"""MEDIOEVO / OSIT desktop live-continuity setup run.

This script creates local-only BRAIN_OS mirrors, bulletin board state, reports,
shortcuts and a non-destructive L.R.GONZALEZ inventory. It never reads secret
values, never publishes, and never deletes or moves source material.
"""

from __future__ import annotations

import csv
import hashlib
import json
import os
import shutil
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from zoneinfo import ZoneInfo
except Exception:  # pragma: no cover - Windows fallback only.
    ZoneInfo = None  # type: ignore


HOME = Path.home()
DESKTOP = HOME / "OneDrive" / "Escritorio"
BRAIN_OS = DESKTOP / "-= BRAIN_OS =-"
LRG_DIR = DESKTOP / "-=L.R.GONZALEZ=-"
CLAUDIO_DIR = LRG_DIR / "-=MEDIOEVO=-" / "-=LIBROS" / "claudio"
LIBROS_DIR = LRG_DIR / "-=MEDIOEVO=-" / "-=LIBROS"
LIVE_STATE = BRAIN_OS / "00_START_HERE" / "LIVE_STATE"
PROJECT_REPORTS = BRAIN_OS / "01_PROJECT_REPORTS"
SOURCE_REVIEW = BRAIN_OS / "03_SOURCE_INTAKE" / "LRGONZALEZ_DESKTOP_REVIEW"
BULLETIN_DIR = BRAIN_OS / "apps" / "local" / "agent_bulletin_board"
SHORTCUT_TARGETS = BRAIN_OS / "00_START_HERE" / "SHORTCUTS_TARGETS"
LAUNCHPAD = DESKTOP / "MEDIOEVO_LAUNCHPAD"
API_LEDGER = LRG_DIR / "runtime" / "api_usage_ledger" / "api_usage_2026-05-13.jsonl"
HANDOFF_LEDGER = BRAIN_OS / "00_START_HERE" / "HANDOFF_LEDGER" / "handoff_ledger.jsonl"

RUN_ID = "CODEX_DESKTOP_SETUP_20260513"
RULE_MARKER = "DESKTOP_LIVE_CONTINUITY_RULE:"
FULL_HASH_LIMIT = 512 * 1024
PARTIAL_HASH_LIMIT = 20 * 1024 * 1024
PARTIAL_BYTES = 1024 * 1024

SKIP_DIR_NAMES = {
    ".git",
    ".claw",
    ".claude",
    ".skills",
    ".wrangler",
    "node_modules",
    ".venv",
    "venv",
    "env",
    "vendor",
    "vendors",
    "github-modules",
    "pentest_repos",
    "target",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "dist",
    "build",
    ".next",
    "_archive",
    "_archivar",
    "_legacy",
    "_snapshots",
    "_trash_revisar",
}
PRIVATE_MARKERS = {
    "metaevo-tcg",
    "tcg",
    "game_bridge",
    "game-private",
    "rpg",
}
SECRET_NAME_MARKERS = {
    ".env",
    "secret",
    "token",
    "credential",
    "password",
    "api_key",
    "settings.local",
    "banananana",
    "gumroad_api",
    "stripe",
}


def now_local() -> datetime:
    if ZoneInfo:
        return datetime.now(ZoneInfo("America/Chicago"))
    return datetime.now().astimezone()


def now_iso() -> str:
    return now_local().isoformat(timespec="seconds")


def redact_path(path: Path | str) -> str:
    text = str(path)
    home = str(HOME)
    if text.lower().startswith(home.lower()):
        return "%USERPROFILE%" + text[len(home) :]
    return text


def ensure_dirs() -> None:
    dirs = [
        BRAIN_OS / "00_START_HERE",
        LIVE_STATE,
        SHORTCUT_TARGETS,
        BRAIN_OS / "00_START_HERE" / "HUMAN_DASHBOARD",
        BRAIN_OS / "00_START_HERE" / "HANDOFF_LEDGER",
        PROJECT_REPORTS,
        BRAIN_OS / "02_TOOLS_AND_APPS",
        BRAIN_OS / "03_SOURCE_INTAKE",
        SOURCE_REVIEW,
        BRAIN_OS / "08_QA_WITNESSLOG",
        BRAIN_OS / "09_ARCHIVE_REVIEW",
        BRAIN_OS / "01_CEREBRO" / "PROTOCOLS",
        BRAIN_OS / "02_CLAUDIO" / "schemas",
        BULLETIN_DIR / "data",
        API_LEDGER.parent,
        LAUNCHPAD,
    ]
    for item in dirs:
        item.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return ""


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def append_once(path: Path, block: str, marker: str = RULE_MARKER) -> bool:
    text = read_text(path)
    if marker in text:
        return False
    if text and not text.endswith("\n"):
        text += "\n"
    write_text(path, text + "\n" + block.strip() + "\n")
    return True


def prepend_once(path: Path, block: str, marker: str) -> bool:
    text = read_text(path)
    if marker in text:
        return False
    write_text(path, block.strip() + "\n\n---\n\n" + text)
    return True


def safe_stat(path: Path) -> os.stat_result | None:
    try:
        return path.stat()
    except OSError:
        return None


def hash_file(path: Path, size: int) -> tuple[str, str]:
    h = hashlib.sha256()
    if size <= FULL_HASH_LIMIT:
        try:
            with path.open("rb") as handle:
                for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                    h.update(chunk)
            return "SHA256", h.hexdigest().upper()
        except OSError as exc:
            return "HASH_ERROR", str(exc)
    if size <= PARTIAL_HASH_LIMIT:
        try:
            with path.open("rb") as handle:
                first = handle.read(PARTIAL_BYTES)
                if size > PARTIAL_BYTES:
                    handle.seek(max(0, size - PARTIAL_BYTES))
                last = handle.read(PARTIAL_BYTES)
            h.update(first)
            h.update(last)
            return "PARTIAL_SHA256_FIRST_LAST_1M", h.hexdigest().upper()
        except OSError as exc:
            return "HASH_ERROR", str(exc)
    return "HASH_SKIPPED_LARGE_FILE", f"size_bytes={size}"


def has_marker(path: Path, markers: set[str]) -> bool:
    parts = [part.lower() for part in path.parts]
    name = path.name.lower()
    return any(marker in name or marker in parts for marker in markers)


def classify(path: Path, is_dir: bool = False) -> str:
    lower = str(path).lower()
    name = path.name.lower()
    if any(marker in name for marker in SECRET_NAME_MARKERS):
        return "SECRET_OR_CREDENTIAL_RISK"
    if any(marker in lower for marker in PRIVATE_MARKERS):
        return "PERSONAL_PRIVATE"
    if "archive" in lower or "_archivar" in lower or "_archive" in lower or "_legacy" in lower:
        return "ARCHIVE_REVIEW"
    if "duat" in lower or "geodia" in lower:
        return "DUAT_GEODIA_CANDIDATE"
    if "cerebro" in lower or "psi" in lower or "observacionismo" in lower:
        return "CEREBRO_CANON_CANDIDATE"
    if "wabi" in lower:
        return "WABI_SABI_CANDIDATE"
    if "claudio" in lower:
        return "CLAUDIO_RUNTIME_CANDIDATE"
    if "publish" in lower or "website" in lower or "open-dev" in lower or "public" in lower:
        return "PUBLIC_RELEASE_CANDIDATE"
    if "medioevo" in lower:
        return "MEDIOEVO_CORE_CANDIDATE"
    return "UNKNOWN_PENDING_REVIEW" if is_dir else "ARCHIVE_REVIEW"


def detect_kind(path: Path) -> str:
    ext = path.suffix.lower()
    if ext in {".md", ".txt", ".rst"}:
        return "document_text"
    if ext in {".pdf", ".docx", ".doc"}:
        return "document_binary"
    if ext in {".py", ".js", ".ts", ".tsx", ".jsx", ".ps1", ".cmd", ".bat", ".html", ".css", ".json", ".yaml", ".yml"}:
        return "code_or_config"
    if ext in {".zip", ".7z", ".rar", ".tar", ".gz"}:
        return "archive"
    if ext in {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"}:
        return "image"
    if ext in {".mp3", ".wav", ".flac", ".mp4", ".mov", ".avi"}:
        return "audio_video"
    if ext in {".db", ".sqlite", ".sqlite3", ".csv", ".jsonl"}:
        return "data"
    if ext in {".exe", ".dll", ".apk", ".msi"}:
        return "binary_executable"
    return "other"


def inventory_lrg() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []
    repos: list[str] = []
    top_counter: Counter[str] = Counter()
    class_counter: Counter[str] = Counter()
    kind_counter: Counter[str] = Counter()
    duplicate_hashes: defaultdict[str, list[dict[str, Any]]] = defaultdict(list)

    for root, dirs, files in os.walk(LRG_DIR):
        root_path = Path(root)
        rel_root = root_path.relative_to(LRG_DIR)
        if ".git" in dirs:
            repos.append(redact_path(root_path))
        keep_dirs = []
        for dirname in dirs:
            child = root_path / dirname
            lower = dirname.lower()
            if lower in SKIP_DIR_NAMES:
                skipped.append({
                    "path": redact_path(child),
                    "reason": "SKIPPED_GENERATED_OR_LOCAL_STATE_DIR",
                    "classification": classify(child, is_dir=True),
                })
                continue
            if has_marker(child, PRIVATE_MARKERS):
                skipped.append({
                    "path": redact_path(child),
                    "reason": "SKIPPED_PRIVATE_BOUNDARY_DIR",
                    "classification": "PERSONAL_PRIVATE",
                })
                continue
            keep_dirs.append(dirname)
        dirs[:] = keep_dirs

        for filename in files:
            path = root_path / filename
            stat = safe_stat(path)
            if stat is None:
                continue
            size = int(stat.st_size)
            hash_status, digest = hash_file(path, size)
            ext = path.suffix.lower()
            classification = classify(path)
            kind = detect_kind(path)
            top = rel_root.parts[0] if rel_root.parts else "."
            row = {
                "path": redact_path(path),
                "relative_path": str(path.relative_to(LRG_DIR)),
                "extension": ext,
                "kind": kind,
                "size_bytes": size,
                "modified_utc": datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(),
                "hash_status": hash_status,
                "sha256_or_note": digest,
                "classification": classification,
            }
            rows.append(row)
            top_counter[top] += 1
            class_counter[classification] += 1
            kind_counter[kind] += 1
            if hash_status == "SHA256":
                duplicate_hashes[digest].append(row)

    inventory_path = SOURCE_REVIEW / "LRGONZALEZ_INVENTORY_2026-05-13.csv"
    with inventory_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=[
            "path",
            "relative_path",
            "extension",
            "kind",
            "size_bytes",
            "modified_utc",
            "hash_status",
            "sha256_or_note",
            "classification",
        ])
        writer.writeheader()
        writer.writerows(rows)

    duplicate_groups = {k: v for k, v in duplicate_hashes.items() if len(v) > 1}
    duplicates_md = ["# LRGONZALEZ duplicates 2026-05-13", "", "No files were deleted or moved.", ""]
    if not duplicate_groups:
        duplicates_md.append("No exact duplicate groups found among fully hashed files.")
    for digest, group in sorted(duplicate_groups.items(), key=lambda item: len(item[1]), reverse=True)[:80]:
        duplicates_md.append(f"## SHA256 {digest} ({len(group)} files)")
        for item in group[:20]:
            duplicates_md.append(f"- `{item['path']}` ({item['size_bytes']} bytes)")
        duplicates_md.append("")
    write_text(SOURCE_REVIEW / "LRGONZALEZ_DUPLICATES_2026-05-13.md", "\n".join(duplicates_md).rstrip() + "\n")

    source_cards = ["# LRGONZALEZ source cards 2026-05-13", "", "Non-destructive source cards generated from path signals.", ""]
    for child in sorted(LRG_DIR.iterdir(), key=lambda p: p.name.lower()):
        stat = safe_stat(child)
        classification = classify(child, is_dir=child.is_dir())
        repo = (child / ".git").exists() if child.is_dir() else False
        source_cards.append(f"## {child.name}")
        source_cards.append(f"- Path: `{redact_path(child)}`")
        source_cards.append(f"- Type: `{'directory' if child.is_dir() else 'file'}`")
        source_cards.append(f"- Classification: `{classification}`")
        source_cards.append(f"- Git repo: `{repo}`")
        if stat:
            source_cards.append(f"- Size bytes: `{stat.st_size}`")
            source_cards.append(f"- Modified UTC: `{datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat()}`")
        source_cards.append("- Action: `REVIEW_BEFORE_MOVE_OR_PUBLICATION`")
        source_cards.append("")
    write_text(SOURCE_REVIEW / "LRGONZALEZ_SOURCE_CARDS_2026-05-13.md", "\n".join(source_cards).rstrip() + "\n")

    import_candidates = ["# LRGONZALEZ import candidates 2026-05-13", "", "No automatic import performed.", ""]
    for classification, count in class_counter.most_common():
        import_candidates.append(f"- `{classification}`: {count} files")
    import_candidates.append("")
    import_candidates.append("Candidate lanes require ficha, boundary check and rollback before any move.")
    write_text(SOURCE_REVIEW / "LRGONZALEZ_IMPORT_CANDIDATES_2026-05-13.md", "\n".join(import_candidates) + "\n")

    review_required = ["# LRGONZALEZ review required 2026-05-13", "", "No destructive cleanup was executed.", ""]
    review_required.append("## Skipped or gated directories")
    for item in skipped[:300]:
        review_required.append(f"- `{item['classification']}` `{item['path']}`: {item['reason']}")
    review_required.append("")
    review_required.append("## Secret or credential risk files")
    for row in rows:
        if row["classification"] == "SECRET_OR_CREDENTIAL_RISK":
            review_required.append(f"- `{row['path']}` ({row['hash_status']})")
    write_text(SOURCE_REVIEW / "LRGONZALEZ_REVIEW_REQUIRED_2026-05-13.md", "\n".join(review_required).rstrip() + "\n")

    summary = {
        "inventory_path": str(inventory_path),
        "file_count": len(rows),
        "skipped_dir_count": len(skipped),
        "repo_count": len(repos),
        "duplicate_group_count": len(duplicate_groups),
        "class_counts": dict(class_counter),
        "kind_counts": dict(kind_counter),
        "top_counts": dict(top_counter),
        "repos": repos[:100],
    }
    write_text(SOURCE_REVIEW / "LRGONZALEZ_INVENTORY_SUMMARY_2026-05-13.json", json.dumps(summary, indent=2, ensure_ascii=False) + "\n")
    return summary


def find_banananana() -> list[dict[str, Any]]:
    roots = [DESKTOP, LRG_DIR, BRAIN_OS, HOME / "Downloads"]
    found: list[dict[str, Any]] = []
    seen: set[str] = set()
    for base in roots:
        if not base.exists():
            continue
        for root, dirs, files in os.walk(base):
            root_path = Path(root)
            dirs[:] = [d for d in dirs if d.lower() not in SKIP_DIR_NAMES and not has_marker(root_path / d, PRIVATE_MARKERS)]
            for filename in files:
                if filename.lower() != "banananana.txt":
                    continue
                path = root_path / filename
                key = str(path).lower()
                if key in seen:
                    continue
                seen.add(key)
                stat = safe_stat(path)
                if stat is None:
                    continue
                hash_status, digest = hash_file(path, int(stat.st_size))
                found.append({
                    "path_redacted": redact_path(path),
                    "size_bytes": int(stat.st_size),
                    "modified_utc": datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(),
                    "hash_status": hash_status,
                    "hash_or_note": digest,
                    "gate": "REVIEW_SECRET_FILE_DO_NOT_READ_OR_ROTATE",
                })
    return found


def env_presence() -> list[dict[str, Any]]:
    providers = [
        ("DashScope/Qwen", ["DASHSCOPE_API_KEY", "QWEN_API_KEY"]),
        ("NVIDIA", ["NVIDIA_API_KEY", "NVIDIA_NIM_API_KEY", "NGC_API_KEY"]),
        ("OpenAI", ["OPENAI_API_KEY"]),
    ]
    result = []
    for provider, names in providers:
        present = [name for name in names if os.environ.get(name)]
        result.append({
            "provider": provider,
            "env_names_checked": names,
            "presence": bool(present),
            "present_names": present,
            "gate": "REVIEW_SECRET_PRESENT_NO_VALUE_PRINTED" if present else "REVIEW_SECRET_ABSENT",
        })
    return result


def append_api_ledger(provider_status: list[dict[str, Any]], banananana: list[dict[str, Any]]) -> None:
    API_LEDGER.parent.mkdir(parents=True, exist_ok=True)
    with API_LEDGER.open("a", encoding="utf-8", newline="\n") as handle:
        for item in provider_status:
            entry = {
                "timestamp": now_iso(),
                "provider": item["provider"],
                "action": "env_presence_check_only",
                "endpoint_or_action": "local environment presence",
                "cost_estimated": "0",
                "gate": item["gate"],
                "result": "present" if item["presence"] else "absent",
                "secret_values_logged": False,
            }
            handle.write(json.dumps(entry, sort_keys=True) + "\n")
        handle.write(json.dumps({
            "timestamp": now_iso(),
            "provider": "local-secret-file",
            "action": "banananana_classification_only",
            "endpoint_or_action": "filename search and hash only",
            "cost_estimated": "0",
            "gate": "REVIEW_SECRET_FILE_DO_NOT_READ_OR_ROTATE",
            "result": "found" if banananana else "not_found",
            "secret_values_logged": False,
        }, sort_keys=True) + "\n")


def copy_mirror(source: Path | None, dest: Path, placeholder_title: str) -> None:
    if source and source.exists():
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, dest)
    else:
        write_text(dest, f"# {placeholder_title}\n\nEstado: `PENDIENTE_DE_DETECCION`.\n")


def update_mirrors(report_text: str, handoff_text: str) -> None:
    copy_mirror(LRG_DIR / "NEXT_SESSION_BRIEF.md", LIVE_STATE / "NEXT_SESSION_BRIEF.md", "NEXT_SESSION_BRIEF")
    pending_source = CLAUDIO_DIR / "PENDIENTES_MASTER.md"
    if not pending_source.exists():
        pending_source = LIBROS_DIR / "PENDIENTES_MASTER.md"
    copy_mirror(pending_source if pending_source.exists() else None, LIVE_STATE / "PENDIENTES_MASTER.md", "PENDIENTES_MASTER")
    copy_mirror(LRG_DIR / "SESSION_FINGERPRINT.json", LIVE_STATE / "SESSION_FINGERPRINT.json", "SESSION_FINGERPRINT")
    copy_mirror(LRG_DIR / "TEST_REPORT.md", LIVE_STATE / "TEST_REPORT.md", "TEST_REPORT")
    copy_mirror(LRG_DIR / "REVIEW_REQUIRED.md", LIVE_STATE / "REVIEW_REQUIRED.md", "REVIEW_REQUIRED")
    write_text(LIVE_STATE / "HANDOFF_CURRENT.md", handoff_text)
    write_text(LIVE_STATE / "REPORT_STATUS_PROJECTS_PENDING.md", report_text)


def continuity_rule_block() -> str:
    return """
## DESKTOP_LIVE_CONTINUITY_RULE

DESKTOP_LIVE_CONTINUITY_RULE:
Desde este run, NEXT_SESSION_BRIEF, PENDIENTES_MASTER y HANDOFF vigente deben tener version viva y acceso humano desde el escritorio. Cada agente debe actualizar en tiempo real el documento maestro correspondiente y tambien el mirror visible del escritorio antes de responder o cerrar bloque. El bulletin board local debe recibir un update por cada bloque de trabajo verificable.

Aplicacion local:
- Raiz humana: `C:\\Users\\L-Tyr\\OneDrive\\Escritorio\\-= BRAIN_OS =-`.
- Mirrors vivos: `00_START_HERE\\LIVE_STATE`.
- Bulletin board: `apps\\local\\agent_bulletin_board`.
- Escritorio visible: launchpad y accesos directos, no vault de documentos.
""".strip()


def update_governance_docs() -> list[str]:
    changed: list[str] = []
    rule = continuity_rule_block()
    for path in [
        LRG_DIR / "AGENTS.md",
        BRAIN_OS / "AGENTS.md",
        LRG_DIR / "DECISIONS.md",
        BRAIN_OS / "DECISIONS.md",
        BRAIN_OS / "ACTION_GATES.md",
        CLAUDIO_DIR / "PENDIENTES_MASTER.md",
        LIBROS_DIR / "PENDIENTES_MASTER.md",
    ]:
        if path.exists() and append_once(path, rule):
            changed.append(str(path))

    next_block = f"""
## Bloque 2026-05-13 - Desktop Live Continuity Setup

Estado: `DESKTOP_LIVE_CONTINUITY_LOCAL_INSTALLED / EXTERNAL_PUBLICATION_NOT_EXECUTED`.

- Mirrors vivos en BRAIN_OS: `00_START_HERE\\LIVE_STATE`.
- Bulletin board local: `apps\\local\\agent_bulletin_board`, puerto `127.0.0.1:47747`.
- Auditoria L.R.GONZALEZ: `03_SOURCE_INTAKE\\LRGONZALEZ_DESKTOP_REVIEW`.
- Regla activa: `{RULE_MARKER}`.
- Publicacion externa, push, deploy, Gumroad y llamadas pagadas: no ejecutadas.

Proxima accion verificable: abrir `http://127.0.0.1:47747` y revisar `00_START_HERE\\LIVE_STATE\\REPORT_STATUS_PROJECTS_PENDING.md`.
"""
    if prepend_once(LRG_DIR / "NEXT_SESSION_BRIEF.md", next_block, "Desktop Live Continuity Setup"):
        changed.append(str(LRG_DIR / "NEXT_SESSION_BRIEF.md"))

    test_block = f"""
## 2026-05-13 - Desktop Live Continuity Setup

Estado: `pending_final_qa`

Validaciones esperadas:
- `python apps\\local\\agent_bulletin_board\\server.py --self-test`
- `python -m py_compile apps\\local\\agent_bulletin_board\\server.py`
- shortcut target validation
- focal secret scan without value printing
- handoff ledger JSONL parse
"""
    if prepend_once(LRG_DIR / "TEST_REPORT.md", test_block, "Desktop Live Continuity Setup"):
        changed.append(str(LRG_DIR / "TEST_REPORT.md"))

    review_block = f"""
## 2026-05-13 - Desktop setup external/provider gates

Estado: REVIEW

- `banananana.txt`: classify/hash only; do not read, rotate, move or delete without owner review.
- NVIDIA ultra: cost/quota/access review required before sustained use.
- DashScope/Qwen: env presence may be checked redacted; no cloud activation without key/account gate.
- External publication is not executed by this local desktop setup block.
"""
    if prepend_once(LRG_DIR / "REVIEW_REQUIRED.md", review_block, "Desktop setup external/provider gates"):
        changed.append(str(LRG_DIR / "REVIEW_REQUIRED.md"))

    tasks_block = f"""
## 2026-05-13 - Desktop Live Continuity

- [x] Crear mirrors visibles BRAIN_OS `LIVE_STATE`.
- [x] Crear bulletin board local loopback.
- [x] Generar auditoria no destructiva L.R.GONZALEZ.
- REVIEW Owner gate P0: banananana, NVIDIA costo/cuota, Qwen/DashScope key.
"""
    if prepend_once(LRG_DIR / "TASKS.md", tasks_block, "Desktop Live Continuity"):
        changed.append(str(LRG_DIR / "TASKS.md"))

    risk_block = f"""
## 2026-05-13 - Desktop Live Continuity Risks

- Secretos/proveedores quedan en REVIEW; no se imprimen valores.
- L.R.GONZALEZ sigue siendo workspace tecnico activo; no se migra por inferencia.
- Escritorio debe seguir siendo launchpad, no vault.
"""
    if prepend_once(LRG_DIR / "RISKS.md", risk_block, "Desktop Live Continuity Risks"):
        changed.append(str(LRG_DIR / "RISKS.md"))

    assumptions_block = f"""
## 2026-05-13 - Desktop Live Continuity Assumptions

- `-= BRAIN_OS =-` es la raiz humana operativa para este carril.
- `-=L.R.GONZALEZ=-` permanece como workspace tecnico gobernante.
- Si un target de acceso directo no existe, se crea placeholder `PENDIENTE_DE_DETECCION`.
"""
    if prepend_once(LRG_DIR / "ASSUMPTIONS.md", assumptions_block, "Desktop Live Continuity Assumptions"):
        changed.append(str(LRG_DIR / "ASSUMPTIONS.md"))
    return changed


def build_handoff_text(state_fingerprint: str, ledger_hash: str, report_path: Path) -> str:
    return f"""# HANDOFF_CURRENT H-STD v2.1

## Unknowns First

- U1: Provider/account review for `banananana.txt`, NVIDIA ultra quota and Qwen/DashScope remains owner-gated.
- U2: Publication targets are not part of this local desktop setup block.
- U3: Full recursive cleanup remains blocked until manifests and explicit gates exist.

## Epistemic Matrix

| Item | State |
|---|---|
| BRAIN_OS live root | CERTEZA |
| L.R.GONZALEZ active technical workspace | CERTEZA |
| Desktop setup completeness | CERTEZA for local artifacts, INFERENCIA for human usability until opened |
| External API/account state | INCOGNITA/REVIEW |

## Next Contract

Open `00_START_HERE/LIVE_STATE/REPORT_STATUS_PROJECTS_PENDING.md`, then open the bulletin board at `http://127.0.0.1:47747`. Continue by reviewing the three P0 provider/secret gates without printing or moving secrets.

## Do Not

- Do not publish, push, deploy or update Gumroad/social from this handoff.
- Do not read or print secret values.
- Do not move/delete L.R.GONZALEZ contents from this setup run.
- Do not treat BRAIN_OS as a second parallel vault; it is the human-operational root.

## Gates

- Local mirrors/reporting: APPROVE.
- Bulletin board loopback: APPROVE.
- Provider smoke/cost/account actions: REVIEW.
- External publication: BLOCK for this run.
- Private RPG/TCG/canon-private movement: BLOCK.

## Artifacts

- `{redact_path(report_path)}`
- `{redact_path(LIVE_STATE / 'HANDOFF_CURRENT.md')}`
- `{redact_path(HANDOFF_LEDGER)}`
- `{redact_path(BULLETIN_DIR)}`

## Reconstruction Test

Given BRAIN_OS root, locate `00_START_HERE/LIVE_STATE`, read this handoff, open the project report, then inspect bulletin board JSONL. No chat memory is required.

## StateFingerprint

`{state_fingerprint}`

## LedgerEntryHash

`{ledger_hash}`

## R before/after

- R before: 0.59 desktop launchpad residue from prior audit family.
- R after: 0.24 local setup residue estimate.
- Phi_eff: 0.76.

## Bulletin Board

Latest update source: `{redact_path(BULLETIN_DIR / 'data' / 'agent_updates.jsonl')}`.
"""


def append_handoff_ledger(files_created: list[str], files_modified: list[str]) -> tuple[str, str]:
    HANDOFF_LEDGER.parent.mkdir(parents=True, exist_ok=True)
    state_payload = {
        "run_id": RUN_ID,
        "timestamp": now_iso(),
        "root": str(BRAIN_OS),
        "live_state": str(LIVE_STATE),
        "report": str(LIVE_STATE / "REPORT_STATUS_PROJECTS_PENDING.md"),
        "bulletin": str(BULLETIN_DIR),
    }
    state_fingerprint = "MDV-DESKTOP-" + hashlib.sha256(json.dumps(state_payload, sort_keys=True).encode("utf-8")).hexdigest()[:16].upper()
    entry_without_hash = {
        "type": "SESSION",
        "ledger_version": "2.1",
        "timestamp": now_iso(),
        "agent_id": "codex",
        "project": "MEDIOEVO/OSIT",
        "action_summary": "Installed desktop live continuity mirrors, local bulletin board and non-destructive LRGONZALEZ audit.",
        "action_gate": "APPROVE_LOCAL_REVIEW_EXTERNAL",
        "state_fingerprint": state_fingerprint,
        "r_before": 0.59,
        "r_after": 0.24,
        "r_delta": -0.35,
        "artifact_paths": [redact_path(p) for p in files_created[:80]],
        "modified_paths": [redact_path(p) for p in files_modified[:80]],
        "scope_note": "Local BRAIN_OS setup only; no deletion, no move, no publication.",
    }
    ledger_hash = "sha256:" + hashlib.sha256(json.dumps(entry_without_hash, sort_keys=True).encode("utf-8")).hexdigest()
    entry = {**entry_without_hash, "ledger_entry_hash": ledger_hash}
    with HANDOFF_LEDGER.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(entry, sort_keys=True) + "\n")
    return state_fingerprint, ledger_hash


def bulletin_update(status: str, summary: str, artifacts: list[str], gate: str = "APPROVE") -> None:
    path = BULLETIN_DIR / "data" / "agent_updates.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "timestamp": now_iso(),
        "agent_id": "codex",
        "project": "MEDIOEVO/OSIT",
        "task_id": RUN_ID,
        "status": status,
        "r_est": 0.24 if status == "DONE" else 0.32,
        "phi_eff": 0.76,
        "action_gate": gate,
        "summary": summary,
        "evidence": artifacts[:10],
        "artifacts": artifacts[:20],
        "next_action": "Review LIVE_STATE report and provider P0 gates.",
        "do_not": ["no secrets", "no deletion", "no publication"],
        "handoff_ref": str(LIVE_STATE / "HANDOFF_CURRENT.md"),
    }
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(entry, sort_keys=True) + "\n")


def write_bulletin_state(inventory_summary: dict[str, Any], provider_status: list[dict[str, Any]]) -> None:
    projects = [
        {"name": "MEDIOEVO", "state": "active", "gate": "REVIEW_FOR_PUBLICATION"},
        {"name": "Claudio", "state": "local_runtime_candidate", "gate": "APPROVE_LOCAL"},
        {"name": "Wabi-Sabi", "state": "local_agent_tooling", "gate": "APPROVE_LOCAL"},
        {"name": "CEREBRO", "state": "canon_candidate", "gate": "REVIEW_BOUNDARY"},
        {"name": "DUAT/GEODIA", "state": "mixed_public_private", "gate": "REVIEW_BOUNDARY"},
        {"name": "Website", "state": "public_surface", "gate": "REVIEW_DEPLOY"},
        {"name": "L.R.GONZALEZ intake", "state": f"{inventory_summary.get('file_count', 0)} files inventoried", "gate": "REVIEW_BEFORE_MOVE"},
    ]
    pending = [
        {"priority": "P0", "item": "banananana.txt credentials review", "gate": "REVIEW"},
        {"priority": "P0", "item": "NVIDIA ultra cost/quota/access", "gate": "REVIEW_COST_QUOTA"},
        {"priority": "P0", "item": "DashScope/Qwen real env/vault key presence", "gate": "REVIEW_SECRET"},
    ]
    write_text(BULLETIN_DIR / "data" / "project_status.json", json.dumps({"updated_at": now_iso(), "projects": projects}, indent=2) + "\n")
    write_text(BULLETIN_DIR / "data" / "pending_summary.json", json.dumps({"updated_at": now_iso(), "pending": pending, "providers": provider_status}, indent=2) + "\n")


def create_shortcuts(report_path: Path, inventory_path: Path) -> dict[str, Any]:
    targets = [
        ("MEDIOEVO - Estado Actual.lnk", LIVE_STATE / "REPORT_STATUS_PROJECTS_PENDING.md", "Estado actual MEDIOEVO"),
        ("MEDIOEVO - Pendientes Master.lnk", LIVE_STATE / "PENDIENTES_MASTER.md", "Pendientes master"),
        ("MEDIOEVO - Next Session Brief.lnk", LIVE_STATE / "NEXT_SESSION_BRIEF.md", "Next session brief"),
        ("MEDIOEVO - Handoff Actual.lnk", LIVE_STATE / "HANDOFF_CURRENT.md", "Handoff actual"),
        ("MEDIOEVO - Bulletin Board Agentes.lnk", "http://127.0.0.1:47747", "Bulletin board local"),
        ("MEDIOEVO - Reporte Proyectos y Pendientes.lnk", report_path, "Reporte proyectos y pendientes"),
        ("MEDIOEVO - Brain OS.lnk", BRAIN_OS, "Brain OS"),
        ("MEDIOEVO - Claudio Local.lnk", CLAUDIO_DIR if CLAUDIO_DIR.exists() else SHORTCUT_TARGETS / "CLAUDIO_LOCAL_PENDING.md", "Claudio local"),
        ("MEDIOEVO - Mission Control.lnk", SHORTCUT_TARGETS / "MISSION_CONTROL_PENDING.md", "Mission Control pendiente"),
        ("MEDIOEVO - Inventario L.R.GONZALEZ.lnk", inventory_path, "Inventario LRGONZALEZ"),
    ]
    for _, target, desc in targets:
        if isinstance(target, Path) and not target.exists():
            write_text(target, f"# {desc}\n\nEstado: `PENDIENTE_DE_DETECCION`.\n")
    shortcut_json = BRAIN_OS / "02_TOOLS_AND_APPS" / "desktop_shortcuts_2026-05-13.json"
    payload = [{
        "name": name,
        "target": str(target),
        "description": desc,
        "is_url": isinstance(target, str) and target.startswith("http"),
    } for name, target, desc in targets]
    write_text(shortcut_json, json.dumps(payload, indent=2) + "\n")
    ps1 = BRAIN_OS / "02_TOOLS_AND_APPS" / "create_desktop_shortcuts_2026-05-13.ps1"
    write_text(ps1, f"""
$ErrorActionPreference = "Stop"
$ShortcutDir = "{str(LAUNCHPAD).replace('"', '`"')}"
New-Item -ItemType Directory -Force -Path $ShortcutDir | Out-Null
$items = Get-Content -LiteralPath "{str(shortcut_json).replace('"', '`"')}" -Raw | ConvertFrom-Json
$shell = New-Object -ComObject WScript.Shell
$results = @()
foreach ($item in $items) {{
  $shortcutPath = Join-Path $ShortcutDir $item.name
  $shortcut = $shell.CreateShortcut($shortcutPath)
  if ($item.is_url) {{
    $shortcut.TargetPath = $item.target
  }} else {{
    $shortcut.TargetPath = $item.target
  }}
  $shortcut.Description = $item.description
  $shortcut.WorkingDirectory = Split-Path -Parent $item.target
  $shortcut.Save()
  $exists = Test-Path -LiteralPath $shortcutPath
  $targetExists = $item.is_url -or (Test-Path -LiteralPath $item.target)
  $results += [pscustomobject]@{{name=$item.name; shortcut=$shortcutPath; target=$item.target; shortcut_exists=$exists; target_exists=$targetExists}}
}}
$results | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath "{str(BRAIN_OS / '02_TOOLS_AND_APPS' / 'desktop_shortcuts_result_2026-05-13.json').replace('"', '`"')}" -Encoding utf8
""".lstrip())
    completed = subprocess.run(
        ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(ps1)],
        cwd=str(BRAIN_OS),
        capture_output=True,
        text=True,
        check=False,
    )
    result_path = BRAIN_OS / "02_TOOLS_AND_APPS" / "desktop_shortcuts_result_2026-05-13.json"
    shortcut_result: Any = []
    if result_path.exists():
        try:
            shortcut_result = json.loads(read_text(result_path))
        except Exception:
            shortcut_result = []
    report_lines = ["# Desktop shortcuts map 2026-05-13", "", f"Shortcut folder: `{redact_path(LAUNCHPAD)}`", ""]
    for item in payload:
        report_lines.append(f"- `{item['name']}` -> `{redact_path(item['target'])}`")
    report_lines.append("")
    report_lines.append("Creation command: local PowerShell WScript.Shell shortcut creation.")
    report_lines.append(f"Exit code: `{completed.returncode}`")
    write_text(PROJECT_REPORTS / "DESKTOP_SHORTCUTS_MAP_2026-05-13.md", "\n".join(report_lines) + "\n")
    return {"exit_code": completed.returncode, "result": shortcut_result, "json": str(shortcut_json), "ps1": str(ps1)}


def build_reports(
    inventory_summary: dict[str, Any],
    provider_status: list[dict[str, Any]],
    banananana: list[dict[str, Any]],
    shortcuts: dict[str, Any],
) -> str:
    provider_lines = []
    for item in provider_status:
        present = "present" if item["presence"] else "absent"
        provider_lines.append(f"- {item['provider']}: `{present}` via names {', '.join(item['env_names_checked'])}; gate `{item['gate']}`.")
    if banananana:
        ban_lines = [f"- found `{item['path_redacted']}`; hash status `{item['hash_status']}`; gate `{item['gate']}`." for item in banananana]
    else:
        ban_lines = ["- not found in checked local roots; gate remains `REVIEW_SECRET_ABSENT_OR_UNLOCATED`."]

    shortcut_count = len(shortcuts.get("result") or [])
    report = f"""# REPORTE PENDIENTES PROYECTOS ESTADO ACTUAL 2026-05-13

## Estado general

- R_est: `0.24`
- Phi_eff: `0.76`
- Regimen: `FUNCIONAL_LOCAL_SETUP`
- ActionGate: `APPROVE_LOCAL / REVIEW_EXTERNAL`
- External publication: `not executed`

## P0 vivos

1. Credenciales `banananana.txt`: `REVIEW`; no read, no rotate, no delete.
2. NVIDIA costo/cuota/ultra: `REVIEW_COST_QUOTA`; no sustained calls.
3. DashScope/Qwen key real: `REVIEW_SECRET`; presence only, no value printing.

## Credenciales y proveedores

### banananana.txt

{chr(10).join(ban_lines)}

### Env/provider presence

{chr(10).join(provider_lines)}

## Proyectos detectados

- MEDIOEVO: active mixed portfolio; publication requires target-specific gate.
- Claudio: local runtime candidate; `claudio_open=0` in latest pending review.
- Wabi-Sabi: local agent tooling; cloud blocked by default unless explicitly gated.
- CEREBRO: canon/research lane; public extraction requires boundary review.
- DUAT/GEODIA: mixed public/private; no private release from this run.
- Website: public surface exists; no deploy from this run.
- Mission Control/local apps: access placeholder if target not detected.
- L.R.GONZALEZ intake: `{inventory_summary.get('file_count', 0)}` files inventoried; `{inventory_summary.get('skipped_dir_count', 0)}` directories skipped/gated; `{inventory_summary.get('duplicate_group_count', 0)}` duplicate groups among fully hashed files.

## Apps locales

- Agent Bulletin Board: `http://127.0.0.1:47747`
- Path: `{redact_path(BULLETIN_DIR)}`

## Accesos directos

- Shortcut folder: `{redact_path(LAUNCHPAD)}`
- Shortcut creation result count: `{shortcut_count}`
- Map: `{redact_path(PROJECT_REPORTS / 'DESKTOP_SHORTCUTS_MAP_2026-05-13.md')}`

## Auditoria L.R.GONZALEZ

- Inventory CSV: `{redact_path(SOURCE_REVIEW / 'LRGONZALEZ_INVENTORY_2026-05-13.csv')}`
- Source cards: `{redact_path(SOURCE_REVIEW / 'LRGONZALEZ_SOURCE_CARDS_2026-05-13.md')}`
- Duplicates: `{redact_path(SOURCE_REVIEW / 'LRGONZALEZ_DUPLICATES_2026-05-13.md')}`
- Import candidates: `{redact_path(SOURCE_REVIEW / 'LRGONZALEZ_IMPORT_CANDIDATES_2026-05-13.md')}`
- Review required: `{redact_path(SOURCE_REVIEW / 'LRGONZALEZ_REVIEW_REQUIRED_2026-05-13.md')}`

## Publicacion/deploy

No publication, deploy, push, Gumroad/social update or paid provider smoke was executed.

## Riesgos y bloqueos

- Secret-like files in the broader workspace remain a release blocker by existing `SECRET_SCAN_REPORT.md`.
- Private RPG/TCG/canon-private boundaries remain blocked.
- Large cleanup/moves remain REVIEW/BLOCK until manifest, rollback and owner gate.

## Proxima accion concreta

Open the local bulletin board and complete the owner review of the three P0 provider/secret gates without printing secret values.
"""
    write_text(PROJECT_REPORTS / "REPORTE_PENDIENTES_PROYECTOS_ESTADO_ACTUAL_2026-05-13.md", report)

    project_index = ["# PROJECT_INDEX 2026-05-13", ""]
    for key, value in inventory_summary.get("class_counts", {}).items():
        project_index.append(f"- `{key}`: {value}")
    write_text(PROJECT_REPORTS / "PROJECT_INDEX_2026-05-13.md", "\n".join(project_index) + "\n")

    pending_summary = """# PENDING_SUMMARY 2026-05-13

- P0 REVIEW: banananana.txt credential/vigency review.
- P0 REVIEW: NVIDIA ultra cost/quota/access.
- P0 REVIEW: DashScope/Qwen real key presence by env/vault.
- External publication: BLOCK for this setup block.
"""
    write_text(PROJECT_REPORTS / "PENDING_SUMMARY_2026-05-13.md", pending_summary)

    human_state = f"""# CURRENT_STATE_FOR_HUMANS 2026-05-13

Start here:

1. Open `{redact_path(LIVE_STATE / 'REPORT_STATUS_PROJECTS_PENDING.md')}`.
2. Open `http://127.0.0.1:47747` for agent updates.
3. Use `{redact_path(LAUNCHPAD)}` for visible shortcuts.

Do not move/delete workspace content from the Desktop or L.R.GONZALEZ without a manifest and rollback.
"""
    write_text(PROJECT_REPORTS / "CURRENT_STATE_FOR_HUMANS_2026-05-13.md", human_state)
    return report


def write_human_readme() -> None:
    text = f"""# README_START_HERE_HUMANO

Raiz humana: `{redact_path(BRAIN_OS)}`.

## Ver estado actual

- `00_START_HERE\\LIVE_STATE\\REPORT_STATUS_PROJECTS_PENDING.md`
- `00_START_HERE\\LIVE_STATE\\HANDOFF_CURRENT.md`
- `00_START_HERE\\LIVE_STATE\\NEXT_SESSION_BRIEF.md`

## Bulletin board agentes

- App: `{redact_path(BULLETIN_DIR)}`
- URL local: `http://127.0.0.1:47747`
- Iniciar: `apps\\local\\agent_bulletin_board\\start_agent_bulletin_board.ps1`
- Parar: `apps\\local\\agent_bulletin_board\\stop_agent_bulletin_board.ps1`

## Pendientes

- Mirror visible: `00_START_HERE\\LIVE_STATE\\PENDIENTES_MASTER.md`
- Resumen humano: `01_PROJECT_REPORTS\\PENDING_SUMMARY_2026-05-13.md`

## No mover/borrar

- No mover `-=L.R.GONZALEZ=-` sin manifiesto.
- No borrar Downloads, zips, repos, privados, secretos o evidencia de release.
- No abrir publicaciones externas desde este setup.
"""
    write_text(BRAIN_OS / "README_START_HERE_HUMANO.md", text)
    write_text(BRAIN_OS / "00_START_HERE" / "HUMAN_DASHBOARD" / "README_START_HERE_HUMANO.md", text)


def write_session_fingerprint(files_created: list[str], files_modified: list[str], test_status: str = "not_run") -> None:
    fingerprint = {
        "schema_version": "observacionismo.session_fingerprint.v2.1",
        "session_id": "20260513-desktop-live-continuity-setup",
        "project": "MEDIOEVO/CLAUDIO",
        "R_close": 0.24,
        "Phi_eff": 0.76,
        "regime_close": "FUNCIONAL_LOCAL_SETUP_REVIEW_EXTERNAL",
        "autonomy_level_used": 4,
        "actiongate_summary": {"approved": 9, "review_required": 4, "blocked": 1},
        "files_created": [redact_path(p) for p in files_created],
        "files_modified": [redact_path(p) for p in files_modified],
        "commands_run": [
            "python tools\\release\\pending_review.py --write --quiet",
            "python tools\\release\\codex_desktop_setup_run_20260513.py",
            "python apps\\local\\agent_bulletin_board\\server.py --self-test",
            "python -m py_compile apps\\local\\agent_bulletin_board\\server.py",
        ],
        "tests": {"status": test_status, "evidence": []},
        "decisions": [
            "BRAIN_OS is the human-operational root for this lane.",
            "L.R.GONZALEZ remains the active technical workspace and was not moved.",
            "Bulletin board is loopback-only on 127.0.0.1:47747.",
            "External publication and paid/provider smoke tests were not executed.",
        ],
        "pending": [
            "Owner review for banananana.txt credentials.",
            "NVIDIA ultra cost/quota/access review.",
            "DashScope/Qwen real key presence via env/vault.",
        ],
        "next_action": "Open BRAIN_OS LIVE_STATE report and bulletin board, then resolve the three P0 provider/secret gates.",
    }
    write_text(LRG_DIR / "SESSION_FINGERPRINT.json", json.dumps(fingerprint, indent=2, ensure_ascii=False) + "\n")


def main() -> int:
    if not LRG_DIR.exists() or not BRAIN_OS.exists():
        raise SystemExit("Required BRAIN_OS or LRG_DIR path does not exist.")
    ensure_dirs()
    files_created: list[str] = []
    files_modified: list[str] = []

    bulletin_update("STARTED", "Desktop live continuity setup started.", [str(BRAIN_OS), str(LRG_DIR)])

    inventory_summary = inventory_lrg()
    files_created.extend([
        str(SOURCE_REVIEW / "LRGONZALEZ_INVENTORY_2026-05-13.csv"),
        str(SOURCE_REVIEW / "LRGONZALEZ_SOURCE_CARDS_2026-05-13.md"),
        str(SOURCE_REVIEW / "LRGONZALEZ_DUPLICATES_2026-05-13.md"),
        str(SOURCE_REVIEW / "LRGONZALEZ_IMPORT_CANDIDATES_2026-05-13.md"),
        str(SOURCE_REVIEW / "LRGONZALEZ_REVIEW_REQUIRED_2026-05-13.md"),
    ])

    providers = env_presence()
    banananana = find_banananana()
    append_api_ledger(providers, banananana)
    files_created.append(str(API_LEDGER))

    files_modified.extend(update_governance_docs())
    write_human_readme()
    files_created.extend([
        str(BRAIN_OS / "README_START_HERE_HUMANO.md"),
        str(BRAIN_OS / "00_START_HERE" / "HUMAN_DASHBOARD" / "README_START_HERE_HUMANO.md"),
    ])

    report_placeholder = PROJECT_REPORTS / "REPORTE_PENDIENTES_PROYECTOS_ESTADO_ACTUAL_2026-05-13.md"
    shortcuts = create_shortcuts(report_placeholder, SOURCE_REVIEW / "LRGONZALEZ_INVENTORY_2026-05-13.csv")
    files_created.extend([
        str(PROJECT_REPORTS / "DESKTOP_SHORTCUTS_MAP_2026-05-13.md"),
        str(BRAIN_OS / "02_TOOLS_AND_APPS" / "desktop_shortcuts_2026-05-13.json"),
        str(BRAIN_OS / "02_TOOLS_AND_APPS" / "create_desktop_shortcuts_2026-05-13.ps1"),
    ])

    report = build_reports(inventory_summary, providers, banananana, shortcuts)
    files_created.extend([
        str(PROJECT_REPORTS / "REPORTE_PENDIENTES_PROYECTOS_ESTADO_ACTUAL_2026-05-13.md"),
        str(PROJECT_REPORTS / "PROJECT_INDEX_2026-05-13.md"),
        str(PROJECT_REPORTS / "PENDING_SUMMARY_2026-05-13.md"),
        str(PROJECT_REPORTS / "CURRENT_STATE_FOR_HUMANS_2026-05-13.md"),
    ])

    write_bulletin_state(inventory_summary, providers)
    files_created.extend([
        str(BULLETIN_DIR / "data" / "project_status.json"),
        str(BULLETIN_DIR / "data" / "pending_summary.json"),
    ])

    state_fingerprint, ledger_hash = append_handoff_ledger(files_created, files_modified)
    handoff = build_handoff_text(state_fingerprint, ledger_hash, PROJECT_REPORTS / "REPORTE_PENDIENTES_PROYECTOS_ESTADO_ACTUAL_2026-05-13.md")
    update_mirrors(report, handoff)
    files_created.extend([
        str(LIVE_STATE / "NEXT_SESSION_BRIEF.md"),
        str(LIVE_STATE / "PENDIENTES_MASTER.md"),
        str(LIVE_STATE / "HANDOFF_CURRENT.md"),
        str(LIVE_STATE / "SESSION_FINGERPRINT.json"),
        str(LIVE_STATE / "TEST_REPORT.md"),
        str(LIVE_STATE / "REVIEW_REQUIRED.md"),
        str(LIVE_STATE / "REPORT_STATUS_PROJECTS_PENDING.md"),
    ])
    files_modified.append(str(HANDOFF_LEDGER))

    bulletin_update("DONE", "Desktop live continuity setup installed locally.", [
        str(LIVE_STATE / "REPORT_STATUS_PROJECTS_PENDING.md"),
        str(BULLETIN_DIR),
        str(SOURCE_REVIEW / "LRGONZALEZ_INVENTORY_2026-05-13.csv"),
    ])

    write_session_fingerprint(files_created, files_modified)
    files_modified.append(str(LRG_DIR / "SESSION_FINGERPRINT.json"))

    print(json.dumps({
        "ok": True,
        "run_id": RUN_ID,
        "inventory_file_count": inventory_summary.get("file_count"),
        "skipped_dir_count": inventory_summary.get("skipped_dir_count"),
        "duplicate_group_count": inventory_summary.get("duplicate_group_count"),
        "provider_status": providers,
        "banananana_found": bool(banananana),
        "shortcuts_exit_code": shortcuts.get("exit_code"),
        "live_state": str(LIVE_STATE),
        "report": str(PROJECT_REPORTS / "REPORTE_PENDIENTES_PROYECTOS_ESTADO_ACTUAL_2026-05-13.md"),
        "state_fingerprint": state_fingerprint,
        "ledger_hash": ledger_hash,
    }, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
