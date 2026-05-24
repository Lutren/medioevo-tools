export interface AssetManifestEntryV12 {
  id: string;
  original_path: string;
  filename: string;
  extension: string;
  size_bytes: number;
  dimensions?: { width: number; height: number } | null;
  kind: string;
  visual_score: number;
  engine_use: string;
  public_safe_guess: "yes" | "no" | "review";
  license_status: "unknown" | "reviewed" | "blocked";
  copy_recommendation: "deny" | "review" | "internal_review_copy_candidate";
  notes: string;
}

export interface AssetManifestV12 {
  schema: "duat.asset_manifest.v1_2";
  source_root: string;
  generated_at: string;
  scan_mode: "metadata_read_only";
  publication_allowed: false;
  asset_count: number;
  copied_count: number;
  assets: AssetManifestEntryV12[];
}

export interface DuatStyleTokens {
  schema: "duat.style_tokens.v1_2";
  generatedAt: string;
  paletteTokens: string[];
  contrastProfile: "low" | "medium" | "high";
  edgeDetailDensity: number;
  metalCopperObsidianCyanAmberRatios: Record<string, number>;
  glowColorTendencies: string[];
  uiFrameStyle: string;
  materialCategories: string[];
  sceneMoodTags: string[];
  lightDirectionTags: string[];
  proportions: {
    tile: string;
    building: string;
    prop: string;
  };
  sourceAssetCount: number;
  publicationAllowed: false;
}

export interface StyleProfile {
  id: string;
  palette: string[];
  moodTags: string[];
  lightTags: string[];
  materialBias: string[];
  proceduralSeed: number;
}
