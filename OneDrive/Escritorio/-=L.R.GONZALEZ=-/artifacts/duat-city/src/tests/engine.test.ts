import { describe, it, expect } from "vitest";
import { tickEngine } from "../sim/engine";
import { createCity } from "../sim/city";

describe("tickEngine", () => {
  it("increments tick", () => {
    const s0 = createCity();
    const s1 = tickEngine(s0);
    expect(s1.tick).toBe(s0.tick + 1);
  });

  it("R stays in [0,1]", () => {
    let state = createCity();
    for (let i = 0; i < 10; i++) state = tickEngine(state);
    expect(state.R).toBeGreaterThanOrEqual(0);
    expect(state.R).toBeLessThanOrEqual(1);
  });

  it("Phi_eff stays in [0,1]", () => {
    let state = createCity();
    for (let i = 0; i < 10; i++) state = tickEngine(state);
    expect(state.Phi_eff).toBeGreaterThanOrEqual(0);
    expect(state.Phi_eff).toBeLessThanOrEqual(1);
  });

  it("agent count stays constant", () => {
    let state = createCity();
    const agentCount = state.agents.length;
    for (let i = 0; i < 5; i++) state = tickEngine(state);
    expect(state.agents.length).toBe(agentCount);
  });

  it("assigns tasks", () => {
    let state = createCity();
    for (let i = 0; i < 3; i++) state = tickEngine(state);
    expect(state.tasks.length).toBeGreaterThan(0);
  });

  it("regime is one of the valid values", () => {
    let state = createCity();
    for (let i = 0; i < 10; i++) state = tickEngine(state);
    expect(["OPTIMO", "FUNCIONAL", "CARGADO", "SATURADO"]).toContain(state.regime);
  });

  it("gate is valid", () => {
    let state = createCity();
    for (let i = 0; i < 5; i++) state = tickEngine(state);
    expect(["APPROVE", "REVIEW", "BLOCK"]).toContain(state.gate);
  });

  it("replays deterministic core state from the same initial seed", () => {
    let left = createCity("replay-smoke");
    let right = createCity("replay-smoke");

    for (let i = 0; i < 12; i++) {
      left = tickEngine(left);
      right = tickEngine(right);
    }

    expect({
      tick: left.tick,
      agents: left.agents,
      tasks: left.tasks,
      events: left.events,
      R: left.R,
      Phi_eff: left.Phi_eff,
    }).toEqual({
      tick: right.tick,
      agents: right.agents,
      tasks: right.tasks,
      events: right.events,
      R: right.R,
      Phi_eff: right.Phi_eff,
    });
  });
});
