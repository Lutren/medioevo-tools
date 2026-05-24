import type { RenderQualityPreset } from "../pixelRealism/renderPasses";

export type BenchmarkBrowserMode = "headed" | "headless" | "CDP" | "fallback";
export type BenchmarkFocusStatus = "focused" | "unconfirmed" | "not_available";

export interface PerformanceBenchmarkV111Scenario {
  id: string;
  label: string;
  qualityPreset: RenderQualityPreset;
  viewMode: "OPERATIONAL" | "BEAUTIFUL" | "DEBUG";
  vibePreset?: string;
  agentCount?: number;
  sceneDemo?: "material_placement";
}

export interface PerformanceBenchmarkV111Result {
  scenario: string;
  label: string;
  avgFps: number;
  minFps: number;
  maxFps: number;
  p95FrameMs: number;
  p99FrameMs: number;
  droppedFrames: number;
  activeLightCells: number;
  activeMaterialCells: number;
  particles: number;
  agents: number;
  pixelFieldResolution: string;
  qualityPreset: RenderQualityPreset;
  viewMode: "OPERATIONAL" | "BEAUTIFUL" | "DEBUG";
  browserMode: BenchmarkBrowserMode;
  focusStatus: BenchmarkFocusStatus;
  finite: boolean;
}

export interface PerformanceBenchmarkV111Document {
  schema: "duat/performance-benchmark/v1.1.1";
  fingerprint: "DUAT-v1.1.1-FOCUSED-FPS-CLOSURE";
  generatedAt: string;
  durationMsPerScenario: number;
  browser: string;
  browserMode: BenchmarkBrowserMode;
  focusStatus: BenchmarkFocusStatus;
  focusedBrowserAvailable: boolean;
  scenarios: PerformanceBenchmarkV111Result[];
  notes: string[];
}

export const V111_BENCHMARK_SCENARIOS: PerformanceBenchmarkV111Scenario[] = [
  { id: "low_80x45_baseline", label: "LOW 80x45 baseline", qualityPreset: "LOW", viewMode: "OPERATIONAL" },
  { id: "medium_160x90", label: "MEDIUM 160x90", qualityPreset: "MEDIUM", viewMode: "OPERATIONAL" },
  { id: "high_320x180", label: "HIGH 320x180", qualityPreset: "HIGH", viewMode: "OPERATIONAL" },
  { id: "beautiful_sunny_castle_lake", label: "BEAUTIFUL sunny/castle/lake", qualityPreset: "BEAUTIFUL", viewMode: "BEAUTIFUL", vibePreset: "sunny_castle_lake" },
  { id: "beautiful_neon_rain_street", label: "BEAUTIFUL neon rain street", qualityPreset: "BEAUTIFUL", viewMode: "BEAUTIFUL", vibePreset: "neon_rain_street" },
  { id: "warm_interior_tavern", label: "warm interior tavern", qualityPreset: "HIGH", viewMode: "OPERATIONAL", vibePreset: "warm_interior_tavern" },
  { id: "archeopunk_city_night", label: "archeopunk city night", qualityPreset: "HIGH", viewMode: "OPERATIONAL", vibePreset: "archeopunk_city_night" },
  { id: "debug_light_grid", label: "DEBUG light grid", qualityPreset: "DEBUG", viewMode: "DEBUG" },
  { id: "material_placement", label: "material placement water/fire/smoke/stone/neon", qualityPreset: "HIGH", viewMode: "OPERATIONAL", sceneDemo: "material_placement" },
  { id: "agents_100_light_engine", label: "100 agents + light engine active", qualityPreset: "HIGH", viewMode: "OPERATIONAL", agentCount: 100, vibePreset: "neon_rain_street" },
];

export function validatePerformanceBenchmarkV111(doc: PerformanceBenchmarkV111Document): boolean {
  const required = new Set(V111_BENCHMARK_SCENARIOS.map(scenario => scenario.id));
  for (const scenario of doc.scenarios) {
    required.delete(scenario.scenario);
    const values = [
      scenario.avgFps,
      scenario.minFps,
      scenario.maxFps,
      scenario.p95FrameMs,
      scenario.p99FrameMs,
      scenario.droppedFrames,
      scenario.activeLightCells,
      scenario.activeMaterialCells,
      scenario.particles,
      scenario.agents,
    ];
    if (!values.every(Number.isFinite)) return false;
    if (!scenario.browserMode || !scenario.focusStatus) return false;
  }
  return doc.schema === "duat/performance-benchmark/v1.1.1"
    && doc.fingerprint === "DUAT-v1.1.1-FOCUSED-FPS-CLOSURE"
    && required.size === 0
    && doc.scenarios.every(scenario => scenario.finite);
}

export function pixelResolutionForQualityV111(quality: RenderQualityPreset): string {
  if (quality === "LOW") return "80x45";
  if (quality === "HIGH" || quality === "BEAUTIFUL") return "320x180";
  return "160x90";
}
