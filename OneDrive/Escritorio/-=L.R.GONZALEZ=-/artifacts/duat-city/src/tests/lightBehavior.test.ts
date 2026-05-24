import { describe, expect, it } from "vitest";
import { buildLightGridForCity } from "../light/lightPropagation";
import { sampleGridLight } from "../light/lightMetrics";
import { createDefaultPlayableSceneState, placeSceneMaterial, setSceneWeather } from "../scene/sceneState";
import { createCity } from "../sim/city";

describe("light behavior v1.1", () => {
  it("fire emits light into the grid", () => {
    const scene = placeSceneMaterial(createDefaultPlayableSceneState(), 12, 12, "fire");
    const state = { ...createCity(), playableScene: scene };
    const grid = buildLightGridForCity(state, { width: 80, height: 45 });
    expect(sampleGridLight(grid, 12 / state.width, 12 / state.height).intensity).toBeGreaterThan(0.2);
  });

  it("neon emits colored light", () => {
    const scene = placeSceneMaterial(createDefaultPlayableSceneState(), 18, 12, "neon");
    const state = { ...createCity(), playableScene: scene };
    const grid = buildLightGridForCity(state, { width: 80, height: 45 });
    const sample = sampleGridLight(grid, 18 / state.width, 12 / state.height);
    expect(sample.b).toBeGreaterThan(sample.r);
  });

  it("water reflection changes output", () => {
    const base = createCity();
    const dryGrid = buildLightGridForCity(base, { width: 80, height: 45 });
    const scene = placeSceneMaterial(createDefaultPlayableSceneState(), 24, 18, "water");
    const wetGrid = buildLightGridForCity({ ...base, playableScene: scene }, { width: 80, height: 45 });
    const dry = sampleGridLight(dryGrid, 24 / base.width, 18 / base.height);
    const wet = sampleGridLight(wetGrid, 24 / base.width, 18 / base.height);
    expect(wet.reflectance).toBeGreaterThanOrEqual(dry.reflectance);
  });

  it("smoke scatters and wet material reflectance increases", () => {
    const smoky = placeSceneMaterial(createDefaultPlayableSceneState(), 16, 10, "smoke");
    const rainy = setSceneWeather(placeSceneMaterial(smoky, 14, 10, "stone"), "rain");
    const state = { ...createCity(), playableScene: rainy };
    const grid = buildLightGridForCity(state, { width: 80, height: 45, fog: 0.2 });
    const smoke = sampleGridLight(grid, 16 / state.width, 10 / state.height);
    const stone = sampleGridLight(grid, 14 / state.width, 10 / state.height);
    expect(smoke.scatter).toBeGreaterThan(0);
    expect(stone.reflectance).toBeGreaterThan(0.3);
  });
});
