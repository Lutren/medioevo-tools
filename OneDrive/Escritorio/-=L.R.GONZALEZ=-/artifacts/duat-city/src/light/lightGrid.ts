import type { RGB } from "../color/colorTypes";
import { clamp01, mixRgb, safeRgb } from "../color/colorSpace";
import type { LightCell, LightGrid, LightSource } from "./lightTypes";
import { EMPTY_LIGHT_CELL } from "./lightTypes";

export function createLightGrid(width = 160, height = 90, ambient: RGB = { r: 18, g: 24, b: 34 }): LightGrid {
  const cell: LightCell = { ...EMPTY_LIGHT_CELL, r: ambient.r / 255, g: ambient.g / 255, b: ambient.b / 255, intensity: luminance(ambient) };
  return {
    width,
    height,
    cells: Array.from({ length: width * height }, () => ({ ...cell, emission: { ...cell.emission } })),
    ambient: safeRgb(ambient),
    sources: [],
    bouncePasses: 0,
  };
}

export function lightIndex(grid: LightGrid, x: number, y: number): number {
  return y * grid.width + x;
}

export function getLightCell(grid: LightGrid, x: number, y: number): LightCell | undefined {
  if (x < 0 || y < 0 || x >= grid.width || y >= grid.height) return undefined;
  return grid.cells[lightIndex(grid, x, y)];
}

export function setLightCell(grid: LightGrid, x: number, y: number, patch: Partial<LightCell>): void {
  const cell = getLightCell(grid, x, y);
  if (!cell) return;
  Object.assign(cell, patch);
  cell.intensity = clamp01(cell.intensity);
  cell.r = clamp01(cell.r);
  cell.g = clamp01(cell.g);
  cell.b = clamp01(cell.b);
  cell.opacity = clamp01(cell.opacity);
  cell.reflectance = clamp01(cell.reflectance);
  cell.scatter = clamp01(cell.scatter);
  cell.dirty = true;
}

export function addLightSource(grid: LightGrid, source: LightSource): LightGrid {
  grid.sources.push(source);
  return grid;
}

export function accumulateCellLight(cell: LightCell, color: RGB, intensity: number): void {
  const k = clamp01(intensity);
  const mixed = mixRgb({ r: cell.r * 255, g: cell.g * 255, b: cell.b * 255 }, color, k);
  cell.r = clamp01(mixed.r / 255);
  cell.g = clamp01(mixed.g / 255);
  cell.b = clamp01(mixed.b / 255);
  cell.intensity = clamp01(cell.intensity + k * (1 - cell.opacity));
  cell.dirty = true;
}

export function luminance(rgb: RGB): number {
  return clamp01((0.2126 * rgb.r + 0.7152 * rgb.g + 0.0722 * rgb.b) / 255);
}
