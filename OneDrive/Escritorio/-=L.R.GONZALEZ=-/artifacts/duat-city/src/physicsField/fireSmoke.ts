import type { PixelField } from "./pixelTypes";
import { getCell, setCellMutable } from "./pixelField";
import { makeCell } from "./materials";
import { stepSmoke } from "./fluidLite";

export function stepFire(field: PixelField, x: number, y: number): boolean {
  let changed = false;
  for (const [dx, dy] of [[0, -1], [1, 0], [-1, 0], [0, 1]] as const) {
    const cell = getCell(field, x + dx, y + dy);
    if (!cell) continue;
    if (cell.material === "wood" && cell.wetness < 0.6) {
      setCellMutable(field, x + dx, y + dy, "fire", true);
      changed = true;
    }
    if (cell.material === "air" || cell.material === "empty") {
      const smoke = makeCell("smoke", true);
      smoke.temperature = 0.6;
      field.cells[(y + dy) * field.width + (x + dx)] = smoke;
      changed = true;
      break;
    }
  }
  const self = getCell(field, x, y);
  if (self) {
    self.light = Math.max(0, self.light * 0.9);
    self.temperature = Math.max(0.2, self.temperature - 0.03);
    if (self.temperature < 0.35 || (field.tick + x + y) % 17 === 0) {
      setCellMutable(field, x, y, "smoke", true);
      changed = true;
    }
  }
  return changed;
}

export function stepFireOrSmoke(field: PixelField, x: number, y: number): boolean {
  const cell = getCell(field, x, y);
  if (!cell) return false;
  if (cell.material === "fire") return stepFire(field, x, y);
  if (cell.material === "smoke") return stepSmoke(field, x, y);
  return false;
}
