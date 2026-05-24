import path from "node:path";
import type { ForensicManifest, ZipEntryRecord } from "./forensicTypes";
import { classifyForensicKind, classifyUsefulFor, scoreIntegrationCandidate } from "./integrationCandidateScorer";

export interface RawZipEntry {
  path: string;
  size: number;
  compressedSize?: number;
}

export function createZipEntryRecord(entry: RawZipEntry, sourceZip: string): ZipEntryRecord {
  const extension = path.extname(entry.path).toLowerCase();
  const kind = classifyForensicKind(entry.path);
  const score = scoreIntegrationCandidate({ path: entry.path, extension, size: entry.size, kind, licenseKnown: false });
  return {
    path_original: entry.path,
    filename: path.basename(entry.path),
    extension: extension.replace(".", ""),
    size: entry.size,
    compressed_size: entry.compressedSize,
    kind,
    source_zip_or_folder: sourceZip,
    useful_for: classifyUsefulFor(entry.path),
    risk: score.risk,
    copy_status: "staged_metadata_only",
    integration_recommendation: score.recommendation,
    notes: `${score.notes} Unknown zip code is never executed by DUAT v1.3.`,
  };
}

export function buildZipManifest(records: ZipEntryRecord[], sourceZip: string, generatedAt = new Date().toISOString()): ForensicManifest<ZipEntryRecord> {
  return {
    schema: "duat/forensics/zip-inventory/v1.3",
    fingerprint: "DUAT-v1.3-GAME-OS-DISK-FORENSICS-LANGUAGE-CORTEX",
    generated_at: generatedAt,
    source_root: sourceZip,
    records,
    boundary: {
      metadata_only: true,
      unknown_code_executed: false,
      publication_allowed: false,
      default_license_status: "unknown",
    },
  };
}
