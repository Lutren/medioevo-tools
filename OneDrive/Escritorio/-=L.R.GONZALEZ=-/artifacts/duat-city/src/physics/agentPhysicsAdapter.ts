import type { CityState } from "../core/types";
import { getActiveTaskForAgent } from "../sim/tasks";
import { getBuildingById } from "../sim/buildings";
import { bodyFromAgent } from "./bodies";
import { stepPhysicsWorld } from "./physicsEngine";
import type { PhysicsBody, PhysicsMetrics } from "./types";
import { EMPTY_PHYSICS_METRICS } from "./types";

export interface AgentPhysicsResult {
  state: CityState;
  bodies: PhysicsBody[];
  metrics: PhysicsMetrics;
}

export function agentsToBodies(state: CityState): PhysicsBody[] {
  return state.agents.map(agent => {
    const task = getActiveTaskForAgent(state.tasks, agent.id);
    const target = task?.targetBuildingId ? getBuildingById(state.buildings, task.targetBuildingId) : undefined;
    return bodyFromAgent(agent, target);
  });
}

export function applyBodiesToAgents(state: CityState, bodies: PhysicsBody[]): CityState {
  const byAgentId = new Map(bodies.filter(b => b.agentId).map(b => [b.agentId!, b]));
  const agents = state.agents.map(agent => {
    const body = byAgentId.get(agent.id);
    if (!body || !Number.isFinite(body.x) || !Number.isFinite(body.y)) return agent;
    return { ...agent, x: body.x, y: body.y };
  });
  return { ...state, agents };
}

export function stepAgentPhysics(
  state: CityState,
  _lod: unknown,
  dt = 0.05,
  enablePhysicsCollisions = true,
): AgentPhysicsResult {
  if (state.agents.length === 0) {
    return { state, bodies: [], metrics: EMPTY_PHYSICS_METRICS };
  }
  const bodies = agentsToBodies(state);
  const world = stepPhysicsWorld(state, bodies, {
    dt,
    enableCollisions: enablePhysicsCollisions,
    cellSize: 1.5,
  });
  const next = applyBodiesToAgents(state, world.bodies);
  return { state: { ...next, physicsMetrics: world.metrics }, bodies: world.bodies, metrics: world.metrics };
}
