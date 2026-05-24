import type { PixelField } from "./pixelTypes";
import { getCell } from "./pixelField";

export function decayLight(field: PixelField, factor = 0.88): void {
  for (const cell of field.cells) {
    if (!Number.isFinite(cell.light)) cell.light = 0;
    cell.light = Math.max(0, Math.min(1, cell.light * factor));
    if (cell.material === "light" && cell.light < 0.05) {
      cell.material = "air";
      cell.active = false;
    }
  }
}

export function addRadialLight(field: PixelField, cx: number, cy: number, radius: number, intensity: number): void {
  const r = Math.max(1, radius);
  for (let y = Math.max(0, cy - r); y <= Math.min(field.height - 1, cy + r); y++) {
    for (let x = Math.max(0, cx - r); x <= Math.min(field.width - 1, cx + r); x++) {
      const d = Math.hypot(x - cx, y - cy);
      if (d > r) continue;
      const cell = getCell(field, x, y);
      if (!cell) continue;
      cell.light = Math.max(cell.light, Math.max(0, intensity * (1 - d / r)));
      cell.active = true;
    }
  }
}
