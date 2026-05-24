import type { GraphicsMetrics } from "../graphics/types";
import type { FpsSnapshot } from "../performance/performanceTypes";
import { classifyPerformance } from "../performance/performanceOverlay";
import { GATE_COLORS } from "../render/palette";

interface PerformancePanelProps {
  snapshot: FpsSnapshot;
  graphicsMetrics?: GraphicsMetrics;
  benchmarkRunning?: boolean;
  benchmarkProgress?: number;
  onReset: () => void;
  onCopyJson: () => void;
  onRunBenchmark: (durationMs?: number) => void;
  focusedBenchmarkRunning?: boolean;
  focusedBenchmarkProgress?: number;
  focusedBenchmarkDuration?: number;
  onFocusedBenchmarkDuration?: (durationMs: number) => void;
  onRunFocusedBenchmark?: (durationMs?: number) => void;
}

export function PerformancePanel({
  snapshot,
  graphicsMetrics,
  benchmarkRunning = false,
  benchmarkProgress = 0,
  onReset,
  onCopyJson,
  onRunBenchmark,
  focusedBenchmarkRunning = false,
  focusedBenchmarkProgress = 0,
  focusedBenchmarkDuration = 10_000,
  onFocusedBenchmarkDuration,
  onRunFocusedBenchmark,
}: PerformancePanelProps) {
  const status = classifyPerformance(snapshot.avgFps);
  const color = status === "PERF_OPTIMO" ? GATE_COLORS.APPROVE : status === "PERF_FUNCIONAL" ? "#7bc8f6" : status === "PERF_CARGADO" ? GATE_COLORS.REVIEW : GATE_COLORS.BLOCK;
  return (
    <div className="section">
      <div className="section-title">Performance</div>
      <div className="stat-row"><span className="stat-key">Status</span><span className="stat-val" style={{ color }}>{status}</span></div>
      <div className="stat-row"><span className="stat-key">Current FPS</span><span className="stat-val">{snapshot.currentFps.toFixed(1)}</span></div>
      <div className="stat-row"><span className="stat-key">Avg FPS</span><span className="stat-val">{snapshot.avgFps.toFixed(1)}</span></div>
      <div className="stat-row"><span className="stat-key">p95 frame</span><span className="stat-val">{snapshot.p95FrameMs.toFixed(2)} ms</span></div>
      <div className="stat-row"><span className="stat-key">Dropped</span><span className="stat-val">{snapshot.droppedFrames}</span></div>
      <div className="stat-row"><span className="stat-key">Agents rendered</span><span className="stat-val">{snapshot.agentsRendered}</span></div>
      <div className="stat-row"><span className="stat-key">Particles</span><span className="stat-val">{snapshot.particlesRendered}</span></div>
      <div className="stat-row"><span className="stat-key">Dirty chunks</span><span className="stat-val">{snapshot.dirtyChunks}</span></div>
      <div className="stat-row"><span className="stat-key">Active cells</span><span className="stat-val">{snapshot.activePixelCells}</span></div>
      <div className="stat-row"><span className="stat-key">View</span><span className="stat-val">{snapshot.viewMode}</span></div>
      <div className="stat-row"><span className="stat-key">Zoom</span><span className="stat-val">{snapshot.cameraZoom.toFixed(2)}</span></div>
      <div className="stat-row"><span className="stat-key">R graphics</span><span className="stat-val">{(graphicsMetrics?.R_graphics ?? 0).toFixed(3)}</span></div>
      <div className="stat-row"><span className="stat-key">Phi graphics</span><span className="stat-val">{(graphicsMetrics?.Phi_graphics ?? 1).toFixed(3)}</span></div>
      {benchmarkRunning && (
        <div className="progress-bar" title="benchmark progress">
          <div className="progress-fill bar-phi" style={{ width: `${Math.max(0, Math.min(1, benchmarkProgress)) * 100}%` }} />
        </div>
      )}
      <div className="ctrl-row">
        <button className="ctrl-btn" onClick={onReset}>Reset sampler</button>
        <button className="ctrl-btn" onClick={onCopyJson}>Copy JSON</button>
      </div>
      <div className="ctrl-row">
        <button className={`ctrl-btn ${benchmarkRunning ? "primary" : ""}`} onClick={() => onRunBenchmark()}>
          {benchmarkRunning ? "Benchmarking" : "Run 30s Benchmark"}
        </button>
      </div>
      <div className="field-label">Focused FPS v1.1.1</div>
      <select
        className="select-input"
        value={focusedBenchmarkDuration}
        onChange={event => onFocusedBenchmarkDuration?.(Number(event.target.value))}
      >
        <option value={10_000}>10s</option>
        <option value={30_000}>30s</option>
        <option value={60_000}>60s</option>
      </select>
      {focusedBenchmarkRunning && (
        <div className="progress-bar" title="focused benchmark progress">
          <div className="progress-fill bar-phi" style={{ width: `${Math.max(0, Math.min(1, focusedBenchmarkProgress)) * 100}%` }} />
        </div>
      )}
      <div className="ctrl-row">
        <button className={`ctrl-btn ${focusedBenchmarkRunning ? "primary" : ""}`} onClick={() => onRunFocusedBenchmark?.(focusedBenchmarkDuration)}>
          {focusedBenchmarkRunning ? "Focused Run" : "Run Focused FPS"}
        </button>
      </div>
      <div className="panel-note">For real focus, click this button in the visible browser and keep the tab active until JSON downloads.</div>
    </div>
  );
}
