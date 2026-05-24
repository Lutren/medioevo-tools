import { describe, expect, it } from "vitest";
import {
  pixelResolutionForQualityV111,
  validatePerformanceBenchmarkV111,
  V111_BENCHMARK_SCENARIOS,
  type PerformanceBenchmarkV111Document,
} from "../performance/benchmarkV111";

describe("focused benchmark runner v1.1.1", () => {
  it("lists all required focused scenarios", () => {
    expect(V111_BENCHMARK_SCENARIOS.map(s => s.id)).toEqual([
      "low_80x45_baseline",
      "medium_160x90",
      "high_320x180",
      "beautiful_sunny_castle_lake",
      "beautiful_neon_rain_street",
      "warm_interior_tavern",
      "archeopunk_city_night",
      "debug_light_grid",
      "material_placement",
      "agents_100_light_engine",
    ]);
  });

  it("validates finite schema and focus fields", () => {
    const doc: PerformanceBenchmarkV111Document = {
      schema: "duat/performance-benchmark/v1.1.1",
      fingerprint: "DUAT-v1.1.1-FOCUSED-FPS-CLOSURE",
      generatedAt: "2026-05-19T00:00:00.000Z",
      durationMsPerScenario: 10_000,
      browser: "test",
      browserMode: "fallback",
      focusStatus: "unconfirmed",
      focusedBrowserAvailable: false,
      scenarios: V111_BENCHMARK_SCENARIOS.map(scenario => ({
        scenario: scenario.id,
        label: scenario.label,
        avgFps: 60,
        minFps: 55,
        maxFps: 61,
        p95FrameMs: 18,
        p99FrameMs: 20,
        droppedFrames: 0,
        activeLightCells: 100,
        activeMaterialCells: 5,
        particles: 8,
        agents: scenario.agentCount ?? 12,
        pixelFieldResolution: pixelResolutionForQualityV111(scenario.qualityPreset),
        qualityPreset: scenario.qualityPreset,
        viewMode: scenario.viewMode,
        browserMode: "fallback",
        focusStatus: "unconfirmed",
        finite: true,
      })),
      notes: ["test"],
    };
    expect(validatePerformanceBenchmarkV111(doc)).toBe(true);
    expect(doc.scenarios.every(scenario => scenario.focusStatus)).toBe(true);
    expect(doc.scenarios.every(scenario => Number.isFinite(scenario.p99FrameMs))).toBe(true);
  });
});
