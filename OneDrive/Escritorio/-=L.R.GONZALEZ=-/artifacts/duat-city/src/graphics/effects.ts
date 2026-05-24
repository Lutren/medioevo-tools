import type { CityState } from "../core/types";
import type { Particle } from "./types";
import { spawnParticle } from "./particles";

export function particlesForState(state: CityState, particlesEnabled: boolean): Particle[] {
  if (!particlesEnabled) return [];
  const particles: Particle[] = [];
  const done = state.tasks.filter(t => t.status === "done").slice(-4);
  for (const task of done) {
    const agent = state.agents.find(a => a.id === task.agentId);
    if (agent) particles.push(spawnParticle("task", agent.x, agent.y, state.tick));
  }
  for (const building of state.buildings.filter(b => b.gate === "BLOCK").slice(0, 5)) {
    particles.push(spawnParticle("block", building.x, building.y, state.tick));
  }
  for (const ruin of state.buildings.filter(b => b.type === "ruin").slice(0, 3)) {
    particles.push(spawnParticle("anomaly", ruin.x, ruin.y, state.tick));
  }
  return particles.slice(-300);
}
