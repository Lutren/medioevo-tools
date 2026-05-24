import type { CityState } from "../core/types";
import type { GraphicsMetrics } from "../graphics/types";
import type { PhysicsMetrics } from "../physics/types";

export interface WabiMcpStatus {
  version: "v0.5-design";
  mode: "LOCALHOST_ONLY_READ_PREPARE_SANDBOX_OPT_IN_DESIGN";
  gated_write_enabled: false;
  execution_allowed: false;
  sandbox_execution_allowed: false;
  real_apply_allowed: false;
  external_clients_allowed: false;
}

export interface WorkpackDraft {
  schema: "wabi/duat-city/workpack-draft/v0.5-design" | "wabi/duat-city/workpack-draft/v0.6-design" | "wabi/duat-city/workpack-draft/v0.7-design" | "wabi/duat-city/workpack-draft/v0.9-design";
  workpack_type?: "city" | "asset-forensics" | "graphics-upgrade" | "physics-field" | "rpg-export" | "asset-allowlist" | "visual-atlas-integration" | "pixel-field-benchmark" | "rpg-visual-export" | "quaternary-timing-diagnostics";
  suggested_files: string[];
  target_files?: string[];
  tasks: string[];
  planned_changes?: string[];
  risks: string[];
  tests_to_run: string[];
  rollback_plan: string[];
  required_owner_review?: string[];
  owner_review_required?: boolean;
  execution_allowed?: false;
  sandbox_execution_allowed?: false;
  real_apply_allowed?: false;
}

export interface SandboxExecutionDesign {
  schema: "wabi/sandbox-policy/v0.5-design";
  sandbox_root: string;
  allowlist: string[];
  denylist: string[];
  commands: string[];
  default_disabled: true;
  requires_future_explicit_opt_in: true;
}

export interface WabiHandoff {
  schema: "wabi/duat-city/handoff/v0.5-design";
  mode: WabiMcpStatus["mode"];
  gated_write_enabled: false;
  execution_allowed: false;
  real_apply_allowed: false;
  city: {
    tick: number;
    R: number;
    Phi_eff: number;
    regime: string;
    gate: string;
    agents: number;
    active_tasks: number;
  };
  physics?: PhysicsMetrics;
  graphics?: GraphicsMetrics;
  recommended_workpacks: WorkpackDraft[];
  next_safe_action: "prepare-only review; no execution";
}

export interface WabiBridgeInput {
  state: CityState;
  physicsMetrics?: PhysicsMetrics;
  graphicsMetrics?: GraphicsMetrics;
}
