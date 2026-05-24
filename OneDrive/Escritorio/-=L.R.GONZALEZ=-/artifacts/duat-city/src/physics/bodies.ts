import type { Agent, Building, CityState, Gate } from "../core/types";
import type { PhysicsBody, PhysicsBounds } from "./types";

export function cityBounds(state: CityState): PhysicsBounds {
  return { minX: 0, minY: 0, maxX: state.width - 1, maxY: state.height - 1 };
}

export function bodyFromAgent(agent: Agent, target?: Building): PhysicsBody {
  const mass = 1;
  return {
    id: `body:${agent.id}`,
    kind: "agent",
    x: agent.x,
    y: agent.y,
    prevX: agent.x,
    prevY: agent.y,
    vx: 0,
    vy: 0,
    radius: 0.22,
    mass,
    invMass: 1 / mass,
    damping: agent.gate === "BLOCK" ? 0.72 : 0.86,
    isStatic: false,
    agentId: agent.id,
    agentRole: agent.role,
    targetX: target?.x,
    targetY: target?.y,
    targetBuildingId: target?.id,
    needs: agent.needs,
    R: agent.R,
    Phi_eff: agent.Phi_eff,
    gate: agent.gate,
  };
}

export function staticSensorBody(id: string, x: number, y: number, gate: Gate = "APPROVE"): PhysicsBody {
  return {
    id,
    kind: "sensor",
    x,
    y,
    prevX: x,
    prevY: y,
    vx: 0,
    vy: 0,
    radius: 0.2,
    mass: Infinity,
    invMass: 0,
    damping: 1,
    isStatic: true,
    R: 0,
    Phi_eff: 1,
    gate,
  };
}
