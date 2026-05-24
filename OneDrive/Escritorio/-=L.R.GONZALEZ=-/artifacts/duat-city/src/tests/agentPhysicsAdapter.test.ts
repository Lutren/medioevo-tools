import { describe, expect, it } from "vitest";
import { createCity } from "../sim/city";
import { tickEngine } from "../sim/engine";
import { createTask } from "../sim/tasks";
import { agentsToBodies, applyBodiesToAgents, stepAgentPhysics } from "../physics/agentPhysicsAdapter";

describe("agent physics adapter", () => {
  it("agentsToBodies count matches agents", () => {
    const state = createCity();
    expect(agentsToBodies(state)).toHaveLength(state.agents.length);
  });

  it("applyBodiesToAgents updates positions", () => {
    const state = createCity();
    const bodies = agentsToBodies(state);
    bodies[0] = { ...bodies[0], x: bodies[0].x + 1, y: bodies[0].y + 1 };
    const next = applyBodiesToAgents(state, bodies);
    expect(next.agents[0].x).toBeCloseTo(state.agents[0].x + 1);
    expect(next.agents[0].y).toBeCloseTo(state.agents[0].y + 1);
  });

  it("physics off preserves default tick path", () => {
    const base = createCity();
    const agent = base.agents[0];
    const target = base.buildings.find(b => b.type === "market") ?? base.buildings[0];
    const task = { ...createTask("eat", agent.id, target.id), status: "active" as const };
    const state = { ...base, tasks: [task] };
    const defaultTick = tickEngine(state);
    const explicitOff = tickEngine(state, { enableAgentPhysics: false });
    expect(explicitOff.agents[0].x).toBeCloseTo(defaultTick.agents[0].x);
    expect(explicitOff.physicsMetrics).toBeUndefined();
  });

  it("physics on moves agents and avoids NaN", () => {
    const base = createCity();
    const agent = base.agents[0];
    const target = base.buildings[0];
    const task = { ...createTask("work", agent.id, target.id), status: "active" as const };
    const state = { ...base, tasks: [task] };
    const result = stepAgentPhysics(state, undefined, 0.05);
    expect(result.state.agents.some(a => a.x !== base.agents.find(old => old.id === a.id)?.x)).toBe(true);
    expect(result.state.agents.every(a => Number.isFinite(a.x) && Number.isFinite(a.y))).toBe(true);
  });
});
