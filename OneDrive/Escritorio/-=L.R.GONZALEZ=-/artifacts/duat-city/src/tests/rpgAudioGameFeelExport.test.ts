import { describe, expect, it } from "vitest";
import { createCity } from "../sim/city";
import { createDefaultPlayableSceneState, placeSceneLight, placeSceneMaterial } from "../scene/sceneState";
import { exportRPGWorld } from "../rpg/worldExport";

describe("RPG audio/game-feel export v1.3.1", () => {
  it("includes procedural audio game-feel profile with materials and lights", () => {
    let scene = createDefaultPlayableSceneState();
    scene = placeSceneMaterial(scene, 10, 10, "fire");
    scene = placeSceneMaterial(scene, 11, 10, "neon");
    scene = placeSceneLight(scene, 11, 9, "neon");
    const world = exportRPGWorld({ ...createCity(), playableScene: scene });
    expect(world.audio_gamefeel_profile?.schema).toBe("duat/rpg-audio-gamefeel/v1.3.1");
    expect(world.audio_gamefeel_profile?.procedural_only).toBe(true);
    expect(world.audio_gamefeel_profile?.requires_user_gesture).toBe(true);
    expect(world.audio_gamefeel_profile?.publication_allowed).toBe(false);
    expect(world.audio_gamefeel_profile?.cue_count).toBeGreaterThan(0);
    expect(world.audio_gamefeel_profile?.cue_tags).toContain("fire");
    expect(world.visual_asset_manifest_refs).toContain("/asset-manifest/audio_gamefeel_manifest_v1_3_1.json");
  });
});
