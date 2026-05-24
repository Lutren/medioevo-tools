export function sdfCircle(px: number, py: number, cx: number, cy: number, radius: number): number {
  return Math.hypot(px - cx, py - cy) - radius;
}

export function sdfBox(px: number, py: number, cx: number, cy: number, hx: number, hy: number): number {
  const dx = Math.abs(px - cx) - hx;
  const dy = Math.abs(py - cy) - hy;
  return Math.hypot(Math.max(dx, 0), Math.max(dy, 0)) + Math.min(Math.max(dx, dy), 0);
}

export function smoothMin(a: number, b: number, k: number): number {
  const h = Math.max(0, Math.min(1, 0.5 + 0.5 * (b - a) / k));
  return b * (1 - h) + a * h - k * h * (1 - h);
}

export function emlBlendDistance(distance: number, R: number): number {
  const y = Math.max(1e-6, Math.abs(distance) + 1);
  return Math.exp(Math.min(6, 1 - R)) - Math.log(y);
}
