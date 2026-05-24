export function clamp(v: number, min: number, max: number): number {
  return Math.max(min, Math.min(max, v));
}

export function lerp(a: number, b: number, t: number): number {
  return a + (b - a) * clamp(t, 0, 1);
}

export function dist(x1: number, y1: number, x2: number, y2: number): number {
  const dx = x2 - x1, dy = y2 - y1;
  return Math.sqrt(dx * dx + dy * dy);
}

export type RandomSource = () => number;

function hashSeed(seed: string | number): number {
  const text = String(seed);
  let h = 2166136261;
  for (let i = 0; i < text.length; i++) {
    h ^= text.charCodeAt(i);
    h = Math.imul(h, 16777619);
  }
  return h >>> 0;
}

export function seededRandom(seed: string | number): RandomSource {
  let t = hashSeed(seed);
  return () => {
    t += 0x6D2B79F5;
    let r = Math.imul(t ^ (t >>> 15), 1 | t);
    r ^= r + Math.imul(r ^ (r >>> 7), 61 | r);
    return ((r ^ (r >>> 14)) >>> 0) / 4294967296;
  };
}

const defaultRandom = seededRandom("duat-city-default-rng");

export function randBetween(min: number, max: number, rng: RandomSource = defaultRandom): number {
  return min + rng() * (max - min);
}

export function randInt(min: number, max: number, rng: RandomSource = defaultRandom): number {
  return Math.floor(randBetween(min, max + 1, rng));
}

export function pick<T>(arr: T[], rng: RandomSource = defaultRandom): T {
  if (arr.length === 0) throw new Error("pick_requires_non_empty_array");
  return arr[Math.floor(rng() * arr.length)];
}

export function uid(rng: RandomSource = defaultRandom): string {
  return Math.floor(rng() * 0xffffffff)
    .toString(36)
    .padStart(7, "0")
    .slice(0, 8);
}

export function formatNum(n: number, decimals = 3): string {
  return n.toFixed(decimals);
}
