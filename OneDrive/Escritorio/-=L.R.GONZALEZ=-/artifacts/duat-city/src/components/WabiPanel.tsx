import type { CityState } from "../core/types";
import { downloadJson } from "../core/persistence";
import { getWabiMcpStatus } from "../wabi/mcpDesignBridge";
import { createSandboxExecutionDesign } from "../wabi/sandboxPolicy";
import {
  createAssetWorkpackDraft,
  createAssetAllowlistWorkpackDraft,
  createGraphicsUpgradeWorkpackDraft,
  createPixelFieldBenchmarkWorkpackDraft,
  createPhysicsFieldWorkpackDraft,
  createQuaternaryTimingDiagnosticsWorkpackDraft,
  createRPGExportWorkpackDraft,
  createRPGVisualExportWorkpackDraft,
  createWorkpackDraftFromCity,
  createVisualAtlasIntegrationWorkpackDraft,
} from "../wabi/workpackDraft";
import { toWabiHandoff } from "../wabi/wabiHandoff";

interface WabiPanelProps {
  state: CityState;
}

export function WabiPanel({ state }: WabiPanelProps) {
  const status = getWabiMcpStatus();
  const draft = createWorkpackDraftFromCity(state);
  const policy = createSandboxExecutionDesign(state);

  function downloadDraft() {
    downloadJson(`wabi-workpack-draft-t${state.tick}.json`, JSON.stringify(draft, null, 2));
  }

  function downloadTypedDraft(label: string, payload: unknown) {
    downloadJson(`wabi-${label}-draft-t${state.tick}.json`, JSON.stringify(payload, null, 2));
  }

  function downloadHandoff() {
    const handoff = toWabiHandoff({
      state,
      physicsMetrics: state.physicsMetrics,
      graphicsMetrics: state.graphicsMetrics,
    });
    downloadJson(`wabi-duat-handoff-t${state.tick}.json`, JSON.stringify(handoff, null, 2));
  }

  return (
    <div className="section">
      <div className="section-title">Wabi MCP v0.5</div>
      <div className="stat-row"><span className="stat-key">Mode</span><span className="stat-val">DESIGN ONLY</span></div>
      <div className="stat-row"><span className="stat-key">Execution</span><span className="stat-val" style={{ color: "#ffcc00" }}>{String(status.execution_allowed)}</span></div>
      <div className="stat-row"><span className="stat-key">Real Apply</span><span className="stat-val" style={{ color: "#ffcc00" }}>{String(status.real_apply_allowed)}</span></div>
      <div className="stat-row"><span className="stat-key">Sandbox</span><span className="stat-val">{policy.default_disabled ? "disabled" : "enabled"}</span></div>
      <div className="ctrl-row">
        <button className="ctrl-btn" onClick={downloadDraft}>Workpack Draft</button>
        <button className="ctrl-btn" onClick={downloadHandoff}>Wabi Handoff</button>
      </div>
      <div className="ctrl-row">
        <button className="ctrl-btn" onClick={() => downloadTypedDraft("asset", createAssetWorkpackDraft(state))}>Asset Draft</button>
        <button className="ctrl-btn" onClick={() => downloadTypedDraft("graphics", createGraphicsUpgradeWorkpackDraft(state))}>Graphics Draft</button>
      </div>
      <div className="ctrl-row">
        <button className="ctrl-btn" onClick={() => downloadTypedDraft("physics-field", createPhysicsFieldWorkpackDraft(state))}>Field Draft</button>
        <button className="ctrl-btn" onClick={() => downloadTypedDraft("rpg-export", createRPGExportWorkpackDraft(state))}>RPG Draft</button>
      </div>
      <div className="ctrl-row">
        <button className="ctrl-btn" onClick={() => downloadTypedDraft("asset-allowlist", createAssetAllowlistWorkpackDraft(state))}>Asset Allowlist</button>
        <button className="ctrl-btn" onClick={() => downloadTypedDraft("visual-atlas", createVisualAtlasIntegrationWorkpackDraft(state))}>Atlas Draft</button>
      </div>
      <div className="ctrl-row">
        <button className="ctrl-btn" onClick={() => downloadTypedDraft("pixel-benchmark", createPixelFieldBenchmarkWorkpackDraft(state))}>Benchmark Draft</button>
        <button className="ctrl-btn" onClick={() => downloadTypedDraft("rpg-visual", createRPGVisualExportWorkpackDraft(state))}>RPG Visual</button>
      </div>
      <div className="ctrl-row">
        <button className="ctrl-btn" onClick={() => downloadTypedDraft("quaternary-timing", createQuaternaryTimingDiagnosticsWorkpackDraft(state))}>Q Timing</button>
      </div>
    </div>
  );
}
