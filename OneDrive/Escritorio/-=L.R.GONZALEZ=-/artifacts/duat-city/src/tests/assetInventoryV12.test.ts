import { describe, expect, it } from "vitest";
import { readFileSync } from "node:fs";

const manifestUrl = new URL("../../public/asset-manifest/assets_du_wabi_manifest_v1_2.json", import.meta.url);
const reviewedUrl = new URL("../../public/reviewed-assets/v1_2/REVIEWED_ASSETS_MANIFEST.json", import.meta.url);

describe("asset inventory v1.2", () => {
  it("manifest parses and remains metadata-only", () => {
    const manifest = JSON.parse(readFileSync(manifestUrl, "utf8"));
    expect(manifest.schema).toBe("duat.asset_manifest.v1_2");
    expect(manifest.publication_allowed).toBe(false);
    expect(manifest.asset_count).toBeGreaterThanOrEqual(0);
    expect(JSON.stringify(manifest)).not.toMatch(/publication_allowed\"\\s*:\\s*true/);
  });

  it("no copied asset lacks provenance", () => {
    const reviewed = JSON.parse(readFileSync(reviewedUrl, "utf8"));
    expect(reviewed.publication_allowed).toBe(false);
    for (const asset of reviewed.assets ?? []) {
      expect(asset.original_path || asset.provenance?.original_path).toBeTruthy();
      expect(asset.publication_allowed ?? asset.provenance?.publication_allowed).toBe(false);
    }
  });
});
