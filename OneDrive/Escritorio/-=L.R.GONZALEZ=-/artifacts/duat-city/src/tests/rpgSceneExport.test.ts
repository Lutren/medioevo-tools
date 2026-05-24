import { describe, expect, it } from "vitest";
import { exportRPGWorld } from "../rpg/worldExport";
import { createDefaultPlayableSceneState, placeSceneLight, placeSceneMaterial } from "../scene/sceneState";
import { createCity } from "../sim/city";
import { compileVibeScene } from "../vibecoding/vibeSceneCompiler";
import { applyVibeSceneToPlayableScene } from "../scene/sceneState";

describe("RPG scene export v1.1", () => {
  it("includes placed materials, lights and vibe config", () => {
    const vibe = compileVibeScene("neon_rain_street", "preset").config;
    let scene = applyVibeSceneToPlayableScene(createDefaultPlayableSceneState(), vibe, 48, 32);
    scene = placeSceneMaterial(scene, 6, 7, "fire");
    scene = placeSceneLight(scene, 8, 7, "neon");
    const world = exportRPGWorld({ ...createCity(), playableScene: scene });
    expect(world.visual_scene_profile?.placed_materials?.some(cell => cell.material === "fire")).toBe(true);
    expect(world.visual_scene_profile?.placed_lights?.some(light => light.kind === "neon")).toBe(true);
    expect(world.visual_scene_profile?.vibe_config).toBeDefined();
    expect(world.playable_scene_profile).toBeDefined();
  });

  it("exports hazards and quest hooks from scene materials", () => {
    const scene = placeSceneMaterial(placeSceneMaterial(createDefaultPlayableSceneState(), 9, 10, "water"), 12, 10, "fire");
    const world = exportRPGWorld({ ...createCity(), playableScene: scene });
    const profile = world.playable_scene_profile as { hazards: string[]; quest_hooks: string[] };
    expect(profile.hazards.some(item => item.startsWith("fire:"))).toBe(true);
    expect(profile.quest_hooks.some(item => item.startsWith("drain flooded passage"))).toBe(true);
    expect(world.pixel_physics_profile?.water_zones.some(zone => zone.includes("9,10"))).toBe(true);
  });
});
