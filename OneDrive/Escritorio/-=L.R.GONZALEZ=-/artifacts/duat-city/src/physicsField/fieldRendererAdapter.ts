import type { CityState, TileType } from "../core/types";
import type { PixelField, PixelMaterial } from "./pixelTypes";
import { createPixelField, setCellMutable } from "./pixelField";
import { addRadialLight } from "./lightMatter";
import { stepPixelField } from "./cellularPhysics";
import { summarizeField } from "./fieldMetrics";

export function tileTypeToMaterial(type: TileType): PixelMaterial {
  switch (type) {
    case "water": return "water";
    case "forest": return "wood";
    case "stone":
    case "wall":
      return "stone";
    case "road":
    case "plaza":
      return "soil";
    case "garden":
      return "soil";
    case "ruin":
      return "dust";
    default:
      return "air";
  }
}

export function cityToPixelField(state: CityState, width = 64, height = 36): PixelField {
  const field = createPixelField(width, height, "air");
  for (const tile of state.tiles) {
    const fx = Math.min(width - 1, Math.max(0, Math.floor((tile.x / state.width) * width)));
    const fy = Math.min(height - 1, Math.max(0, Math.floor((tile.y / state.height) * height)));
    const material = tileTypeToMaterial(tile.type);
    if (material !== "air") setCellMutable(field, fx, fy, material, tile.type === "water" || tile.type === "ruin");
    if (tile.fibmob.polarity === "void") setCellMutable(field, fx, fy, "dust", true);
  }
  for (const building of state.buildings) {
    const fx = Math.min(width - 1, Math.max(0, Math.floor((building.x / state.width) * width)));
    const fy = Math.min(height - 1, Math.max(0, Math.floor((building.y / state.height) * height)));
    if (building.gate === "BLOCK") setCellMutable(field, fx, fy, "smoke", true);
    if (building.type === "market" || building.type === "clinic" || building.type === "observatory" || building.type === "temple" || building.type === "theater") {
      addRadialLight(field, fx, fy, 5, building.Phi_eff);
    }
  }
  for (const agent of state.agents) {
    const fx = Math.min(width - 1, Math.max(0, Math.floor((agent.x / state.width) * width)));
    const fy = Math.min(height - 1, Math.max(0, Math.floor((agent.y / state.height) * height)));
    setCellMutable(field, fx, fy, "agent", false);
  }
  return field;
}

export function stepCityField(state: CityState): Pick<CityState, "fieldMetrics" | "fieldSummary"> {
  const result = stepPixelField(cityToPixelField(state));
  return {
    fieldMetrics: result.metrics,
    fieldSummary: summarizeField(result.field, result.metrics),
  };
}
