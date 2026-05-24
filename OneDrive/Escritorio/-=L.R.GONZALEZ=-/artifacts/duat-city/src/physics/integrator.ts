import type { CityState } from "../core/types";
import type { PhysicsBody } from "./types";
import { clampDt, normalize, sub } from "./vector";

export function applyForces(body: PhysicsBody, state: CityState): { ax: number; ay: number } {
  if (body.isStatic) return { ax: 0, ay: 0 };

  let ax = 0;
  let ay = 0;

  if (body.targetX !== undefined && body.targetY !== undefined) {
    const dir = normalize(sub({ x: body.targetX, y: body.targetY }, { x: body.x, y: body.y }));
    const gateFactor = body.gate === "BLOCK" ? 0.35 : body.gate === "REVIEW" ? 0.65 : 1;
    ax += dir.x * 5.5 * gateFactor;
    ay += dir.y * 5.5 * gateFactor;
  }

  const tx = Math.round(body.x);
  const ty = Math.round(body.y);
  const tile = tx >= 0 && ty >= 0 && tx < state.width && ty < state.height
    ? state.tiles[ty * state.width + tx]
    : undefined;
  if (tile?.type === "road") {
    body.damping = Math.min(0.95, body.damping + 0.05);
  }
  if (tile && ["water", "wall", "stone"].includes(tile.type)) {
    const away = normalize(sub({ x: body.x, y: body.y }, { x: tile.x + 0.5, y: tile.y + 0.5 }));
    ax += away.x * 3.2;
    ay += away.y * 3.2;
    body.damping = Math.max(0.72, body.damping - 0.04);
  }

  const needs = body.needs;
  if (needs) {
    const pullToType = (type: string, strength: number) => {
      const b = state.buildings.find(candidate => candidate.type === type);
      if (!b) return;
      const dir = normalize(sub({ x: b.x, y: b.y }, { x: body.x, y: body.y }));
      ax += dir.x * strength;
      ay += dir.y * strength;
    };
    if (needs.hunger < 0.3) pullToType("market", 1.8);
    if (needs.safety < 0.35 || needs.energy < 0.25) pullToType("clinic", 1.5);
  }

  const nearRuin = state.buildings.find(b => b.type === "ruin" && Math.hypot(b.x - body.x, b.y - body.y) < 3);
  if (nearRuin && body.agentRole !== "Scout" && body.agentRole !== "Observer") {
    const away = normalize(sub({ x: body.x, y: body.y }, { x: nearRuin.x, y: nearRuin.y }));
    ax += away.x * 2.2;
    ay += away.y * 2.2;
  }

  return { ax, ay };
}

export function integrateBody(body: PhysicsBody, dtInput: number | undefined, ax: number, ay: number): void {
  if (body.isStatic) return;
  const dt = clampDt(dtInput);
  body.prevX = body.x;
  body.prevY = body.y;
  body.vx = (body.vx + ax * dt) * body.damping;
  body.vy = (body.vy + ay * dt) * body.damping;
  body.x += body.vx * dt;
  body.y += body.vy * dt;
}
