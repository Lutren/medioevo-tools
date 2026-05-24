import type { AssetRef, AssetRequest, ReviewedAssetsManifestV12 } from "./assetTypes";
import { resolveAsset } from "./assetResolver";

export interface AssetAtlasV2 {
  schema: "duat.asset_atlas.v2";
  styleProfile: string;
  refs: Record<string, AssetRef>;
}

export function createAssetAtlasV2(requests: AssetRequest[], styleProfile = "archeopunk_city_rain", reviewed?: ReviewedAssetsManifestV12 | null): AssetAtlasV2 {
  const refs: Record<string, AssetRef> = {};
  for (const request of requests) {
    const ref = resolveAsset({ ...request, styleProfile: request.styleProfile ?? styleProfile }, reviewed);
    refs[ref.key] = ref;
  }
  return { schema: "duat.asset_atlas.v2", styleProfile, refs };
}

export function getAtlasRef(atlas: AssetAtlasV2, key: string): AssetRef {
  return atlas.refs[key] ?? {
    key,
    domain: "prop",
    mode: "fallback",
    fallbackKey: `procedural/${atlas.styleProfile}/${key}`,
    provenance: { publication_allowed: false, boundary: "PROCEDURAL_FALLBACK" },
  };
}
