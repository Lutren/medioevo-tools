import type { FieldMetrics, PixelField, PhysicsFieldSummary } from "./pixelTypes";
import { EMPTY_FIELD_METRICS } from "./pixelTypes";

export function computeFieldMetrics(field: PixelField, updatedCells: number, unresolvedField: number): FieldMetrics {
  let activeCells = 0;
  let heat = 0;
  let pressure = 0;
  for (const cell of field.cells) {
    if (cell.active) activeCells++;
    heat += Number.isFinite(cell.temperature) ? cell.temperature : 1;
    pressure += Number.isFinite(cell.pressure) ? cell.pressure : 1;
  }
  const total = Math.max(1, field.cells.length);
  const activeRatio = activeCells / total;
  const unresolvedRatio = unresolvedField / Math.max(1, activeCells);
  const pressureNorm = Math.min(1, pressure / total);
  const heatNorm = Math.min(1, heat / total);
  const R_field = clamp01(0.45 * unresolvedRatio + 0.25 * activeRatio + 0.15 * pressureNorm + 0.15 * heatNorm);
  const Phi_field = clamp01(1 - R_field + 0.25 * (updatedCells / Math.max(1, activeCells)));
  return {
    activeCells,
    updatedCells,
    skippedCells: Math.max(0, total - updatedCells),
    heat: heatNorm,
    pressure: pressureNorm,
    unresolvedField,
    R_field,
    Phi_field,
  };
}

export function summarizeField(field: PixelField, metrics: FieldMetrics = EMPTY_FIELD_METRICS): PhysicsFieldSummary {
  const counts: Record<string, number> = {};
  const hazards: string[] = [];
  for (const cell of field.cells) counts[cell.material] = (counts[cell.material] ?? 0) + 1;
  if ((counts.fire ?? 0) > 0) hazards.push("fire");
  if ((counts.water ?? 0) > field.width) hazards.push("flooding");
  if ((counts.smoke ?? 0) > field.width * 0.5) hazards.push("smoke");
  return {
    resolution: `${field.width}x${field.height}`,
    dominant_materials: counts,
    hazards,
    R_field: metrics.R_field,
    Phi_field: metrics.Phi_field,
  };
}

function clamp01(value: number): number {
  if (!Number.isFinite(value)) return 1;
  return Math.max(0, Math.min(1, value));
}
