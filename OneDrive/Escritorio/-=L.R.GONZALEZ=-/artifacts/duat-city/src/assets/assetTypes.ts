export type AssetDomain = "tile" | "building" | "prop" | "agent" | "material" | "ui" | "effect";
export type AssetMode = "reviewed" | "procedural" | "fallback";

export interface AssetRef {
  key: string;
  domain: AssetDomain;
  mode: AssetMode;
  path?: string;
  fallbackKey: string;
  provenance?: {
    original_path?: string;
    sha256?: string;
    publication_allowed: false;
    boundary: "INTERNAL_REVIEW_ONLY" | "PROCEDURAL_FALLBACK";
  };
}

export interface AssetRequest {
  domain: AssetDomain;
  type: string;
  styleProfile?: string;
}

export interface ReviewedAssetsManifestV12 {
  schema: "duat.reviewed_assets_manifest.v1_2";
  copied_count: number;
  publication_allowed: false;
  boundary: "INTERNAL_REVIEW_ONLY";
  assets: AssetRef[];
}
