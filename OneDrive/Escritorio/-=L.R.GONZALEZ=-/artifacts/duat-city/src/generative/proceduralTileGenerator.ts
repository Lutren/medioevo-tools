import type { PixelArtBitmap } from "./pixelArtGenerator";
import { generatePixelArtBitmap } from "./pixelArtGenerator";

export type ProceduralTileKind = "wet_street" | "canal_edge" | "bridge_segment" | "water" | "stone";

export function generateProceduralTile(kind: ProceduralTileKind, seed = 1, styleProfile = "wet_isometric_city"): PixelArtBitmap {
  const size = kind === "bridge_segment" ? 18 : 16;
  return generatePixelArtBitmap(size, 10, seed, styleProfile, `tile:${kind}`);
}
