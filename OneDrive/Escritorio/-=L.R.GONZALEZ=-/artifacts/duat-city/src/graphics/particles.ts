import type { Particle } from "./types";

export function spawnParticle(kind: Particle["kind"], x: number, y: number, tick: number): Particle {
  const angle = ((tick * 137.5) % 360) * Math.PI / 180;
  return {
    id: `${kind}:${tick}:${Math.round(x * 10)}:${Math.round(y * 10)}`,
    x,
    y,
    vx: Math.cos(angle) * 0.02,
    vy: Math.sin(angle) * 0.02,
    age: 0,
    ttl: kind === "block" ? 45 : 30,
    kind,
  };
}

export function stepParticles(particles: Particle[], compress = false): Particle[] {
  if (compress) return [];
  return particles
    .map(p => ({ ...p, x: p.x + p.vx, y: p.y + p.vy, age: p.age + 1 }))
    .filter(p => p.age < p.ttl)
    .slice(-300);
}
