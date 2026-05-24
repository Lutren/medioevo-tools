export interface Vec2 {
  x: number;
  y: number;
}

export const vec = (x = 0, y = 0): Vec2 => ({ x: finite(x), y: finite(y) });
export const add = (a: Vec2, b: Vec2): Vec2 => vec(a.x + b.x, a.y + b.y);
export const sub = (a: Vec2, b: Vec2): Vec2 => vec(a.x - b.x, a.y - b.y);
export const scale = (a: Vec2, s: number): Vec2 => vec(a.x * finite(s), a.y * finite(s));
export const lenSq = (a: Vec2): number => finite(a.x * a.x + a.y * a.y);
export const len = (a: Vec2): number => Math.sqrt(lenSq(a));

export function finite(n: number, fallback = 0): number {
  return Number.isFinite(n) ? n : fallback;
}

export function clamp(n: number, min: number, max: number): number {
  return Math.max(min, Math.min(max, finite(n, min)));
}

export function clampDt(dt: number | undefined): number {
  return clamp(dt ?? 0.05, 0.01, 0.05);
}

export function normalize(a: Vec2): Vec2 {
  const l = len(a);
  if (l <= 1e-9) return vec(0, 0);
  return vec(a.x / l, a.y / l);
}

export function distance(a: Vec2, b: Vec2): number {
  return len(sub(a, b));
}
