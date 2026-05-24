import type { RenderQualityPreset } from "../pixelRealism/renderPasses";

export interface PerformanceBenchmarkV11Scenario {
  id: string;
  label: string;
  qualityPreset: RenderQualityPreset;
  viewMode: "OPERATIONAL" | "BEAUTIFUL" | "DEBUG";
  vibePreset?: string;
  agentCount?: number;
}

export interface PerformanceBenchmarkV11Result {
  scenario: string;
  label: string;
  avgFPS: number;
  p95FrameMs: number;
  minFPS: number;
  maxFPS: number;
  droppedFrames: number;
  activeLightCells: number;
  activeMaterialCells: number;
  particles: number;
  agents: number;
  pixelFieldResolution: string;
  qualityPreset: RenderQualityPreset;
  visibleBrowser: boolean;
  finite: boolean;
}

export interface PerformanceBenchmarkV11Document {
  schema: "duat/performance-benchmark/v1.1";
  fingerprint: "DUAT-v1.1-PLAYABLE-SCENE-QA";
  generatedAt: string;
  durationMsPerScenario: number;
  browser: string;
  visibleBrowser: boolean;
  scenarios: PerformanceBenchmarkV11Result[];
  notes: string[];
}

export const V11_BENCHMARK_SCENARIOS: PerformanceBenchmarkV11Scenario[] = [
  { id: "low_80x45", label: "LOW 80x45", qualityPreset: "LOW", viewMode: "OPERATIONAL" },
  { id: "medium_160x90", label: "MEDIUM 160x90", qualityPreset: "MEDIUM", viewMode: "OPERATIONAL" },
  { id: "high_320x180", label: "HIGH 320x180", qualityPreset: "HIGH", viewMode: "OPERATIONAL" },
  { id: "beautiful", label: "BEAUTIFUL", qualityPreset: "BEAUTIFUL", viewMode: "BEAUTIFUL", vibePreset: "sunny_castle_lake" },
  { id: "debug_light_grid", label: "DEBUG light grid", qualityPreset: "DEBUG", viewMode: "DEBUG" },
  { id: "neon_rain_street", label: "neon rain street", qualityPreset: "HIGH", viewMode: "OPERATIONAL", vibePreset: "neon_rain_street" },
  { id: "warm_interior_tavern", label: "warm interior tavern", qualityPreset: "HIGH", viewMode: "OPERATIONAL", vibePreset: "warm_interior_tavern" },
  { id: "archeopunk_city_night", label: "archeopunk city night", qualityPreset: "HIGH", viewMode: "OPERATIONAL", vibePreset: "archeopunk_city_night" },
  { id: "agents_50", label: "50 agents", qualityPreset: "MEDIUM", viewMode: "OPERATIONAL", agentCount: 50 },
  { id: "agents_100", label: "100 agents", qualityPreset: "MEDIUM", viewMode: "OPERATIONAL", agentCount: 100 },
];

export function validatePerformanceBenchmarkV11(doc: PerformanceBenchmarkV11Document): boolean {
  const required = new Set(V11_BENCHMARK_SCENARIOS.map(scenario => scenario.id));
  for (const scenario of doc.scenarios) {
    required.delete(scenario.scenario);
    const values = [
      scenario.avgFPS,
      scenario.p95FrameMs,
      scenario.minFPS,
      scenario.maxFPS,
      scenario.droppedFrames,
      scenario.activeLightCells,
      scenario.activeMaterialCells,
      scenario.particles,
      scenario.agents,
    ];
    if (!values.every(Number.isFinite)) return false;
  }
  return doc.schema === "duat/performance-benchmark/v1.1"
    && doc.fingerprint === "DUAT-v1.1-PLAYABLE-SCENE-QA"
    && required.size === 0
    && doc.scenarios.every(scenario => scenario.finite);
}

export function pixelResolutionForQuality(quality: RenderQualityPreset): string {
  if (quality === "LOW") return "80x45";
  if (quality === "HIGH" || quality === "BEAUTIFUL") return "320x180";
  return "160x90";
}
