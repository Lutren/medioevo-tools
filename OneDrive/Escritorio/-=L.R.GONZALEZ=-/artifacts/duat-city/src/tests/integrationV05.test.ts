import { describe, expect, it } from "vitest";
import { createCity } from "../sim/city";
import { AGENT_ROLES, createAgent } from "../sim/agents";
import { tickEngine } from "../sim/engine";
import { exportRPGWorld } from "../rpg/worldExport";
import { toWabiHandoff } from "../wabi/wabiHandoff";

describe("v0.5 integration", () => {
  it("simulates 1000 ticks with 50 agents without NaN", () => {
    let state = createCity();
    const agents = Array.from({ length: 50 }, (_, i) => createAgent(AGENT_ROLES[i % AGENT_ROLES.length], 24 + (i % 5) * 0.1, 16 + (i % 7) * 0.1));
    state = { ...state, agents };
    for (let i = 0; i < 1000; i++) {
      state = tickEngine(state, { enableAgentPhysics: true, enablePhysicsCollisions: true });
    }

    const completed = state.tasks.filter(t => t.status === "done").length;
    const world = exportRPGWorld(state);
    const handoff = toWabiHandoff({ state, physicsMetrics: state.physicsMetrics, graphicsMetrics: state.graphicsMetrics });

    expect(completed).toBeGreaterThan(0);
    expect(state.witnesslog.length).toBeGreaterThan(0);
    expect([state.R, state.Phi_eff, state.physicsMetrics?.R_physics ?? 0, state.physicsMetrics?.Phi_physics ?? 1]).toEqual(expect.arrayContaining([expect.any(Number)]));
    expect(state.agents.every(a => Number.isFinite(a.x) && Number.isFinite(a.y))).toBe(true);
    expect(world.schema).toBe("medioevo-rpg/world/v3");
    expect(handoff.schema).toBe("wabi/duat-city/handoff/v0.5-design");
  });
});
