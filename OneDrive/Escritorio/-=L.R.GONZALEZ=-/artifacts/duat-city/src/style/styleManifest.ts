import type { AssetManifestV12, DuatStyleTokens } from "./styleTypes";
import { analyzeStyleFromManifest } from "./styleAnalyzer";
import { DEFAULT_DUAT_STYLE_TOKENS, mergeStyleTokens } from "./styleTokens";

export function parseAssetManifestV12(value: unknown): AssetManifestV12 {
  const manifest = value as AssetManifestV12;
  if (!manifest || manifest.schema !== "duat.asset_manifest.v1_2" || !Array.isArray(manifest.assets)) {
    return {
      schema: "duat.asset_manifest.v1_2",
      source_root: "",
      generated_at: "fallback",
      scan_mode: "metadata_read_only",
      publication_allowed: false,
      asset_count: 0,
      copied_count: 0,
      assets: [],
    };
  }
  return { ...manifest, publication_allowed: false };
}

export function createStyleManifest(value: unknown): DuatStyleTokens {
  const manifest = parseAssetManifestV12(value);
  return manifest.assets.length > 0 ? analyzeStyleFromManifest(manifest) : DEFAULT_DUAT_STYLE_TOKENS;
}

export function validateStyleTokens(value: unknown): DuatStyleTokens {
  const tokens = value as Partial<DuatStyleTokens>;
  return mergeStyleTokens(tokens ?? {});
}
