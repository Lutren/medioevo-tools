import { describe, expect, it } from "vitest";
import { runVisualBenchmark, VISUAL_BENCHMARK_SCENARIOS } from "../bench/visualBenchmark";

describe("visual benchmark v0.7", () => {
  it("outputs FPS and frame-time fields for every scenario", () => {
    const output = runVisualBenchmark(12);
    expect(output.schema).toBe("duat.visual-benchmark.v0.7");
    expect(output.scenarios.map(s => s.id)).toEqual(VISUAL_BENCHMARK_SCENARIOS.map(s => s.id));
    for (const scenario of output.scenarios) {
      expect(scenario.avg_fps).toBeGreaterThan(0);
      expect(scenario.frame_time_avg_ms).toBeGreaterThan(0);
      expect(Number.isFinite(scenario.frame_time_p95_ms)).toBe(true);
      expect(Number.isFinite(scenario.R_graphics)).toBe(true);
      expect(Number.isFinite(scenario.Phi_physics)).toBe(true);
    }
  });
});
