import type { CityState } from "../core/types";
import type { LightGrid, LightSource } from "./lightTypes";
import { setLightCell } from "./lightGrid";

export function applyTileOpacity(grid: LightGrid, state: CityState): void {
  for (const tile of state.tiles) {
    const x = Math.floor((tile.x / state.width) * grid.width);
    const y = Math.floor((tile.y / state.height) * grid.height);
    const opacity = opacityForTile(tile.type);
    if (opacity > 0) setLightCell(grid, x, y, { opacity });
  }
}

export function hasLineOcclusion(grid: LightGrid, x0: number, y0: number, x1: number, y1: number): number {
  const steps = Math.max(1, Math.ceil(Math.hypot(x1 - x0, y1 - y0)));
  let opacity = 0;
  for (let i = 1; i < steps; i++) {
    const t = i / steps;
    const x = Math.round(x0 + (x1 - x0) * t);
    const y = Math.round(y0 + (y1 - y0) * t);
    opacity += grid.cells[y * grid.width + x]?.opacity ?? 0;
    if (opacity >= 1.8) break;
  }
  return Math.min(1, opacity / 2);
}

export function softShadowFactor(grid: LightGrid, source: LightSource, x: number, y: number): number {
  const sx = Math.floor(source.x);
  const sy = Math.floor(source.y);
  const main = hasLineOcclusion(grid, sx, sy, x, y);
  const sideA = hasLineOcclusion(grid, sx + 1, sy, x, y);
  const sideB = hasLineOcclusion(grid, sx, sy + 1, x, y);
  return Math.max(0, 1 - (main * 0.62 + sideA * 0.2 + sideB * 0.18));
}

export function opacityForTile(type: string): number {
  if (["wall", "stone", "ruin"].includes(type)) return 0.82;
  if (["residential", "workshop", "archive", "clinic", "academy", "temple", "gatehouse"].includes(type)) return 0.64;
  if (type === "forest") return 0.32;
  if (type === "water" || type === "glass") return 0.16;
  return 0;
}
