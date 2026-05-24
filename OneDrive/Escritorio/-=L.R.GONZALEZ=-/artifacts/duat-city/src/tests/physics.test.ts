import { describe, expect, it } from "vitest";
import { createCity } from "../sim/city";
import { resolveCircleCollision } from "../physics/collisions";
import { stepPhysicsWorld } from "../physics/physicsEngine";
import { computePhysicsMetrics } from "../physics/physicsMetrics";
import { buildSpatialHash, estimatePairChecks, queryNearby } from "../physics/spatialHash";
import { add, vec } from "../physics/vector";
import type { PhysicsBody } from "../physics/types";

function body(id: string, x: number, y: number): PhysicsBody {
  return {
    id, kind: "agent", x, y, prevX: x, prevY: y, vx: 0, vy: 0,
    radius: 0.4, mass: 1, invMass: 1, damping: 0.9, isStatic: false,
    R: 0.1, Phi_eff: 0.9, gate: "APPROVE",
  };
}

describe("physics core", () => {
  it("vector ops do not produce NaN", () => {
    const out = add(vec(Number.NaN, 1), vec(2, Number.POSITIVE_INFINITY));
    expect(Number.isNaN(out.x)).toBe(false);
    expect(Number.isNaN(out.y)).toBe(false);
  });

  it("spatial hash returns nearby bodies and reduces pair checks", () => {
    const bodies = [body("a", 1, 1), body("b", 1.2, 1.1), body("c", 20, 20)];
    const hash = buildSpatialHash(bodies, 2);
    expect(queryNearby(hash, bodies[0]).map(b => b.id)).toContain("b");
    expect(estimatePairChecks(hash)).toBeLessThan((bodies.length * (bodies.length - 1)) / 2);
  });

  it("collision resolution separates overlapping circles", () => {
    const a = body("a", 1, 1);
    const b = body("b", 1.1, 1);
    expect(resolveCircleCollision(a, b)).toBe(true);
    expect(Math.hypot(a.x - b.x, a.y - b.y)).toBeGreaterThanOrEqual(a.radius + b.radius - 1e-6);
  });

  it("bodies stay within bounds", () => {
    const state = createCity();
    const b = body("a", -2, 500);
    const world = stepPhysicsWorld(state, [b], { dt: 0.05 });
    expect(world.bodies[0].x).toBeGreaterThanOrEqual(0);
    expect(world.bodies[0].y).toBeLessThanOrEqual(state.height - 1);
  });

  it("R_physics rises with unresolved collisions", () => {
    const low = computePhysicsMetrics({ bodyCount: 10, pairChecks: 5, resolvedCollisions: 5, unresolvedCollisions: 0, outOfBounds: 0, nanDetected: 0 });
    const high = computePhysicsMetrics({ bodyCount: 10, pairChecks: 5, resolvedCollisions: 0, unresolvedCollisions: 5, outOfBounds: 0, nanDetected: 0 });
    expect(high.R_physics).toBeGreaterThan(low.R_physics);
  });
});
