import { createAssetAtlasV2 } from "./assetAtlasV2";

export function createTileAtlas(styleProfile = "wet_isometric_city") {
  return createAssetAtlasV2([
    { domain: "tile", type: "wet_street" },
    { domain: "tile", type: "canal_edge" },
    { domain: "tile", type: "bridge_segment" },
    { domain: "tile", type: "water" },
  ], styleProfile);
}
