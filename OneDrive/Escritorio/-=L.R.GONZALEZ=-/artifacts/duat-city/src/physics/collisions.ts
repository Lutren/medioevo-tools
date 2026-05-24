import type { CityState, TileType } from "../core/types";
import type { PhysicsBody, PhysicsBounds } from "./types";
import { clamp, distance, finite, normalize, sub } from "./vector";

const WALKABLE: TileType[] = ["empty", "road", "plaza", "garden"];

export function isFiniteBody(body: PhysicsBody): boolean {
  return [body.x, body.y, body.prevX, body.prevY, body.vx, body.vy].every(Number.isFinite);
}

export function resolveBounds(body: PhysicsBody, bounds: PhysicsBounds): boolean {
  const beforeX = body.x;
  const beforeY = body.y;
  body.x = clamp(body.x, bounds.minX, bounds.maxX);
  body.y = clamp(body.y, bounds.minY, bounds.maxY);
  if (body.x !== beforeX) body.vx *= -0.35;
  if (body.y !== beforeY) body.vy *= -0.35;
  return body.x !== beforeX || body.y !== beforeY;
}

export function resolveCircleCollision(a: PhysicsBody, b: PhysicsBody): boolean {
  if (a.id === b.id || (a.isStatic && b.isStatic)) return false;
  const delta = sub({ x: b.x, y: b.y }, { x: a.x, y: a.y });
  const dist = Math.max(distance({ x: a.x, y: a.y }, { x: b.x, y: b.y }), 1e-6);
  const minDist = a.radius + b.radius;
  if (dist >= minDist) return false;

  const n = normalize(delta);
  const overlap = minDist - dist;
  const totalInv = a.invMass + b.invMass || 1;
  const aShare = a.isStatic ? 0 : a.invMass / totalInv;
  const bShare = b.isStatic ? 0 : b.invMass / totalInv;

  a.x -= n.x * overlap * aShare;
  a.y -= n.y * overlap * aShare;
  b.x += n.x * overlap * bShare;
  b.y += n.y * overlap * bShare;

  const rvx = b.vx - a.vx;
  const rvy = b.vy - a.vy;
  const sepVelocity = rvx * n.x + rvy * n.y;
  if (sepVelocity < 0) {
    const impulse = -(1.2 * sepVelocity) / totalInv;
    if (!a.isStatic) {
      a.vx -= impulse * a.invMass * n.x;
      a.vy -= impulse * a.invMass * n.y;
    }
    if (!b.isStatic) {
      b.vx += impulse * b.invMass * n.x;
      b.vy += impulse * b.invMass * n.y;
    }
  }

  return true;
}

export function resolveSolidTileCollision(body: PhysicsBody, state: CityState): boolean {
  if (body.kind !== "agent" || body.isStatic) return false;
  const tx = Math.round(body.x);
  const ty = Math.round(body.y);
  if (tx < 0 || ty < 0 || tx >= state.width || ty >= state.height) return false;

  const tile = state.tiles[ty * state.width + tx];
  if (!tile || WALKABLE.includes(tile.type)) return false;
  if (tile.buildingId && tile.buildingId === body.targetBuildingId) return false;

  body.x = finite(body.prevX);
  body.y = finite(body.prevY);
  body.vx *= -0.25;
  body.vy *= -0.25;
  return true;
}
