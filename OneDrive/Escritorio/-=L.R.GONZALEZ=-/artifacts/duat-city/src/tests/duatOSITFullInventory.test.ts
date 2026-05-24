import { readFileSync } from "node:fs";
import { describe, expect, it } from "vitest";

const manifestUrl = new URL("../../public/asset-manifest/duat_osit_full_sources_manifest_v1_4.json", import.meta.url);

describe("DUAT OSIT full source inventory v1.4", () => {
  it("parses source manifest and keeps raw adoption blocked", () => {
    const manifest = JSON.parse(readFileSync(manifestUrl, "utf8"));
    expect(manifest.schema).toBe("duat/osit-full-source-inventory/v1.4");
    expect(manifest.fingerprint).toBe("DUAT-v1.4-OSIT-OBSERVACIONISMO-FULL");
    expect(manifest.source_count).toBe(27);
    expect(manifest.found_count).toBe(27);
    expect(manifest.boundary.unknown_code_executed).toBe(false);
    expect(manifest.boundary.assets_copied_to_public).toBe(false);
    expect(manifest.boundary.publication_allowed).toBe(false);
    expect(manifest.staging.raw_wholesale_extraction).toBe("BLOCKED_BY_SOURCE_ADOPTION_LAW");
    expect(Array.isArray(manifest.sampled_zip_entries)).toBe(true);
    expect(manifest.module_observacionismo.visual_renderer_assets.action_gate).toBe("REVIEW");
    for (const record of manifest.records) {
      expect(Number.isFinite(record.observacionismo_state.R)).toBe(true);
      expect(Number.isFinite(record.observacionismo_state.Phi_eff)).toBe(true);
      expect(["APPROVE", "REVIEW", "BLOCK"]).toContain(record.observacionismo_state.action_gate);
    }
  });
});
