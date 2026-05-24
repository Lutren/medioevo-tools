import type { Agent, CityObject, CityState, Task } from "../core/types";
import { clamp, uid, type RandomSource } from "../core/math";
import { getObjectDef } from "./objects";

export type RoutinePhase = "morning_work" | "midday_social" | "evening_home" | "emergency";

export function routineForTick(tick: number, agent: Agent): RoutinePhase {
  if (agent.needs.safety < 0.2 || agent.gate === "BLOCK") return "emergency";
  const phase = tick % 96;
  if (phase < 36) return "morning_work";
  if (phase < 64) return "midday_social";
  return "evening_home";
}

function needCategory(agent: Agent): CityObject["defId"] | "market-stall" | "bed" | "clinic-bed" | "archive-desk" | "workbench" | undefined {
  const n = agent.needs;
  if (n.hunger < 0.3) return "market-stall";
  if (n.energy < 0.3) return "bed";
  if (n.safety < 0.3) return "clinic-bed";
  if (n.curiosity < 0.25) return "archive-desk";
  if (n.purpose < 0.25) return "workbench";
  return undefined;
}

export function chooseObjectForNeed(agent: Agent, state: CityState): CityObject | undefined {
  const preferredDef = needCategory(agent);
  if (!preferredDef) return undefined;
  const candidates = state.objects.filter(obj => obj.defId === preferredDef && !obj.occupiedBy);
  if (candidates.length === 0) return undefined;
  return candidates.reduce((best, obj) => {
    const bestD = Math.hypot(agent.x - best.x, agent.y - best.y);
    const d = Math.hypot(agent.x - obj.x, agent.y - obj.y);
    return d < bestD ? obj : best;
  });
}

export function createLifeTaskForAgent(agent: Agent, state: CityState, rng?: RandomSource): Task | undefined {
  const obj = chooseObjectForNeed(agent, state);
  if (!obj) return undefined;
  const def = getObjectDef(obj.defId);
  if (!def) return undefined;
  const type: Task["type"] =
    def.category === "rest" ? "rest" :
    def.category === "food" || def.category === "garden" ? "eat" :
    def.category === "health" ? "heal" :
    def.category === "archive" || def.category === "learning" ? "research" :
    def.category === "work" ? "work" :
    def.category === "ruin" ? "explore" : "work";

  return {
    id: uid(rng),
    type,
    title: `${def.name} interaction (${agent.name})`,
    agentId: agent.id,
    targetBuildingId: obj.buildingId,
    progress: 0,
    status: "pending",
    R_delta: def.effects.R_delta ?? -0.015,
    Phi_delta: def.effects.Phi_delta ?? 0.01,
    evidence: [`object=${obj.id}`],
  };
}

export function applyObjectInteraction(agent: Agent, object: CityObject, state: CityState): { agent: Agent; state: CityState; evidence: string[] } {
  const def = getObjectDef(object.defId);
  if (!def) return { agent, state, evidence: [] };
  const needs = { ...agent.needs };
  for (const key of ["energy", "hunger", "social", "purpose", "safety", "curiosity"] as const) {
    const delta = def.effects[key];
    if (typeof delta === "number") needs[key] = clamp(needs[key] + delta, 0, 1);
  }
  const resources = { ...state.resources };
  if (def.effects.resource_delta) {
    for (const [key, delta] of Object.entries(def.effects.resource_delta)) {
      resources[key as keyof typeof resources] = clamp((resources[key as keyof typeof resources] ?? 0) + Number(delta), 0, 999);
    }
  }
  const updatedAgent: Agent = {
    ...agent,
    needs,
    mood: clamp(agent.mood + 0.025, 0, 1),
    R: clamp(agent.R + (def.effects.R_delta ?? 0), 0, 1),
    Phi_eff: clamp(agent.Phi_eff + (def.effects.Phi_delta ?? 0), 0, 1),
    memory: [...agent.memory, `Used ${def.name}`].slice(-10),
  };
  return {
    agent: updatedAgent,
    state: { ...state, resources },
    evidence: [`object_interaction=${object.id}`, `def=${def.id}`],
  };
}
