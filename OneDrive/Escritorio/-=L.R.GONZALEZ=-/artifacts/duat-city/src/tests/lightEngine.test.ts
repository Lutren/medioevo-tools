import { describe, expect, it } from "vitest";
import { ambientLightForTick, computeLightMap, sampleLight } from "../graphics/lightEngine";
import { buildLightGridForCity } from "../light/lightPropagation";
import { computeLightMetrics, sampleGridLight } from "../light/lightMetrics";
import { setLightCell } from "../light/lightGrid";
import { createCity } from "../sim/city";

describe("lightEngine", () => {
  it("clamps ambient and sampled light to 0..1", () => {
    for (const tick of [0, 12, 48, 96, 1000]) {
      const ambient = ambientLightForTick(tick);
      expect(ambient).toBeGreaterThanOrEqual(0);
      expect(ambient).toBeLessThanOrEqual(1);
    }
    const map = computeLightMap(createCity(), 16, 12);
    const value = sampleLight(map, 0.5, 0.5);
    expect(value).toBeGreaterThanOrEqual(0);
    expect(value).toBeLessThanOrEqual(1);
    expect(Number.isNaN(value)).toBe(false);
  });

  it("point light decays away from source", () => {
    const state = createCity();
    const market = state.buildings.find(b => b.type === "market")!;
    const map = computeLightMap(state, 48, 32);
    const near = sampleLight(map, market.x / state.width, market.y / state.height);
    const far = sampleLight(map, 0, 0);
    expect(near).toBeGreaterThanOrEqual(far);
  });

  it("colored light blends and remains finite in the v1.0 grid", () => {
    const state = createCity();
    const grid = buildLightGridForCity(state, { width: 64, height: 36, bouncePasses: 1 });
    const metrics = computeLightMetrics(grid);
    expect(metrics.activeLightCells).toBeGreaterThan(0);
    expect(Number.isNaN(metrics.R_light)).toBe(false);
    expect(Number.isNaN(metrics.Phi_light)).toBe(false);
    const sample = sampleGridLight(grid, 0.5, 0.5);
    expect(sample.r + sample.g + sample.b).toBeGreaterThan(0);
  });

  it("opacity blocks light and reflections stay finite", () => {
    const state = createCity();
    const open = buildLightGridForCity(state, { width: 64, height: 36, bouncePasses: 1 });
    const blocked = buildLightGridForCity(state, { width: 64, height: 36, bouncePasses: 1 });
    setLightCell(blocked, 32, 18, { opacity: 1 });
    const openSample = sampleGridLight(open, 0.5, 0.5);
    const blockedSample = sampleGridLight(blocked, 0.5, 0.5);
    expect(blockedSample.intensity).toBeLessThanOrEqual(openSample.intensity + 0.5);
    expect(computeLightMetrics(blocked).finite).toBe(true);
  });
});
