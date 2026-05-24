import type { CityState } from "../core/types";
import type { WorkpackDraft } from "./types";

export function createWorkpackDraftFromCity(state: CityState): WorkpackDraft {
  const blocked = state.tasks.filter(t => t.status === "blocked" || t.status === "failed").length;
  const highR = state.R > 0.45;
  return {
    schema: "wabi/duat-city/workpack-draft/v0.5-design",
    workpack_type: "city",
    suggested_files: [
      "artifacts/duat-city/src/sim/engine.ts",
      "artifacts/duat-city/src/physics/agentPhysicsAdapter.ts",
      "artifacts/duat-city/src/core/handoff.ts",
    ],
    tasks: [
      highR ? "Review DUAT city R drivers before feature expansion" : "Prepare local deterministic simulation test pass",
      blocked > 0 ? "Inspect blocked or failed tasks and produce handoff" : "Keep task closure loop active",
    ],
    risks: [
      "DESIGN ONLY: no execution allowed",
      "No real MCP apply path is enabled",
      state.gate === "BLOCK" ? "City gate BLOCK: no new features" : "City gate allows prepare-only planning",
    ],
    tests_to_run: [
      "pnpm --filter @workspace/duat-city run test",
      "pnpm --filter @workspace/duat-city run typecheck",
      "pnpm --filter @workspace/duat-city run build",
    ],
    rollback_plan: [
      "Do not execute this draft automatically",
      "Use git diff on artifacts/duat-city before any future apply",
      "Revert only path-scoped changes owned by the workpack",
    ],
    execution_allowed: false,
    sandbox_execution_allowed: false,
    real_apply_allowed: false,
  };
}

function createTypedDraft(type: NonNullable<WorkpackDraft["workpack_type"]>, state: CityState, targetFiles: string[], plannedChanges: string[], review: string[]): WorkpackDraft {
  return {
    schema: "wabi/duat-city/workpack-draft/v0.6-design",
    workpack_type: type,
    suggested_files: targetFiles,
    target_files: targetFiles,
    tasks: plannedChanges,
    planned_changes: plannedChanges,
    risks: [
      "DESIGN ONLY: no execution allowed",
      "No MCP call, real apply, push, deploy or external API is enabled",
      state.gate === "BLOCK" ? "City gate BLOCK: reduce scope before implementation" : "Local draft only; owner review still required for copied assets",
    ],
    tests_to_run: [
      "corepack pnpm --filter @workspace/duat-city run test",
      "corepack pnpm --filter @workspace/duat-city run typecheck",
      "corepack pnpm --filter @workspace/duat-city run build",
    ],
    rollback_plan: [
      "Keep original source folders untouched",
      "Remove only path-scoped files listed in target_files if owner rejects the draft",
      "Regenerate manifests from qa_artifacts run evidence before any future asset copy",
    ],
    required_owner_review: review,
    owner_review_required: review.length > 0,
    execution_allowed: false,
    sandbox_execution_allowed: false,
    real_apply_allowed: false,
  };
}

function createTypedDraftV07(type: NonNullable<WorkpackDraft["workpack_type"]>, state: CityState, targetFiles: string[], plannedChanges: string[], review: string[]): WorkpackDraft {
  return {
    ...createTypedDraft(type, state, targetFiles, plannedChanges, review),
    schema: "wabi/duat-city/workpack-draft/v0.7-design",
  };
}

export function createAssetWorkpackDraft(state: CityState): WorkpackDraft {
  return createTypedDraft("asset-forensics", state, [
    "artifacts/duat-city/public/asset-manifest/visual_assets_manifest_v0_6.json",
    "artifacts/duat-city/docs/ASSET_BOUNDARY_REPORT_v0_6.md",
  ], [
    "Review candidate DUAT ASSETS and medioevo-site isometric/building images",
    "Approve or reject individual assets by provenance before any copy",
    "Keep public export sanitized with root tokens instead of absolute private paths",
  ], [
    "Unknown asset licenses and private/commercial boundary",
    "Any move from review to copied asset status",
  ]);
}

export function createGraphicsUpgradeWorkpackDraft(state: CityState): WorkpackDraft {
  return createTypedDraft("graphics-upgrade", state, [
    "artifacts/duat-city/src/graphics/isoMath.ts",
    "artifacts/duat-city/src/graphics/lightEngine.ts",
    "artifacts/duat-city/src/render/canvasRenderer.ts",
  ], [
    "Extend 2.5D tile/building/agent renderers without WebGL",
    "Tune day/night and local point lights",
    "Benchmark 100 agents with debug overlays disabled",
  ], [
    "Visual acceptance by owner",
    "Browser screenshot/performance review on target machine",
  ]);
}

export function createPhysicsFieldWorkpackDraft(state: CityState): WorkpackDraft {
  return createTypedDraft("physics-field", state, [
    "artifacts/duat-city/src/physicsField/*",
    "artifacts/duat-city/src/physics/agentPhysicsAdapter.ts",
  ], [
    "Tune water/smoke/fire/dust cellular rules",
    "Feed field hazards into agent movement pressure and events",
    "Keep field resolution low and active-cell based",
  ], [
    "No claims of real physics",
    "Performance benchmark at larger city sizes",
  ]);
}

export function createRPGExportWorkpackDraft(state: CityState): WorkpackDraft {
  return createTypedDraft("rpg-export", state, [
    "artifacts/duat-city/src/rpg/worldExport.ts",
    "artifacts/duat-city/src/rpg/rpgTypes.ts",
    "artifacts/duat-city/public/asset-manifest/*.json",
  ], [
    "Validate medioevo-rpg/world/v2 schema consumers",
    "Review faction/NPC schedule output for private lore leakage",
    "Keep asset refs as manifest references, not copied private files",
  ], [
    "Consumer compatibility with v1 exports",
    "Owner review for lore and asset refs",
  ]);
}

export function createAssetAllowlistWorkpackDraft(state: CityState): WorkpackDraft {
  return createTypedDraftV07("asset-allowlist", state, [
    "artifacts/duat-city/docs/ASSET_ALLOWLIST_v0_7.md",
    "artifacts/duat-city/public/asset-manifest/asset_allowlist_v0_7.json",
    "artifacts/duat-city/public/reviewed-assets/v0_7/REVIEWED_ASSETS_MANIFEST.json",
  ], [
    "Review allowlisted internal DUAT assets and keep copy count under 510",
    "Verify copied assets have SHA256, provenance, boundary and publication_allowed=false",
    "Reject REVIEW_REQUIRED or DENY assets from any runtime copy path",
  ], [
    "Owner review remains required before public release use",
    "License/provenance status is internal-review only",
  ]);
}

export function createVisualAtlasIntegrationWorkpackDraft(state: CityState): WorkpackDraft {
  return createTypedDraftV07("visual-atlas-integration", state, [
    "artifacts/duat-city/src/graphics/assetManifestLoader.ts",
    "artifacts/duat-city/src/graphics/spriteResolver.ts",
    "artifacts/duat-city/src/graphics/atlas.ts",
    "artifacts/duat-city/src/render/canvasRenderer.ts",
  ], [
    "Load reviewed asset manifest when present",
    "Resolve TileType, BuildingType, AgentRole and UI sprite ids with procedural fallback",
    "Keep renderer non-crashing when images or manifest are absent",
  ], [
    "Visual owner review for final sprite mapping",
  ]);
}

export function createPixelFieldBenchmarkWorkpackDraft(state: CityState): WorkpackDraft {
  return createTypedDraftV07("pixel-field-benchmark", state, [
    "artifacts/duat-city/src/bench/visualBenchmark.ts",
    "artifacts/duat-city/docs/VISUAL_BENCHMARK_v0_7.json",
    "artifacts/duat-city/docs/PIXEL_FIELD_QA_v0_7.md",
  ], [
    "Run local visual benchmark scenarios with pixel field on/off",
    "Record active cells, skipped cells, R_field intent and graphics/physics metrics",
    "Keep benchmark as local estimate, not cloud profiling",
  ], [
    "Manual browser profiling is still recommended for exact FPS/CPU",
  ]);
}

export function createRPGVisualExportWorkpackDraft(state: CityState): WorkpackDraft {
  return createTypedDraftV07("rpg-visual-export", state, [
    "artifacts/duat-city/src/rpg/worldExport.ts",
    "artifacts/duat-city/src/rpg/rpgTypes.ts",
    "artifacts/duat-city/public/asset-manifest/asset_allowlist_v0_7.json",
  ], [
    "Add visual profile, reviewed asset refs, tile atlas refs and screenshot refs to RPG v2 export",
    "Keep private source paths out of public manifests",
    "Validate schema with rpgVisualExport tests",
  ], [
    "Consumer compatibility review for MEDIOEVO RPG imports",
  ]);
}

export function createQuaternaryTimingDiagnosticsWorkpackDraft(state: CityState): WorkpackDraft {
  return {
    ...createTypedDraft("quaternary-timing-diagnostics", state, [
      "artifacts/duat-city/src/quaternary/*",
      "artifacts/duat-city/src/sim/quaternaryAdapter.ts",
      "artifacts/duat-city/src/components/QuaternaryPanel.tsx",
      "artifacts/duat-city/docs/QUATERNARY_TIMING_CORE_v0_9.md",
    ], [
      "Review quaternary timing metrics and top unstable sources",
      "Prepare local diagnostics only; no MCP execution or real apply path",
      "Keep public claims limited to operational formal-lab software",
    ], [
      "Owner review required for public claims, assets or external publication",
    ]),
    schema: "wabi/duat-city/workpack-draft/v0.9-design",
    owner_review_required: false,
    required_owner_review: [
      "Public claims/assets still require owner review before release",
    ],
    execution_allowed: false,
    sandbox_execution_allowed: false,
    real_apply_allowed: false,
  };
}
