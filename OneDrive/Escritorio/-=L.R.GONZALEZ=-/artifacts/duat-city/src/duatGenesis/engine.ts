import type { DuatEngineParams, ActiveObserver, KernelCell } from "./types";

export type DuatSeedMode = "duat" | "osiris" | "atum" | "none";

const DEFAULT_WIDTH = 130;
const DEFAULT_HEIGHT = 82;

function clamp(v: number, lo: number, hi: number): number {
  return v < lo ? lo : v > hi ? hi : v;
}

function bell(x: number, mean: number, sigma: number): number {
  return Math.exp(-((x - mean) ** 2) / (2 * sigma * sigma));
}

function ix(x: number, y: number, width: number, height: number): number {
  return ((y % height + height) % height) * width + ((x % width + width) % width);
}

class Mulberry32 {
  state: number;
  constructor(seed = 734567) {
    this.state = seed >>> 0;
  }
  next(): number {
    let z = this.state;
    z = (z + 0x6d2b79f5) | 0;
    z = Math.imul(z ^ (z >>> 15), 1 | z);
    z = Math.imul(z + (2 * (z & 65535)) >>> 0, 9 | (z >>> 15));
    z ^= z >>> 6;
    z ^= z >>> 11;
    this.state = z >>> 0;
    return (z >>> 0) * 2.3283064365386963e-10;
  }
  centered(variance: number): number {
    return (this.next() - 0.5) * 2 * variance;
  }
}

function buildGravityKernel(radius: number): KernelCell[] {
  const cells: KernelCell[] = [];
  for (let dy = -radius; dy <= radius; dy += 1) {
    for (let dx = -radius; dx <= radius; dx += 1) {
      if (dx === 0 && dy === 0) continue;
      const r = Math.sqrt(dx * dx + dy * dy) / radius;
      if (r > 1) continue;
      const w = Math.exp(-((r - 0.5) ** 2) / (2 * 0.22 ** 2));
      cells.push({ dx, dy, w });
    }
  }
  return normalize(cells);
}

function buildLightKernel(innerRadius: number, outerRadius: number): KernelCell[] {
  const cells: KernelCell[] = [];
  for (let dy = -outerRadius; dy <= outerRadius; dy += 1) {
    for (let dx = -outerRadius; dx <= outerRadius; dx += 1) {
      const r = Math.sqrt(dx * dx + dy * dy);
      if (r < innerRadius || r > outerRadius) continue;
      cells.push({ dx, dy, w: 1 });
    }
  }
  return normalize(cells);
}

function normalize(cells: KernelCell[]): KernelCell[] {
  const sum = cells.reduce((acc, cell) => acc + cell.w, 0);
  if (sum === 0) return cells;
  return cells.map((cell) => ({ ...cell, w: cell.w / sum }));
}

export class DuatEngine {
  readonly width: number;
  readonly height: number;
  readonly psi: Float32Array;
  readonly nextPsi: Float32Array;
  readonly gravity: Float32Array;
  readonly light: Float32Array;
  readonly previous: Float32Array;
  frame = 0;
  lastClipRatio = 0;
  seed: number;
  private rng: Mulberry32;
  private readonly GK: KernelCell[];
  private readonly LK: KernelCell[];

  constructor(seed = 734567, width = DEFAULT_WIDTH, height = DEFAULT_HEIGHT) {
    this.width = width;
    this.height = height;
    this.seed = seed;
    this.rng = new Mulberry32(seed);
    this.psi = new Float32Array(width * height);
    this.nextPsi = new Float32Array(width * height);
    this.gravity = new Float32Array(width * height);
    this.light = new Float32Array(width * height);
    this.previous = new Float32Array(width * height);
    this.GK = buildGravityKernel(3);
    this.LK = buildLightKernel(4, 8);
    this.resetNu();
  }

  reset(seed = this.seed): void {
    this.seed = seed;
    this.rng = new Mulberry32(seed);
    this.frame = 0;
    this.lastClipRatio = 0;
    this.resetNu();
  }

  resetNu(): void {
    this.psi.fill(0);
    this.nextPsi.fill(0);
    this.gravity.fill(0);
    this.light.fill(0);
    this.previous.fill(0);
    this.lastClipRatio = 0;
    for (let i = 0; i < this.psi.length; i += 1) {
      this.psi[i] = this.rng.next() < 0.012 ? this.rng.next() * 0.35 : 0;
    }
  }

  step(params: DuatEngineParams, observer?: ActiveObserver | null): void {
    this.previous.set(this.psi);
    if (params.ruleMode === "conway") {
      this.stepConway(params, observer);
    } else {
      this.stepDuat(params, observer);
    }
    this.psi.set(this.nextPsi);
    this.frame += 1;
  }

  paint(x: number, y: number, radius: number, value: number): void {
    for (let dy = -radius; dy <= radius; dy += 1) {
      for (let dx = -radius; dx <= radius; dx += 1) {
        if (dx * dx + dy * dy > radius * radius) continue;
        this.psi[ix(x + dx, y + dy, this.width, this.height)] = clamp(value, 0, 1);
      }
    }
  }

  seedAtum(cx: number, cy: number): void {
    this.paint(cx, cy, 0, 1);
    for (let r = 1; r <= 3; r += 1) {
      for (let a = 0; a < 12; a += 1) {
        const dx = Math.round(Math.cos((a * Math.PI) / 6) * r);
        const dy = Math.round(Math.sin((a * Math.PI) / 6) * r);
        const id = ix(cx + dx, cy + dy, this.width, this.height);
        this.psi[id] = Math.max(this.psi[id], 0.55 * (1 - r / 4));
      }
    }
  }

  seedDuat(cx: number, cy: number): void {
    for (let i = 0; i < 42; i += 1) {
      const angle = (i / 42) * Math.PI * 2;
      const ring = i < 14 ? 6 : i < 28 ? 12 : 18;
      const x = Math.round(cx + Math.cos(angle) * ring);
      const y = Math.round(cy + Math.sin(angle) * ring * 0.62);
      this.psi[ix(x, y, this.width, this.height)] = 0.62 + this.rng.next() * 0.34;
    }
  }

  seedOsiris(cx: number, cy: number): void {
    for (let dy = -6; dy <= 6; dy += 1) {
      for (let dx = -6; dx <= 6; dx += 1) {
        const r = Math.sqrt(dx * dx + dy * dy);
        if (r > 6) continue;
        const value = Math.exp(-(r * r) / (2 * 2.35 * 2.35));
        const id = ix(cx + dx, cy + dy, this.width, this.height);
        this.psi[id] = Math.max(this.psi[id], value);
      }
    }
  }

  private stepDuat(params: DuatEngineParams, observer?: ActiveObserver | null): void {
    const mu = params.chi * 0.42 + 0.04;
    const ablation = params.ablationMode ?? "full";
    let clipped = 0;
    for (let y = 0; y < this.height; y += 1) {
      for (let x = 0; x < this.width; x += 1) {
        const id = ix(x, y, this.width, this.height);
        let g = 0;
        let l = 0;
        for (const cell of this.GK) g += this.psi[ix(x + cell.dx, y + cell.dy, this.width, this.height)] * cell.w;
        for (const cell of this.LK) l += this.psi[ix(x + cell.dx, y + cell.dy, this.width, this.height)] * cell.w;
        const effectiveG = ablation === "no-g" ? 0 : g;
        const effectiveL = ablation === "no-l" ? 0 : l;
        this.gravity[id] = effectiveG;
        this.light[id] = effectiveL;

        let obs = 0;
        if (observer && ablation !== "no-observer") {
          const dx = x - observer.x;
          const dy = y - observer.y;
          const d2 = dx * dx + dy * dy;
          if (d2 < 32) {
            const saturationGate = 1 - observer.profile.saturation * 0.45;
            obs = observer.strength * saturationGate * Math.exp(-d2 / 6);
          }
        }

        const growth = 2 * bell(effectiveG, mu, params.sigma) - 1;
        const sourceGate = clamp((effectiveG + effectiveL + this.psi[id]) * 2.8 + obs * 0.8, 0, 1);
        const capacity = 1 - this.psi[id];
        const growthTerm = growth >= 0 ? growth * sourceGate * capacity : growth * sourceGate * this.psi[id];
        const vacuumDrag = this.psi[id] * (1 - sourceGate) * 0.08;
        const lightCoupling = (params.chi - 0.5) * effectiveL * 0.55;
        const lightTerm = lightCoupling >= 0 ? lightCoupling * capacity : lightCoupling * this.psi[id];
        const observerTerm = obs * 0.28 * capacity;
        const rawNoise = ablation === "no-noise" ? 0 : this.rng.centered(params.noise);
        const negativeNoiseGate = clamp(this.psi[id] + sourceGate, 0, 1);
        const noise = rawNoise < 0 ? rawNoise * negativeNoiseGate : rawNoise;
        const raw = this.psi[id] + params.dt * (growthTerm - vacuumDrag + lightTerm + observerTerm) + noise;
        if (raw < 0 || raw > 1) clipped += 1;
        this.nextPsi[id] = clamp(raw, 0, 1);
      }
    }
    this.lastClipRatio = clipped / this.psi.length;
  }

  private stepConway(params: DuatEngineParams, observer?: ActiveObserver | null): void {
    this.lastClipRatio = 0;
    for (let y = 0; y < this.height; y += 1) {
      for (let x = 0; x < this.width; x += 1) {
        const id = ix(x, y, this.width, this.height);
        let live = 0;
        for (let dy = -1; dy <= 1; dy += 1) {
          for (let dx = -1; dx <= 1; dx += 1) {
            if (dx === 0 && dy === 0) continue;
            live += this.psi[ix(x + dx, y + dy, this.width, this.height)] > 0.5 ? 1 : 0;
          }
        }
        const alive = this.psi[id] > 0.5;
        let next = alive ? (live === 2 || live === 3 ? 1 : 0) : live === 3 ? 1 : 0;
        if (observer) {
          const dx = x - observer.x;
          const dy = y - observer.y;
          if (dx * dx + dy * dy < 16 && this.rng.next() < params.observerStrength * 0.08) {
            next = 1 - next;
          }
        }
        this.gravity[id] = live / 8;
        this.light[id] = Math.abs(live - 3) / 8;
        this.nextPsi[id] = next;
      }
    }
  }
}
