import type { PixelArtBitmap } from "./pixelArtGenerator";
import { generatePixelArtBitmap } from "./pixelArtGenerator";

export type ProceduralPropKind = "bronze_lamp_post" | "pipe_cluster" | "drainage_grate" | "archive_door" | "tube_meter";

export function generateProceduralProp(kind: ProceduralPropKind, seed = 1, styleProfile = "archeopunk_city_rain"): PixelArtBitmap {
  return generatePixelArtBitmap(12, 16, seed, styleProfile, `prop:${kind}`);
}
