import type { CityState } from "../core/types";
import type { GraphicsBudget, GraphicsMetrics } from "../graphics/types";
import type { PhysicsMetrics } from "../physics/types";
import type { Camera } from "./camera";
import type { LODState } from "./lod-controller";
import { renderCity, type RenderOptions } from "./canvasRenderer";

export function renderCityFrame(
  ctx: CanvasRenderingContext2D,
  state: CityState,
  camera: Camera,
  lod: LODState,
  graphicsBudget: GraphicsBudget | undefined,
  physicsMetrics: PhysicsMetrics | undefined,
  opts: RenderOptions,
): void {
  renderCity(ctx, state, camera, lod, { ...opts, graphicsBudget, physicsMetrics });
}

export function renderDebugOverlay(
  ctx: CanvasRenderingContext2D,
  metrics: { physics?: PhysicsMetrics; graphics?: GraphicsMetrics },
): void {
  ctx.save();
  ctx.fillStyle = "rgba(10,14,20,0.82)";
  ctx.fillRect(8, 8, 190, 54);
  ctx.fillStyle = "#c9d1d9";
  ctx.font = "10px monospace";
  ctx.fillText(`R_phys ${metrics.physics?.R_physics.toFixed(3) ?? "n/a"}`, 16, 25);
  ctx.fillText(`Phi_phys ${metrics.physics?.Phi_physics.toFixed(3) ?? "n/a"}`, 16, 39);
  ctx.fillText(`R_graph ${metrics.graphics?.R_graphics.toFixed(3) ?? "n/a"}`, 16, 53);
  ctx.restore();
}
