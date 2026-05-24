import type { LovableRendererCandidate } from "./lovableRendererScanner";

export interface IsometricTechSummary {
  schema: "duat/forensics/isometric-tech-inventory/v1.3.2";
  fingerprint: "DUAT-v1.3.2-LOVABLE-ISO-EXTRACTION-VERMEER-LIGHT";
  generated_at: string;
  candidate_count: number;
  stacks: Record<string, number>;
  recommendations: Record<string, number>;
  top_useful_for: Record<string, number>;
  boundary: {
    metadata_only: true;
    unknown_code_executed: false;
    publication_allowed: false;
  };
}

export function buildIsometricTechInventory(
  records: LovableRendererCandidate[],
  generatedAt = new Date().toISOString(),
): IsometricTechSummary {
  const stacks: Record<string, number> = {};
  const recommendations: Record<string, number> = {};
  const useful: Record<string, number> = {};

  for (const record of records) {
    recommendations[record.integration_recommendation] = (recommendations[record.integration_recommendation] ?? 0) + 1;
    for (const stack of record.stack_detected) stacks[stack] = (stacks[stack] ?? 0) + 1;
    for (const item of record.useful_for) useful[item] = (useful[item] ?? 0) + 1;
  }

  return {
    schema: "duat/forensics/isometric-tech-inventory/v1.3.2",
    fingerprint: "DUAT-v1.3.2-LOVABLE-ISO-EXTRACTION-VERMEER-LIGHT",
    generated_at: generatedAt,
    candidate_count: records.length,
    stacks,
    recommendations,
    top_useful_for: useful,
    boundary: {
      metadata_only: true,
      unknown_code_executed: false,
      publication_allowed: false,
    },
  };
}
