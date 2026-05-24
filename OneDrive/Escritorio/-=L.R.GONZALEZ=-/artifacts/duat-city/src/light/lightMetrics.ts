import type { LightGrid, LightMetrics } from "./lightTypes";

export function computeLightMetrics(grid: LightGrid): LightMetrics {
  let activeLightCells = 0;
  let blockedCells = 0;
  let emittedCells = 0;
  let reflectedCells = 0;
  let finite = true;
  for (const cell of grid.cells) {
    if (!Number.isFinite(cell.r) || !Number.isFinite(cell.g) || !Number.isFinite(cell.b) || !Number.isFinite(cell.intensity)) finite = false;
    if (cell.intensity > 0.08) activeLightCells++;
    if (cell.opacity > 0.5) blockedCells++;
    if (cell.emission.r + cell.emission.g + cell.emission.b > 0) emittedCells++;
    if (cell.reflectance > 0.2) reflectedCells++;
  }
  const activeRatio = activeLightCells / Math.max(1, grid.cells.length);
  const tooActive = Math.max(0, activeRatio - 0.72);
  const blockedRatio = blockedCells / Math.max(1, grid.cells.length);
  const R_light = finite ? Math.min(1, tooActive * 1.6 + blockedRatio * 0.18 + (grid.bouncePasses > 6 ? 0.08 : 0)) : 1;
  const Phi_light = Math.max(0, Math.min(1, 1 - R_light + Math.min(0.12, reflectedCells / Math.max(1, activeLightCells) * 0.12)));
  return { activeLightCells, blockedCells, emittedCells, reflectedCells, R_light, Phi_light, finite };
}

export function sampleGridLight(grid: LightGrid, xNorm: number, yNorm: number): { r: number; g: number; b: number; intensity: number; reflectance: number; scatter: number } {
  const x = Math.max(0, Math.min(grid.width - 1, Math.floor(xNorm * grid.width)));
  const y = Math.max(0, Math.min(grid.height - 1, Math.floor(yNorm * grid.height)));
  const cell = grid.cells[y * grid.width + x];
  return {
    r: Math.max(0, Math.min(1, cell?.r ?? 0)),
    g: Math.max(0, Math.min(1, cell?.g ?? 0)),
    b: Math.max(0, Math.min(1, cell?.b ?? 0)),
    intensity: Math.max(0, Math.min(1, cell?.intensity ?? 0)),
    reflectance: Math.max(0, Math.min(1, cell?.reflectance ?? 0)),
    scatter: Math.max(0, Math.min(1, cell?.scatter ?? 0)),
  };
}
