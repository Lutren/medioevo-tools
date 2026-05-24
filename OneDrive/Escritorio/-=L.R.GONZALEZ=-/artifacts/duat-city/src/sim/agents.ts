import type { Agent, AgentNeeds, Gate, Building } from "../core/types";
import { uid, clamp, dist, randBetween, type RandomSource } from "../core/math";
import { computeAgentGate, computePhiEff } from "../core/metrics";
import { generateAgentLineage, generateOriginStory } from "../generative/agentLineageGenerator";
import { defaultSkillPackForRole, installSkillPack } from "../brain/skillPacks";

export const AGENT_ROLES = [
  "Observer", "Engineer", "Archivist", "Medic", "Builder",
  "Trader", "Teacher", "Scout", "Gatekeeper", "Storykeeper", "Artisan", "Courier",
  "Psychologist",
] as const;

export type AgentRole = typeof AGENT_ROLES[number];

export const ROLE_TASK_PREFS: Record<AgentRole, string[]> = {
  Observer: ["explore", "research"],
  Engineer: ["work", "build"],
  Archivist: ["archive", "research"],
  Medic: ["heal", "rest"],
  Builder: ["build", "work"],
  Trader: ["trade", "explore"],
  Teacher: ["teach", "research"],
  Scout: ["explore", "quest"],
  Gatekeeper: ["work", "archive"],
  Storykeeper: ["archive", "quest"],
  Artisan: ["work", "build"],
  Courier: ["trade", "handoff"],
  Psychologist: ["heal", "teach"],
};

export function makeDefaultNeeds(rng?: RandomSource): AgentNeeds {
  return {
    energy: randBetween(0.6, 1.0, rng),
    hunger: randBetween(0.6, 1.0, rng),
    social: randBetween(0.5, 1.0, rng),
    purpose: randBetween(0.5, 1.0, rng),
    safety: randBetween(0.7, 1.0, rng),
    curiosity: randBetween(0.4, 1.0, rng),
  };
}

export function createAgent(role: AgentRole, x: number, y: number, rng?: RandomSource): Agent {
  const id = uid(rng);
  const lineage = generateAgentLineage(role, rng);
  return {
    id,
    name: `${role}-${id.slice(0, 4)}`,
    role,
    x,
    y,
    needs: makeDefaultNeeds(rng),
    mood: randBetween(0.5, 0.9, rng),
    trust: randBetween(0.5, 0.9, rng),
    R: randBetween(0.05, 0.25, rng),
    Phi_eff: randBetween(0.7, 0.95, rng),
    gate: "APPROVE",
    lineage,
    originStory: generateOriginStory(role, lineage),
    skills: [],
    memory: [],
    relationships: {},
    inventory: {},
  };
}

export function createInitialAgents(cityWidth: number, cityHeight: number, rng?: RandomSource): Agent[] {
  const cx = Math.floor(cityWidth / 2);
  const cy = Math.floor(cityHeight / 2);
  return AGENT_ROLES.map((role, i) => {
    const angle = (i / AGENT_ROLES.length) * Math.PI * 2;
    const r = 4;
    const x = clamp(cx + Math.round(Math.cos(angle) * r), 1, cityWidth - 2);
    const y = clamp(cy + Math.round(Math.sin(angle) * r), 1, cityHeight - 2);
    return createAgent(role as AgentRole, x, y, rng);
  });
}

export function decayNeeds(agent: Agent, dt: number): Agent {
  const rate = 0.0004 * dt;
  return {
    ...agent,
    needs: {
      energy: clamp(agent.needs.energy - rate * 1.2, 0, 1),
      hunger: clamp(agent.needs.hunger - rate * 1.0, 0, 1),
      social: clamp(agent.needs.social - rate * 0.7, 0, 1),
      purpose: clamp(agent.needs.purpose - rate * 0.6, 0, 1),
      safety: clamp(agent.needs.safety - rate * 0.5, 0, 1),
      curiosity: clamp(agent.needs.curiosity - rate * 0.8, 0, 1),
    },
  };
}

export function computeAgentR(agent: Agent): number {
  const needs = agent.needs;
  let r = 0;
  if (needs.energy < 0.25) r += 0.12;
  if (needs.hunger < 0.25) r += 0.15;
  if (needs.social < 0.2) r += 0.08;
  if (needs.purpose < 0.2) r += 0.06;
  if (needs.safety < 0.2) r += 0.10;
  if (needs.curiosity < 0.15) r += 0.04;
  return clamp(r + agent.R * 0.3, 0, 1);
}

export function updateAgentMetrics(agent: Agent): Agent {
  const R = computeAgentR(agent);
  const Phi_eff = computePhiEff(R, agent.mood, agent.trust);
  const gate: Gate = computeAgentGate(R);
  return { ...agent, R, Phi_eff, gate };
}

export function moveAgentToward(
  agent: Agent,
  targetX: number,
  targetY: number,
  speed: number,
  dt: number
): Agent {
  const d = dist(agent.x, agent.y, targetX, targetY);
  if (d < 0.15) return { ...agent, x: targetX, y: targetY };
  const step = Math.min(d, speed * dt * 0.004);
  const nx = agent.x + ((targetX - agent.x) / d) * step;
  const ny = agent.y + ((targetY - agent.y) / d) * step;
  return { ...agent, x: nx, y: ny };
}

export function restoreNeedAtBuilding(
  agent: Agent,
  buildingType: string
): Agent {
  const n = { ...agent.needs };
  switch (buildingType) {
    case "residential": n.energy = clamp(n.energy + 0.08, 0, 1); break;
    case "market":
    case "garden": n.hunger = clamp(n.hunger + 0.10, 0, 1); n.social = clamp(n.social + 0.04, 0, 1); break;
    case "clinic": n.safety = clamp(n.safety + 0.12, 0, 1); n.energy = clamp(n.energy + 0.05, 0, 1); break;
    case "archive": n.curiosity = clamp(n.curiosity + 0.10, 0, 1); n.purpose = clamp(n.purpose + 0.06, 0, 1); break;
    case "academy": {
      n.purpose = clamp(n.purpose + 0.10, 0, 1);
      n.curiosity = clamp(n.curiosity + 0.06, 0, 1);
      const trained = installSkillPack(agent, defaultSkillPackForRole(agent.role));
      return { ...trained, needs: n, mood: clamp(trained.mood + 0.02, 0, 1) };
    }
    case "theater": n.social = clamp(n.social + 0.06, 0, 1); n.purpose = clamp(n.purpose + 0.08, 0, 1); break;
    case "plaza":
    case "temple": n.social = clamp(n.social + 0.10, 0, 1); n.purpose = clamp(n.purpose + 0.04, 0, 1); break;
    case "observatory": n.curiosity = clamp(n.curiosity + 0.12, 0, 1); n.purpose = clamp(n.purpose + 0.06, 0, 1); break;
    case "workshop": n.purpose = clamp(n.purpose + 0.08, 0, 1); break;
    default: break;
  }
  const mood = clamp(agent.mood + 0.02, 0, 1);
  return { ...agent, needs: n, mood };
}

export function addMemory(agent: Agent, entry: string): Agent {
  const memory = [...agent.memory, entry].slice(-10);
  return { ...agent, memory };
}

export function updateRelationship(
  agent: Agent,
  otherId: string,
  delta: number
): Agent {
  const rel = { ...agent.relationships };
  rel[otherId] = clamp((rel[otherId] ?? 0) + delta, -1, 1);
  return { ...agent, relationships: rel };
}

export function findNearestBuilding(
  agent: Agent,
  buildings: Building[],
  type: string
): Building | undefined {
  const matching = buildings.filter(b => b.type === type);
  if (matching.length === 0) return undefined;
  return matching.reduce((best, b) => {
    const dBest = dist(agent.x, agent.y, best.x, best.y);
    const dB = dist(agent.x, agent.y, b.x, b.y);
    return dB < dBest ? b : best;
  });
}
