import {
  createAssetAllowlistWorkpackDraft,
  createPixelFieldBenchmarkWorkpackDraft,
  createQuaternaryTimingDiagnosticsWorkpackDraft,
  createRPGVisualExportWorkpackDraft,
  createVisualAtlasIntegrationWorkpackDraft,
  createWorkpackDraftFromCity,
} from "./workpackDraft";
import { getWabiMcpStatus } from "./mcpDesignBridge";
import type { WabiBridgeInput, WabiHandoff } from "./types";

export function toWabiHandoff(input: WabiBridgeInput): WabiHandoff {
  const status = getWabiMcpStatus();
  const activeTasks = input.state.tasks.filter(t => t.status === "active").length;
  return {
    schema: "wabi/duat-city/handoff/v0.5-design",
    mode: status.mode,
    gated_write_enabled: false,
    execution_allowed: false,
    real_apply_allowed: false,
    city: {
      tick: input.state.tick,
      R: input.state.R,
      Phi_eff: input.state.Phi_eff,
      regime: input.state.regime,
      gate: input.state.gate,
      agents: input.state.agents.length,
      active_tasks: activeTasks,
    },
    physics: input.physicsMetrics,
    graphics: input.graphicsMetrics,
    recommended_workpacks: [
      createWorkpackDraftFromCity(input.state),
      createAssetAllowlistWorkpackDraft(input.state),
      createVisualAtlasIntegrationWorkpackDraft(input.state),
      createPixelFieldBenchmarkWorkpackDraft(input.state),
      createRPGVisualExportWorkpackDraft(input.state),
      createQuaternaryTimingDiagnosticsWorkpackDraft(input.state),
    ],
    next_safe_action: "prepare-only review; no execution",
  };
}
