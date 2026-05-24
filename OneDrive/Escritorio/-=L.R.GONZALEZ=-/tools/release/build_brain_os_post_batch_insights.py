from __future__ import annotations

import hashlib
import json
import re
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST_ROOT = Path(r"C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\POST")
MATRIX_JSON = ROOT / "docs" / "intake" / "BRAIN_OS_POST_BATCH_INSIGHTS_MATRIX_2026-05-18.json"
MATRIX_MD = ROOT / "docs" / "intake" / "BRAIN_OS_POST_BATCH_INSIGHTS_MATRIX_2026-05-18.md"
FICHA_DIR = ROOT / "docs" / "intake" / "curador_fichas" / "brain_os_post"
REGISTER = ROOT / "SOURCE_INTAKE_REGISTER.md"

ALIAS_NOT_FOUND = (
    r"C:\Users\L-Tyr\OneDrive\Escritorio\-= BRAIN_OS =-\POST"
    r"\# 00  LEER PRIMERO Portafolio MEDI.txt"
)

TERMS = [
    "PASS",
    "PROBADO",
    "Benchmark",
    "consciencia",
    "conciencia",
    "AGI",
    "medicina",
    "secret",
    "token",
    "derivada",
    "derivacion",
    "derivación",
    "fisica",
    "física",
    "publicacion",
    "publicación",
    "publication",
    "ActionGate",
    "GhostGate",
    "ObservationEnvelope",
    "Handoff",
    "Phi_eff",
    "Phi",
    "Shannon",
    "arXiv",
    "quant-ph",
    "quantum",
    "thermodynamic",
    "100%",
    "AI generated",
    "Wikipedia",
    "Reddit",
    "Instagram",
    "TikTok",
    "YouTube",
    "Jung",
    "sueño",
    "neurobiología",
    "hipnagogia",
    "metacognición",
    "prefrontal",
    "cósmica",
    "nmap",
    "nikto",
    "maltego",
    "recon-ng",
    "metasploit",
    "sqlmap",
    "john",
    "hashcat",
    "payload",
    "shell",
    "dump",
    "bypass",
    "exfiltration",
    "exfiltración",
    "cookie",
    "password",
]


@dataclass(frozen=True)
class SourceDef:
    source_id: str
    filename: str
    classification: str
    lane: str
    intake_action: str
    gate: str
    ficha_slug: str | None
    target_lane: str
    useful_deltas: tuple[str, ...]
    rejected_material: tuple[str, ...]
    claim_boundary: str
    evidence_hint: str
    previously_registered: bool = False

    @property
    def path(self) -> Path:
        return POST_ROOT / self.filename


SOURCE_DEFS = [
    SourceDef(
        "portfolio_medi_post",
        "# 00 — LEER PRIMERO Portafolio MEDI.txt",
        "INTERNAL_CANON_PORTFOLIO_SOURCE",
        "claim-boundary",
        "SELECTIVE_CLAIM_EXTRACTION_ONLY",
        "APPROVE_LOCAL_DOCS_ONLY",
        None,
        "docs/intake; claim-boundary docs; publication review",
        (
            "Canonical POST entrypoint and public/private boundary language.",
            "Explicit PublicationGate and overclaim downgrade vocabulary.",
        ),
        (
            "Alias registration for a path that does not exist.",
            "Publication or wholesale canon import.",
        ),
        "BLOCK_PUBLICATION_AND_RAW_ADOPTION",
        "Already fichado in the first POST selective extraction pass.",
        True,
    ),
    SourceDef(
        "deep_research_report_post",
        "deep-research-report.md",
        "POST_SYNTHESIS_REVIEW_SOURCE",
        "claim-boundary",
        "INSIGHT_DELTA_ONLY",
        "REVIEW",
        "2026-05-18_batch_deep_research_report.md",
        "docs/intake; claims register; falsifier queue",
        (
            "Separates operational OSIT value from unproven physics claims.",
            "Surfaces benchmark, Handoff and ObservationEnvelope as evidence-dependent contracts.",
        ),
        (
            "Self-reported benchmark or PASS language as proof.",
            "Citation markers or research synthesis as primary evidence.",
        ),
        "REQUIRES_EVIDENCE_FOR_STRONG_SCIENCE_AND_BENCHMARK_CLAIMS",
        "Useful as reviewer synthesis; not a primary-source proof.",
    ),
    SourceDef(
        "cloud_gate_pdf_post",
        "Del Cálculo al Gate_ Cómo OSIT Transforma la Planificación en la Nube en Acciones Locales Seguras y Auditables.pdf",
        "POST_PDF_CLOUD_GATE_REVIEW_SOURCE",
        "gate",
        "PDF_INSIGHT_ONLY",
        "REVIEW",
        "2026-05-18_batch_cloud_gate_pdf.md",
        "ActionGate docs; cloud/local planning review; no runtime import",
        (
            "Frames cloud planning as local gated execution.",
            "Links ActionGate/GhostGate vocabulary to secret and token boundaries.",
        ),
        (
            "Cloud execution or provider configuration changes.",
            "Any secret/token handling beyond boundary documentation.",
        ),
        "CLOUD_PLAN_REQUIRES_LOCAL_ACTIONGATE_AND_SECRET_BOUNDARY",
        "PDF text was read locally for metadata and anchors only.",
    ),
    SourceDef(
        "noumeno_informacional_post",
        "El Noúmeno Informacional Unificació.txt",
        "POST_STRONG_THEORY_SOURCE",
        "claim-boundary",
        "STRONG_CLAIM_REVIEW_ONLY",
        "BLOCK",
        "2026-05-18_batch_noumeno_informacional.md",
        "research backlog; falsifier queue; public copy exclusion",
        (
            "Identifies physics/consciousness claims that need formal-lab demotion.",
            "Keeps ActionGate/GhostGate overlap as vocabulary only.",
        ),
        (
            "Consciousness or universal physics claims as fact.",
            "Public-facing publication or runtime canonization.",
        ),
        "BLOCK_STRONG_PHYSICS_OR_CONSCIOUSNESS_AS_FACT",
        "High overclaim density; use only as a negative-boundary source.",
    ),
    SourceDef(
        "estado_arquitectonico_rev_post",
        "ESTADO ANÁLISIS_ARQUITECTÓNICO  REV.txt",
        "POST_ARCHITECTURE_REVIEW_STATUS",
        "gate",
        "ARCHITECTURE_DELTA_ONLY",
        "APPROVE_LOCAL_DOCS_ONLY",
        "2026-05-18_batch_estado_arquitectonico_rev.md",
        "ActionGate/GhostGate/ScienceClaimGate docs; continuity reports",
        (
            "Reinforces ActionGate, GhostGate and ScienceClaimGate separation.",
            "Useful concise status/handoff shape for agent closure.",
        ),
        (
            "Runtime refactor from status text.",
            "Treating praise/evaluation as test evidence.",
        ),
        "OPERATIONAL_GATE_VOCABULARY_ONLY",
        "Short status source with direct line anchors.",
    ),
    SourceDef(
        "estado_post",
        "ESTADO.txt",
        "POST_FORMAL_LAB_STATUS_SOURCE",
        "math-state",
        "CLAIM_BOUNDARY_DELTA_ONLY",
        "REVIEW",
        "2026-05-18_batch_estado.md",
        "formal-lab backlog; math/state claim boundary",
        (
            "Separates physical truth, formal-lab possibility, metaphor and unproven limit.",
            "Connects R/Phi language to bounded research helpers.",
        ),
        (
            "Derivation language as approved science.",
            "Consciousness/physics claims without local falsifiers.",
        ),
        "FORMAL_LAB_NOT_SCIENTIFIC_PROOF",
        "Useful boundary source; strong derivation terms stay downgraded.",
    ),
    SourceDef(
        "estadoqqqqq_post",
        "ESTADOqqqqq.txt",
        "POST_BATCH_META_REVIEW_SOURCE",
        "continuity",
        "CURATED_META_REVIEW_ONLY",
        "APPROVE_LOCAL_DOCS_ONLY",
        "2026-05-18_batch_estadoqqqqq.md",
        "batch intake decisions; deduplication log; next-session handoff",
        (
            "Names which POST docs are direct, cleanup-needed or dangerous without demotion.",
            "Reinforces ObservationEnvelope, Handoff and GhostGate as existing contracts.",
        ),
        (
            "Using the meta-review as a substitute for fichas.",
            "Adopting dangerous/overclaim sources without demotion.",
        ),
        "META_REVIEW_GUIDANCE_ONLY",
        "Useful for prioritization and duplicate prevention.",
    ),
    SourceDef(
        "estado_security_workbench_post",
        "ESTADO222222222.txt",
        "POST_ETHICAL_SECURITY_WORKBENCH_SOURCE",
        "security",
        "DEFENSIVE_SECURITY_WORKBENCH_INSIGHT_ONLY",
        "REVIEW",
        "2026-05-18_batch_estado_security_workbench.md",
        "packages/open-dev/obs-safe-integration-kit; docs/intake; future Wabi wrapper task packet",
        (
            "Defines MEDIOEVO Ethical Security Workbench as defensive, local-first and owner-authorized.",
            "Requires ScopeRegistry, Security ActionGate, DryRunPlan, OutputSanitizer, RiskMapper, WitnessLog and Handoff before any tool execution.",
            "Separates safe defensive checks from OSINT and offensive validators with APPROVE/REVIEW/BLOCK defaults.",
        ),
        (
            "Running Nmap, Nikto, sqlmap, Metasploit, John, hashcat, Maltego or recon-ng directly from intake text.",
            "Scanning third-party targets or external infrastructure without explicit authorization.",
            "Payloads, shells, dumps, bypass, exfiltration, credential handling or password cracking.",
            "Adding Wabi CLI commands before the obs-safe contract is tested.",
        ),
        "DEFENSIVE_DRY_RUN_FIXTURE_ONLY_SECURITY_CONTRACT",
        "New exact POST source for architecture and safety contracts; no offensive execution authorized.",
    ),
    SourceDef(
        "ingenieria_observacionista_inversa_post",
        "Ingeniería Observacionista Inversa_ Un Modelo Operativo para Elevar la Eficiencia de la Investigación desde un Estado Óptimo.md",
        "POST_ENGINEERING_METHOD_SOURCE",
        "math-state",
        "METHOD_DELTA_ONLY",
        "REVIEW",
        "2026-05-18_batch_ingenieria_observacionista_inversa.md",
        "MOI/IOI method docs; Phi_eff calibration backlog; no runtime import",
        (
            "Defines IOI as operator/gate method rather than raw theory expansion.",
            "Links Phi_eff, Handoff, ObservationEnvelope and ActionGate to traceability.",
        ),
        (
            "PROBADO language as accepted proof.",
            "Direct implementation in Wabi/Claudio without tests.",
        ),
        "METHOD_AS_REVIEWED_DOCS_ONLY_UNTIL_TESTED",
        "Useful method source; still needs target-lane tests.",
    ),
    SourceDef(
        "zip_truthgate_eic_v0_3_post",
        "MEDIOEVO_OSIT_DOCUMENTOS_ACTUALIZADOS_TRUTHGATE_EIC_v0_3_2026-05-17.zip",
        "ZIP_CONTAINER_TRUTHGATE_EIC_SOURCE",
        "gate",
        "ZIP_METADATA_AND_MEMBER_ANCHORS_ONLY",
        "REVIEW",
        "2026-05-18_batch_zip_truthgate_eic_v0_3.md",
        "TruthGate/EIC docs; claims/source cards; tests roadmap",
        (
            "Container reinforces TruthGate, claims register, SourceCards and falsifier docs.",
            "Internal members can be referenced as zip_path::member anchors only.",
        ),
        (
            "Extraction into runtime or repo tree.",
            "Importing internal code or claims as approved.",
        ),
        "ZIP_CONTAINER_NO_EXTRACTION_NO_RUNTIME_IMPORT",
        "ZIP passed testzip and has no suspicious member names.",
    ),
    SourceDef(
        "zip_formalizados_v2_1_post",
        "MEDIOEVO_OSIT_DOCUMENTOS_FORMALIZADOS_v2_1_2026-05-17.zip",
        "ZIP_CONTAINER_FORMALIZED_DOCS_SOURCE",
        "math-state",
        "ZIP_METADATA_AND_MEMBER_ANCHORS_ONLY",
        "REVIEW",
        "2026-05-18_batch_zip_formalizados_v2_1.md",
        "formalized docs; math/tests review; runtime import blocked",
        (
            "Contains formalized docs plus an internal engine member that must remain non-imported.",
            "ObservationEnvelope and TruthGate terms converge with existing local contracts.",
        ),
        (
            "Importing osit_epistemic_engine_v2_1.py.",
            "Treating PASS markers as verified tests.",
        ),
        "RUNTIME_CODE_IN_CONTAINER_REQUIRES_REBUILD_AND_TESTS",
        "ZIP passed testzip and has no suspicious member names.",
    ),
    SourceDef(
        "zip_teorias_consciencia_v0_1_post",
        "MEDIOEVO_OSIT_TEORIAS_COMUNICACION_CONSCIENCIA_v0_1_2026-05-17.zip",
        "ZIP_CONTAINER_THEORY_CONSCIOUSNESS_SOURCE",
        "claim-boundary",
        "ZIP_METADATA_AND_MEMBER_ANCHORS_ONLY",
        "BLOCK",
        "2026-05-18_batch_zip_teorias_consciencia_v0_1.md",
        "claim demotion; theory backlog; public copy exclusion",
        (
            "Useful for mapping theory/source-card claims to explicit demotion gates.",
            "Highlights consciousness and physics claim density.",
        ),
        (
            "Consciousness/physics claims as fact.",
            "Public or runtime adoption from the container.",
        ),
        "BLOCK_CONSCIOUSNESS_OR_PHYSICS_AS_FACT",
        "ZIP passed testzip and has no suspicious member names.",
    ),
    SourceDef(
        "zip_trabajo_mejorado_v0_2_post",
        "MEDIOEVO_OSIT_TRABAJO_MEJORADO_v0_2_2026-05-17.zip",
        "ZIP_CONTAINER_WORK_IMPROVED_SOURCE",
        "continuity",
        "ZIP_METADATA_AND_MEMBER_ANCHORS_ONLY",
        "REVIEW",
        "2026-05-18_batch_zip_trabajo_mejorado_v0_2.md",
        "public-safe language; QA reconstruction; Handoff; SourceCards",
        (
            "Reinforces public-safe language, QA reconstruction and Handoff discipline.",
            "Good candidate for future selective extraction after target-lane tests.",
        ),
        (
            "Publication from ZIP contents.",
            "Runtime or public package adoption without allowlist and scans.",
        ),
        "PUBLIC_SAFE_COPY_AND_QA_REQUIRE_EVIDENCE",
        "ZIP passed testzip and has no suspicious member names.",
    ),
    SourceDef(
        "osit_epistemic_engine_formal_framework_post",
        "# OSIT Epistemic Engine A Formal Fr.txt",
        "POST_FORMAL_FRAMEWORK_PREPRINT_SOURCE",
        "math-state",
        "FORMAL_FRAMEWORK_INSIGHT_ONLY",
        "REVIEW",
        "2026-05-18_batch_osit_epistemic_engine_formal_framework.md",
        "docs/intake; ActionGate contracts; Wabi/Claudio R/Phi backlog; tests/release",
        (
            "Five-component architecture: R, Phi_eff, regime state machine, GhostGate and Handoff.",
            "Shannon/R bridge and jamming ceiling are useful hypotheses for bounded fixtures and calibration tests.",
            "Embedded Python runtime and benchmark claims become rebuild requirements, not imported code.",
        ),
        (
            "arXiv/quant-ph/preprint status as publication proof.",
            "100% benchmark coverage as accepted local benchmark without current tests.",
            "Quantum, thermodynamic or Shannon identity language as validated science.",
            "Direct import of embedded runtime code.",
        ),
        "FORMAL_FRAMEWORK_REQUIRES_LOCAL_EVIDENCE_NO_RUNTIME_IMPORT",
        "New exact POST source; preflight returned NEEDS_FICHA_BEFORE_USE.",
    ),
    SourceDef(
        "ra_horus_symbolic_agency_post",
        "El Ojo de Ra y el Ojo de Horus (a m.txt",
        "POST_SYMBOLIC_AGENCY_AND_DREAM_MODULES_SOURCE",
        "gate",
        "SYMBOLIC_AGENCY_INSIGHT_ONLY",
        "REVIEW",
        "2026-05-18_batch_ra_horus_symbolic_agency.md",
        "docs/intake; obs-safe-integration-kit agency/generation/knowledge/dynamic-state modules; tests",
        (
            "Four metacognition/control states are useful as an agency state machine requirement.",
            "Pre-action generation gate maps to existing ActionGate discipline without accepting neuroscience claims.",
            "Prerequisite graph, dynamic temperature and R velocity can be rebuilt clean-room as local runtime modules.",
        ),
        (
            "Dream interpretation, Jung, neuroscience, medicine or physics wording as validated fact.",
            "External web snippets as primary evidence.",
            "AI generated image material.",
            "Direct import of embedded Dream Modules code.",
        ),
        "SYMBOLIC_DREAM_PHENOMENOLOGY_AS_ARCHITECTURE_ONLY_REQUIRES_TESTS",
        "New exact POST source; preflight returned NEEDS_FICHA_BEFORE_USE.",
    ),
    SourceDef(
        "osit_epistemic_engine_post",
        "Untitled.txt",
        "OSIT_RUNTIME_PROTOTYPE_SOURCE",
        "runtime-comparison",
        "CODE_INSIGHT_ONLY",
        "REVIEW",
        None,
        "docs/intake; Wabi-Sabi comparison docs; Claudio R/Phi backlog",
        (
            "Existing first-pass prototype source for R/Phi, GhostGate and Handoff comparisons.",
            "Keeps benchmark defects as negative fixtures.",
        ),
        (
            "Direct runtime import.",
            "Claiming benchmark pass.",
        ),
        "CODE_INSIGHT_ONLY_NO_RUNTIME_IMPORT",
        "Already fichado in the first POST selective extraction pass.",
        True,
    ),
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def read_text(path: Path) -> tuple[str, str]:
    data = path.read_bytes()
    for encoding in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
        try:
            return data.decode(encoding), encoding
        except UnicodeDecodeError:
            continue
    return data.decode("utf-8", errors="replace"), "utf-8-replace"


def term_hits(lines: list[str]) -> dict[str, dict[str, Any]]:
    hits: dict[str, list[int]] = {}
    for line_no, line in enumerate(lines, 1):
        for term in TERMS:
            if re.search(re.escape(term), line, re.IGNORECASE):
                hits.setdefault(term, []).append(line_no)
    return {
        term: {"count": len(values), "first_lines": values[:8]}
        for term, values in sorted(hits.items())
    }


def pdf_metadata(path: Path) -> dict[str, Any]:
    try:
        from pypdf import PdfReader
    except ImportError:
        return {"pdf_text_extraction": "UNAVAILABLE", "term_hits": {}}

    reader = PdfReader(str(path))
    lines: list[str] = []
    for page in reader.pages:
        lines.extend((page.extract_text() or "").splitlines())
    return {
        "page_count": len(reader.pages),
        "text_line_count": len(lines),
        "term_hits": term_hits(lines),
    }


def zip_metadata(path: Path) -> dict[str, Any]:
    suspicious = re.compile(r"(secret|token|key|credential|password|\.env)", re.IGNORECASE)
    text_suffixes = {".txt", ".md", ".json", ".py", ".yaml", ".yml", ".csv"}
    member_term_hits: dict[str, dict[str, Any]] = {}
    with zipfile.ZipFile(path) as archive:
        entries = [info.filename for info in archive.infolist()]
        testzip = archive.testzip()
        suspicious_names = [name for name in entries if suspicious.search(name)]
        for info in archive.infolist():
            suffix = Path(info.filename).suffix.lower()
            if info.is_dir() or suffix not in text_suffixes or info.file_size > 500_000:
                continue
            data = archive.read(info)
            text = None
            for encoding in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
                try:
                    text = data.decode(encoding)
                    break
                except UnicodeDecodeError:
                    continue
            if text is None:
                text = data.decode("utf-8", errors="replace")
            hits = term_hits(text.splitlines())
            if hits:
                member_term_hits[info.filename] = {
                    "line_count": len(text.splitlines()),
                    "term_hits": hits,
                }
    return {
        "testzip": testzip,
        "entry_count": len(entries),
        "entries": entries,
        "suspicious_name_entries": suspicious_names,
        "text_member_hits": member_term_hits,
    }


def source_metadata(defn: SourceDef) -> dict[str, Any]:
    path = defn.path
    record: dict[str, Any] = {
        "id": defn.source_id,
        "path": str(path),
        "exists": path.exists(),
        "classification": defn.classification,
        "lane": defn.lane,
        "intake_action": defn.intake_action,
        "action_gate": defn.gate,
        "publication_gate": "BLOCK",
        "runtime_import": "BLOCK",
        "raw_adoption": "BLOCK",
        "target_lane": defn.target_lane,
        "claim_boundary": defn.claim_boundary,
        "previously_registered": defn.previously_registered,
        "ficha": (
            f"docs/intake/curador_fichas/brain_os_post/{defn.ficha_slug}"
            if defn.ficha_slug
            else None
        ),
    }
    if not path.exists():
        record["status"] = "NOT_FOUND"
        return record

    record.update(
        {
            "sha256": sha256(path),
            "size_bytes": path.stat().st_size,
            "suffix": path.suffix.lower(),
        }
    )
    if path.suffix.lower() in {".txt", ".md"}:
        text, encoding = read_text(path)
        lines = text.splitlines()
        record["text"] = {
            "encoding": encoding,
            "line_count": len(lines),
            "term_hits": term_hits(lines),
        }
    elif path.suffix.lower() == ".pdf":
        record["pdf"] = pdf_metadata(path)
    elif path.suffix.lower() == ".zip":
        record["zip"] = zip_metadata(path)
    return record


def by_id(sources: list[dict[str, Any]], source_id: str) -> dict[str, Any]:
    return next(source for source in sources if source["id"] == source_id)


def delta(
    sources: list[dict[str, Any]],
    delta_id: str,
    layer: str,
    source_id: str,
    evidence: list[str],
    target_lane: str,
    claim_boundary: str,
    evidence_state: str,
    action_gate: str,
    integration_status: str,
    summary: str,
) -> dict[str, Any]:
    source = by_id(sources, source_id)
    return {
        "id": delta_id,
        "layer": layer,
        "source_id": source_id,
        "source_path": source["path"],
        "source_sha256": source["sha256"],
        "line_or_member_evidence": evidence,
        "target_lane": target_lane,
        "claim_boundary": claim_boundary,
        "evidence_state": evidence_state,
        "action_gate": action_gate,
        "integration_status": integration_status,
        "summary": summary,
    }


def build_deltas(sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        delta(
            sources,
            "boundary.alias_normalization_and_no_register",
            "Boundary",
            "portfolio_medi_post",
            [
                f"alias:{ALIAS_NOT_FOUND}=NOT_FOUND_ALIAS_DO_NOT_REGISTER",
                "canonical:line 1",
                "canonical:sha256 C1169FF35BC0ED886992C330121B3EAC744A5B051136A15C6FF256C085B6DDAD",
            ],
            "SOURCE_INTAKE_REGISTER.md; docs/intake",
            "CANONICAL_PATH_ONLY",
            "CERTEZA_FROM_FILESYSTEM_AND_HASH",
            "APPROVE_LOCAL_DOCS_ONLY",
            "OVERLAP_REINFORCES_EXISTING",
            "The missing #00 alias is recorded only as an alias; the already fichado canonical Portafolio MEDI path stays authoritative.",
        ),
        delta(
            sources,
            "boundary.publication_runtime_raw_adoption_block",
            "Boundary",
            "deep_research_report_post",
            ["line 219", "line 326", "line 435"],
            "VISIBILITY_MATRIX.md; publication review; docs/intake",
            "PUBLICATION_RUNTIME_AND_RAW_ADOPTION_BLOCKED",
            "OVERLAP_REINFORCES_EXISTING",
            "APPROVE_LOCAL_DOCS_ONLY",
            "OVERLAP_REINFORCES_EXISTING",
            "The batch reinforces that useful synthesis can be documented without publication, runtime import or wholesale adoption.",
        ),
        delta(
            sources,
            "boundary.cloud_plan_requires_local_gate",
            "Boundary",
            "cloud_gate_pdf_post",
            ["pdf_text_line 62", "pdf_text_line 131", "pdf_text_line 162", "pdf_text_line 256"],
            "ActionGate cloud/local planning docs",
            "CLOUD_OR_SECRET_ACTIONS_BLOCKED_WITHOUT_EXPLICIT_GATE",
            "REQUIRES_EVIDENCE",
            "BLOCK",
            "REQUIRES_EVIDENCE",
            "Cloud planning language must stay documentary until local gates, redaction and provider review exist.",
        ),
        delta(
            sources,
            "security.scope_registry_authorization_required",
            "Security",
            "estado_security_workbench_post",
            ["line 304", "line 311", "line 320", "line 321", "line 322", "line 323", "line 324", "line 325"],
            "obs-safe security scope registry; future Wabi wrapper gate",
            "TARGET_AUTHORIZATION_REQUIRED_BEFORE_SECURITY_TOOL_USE",
            "REQUIRES_EVIDENCE",
            "REVIEW",
            "REQUIRES_EVIDENCE",
            "Security workbench actions need an explicit ScopeRegistry record; localhost can be implied local, but public or third-party targets are blocked without authorization.",
        ),
        delta(
            sources,
            "security.action_gate_dual_use_tools",
            "Security",
            "estado_security_workbench_post",
            ["line 216", "line 328", "line 331", "line 334", "line 335", "line 336", "line 337", "line 338", "line 339"],
            "obs-safe security ActionGate; dry-run contracts",
            "DUAL_USE_TOOLS_REQUIRE_SECURITY_ACTION_GATE",
            "REQUIRES_EVIDENCE",
            "REVIEW",
            "REQUIRES_EVIDENCE",
            "Dual-use security requests must return APPROVE, REVIEW or BLOCK with reasons, risk flags, required confirmations, safe next action and witness evidence before any adapter is considered.",
        ),
        delta(
            sources,
            "security.tool_catalog_default_gates",
            "Security",
            "estado_security_workbench_post",
            ["line 245", "line 247", "line 254", "line 261", "line 262", "line 263", "line 264", "line 265", "line 276"],
            "obs-safe tool catalog; security tool policy docs",
            "TOOL_DEFAULT_GATES_MUST_NOT_ELEVATE_DUAL_USE_ACTIONS",
            "REQUIRES_EVIDENCE",
            "REVIEW",
            "REQUIRES_EVIDENCE",
            "The tool catalog can classify safe checks, OSINT and controlled validators, but dangerous tools and sensitive modes remain REVIEW or BLOCK by default.",
        ),
        delta(
            sources,
            "security.dry_run_adapter_contract",
            "Security",
            "estado_security_workbench_post",
            ["line 278", "line 281", "line 285", "line 287", "line 289", "line 290", "line 295", "line 296", "line 300"],
            "obs-safe dry-run adapters; fixture parsers; CLI commands",
            "ADAPTERS_RETURN_DRY_RUN_PLAN_AND_PARSE_FIXTURES_ONLY",
            "REQUIRES_EVIDENCE",
            "REVIEW",
            "REQUIRES_EVIDENCE",
            "Security adapters must expose metadata, dry-run plans, parser contracts and reports; no real command execution is accepted in v0.1.",
        ),
        delta(
            sources,
            "security.output_sanitizer_redaction",
            "Security",
            "estado_security_workbench_post",
            ["line 341", "line 343", "line 344", "line 346", "line 347", "line 348", "line 350", "line 356", "line 358", "line 367"],
            "obs-safe output sanitizer; report builder",
            "SECURITY_OUTPUT_MUST_REDACT_SECRETS_HASHES_COOKIES_DUMPS_AND_PAYLOADS",
            "REQUIRES_EVIDENCE",
            "REVIEW",
            "REQUIRES_EVIDENCE",
            "Security evidence must preserve severity, category, minimum evidence and fingerprint while redacting secrets, cookies, passwords, hashes, dumps and offensive payload markers.",
        ),
        delta(
            sources,
            "security.risk_mapper_business_remediation",
            "Security",
            "estado_security_workbench_post",
            ["line 369", "line 371", "line 375", "line 377", "line 378", "line 379", "line 380", "line 381", "line 383", "line 391"],
            "obs-safe risk mapper; remediation planner; report builder",
            "SECURITY_FINDINGS_REQUIRE_BUSINESS_REMEDIATION_CONTEXT",
            "REQUIRES_EVIDENCE",
            "REVIEW",
            "REQUIRES_EVIDENCE",
            "Findings should be mapped to severity plus CERTEZA, INFERENCIA, INCOGNITA and BLOQUEO so owners receive remediation rather than raw exploit output.",
        ),
        delta(
            sources,
            "security.witnesslog_handoff_security",
            "Security",
            "estado_security_workbench_post",
            ["line 150", "line 151", "line 152", "line 393", "line 394", "line 396", "line 401", "line 405", "line 408", "line 409"],
            "obs-safe WitnessLog; Handoff; NEXT_SESSION_BRIEF",
            "SECURITY_DECISIONS_REQUIRE_APPEND_ONLY_WITNESS_AND_RECONSTRUCTABLE_HANDOFF",
            "REQUIRES_EVIDENCE",
            "REVIEW",
            "REQUIRES_EVIDENCE",
            "Every security decision needs an append-only witness event and handoff that records fingerprint, gate, redactions and external-target safety.",
        ),
        delta(
            sources,
            "math_state.phi_eff_as_method_not_proof",
            "Math-State",
            "ingenieria_observacionista_inversa_post",
            ["line 7", "line 9", "line 11", "line 16", "line 100"],
            "MOI/IOI docs; Wabi/Claudio Phi_eff backlog",
            "METHOD_REQUIRES_TARGET_LANE_TESTS",
            "REQUIRES_EVIDENCE",
            "REVIEW",
            "REQUIRES_EVIDENCE",
            "Phi_eff and IOI language can guide future tests, but PROBADO remains downgraded until measured locally.",
        ),
        delta(
            sources,
            "math_state.formal_lab_demotes_physics_claims",
            "Math-State",
            "estado_post",
            ["line 85", "line 110", "line 112", "line 236", "line 264"],
            "formal-lab backlog; claim falsification register",
            "FORMAL_LAB_NOT_PRIMARY_SCIENCE",
            "REQUIRES_EVIDENCE",
            "REVIEW",
            "REQUIRES_EVIDENCE",
            "The source is useful because it explicitly separates physical truth, formal-lab possibility, metaphor and unproven limits.",
        ),
        delta(
            sources,
            "math_state.formal_framework_shannon_bridge_requires_calibration",
            "Math-State",
            "osit_epistemic_engine_formal_framework_post",
            ["line 55", "line 60", "line 67", "line 76", "line 227", "line 233"],
            "Wabi/Claudio R/Phi fixtures; calibration backlog; docs/intake",
            "SHANNON_BRIDGE_IS_HYPOTHESIS_UNTIL_LOCAL_CALIBRATION",
            "REQUIRES_EVIDENCE",
            "REVIEW",
            "REQUIRES_EVIDENCE",
            "The formal R/Shannon bridge is architecturally useful as a testable hypothesis, but identity/derivation claims require local calibration evidence.",
        ),
        delta(
            sources,
            "gate.ghostgate_actiongate_scienceclaimgate_split",
            "Gate",
            "estado_arquitectonico_rev_post",
            ["line 6", "line 24", "line 49", "line 58"],
            "ActionGate/GhostGate/ScienceClaimGate docs",
            "GATE_VOCABULARY_ONLY_UNTIL_RUNTIME_TESTS",
            "OVERLAP_REINFORCES_EXISTING",
            "APPROVE_LOCAL_DOCS_ONLY",
            "OVERLAP_REINFORCES_EXISTING",
            "The concise architecture status reinforces gate separation without requiring runtime changes.",
        ),
        delta(
            sources,
            "gate.formal_framework_ghostgate_classical_simulation",
            "Gate",
            "osit_epistemic_engine_formal_framework_post",
            ["line 130", "line 132", "line 139", "line 141", "line 143", "line 769"],
            "ActionGate/GhostGate fixtures; pre-action simulation contracts",
            "CLASSICAL_SIMULATION_CONTRACT_NOT_QUANTUM_PHYSICS_CLAIM",
            "REQUIRES_EVIDENCE",
            "REVIEW",
            "OVERLAP_REINFORCES_EXISTING",
            "GhostGate is useful as a deterministic pre-action simulation contract; quantum language stays analogy-only.",
        ),
        delta(
            sources,
            "gate.ra_horus_agency_state_machine_requires_runtime_tests",
            "Gate",
            "ra_horus_symbolic_agency_post",
            ["line 447", "line 452", "line 453", "line 454", "line 455", "line 615", "line 625"],
            "obs-safe-integration-kit agency module; Wabi/Claudio gate fixtures",
            "DREAM_CONTROL_STATES_ARE_ARCHITECTURE_ANALOGY_NOT_NEUROSCIENCE_PROOF",
            "REQUIRES_EVIDENCE",
            "REVIEW",
            "OVERLAP_REINFORCES_EXISTING",
            "The four control/metacognition states are useful as agency-state requirements, but require clean-room runtime tests.",
        ),
        delta(
            sources,
            "gate.ra_horus_pre_action_generation_gate",
            "Gate",
            "ra_horus_symbolic_agency_post",
            ["line 472", "line 474", "line 478", "line 480", "line 723", "line 747", "line 756"],
            "obs-safe-integration-kit generation gate; ActionGate pre-generation tests",
            "PREFRONTAL_GATE_IS_LOCAL_ANALOGY_REQUIRES_EVIDENCE",
            "REQUIRES_EVIDENCE",
            "REVIEW",
            "OVERLAP_REINFORCES_EXISTING",
            "The prefrontal/hipnagogia analogy is useful to require pre-generation gates, not as a medical or neuroscience claim.",
        ),
        delta(
            sources,
            "continuity.meta_review_prioritizes_direct_cleanup_dangerous",
            "Continuity",
            "estadoqqqqq_post",
            ["line 37", "line 64", "line 77", "line 80", "line 92", "line 144"],
            "batch intake plan; NEXT_SESSION_BRIEF.md",
            "META_REVIEW_NOT_A_FICHA",
            "OVERLAP_REINFORCES_EXISTING",
            "APPROVE_LOCAL_DOCS_ONLY",
            "OVERLAP_REINFORCES_EXISTING",
            "The meta-review is useful for deduplication and routing, while fichas remain the evidence surface.",
        ),
        delta(
            sources,
            "continuity.ra_horus_prerequisite_knowledge_graph",
            "Continuity",
            "ra_horus_symbolic_agency_post",
            ["line 491", "line 499", "line 502", "line 503", "line 504", "line 844", "line 909"],
            "obs-safe-integration-kit knowledge graph; source-card compiler backlog",
            "KNOWLEDGE_UNLOCK_REQUIRES_PREREQUISITES_AND_PHI_TESTS",
            "REQUIRES_EVIDENCE",
            "REVIEW",
            "OVERLAP_REINFORCES_EXISTING",
            "The Metroidvania/prerequisite graph idea is useful for knowledge access control and should never hallucinate locked node content.",
        ),
        delta(
            sources,
            "continuity.formal_framework_handoff_fingerprint_contract",
            "Continuity",
            "osit_epistemic_engine_formal_framework_post",
            ["line 173", "line 175", "line 182", "line 188", "line 699", "line 705", "line 731"],
            "SESSION_FINGERPRINT; NEXT_SESSION_BRIEF; Handoff validators",
            "HANDOFF_FINGERPRINT_REQUIRES_VALIDATOR_TESTS",
            "REQUIRES_EVIDENCE",
            "REVIEW",
            "OVERLAP_REINFORCES_EXISTING",
            "Handoff fingerprint invariants reinforce closure architecture, but must be validated against current session artifacts.",
        ),
        delta(
            sources,
            "math_state.ra_horus_dynamic_temperature_and_r_velocity",
            "Math-State",
            "ra_horus_symbolic_agency_post",
            ["line 514", "line 520", "line 523", "line 524", "line 1038", "line 1069", "line 1218", "line 1286"],
            "obs-safe-integration-kit dynamic state; R/Phi runtime fixtures",
            "TEMPERATURE_AND_R_VELOCITY_REQUIRE_SYNTHETIC_RUNTIME_TESTS",
            "REQUIRES_EVIDENCE",
            "REVIEW",
            "REQUIRES_EVIDENCE",
            "Dynamic temperature and R velocity are useful runtime heuristics only after deterministic tests prove monotonic and bounded behavior.",
        ),
        delta(
            sources,
            "falsifiers.benchmark_pass_terms_require_current_evidence",
            "Falsifiers",
            "deep_research_report_post",
            ["line 52", "line 194", "line 234", "line 422", "line 424", "line 436", "line 557", "line 564"],
            "tests/release; Wabi/Claudio benchmark fixtures",
            "SELF_REPORTED_BENCHMARK_NOT_A_PASS",
            "REQUIRES_EVIDENCE",
            "REVIEW",
            "FALSIFIER_OR_DEFECT",
            "Benchmark and PASS terms are retained as test prompts or negative fixtures, not accepted proof.",
        ),
        delta(
            sources,
            "falsifiers.formal_framework_preprint_benchmark_claims_require_current_evidence",
            "Falsifiers",
            "osit_epistemic_engine_formal_framework_post",
            ["line 6", "line 12", "line 192", "line 205", "line 247", "line 257", "line 1214"],
            "tests/release; claim guardrails; publication review",
            "PREPRINT_AND_100_PERCENT_BENCHMARK_CLAIMS_NOT_APPROVED",
            "REQUIRES_EVIDENCE",
            "REVIEW",
            "FALSIFIER_OR_DEFECT",
            "Preprint, arXiv/quant-ph and 100% benchmark language are useful negative fixtures until current local benchmarks prove the exact runtime.",
        ),
        delta(
            sources,
            "falsifiers.ra_horus_dream_science_and_raw_code_claims_blocked",
            "Falsifiers",
            "ra_horus_symbolic_agency_post",
            ["line 83", "line 125", "line 182", "line 186", "line 214", "line 338", "line 366", "line 591"],
            "tests/release; claim guardrails; obs-safe clean-room runtime tests",
            "DREAM_JUNG_MEDICINE_PHYSICS_AND_RAW_CODE_CLAIMS_NOT_APPROVED",
            "REQUIRES_EVIDENCE",
            "BLOCK",
            "FALSIFIER_OR_DEFECT",
            "Dream interpretation, Jung/neurobiology/medicine/physics language and embedded module code stay blocked as facts or raw imports.",
        ),
        delta(
            sources,
            "falsifiers.noumeno_consciousness_physics_claims_blocked",
            "Falsifiers",
            "noumeno_informacional_post",
            ["line 1", "line 2", "line 4", "line 7", "line 156", "line 589", "line 616"],
            "research backlog; public copy exclusion",
            "BLOCK_CONSCIOUSNESS_OR_PHYSICS_AS_FACT",
            "REQUIRES_EVIDENCE",
            "BLOCK",
            "FALSIFIER_OR_DEFECT",
            "The source is a strong negative-boundary example: useful to detect overclaiming, not to publish or canonize as fact.",
        ),
        delta(
            sources,
            "falsifiers.security_offensive_execution_blocked",
            "Falsifiers",
            "estado_security_workbench_post",
            ["line 182", "line 498", "line 499", "line 500", "line 501", "line 502", "line 503", "line 504", "line 505"],
            "tests/release; obs-safe security fixtures; blocked action regression tests",
            "OFFENSIVE_SECURITY_EXECUTION_AND_SECRET_OUTPUT_BLOCKED",
            "FALSIFIER_OR_DEFECT",
            "BLOCK",
            "FALSIFIER_OR_DEFECT",
            "The acceptance criteria explicitly fail if unauthorized target execution, real cracking, payloads, shells, dumps, bypass, exfiltration or secret printing become possible.",
        ),
        delta(
            sources,
            "zip.truthgate_eic_member_anchors",
            "Gate",
            "zip_truthgate_eic_v0_3_post",
            [
                "zip::04_CLAIMS_Y_SOURCE_CARDS/CLAIMS_REGISTER_v0_3.md",
                "zip::04_CLAIMS_Y_SOURCE_CARDS/SOURCE_CARDS_v0_3.md",
                "zip::05_TESTS_Y_ROADMAP/TESTS_FALSIFICADORES_v0_3.md",
            ],
            "TruthGate/EIC docs; claims/source cards; tests roadmap",
            "ZIP_MEMBER_REFERENCE_ONLY",
            "REQUIRES_EVIDENCE",
            "REVIEW",
            "OVERLAP_REINFORCES_EXISTING",
            "The container has useful claim/source-card structure, but every member remains referenced by zip path only.",
        ),
        delta(
            sources,
            "zip.formalizados_engine_runtime_import_block",
            "Math-State",
            "zip_formalizados_v2_1_post",
            [
                "zip::04_MATEMATICAS_Y_TESTS/osit_epistemic_engine_v2_1.py",
                "zip::01_CANON_Y_METODO/MOI_v0_4_TRUTHGATE.md",
                "zip::09_HANDOFF/HANDOFF_v2_1.md",
            ],
            "formalized docs; future engine rebuild backlog",
            "RUNTIME_CODE_IN_ZIP_NOT_IMPORTED",
            "REQUIRES_EVIDENCE",
            "REVIEW",
            "REQUIRES_EVIDENCE",
            "The Python engine member is explicitly treated as source evidence only, not as code to import.",
        ),
        delta(
            sources,
            "zip.teorias_consciencia_claims_blocked",
            "Boundary",
            "zip_teorias_consciencia_v0_1_post",
            [
                "zip::01_TEORIAS_ACTUALIZADAS/05_BIOLOGIA_IA_CONSCIENCIA_MTS.md",
                "zip::02_SOURCE_CARDS_Y_CLAIMS/CLAIMS_REGISTER.md",
                "zip::02_SOURCE_CARDS_Y_CLAIMS/SOURCE_CARDS.md",
            ],
            "claim demotion; theory backlog; public copy exclusion",
            "BLOCK_CONSCIOUSNESS_OR_PHYSICS_AS_FACT",
            "REQUIRES_EVIDENCE",
            "BLOCK",
            "FALSIFIER_OR_DEFECT",
            "The container is valuable for locating overclaim surfaces; consciousness and physics claims remain blocked as facts.",
        ),
        delta(
            sources,
            "zip.trabajo_mejorado_public_safe_qa_handoff",
            "Continuity",
            "zip_trabajo_mejorado_v0_2_post",
            [
                "zip::05_PRODUCTO_PUBLIC_SAFE/02_PUBLIC_SAFE_LANGUAGE.md",
                "zip::09_QA_RECONSTRUCTION/QA_REPORT.md",
                "zip::10_HANDOFF/HANDOFF.md",
            ],
            "public-safe language; QA reconstruction; Handoff",
            "PUBLIC_SAFE_COPY_REQUIRES_ALLOWLIST_AND_TESTS",
            "REQUIRES_EVIDENCE",
            "REVIEW",
            "OVERLAP_REINFORCES_EXISTING",
            "The container reinforces public-safe and QA habits, but publication remains blocked.",
        ),
    ]


def guardrail(
    sources: list[dict[str, Any]],
    term: str,
    source_id: str,
    evidence: list[str],
    boundary: str,
    action_gate: str,
) -> dict[str, Any]:
    source = by_id(sources, source_id)
    return {
        "term": term,
        "source_id": source_id,
        "source_path": source["path"],
        "source_sha256": source["sha256"],
        "line_or_member_evidence": evidence,
        "target_lane": "claim guardrail; no publication; no runtime import",
        "claim_boundary": boundary,
        "evidence_state": "REQUIRES_EVIDENCE" if action_gate != "BLOCK" else "BLOCK",
        "action_gate": action_gate,
    }


def build_guardrails(sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        guardrail(sources, "PASS", "deep_research_report_post", ["line 234"], "SELF_REPORTED_PASS_REQUIRES_CURRENT_EVIDENCE", "REVIEW"),
        guardrail(sources, "PROBADO", "ingenieria_observacionista_inversa_post", ["line 100"], "PROBADO_REQUIRES_REVIEWED_EVIDENCE", "REVIEW"),
        guardrail(sources, "Benchmark", "deep_research_report_post", ["line 52", "line 422"], "BENCHMARK_REQUIRES_LOCAL_TEST_OUTPUT", "REVIEW"),
        guardrail(sources, "consciencia", "noumeno_informacional_post", ["line 156", "line 589"], "CONSCIOUSNESS_AS_FACT_BLOCKED", "BLOCK"),
        guardrail(sources, "conciencia", "estado_post", ["line 25"], "CONSCIOUSNESS_AS_FACT_BLOCKED", "BLOCK"),
        guardrail(sources, "AGI", "cloud_gate_pdf_post", ["pdf_text_line 80", "pdf_text_line 307"], "AGI_AS_FACT_BLOCKED", "BLOCK"),
        guardrail(sources, "medicina", "portfolio_medi_post", ["line 162"], "MEDICAL_CLAIM_BLOCKED_WITHOUT_PRIMARY_REVIEW", "BLOCK"),
        guardrail(sources, "secret", "cloud_gate_pdf_post", ["pdf_text_line 131", "pdf_text_line 251"], "SECRET_HANDLING_BLOCKED", "BLOCK"),
        guardrail(sources, "token", "cloud_gate_pdf_post", ["pdf_text_line 162", "pdf_text_line 256"], "TOKEN_HANDLING_BLOCKED", "BLOCK"),
        guardrail(sources, "derivada", "cloud_gate_pdf_post", ["pdf_text_line 48"], "DERIVATION_LANGUAGE_REQUIRES_REVIEWED_PROOF", "REVIEW"),
        guardrail(sources, "arXiv", "osit_epistemic_engine_formal_framework_post", ["line 6"], "PREPRINT_STATUS_NOT_PUBLICATION_PROOF", "REVIEW"),
        guardrail(sources, "quant-ph", "osit_epistemic_engine_formal_framework_post", ["line 6"], "QUANTUM_CATEGORY_REQUIRES_REVIEWED_EVIDENCE", "REVIEW"),
        guardrail(sources, "100%", "osit_epistemic_engine_formal_framework_post", ["line 12", "line 205", "line 257"], "BENCHMARK_PERCENT_REQUIRES_CURRENT_LOCAL_OUTPUT", "REVIEW"),
        guardrail(sources, "Shannon", "osit_epistemic_engine_formal_framework_post", ["line 55", "line 67", "line 76"], "FORMAL_IDENTITY_REQUIRES_CALIBRATION", "REVIEW"),
        guardrail(sources, "sueño", "ra_horus_symbolic_agency_post", ["line 50", "line 214", "line 366"], "DREAM_INTERPRETATION_REQUIRES_EVIDENCE", "REVIEW"),
        guardrail(sources, "Jung", "ra_horus_symbolic_agency_post", ["line 83", "line 104", "line 109"], "JUNG_ARCHETYPE_LANGUAGE_NOT_APPROVED_SCIENCE", "REVIEW"),
        guardrail(sources, "neurobiología", "ra_horus_symbolic_agency_post", ["line 214"], "NEUROBIOLOGY_CLAIMS_REQUIRE_PRIMARY_REVIEW", "REVIEW"),
        guardrail(sources, "hipnagogia", "ra_horus_symbolic_agency_post", ["line 393", "line 472", "line 474", "line 723"], "HYPNAGOGIA_ANALOGY_REQUIRES_BOUNDARY", "REVIEW"),
        guardrail(sources, "metacognición", "ra_horus_symbolic_agency_post", ["line 449", "line 452", "line 453", "line 454", "line 455"], "METACOGNITION_ANALOGY_REQUIRES_RUNTIME_TESTS", "REVIEW"),
        guardrail(sources, "prefrontal", "ra_horus_symbolic_agency_post", ["line 480", "line 747", "line 749"], "PREFRONTAL_ANALOGY_NOT_MEDICAL_PROOF", "REVIEW"),
        guardrail(sources, "AI generated", "ra_horus_symbolic_agency_post", ["line 182", "line 186", "line 202", "line 206"], "AI_IMAGE_MATERIAL_NOT_SOURCE_EVIDENCE", "BLOCK"),
        guardrail(sources, "cósmica", "ra_horus_symbolic_agency_post", ["line 70", "line 125"], "COSMIC_OR_SPIRITUAL_CLAIM_NOT_APPROVED", "BLOCK"),
        guardrail(sources, "nmap", "estado_security_workbench_post", ["line 7", "line 40", "line 173", "line 248"], "NMAP_REQUIRES_SECURITY_SCOPE_AND_DRY_RUN_CONTRACT", "REVIEW"),
        guardrail(sources, "nikto", "estado_security_workbench_post", ["line 7", "line 41", "line 174", "line 249"], "NIKTO_REQUIRES_SECURITY_SCOPE_AND_DRY_RUN_CONTRACT", "REVIEW"),
        guardrail(sources, "maltego", "estado_security_workbench_post", ["line 7", "line 42", "line 175", "line 255"], "OSINT_TOOL_REQUIRES_AUTHORIZED_SCOPE", "REVIEW"),
        guardrail(sources, "recon-ng", "estado_security_workbench_post", ["line 7", "line 42", "line 176", "line 256"], "OSINT_TOOL_REQUIRES_AUTHORIZED_SCOPE", "REVIEW"),
        guardrail(sources, "metasploit", "estado_security_workbench_post", ["line 7", "line 44", "line 177", "line 258"], "METASPLOIT_REQUIRES_LAB_DRY_RUN_REVIEW", "REVIEW"),
        guardrail(sources, "sqlmap", "estado_security_workbench_post", ["line 7", "line 45", "line 178", "line 257"], "SQLMAP_REQUIRES_LAB_DRY_RUN_REVIEW", "REVIEW"),
        guardrail(sources, "john", "estado_security_workbench_post", ["line 7", "line 46", "line 179", "line 259"], "PASSWORD_AUDIT_TOOL_REQUIRES_SYNTHETIC_OR_OWNED_HASH_REVIEW", "REVIEW"),
        guardrail(sources, "hashcat", "estado_security_workbench_post", ["line 7", "line 46", "line 180", "line 259"], "PASSWORD_AUDIT_TOOL_REQUIRES_SYNTHETIC_OR_OWNED_HASH_REVIEW", "REVIEW"),
        guardrail(sources, "payload", "estado_security_workbench_post", ["line 182", "line 265", "line 468", "line 502"], "PAYLOAD_EXECUTION_BLOCKED", "BLOCK"),
        guardrail(sources, "shell", "estado_security_workbench_post", ["line 94", "line 182", "line 266", "line 503"], "SHELL_ACCESS_BLOCKED", "BLOCK"),
        guardrail(sources, "dump", "estado_security_workbench_post", ["line 93", "line 182", "line 270", "line 501"], "DUMP_OR_DATABASE_RECORD_OUTPUT_BLOCKED", "BLOCK"),
        guardrail(sources, "bypass", "estado_security_workbench_post", ["line 97", "line 182", "line 273", "line 504"], "BYPASS_OR_EVASION_BLOCKED", "BLOCK"),
        guardrail(sources, "exfiltration", "estado_security_workbench_post", ["line 182", "line 274", "line 505"], "EXFILTRATION_BLOCKED", "BLOCK"),
        guardrail(sources, "cookie", "estado_security_workbench_post", ["line 348", "line 501"], "COOKIE_OR_SESSION_OUTPUT_REDACTION_REQUIRED", "BLOCK"),
        guardrail(sources, "password", "estado_security_workbench_post", ["line 95", "line 271", "line 346", "line 501"], "PASSWORD_OR_CRACKING_OUTPUT_BLOCKED", "BLOCK"),
    ]


def build_falsifiers(sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "id": "missing_00_alias",
            "raw_claim": ALIAS_NOT_FOUND,
            "source_path": ALIAS_NOT_FOUND,
            "claim_boundary": "NOT_FOUND_ALIAS_DO_NOT_REGISTER",
            "evidence_state": "FALSIFIER_OR_DEFECT",
            "action_gate": "BLOCK",
        },
        {
            "id": "zip_runtime_code_member",
            "raw_claim": "osit_epistemic_engine_v2_1.py inside ZIP",
            "source_path": by_id(sources, "zip_formalizados_v2_1_post")["path"],
            "source_sha256": by_id(sources, "zip_formalizados_v2_1_post")["sha256"],
            "line_or_member_evidence": ["zip::04_MATEMATICAS_Y_TESTS/osit_epistemic_engine_v2_1.py"],
            "claim_boundary": "RUNTIME_IMPORT_BLOCK",
            "evidence_state": "REQUIRES_EVIDENCE",
            "action_gate": "REVIEW",
        },
        {
            "id": "self_reported_pass_terms",
            "raw_claim": "PASS / Benchmark / PROBADO markers in source text",
            "source_path": by_id(sources, "deep_research_report_post")["path"],
            "source_sha256": by_id(sources, "deep_research_report_post")["sha256"],
            "line_or_member_evidence": ["line 52", "line 234", "line 422"],
            "claim_boundary": "NOT_A_PASS_WITHOUT_CURRENT_TEST",
            "evidence_state": "FALSIFIER_OR_DEFECT",
            "action_gate": "REVIEW",
        },
        {
            "id": "formal_framework_preprint_benchmark_claim",
            "raw_claim": "arXiv/quant-ph proposed preprint and 100% benchmark coverage",
            "source_path": by_id(sources, "osit_epistemic_engine_formal_framework_post")["path"],
            "source_sha256": by_id(sources, "osit_epistemic_engine_formal_framework_post")["sha256"],
            "line_or_member_evidence": ["line 6", "line 12", "line 205", "line 257"],
            "claim_boundary": "PREPRINT_AND_BENCHMARK_CLAIMS_REQUIRE_CURRENT_EVIDENCE",
            "evidence_state": "FALSIFIER_OR_DEFECT",
            "action_gate": "REVIEW",
        },
        {
            "id": "ra_horus_dream_modules_raw_code_claim",
            "raw_claim": "Dream interpretation, neuroscience/medicine/physics analogies and embedded Dream Modules runtime code",
            "source_path": by_id(sources, "ra_horus_symbolic_agency_post")["path"],
            "source_sha256": by_id(sources, "ra_horus_symbolic_agency_post")["sha256"],
            "line_or_member_evidence": ["line 214", "line 338", "line 366", "line 591", "line 615", "line 747", "line 1038"],
            "claim_boundary": "RAW_CODE_AND_SCIENCE_DREAM_CLAIMS_BLOCKED",
            "evidence_state": "FALSIFIER_OR_DEFECT",
            "action_gate": "BLOCK",
        },
        {
            "id": "security_offensive_execution_blocked",
            "raw_claim": "Security workbench adapters may execute offensive tools, payloads, shells, dumps, bypass, exfiltration or real password cracking.",
            "source_path": by_id(sources, "estado_security_workbench_post")["path"],
            "source_sha256": by_id(sources, "estado_security_workbench_post")["sha256"],
            "line_or_member_evidence": ["line 182", "line 498", "line 499", "line 500", "line 501", "line 502", "line 503", "line 504", "line 505"],
            "claim_boundary": "OFFENSIVE_EXECUTION_BLOCK",
            "evidence_state": "FALSIFIER_OR_DEFECT",
            "action_gate": "BLOCK",
        },
    ]


def build_deduplication(sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    repeated_ids = [
        "estado_post",
        "estadoqqqqq_post",
        "ingenieria_observacionista_inversa_post",
        "zip_truthgate_eic_v0_3_post",
        "zip_formalizados_v2_1_post",
        "zip_teorias_consciencia_v0_1_post",
        "zip_trabajo_mejorado_v0_2_post",
        "osit_epistemic_engine_formal_framework_post",
        "ra_horus_symbolic_agency_post",
        "osit_epistemic_engine_post",
    ]
    return [
        {
            "source_id": source["id"],
            "path": source["path"],
            "sha256": source["sha256"],
            "normalized_once": True,
            "reason": "Repeated in the incoming plan/list; kept once by exact path and SHA256.",
        }
        for source in sources
        if source["id"] in repeated_ids
    ]


def build_matrix() -> dict[str, Any]:
    sources = [source_metadata(defn) for defn in SOURCE_DEFS]
    new_sources = [source for source in sources if not source["previously_registered"]]
    zip_sources = [source for source in sources if source.get("suffix") == ".zip"]
    return {
        "schema_version": "brain_os.post_batch_insights_matrix.v1",
        "created_date": "2026-05-18",
        "status": "LOCAL_INTAKE_GOVERNANCE_ONLY",
        "decision": "CURATE_POST_BATCH_DELTAS_WITHOUT_RUNTIME_IMPORT",
        "gate_summary": {
            "ActionGate": "APPROVE_LOCAL_DOCS_ONLY_FOR_MATRIX_AND_FICHAS",
            "RuntimeImport": "BLOCK",
            "PublicationGate": "BLOCK",
            "RawAdoption": "BLOCK",
        },
        "source_root": str(POST_ROOT),
        "not_found_aliases": [
            {
                "path": ALIAS_NOT_FOUND,
                "status": "NOT_FOUND_ALIAS_DO_NOT_REGISTER",
                "canonical_path": by_id(sources, "portfolio_medi_post")["path"],
                "canonical_sha256": by_id(sources, "portfolio_medi_post")["sha256"],
            }
        ],
        "sources": sources,
        "new_source_count": len(new_sources),
        "zip_inventory": [
            {
                "source_id": source["id"],
                "path": source["path"],
                "sha256": source["sha256"],
                "testzip": source["zip"]["testzip"],
                "entry_count": source["zip"]["entry_count"],
                "entries": source["zip"]["entries"],
                "suspicious_name_entries": source["zip"]["suspicious_name_entries"],
            }
            for source in zip_sources
        ],
        "deduplication": build_deduplication(sources),
        "layers": ["Boundary", "Math-State", "Gate", "Continuity", "Falsifiers"],
        "deltas": build_deltas(sources),
        "claim_guardrails": build_guardrails(sources),
        "falsifiers": build_falsifiers(sources),
        "next_gate": "Use this as intake evidence only; runtime import, publication and raw adoption remain BLOCK until a later reviewed task has target-lane tests.",
    }


def md_table(rows: list[list[str]]) -> str:
    if not rows:
        return ""
    widths = [max(len(row[idx]) for row in rows) for idx in range(len(rows[0]))]
    out = []
    for idx, row in enumerate(rows):
        out.append("| " + " | ".join(cell.ljust(widths[col]) for col, cell in enumerate(row)) + " |")
        if idx == 0:
            out.append("| " + " | ".join("-" * widths[col] for col in range(len(row))) + " |")
    return "\n".join(out)


def render_matrix_md(matrix: dict[str, Any]) -> str:
    rows = [["source", "sha256", "classification", "gate", "ficha"]]
    for source in matrix["sources"]:
        rows.append(
            [
                f"`{source['path']}`",
                f"`{source.get('sha256', 'NOT_FOUND')}`",
                f"`{source['classification']}`",
                f"`{source['action_gate']}`",
                f"`{source['ficha'] or 'previously_registered'}`",
            ]
        )
    zip_rows = [["zip", "testzip", "entries", "suspicious_name_entries"]]
    for item in matrix["zip_inventory"]:
        zip_rows.append(
            [
                f"`{item['path']}`",
                f"`{item['testzip']}`",
                str(item["entry_count"]),
                str(len(item["suspicious_name_entries"])),
            ]
        )
    delta_rows = [["id", "layer", "source", "status", "gate"]]
    for item in matrix["deltas"]:
        delta_rows.append(
            [
                f"`{item['id']}`",
                f"`{item['layer']}`",
                f"`{item['source_id']}`",
                f"`{item['integration_status']}`",
                f"`{item['action_gate']}`",
            ]
        )
    return "\n".join(
        [
            "# BRAIN_OS POST Batch Insights Matrix 2026-05-18",
            "",
            "Status: `LOCAL_INTAKE_GOVERNANCE_ONLY`",
            "",
            "ActionGate: `APPROVE_LOCAL_DOCS_ONLY_FOR_MATRIX_AND_FICHAS`",
            "",
            "RuntimeImport=BLOCK",
            "",
            "PublicationGate=BLOCK",
            "",
            "RawAdoption=BLOCK",
            "",
            "This is the second curated matrix for the complete POST batch. It registers exact-path evidence, hashes, ZIP metadata and claim guardrails without extracting containers into runtime, publishing content or adopting raw sources.",
            "",
            "## Alias Normalization",
            "",
            f"- Missing alias: `{ALIAS_NOT_FOUND}` -> `NOT_FOUND_ALIAS_DO_NOT_REGISTER`.",
            f"- Canonical source: `{matrix['not_found_aliases'][0]['canonical_path']}`.",
            "",
            "## Sources",
            "",
            md_table(rows),
            "",
            "## ZIP Containers",
            "",
            md_table(zip_rows),
            "",
            "ZIP entries are referenced as `zip_path::internal/path`, never as adopted files.",
            "",
            "## Deltas",
            "",
            md_table(delta_rows),
            "",
            "## Guardrails",
            "",
            "- `PASS`, `PROBADO`, `Benchmark`, `derivada` and similar success terms remain `REQUIRES_EVIDENCE`.",
            "- `consciencia`, `conciencia`, `AGI`, `medicina`, secret-like handling and token-like handling remain `BLOCK` when stated as facts or operational actions.",
            "- Runtime code inside ZIPs remains `RuntimeImport=BLOCK` until rebuilt from reviewed requirements with target-lane tests.",
            "",
            "## Evidence",
            "",
            "- Full machine-readable matrix: `docs/intake/BRAIN_OS_POST_BATCH_INSIGHTS_MATRIX_2026-05-18.json`.",
            "- Fichas: `docs/intake/curador_fichas/brain_os_post/2026-05-18_batch_*.md`.",
            "- Tests: `tests/release/test_brain_os_post_batch_insights.py`.",
            "",
        ]
    )


def render_ficha(defn: SourceDef, source: dict[str, Any]) -> str:
    metadata_lines = [
        f"| path | `{source['path']}` |",
        f"| kind | `{source.get('suffix', 'missing')}` |",
        f"| sha256 | `{source.get('sha256', 'NOT_FOUND')}` |",
        f"| size_bytes | `{source.get('size_bytes', 'NOT_FOUND')}` |",
        f"| classification | `{source['classification']}` |",
        f"| lane | `{source['lane']}` |",
        f"| intake_action | `{source['intake_action']}` |",
        f"| target_lane | `{source['target_lane']}` |",
        f"| action_gate | `{source['action_gate']}` |",
        f"| publication_gate | `{source['publication_gate']}` |",
        f"| runtime_import | `{source['runtime_import']}` |",
        f"| raw_adoption | `{source['raw_adoption']}` |",
    ]
    if source.get("text"):
        metadata_lines.append(f"| line_count | `{source['text']['line_count']}` |")
        metadata_lines.append(f"| encoding | `{source['text']['encoding']}` |")
    if source.get("pdf"):
        metadata_lines.append(f"| page_count | `{source['pdf'].get('page_count', 'UNAVAILABLE')}` |")
        metadata_lines.append(f"| text_line_count | `{source['pdf'].get('text_line_count', 'UNAVAILABLE')}` |")
    if source.get("zip"):
        metadata_lines.append(f"| zip_testzip | `{source['zip']['testzip']}` |")
        metadata_lines.append(f"| zip_entry_count | `{source['zip']['entry_count']}` |")
        metadata_lines.append(f"| suspicious_name_entries | `{len(source['zip']['suspicious_name_entries'])}` |")

    term_lines: list[str] = []
    term_source = source.get("text") or source.get("pdf")
    if term_source:
        for term, meta in term_source.get("term_hits", {}).items():
            term_lines.append(f"- `{term}`: count `{meta['count']}`, first lines `{meta['first_lines']}`")
    elif source.get("zip"):
        aggregate: dict[str, int] = {}
        for member in source["zip"]["text_member_hits"].values():
            for term, meta in member["term_hits"].items():
                aggregate[term] = aggregate.get(term, 0) + int(meta["count"])
        for term, count in sorted(aggregate.items()):
            term_lines.append(f"- `{term}`: aggregate member count `{count}`")

    zip_entries: list[str] = []
    if source.get("zip"):
        zip_entries = [f"- `{entry}`" for entry in source["zip"]["entries"]]

    return "\n".join(
        [
            f"# Ficha Curador - BRAIN_OS POST Batch - {defn.source_id}",
            "",
            "Status: `FICHADO_BATCH_SELECTIVE_EXTRACTION`",
            "",
            f"ActionGate: `{source['action_gate']}`",
            "",
            "PublicationGate: `BLOCK`",
            "",
            "RuntimeImport: `BLOCK`",
            "",
            "RawAdoption: `BLOCK`",
            "",
            "## Source",
            "",
            "| field | value |",
            "|---|---|",
            *metadata_lines,
            "",
            "## Useful Deltas",
            "",
            *[f"- {item}" for item in defn.useful_deltas],
            "",
            "## Rejected Material",
            "",
            *[f"- {item}" for item in defn.rejected_material],
            "",
            "## Claim Boundary",
            "",
            f"`{defn.claim_boundary}`",
            "",
            "Strong terms are not promoted by this ficha. Publication, runtime import and raw adoption stay blocked.",
            "",
            "## Term Signals",
            "",
            *(term_lines or ["- No tracked term signals found."]),
            "",
            "## ZIP Internal Entries" if zip_entries else "## ZIP Internal Entries",
            "",
            *(zip_entries or ["- Not a ZIP container."]),
            "",
            "## Evidence",
            "",
            f"- Hash computed from exact source path on 2026-05-18.",
            f"- Evidence hint: {defn.evidence_hint}",
            "- Matrix: `docs/intake/BRAIN_OS_POST_BATCH_INSIGHTS_MATRIX_2026-05-18.json`.",
            "",
            "## Decision",
            "",
            "`DOCUMENTED_FOR_SELECTIVE_EXTRACTION_ONLY`.",
            "",
            "No source was moved, extracted into runtime, published or imported.",
            "",
        ]
    )


def render_register_section(matrix: dict[str, Any]) -> str:
    rows = [
        "| source | exists | sha256 | classification | lane | intake_action | gate | ficha |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for source in matrix["sources"]:
        if source["previously_registered"]:
            continue
        rows.append(
            "| "
            + " | ".join(
                [
                    f"`{source['path']}`",
                    "yes" if source["exists"] else "no",
                    f"`{source.get('sha256', 'NOT_FOUND')}`",
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
            "<!-- BRAIN_OS_POST_BATCH_INSIGHTS_2026_05_18_START -->",
            "## 2026-05-18 - BRAIN_OS POST Batch Insights Matrix",
            "",
            f"Scope: exact-path fichas for the {matrix['new_source_count']} new POST sources. The previously fichado `Portafolio MEDI` and `Untitled.txt` entries remain governed by the earlier `BRAIN_OS POST Selective Extraction` section.",
            "",
            *rows,
            "",
            "Decision:",
            "",
            "- `Adopcion cruda`: `BLOCK`.",
            "- `RuntimeImport`: `BLOCK`.",
            "- `PublicationGate`: `BLOCK`.",
            "- ZIP handling: metadata/member-reference only; no extraction to runtime.",
            "- Missing alias `# 00  LEER PRIMERO...`: `NOT_FOUND_ALIAS_DO_NOT_REGISTER`.",
            "",
            "<!-- BRAIN_OS_POST_BATCH_INSIGHTS_2026_05_18_END -->",
            "",
        ]
    )


def update_register(section: str) -> None:
    start = "<!-- BRAIN_OS_POST_BATCH_INSIGHTS_2026_05_18_START -->"
    end = "<!-- BRAIN_OS_POST_BATCH_INSIGHTS_2026_05_18_END -->"
    text = REGISTER.read_text(encoding="utf-8")
    if start in text and end in text:
        pattern = re.compile(re.escape(start) + r".*?" + re.escape(end) + r"\n?", re.S)
        text = pattern.sub(lambda _match: section, text)
    else:
        text = text.rstrip() + "\n\n" + section
    REGISTER.write_text(text, encoding="utf-8")


def main() -> int:
    FICHA_DIR.mkdir(parents=True, exist_ok=True)
    matrix = build_matrix()
    MATRIX_JSON.write_text(json.dumps(matrix, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    MATRIX_MD.write_text(render_matrix_md(matrix), encoding="utf-8")

    by_source_id = {source["id"]: source for source in matrix["sources"]}
    for defn in SOURCE_DEFS:
        if defn.ficha_slug is None:
            continue
        ficha_path = FICHA_DIR / defn.ficha_slug
        ficha_path.write_text(render_ficha(defn, by_source_id[defn.source_id]), encoding="utf-8")

    update_register(render_register_section(matrix))
    print(json.dumps({"matrix": str(MATRIX_JSON), "sources": len(matrix["sources"]), "new_sources": matrix["new_source_count"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
