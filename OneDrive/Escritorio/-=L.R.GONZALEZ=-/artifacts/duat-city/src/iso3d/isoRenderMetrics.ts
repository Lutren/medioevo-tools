import type { CityState } from "../core/types";
import type { IsoBillboard, IsoRenderMetrics } from "./isoTypes";
import { estimateIsoLightCells, estimateIsoMaterialCells } from "./isoWorld";

export function computeIsoRenderMetrics(
  state: CityState,
  billboards: IsoBillboard[],
  cacheHitRatio = 0,
): IsoRenderMetrics {
  const visibleSprites = billboards.length;
  const activeLightCells = estimateIsoLightCells(state);
  const activeMaterialCells = estimateIsoMaterialCells(state);
  const drawCallsEstimate = Math.max(1, Math.ceil(visibleSprites / 24) + 4);
  const avgFrameCostMs = clamp(4 + drawCallsEstimate * 0.35 + activeLightCells * 0.01 + activeMaterialCells * 0.006 - cacheHitRatio * 2, 1, 42);
  const p95FrameCostMs = clamp(avgFrameCostMs * 1.55, avgFrameCostMs, 60);
  const risk = clamp((p95FrameCostMs - 16) / 48 + activeLightCells / 2400, 0, 1);
  const phi = clamp(0.88 - risk * 0.42 + cacheHitRatio * 0.12, 0, 1);

  return {
    visibleSprites,
    drawCallsEstimate,
    activeLightCells,
    activeMaterialCells,
    cacheHitRatio: round(cacheHitRatio),
    avgFrameCostMs: round(avgFrameCostMs),
    p95FrameCostMs: round(p95FrameCostMs),
    R_iso: round(risk),
    Phi_iso: round(phi),
  };
}

function clamp(value: number, min: number, max: number): number {
  return Math.max(min, Math.min(max, Number.isFinite(value) ? value : min));
}

function round(value: number): number {
  return Number(value.toFixed(3));
}
