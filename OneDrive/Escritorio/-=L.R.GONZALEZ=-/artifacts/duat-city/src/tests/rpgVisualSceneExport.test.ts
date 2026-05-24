import { describe, expect, it } from "vitest";
import { exportRPGWorld } from "../rpg/worldExport";
import { createCity } from "../sim/city";
import { createPixelRealismRuntime } from "../pixelRealism/pixelRealismMetrics";
import { defaultPixelRealismConfig } from "../pixelRealism/renderPasses";

describe("RPG visual scene export v1.0", () => {
  it("includes visual_scene_profile and pixel_physics_profile", () => {
    const state = createCity();
    const runtime = createPixelRealismRuntime(state, defaultPixelRealismConfig());
    const world = exportRPGWorld({ ...state, pixelRealism: runtime.metrics });
    expect(world.visual_scene_profile).toBeDefined();
    expect(world.pixel_physics_profile).toBeDefined();
    expect(world.visual_scene_profile?.palette).toBe(runtime.metrics.palette);
    expect(world.pixel_physics_profile?.danger_materials).toContain("ruinMatter");
  });

  it("generates visual quest hooks from hazards", () => {
    const state = createCity();
    const runtime = createPixelRealismRuntime(state, defaultPixelRealismConfig());
    const world = exportRPGWorld({ ...state, pixelRealism: runtime.metrics });
    expect(world.quests.some(q => q.title === "Restore broken light source")).toBe(true);
    expect(world.quests.some(q => q.title === "Follow reflection anomaly")).toBe(true);
  });
});
