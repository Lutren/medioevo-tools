import type { AssetRef, AssetRequest, ReviewedAssetsManifestV12 } from "./assetTypes";
import { createDefaultAssetRegistry, createProceduralAssetRef } from "./assetRegistry";

export function resolveAsset(request: AssetRequest, reviewed?: ReviewedAssetsManifestV12 | null): AssetRef {
  const key = `${request.domain}/${request.type}`;
  const reviewedAsset = reviewed?.assets?.find(asset => asset.key === key && asset.provenance?.publication_allowed === false);
  if (reviewedAsset) return { ...reviewedAsset, mode: "reviewed" };
  const registry = createDefaultAssetRegistry(request.styleProfile);
  return registry[key] ?? createProceduralAssetRef(request.domain, request.type, request.styleProfile);
}

export function safeReviewedManifest(value: unknown): ReviewedAssetsManifestV12 {
  const manifest = value as ReviewedAssetsManifestV12;
  if (!manifest || manifest.schema !== "duat.reviewed_assets_manifest.v1_2" || !Array.isArray(manifest.assets)) {
    return { schema: "duat.reviewed_assets_manifest.v1_2", copied_count: 0, publication_allowed: false, boundary: "INTERNAL_REVIEW_ONLY", assets: [] };
  }
  return { ...manifest, publication_allowed: false, boundary: "INTERNAL_REVIEW_ONLY" };
}
