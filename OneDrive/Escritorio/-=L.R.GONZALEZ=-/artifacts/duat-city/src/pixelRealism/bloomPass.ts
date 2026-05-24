import type { CityState } from "../core/types";
import type { Camera } from "../render/camera";
import { TILE_SIZE, worldToScreen } from "../render/camera";
import type { PixelRealismConfig } from "./renderPasses";

export function drawBloomPass(ctx: CanvasRenderingContext2D, state: CityState, cam: Camera, config: PixelRealismConfig): void {
  if (config.bloomAmount <= 0 || config.qualityPreset === "LOW" || config.qualityPreset === "DEBUG") return;
  const ts = TILE_SIZE * cam.zoom;
  ctx.save();
  ctx.globalCompositeOperation = "lighter";
  for (const building of state.buildings) {
    const luminous = ["market", "observatory", "archive", "clinic", "temple", "gatehouse", "ruin"].includes(building.type);
    if (!luminous) continue;
    const { x, y } = worldToScreen(building.x, building.y, cam);
    const radius = ts * (building.type === "ruin" ? 1.1 : 0.85);
    const gradient = ctx.createRadialGradient(x + ts / 2, y + ts / 2, 0, x + ts / 2, y + ts / 2, radius);
    const color = building.type === "market" ? "34, 232, 255" : building.type === "ruin" ? "167, 92, 255" : "255, 184, 94";
    gradient.addColorStop(0, `rgba(${color}, ${0.24 * config.bloomAmount})`);
    gradient.addColorStop(1, `rgba(${color}, 0)`);
    ctx.fillStyle = gradient;
    ctx.fillRect(x - radius, y - radius, radius * 2 + ts, radius * 2 + ts);
  }
  ctx.restore();
}
