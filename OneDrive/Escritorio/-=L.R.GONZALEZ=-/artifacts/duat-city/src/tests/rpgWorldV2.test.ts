import { describe, expect, it } from "vitest";
import { exportRPGWorld } from "../rpg/worldExport";
import { placeTile, createCity } from "../sim/city";

describe("RPG world v2", () => {
  it("exports map tiles, field summary and asset refs", () => {
    const world = exportRPGWorld(createCity());
    expect(world.schema).toBe("medioevo-rpg/world/v3");
    expect(world.map_tiles?.length).toBeGreaterThan(0);
    expect(world.visual_asset_manifest_refs?.length).toBeGreaterThan(0);
    expect(world.physics_field_summary).toBeDefined();
  });

  it("hazards create quests", () => {
    const state = placeTile(createCity(), 10, 10, "water");
    const world = exportRPGWorld(state);
    expect(world.quests.some(q => q.title.toLowerCase().includes("flood"))).toBe(true);
  });

  it("does not produce NaN in tile export", () => {
    const world = exportRPGWorld(createCity());
    const encoded = JSON.stringify(world.map_tiles);
    expect(encoded).not.toMatch(/NaN/);
  });
});
