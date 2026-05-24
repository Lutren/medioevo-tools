import type { PhysicsMetrics } from "./types";
import { clamp } from "./vector";

export interface PhysicsMetricInput {
  bodyCount: number;
  pairChecks: number;
  resolvedCollisions: number;
  unresolvedCollisions: number;
  outOfBounds: number;
  nanDetected: number;
}

export function computePhysicsMetrics(input: PhysicsMetricInput): PhysicsMetrics {
  const n2 = Math.max(1, input.bodyCount * input.bodyCount);
  const unresolvedRate = input.unresolvedCollisions / Math.max(1, input.pairChecks);
  const pairPressure = input.pairChecks / n2;
  const R_physics = clamp(
    unresolvedRate * 0.55 +
    input.outOfBounds * 0.08 +
    input.nanDetected * 0.5 +
    pairPressure * 0.25,
    0,
    1,
  );
  const Phi_physics = clamp(input.resolvedCollisions / Math.max(input.pairChecks, 1), 0, 1);
  return {
    ...input,
    frameCostEstimate: Math.round((input.bodyCount + input.pairChecks * 0.4) * 100) / 100,
    R_physics,
    Phi_physics,
  };
}
