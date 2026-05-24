from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal


EpistemicState = Literal["CERTEZA", "INFERENCIA", "INCOGNITA", "BLOQUEO"]
ModuleRisk = Literal["low", "medium", "high"]
ModuleBoundary = Literal["public", "private", "protected"]
ModuleStatus = Literal["planned", "active", "review", "deprecated"]


@dataclass(frozen=True)
class DuatModuleCard:
    id: str
    name: str
    purpose: str
    inputs: tuple[str, ...]
    outputs: tuple[str, ...]
    owner_agent: str
    risk: ModuleRisk
    boundary: ModuleBoundary
    status: ModuleStatus
    tests: tuple[str, ...]
    evidence: tuple[str, ...] = field(default_factory=tuple)
    epistemic_state: EpistemicState = "INFERENCIA"
    next_action: str = ""


DUAT_MODULES: tuple[DuatModuleCard, ...] = (
    DuatModuleCard(
        id="project_analyzer",
        name="Project Analyzer",
        purpose=(
            "Analyze repos, ZIPs, folders, prompts, docs, assets and workflows "
            "into public-safe source cards, module maps and risk maps."
        ),
        inputs=("repo", "zip", "folder", "package.json", "README", "src"),
        outputs=("PROJECT_SOURCE_CARD.md", "MODULE_MAP.json", "RISK_MAP.json", "NEXT_PATCH_PLAN.md"),
        owner_agent="Curator Agent",
        risk="medium",
        boundary="public",
        status="planned",
        tests=("module registry validates required fields",),
        next_action="Implement intake scanner and source card generator.",
    ),
    DuatModuleCard(
        id="image_reactor",
        name="Image Reactor",
        purpose="Analyze screenshots/assets, extract style vectors and produce approved public-safe asset prompts.",
        inputs=("image", "screenshot", "logo", "asset pack", "UI mockup"),
        outputs=("IMAGE_SOURCE_CARD.md", "STYLE_VECTOR.json", "ASSET_QA_REPORT.md", "PROMPT_FOR_GENERATION.md"),
        owner_agent="DUAT Visual Agent",
        risk="medium",
        boundary="public",
        status="planned",
        tests=("style vector schema validates",),
        next_action="Add image source card schema and prompt builder.",
    ),
    DuatModuleCard(
        id="company_observatory",
        name="Company Observatory",
        purpose="Research public capabilities and reconstruct original MEDIOEVO modules from cited public evidence.",
        inputs=("company name", "public docs", "public changelog", "demo", "screenshot", "feature page"),
        outputs=("COMPANY_SOURCE_CARD.md", "CAPABILITY_VECTOR.json", "MODULE_OPPORTUNITY_MAP.md"),
        owner_agent="Research Agent",
        risk="medium",
        boundary="public",
        status="planned",
        tests=("source card requires citation/evidence fields",),
        next_action="Implement source-backed research template.",
    ),
    DuatModuleCard(
        id="tool_forge",
        name="Tool Forge",
        purpose="Convert repeated needs into small tested tools, components, scripts or prompts.",
        inputs=("need", "example", "success criteria", "risk", "output format"),
        outputs=("component", "function", "test", "module_card", "WitnessLog event"),
        owner_agent="Code Reviewer",
        risk="medium",
        boundary="public",
        status="planned",
        tests=("generated module includes tests and witness event",),
        next_action="Add generator scaffold.",
    ),
    DuatModuleCard(
        id="module_refactor_engine",
        name="Module Refactor Engine",
        purpose="Upgrade existing demo tools into verifiable modules without destructive changes.",
        inputs=("existing module", "test result", "risk", "target behavior"),
        outputs=("patch", "test", "migration note", "handoff"),
        owner_agent="Release Engineer",
        risk="high",
        boundary="protected",
        status="planned",
        tests=("no destructive changes without evidence",),
        next_action="Refactor Claim Classifier, ActionGate, WitnessLog and Handoff.",
    ),
    DuatModuleCard(
        id="bulletin_board_sync",
        name="Bulletin Board Sync",
        purpose="Make next actions, unknowns, R, regime, fingerprint and handoff visible to the user.",
        inputs=("run status", "handoff", "witness log", "next action"),
        outputs=("bulletin payload", "dashboard update", "copyable JSON"),
        owner_agent="Coordinator Agent",
        risk="low",
        boundary="public",
        status="planned",
        tests=("payload schema validates",),
        next_action="Connect to local dashboard or static JSON artifact.",
    ),
    DuatModuleCard(
        id="evaluation_harness",
        name="Evaluation Harness",
        purpose="Measure whether Observacionismo reduces residue and improves continuity, traceability and action quality.",
        inputs=("before state", "after state", "tests", "handoff", "token counts"),
        outputs=("R_DELTA_REPORT.md", "EFFICIENCY_REPORT.md", "FALSIFIER_REPORT.md"),
        owner_agent="Claim Auditor",
        risk="medium",
        boundary="public",
        status="planned",
        tests=("calculates before/after metrics",),
        next_action="Add metrics for continuity, QA, token compression and ActionGate outcomes.",
    ),
    DuatModuleCard(
        id="legacy_transfer",
        name="Legacy Transfer",
        purpose="Prepare safe operator docs for family and collaborators without exposing secrets or private IP.",
        inputs=("repo", "products", "Gumroad status", "public URLs", "safe docs"),
        outputs=(
            "FAMILY_README_START_HERE.md",
            "REVENUE_AND_PUBLICATION_HANDOFF.md",
            "WHAT_IS_SAFE_TO_SHARE.md",
            "WHAT_MUST_STAY_PRIVATE.md",
        ),
        owner_agent="Product Strategist",
        risk="high",
        boundary="protected",
        status="planned",
        tests=("secret/private material scan passes",),
        next_action="Generate safe handoff docs without secrets.",
    ),
)


def get_public_modules() -> tuple[DuatModuleCard, ...]:
    return tuple(module for module in DUAT_MODULES if module.boundary == "public")


def get_modules_by_status(status: ModuleStatus) -> tuple[DuatModuleCard, ...]:
    return tuple(module for module in DUAT_MODULES if module.status == status)


def validate_module_card(card: DuatModuleCard) -> list[str]:
    errors: list[str] = []
    if not card.id:
        errors.append("missing id")
    if not card.name:
        errors.append("missing name")
    if not card.purpose:
        errors.append("missing purpose")
    if not card.inputs:
        errors.append("missing inputs")
    if not card.outputs:
        errors.append("missing outputs")
    if not card.owner_agent:
        errors.append("missing owner_agent")
    if not card.next_action:
        errors.append("missing next_action")
    return errors
