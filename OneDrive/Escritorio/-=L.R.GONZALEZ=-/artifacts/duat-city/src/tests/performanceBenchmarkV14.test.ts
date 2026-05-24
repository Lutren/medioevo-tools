import { readFileSync } from "node:fs";
import { describe, expect, it } from "vitest";

const reportUrl = new URL("../../docs/PERFORMANCE_BENCHMARK_v1_4.json", import.meta.url);

describe("performance benchmark v1.4", () => {
  it("has finite fallback frame-sampler schema and explicit headed limitation", () => {
    const doc = JSON.parse(readFileSync(reportUrl, "utf8"));
    expect(doc.schema).toBe("duat/performance-benchmark/v1.4");
    expect(doc.fingerprint).toBe("DUAT-v1.4-OSIT-OBSERVACIONISMO-FULL");
    expect(doc.headedFpsVerified).toBe(false);
    expect(doc.scenarios).toHaveLength(3);
    for (const scenario of doc.scenarios) {
      expect(Number.isFinite(scenario.avgFps)).toBe(true);
      expect(Number.isFinite(scenario.p95FrameMs)).toBe(true);
      expect(Number.isFinite(scenario.appAvgFps)).toBe(true);
      expect(Number.isFinite(scenario.appP95FrameMs)).toBe(true);
      expect(Number.isFinite(scenario.droppedFrames)).toBe(true);
      expect(scenario.runtimeMode).toBe("static-render-benchmark");
    }
    const high = doc.scenarios.find((scenario: { id: string }) => scenario.id === "high_iso3d_operational");
    const beautiful = doc.scenarios.find((scenario: { id: string }) => scenario.id === "beautiful_vermeer_city");
    expect(high.appAvgFps).toBeGreaterThanOrEqual(30);
    expect(beautiful.appAvgFps).toBeGreaterThanOrEqual(30);
  });
});
