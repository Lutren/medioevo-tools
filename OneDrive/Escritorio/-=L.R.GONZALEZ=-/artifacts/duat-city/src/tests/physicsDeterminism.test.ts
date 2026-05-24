import { describe, expect, it } from "vitest";
import { createCity } from "../sim/city";
import { tickEngine } from "../sim/engine";

describe("physics determinism", () => {
  it("same seed and physics ticks produce the same agent position hash", () => {
    expect(runPhysicsHash("physics-seed", 24)).toBe(runPhysicsHash("physics-seed", 24));
  });
});

function runPhysicsHash(seed: string, ticks: number): string {
  let state = createCity(seed);
  for (let i = 0; i < ticks; i++) {
    state = tickEngine(state, { enableAgentPhysics: true, enablePhysicsCollisions: true, physicsDt: 0.05 });
  }
  return state.agents
    .map(agent => `${agent.id}:${agent.x.toFixed(5)}:${agent.y.toFixed(5)}:${agent.gate}`)
    .join("|");
}
