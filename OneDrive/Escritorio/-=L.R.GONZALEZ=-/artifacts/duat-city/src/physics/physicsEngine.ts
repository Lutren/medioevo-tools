import type { CityState } from "../core/types";
import type { PhysicsBody, PhysicsMetrics, PhysicsStepOptions, PhysicsWorld } from "./types";
import { EMPTY_PHYSICS_METRICS } from "./types";
import { cityBounds } from "./bodies";
import { isFiniteBody, resolveCircleCollision } from "./collisions";
import { buildSpatialHash, queryNearby } from "./spatialHash";
import { NewtonianKernel, FractalKernel, type PhysicsKernel } from "./kernels";
import { computePhysicsMetrics } from "./physicsMetrics";

export function stepPhysicsWorld(
  state: CityState,
  bodies: PhysicsBody[],
  options: PhysicsStepOptions = {},
): PhysicsWorld {
  if (bodies.length === 0) {
    return { bodies, bounds: cityBounds(state), tick: state.tick, metrics: EMPTY_PHYSICS_METRICS };
  }

  // Select Kernel based on Plane
  const kernel: PhysicsKernel = state.context.activePlane === "astral" ? FractalKernel : NewtonianKernel;
  
  const bounds = cityBounds(state);
  const dt = options.dt ?? 0.05;
  
  // Delegate integration to Kernel
  kernel.step(state, bodies, dt);

  let resolvedCollisions = 0;
  let unresolvedCollisions = 0;
  let pairChecks = 0;

  if (options.enableCollisions !== false) {
    const hash = buildSpatialHash(bodies, options.cellSize ?? 1.5);
    const seen = new Set<string>();
    for (const body of bodies) {
      for (const other of queryNearby(hash, body)) {
        if (body.id === other.id) continue;
        const key = body.id < other.id ? `${body.id}|${other.id}` : `${other.id}|${body.id}`;
        if (seen.has(key)) continue;
        seen.add(key);
        pairChecks++;
        if (resolveCircleCollision(body, other)) resolvedCollisions++;
      }
    }
  }

  const metrics: PhysicsMetrics = computePhysicsMetrics({
    bodyCount: bodies.length,
    pairChecks,
    resolvedCollisions,
    unresolvedCollisions,
    outOfBounds: 0,
    nanDetected: 0,
  });

  return { bodies, bounds, tick: state.tick, metrics };
}
