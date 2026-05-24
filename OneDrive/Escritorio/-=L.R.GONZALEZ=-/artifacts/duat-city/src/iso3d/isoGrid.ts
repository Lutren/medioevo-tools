import type { IsoGridConfig, IsoVector2, IsoVector3, IsoWorldTile } from "./isoTypes";

export function createIsoGrid(width: number, height: number, tileWidth = 32, tileHeight = 16): IsoGridConfig {
  return {
    width: safeInt(width, 1),
    height: safeInt(height, 1),
    tileWidth: safeNumber(tileWidth, 32),
    tileHeight: safeNumber(tileHeight, 16),
    elevationScale: 10,
  };
}

export function gridToIsoWorld(grid: IsoVector2, config: IsoGridConfig, elevation = 0): IsoVector3 {
  const x = (safeNumber(grid.x, 0) - safeNumber(grid.y, 0)) * config.tileWidth * 0.5;
  const y = (safeNumber(grid.x, 0) + safeNumber(grid.y, 0)) * config.tileHeight * 0.5;
  const z = safeNumber(elevation, 0) * config.elevationScale;
  return { x: round(x), y: round(y), z: round(z) };
}

export function isoWorldToGrid(world: IsoVector3, config: IsoGridConfig): IsoVector2 {
  const a = safeNumber(world.x, 0) / (config.tileWidth * 0.5);
  const b = safeNumber(world.y, 0) / (config.tileHeight * 0.5);
  return { x: round((a + b) * 0.5), y: round((b - a) * 0.5) };
}

export function computeIsoDepth(position: IsoVector3): number {
  return round(safeNumber(position.y, 0) + safeNumber(position.z, 0) * 0.75 + safeNumber(position.x, 0) * 0.001);
}

export function sortIsoDepth<T extends { depth: number; id: string }>(items: T[]): T[] {
  return [...items].sort((a, b) => a.depth - b.depth || a.id.localeCompare(b.id));
}

export function createIsoWorldTile(input: Omit<IsoWorldTile, "world" | "depth">, config: IsoGridConfig): IsoWorldTile {
  const world = gridToIsoWorld(input.grid, config, input.elevation);
  return { ...input, world, depth: computeIsoDepth(world) };
}

function safeNumber(value: number, fallback: number): number {
  return Number.isFinite(value) ? value : fallback;
}

function safeInt(value: number, fallback: number): number {
  const number = Number.isFinite(value) ? Math.round(value) : fallback;
  return Math.max(1, number);
}

function round(value: number): number {
  return Number(value.toFixed(3));
}
