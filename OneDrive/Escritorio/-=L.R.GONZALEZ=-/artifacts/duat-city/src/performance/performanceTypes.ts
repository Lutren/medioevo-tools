import type { ViewMode } from "../graphics/types";

export type PerformanceStatus = "PERF_OPTIMO" | "PERF_FUNCIONAL" | "PERF_CARGADO" | "PERF_SATURADO";

export interface PerformanceRenderCounters {
  agentsRendered: number;
  buildingsRendered: number;
  tilesRendered: number;
  particlesRendered: number;
  activePixelCells: number;
  dirtyChunks: number;
  overlaysEnabled: boolean;
  viewMode: ViewMode;
  cameraZoom: number;
}

export interface FpsSamplerOptions {
  sampleWindowSeconds?: number;
  targetFrameMs?: number;
}

export interface FpsSnapshot extends PerformanceRenderCounters {
  currentFps: number;
  avgFps: number;
  minFps: number;
  maxFps: number;
  frameMs: number;
  avgFrameMs: number;
  p50FrameMs: number;
  p95FrameMs: number;
  p99FrameMs: number;
  droppedFrames: number;
  longFramesOver16ms: number;
  longFramesOver33ms: number;
  sampleWindowSeconds: number;
  totalFrames: number;
  lastResetAt: number;
}

export interface PerformanceBenchmarkOutput {
  schema: "duat/performance-benchmark/v0.8";
  timestamp: string;
  durationMs: number;
  viewMode: string;
  agents: number;
  buildings: number;
  avgFps: number;
  p95FrameMs: number;
  droppedFrames: number;
  R_graphics: number;
  Phi_graphics: number;
  notes: string[];
}

export function defaultRenderCounters(viewMode: ViewMode = "OPERATIONAL", cameraZoom = 1): PerformanceRenderCounters {
  return {
    agentsRendered: 0,
    buildingsRendered: 0,
    tilesRendered: 0,
    particlesRendered: 0,
    activePixelCells: 0,
    dirtyChunks: 0,
    overlaysEnabled: false,
    viewMode,
    cameraZoom,
  };
}
