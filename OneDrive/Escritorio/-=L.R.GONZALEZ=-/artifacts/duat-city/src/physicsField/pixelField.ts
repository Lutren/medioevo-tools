import type { PixelCell, PixelField, PixelMaterial } from "./pixelTypes";
import { makeCell } from "./materials";

export function createPixelField(width = 128, height = 72, fill: PixelMaterial = "air"): PixelField {
  return {
    width,
    height,
    tick: 0,
    cells: Array.from({ length: width * height }, () => makeCell(fill, false)),
    qPacked: new Uint8Array(width * height),
  };
}

export function fieldIndex(field: PixelField, x: number, y: number): number {
  return y * field.width + x;
}

export function inField(field: PixelField, x: number, y: number): boolean {
  return x >= 0 && y >= 0 && x < field.width && y < field.height;
}

export function getCell(field: PixelField, x: number, y: number): PixelCell | undefined {
  if (!inField(field, x, y)) return undefined;
  return field.cells[fieldIndex(field, x, y)];
}

export function setCell(field: PixelField, x: number, y: number, material: PixelMaterial, active = true): PixelField {
  if (!inField(field, x, y)) return field;
  const cells = field.cells.slice();
  cells[fieldIndex(field, x, y)] = makeCell(material, active);
  return { ...field, cells };
}

export function setCellMutable(field: PixelField, x: number, y: number, material: PixelMaterial, active = true): void {
  if (!inField(field, x, y)) return;
  field.cells[fieldIndex(field, x, y)] = makeCell(material, active);
}

export function swapCells(field: PixelField, ax: number, ay: number, bx: number, by: number): boolean {
  if (!inField(field, ax, ay) || !inField(field, bx, by)) return false;
  const ai = fieldIndex(field, ax, ay);
  const bi = fieldIndex(field, bx, by);
  const a = field.cells[ai];
  field.cells[ai] = { ...field.cells[bi], active: true };
  field.cells[bi] = { ...a, active: true };
  return true;
}

export function cloneField(field: PixelField): PixelField {
  return { ...field, cells: field.cells.map(cell => ({ ...cell })), qPacked: field.qPacked ? new Uint8Array(field.qPacked) : undefined };
}
