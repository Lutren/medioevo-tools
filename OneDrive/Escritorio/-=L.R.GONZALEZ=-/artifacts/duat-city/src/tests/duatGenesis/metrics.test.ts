import { describe, it, expect } from "vitest";
import { DuatEngine } from "../../duatGenesis/engine";
import { MetricsTracker, CHI_STAR } from "../../duatGenesis/metrics";
import type { DuatEngineParams } from "../../duatGenesis/types";

const DEFAULT_PARAMS: DuatEngineParams = {
  chi: CHI_STAR,
  sigma: 0.135,
  dt: 0.19,
  noise: 0.011,
  observerStrength: 0.65,
  speed: 1,
  running: true,
  ruleMode: "duat",
  ablationMode: "full",
};

describe("MetricsTracker", () => {
  it("computes metrics after stepping", () => {
    const engine = new DuatEngine(42, 48, 30);
    const tracker = new MetricsTracker();
    engine.seedDuat(24, 15);
    let metrics = tracker.update(
      engine.psi,
      engine.previous,
      engine.gravity,
      engine.light,
      engine.width,
      engine.height,
      DEFAULT_PARAMS,
    );
    for (let i = 0; i < 52; i += 1) {
      engine.step(DEFAULT_PARAMS);
      metrics = tracker.update(
        engine.psi,
        engine.previous,
        engine.gravity,
        engine.light,
        engine.width,
        engine.height,
        DEFAULT_PARAMS,
        engine.lastClipRatio,
      );
    }
    expect(metrics.mean).toBeGreaterThanOrEqual(0);
    expect(metrics.mean).toBeLessThanOrEqual(1);
    expect(metrics.liveness).toBeGreaterThanOrEqual(0);
    expect(metrics.liveness).toBeLessThanOrEqual(1);
    expect(metrics.residue).toBeGreaterThanOrEqual(0);
    expect(metrics.residue).toBeLessThanOrEqual(1);
    expect(metrics.phiEff).toBeGreaterThanOrEqual(0);
    expect(metrics.phiEff).toBeLessThanOrEqual(1);
    expect(metrics.clipArtifactRatio).toBeGreaterThanOrEqual(0);
    expect(metrics.clipArtifactRatio).toBeLessThanOrEqual(1);
    expect(metrics.dimObs).toBeGreaterThanOrEqual(1);
    expect(metrics.dimObs).toBeLessThanOrEqual(5);
  });

  it("classifies cosmology states correctly", () => {
    const tracker = new MetricsTracker();
    const engine = new DuatEngine(42, 48, 30);
    engine.seedDuat(24, 15);
    let metrics = tracker.update(
      engine.psi,
      engine.previous,
      engine.gravity,
      engine.light,
      engine.width,
      engine.height,
      DEFAULT_PARAMS,
    );
    for (let i = 0; i < 60; i += 1) {
      engine.step(DEFAULT_PARAMS);
      metrics = tracker.update(
        engine.psi,
        engine.previous,
        engine.gravity,
        engine.light,
        engine.width,
        engine.height,
        DEFAULT_PARAMS,
        engine.lastClipRatio,
      );
    }
    expect(["NU", "ATUM", "DUAT", "MAAT", "OSIRIS", "COLAPSO"]).toContain(metrics.cosmologyState);
  });

  it("produces consistent Phi_eff = 1 - residue^1.097", () => {
    const tracker = new MetricsTracker();
    const engine = new DuatEngine(42, 48, 30);
    engine.seedDuat(24, 15);
    for (let i = 0; i < 30; i += 1) {
      engine.step(DEFAULT_PARAMS);
      const metrics = tracker.update(
        engine.psi,
        engine.previous,
        engine.gravity,
        engine.light,
        engine.width,
        engine.height,
        DEFAULT_PARAMS,
        engine.lastClipRatio,
      );
      const expectedPhi = Math.min(1, Math.max(0, 1 - Math.pow(metrics.residue, 1.097)));
      expect(Math.abs(metrics.phiEff - expectedPhi)).toBeLessThanOrEqual(1e-10);
    }
  });
});
