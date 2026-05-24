from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
BRAIN_ROOT = Path(r"C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-")
POST_ROOT = BRAIN_ROOT / "POST"

OUT_JSON = ROOT / "docs" / "intake" / "BRAIN_OS_POST_ABSORPTION_CLEANUP_POSTERIOR_2026-05-18.json"
OUT_MD = ROOT / "docs" / "intake" / "BRAIN_OS_POST_ABSORPTION_CLEANUP_POSTERIOR_2026-05-18.md"
FICHA_DIR = ROOT / "docs" / "intake" / "curador_fichas" / "brain_os_post_posterior"
REGISTER = ROOT / "SOURCE_INTAKE_REGISTER.md"

MARKER_START = "<!-- BRAIN_OS_POST_ABSORPTION_CLEANUP_POSTERIOR_2026_05_18_START -->"
MARKER_END = "<!-- BRAIN_OS_POST_ABSORPTION_CLEANUP_POSTERIOR_2026_05_18_END -->"

DENIED_TARGET_ROOTS = [
    ROOT / "runtime",
    ROOT / "apps",
    ROOT / "packages",
]


@dataclass(frozen=True)
class SourceDef:
    source_id: str
    path: Path
    portfolio_set: str | None
    classification: str
    lane: str
    intake_action: str
    action_gate: str
    target_destination: str
    unique_delta: str
    conflict: str
    strong_claim_boundary: str
    falsifier: str
    state: str
    note: str
    already_registered: bool = False


def brain(path: str) -> Path:
    return BRAIN_ROOT / path


def post(path: str) -> Path:
    return POST_ROOT / path


SOURCES = [
    SourceDef(
        "post_container_scope",
        POST_ROOT,
        None,
        "POST_CONTAINER_SCOPE",
        "archive",
        "TOP_LEVEL_INVENTORY_ONLY",
        "REVIEW",
        "docs/intake/curador_fichas/brain_os_post_posterior",
        "Single bounded scope for the POST cleanup pass.",
        "Contains registered, unregistered, duplicate and asset material in one directory.",
        "No claim promoted from directory presence.",
        "Any raw copy from POST into runtime/apps/packages falsifies closure.",
        "MATRIX_ONLY",
        "Directory is kept in place; no move, archive or delete was executed.",
    ),
    SourceDef(
        "post_medi_portfolio_existing",
        post("# 00 — LEER PRIMERO Portafolio MEDI.txt"),
        "post_medi_portfolio",
        "INTERNAL_CANON_PORTFOLIO_SOURCE",
        "claims",
        "EXISTING_FICHA_REFERENCE_ONLY",
        "APPROVE_LOCAL_DOCS_ONLY",
        "docs/intake/BRAIN_OS_POST_CLAIMS_DELTA_2026-05-18.md",
        "Canonical POST portfolio boundary already extracted as claim delta.",
        "Can be confused with a public portfolio if the private boundary is removed.",
        "PublicationGate remains BLOCK for raw portfolio text.",
        "Publishing this full text without a public-safe extraction falsifies the boundary.",
        "ALREADY_REGISTERED_REFERENCE",
        "Original ficha remains docs/intake/curador_fichas/brain_os_post/2026-05-18_portafolio_medi.md.",
        True,
    ),
    SourceDef(
        "post_assets_du_wabi",
        post("Assets Du WABI"),
        None,
        "POST_WABI_ASSET_BATCH",
        "ui_design",
        "ASSET_METADATA_ONLY",
        "REVIEW",
        "docs/design or product UI backlog after asset-rights review",
        "Possible visual vocabulary for Wabi/DUAT interface moodboards.",
        "Image assets may be generated, third-party, duplicated or rights-unclear.",
        "No asset is public-safe or product-ready until provenance is established.",
        "Using any raw image in a release before provenance review falsifies cleanup.",
        "NEEDS_PROVENANCE_REVIEW",
        "Directory-level ficha only; individual images stay unadopted.",
    ),
    SourceDef(
        "post_bu_backup",
        post("BU"),
        None,
        "POST_BACKUP_LEGACY_BATCH",
        "archive",
        "BACKUP_INDEX_ONLY",
        "REVIEW",
        "DUPLICATES_AND_DEAD_CODE.md or future MIGRATION_LOG only after gate",
        "Legacy backup evidence that may explain older POST state.",
        "Backup contents can duplicate or contradict current canon.",
        "No backup file becomes canon without a separate exact-path ficha.",
        "Moving or deleting BU without rollback evidence falsifies the migration gate.",
        "ARCHIVE_REVIEW_REQUIRED",
        "No archive/move/delete was executed.",
    ),
    SourceDef(
        "post_teorias_consciencia_extracted_dir",
        post("MEDIOEVO_OSIT_TEORIAS_COMUNICACION_CONSCIENCIA_v0_1_2026-05-17"),
        None,
        "EXTRACTED_POST_ZIP_SHADOW_COPY",
        "claims",
        "DIRECTORY_MANIFEST_ONLY",
        "BLOCK",
        "docs/intake; compare only against registered ZIP container",
        "Readable extracted view for the already registered theory ZIP.",
        "Extracted directory can bypass ZIP-container-only handling.",
        "Consciousness/communication claims remain formal-lab only.",
        "Importing extracted files into runtime or public staging falsifies ZIP boundary.",
        "SHADOW_COPY_DO_NOT_IMPORT",
        "The ZIP container is already registered; this directory is a shadow copy.",
    ),
    SourceDef(
        "post_trabajo_mejorado_extracted_dir",
        post("MEDIOEVO_OSIT_TRABAJO_MEJORADO_v0_2_2026-05-17"),
        None,
        "EXTRACTED_POST_ZIP_SHADOW_COPY",
        "continuity",
        "DIRECTORY_MANIFEST_ONLY",
        "REVIEW",
        "docs/intake; compare only against registered ZIP container",
        "Readable extracted view for the already registered improved-work ZIP.",
        "May look like a ready implementation package despite unresolved gates.",
        "Runtime import remains blocked until target tests prove each extracted contract.",
        "Copying its code/prompts into runtime/apps/packages falsifies closure.",
        "SHADOW_COPY_DO_NOT_IMPORT",
        "The ZIP container is already registered; this directory is a shadow copy.",
    ),
    SourceDef(
        "post_codcx",
        post("codcx.txt"),
        None,
        "POST_CODEX_COORDINATION_SOURCE",
        "continuity",
        "PROMPT_DELTA_ONLY",
        "REVIEW",
        "NEXT_SESSION_BRIEF/TASKS only as distilled coordination delta",
        "Potential task-routing or prompt-contract detail.",
        "Prompt text can contain overbroad authority or third-party phrasing.",
        "No prompt becomes an agent instruction without boundary review.",
        "Treating prompt text as governing policy falsifies AGENTS hierarchy.",
        "DISTILL_ONLY",
        "Kept as raw source; no prompt adoption.",
    ),
    SourceDef(
        "post_deriva_continuo",
        post("Continúo. Exploración abierta. Deri.md"),
        None,
        "POST_DERIVATION_CONTINUITY_SOURCE",
        "theory",
        "DERIVATION_DELTA_ONLY",
        "REVIEW",
        "docs/intake delta matrix; OSIT formal-lab backlog",
        "May contain derivation steps useful for OSIT formal-lab reconstruction.",
        "Exploratory derivation can conflict with current evidence-gated OSIT claims.",
        "Mathematical or physical claims require falsifiers and current tests.",
        "Using derivation prose as proof falsifies the ScienceClaimGate.",
        "REVIEW_FOR_FORMAL_LAB",
        "No formula or claim imported into runtime.",
    ),
    SourceDef(
        "post_entendido_pendiente",
        post("Entendido. au poe favior = aun por.txt"),
        None,
        "POST_PENDING_ANALYSIS_SOURCE",
        "continuity",
        "PENDING_DELTA_ONLY",
        "REVIEW",
        "TASKS/RISKS as distilled pending items only",
        "May carry unfinished analysis or pending-action language.",
        "Filename and content suggest rough operator residue, not polished canon.",
        "No pending item is closure evidence.",
        "Marking unfinished analysis as completed falsifies Phi_eff evidence.",
        "PENDING_REVIEW",
        "Useful only for queue extraction.",
    ),
    SourceDef(
        "post_doi_ioi_rigor",
        post("Voy a aplicar DO → IOI con rigor. T.txt"),
        None,
        "POST_DO_IOI_METHOD_SOURCE",
        "theory",
        "METHOD_DELTA_ONLY",
        "REVIEW",
        "docs/intake; DUAT/OSIT method backlog",
        "Possible DO to IOI mapping language for selective extraction workflow.",
        "Method prose can be mistaken for implemented pipeline.",
        "Method claims need local fixture tests before runtime use.",
        "Claiming implementation from method text falsifies runtime evidence.",
        "METHOD_REVIEW",
        "No method code was generated from this source.",
    ),
    SourceDef(
        "post_osit_exploracion_pdf",
        post("OSIT-EXPLORACION-COMPLETA-v2-2026-0518.pdf"),
        None,
        "POST_OSIT_EXPLORATION_PDF_SOURCE",
        "claims",
        "PDF_INSIGHT_ONLY",
        "REVIEW",
        "docs/intake; OSIT claim falsifier queue",
        "Potential summary of OSIT exploration scope and open questions.",
        "PDF may repeat strong claims without primary evidence.",
        "Exploration claims stay REVIEW until falsifier/test evidence exists.",
        "Public or runtime use before claim review falsifies the claim boundary.",
        "CLAIM_REVIEW_REQUIRED",
        "PDF is not extracted or republished.",
    ),
    SourceDef(
        "post_osit_resolucion_pdf",
        post("OSIT-RESOLUCION-BLOQUEOS-2026-0518.pdf"),
        None,
        "POST_OSIT_BLOCKER_RESOLUTION_PDF_SOURCE",
        "runtime",
        "PDF_BLOCKER_DELTA_ONLY",
        "REVIEW",
        "NEXT_SESSION_BRIEF; OSIT runtime backlog after tests",
        "May list blocker-resolution language for OSIT work.",
        "Resolution wording can overstate implementation closure.",
        "Resolved blockers require reproduced commands/tests.",
        "Marking blocker resolution without current evidence falsifies closure.",
        "BLOCKER_REVIEW_REQUIRED",
        "PDF kept as source only.",
    ),
    SourceDef(
        "post_osit_resolucion_pdf_duplicate",
        post("OSIT-RESOLUCION-BLOQUEOS-2026-0518 (1).pdf"),
        None,
        "POST_OSIT_BLOCKER_RESOLUTION_DUPLICATE_CANDIDATE",
        "archive",
        "DUPLICATE_EVIDENCE_ONLY",
        "REVIEW",
        "DUPLICATES_AND_DEAD_CODE.md after exact duplicate gate",
        "Potential exact duplicate of OSIT blocker-resolution PDF.",
        "Duplicate filename can create two competing source truths.",
        "Duplicate status must be hash-proven before any archive action.",
        "Deleting/moving duplicate without MIGRATION_LOG falsifies cleanup gate.",
        "DUPLICATE_REVIEW_REQUIRED",
        "No duplicate cleanup was executed.",
    ),
    SourceDef(
        "post_spin_torsion_ansaz_pdf",
        post("OSIT-SPIN-TORSION-ANSAZ.pdf"),
        None,
        "POST_SPIN_TORSION_STRONG_CLAIM_SOURCE",
        "claims",
        "STRONG_CLAIM_REVIEW_ONLY",
        "BLOCK",
        "claim falsifier queue; no public copy",
        "May surface terms that need explicit OSIT physics boundaries.",
        "Spin/torsion language risks being read as validated physics.",
        "ScienceClaimGate: BLOCK as public/validated claim.",
        "Using this as proof of physics falsifies the formal-lab boundary.",
        "CLAIM_BLOCKED_PENDING_PRIMARY_EVIDENCE",
        "No science claim imported.",
    ),
    SourceDef(
        "post_spin_torsion_scale_pdf",
        post("OSIT-SPIN-TORSION-SCALE.pdf"),
        None,
        "POST_SPIN_TORSION_SCALE_STRONG_CLAIM_SOURCE",
        "claims",
        "STRONG_CLAIM_REVIEW_ONLY",
        "BLOCK",
        "claim falsifier queue; no public copy",
        "May define scale-language requiring a formal-lab downgrade.",
        "Scale claims can exceed current OSIT evidence.",
        "ScienceClaimGate: BLOCK as public/validated claim.",
        "Using this as proof of scale physics falsifies the formal-lab boundary.",
        "CLAIM_BLOCKED_PENDING_PRIMARY_EVIDENCE",
        "No science claim imported.",
    ),
    SourceDef(
        "brain_os_identity_portfolio",
        brain("01_PORTFOLIO_AND_IDENTITY.md"),
        "brain_os_identity_portfolio",
        "BRAIN_OS_IDENTITY_PORTFOLIO_SOURCE",
        "portfolio",
        "PORTFOLIO_BOUNDARY_ONLY",
        "REVIEW",
        "docs/intake; public/private portfolio boundary matrix",
        "Human identity and portfolio framing for MEDIOEVO/BRAIN_OS.",
        "Identity material may not be public-safe as-is.",
        "Public profile copy requires separate public-safe extraction.",
        "Publishing raw identity text falsifies privacy boundary.",
        "PUBLIC_SAFE_EXTRACTION_REQUIRED",
        "Registered as portfolio source, not publication copy.",
    ),
    SourceDef(
        "osit_agent_knowledge_portfolio_md",
        brain("MEDIOEVO_OSIT_AGENT_KNOWLEDGE_PORTFOLIO_v1_0.md"),
        "osit_agent_knowledge_portfolio",
        "OSIT_AGENT_KNOWLEDGE_PORTFOLIO_MD_SOURCE",
        "portfolio",
        "PORTFOLIO_DELTA_ONLY",
        "REVIEW",
        "docs/intake; OSIT agent knowledge public/private split",
        "Structured knowledge map for OSIT agent onboarding.",
        "Can blend internal theory, agent prompts and public-facing summary.",
        "Agent knowledge claims require layer split and claim gates.",
        "Using it as a raw agent prompt falsifies selective extraction law.",
        "SELECTIVE_AGENT_KNOWLEDGE_ONLY",
        "Markdown is source material, not an active prompt.",
    ),
    SourceDef(
        "osit_agent_knowledge_portfolio_pdf",
        brain("MEDIOEVO_OSIT_AGENT_KNOWLEDGE_PORTFOLIO_v1_0.pdf"),
        "osit_agent_knowledge_portfolio",
        "OSIT_AGENT_KNOWLEDGE_PORTFOLIO_PDF_SOURCE",
        "portfolio",
        "PDF_PORTFOLIO_REFERENCE_ONLY",
        "REVIEW",
        "docs/intake; distribution artifact review",
        "Rendered portfolio artifact matching the knowledge portfolio lane.",
        "PDF distribution can be confused with approval to publish.",
        "PDF remains internal until public-safe review and scan.",
        "External upload or publication falsifies PublicationGate.",
        "NO_PUBLICATION",
        "PDF is not repackaged.",
    ),
    SourceDef(
        "osit_knowledge_folder_zip",
        brain("MEDIOEVO_OSIT_KNOWLEDGE_FOLDER_v1_0.zip"),
        "osit_agent_knowledge_portfolio",
        "OSIT_KNOWLEDGE_FOLDER_ZIP_SOURCE",
        "portfolio",
        "ZIP_METADATA_ONLY",
        "REVIEW",
        "docs/intake; ZIP manifest review only",
        "Packaged knowledge folder may be useful as a distribution inventory.",
        "ZIP may hide files that need per-file gates.",
        "ZIP contents remain unadopted until per-member fichas exist.",
        "Extracting ZIP into runtime/apps/packages falsifies ZIP boundary.",
        "ZIP_CONTAINER_REVIEW",
        "No extraction was executed.",
    ),
]


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_")[:80] or "source"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def iter_files(path: Path) -> list[Path]:
    denied_names = {".git", "node_modules", ".venv", "__pycache__", ".pytest_cache"}
    files: list[Path] = []
    for child in sorted(path.rglob("*")):
        if any(part in denied_names for part in child.parts):
            continue
        if child.is_file():
            files.append(child)
    return files


def sha256_dir(path: Path) -> tuple[str, int, int]:
    digest = hashlib.sha256()
    file_count = 0
    byte_count = 0
    for child in iter_files(path):
        rel_path = child.relative_to(path).as_posix()
        file_hash = sha256_file(child)
        size = child.stat().st_size
        digest.update(rel_path.encode("utf-8", "surrogatepass"))
        digest.update(b"\0")
        digest.update(str(size).encode("ascii"))
        digest.update(b"\0")
        digest.update(file_hash.encode("ascii"))
        digest.update(b"\n")
        file_count += 1
        byte_count += size
    return digest.hexdigest().upper(), file_count, byte_count


def hash_source(path: Path) -> dict[str, Any]:
    exists = path.exists()
    if not exists:
        return {
            "exists": False,
            "hash_kind": "missing",
            "sha256": "NOT_FOUND",
            "file_count": 0,
            "byte_count": 0,
        }
    if path.is_dir():
        sha, file_count, byte_count = sha256_dir(path)
        return {
            "exists": True,
            "hash_kind": "directory_tree_sha256",
            "sha256": sha,
            "file_count": file_count,
            "byte_count": byte_count,
        }
    size = path.stat().st_size
    return {
        "exists": True,
        "hash_kind": "file_sha256",
        "sha256": sha256_file(path),
        "file_count": 1,
        "byte_count": size,
    }


def rel_ficha(source_id: str) -> str:
    return f"docs/intake/curador_fichas/brain_os_post_posterior/2026-05-18_{slugify(source_id)}.md"


def source_record(defn: SourceDef) -> dict[str, Any]:
    hash_info = hash_source(defn.path)
    ficha = rel_ficha(defn.source_id)
    record = {
        "id": defn.source_id,
        "path": str(defn.path),
        "portfolio_set": defn.portfolio_set,
        "classification": defn.classification,
        "lane": defn.lane,
        "intake_action": defn.intake_action,
        "action_gate": defn.action_gate,
        "publication_gate": "BLOCK",
        "runtime_import": "BLOCK",
        "raw_adoption": "BLOCK",
        "target_destination": defn.target_destination,
        "state": defn.state,
        "note": defn.note,
        "already_registered": defn.already_registered,
        "ficha": ficha,
        **hash_info,
    }
    return record


def duplicate_candidates(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_hash: dict[str, list[dict[str, Any]]] = {}
    for record in records:
        if record["exists"] and record["hash_kind"] == "file_sha256":
            by_hash.setdefault(record["sha256"], []).append(record)
    return [
        {
            "sha256": sha,
            "paths": [item["path"] for item in items],
            "gate": "REVIEW_BEFORE_MIGRATION",
            "action": "document only; no move/delete executed",
        }
        for sha, items in sorted(by_hash.items())
        if len(items) > 1
    ]


def raw_copy_check(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    source_hashes = {
        record["sha256"]: record
        for record in records
        if record["exists"] and record["hash_kind"] == "file_sha256"
    }
    source_paths = {record["path"].lower() for record in source_hashes.values()}
    source_sizes = {record["byte_count"] for record in source_hashes.values()}
    checks: list[dict[str, Any]] = []
    for target_root in DENIED_TARGET_ROOTS:
        matches: list[str] = []
        if target_root.exists():
            for path in iter_files(target_root):
                try:
                    if path.stat().st_size not in source_sizes:
                        continue
                    if str(path).lower() in source_paths:
                        continue
                    file_hash = sha256_file(path)
                except OSError:
                    continue
                if file_hash in source_hashes:
                    matches.append(str(path))
        checks.append(
            {
                "target_root": str(target_root),
                "status": "PASS_NO_RAW_SOURCE_HASH_MATCH" if not matches else "FAIL_RAW_SOURCE_HASH_MATCH",
                "matches": matches,
            }
        )
    return checks


def build_matrix() -> dict[str, Any]:
    records = [source_record(defn) for defn in SOURCES]
    deltas = [
        {
            "id": defn.source_id,
            "source_path": str(defn.path),
            "source_sha256": records[index]["sha256"],
            "source_hash_kind": records[index]["hash_kind"],
            "portfolio_set": defn.portfolio_set,
            "lane": defn.lane,
            "unique_contribution": defn.unique_delta,
            "conflict": defn.conflict,
            "strong_claim_boundary": defn.strong_claim_boundary,
            "falsifier": defn.falsifier,
            "destination": defn.target_destination,
            "state": defn.state,
            "action_gate": defn.action_gate,
        }
        for index, defn in enumerate(SOURCES)
    ]
    portfolio_sets = {
        "post_medi_portfolio": [
            r"C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\POST\# 00 — LEER PRIMERO Portafolio MEDI.txt"
        ],
        "brain_os_identity_portfolio": [
            r"C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\01_PORTFOLIO_AND_IDENTITY.md"
        ],
        "osit_agent_knowledge_portfolio": [
            r"C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\MEDIOEVO_OSIT_AGENT_KNOWLEDGE_PORTFOLIO_v1_0.md",
            r"C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\MEDIOEVO_OSIT_AGENT_KNOWLEDGE_PORTFOLIO_v1_0.pdf",
            r"C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\MEDIOEVO_OSIT_KNOWLEDGE_FOLDER_v1_0.zip",
        ],
    }
    return {
        "schema": "medioevo.brain_os_post_absorption_cleanup.v1",
        "generated_at": "2026-05-18",
        "scope": "POST top-level posterior cleanup plus three BRAIN_OS portfolio sets",
        "source_count": len(records),
        "new_registration_count": sum(1 for record in records if not record["already_registered"]),
        "portfolio_set_count": len(portfolio_sets),
        "gate_summary": {
            "PublicationGate": "BLOCK",
            "RuntimeImportGate": "BLOCK",
            "RawAdoption": "BLOCK",
            "MigrationMoveDelete": "BLOCK_WITHOUT_MIGRATION_LOG_ROLLBACK_ACTIONGATE",
        },
        "sources": records,
        "portfolio_sets": portfolio_sets,
        "delta_matrix": deltas,
        "duplicate_candidates": duplicate_candidates(records),
        "raw_copy_check": raw_copy_check(records),
        "test_plan": [
            "python tools/release/build_brain_os_post_absorption_cleanup.py",
            "python tools/release/curador_preflight.py --path <exact source path>",
            "python tools/release/scan_secrets.py --path docs/intake --json",
            "python -m pytest tests/release/test_brain_os_post_absorption_cleanup.py -q",
            "rg -n \"PublicationGate[=:]+APPROVE|RuntimeImport[=:]+APPROVE|RawAdoption[=:]+APPROVE\" docs/intake/BRAIN_OS_POST_ABSORPTION_CLEANUP_POSTERIOR_2026-05-18.md docs/intake/BRAIN_OS_POST_ABSORPTION_CLEANUP_POSTERIOR_2026-05-18.json",
        ],
    }


def md_escape(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def render_matrix_md(matrix: dict[str, Any]) -> str:
    rows = [
        "| source | lane | sha256 | action | destino | estado |",
        "|---|---|---|---|---|---|",
    ]
    for source in matrix["sources"]:
        rows.append(
            "| "
            + " | ".join(
                [
                    f"`{md_escape(source['path'])}`",
                    f"`{source['lane']}`",
                    f"`{source['sha256']}`",
                    f"`{source['intake_action']}`",
                    md_escape(source["target_destination"]),
                    f"`{source['state']}`",
                ]
            )
            + " |"
        )
    delta_rows = [
        "| fuente | aporte unico | conflicto | claim/falsificador | destino | estado |",
        "|---|---|---|---|---|---|",
    ]
    for delta in matrix["delta_matrix"]:
        delta_rows.append(
            "| "
            + " | ".join(
                [
                    f"`{md_escape(delta['id'])}`",
                    md_escape(delta["unique_contribution"]),
                    md_escape(delta["conflict"]),
                    md_escape(delta["strong_claim_boundary"] + " Falsifier: " + delta["falsifier"]),
                    md_escape(delta["destination"]),
                    f"`{delta['state']}`",
                ]
            )
            + " |"
        )
    raw_rows = [
        "| target | status | matches |",
        "|---|---|---|",
    ]
    for check in matrix["raw_copy_check"]:
        raw_rows.append(
            f"| `{check['target_root']}` | `{check['status']}` | `{len(check['matches'])}` |"
        )
    return "\n".join(
        [
            "# BRAIN_OS POST Absorcion y Limpieza Posterior - 2026-05-18",
            "",
            "Scope: POST top-level posterior cleanup plus three BRAIN_OS portfolio sets.",
            "",
            "Gates:",
            "",
            "- `PublicationGate`: `BLOCK`.",
            "- `RuntimeImportGate`: `BLOCK`.",
            "- `RawAdoption`: `BLOCK`.",
            "- `MigrationMoveDelete`: `BLOCK_WITHOUT_MIGRATION_LOG_ROLLBACK_ACTIONGATE`.",
            "",
            "No source was moved, deleted, archived, published, extracted into runtime, copied into apps/packages, or adopted as raw canon.",
            "",
            "## Exact-Path Register",
            "",
            *rows,
            "",
            "## Canonico De Deltas Utiles",
            "",
            *delta_rows,
            "",
            "## Duplicate Candidates",
            "",
            *(
                [
                    f"- `{item['sha256']}`: "
                    + ", ".join(f"`{path}`" for path in item["paths"])
                    + " -> `REVIEW_BEFORE_MIGRATION`."
                    for item in matrix["duplicate_candidates"]
                ]
                or ["- No file-level duplicate source hashes detected inside this matrix."]
            ),
            "",
            "## Raw Copy Check",
            "",
            *raw_rows,
            "",
            "## Next Gate",
            "",
            "The only approved next action is to review one exact ficha, pick one delta, add a falsifier/test in the proper lane, and keep publication/runtime import blocked until that test passes.",
            "",
        ]
    )


def render_ficha(record: dict[str, Any], delta: dict[str, Any]) -> str:
    return "\n".join(
        [
            f"# Ficha Curador - {record['id']}",
            "",
            f"- source_path: `{record['path']}`",
            f"- exists: `{record['exists']}`",
            f"- hash_kind: `{record['hash_kind']}`",
            f"- sha256: `{record['sha256']}`",
            f"- file_count: `{record['file_count']}`",
            f"- byte_count: `{record['byte_count']}`",
            f"- classification: `{record['classification']}`",
            f"- lane: `{record['lane']}`",
            f"- intake_action: `{record['intake_action']}`",
            f"- action_gate: `{record['action_gate']}`",
            f"- PublicationGate: `{record['publication_gate']}`",
            f"- RuntimeImportGate: `{record['runtime_import']}`",
            f"- RawAdoption: `{record['raw_adoption']}`",
            f"- target_destination: `{record['target_destination']}`",
            f"- state: `{record['state']}`",
            "",
            "## Delta",
            "",
            f"- aporte_unico: {delta['unique_contribution']}",
            f"- conflicto: {delta['conflict']}",
            f"- claim_boundary: {delta['strong_claim_boundary']}",
            f"- falsificador: {delta['falsifier']}",
            "",
            "## Decision",
            "",
            "`DOCUMENTED_FOR_SELECTIVE_EXTRACTION_ONLY`.",
            "",
            "No move, delete, archive, runtime import, publication, deploy, push or raw adoption is authorized by this ficha.",
            "",
        ]
    )


def render_register_section(matrix: dict[str, Any]) -> str:
    rows = [
        "| source | exists | hash_kind | sha256 | classification | lane | intake_action | gate | ficha |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for source in matrix["sources"]:
        rows.append(
            "| "
            + " | ".join(
                [
                    f"`{md_escape(source['path'])}`",
                    "yes" if source["exists"] else "no",
                    f"`{source['hash_kind']}`",
                    f"`{source['sha256']}`",
                    f"`{source['classification']}`",
                    f"`{source['lane']}`",
                    f"`{source['intake_action']}`",
                    f"`{source['action_gate']} / PublicationGate=BLOCK / RuntimeImport=BLOCK / RawAdoption=BLOCK`",
                    f"`{source['ficha']}`",
                ]
            )
            + " |"
        )
    return "\n".join(
        [
            MARKER_START,
            "## 2026-05-18 - BRAIN_OS POST Absorcion y Limpieza Posterior",
            "",
            "Scope: exact-path register for POST posterior cleanup and the three BRAIN_OS portfolio sets. This section is documentary only: no movement, deletion, archive, runtime import, publication or raw adoption.",
            "",
            *rows,
            "",
            "Decision:",
            "",
            "- `Adopcion cruda`: `BLOCK`.",
            "- `RuntimeImport`: `BLOCK`.",
            "- `PublicationGate`: `BLOCK`.",
            "- `MIGRATION_LOG` required before any move/archive/delete by exact path.",
            "- Useful deltas flow only through `docs/intake/BRAIN_OS_POST_ABSORPTION_CLEANUP_POSTERIOR_2026-05-18.*` and per-path fichas.",
            "",
            MARKER_END,
            "",
        ]
    )


def update_register(section: str) -> None:
    text = REGISTER.read_text(encoding="utf-8")
    if MARKER_START in text and MARKER_END in text:
        pattern = re.compile(re.escape(MARKER_START) + r".*?" + re.escape(MARKER_END) + r"\n?", re.S)
        text = pattern.sub(lambda _match: section, text)
    else:
        text = text.rstrip() + "\n\n" + section
    REGISTER.write_text(text, encoding="utf-8")


def main() -> int:
    FICHA_DIR.mkdir(parents=True, exist_ok=True)
    matrix = build_matrix()
    OUT_JSON.write_text(json.dumps(matrix, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    OUT_MD.write_text(render_matrix_md(matrix), encoding="utf-8")
    deltas = {delta["id"]: delta for delta in matrix["delta_matrix"]}
    for source in matrix["sources"]:
        ficha_path = ROOT / source["ficha"]
        ficha_path.write_text(render_ficha(source, deltas[source["id"]]), encoding="utf-8")
    update_register(render_register_section(matrix))
    print(
        json.dumps(
            {
                "matrix": str(OUT_JSON),
                "sources": matrix["source_count"],
                "new_registrations": matrix["new_registration_count"],
                "portfolio_sets": matrix["portfolio_set_count"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
