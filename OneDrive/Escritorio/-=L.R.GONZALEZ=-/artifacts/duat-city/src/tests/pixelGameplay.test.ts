import { describe, expect, it } from "vitest";
import { createCity } from "../sim/city";
import { applyMaterialGameplayToAgents } from "../game/gameSystems";
import { createDefaultPlayableSceneState, placeSceneMaterial, stepPlayableScene } from "../scene/sceneState";

describe("pixel physics gameplay v1.2", () => {
  it("water affects movement state and fire increases risk", () => {
    const city = createCity();
    const agent = city.agents[0];
    let scene = createDefaultPlayableSceneState();
    scene = placeSceneMaterial(scene, Math.round(agent.x), Math.round(agent.y), "water");
    const wetAgent = applyMaterialGameplayToAgents([agent], scene)[0];
    expect(wetAgent.Phi_eff).toBeLessThanOrEqual(agent.Phi_eff);
    scene = placeSceneMaterial(createDefaultPlayableSceneState(), Math.round(agent.x), Math.round(agent.y), "fire");
    const fireAgent = applyMaterialGameplayToAgents([agent], scene)[0];
    expect(fireAgent.R).toBeGreaterThan(agent.R);
  });

  it("smoke rises and neon emits", () => {
    let scene = createDefaultPlayableSceneState();
    scene = placeSceneMaterial(scene, 10, 10, "smoke");
    scene = placeSceneMaterial(scene, 12, 10, "neon");
    const stepped = stepPlayableScene(scene, 48, 32);
    expect(stepped.materials.find(cell => cell.material === "smoke")?.y).toBeLessThanOrEqual(10);
    expect(stepped.metrics.emissiveCells).toBeGreaterThan(0);
  });
});
