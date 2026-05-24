import type { PixelField } from "./pixelTypes";
import { cloneField, getCell } from "./pixelField";
import { stepDust, stepSmoke, stepWater } from "./fluidLite";
import { stepFire } from "./fireSmoke";
import { decayLight } from "./lightMatter";
import { computeFieldMetrics } from "./fieldMetrics";

export function stepPixelField(field: PixelField): { field: PixelField; metrics: ReturnType<typeof computeFieldMetrics> } {
  const next = cloneField({ ...field, tick: field.tick + 1 });
  let updatedCells = 0;
  let unresolvedField = 0;

  decayLight(next);

  for (let y = next.height - 1; y >= 0; y--) {
    for (let x = 0; x < next.width; x++) {
      const cell = getCell(next, x, y);
      if (!cell || !cell.active) continue;
      if (![cell.mass, cell.vx, cell.vy, cell.temperature, cell.pressure, cell.wetness, cell.light, cell.R, cell.Phi_eff].every(Number.isFinite)) {
        unresolvedField++;
        cell.active = false;
        continue;
      }
      let changed = false;
      if (cell.material === "water") changed = stepWater(next, x, y);
      else if (cell.material === "smoke") changed = stepSmoke(next, x, y);
      else if (cell.material === "dust") changed = stepDust(next, x, y);
      else if (cell.material === "fire") changed = stepFire(next, x, y);
      else if (cell.material === "light") cell.light = Math.max(0, cell.light - 0.04);

      if (changed) updatedCells++;
      else if (cell.material === "water" || cell.material === "dust" || cell.material === "smoke" || cell.material === "fire") unresolvedField++;
      cell.active = changed || cell.material === "fire" || cell.material === "smoke";
    }
  }

  const metrics = computeFieldMetrics(next, updatedCells, unresolvedField);
  applyCellQuaternaryPack(field, next);
  return { field: next, metrics };
}

function applyCellQuaternaryPack(previous: PixelField, next: PixelField): void {
  const packed = next.qPacked ?? new Uint8Array(next.width * next.height);
  const previousPacked = previous.qPacked;
  for (let i = 0; i < next.cells.length; i++) {
    const cell = next.cells[i];
    const prev = previous.cells[i];
    const presence = cell.material !== "air" && cell.material !== "empty" && (cell.active || cell.mass > 0 || cell.light > 0.01);
    const difference = Boolean(cell.active) || cell.material !== prev?.material || Math.abs((cell.light ?? 0) - (prev?.light ?? 0)) > 0.05;
    const q = !presence && !difference ? 0 : !presence && difference ? 1 : presence && !difference ? 2 : 3;
    const previousQ = previousPacked?.[i] ?? 0;
    const previousState = previousQ & 3;
    const previousDwell = previousQ >> 2;
    const dwell = previousState === q ? Math.min(63, previousDwell + 1) : 1;
    packed[i] = (dwell << 2) | q;
  }
  next.qPacked = packed;
}
