from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from _common import ROOT, print_json, sha256_file, validate_root_arg, add_common_args


DOWNLOADS = Path.home() / "Downloads"

KNOWN_FILES = [
    {
        "path": DOWNLOADS / "observacionismo_ai_os_fullstack.zip",
        "classification": "EXTERNAL_TECHNICAL_ZIP",
        "lane": "obsai",
        "intake_action": "SELECTIVE_ABSORPTION_ONLY",
        "target": "packages/obsai-core",
        "notes": "Use as source material for obsai-core, metrics, gate and CLI. Do not copy wholesale.",
    },
    {
        "path": DOWNLOADS / "operational_ai_threshold.zip",
        "classification": "EXTERNAL_TECHNICAL_ZIP",
        "lane": "obsai",
        "intake_action": "SELECTIVE_ABSORPTION_ONLY",
        "target": "packages/obsai-core",
        "notes": "Threshold heuristics remain DEMO_ONLY until calibrated with a real dataset.",
    },
    {
        "path": DOWNLOADS / "residueos_mvp.zip",
        "classification": "EXTERNAL_TECHNICAL_ZIP",
        "lane": "residueos",
        "intake_action": "SELECTIVE_ABSORPTION_ONLY",
        "target": "apps/residueos",
        "notes": "JSON store is DEMO_ONLY until migrated to SQLite with audit and human review.",
    },
    {
        "path": DOWNLOADS / "medioevo_observacionismo_codex_pack.zip",
        "classification": "EXTERNAL_CANON_TOOLKIT_ZIP",
        "lane": "lore",
        "intake_action": "SELECTIVE_ABSORPTION_ONLY",
        "target": "packages/lore-compiler and game-private manifests",
        "notes": "Feed Lore Compiler and private WorldPulse work. Do not publish the game.",
    },
    {
        "path": DOWNLOADS / "duat_lg_patch.zip",
        "classification": "EXTERNAL_RESEARCH_TOOLKIT_ZIP",
        "lane": "research-boundary",
        "intake_action": "RESEARCH_ONLY",
        "target": "research/",
        "notes": "Formal research/toolkit source. No product claims without falsifier or prediction requirement.",
    },
    {
        "path": DOWNLOADS / "A_MEDIOEVO_OBSERVACIONISMO_DIEGETICO.md",
        "classification": "BOOKS_EDITORIAL_SOURCE",
        "lane": "lore",
        "intake_action": "CLASSIFY_BEFORE_EXTRACTION",
        "target": "books/ or packages/lore-compiler fixtures",
        "notes": "Diegetic MEDIOEVO source. Extract only evidence-backed data; mark inference.",
    },
    {
        "path": DOWNLOADS / "# Sí la idea fuerte es que el ecosi.txt",
        "classification": "PRIVATE_GAME_DESIGN_SOURCE",
        "lane": "rpg-private",
        "intake_action": "CLASSIFY_BEFORE_EXTRACTION",
        "target": "E:/Medioevo_RPG docs/data only",
        "notes": "WorldPulse/ecosystem-as-nervous-system game design source. Private game only.",
    },
    {
        "path": DOWNLOADS / "para el motor gemma 4 te tengo esto.txt",
        "classification": "EXTERNAL_AI_ARCHITECTURE_SOURCE",
        "lane": "obsai",
        "intake_action": "SELECTIVE_ABSORPTION_ONLY",
        "target": "packages/obsai-core or research/ after claim review",
        "notes": "Gemma/Observacionismo agent architecture source. No model modification claims without implementation evidence.",
    },
    {
        "path": DOWNLOADS / "# La App que no existe y que el mun.txt",
        "classification": "PRODUCT_CONCEPT_SOURCE",
        "lane": "residueos",
        "intake_action": "PRODUCT_IDEA_ONLY",
        "target": "apps/residueos or future kairos brief",
        "notes": "Kairos assistant concept. Do not claim product availability until implemented and tested.",
    },
    {
        "path": DOWNLOADS / "deep-research-report.md",
        "classification": "RESEARCH_ONLY_REPORT",
        "lane": "research-boundary",
        "intake_action": "RESEARCH_ONLY",
        "target": "research/",
        "notes": "Operational access-consciousness report. Keep separate from product claims.",
    },
    {
        "path": DOWNLOADS / "# Resultado matemático.txt",
        "classification": "RESEARCH_ONLY_REPORT",
        "lane": "research-boundary",
        "intake_action": "RESEARCH_ONLY",
        "target": "research/",
        "notes": "Mathematical boundary note: operational access only, not phenomenal consciousness proof.",
    },
    {
        "path": DOWNLOADS / "A continuación presento una formali.txt",
        "classification": "RESEARCH_ONLY_REPORT",
        "lane": "research-boundary",
        "intake_action": "RESEARCH_ONLY",
        "target": "research/",
        "notes": "Formal cosmology/model review. No physics or cosmology product claims.",
    },
    {
        "path": DOWNLOADS / "Voy a tomar la petición literalment.txt",
        "classification": "RESEARCH_LORE_TRANSLATION_SOURCE",
        "lane": "research-boundary",
        "intake_action": "RESEARCH_ONLY",
        "target": "research/ or lore residue with explicit inference labels",
        "notes": "Symbolic translation source. Treat as interpretive research, not canon fact.",
    },
    {
        "path": DOWNLOADS / "insights de programacion e ia..txt",
        "classification": "EXTERNAL_AI_ARCHITECTURE_SOURCE",
        "lane": "obsai",
        "intake_action": "SELECTIVE_ABSORPTION_ONLY",
        "target": "packages/obsai-core docs or research/",
        "notes": "Operational AI/programming insights. Absorb only concrete implementable controls.",
    },
    {
        "path": DOWNLOADS / "B_observacionist_agent.py",
        "classification": "EXTERNAL_RESEARCH_CODE",
        "lane": "obsai",
        "intake_action": "SELECTIVE_ABSORPTION_ONLY",
        "target": "packages/obsai-core experiments or research/",
        "notes": "Prototype code with numpy/scipy dependencies. Do not copy into core without stdlib/dependency decision.",
    },
    {
        "path": DOWNLOADS / "C_lg_benchmark.py",
        "classification": "EXTERNAL_RESEARCH_CODE",
        "lane": "obsai",
        "intake_action": "SELECTIVE_ABSORPTION_ONLY",
        "target": "packages/obsai-core experiments or research/",
        "notes": "LG/R benchmark prototype. Dataset and calibration claims remain DEMO_ONLY.",
    },
    {
        "path": DOWNLOADS / "D_MANUSCRITO_DE_CALIBRACION.md",
        "classification": "BOOKS_EDITORIAL_SOURCE",
        "lane": "lore",
        "intake_action": "CLASSIFY_BEFORE_EXTRACTION",
        "target": "packages/lore-compiler fixtures or game-private lore manifests",
        "notes": "Diegetic calibration manuscript. Evidence/inference split required before gameplay extraction.",
    },
    {
        "path": DOWNLOADS / "_ARCHIVO_OBSERVACIONISMO_DUPLICADOS_2026-04-29",
        "classification": "ARCHIVE_DUPLICATE_ROOT",
        "lane": "cleanup",
        "intake_action": "MANIFEST_ONLY",
        "target": "_archive/source-intake",
        "notes": "Duplicate source archive root; do not absorb unless a primary source is missing.",
    },
    {
        "path": DOWNLOADS / "_ARCHIVO_OBSERVACIONISMO_DUPLICADOS_2026-04-29" / "operational_ai_threshold (1).zip",
        "classification": "ARCHIVE_DUPLICATE",
        "lane": "cleanup",
        "intake_action": "MANIFEST_ONLY",
        "target": "_archive/source-intake",
        "notes": "Duplicate archive copy; keep as evidence, do not absorb unless primary is missing.",
    },
    {
        "path": DOWNLOADS / "_ARCHIVO_OBSERVACIONISMO_DUPLICADOS_2026-04-29" / "A_MEDIOEVO_OBSERVACIONISMO_DIEGETICO (1).md",
        "classification": "ARCHIVE_DUPLICATE",
        "lane": "cleanup",
        "intake_action": "MANIFEST_ONLY",
        "target": "_archive/source-intake",
        "notes": "Duplicate archive copy; keep as evidence, do not absorb unless primary is missing.",
    },
]

EXTERNAL_ROOTS = [
    {
        "path": Path("E:/-=Medioevo=-"),
        "classification": "BOOKS_COMMERCIAL_ARCHIVE",
        "lane": "publishing",
        "intake_action": "MANIFEST_AND_CHECKSUM_ONLY",
        "notes": "Books 00-34, audiobooks, Gumroad assets, consolidated 6+1 and editorial/commercial files.",
    },
    {
        "path": Path("E:/Medioevo_RPG"),
        "classification": "PRIVATE_GAME",
        "lane": "rpg-private",
        "intake_action": "PRIVATE_REPO_ACTIVE_MANIFEST_ONLY",
        "notes": "Godot private game with private local Git repo, WorldPulseBridge and headless validations. Do not publish or mix with open source.",
    },
    {
        "path": Path("E:/MEDIOEVO"),
        "classification": "LOCAL_SECRET_STATE",
        "lane": "cleanup",
        "intake_action": "DO_NOT_COPY",
        "notes": "Sessions, profiles and authentications. Treat as secret/local state.",
    },
    {
        "path": Path("E:/MEDIOEVO_ASSETS"),
        "classification": "PRIVATE_OR_COMMERCIAL_ASSETS",
        "lane": "publishing",
        "intake_action": "MANIFEST_AND_LICENSE_REVIEW_ONLY",
        "notes": "Commercial/private assets, including TCG and Claudio material under review.",
    },
    {
        "path": Path("E:/MEDIOEVO_AUDIO_LIBRARY"),
        "classification": "COMMERCIAL_AUDIO_ASSETS",
        "lane": "publishing",
        "intake_action": "MANIFEST_AND_LICENSE_REVIEW_ONLY",
        "notes": "Observed adjacent audio library; include in commercial manifests only after rights review.",
    },
    {
        "path": Path("E:/Audiobooks"),
        "classification": "COMMERCIAL_AUDIO_ASSETS",
        "lane": "publishing",
        "intake_action": "MANIFEST_AND_LICENSE_REVIEW_ONLY",
        "notes": "Observed adjacent audiobook root; do not copy into open packages.",
    },
]


def file_record(item: dict[str, Any], hash_files: bool) -> dict[str, Any]:
    path = item["path"]
    record = {
        "path": str(path),
        "exists": path.exists(),
        "classification": item["classification"],
        "lane": item["lane"],
        "intake_action": item["intake_action"],
        "target": item["target"],
        "notes": item["notes"],
    }
    if path.exists() and path.is_file():
        stat = path.stat()
        record["bytes"] = stat.st_size
        record["last_write_time_utc"] = datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat()
        if hash_files:
            try:
                record["sha256"] = sha256_file(path)
            except OSError as exc:
                record["sha256_error"] = str(exc)
    return record


def dir_record(item: dict[str, Any]) -> dict[str, Any]:
    path = item["path"]
    record = {
        "path": str(path),
        "exists": path.exists(),
        "classification": item["classification"],
        "lane": item["lane"],
        "intake_action": item["intake_action"],
        "notes": item["notes"],
    }
    if path.exists() and path.is_dir():
        child_dirs = 0
        child_files = 0
        sample_children: list[str] = []
        try:
            for child in sorted(path.iterdir(), key=lambda p: p.name.lower()):
                if child.is_dir():
                    child_dirs += 1
                elif child.is_file():
                    child_files += 1
                if len(sample_children) < 20:
                    sample_children.append(child.name)
        except OSError as exc:
            record["read_error"] = str(exc)
        else:
            record["child_dirs"] = child_dirs
            record["child_files"] = child_files
            record["sample_children"] = sample_children
            record["is_git_repo"] = (path / ".git").exists()
    return record


def build_register(hash_files: bool) -> dict[str, Any]:
    known_paths = {item["path"].resolve() for item in KNOWN_FILES}
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "workspace_root": str(ROOT),
        "rules": [
            "Classify every new source before extracting or copying code.",
            "Absorb selectively; never copy ZIPs wholesale into public or commercial packages.",
            "Keep research claims separate from product claims.",
            "Keep the game and TCG private unless a separate private release lane is explicitly authorized.",
            "Mark thresholds, weights and calibration as DEMO_ONLY until a real dataset exists.",
        ],
        "downloads": [file_record(item, hash_files=hash_files) for item in KNOWN_FILES],
        "unclassified_downloads": unclassified_download_records(known_paths),
        "external_roots": [dir_record(item) for item in EXTERNAL_ROOTS],
    }


def unclassified_download_records(known_paths: set[Path]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    if not DOWNLOADS.exists():
        return records
    try:
        children = sorted(DOWNLOADS.iterdir(), key=lambda path: path.name.lower())
    except OSError:
        return records
    for child in children:
        try:
            resolved = child.resolve()
        except OSError:
            resolved = child
        if resolved in known_paths:
            continue
        if child.name.lower() == "desktop.ini":
            continue
        record = {
            "path": str(child),
            "exists": child.exists(),
            "kind": "directory" if child.is_dir() else "file",
            "classification": "UNCLASSIFIED_DOWNLOAD",
            "lane": "cleanup",
            "intake_action": "CLASSIFY_BEFORE_USE",
            "notes": "Observed in Downloads but not yet assigned to a lane-specific source contract.",
        }
        if child.is_file():
            try:
                stat = child.stat()
            except OSError as exc:
                record["stat_error"] = str(exc)
            else:
                record["bytes"] = stat.st_size
                record["last_write_time_utc"] = datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat()
        records.append(record)
    return records


def md_bool(value: bool) -> str:
    return "yes" if value else "no"


def short_hash(record: dict[str, Any]) -> str:
    value = record.get("sha256")
    if isinstance(value, str):
        return value[:16]
    return record.get("sha256_error", "")


def render_markdown(register: dict[str, Any]) -> str:
    lines = [
        "# SOURCE_INTAKE_REGISTER",
        "",
        f"Generated UTC: `{register['generated_at_utc']}`",
        "",
        "Status: active control document. This is a manifest of sources, not permission to publish.",
        "",
        "## Rules",
        "",
    ]
    for rule in register["rules"]:
        lines.append(f"- {rule}")

    lines.extend(
        [
            "",
            "## Downloads Intake",
            "",
            "| source | exists | bytes | sha256_prefix | classification | lane | intake_action | target |",
            "|---|---:|---:|---|---|---|---|---|",
        ]
    )
    for record in register["downloads"]:
        bytes_value = record.get("bytes", "")
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{record['path']}`",
                    md_bool(bool(record["exists"])),
                    str(bytes_value),
                    short_hash(record),
                    record["classification"],
                    record["lane"],
                    record["intake_action"],
                    record["target"],
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Unclassified Downloads",
            "",
            "| source | kind | exists | bytes | lane | intake_action |",
            "|---|---|---:|---:|---|---|",
        ]
    )
    for record in register["unclassified_downloads"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{record['path']}`",
                    record["kind"],
                    md_bool(bool(record["exists"])),
                    str(record.get("bytes", "")),
                    record["lane"],
                    record["intake_action"],
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## External Roots",
            "",
            "| root | exists | child_dirs | child_files | git_repo | classification | lane | intake_action |",
            "|---|---:|---:|---:|---:|---|---|---|",
        ]
    )
    for record in register["external_roots"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{record['path']}`",
                    md_bool(bool(record["exists"])),
                    str(record.get("child_dirs", "")),
                    str(record.get("child_files", "")),
                    md_bool(bool(record.get("is_git_repo", False))),
                    record["classification"],
                    record["lane"],
                    record["intake_action"],
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Lane Decisions",
            "",
            "| lane | allowed intake | hard boundary |",
            "|---|---|---|",
            "| residueos | Extract only gate/API/store concepts into `apps/residueos`; migrate demo JSON stores to SQLite before product closure. | Calibration and confusion matrix stay `DEMO_ONLY` until a real dataset exists. |",
            "| obsai | Extract metrics, action gate and CLI primitives into `packages/obsai-core`. | No claims of consciousness, physics proof or solved cosmology. |",
            "| lore | Extract canon-to-data fixtures and schemas with evidence fields. | Full books, private lore and game data do not enter open packages. |",
            "| rpg-private | Use manifests, hashes and private repo discipline before edits. | No public packaging, no free release, no source mixing. |",
            "| publishing | Use manifests and checksums for books/assets/products. | No publication claim without Gumroad/web verification. |",
            "| research-boundary | Store as `RESEARCH_ONLY` with falsifier or `PREDICTION_REQUIRED`. | No product copy can imply validated science. |",
            "",
            "## Residue",
            "",
            "- This register does not extract or inspect inside ZIPs.",
            "- Duplicate files in `_ARCHIVO_OBSERVACIONISMO_DUPLICADOS_2026-04-29` are kept as manifest-only evidence.",
            "- Deep recursive counts for `E:\\` roots are intentionally not performed here to avoid slow or unsafe broad scans.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a source-intake register for external MEDIOEVO/Observacionismo sources.")
    add_common_args(parser)
    parser.add_argument("--hash", action="store_true", help="hash known file sources")
    parser.add_argument("--write", action="store_true", help="write SOURCE_INTAKE_REGISTER.md and source_intake_register.json")
    args = parser.parse_args()
    validate_root_arg(args)

    register = build_register(hash_files=args.hash)
    if args.write:
        (ROOT / "SOURCE_INTAKE_REGISTER.md").write_text(render_markdown(register), encoding="utf-8")
        (ROOT / "source_intake_register.json").write_text(json.dumps(register, indent=2, ensure_ascii=False), encoding="utf-8")
        print("wrote SOURCE_INTAKE_REGISTER.md")
        print("wrote source_intake_register.json")
    else:
        print_json(register)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
