import { describe, expect, it } from "vitest";
import { applyObjectInteraction, createLifeTaskForAgent } from "../sim/agentLife";
import { createCity } from "../sim/city";

describe("agent life simulation", () => {
  it("hunger creates eat task", () => {
    const state = createCity();
    const agent = { ...state.agents[0], needs: { ...state.agents[0].needs, hunger: 0.05 } };
    const task = createLifeTaskForAgent(agent, state);
    expect(task?.type).toBe("eat");
  });

  it("energy creates rest task", () => {
    const state = createCity();
    const agent = { ...state.agents[0], needs: { ...state.agents[0].needs, hunger: 0.8, energy: 0.05 } };
    const task = createLifeTaskForAgent(agent, state);
    expect(task?.type).toBe("rest");
  });

  it("agent can use building object", () => {
    const state = createCity();
    const object = state.objects.find(obj => obj.defId === "market-stall")!;
    const agent = { ...state.agents[0], needs: { ...state.agents[0].needs, hunger: 0.1 } };
    const result = applyObjectInteraction(agent, object, state);
    expect(result.agent.needs.hunger).toBeGreaterThan(agent.needs.hunger);
    expect(result.evidence.length).toBeGreaterThan(0);
  });

  it("relationship state remains mutable around interactions", () => {
    const state = createCity();
    const object = state.objects[0];
    const agent = { ...state.agents[0], relationships: { other: 0.1 } };
    const result = applyObjectInteraction(agent, object, state);
    expect(result.agent.relationships.other).toBe(0.1);
    expect(result.agent.memory.at(-1)).toMatch(/Used/);
  });
});
