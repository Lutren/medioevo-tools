import { describe, it, expect } from "vitest";
import { DuatEngine } from "../../duatGenesis/engine";
import type { DuatEngineParams } from "../../duatGenesis/types";

const DEFAULT_PARAMS: DuatEngineParams = {
  chi: 0.567,
  sigma: 0.135,
  dt: 0.19,
  noise: 0.011,
  observerStrength: 0.65,
  speed: 1,
  running: true,
  ruleMode: "duat",
  ablationMode: "full",
};

describe("DuatEngine", () => {
  it("is deterministic for same seed and params", () => {
    const a = new DuatEngine(1919, 48, 30);
    const b = new DuatEngine(1919, 48, 30);
    a.seedDuat(24, 15);
    b.seedDuat(24, 15);
    for (let i = 0; i < 20; i += 1) {
      a.step(DEFAULT_PARAMS);
      b.step(DEFAULT_PARAMS);
    }
    let maxDelta = 0;
    for (let i = 0; i < a.psi.length; i += 1) {
      maxDelta = Math.max(maxDelta, Math.abs(a.psi[i] - b.psi[i]));
    }
    expect(maxDelta).toBeLessThanOrEqual(1e-7);
  });

  it("keeps all values within [0, 1]", () => {
    const engine = new DuatEngine(2026, 48, 30);
    engine.seedAtum(16, 15);
    for (let i = 0; i < 28; i += 1) {
      engine.step(DEFAULT_PARAMS);
    }
    for (const field of [engine.psi, engine.gravity, engine.light]) {
      for (const value of field) {
        expect(value).toBeGreaterThanOrEqual(0);
        expect(value).toBeLessThanOrEqual(1);
        expect(Number.isFinite(value)).toBe(true);
      }
    }
  });

  it("responds to observer strength", () => {
    const withObserver = new DuatEngine(42, 48, 30);
    const withoutObserver = new DuatEngine(42, 48, 30);
    withObserver.seedDuat(24, 15);
    withoutObserver.seedDuat(24, 15);
    const observer = { x: 24, y: 15, strength: 0.55, profile: { id: "a" as const, name: "Test", resolution: 1, saturation: 0.38, noise: 0.012, temporalWindow: 16, modality: "visual" as const } };
    for (let i = 0; i < 32; i += 1) {
      withObserver.step(DEFAULT_PARAMS, observer);
      withoutObserver.step(DEFAULT_PARAMS);
    }
    let delta = 0;
    for (let i = 0; i < withObserver.psi.length; i += 1) {
      delta += Math.abs(withObserver.psi[i] - withoutObserver.psi[i]);
    }
    expect(delta).toBeGreaterThan(0);
  });

  it("preserves clipArtifactRatio low after clamp fix", () => {
    const engine = new DuatEngine(5150, 48, 30);
    engine.seedDuat(24, 15);
    for (let i = 0; i < 36; i += 1) {
      engine.step(DEFAULT_PARAMS);
    }
    expect(engine.lastClipRatio).toBeLessThan(0.18);
  });

  it("renders a non-blank frame", () => {
    const engine = new DuatEngine(1234, 48, 30);
    engine.seedOsiris(24, 15);
    for (let i = 0; i < 10; i += 1) {
      engine.step(DEFAULT_PARAMS);
    }
    const canvas = document.createElement("canvas");
    canvas.width = 48 * 4;
    canvas.height = 30 * 4;
    const ctx = canvas.getContext("2d")!;
    const img = ctx.createImageData(canvas.width, canvas.height);
    for (let y = 0; y < engine.height; y += 1) {
      for (let x = 0; x < engine.width; x += 1) {
        const id = y * engine.width + x;
        const v = engine.psi[id];
        const px = x * 4;
        const py = y * 4;
        for (let dy = 0; dy < 4; dy += 1) {
          for (let dx = 0; dx < 4; dx += 1) {
            const p = ((py + dy) * (48 * 4) + px + dx) * 4;
            img.data[p] = Math.round(v * 200);
            img.data[p + 1] = Math.round(v * 150);
            img.data[p + 2] = Math.round(v * 100);
            img.data[p + 3] = 255;
          }
        }
      }
    }
    ctx.putImageData(img, 0, 0);
    const data = ctx.getImageData(0, 0, canvas.width, canvas.height).data;
    let nonBlank = 0;
    for (let i = 0; i < data.length; i += 4) {
      if (data[i] + data[i + 1] + data[i + 2] > 0) nonBlank += 1;
    }
    expect(nonBlank).toBeGreaterThan(0);
  });
});
