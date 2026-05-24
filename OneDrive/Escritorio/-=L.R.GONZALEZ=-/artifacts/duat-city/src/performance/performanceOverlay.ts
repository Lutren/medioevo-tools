import type { CityState } from "../core/types";
import type { FpsSnapshot, PerformanceBenchmarkOutput, PerformanceStatus } from "./performanceTypes";

export function classifyPerformance(avgFps: number): PerformanceStatus {
  if (avgFps >= 55) return "PERF_OPTIMO";
  if (avgFps >= 30) return "PERF_FUNCIONAL";
  if (avgFps >= 20) return "PERF_CARGADO";
  return "PERF_SATURADO";
}

export function createPerformanceBenchmarkOutput(
  snapshot: FpsSnapshot,
  state: CityState,
  durationMs: number,
  notes: string[] = [],
): PerformanceBenchmarkOutput {
  return {
    schema: "duat/performance-benchmark/v0.8",
    timestamp: new Date().toISOString(),
    durationMs,
    viewMode: snapshot.viewMode,
    agents: state.agents.length,
    buildings: state.buildings.length,
    avgFps: finite(snapshot.avgFps),
    p95FrameMs: finite(snapshot.p95FrameMs),
    droppedFrames: Math.max(0, Math.floor(finite(snapshot.droppedFrames))),
    R_graphics: finite(state.graphicsMetrics?.R_graphics ?? 0),
    Phi_graphics: finite(state.graphicsMetrics?.Phi_graphics ?? 1),
    notes,
  };
}

function finite(value: number): number {
  return Number.isFinite(value) ? value : 0;
}
