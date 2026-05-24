import { describe, it, expect } from "vitest";
import { createAgent, decayNeeds, updateAgentMetrics, moveAgentToward, restoreNeedAtBuilding } from "../sim/agents";

describe("createAgent", () => {
  it("creates agent with correct role", () => {
    const a = createAgent("Observer", 10, 10);
    expect(a.role).toBe("Observer");
    expect(a.x).toBe(10);
    expect(a.y).toBe(10);
  });
  it("agent has valid initial needs", () => {
    const a = createAgent("Builder", 5, 5);
    expect(a.needs.energy).toBeGreaterThanOrEqual(0);
    expect(a.needs.energy).toBeLessThanOrEqual(1);
    expect(a.needs.hunger).toBeGreaterThanOrEqual(0);
  });
  it("initial gate is APPROVE", () => {
    const a = createAgent("Scout", 0, 0);
    expect(a.gate).toBe("APPROVE");
  });
});

describe("decayNeeds", () => {
  it("reduces all needs over time", () => {
    const a = createAgent("Medic", 5, 5);
    const b = decayNeeds(a, 100);
    expect(b.needs.energy).toBeLessThan(a.needs.energy);
    expect(b.needs.hunger).toBeLessThan(a.needs.hunger);
  });
  it("needs stay in [0,1]", () => {
    let a = createAgent("Engineer", 0, 0);
    a = { ...a, needs: { energy: 0, hunger: 0, social: 0, purpose: 0, safety: 0, curiosity: 0 } };
    const b = decayNeeds(a, 1000);
    for (const val of Object.values(b.needs)) {
      expect(val).toBeGreaterThanOrEqual(0);
      expect(val).toBeLessThanOrEqual(1);
    }
  });
});

describe("updateAgentMetrics", () => {
  it("computes R and Phi_eff in [0,1]", () => {
    const a = createAgent("Trader", 5, 5);
    const b = updateAgentMetrics(a);
    expect(b.R).toBeGreaterThanOrEqual(0);
    expect(b.R).toBeLessThanOrEqual(1);
    expect(b.Phi_eff).toBeGreaterThanOrEqual(0);
    expect(b.Phi_eff).toBeLessThanOrEqual(1);
  });
  it("high needs → lower R", () => {
    const healthy = createAgent("Teacher", 5, 5);
    const fullNeeds = { ...healthy, needs: { energy: 1, hunger: 1, social: 1, purpose: 1, safety: 1, curiosity: 1 } };
    const lowNeeds = { ...healthy, needs: { energy: 0, hunger: 0, social: 0, purpose: 0, safety: 0, curiosity: 0 } };
    const rHealthy = updateAgentMetrics(fullNeeds).R;
    const rLow = updateAgentMetrics(lowNeeds).R;
    expect(rHealthy).toBeLessThan(rLow);
  });
});

describe("moveAgentToward", () => {
  it("moves agent closer to target", () => {
    const a = createAgent("Courier", 0, 0);
    const moved = moveAgentToward(a, 10, 0, 2, 50);
    expect(moved.x).toBeGreaterThan(0);
  });
  it("snaps to target when very close", () => {
    const a = createAgent("Scout", 5, 5);
    const moved = moveAgentToward(a, 5.05, 5, 2, 100);
    expect(moved.x).toBeCloseTo(5.05, 0);
  });
});

describe("restoreNeedAtBuilding", () => {
  it("restores energy at residential", () => {
    const a = createAgent("Builder", 0, 0);
    const low = { ...a, needs: { ...a.needs, energy: 0.2 } };
    const restored = restoreNeedAtBuilding(low, "residential");
    expect(restored.needs.energy).toBeGreaterThan(low.needs.energy);
  });
  it("restores hunger at garden", () => {
    const a = createAgent("Artisan", 0, 0);
    const low = { ...a, needs: { ...a.needs, hunger: 0.1 } };
    const restored = restoreNeedAtBuilding(low, "garden");
    expect(restored.needs.hunger).toBeGreaterThan(low.needs.hunger);
  });
});
