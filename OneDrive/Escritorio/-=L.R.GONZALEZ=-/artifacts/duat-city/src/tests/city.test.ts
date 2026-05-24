import { describe, it, expect } from "vitest";
import { createCity, placeTile, eraseTile, computeGlobalR } from "../sim/city";
import { AGENT_ROLES } from "../sim/agents";

describe("createCity", () => {
  it("creates correct grid size", () => {
    const city = createCity();
    expect(city.tiles.length).toBe(48 * 32);
    expect(city.width).toBe(48);
    expect(city.height).toBe(32);
  });
  it("starts with agents", () => {
    const city = createCity();
    expect(city.agents.length).toBe(AGENT_ROLES.length);
  });
  it("has initial buildings", () => {
    const city = createCity();
    expect(city.buildings.length).toBeGreaterThan(0);
  });
  it("has road tiles in center", () => {
    const city = createCity();
    const roads = city.tiles.filter(t => t.type === "road");
    expect(roads.length).toBeGreaterThan(0);
  });
  it("initializes resources", () => {
    const city = createCity();
    expect(city.resources.food).toBeGreaterThan(0);
    expect(city.resources.materials).toBeGreaterThan(0);
  });
});

describe("placeTile", () => {
  it("places a building on empty tile", () => {
    let city = createCity();
    city = placeTile(city, 10, 10, "workshop");
    const tile = city.tiles[10 * city.width + 10];
    expect(tile.type).toBe("workshop");
    expect(tile.buildingId).toBeDefined();
    expect(city.buildings.find(b => b.type === "workshop" && b.x === 10)).toBeDefined();
  });
  it("replaces existing building", () => {
    let city = createCity();
    city = placeTile(city, 5, 5, "residential");
    const beforeCount = city.buildings.length;
    city = placeTile(city, 5, 5, "clinic");
    const afterCount = city.buildings.length;
    expect(afterCount).toBe(beforeCount); // replaced, not added
    const tile = city.tiles[5 * city.width + 5];
    expect(tile.type).toBe("clinic");
  });
  it("out-of-bounds returns unchanged state", () => {
    const city = createCity();
    const after = placeTile(city, -1, -1, "workshop");
    expect(after.buildings.length).toBe(city.buildings.length);
  });
});

describe("eraseTile", () => {
  it("removes building from tile", () => {
    let city = createCity();
    city = placeTile(city, 20, 15, "academy");
    const before = city.buildings.length;
    city = eraseTile(city, 20, 15);
    expect(city.buildings.length).toBe(before - 1);
    expect(city.tiles[15 * city.width + 20].type).toBe("empty");
  });
});

describe("computeGlobalR", () => {
  it("returns value in [0,1]", () => {
    const city = createCity();
    const r = computeGlobalR(city);
    expect(r).toBeGreaterThanOrEqual(0);
    expect(r).toBeLessThanOrEqual(1);
  });
});
