import { describe, expect, it } from "vitest";
import { exportRPGWorld } from "../rpg/worldExport";
import { createCity } from "../sim/city";

describe("RPG visual export v0.7", () => {
  it("includes visual profile, asset refs and physics field summary", () => {
    const world = exportRPGWorld(createCity());
    expect(world.schema).toBe("medioevo-rpg/world/v3");
    expect(world.visual_style_profile).toBeDefined();
    expect(world.reviewed_asset_refs?.some(ref => ref.includes("REVIEWED_ASSETS_MANIFEST"))).toBe(true);
    expect(world.tile_atlas_refs?.road).toBe("tile/road");
    expect(world.agent_icon_refs?.default).toBe("agent/default");
    expect(world.light_profile).toBeDefined();
    expect(world.physics_field_summary).toBeDefined();
  });

  it("graphics profile mirrors screenshot and asset references", () => {
    const world = exportRPGWorld(createCity());
    expect(world.graphics_profile.reviewed_asset_refs?.length).toBeGreaterThan(0);
    expect(world.graphics_profile.screenshot_paths?.some(path => path.includes("screenshots/v0_7"))).toBe(true);
  });
});
