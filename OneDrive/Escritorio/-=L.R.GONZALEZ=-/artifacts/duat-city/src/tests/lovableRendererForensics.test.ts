import { readFileSync } from "node:fs";
import { describe, expect, it } from "vitest";
import { scanLovableRendererCandidates } from "../forensics/lovableRendererScanner";
import { scoreRendererCandidate } from "../forensics/rendererCandidateScorer";

const manifests = [
  new URL("../../public/asset-manifest/lovable_renderer_candidates_v1_3_2.json", import.meta.url),
  new URL("../../public/asset-manifest/isometric_renderer_inventory_v1_3_2.json", import.meta.url),
  new URL("../../public/asset-manifest/ui_i18n_assets_inventory_v1_3_2.json", import.meta.url),
  new URL("../../public/asset-manifest/visual_bible_inventory_v1_3_2.json", import.meta.url),
];

describe("Lovable renderer forensics v1.3.2", () => {
  it("manifests parse and record no unknown code execution", () => {
    for (const url of manifests) {
      const manifest = JSON.parse(readFileSync(url, "utf8"));
      expect(manifest.fingerprint).toBe("DUAT-v1.3.2-LOVABLE-ISO-EXTRACTION-VERMEER-LIGHT");
      expect(manifest.boundary.metadata_only).toBe(true);
      expect(manifest.boundary.unknown_code_executed).toBe(false);
      expect(manifest.boundary.publication_allowed).toBe(false);
      expect(Array.isArray(manifest.records)).toBe(true);
    }
  });

  it("scores renderer candidates without adopting raw code", () => {
    const score = scoreRendererCandidate({ path: "src/components/IsometricScene.tsx" });
    expect(score.recommendation).toBe("adapt");
    expect(score.requiresDependency).toBe(false);
    const records = scanLovableRendererCandidates([{ path: "src/three/WorldCanvas.tsx", source_zip: "lovable.zip", size: 500 }]);
    expect(records[0].unknown_code_execution_risk).toBe(false);
    expect(records[0].integration_recommendation).toBe("adapt");
  });
});
