import { scoreRendererCandidate } from "./rendererCandidateScorer";
import type { RendererCandidateType } from "./rendererCandidateScorer";

export interface RendererEntryInput {
  path: string;
  source_zip: string;
  size?: number;
}

export interface LovableRendererCandidate {
  path: string;
  source_zip: string;
  type: RendererCandidateType;
  stack_detected: string[];
  useful_for: string[];
  risk: "low" | "medium" | "high";
  integration_recommendation: "adopt" | "adapt" | "reference_only" | "reject";
  reason: string;
  requires_dependency: boolean;
  unknown_code_execution_risk: false;
  notes: string;
}

export interface LovableRendererManifest {
  schema: "duat/forensics/lovable-renderer-candidates/v1.3.2";
  fingerprint: "DUAT-v1.3.2-LOVABLE-ISO-EXTRACTION-VERMEER-LIGHT";
  generated_at: string;
  source_root: string;
  records: LovableRendererCandidate[];
  boundary: {
    metadata_only: true;
    unknown_code_executed: false;
    publication_allowed: false;
    no_raw_source_adoption: true;
  };
}

export function scanLovableRendererCandidates(entries: RendererEntryInput[]): LovableRendererCandidate[] {
  const records: LovableRendererCandidate[] = [];
  for (const entry of entries) {
    const score = scoreRendererCandidate({ path: entry.path, sourceZip: entry.source_zip, size: entry.size });
    if (score.recommendation === "reject") continue;
    records.push({
      path: entry.path,
      source_zip: entry.source_zip,
      type: score.types[0],
      stack_detected: score.stackDetected,
      useful_for: score.usefulFor,
      risk: score.risk,
      integration_recommendation: score.recommendation,
      reason: score.reason,
      requires_dependency: score.requiresDependency,
      unknown_code_execution_risk: false,
      notes: "Metadata/read-only candidate. DUAT v1.3.2 adapts concepts through local typed adapter, not raw zip execution.",
    });
  }
  return records.sort((a, b) => a.source_zip.localeCompare(b.source_zip) || a.path.localeCompare(b.path));
}

export function buildLovableRendererManifest(
  records: LovableRendererCandidate[],
  sourceRoot: string,
  generatedAt = new Date().toISOString(),
): LovableRendererManifest {
  return {
    schema: "duat/forensics/lovable-renderer-candidates/v1.3.2",
    fingerprint: "DUAT-v1.3.2-LOVABLE-ISO-EXTRACTION-VERMEER-LIGHT",
    generated_at: generatedAt,
    source_root: sourceRoot,
    records,
    boundary: {
      metadata_only: true,
      unknown_code_executed: false,
      publication_allowed: false,
      no_raw_source_adoption: true,
    },
  };
}
