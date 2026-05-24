import type { CityState } from "../core/types";
import type { PhysicsBody, PhysicsMetrics, PhysicsStepOptions, PhysicsWorld } from "./types";
import { EMPTY_PHYSICS_METRICS } from "./types";
import { cityBounds } from "./bodies";
import { isFiniteBody, resolveBounds, resolveCircleCollision, resolveSolidTileCollision } from "./collisions";
import { applyForces, integrateBody } from "./integrator";
import { computePhysicsMetrics } from "./physicsMetrics";
import { buildSpatialHash, queryNearby } from "./spatialHash";

export function stepPhysicsWorld(
  state: CityState,
  bodies: PhysicsBody[],
  options: PhysicsStepOptions = {},
): PhysicsWorld {
  if (bodies.length === 0) {
    return { bodies, bounds: cityBounds(state), tick: state.tick, metrics: EMPTY_PHYSICS_METRICS };
  }

  const bounds = cityBounds(state);
  const dt = options.dt ?? 0.05;
  let outOfBounds = 0;
  let nanDetected = 0;
  let resolvedCollisions = 0;
  let unresolvedCollisions = 0;
  let pairChecks = 0;

  for (const body of bodies) {
    const force = applyForces(body, state);
    integrateBody(body, dt, force.ax, force.ay);
    if (resolveBounds(body, bounds)) outOfBounds++;
    if (resolveSolidTileCollision(body, state)) resolvedCollisions++;
    if (!isFiniteBody(body)) {
      nanDetected++;
      body.x = body.prevX || 0;
      body.y = body.prevY || 0;
      body.vx = 0;
      body.vy = 0;
    }
  }

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

    for (const body of bodies) {
      for (const other of queryNearby(hash, body)) {
        if (body.id >= other.id) continue;
        const d = Math.hypot(body.x - other.x, body.y - other.y);
        if (d + 1e-6 < body.radius + other.radius) unresolvedCollisions++;
      }
    }
  }

  const metrics: PhysicsMetrics = computePhysicsMetrics({
    bodyCount: bodies.length,
    pairChecks,
    resolvedCollisions,
    unresolvedCollisions,
    outOfBounds,
    nanDetected,
  });

  return { bodies, bounds, tick: state.tick, metrics };
}
