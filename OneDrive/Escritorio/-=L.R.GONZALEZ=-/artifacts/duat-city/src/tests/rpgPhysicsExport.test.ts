import { describe, expect, it } from "vitest";
import { createCity, placeTile } from "../sim/city";
import { exportRPGWorld } from "../rpg/worldExport";
import { generateQuests } from "../rpg/questGenerator";

describe("RPG physics and graphics export", () => {
  it("export includes physics_profile and graphics_profile", () => {
    const world = exportRPGWorld(createCity());
    expect(world.physics_profile.walkable_routes.length).toBeGreaterThan(0);
    expect(Object.keys(world.graphics_profile.fibmob_polarity_map).length).toBeGreaterThan(0);
  });

  it("high collision creates route quest hook", () => {
    const state = { ...createCity(), physicsMetrics: { bodyCount: 2, pairChecks: 1, resolvedCollisions: 2, unresolvedCollisions: 0, outOfBounds: 0, nanDetected: 0, frameCostEstimate: 1, R_physics: 0.1, Phi_physics: 1 } };
    const world = exportRPGWorld(state);
    const quests = generateQuests(state, world.physics_profile);
    expect(quests.some(q => q.title.includes("Blocked Route"))).toBe(true);
  });

  it("ruin plus FibMob void creates anomaly hook and no NaN", () => {
    const base = placeTile(createCity(), 1, 7, "ruin");
    const withRuin = {
      ...base,
      tiles: base.tiles.map(t => t.x === 1 && t.y === 7 ? { ...t, fibmob: { ...t.fibmob, polarity: "void" as const } } : t),
    };
    const world = exportRPGWorld(withRuin);
    expect(world.quests.some(q => q.title.includes("Ruin Anomaly") || q.title.includes("Investigate"))).toBe(true);
    expect(Number.isNaN(world.tick)).toBe(false);
  });
});
