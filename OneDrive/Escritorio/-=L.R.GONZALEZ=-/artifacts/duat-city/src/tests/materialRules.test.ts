import { describe, expect, it } from "vitest";
import { evaluateMaterialRules, getMaterialDefinition } from "../physicsField/materialRules";

describe("material pixel physics v1.0", () => {
  it("fire emits light and heat", () => {
    const fire = evaluateMaterialRules("fire", 0, 3);
    expect(fire.emitsLight).toBe(true);
    expect(fire.heatDelta).toBeGreaterThan(0);
  });

  it("water reflects and moves down/laterally", () => {
    const water = evaluateMaterialRules("water", 1, 0);
    expect(water.reflectance).toBeGreaterThan(0.5);
    expect(water.velocity.y).toBeGreaterThan(0);
  });

  it("smoke rises and scatters light", () => {
    const smoke = evaluateMaterialRules("smoke", 0, 0);
    expect(smoke.velocity.y).toBeLessThan(0);
    expect(smoke.scatter).toBeGreaterThan(0.2);
  });

  it("wet stone is more reflective than dry stone", () => {
    const dry = evaluateMaterialRules("stone", 0, 0);
    const wet = evaluateMaterialRules("stone", 1, 0);
    expect(wet.reflectance).toBeGreaterThan(dry.reflectance);
  });

  it("all required materials have definitions", () => {
    for (const material of ["empty", "air", "stone", "brick", "wood", "metal", "glass", "water", "soil", "grass", "fire", "smoke", "dust", "neon", "cloth", "skin", "obsidian", "gold", "crystal", "ruinMatter"] as const) {
      expect(getMaterialDefinition(material).baseColor).toMatch(/^#/);
    }
  });
});
