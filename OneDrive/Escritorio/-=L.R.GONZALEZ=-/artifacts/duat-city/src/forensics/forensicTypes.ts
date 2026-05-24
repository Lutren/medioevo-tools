export type ForensicKind =
  | "ui_component"
  | "tile"
  | "building"
  | "prop"
  | "agent"
  | "material"
  | "scene_reference"
  | "light_effect"
  | "particle"
  | "glyph"
  | "audio"
  | "physics"
  | "light"
  | "brain_os"
  | "language"
  | "code"
  | "document"
  | "unknown";

export type UsefulFor =
  | "audio"
  | "physics"
  | "light"
  | "brain_os"
  | "language"
  | "agents"
  | "ui"
  | "rpg"
  | "assets"
  | "unknown";

export type IntegrationRecommendation =
  | "adopt"
  | "adapt"
  | "reference_only"
  | "reject"
  | "review_required";

export interface ForensicAssetRecord {
  path_original: string;
  original_path?: string;
  filename: string;
  extension: string;
  size_bytes: number;
  dimensions?: { width: number; height: number };
  kind: ForensicKind;
  visual_score: number;
  engine_use: string;
  public_safe_guess: "yes" | "no" | "review";
  license_status: "unknown" | "reviewed" | "blocked";
  copy_recommendation: "deny" | "review" | "internal_review_copy_candidate";
  source_zip_or_folder: string;
  useful_for: UsefulFor[];
  risk: "low" | "medium" | "high";
  copy_status: "not_copied" | "staged_metadata_only" | "copied_internal_review";
  integration_recommendation: IntegrationRecommendation;
  notes: string;
}

export interface ZipEntryRecord {
  path_original: string;
  filename: string;
  extension: string;
  size: number;
  compressed_size?: number;
  kind: ForensicKind;
  source_zip_or_folder: string;
  useful_for: UsefulFor[];
  risk: "low" | "medium" | "high";
  copy_status: "not_copied" | "staged_metadata_only";
  integration_recommendation: IntegrationRecommendation;
  notes: string;
}

export interface CodeCandidateRecord extends ZipEntryRecord {
  language: "typescript" | "javascript" | "json" | "markdown" | "css" | "html" | "unknown";
  exports_hint: string[];
  safe_to_execute: false;
}

export interface ForensicManifest<TRecord> {
  schema: string;
  fingerprint: "DUAT-v1.3-GAME-OS-DISK-FORENSICS-LANGUAGE-CORTEX";
  generated_at: string;
  source_root: string;
  records: TRecord[];
  boundary: {
    metadata_only: true;
    unknown_code_executed: false;
    publication_allowed: false;
    default_license_status: "unknown";
  };
}
