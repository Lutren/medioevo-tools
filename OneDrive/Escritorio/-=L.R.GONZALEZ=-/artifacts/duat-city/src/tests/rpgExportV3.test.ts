import { describe, expect, it } from "vitest";
import { createCity } from "../sim/city";
import { exportRPGWorld } from "../rpg/worldExport";
import { compileVibeAction } from "../vibecoding/vibeActionCompiler";
import { createGameState } from "../game/gameState";
import { tickGame } from "../game/gameLoop";

describe("RPG export v3", () => {
  it("includes style tokens, asset refs, procedural seeds and material/light summaries", () => {
    const world = exportRPGWorld(createCity());
    expect(world.schema).toBe("medioevo-rpg/world/v3");
    expect(world.style_tokens).toBeDefined();
    expect(world.asset_references?.some(ref => ref.includes("v1_2"))).toBe(true);
    expect(world.procedural_generation_seeds?.tiles).toBeGreaterThan(0);
    expect(world.material_field_summary).toBeDefined();
    expect(world.light_field_summary).toBeDefined();
  });

  it("exports vibe history, hazards and interaction points", () => {
    const game = tickGame(createGameState(), compileVibeAction("haz un mercado subterraneo con luces rosas y humo"));
    const world = exportRPGWorld({ ...game.city, playableScene: game.scene });
    expect(world.visual_scene_profile?.placed_materials?.length).toBeGreaterThan(0);
    expect(world.pixel_physics_profile?.danger_materials).toContain("fire");
    expect(world.interaction_points?.length).toBeGreaterThan(0);
  });
});
