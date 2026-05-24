import type { CityState } from "../core/types";
import type { LightGrid } from "./lightTypes";
import { accumulateCellLight, getLightCell, setLightCell } from "./lightGrid";

export function applyWaterReflection(grid: LightGrid, state: CityState): number {
  let reflected = 0;
  for (const tile of state.tiles) {
    if (tile.type !== "water" && tile.type !== "road") continue;
    const wet = tile.type === "water" ? 0.75 : 0.16;
    const x = Math.floor((tile.x / state.width) * grid.width);
    const y = Math.floor((tile.y / state.height) * grid.height);
    const cell = getLightCell(grid, x, y);
    const above = getLightCell(grid, x, Math.max(0, y - 2));
    if (!cell || !above || above.intensity <= 0.05) continue;
    accumulateCellLight(cell, { r: above.r * 255, g: above.g * 255, b: above.b * 255 }, above.intensity * wet * 0.34);
    setLightCell(grid, x, y, { reflectance: Math.max(cell.reflectance, wet) });
    reflected++;
  }
  const scene = state.playableScene;
  if (scene) {
    for (const placed of scene.materials) {
      if (placed.material !== "water" && placed.wetness <= 0.35 && placed.material !== "neon") continue;
      const wet = placed.material === "water" ? 0.82 : Math.max(0.2, placed.wetness);
      const x = Math.floor((placed.x / state.width) * grid.width);
      const y = Math.floor((placed.y / state.height) * grid.height);
      const cell = getLightCell(grid, x, y);
      const above = getLightCell(grid, x, Math.max(0, y - 2));
      if (!cell || !above || above.intensity <= 0.04) continue;
      accumulateCellLight(cell, { r: above.r * 255, g: above.g * 255, b: above.b * 255 }, above.intensity * wet * 0.42);
      setLightCell(grid, x, y, { reflectance: Math.max(cell.reflectance, wet) });
      reflected++;
    }
  }
  return reflected;
}
