import type { CityState } from "../core/types";
import type { Camera } from "../render/camera";
import { worldToScreen, TILE_SIZE } from "../render/camera";
import type { PixelRealismConfig } from "./renderPasses";

export function drawReflectionPass(ctx: CanvasRenderingContext2D, state: CityState, cam: Camera, config: PixelRealismConfig): void {
  if (config.qualityPreset === "LOW") return;
  const ts = TILE_SIZE * cam.zoom;
  ctx.save();
  ctx.globalCompositeOperation = "screen";
  for (const tile of state.tiles) {
    if (tile.type !== "water" && !(config.weather === "rain" && tile.type === "road")) continue;
    const { x, y } = worldToScreen(tile.x, tile.y, cam);
    if (x < -ts || y < -ts || x > ctx.canvas.width + ts || y > ctx.canvas.height + ts) continue;
    const alpha = tile.type === "water" ? 0.28 : 0.12;
    ctx.fillStyle = `rgba(91, 209, 255, ${alpha})`;
    ctx.fillRect(x + ts * 0.18, y + ts * 0.42, ts * 0.64, Math.max(1, ts * 0.10));
    ctx.fillStyle = `rgba(255, 180, 88, ${alpha * 0.55})`;
    ctx.fillRect(x + ts * 0.34, y + ts * 0.50, ts * 0.32, Math.max(1, ts * 0.05));
  }
  ctx.restore();
}
