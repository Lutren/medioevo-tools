import type { AgentNeeds, Gate } from "../core/types";

export type PhysicsBodyKind = "agent" | "particle" | "resource" | "sensor";

export interface PhysicsBody {
  id: string;
  kind: PhysicsBodyKind;
  x: number;
  y: number;
  prevX: number;
  prevY: number;
  vx: number;
  vy: number;
  radius: number;
  mass: number;
  invMass: number;
  damping: number;
  isStatic: boolean;
  agentId?: string;
  agentRole?: string;
  buildingId?: string;
  targetX?: number;
  targetY?: number;
  targetBuildingId?: string;
  needs?: AgentNeeds;
  R: number;
  Phi_eff: number;
  gate: Gate;
}

export interface PhysicsBounds {
  minX: number;
  minY: number;
  maxX: number;
  maxY: number;
}

export interface PhysicsMetrics {
  bodyCount: number;
  pairChecks: number;
  resolvedCollisions: number;
  unresolvedCollisions: number;
  outOfBounds: number;
  nanDetected: number;
  frameCostEstimate: number;
  R_physics: number;
  Phi_physics: number;
}

export interface PhysicsWorld {
  bodies: PhysicsBody[];
  bounds: PhysicsBounds;
  tick: number;
  metrics: PhysicsMetrics;
}

export interface PhysicsStepOptions {
  dt?: number;
  cellSize?: number;
  enableCollisions?: boolean;
}

export const EMPTY_PHYSICS_METRICS: PhysicsMetrics = {
  bodyCount: 0,
  pairChecks: 0,
  resolvedCollisions: 0,
  unresolvedCollisions: 0,
  outOfBounds: 0,
  nanDetected: 0,
  frameCostEstimate: 0,
  R_physics: 0,
  Phi_physics: 1,
};
