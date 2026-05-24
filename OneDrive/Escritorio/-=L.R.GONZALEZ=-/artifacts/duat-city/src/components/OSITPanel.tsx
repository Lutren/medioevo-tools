import type { CityState } from "../core/types";
import type { ViewMode } from "../graphics/types";
import type { FpsSnapshot } from "../performance/performanceTypes";
import { rColor, GATE_COLORS, REGIME_COLORS } from "../render/palette";
import { computeRegime, computeGate, computeNextAction } from "../core/metrics";
import { getWitnessTail } from "../core/witnesslog";
import { getResourceShortage } from "../sim/resources";
import { TaskPanel } from "./TaskPanel";
import { ResourcePanel } from "./ResourcePanel";
import { WabiPanel } from "./WabiPanel";
import { PerformancePanel } from "./PerformancePanel";
import { QuaternaryPanel } from "./QuaternaryPanel";

interface OSITPanelProps {
  state: CityState;
  viewMode?: ViewMode;
  focus?: "wabi";
  performanceSnapshot?: FpsSnapshot;
  benchmarkRunning?: boolean;
  benchmarkProgress?: number;
  onResetPerformance?: () => void;
  onCopyPerformanceJson?: () => void;
  onRunPerformanceBenchmark?: (durationMs?: number) => void;
  focusedBenchmarkRunning?: boolean;
  focusedBenchmarkProgress?: number;
  focusedBenchmarkDuration?: number;
  onFocusedBenchmarkDuration?: (durationMs: number) => void;
  onRunFocusedBenchmark?: (durationMs?: number) => void;
}

export function OSITPanel({
  state,
  viewMode = "OPERATIONAL",
  focus,
  performanceSnapshot,
  benchmarkRunning,
  benchmarkProgress,
  onResetPerformance,
  onCopyPerformanceJson,
  onRunPerformanceBenchmark,
  focusedBenchmarkRunning,
  focusedBenchmarkProgress,
  focusedBenchmarkDuration,
  onFocusedBenchmarkDuration,
  onRunFocusedBenchmark,
}: OSITPanelProps) {
  const { R, Phi_eff, regime, gate, tick } = state;
  const shortages = getResourceShortage(state.resources);
  const witness = getWitnessTail(state, 8);
  const nextAction = computeNextAction(gate, regime);

  const blocked = state.agents.filter(a => a.gate === "BLOCK").length;
  const review = state.agents.filter(a => a.gate === "REVIEW").length;
  const ruins = state.buildings.filter(b => b.type === "ruin").length;
  const failed = state.tasks.filter(t => t.status === "failed").length;
  const RPhysics = state.physicsMetrics?.R_physics ?? 0;
  const PhiPhysics = state.physicsMetrics?.Phi_physics ?? 1;
  const RGraphics = state.graphicsMetrics?.R_graphics ?? 0;
  const PhiGraphics = state.graphicsMetrics?.Phi_graphics ?? 1;
  const RField = state.fieldMetrics?.R_field ?? 0;
  const PhiField = state.fieldMetrics?.Phi_field ?? 1;
  const pixel = state.pixelRealism;
  const combinedR = Math.max(0, Math.min(1, 0.50 * R + 0.18 * RPhysics + 0.18 * RGraphics + 0.14 * RField));
  const combinedPhi = Math.max(0, Math.min(1, 0.50 * Phi_eff + 0.18 * PhiPhysics + 0.18 * PhiGraphics + 0.14 * PhiField));

  return (
    <div className="panel-right">
      <div className="section">
        <div className="section-title">📊 OSIT / DUAT Dashboard</div>
        <div className="stat-row">
          <span className="stat-key">Tick</span>
          <span className="stat-val">{tick}</span>
        </div>
        <div className="stat-row">
          <span className="stat-key">Regime</span>
          <span className="stat-val" style={{ color: REGIME_COLORS[regime] }}>{regime}</span>
        </div>
        <div className="stat-row">
          <span className="stat-key">Gate</span>
          <span className="stat-val" style={{ color: GATE_COLORS[gate] }}>{gate}</span>
        </div>
        <div className="need-row" style={{ marginTop: 4 }}>
          <span className="need-label">R</span>
          <div className="need-bar-wrap"><div className="progress-bar"><div className="progress-fill bar-r" style={{ width: `${R * 100}%` }} /></div></div>
          <span className="stat-val" style={{ color: rColor(R), minWidth: 36 }}>{R.toFixed(3)}</span>
        </div>
        <div className="need-row">
          <span className="need-label">Φ_eff</span>
          <div className="need-bar-wrap"><div className="progress-bar"><div className="progress-fill bar-phi" style={{ width: `${Phi_eff * 100}%` }} /></div></div>
          <span className="stat-val" style={{ color: rColor(1 - Phi_eff), minWidth: 36 }}>{Phi_eff.toFixed(3)}</span>
        </div>
      </div>

      <div className="section">
        <div className="section-title">Risk Indicators</div>
        <div className="stat-row"><span className="stat-key">Blocked Agents</span><span className="stat-val" style={{ color: blocked > 0 ? "#ff4444" : "#00ff9d" }}>{blocked}</span></div>
        <div className="stat-row"><span className="stat-key">In Review</span><span className="stat-val" style={{ color: review > 0 ? "#ffcc00" : "#00ff9d" }}>{review}</span></div>
        <div className="stat-row"><span className="stat-key">Failed Tasks</span><span className="stat-val" style={{ color: failed > 0 ? "#ff4444" : "#00ff9d" }}>{failed}</span></div>
        <div className="stat-row"><span className="stat-key">Ruins</span><span className="stat-val" style={{ color: ruins > 0 ? "#ff6b35" : "#00ff9d" }}>{ruins}</span></div>
        {shortages.length > 0 && (
          <div className="stat-row">
            <span className="stat-key">Shortages</span>
            <span className="stat-val" style={{ color: "#ff4444" }}>{shortages.join(", ")}</span>
          </div>
        )}
      </div>

      <div className="section">
        <div className="section-title">Subsystem Metrics</div>
        <div className="stat-row"><span className="stat-key">R physics</span><span className="stat-val">{RPhysics.toFixed(3)}</span></div>
        <div className="stat-row"><span className="stat-key">Phi physics</span><span className="stat-val">{PhiPhysics.toFixed(3)}</span></div>
        <div className="stat-row"><span className="stat-key">R graphics</span><span className="stat-val">{RGraphics.toFixed(3)}</span></div>
        <div className="stat-row"><span className="stat-key">Phi graphics</span><span className="stat-val">{PhiGraphics.toFixed(3)}</span></div>
        <div className="stat-row"><span className="stat-key">R field</span><span className="stat-val">{RField.toFixed(3)}</span></div>
        <div className="stat-row"><span className="stat-key">Phi field</span><span className="stat-val">{PhiField.toFixed(3)}</span></div>
        <div className="stat-row"><span className="stat-key">R combined</span><span className="stat-val" style={{ color: rColor(combinedR) }}>{combinedR.toFixed(3)}</span></div>
        <div className="stat-row"><span className="stat-key">Phi combined</span><span className="stat-val" style={{ color: rColor(1 - combinedPhi) }}>{combinedPhi.toFixed(3)}</span></div>
      </div>

      <div className="section">
        <div className="section-title">Pixel Realism Health</div>
        <div className="stat-row"><span className="stat-key">Light health</span><span className="stat-val">{pixel ? `${pixel.R_light.toFixed(3)} / ${pixel.Phi_light.toFixed(3)}` : "n/a"}</span></div>
        <div className="stat-row"><span className="stat-key">Color health</span><span className="stat-val">{pixel ? `${pixel.R_color.toFixed(3)} / ${pixel.Phi_color.toFixed(3)}` : "n/a"}</span></div>
        <div className="stat-row"><span className="stat-key">Pixel field</span><span className="stat-val">{pixel ? `${pixel.R_pixelField.toFixed(3)} / ${pixel.Phi_pixelField.toFixed(3)}` : "n/a"}</span></div>
        <div className="stat-row"><span className="stat-key">Render quality</span><span className="stat-val">{pixel?.qualityPreset ?? "n/a"}</span></div>
        <div className="stat-row"><span className="stat-key">Vibe scene</span><span className="stat-val">{pixel?.vibePreset ?? "none"}</span></div>
        <div className="stat-row"><span className="stat-key">Playable scene</span><span className="stat-val">{state.playableScene ? `${state.playableScene.metrics.activeMaterialCells} cells / ${state.playableScene.metrics.activeLightSources} lights` : "none"}</span></div>
        <div className="stat-row"><span className="stat-key">Q summary</span><span className="stat-val">{pixel ? JSON.stringify(pixel.qStateCounts) : "n/a"}</span></div>
      </div>

      <QuaternaryPanel state={state} />

      {performanceSnapshot && (
        <PerformancePanel
          snapshot={performanceSnapshot}
          graphicsMetrics={state.graphicsMetrics}
          benchmarkRunning={benchmarkRunning}
          benchmarkProgress={benchmarkProgress}
          onReset={onResetPerformance ?? (() => undefined)}
          onCopyJson={onCopyPerformanceJson ?? (() => undefined)}
          onRunBenchmark={onRunPerformanceBenchmark ?? (() => undefined)}
          focusedBenchmarkRunning={focusedBenchmarkRunning}
          focusedBenchmarkProgress={focusedBenchmarkProgress}
          focusedBenchmarkDuration={focusedBenchmarkDuration}
          onFocusedBenchmarkDuration={onFocusedBenchmarkDuration}
          onRunFocusedBenchmark={onRunFocusedBenchmark}
        />
      )}

      <div className="section">
        <div className="section-title">Next Action</div>
        <div style={{ color: GATE_COLORS[gate], fontSize: 11, lineHeight: 1.4 }}>{nextAction}</div>
      </div>

      <div className="section">
        <div className="section-title">Witness Log</div>
        {witness.length === 0 && <span className="stat-key">No entries yet</span>}
        {witness.map(w => (
          <div key={w.id} className="witness-entry">
            <span className="witness-tick">T{w.tick}</span>
            <span className="witness-summary">{w.summary}</span>
          </div>
        ))}
      </div>

      {viewMode === "DEBUG" && (
        <div className="section">
          <div className="section-title">Pixel Field QA</div>
          <div className="stat-row"><span className="stat-key">Active cells</span><span className="stat-val">{state.fieldMetrics?.activeCells ?? 0}</span></div>
          <div className="stat-row"><span className="stat-key">Skipped cells</span><span className="stat-val">{state.fieldMetrics?.skippedCells ?? 0}</span></div>
          <div className="stat-row"><span className="stat-key">Hazards</span><span className="stat-val">{state.fieldSummary?.hazards.join(", ") || "none"}</span></div>
          <div style={{ color: "#8cb7c9", fontSize: 11, lineHeight: 1.35 }}>water falls · smoke rises · fire emits smoke/light · inactive cells skipped</div>
        </div>
      )}

      {focus === "wabi" && <WabiPanel state={state} />}
      <TaskPanel state={state} />
      <ResourcePanel state={state} />
      {focus !== "wabi" && <WabiPanel state={state} />}
    </div>
  );
}
