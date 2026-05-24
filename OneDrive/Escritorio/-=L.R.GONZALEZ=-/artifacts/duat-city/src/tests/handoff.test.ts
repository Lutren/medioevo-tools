import { describe, it, expect } from "vitest";
import { generateHandoff } from "../core/handoff";
import { createCity } from "../sim/city";
import { AGENT_ROLES } from "../sim/agents";

describe("generateHandoff", () => {
  const state = createCity();
  const handoff = generateHandoff(state);

  it("has correct schema", () => {
    expect(handoff.schema).toBe("duat-agent-city/handoff/v1");
  });
  it("has tick", () => {
    expect(typeof handoff.tick).toBe("number");
  });
  it("R is in [0,1]", () => {
    expect(handoff.R).toBeGreaterThanOrEqual(0);
    expect(handoff.R).toBeLessThanOrEqual(1);
  });
  it("Phi_eff is in [0,1]", () => {
    expect(handoff.Phi_eff).toBeGreaterThanOrEqual(0);
    expect(handoff.Phi_eff).toBeLessThanOrEqual(1);
  });
  it("regime is valid", () => {
    expect(["OPTIMO", "FUNCIONAL", "CARGADO", "SATURADO"]).toContain(handoff.regime);
  });
  it("gate is valid", () => {
    expect(["APPROVE", "REVIEW", "BLOCK"]).toContain(handoff.gate);
  });
  it("has city summary", () => {
    expect(handoff.city.agents).toBe(AGENT_ROLES.length);
    expect(typeof handoff.city.buildings).toBe("number");
  });
  it("has next_action string", () => {
    expect(typeof handoff.next_action).toBe("string");
    expect(handoff.next_action.length).toBeGreaterThan(0);
  });
  it("risks is an array", () => {
    expect(Array.isArray(handoff.risks)).toBe(true);
  });
});
