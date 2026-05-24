import { describe, expect, it } from "vitest";
import { createCity } from "../sim/city";
import { exportRPGWorld } from "../rpg/worldExport";
import { createDefaultPlayableSceneState, applyVibeSceneToPlayableScene } from "../scene/sceneState";
import { parseVibePrompt } from "../vibecoding/vibeParser";

describe("RPG art direction export v1.2", () => {
  it("includes art direction profile with narrative lenses and symbolic objects", () => {
    const city = createCity();
    const vibe = parseVibePrompt("mas Caravaggio, mas vigilancia, archivo mitico").config;
    const playableScene = applyVibeSceneToPlayableScene(createDefaultPlayableSceneState(), vibe, city.width, city.height);
    const world = exportRPGWorld({ ...city, playableScene });
    expect(world.art_direction_profile?.light_canon).toBe("caravaggio_chiaroscuro");
    expect(world.art_direction_profile?.narrative_lenses).toContain("surveillance_dystopia_lens");
    expect(world.art_direction_profile?.symbolic_objects.length).toBe(13);
    expect(world.art_direction_profile?.public_boundary_note).toContain("no characters");
  });
});
