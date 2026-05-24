export interface ReviewedAssetManifestEntry {
  id: string;
  filename: string;
  original_path: string;
  copied_path: string;
  intended_use: string;
  boundary: "INTERNAL_REVIEWED_ASSET";
  publication_allowed?: false;
  sha256: string;
  origin_sha256: string;
  sprite_ids: string[];
}

export interface ReviewedAssetsManifest {
  schema: "duat.reviewed-assets.v0.7";
  generated_at: string;
  boundary: "INTERNAL_REVIEWED_ASSET";
  publication_allowed: false;
  assets: ReviewedAssetManifestEntry[];
}

export function parseReviewedAssetsManifest(input: unknown): ReviewedAssetsManifest | null {
  if (!input || typeof input !== "object") return null;
  const manifest = input as ReviewedAssetsManifest;
  if (manifest.schema !== "duat.reviewed-assets.v0.7") return null;
  if (!Array.isArray(manifest.assets)) return null;
  return manifest;
}

export async function loadReviewedAssetsManifest(path = "/reviewed-assets/v0_7/REVIEWED_ASSETS_MANIFEST.json"): Promise<ReviewedAssetsManifest | null> {
  if (typeof fetch !== "function") return null;
  try {
    const response = await fetch(path, { cache: "no-store" });
    if (!response.ok) return null;
    return parseReviewedAssetsManifest(await response.json());
  } catch {
    return null;
  }
}
