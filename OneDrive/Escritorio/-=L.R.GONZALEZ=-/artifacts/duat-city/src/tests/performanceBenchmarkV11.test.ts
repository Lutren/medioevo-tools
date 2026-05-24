import { describe, expect, it } from "vitest";
import {
  pixelResolutionForQuality,
  validatePerformanceBenchmarkV11,
  V11_BENCHMARK_SCENARIOS,
  type PerformanceBenchmarkV11Document,
} from "../performance/benchmarkV11";

describe("performance benchmark v1.1 schema", () => {
  it("lists all required scenarios", () => {
    expect(V11_BENCHMARK_SCENARIOS.map(s => s.id)).toEqual([
      "low_80x45",
      "medium_160x90",
      "high_320x180",
      "beautiful",
      "debug_light_grid",
      "neon_rain_street",
      "warm_interior_tavern",
      "archeopunk_city_night",
      "agents_50",
      "agents_100",
    ]);
  });

  it("validates finite benchmark documents", () => {
    const doc: PerformanceBenchmarkV11Document = {
      schema: "duat/performance-benchmark/v1.1",
      fingerprint: "DUAT-v1.1-PLAYABLE-SCENE-QA",
      generatedAt: "2026-05-19T00:00:00.000Z",
      durationMsPerScenario: 1000,
      browser: "test",
      visibleBrowser: true,
      scenarios: V11_BENCHMARK_SCENARIOS.map(scenario => ({
        scenario: scenario.id,
        label: scenario.label,
        avgFPS: 60,
        p95FrameMs: 18,
        minFPS: 42,
        maxFPS: 62,
        droppedFrames: 0,
        activeLightCells: 10,
        activeMaterialCells: 3,
        particles: 4,
        agents: scenario.agentCount ?? 12,
        pixelFieldResolution: pixelResolutionForQuality(scenario.qualityPreset),
        qualityPreset: scenario.qualityPreset,
        visibleBrowser: true,
        finite: true,
      })),
      notes: [],
    };
    expect(validatePerformanceBenchmarkV11(doc)).toBe(true);
    expect(doc.scenarios.every(s => Number.isFinite(s.avgFPS))).toBe(true);
  });
});
