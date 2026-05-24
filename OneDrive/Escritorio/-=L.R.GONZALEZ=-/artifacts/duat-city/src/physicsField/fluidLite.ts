import type { PixelField } from "./pixelTypes";
import { getCell, inField, swapCells } from "./pixelField";
import { isSolid } from "./materials";

export function stepWater(field: PixelField, x: number, y: number): boolean {
  const below = getCell(field, x, y + 1);
  if (below && !isSolid(below.material) && below.material !== "water") {
    return swapCells(field, x, y, x, y + 1);
  }
  const dir = (field.tick + x + y) % 2 === 0 ? -1 : 1;
  for (const dx of [dir, -dir]) {
    const side = getCell(field, x + dx, y);
    if (side && !isSolid(side.material) && side.material !== "water") {
      return swapCells(field, x, y, x + dx, y);
    }
  }
  return false;
}

export function stepSmoke(field: PixelField, x: number, y: number): boolean {
  const above = getCell(field, x, y - 1);
  if (above && !isSolid(above.material) && above.material !== "smoke") {
    return swapCells(field, x, y, x, y - 1);
  }
  const dir = (field.tick + x) % 2 === 0 ? -1 : 1;
  const sideY = Math.max(0, y - 1);
  if (inField(field, x + dir, sideY)) {
    const side = getCell(field, x + dir, sideY);
    if (side && !isSolid(side.material) && side.material !== "smoke") {
      return swapCells(field, x, y, x + dir, sideY);
    }
  }
  return false;
}

export function stepDust(field: PixelField, x: number, y: number): boolean {
  const below = getCell(field, x, y + 1);
  if (below && !isSolid(below.material) && below.material !== "dust" && below.material !== "water") {
    return swapCells(field, x, y, x, y + 1);
  }
  return false;
}
