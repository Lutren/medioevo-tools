import type { CityState } from "../core/types";
import type { Camera } from "../render/camera";
import { TILE_SIZE, worldToScreen } from "../render/camera";

export function drawSelectionOutline(ctx: CanvasRenderingContext2D, state: CityState, cam: Camera, selectedId: string | null): void {
  if (!selectedId) return;
  const building = state.buildings.find(b => b.id === selectedId);
  if (!building) return;
  const ts = TILE_SIZE * cam.zoom;
  const { x, y } = worldToScreen(building.x, building.y, cam);
  ctx.save();
  ctx.strokeStyle = "rgba(255,255,255,0.92)";
  ctx.lineWidth = 2;
  ctx.setLineDash([4, 3]);
  ctx.strokeRect(x + ts * 0.16, y + ts * 0.02, ts * 0.68, ts * 0.74);
  ctx.restore();
}
