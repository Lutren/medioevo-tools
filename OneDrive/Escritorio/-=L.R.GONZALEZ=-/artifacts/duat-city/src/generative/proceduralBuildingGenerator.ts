import type { PixelArtBitmap } from "./pixelArtGenerator";
import { generatePixelArtBitmap } from "./pixelArtGenerator";

export type ProceduralBuildingKind = "archive" | "forge" | "garden" | "market" | "theater" | "rooftop_module" | "wall_facade";

export function generateProceduralBuilding(kind: ProceduralBuildingKind, seed = 1, styleProfile = "archeopunk_city_rain"): PixelArtBitmap {
  const height = kind === "rooftop_module" ? 14 : 24;
  return generatePixelArtBitmap(20, height, seed, styleProfile, `building:${kind}`);
}
