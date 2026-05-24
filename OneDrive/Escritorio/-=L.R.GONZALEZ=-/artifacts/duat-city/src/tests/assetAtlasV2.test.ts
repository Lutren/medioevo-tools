import { describe, expect, it } from "vitest";
import { createAssetAtlasV2 } from "../assets/assetAtlasV2";
import { resolveAsset } from "../assets/assetResolver";
import type { ReviewedAssetsManifestV12 } from "../assets/assetTypes";

describe("asset atlas v2", () => {
  it("resolves reviewed and fallback assets safely", () => {
    const reviewed: ReviewedAssetsManifestV12 = {
      schema: "duat.reviewed_assets_manifest.v1_2",
      copied_count: 1,
      publication_allowed: false,
      boundary: "INTERNAL_REVIEW_ONLY",
      assets: [{ key: "tile/wet_street", domain: "tile", mode: "reviewed", path: "/reviewed-assets/v1_2/wet.png", fallbackKey: "fallback", provenance: { publication_allowed: false, boundary: "INTERNAL_REVIEW_ONLY", original_path: "source" } }],
    };
    expect(resolveAsset({ domain: "tile", type: "wet_street" }, reviewed).mode).toBe("reviewed");
    expect(resolveAsset({ domain: "tile", type: "missing" }, reviewed).mode).toBe("procedural");
  });

  it("missing atlas key is safe", () => {
    const atlas = createAssetAtlasV2([{ domain: "ui", type: "terminal_frame" }]);
    expect(atlas.refs["ui/terminal_frame"].provenance?.publication_allowed).toBe(false);
  });
});
