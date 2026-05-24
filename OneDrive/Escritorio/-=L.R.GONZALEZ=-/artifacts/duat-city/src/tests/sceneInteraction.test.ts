import { describe, expect, it } from "vitest";
import {
  createDefaultPlayableSceneState,
  deserializePlayableScene,
  eraseSceneAt,
  placeSceneLight,
  placeSceneMaterial,
  serializePlayableScene,
  stepPlayableScene,
} from "../scene/sceneState";

describe("playable scene interaction v1.1", () => {
  it("places and erases material cells", () => {
    const scene = placeSceneMaterial(createDefaultPlayableSceneState(), 10, 12, "water");
    expect(scene.materials).toHaveLength(1);
    expect(scene.metrics.activeMaterialCells).toBe(1);
    const erased = eraseSceneAt(scene, 10, 12);
    expect(erased.materials).toHaveLength(0);
  });

  it("places light sources", () => {
    const scene = placeSceneLight(createDefaultPlayableSceneState(), 8, 9, "neon");
    expect(scene.lights[0].kind).toBe("neon");
    expect(scene.metrics.activeLightSources).toBe(1);
  });

  it("saves and loads scene JSON", () => {
    const scene = placeSceneMaterial(placeSceneLight(createDefaultPlayableSceneState(), 4, 5, "torch"), 4, 6, "fire");
    const loaded = deserializePlayableScene(serializePlayableScene(scene));
    expect(loaded?.lights[0].kind).toBe("torch");
    expect(loaded?.materials[0].material).toBe("fire");
  });

  it("steps without NaN", () => {
    const scene = placeSceneMaterial(createDefaultPlayableSceneState(), 5, 5, "water");
    const next = stepPlayableScene(scene, 48, 32);
    const finite = [
      next.tick,
      next.metrics.activeMaterialCells,
      next.metrics.activeLightSources,
      next.metrics.particles,
    ].every(Number.isFinite);
    expect(finite).toBe(true);
  });
});
