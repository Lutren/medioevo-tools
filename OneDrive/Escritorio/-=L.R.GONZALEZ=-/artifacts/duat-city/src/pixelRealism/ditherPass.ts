import type { PixelRealismConfig } from "./renderPasses";

export function drawDitherPass(ctx: CanvasRenderingContext2D, config: PixelRealismConfig): void {
  if (!config.dither || config.qualityPreset === "DEBUG") return;
  ctx.save();
  ctx.globalCompositeOperation = "overlay";
  const step = Math.max(2, config.pixelScale * 2);
  for (let y = 0; y < ctx.canvas.height; y += step) {
    for (let x = (y / step) % 2 === 0 ? 0 : step; x < ctx.canvas.width; x += step * 2) {
      ctx.fillStyle = "rgba(255,255,255,0.025)";
      ctx.fillRect(x, y, step, step);
    }
  }
  ctx.restore();
}
