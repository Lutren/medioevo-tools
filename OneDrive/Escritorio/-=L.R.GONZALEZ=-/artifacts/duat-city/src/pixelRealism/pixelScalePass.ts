export function applyPixelScalePass(ctx: CanvasRenderingContext2D, pixelScale: number): void {
  ctx.imageSmoothingEnabled = false;
  if (pixelScale >= 3) {
    ctx.lineWidth = Math.max(1, Math.floor(pixelScale / 2));
  }
}
