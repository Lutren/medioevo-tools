import type { Particle } from "./types";

export type ParticleKindV06 = Particle["kind"] | "dust" | "smoke" | "rain" | "osit" | "ruin";

export interface VisualParticle extends Omit<Particle, "kind"> {
  kind: ParticleKindV06;
  color: string;
}

export function spawnVisualParticle(kind: ParticleKindV06, x: number, y: number, tick: number): VisualParticle {
  const angle = ((tick * 137 + x * 11 + y * 3) % 360) * Math.PI / 180;
  const speed = kind === "rain" ? 0.12 : kind === "smoke" ? 0.025 : 0.04;
  return {
    id: `${kind}:${tick}:${Math.round(x * 10)}:${Math.round(y * 10)}`,
    kind,
    x,
    y,
    vx: kind === "rain" ? -0.02 : Math.cos(angle) * speed,
    vy: kind === "rain" ? 0.18 : kind === "smoke" ? -speed : Math.sin(angle) * speed,
    age: 0,
    ttl: kind === "rain" ? 24 : kind === "smoke" ? 64 : 36,
    color: particleColor(kind),
  };
}

export function stepVisualParticles(particles: VisualParticle[], maxParticles = 300, compress = false): VisualParticle[] {
  if (compress) return [];
  return particles
    .map(p => ({ ...p, x: p.x + p.vx, y: p.y + p.vy, age: p.age + 1 }))
    .filter(p => p.age < p.ttl)
    .slice(-maxParticles);
}

export function drawVisualParticles(ctx: CanvasRenderingContext2D, particles: VisualParticle[], tileSize: number): void {
  ctx.save();
  for (const p of particles) {
    const alpha = Math.max(0, 1 - p.age / p.ttl);
    ctx.fillStyle = p.color.replace("ALPHA", alpha.toFixed(3));
    ctx.beginPath();
    ctx.arc(p.x * tileSize, p.y * tileSize, Math.max(1, tileSize * 0.08), 0, Math.PI * 2);
    ctx.fill();
  }
  ctx.restore();
}

function particleColor(kind: ParticleKindV06): string {
  switch (kind) {
    case "rain": return "rgba(116,220,255,ALPHA)";
    case "smoke": return "rgba(140,150,160,ALPHA)";
    case "dust": return "rgba(190,150,95,ALPHA)";
    case "ruin":
    case "anomaly": return "rgba(255,209,102,ALPHA)";
    case "osit": return "rgba(36,232,255,ALPHA)";
    case "block": return "rgba(255,68,68,ALPHA)";
    default: return "rgba(69,255,152,ALPHA)";
  }
}
