import { mobiusField } from "../core/fibmob";
import type { Tile } from "../core/types";

export interface FibMobVisual {
  rarity: number;
  colorShift: number;
  anomaly: boolean;
  saturation: number;
}

export function fibMobVisualForTile(tile: Tile, k = 1): FibMobVisual {
  const field = mobiusField(tile.id + 1, k);
  return {
    rarity: field.rarity,
    colorShift: field.mu === 0 ? -0.15 : field.mu > 0 ? 0.08 : 0.02,
    anomaly: tile.type === "ruin" || field.mu === 0,
    saturation: field.mu === 0 ? 0.35 : Math.min(0.2, Math.abs(field.mu) * 0.05),
  };
}
