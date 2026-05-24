import type { TileType } from "../core/types";

export function materialForTile(type: TileType): "floor" | "solid" | "fluid" | "organic" | "anomaly" {
  if (type === "water") return "fluid";
  if (type === "forest" || type === "garden") return "organic";
  if (type === "stone" || type === "wall") return "solid";
  if (type === "ruin") return "anomaly";
  return "floor";
}

export function frictionForTile(type: TileType): number {
  switch (materialForTile(type)) {
    case "fluid": return 0.65;
    case "solid": return 1;
    case "organic": return 0.35;
    case "anomaly": return 0.55;
    default: return type === "road" ? 0.08 : 0.22;
  }
}
