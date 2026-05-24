export interface ShadowInput {
  tick: number;
  hour?: number;
  height?: number;
}

export function shadowDirection(input: ShadowInput): { x: number; y: number; alpha: number } {
  const hour = input.hour ?? ((input.tick / 4) % 24);
  const angle = ((hour / 24) * Math.PI * 2) - Math.PI / 2;
  const length = 0.35 + Math.max(0, Math.cos(angle)) * 0.65;
  return {
    x: Math.cos(angle) * length * (input.height ?? 1),
    y: Math.sin(angle) * length * 0.45 * (input.height ?? 1),
    alpha: Math.max(0.08, Math.min(0.32, 0.22 + Math.sin(angle) * 0.08)),
  };
}

export function drawBlobShadow(ctx: CanvasRenderingContext2D, cx: number, cy: number, rx: number, ry: number, alpha = 0.25): void {
  ctx.save();
  ctx.fillStyle = `rgba(0,0,0,${alpha})`;
  ctx.beginPath();
  ctx.ellipse(cx, cy, rx, ry, 0, 0, Math.PI * 2);
  ctx.fill();
  ctx.restore();
}
