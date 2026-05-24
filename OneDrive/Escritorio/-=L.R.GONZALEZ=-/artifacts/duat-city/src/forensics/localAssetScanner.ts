import path from "node:path";
import type { ForensicAssetRecord, ForensicManifest } from "./forensicTypes";
import { classifyForensicKind, classifyUsefulFor, finiteVisualScore, scoreIntegrationCandidate } from "./integrationCandidateScorer";

const SUPPORTED_EXTENSIONS = new Set([".png", ".jpg", ".jpeg", ".webp", ".svg", ".gif", ".aseprite", ".psd", ".json", ".atlas"]);

export function createAssetRecord(filePath: string, sizeBytes: number, sourceRoot: string): ForensicAssetRecord | null {
  const extension = path.extname(filePath).toLowerCase();
  if (!SUPPORTED_EXTENSIONS.has(extension)) return null;
  const usefulFor = classifyUsefulFor(filePath);
  const kind = classifyForensicKind(filePath);
  const score = scoreIntegrationCandidate({ path: filePath, extension, size: sizeBytes, kind, licenseKnown: false });
  return {
    path_original: filePath,
    original_path: filePath,
    filename: path.basename(filePath),
    extension: extension.replace(".", ""),
    size_bytes: sizeBytes,
    kind,
    visual_score: finiteVisualScore(sizeBytes, usefulFor),
    engine_use: usefulFor.filter(v => v !== "unknown").join(",") || "review",
    public_safe_guess: "review",
    license_status: "unknown",
    copy_recommendation: "review",
    source_zip_or_folder: sourceRoot,
    useful_for: usefulFor,
    risk: score.risk,
    copy_status: "not_copied",
    integration_recommendation: score.recommendation,
    notes: score.notes,
  };
}

export function buildAssetManifest(records: ForensicAssetRecord[], sourceRoot: string, generatedAt = new Date().toISOString()): ForensicManifest<ForensicAssetRecord> {
  return {
    schema: "duat/forensics/local-assets/v1.3",
    fingerprint: "DUAT-v1.3-GAME-OS-DISK-FORENSICS-LANGUAGE-CORTEX",
    generated_at: generatedAt,
    source_root: sourceRoot,
    records,
    boundary: {
      metadata_only: true,
      unknown_code_executed: false,
      publication_allowed: false,
      default_license_status: "unknown",
    },
  };
}
