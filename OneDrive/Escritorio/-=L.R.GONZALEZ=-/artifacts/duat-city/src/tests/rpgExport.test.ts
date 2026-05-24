import { describe, it, expect } from "vitest";
import { exportRPGWorld } from "../rpg/worldExport";
import { generateQuests } from "../rpg/questGenerator";
import { generateFactions } from "../rpg/factionGenerator";
import { createCity } from "../sim/city";
import { placeTile } from "../sim/city";

describe("exportRPGWorld", () => {
  it("has correct schema", () => {
    const state = createCity();
    const world = exportRPGWorld(state);
    expect(world.schema).toBe("medioevo-rpg/world/v3");
  });
  it("NPCs match agents", () => {
    const state = createCity();
    const world = exportRPGWorld(state);
    expect(world.npcs.length).toBe(state.agents.length);
  });
  it("locations match buildings", () => {
    const state = createCity();
    const world = exportRPGWorld(state);
    expect(world.locations.length).toBe(state.buildings.length);
  });
  it("has factions", () => {
    const state = createCity();
    const world = exportRPGWorld(state);
    expect(world.factions.length).toBeGreaterThan(0);
  });
  it("ruin generates risk zone", () => {
    let state = createCity();
    state = placeTile(state, 30, 20, "ruin");
    const world = exportRPGWorld(state);
    expect(world.risk_zones.length).toBeGreaterThan(0);
  });
});

describe("generateQuests", () => {
  it("returns array", () => {
    const state = createCity();
    const quests = generateQuests(state);
    expect(Array.isArray(quests)).toBe(true);
  });
  it("generates food quest when food is low", () => {
    const state = createCity();
    const lowFood = { ...state, resources: { ...state.resources, food: 10 } };
    const quests = generateQuests(lowFood);
    const foodQuest = quests.find(q => q.type === "resource");
    expect(foodQuest).toBeDefined();
  });
});

describe("generateFactions", () => {
  it("returns 6 base factions", () => {
    const state = createCity();
    const factions = generateFactions(state);
    expect(factions.length).toBe(6);
  });
  it("all have alignment", () => {
    const state = createCity();
    const factions = generateFactions(state);
    for (const f of factions) {
      expect(["order", "conflict", "neutral", "void"]).toContain(f.alignment);
    }
  });
});
