import { describe, it, expect } from "vitest";
import { runDuatSweep, summarizeSweep, FAST_SWEEP_CONFIG } from "../../duatGenesis/sweep";

describe("Sweep", () => {
  it("runs a fast sweep quickly", () => {
    const rows = runDuatSweep({}, FAST_SWEEP_CONFIG);
    expect(rows.length).toBeGreaterThan(0);
    for (const row of rows) {
      expect(row.mean).toBeGreaterThanOrEqual(0);
      expect(row.mean).toBeLessThanOrEqual(1);
      expect(row.liveness).toBeGreaterThanOrEqual(0);
      expect(row.liveness).toBeLessThanOrEqual(1);
      expect(row.clipArtifactRatio).toBeGreaterThanOrEqual(0);
      expect(row.clipArtifactRatio).toBeLessThanOrEqual(1);
    }
  });

  it("summarizes sweep correctly", () => {
    const rows = runDuatSweep({}, FAST_SWEEP_CONFIG);
    const summary = summarizeSweep(rows);
    expect(summary.rows).toBe(rows.length);
    expect(summary.meanLiveness).toBeGreaterThanOrEqual(0);
    expect(summary.meanResidue).toBeGreaterThanOrEqual(0);
    expect(summary.maxClipArtifactRatio).toBeGreaterThanOrEqual(0);
    expect(summary.fertileRows).toBeGreaterThanOrEqual(0);
    expect(Object.keys(summary.phaseCounts).length).toBeGreaterThan(0);
  });
});
