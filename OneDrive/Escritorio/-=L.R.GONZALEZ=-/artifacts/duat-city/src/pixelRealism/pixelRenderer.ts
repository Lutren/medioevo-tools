import type { CityState } from "../core/types";
import type { Camera } from "../render/camera";
import type { PixelRealismRuntime } from "./pixelRealismMetrics";
import { applyPixelScalePass } from "./pixelScalePass";
import { drawAtmospherePass } from "./atmospherePass";
import { drawReflectionPass } from "./reflectionPass";
import { drawBloomPass } from "./bloomPass";
import { drawDitherPass } from "./ditherPass";
import { drawSelectionOutline } from "./outlinePass";
import { shouldRunReflectionPass } from "./renderBudget";

export interface PixelRendererOptions {
  runtime: PixelRealismRuntime;
  selectedId: string | null;
  debug?: boolean;
}

export function beginPixelRealismFrame(ctx: CanvasRenderingContext2D, runtime: PixelRealismRuntime): void {
  applyPixelScalePass(ctx, runtime.config.pixelScale);
  if (runtime.config.timeOfDay === "night") {
    ctx.fillStyle = "#070c17";
    ctx.fillRect(0, 0, ctx.canvas.width, ctx.canvas.height);
  }
}

export function finishPixelRealismFrame(ctx: CanvasRenderingContext2D, state: CityState, cam: Camera, options: PixelRendererOptions): void {
  const { runtime } = options;
  if (runtime.quality.reflections && shouldRunReflectionPass(state, runtime.config)) drawReflectionPass(ctx, state, cam, runtime.config);
  if (runtime.quality.fog) drawAtmospherePass(ctx, state, runtime.config);
  if (runtime.quality.bloom) drawBloomPass(ctx, state, cam, runtime.config);
  drawDitherPass(ctx, runtime.config);
  drawSelectionOutline(ctx, state, cam, options.selectedId);
  if (runtime.config.qualityPreset === "DEBUG" || options.debug) drawDebugOverlays(ctx, runtime);
}

export function drawDebugOverlays(ctx: CanvasRenderingContext2D, runtime: PixelRealismRuntime): void {
  ctx.save();
  const gx = Math.max(8, Math.floor(ctx.canvas.width / 16));
  const gy = Math.max(8, Math.floor(ctx.canvas.height / 10));
  ctx.strokeStyle = "rgba(34, 232, 255, 0.18)";
  ctx.lineWidth = 1;
  for (let x = 0; x < ctx.canvas.width; x += gx) {
    ctx.beginPath();
    ctx.moveTo(x, 0);
    ctx.lineTo(x, ctx.canvas.height);
    ctx.stroke();
  }
  for (let y = 0; y < ctx.canvas.height; y += gy) {
    ctx.beginPath();
    ctx.moveTo(0, y);
    ctx.lineTo(ctx.canvas.width, y);
    ctx.stroke();
  }
  ctx.fillStyle = "rgba(5, 10, 18, 0.82)";
  ctx.fillRect(10, 64, 210, 72);
  ctx.fillStyle = "#9ee7ff";
  ctx.font = "10px monospace";
  ctx.fillText(`Pixel Realism ${runtime.config.qualityPreset}`, 18, 82);
  ctx.fillText(`light cells ${runtime.metrics.activeLightCells}`, 18, 98);
  ctx.fillText(`R_light ${runtime.metrics.R_light.toFixed(3)}`, 18, 114);
  ctx.fillText(`Q ${JSON.stringify(runtime.metrics.qStateCounts)}`, 18, 130);
  ctx.restore();
}
