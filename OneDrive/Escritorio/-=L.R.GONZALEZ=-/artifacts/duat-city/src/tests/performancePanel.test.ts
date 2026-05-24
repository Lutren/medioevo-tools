import { describe, expect, it } from "vitest";
import { createCity } from "../sim/city";
import { createPerformanceBenchmarkOutput, classifyPerformance } from "../performance/performanceOverlay";
import { type FpsSnapshot, defaultRenderCounters } from "../performance/performanceTypes";

describe("performance overlay v0.8", () => {
  it("classifies performance regimes", () => {
    expect(classifyPerformance(60)).toBe("PERF_OPTIMO");
    expect(classifyPerformance(45)).toBe("PERF_FUNCIONAL");
    expect(classifyPerformance(24)).toBe("PERF_CARGADO");
    expect(classifyPerformance(12)).toBe("PERF_SATURADO");
  });

  it("benchmark schema has required fields", () => {
    const snapshot: FpsSnapshot = {
      ...defaultRenderCounters("DEBUG", 1.2),
      currentFps: 58,
      avgFps: 55,
      minFps: 40,
      maxFps: 62,
      frameMs: 16,
      avgFrameMs: 18,
      p50FrameMs: 17,
      p95FrameMs: 28,
      p99FrameMs: 33,
      droppedFrames: 2,
      longFramesOver16ms: 4,
      longFramesOver33ms: 1,
      sampleWindowSeconds: 10,
      totalFrames: 120,
      lastResetAt: 1,
    };
    const output = createPerformanceBenchmarkOutput(snapshot, createCity(), 30_000, ["test"]);
    expect(output.schema).toBe("duat/performance-benchmark/v0.8");
    expect(output.avgFps).toBe(55);
    expect(output.p95FrameMs).toBe(28);
    expect(output.notes).toContain("test");
  });
});
