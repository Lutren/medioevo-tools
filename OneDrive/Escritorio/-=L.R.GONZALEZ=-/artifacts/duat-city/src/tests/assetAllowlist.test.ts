import { describe, expect, it } from "vitest";
import { readFileSync } from "node:fs";

const allowlist = readJson("../../public/asset-manifest/asset_allowlist_v0_7.json");
const reviewed = readJson("../../public/reviewed-assets/v0_7/REVIEWED_ASSETS_MANIFEST.json");

describe("asset allowlist v0.7", () => {
  it("parses and stays under the copy limit", () => {
    expect(allowlist.schema).toBe("duat.asset-allowlist.v0.7");
    expect(allowlist.max_assets).toBeLessThanOrEqual(510);
    expect(allowlist.copied_count).toBe(reviewed.assets.length);
    expect(reviewed.assets.length).toBeLessThanOrEqual(510);
  });

  it("copied assets have hash, provenance and internal boundary", () => {
    for (const asset of reviewed.assets) {
      expect(asset.sha256).toMatch(/^[A-F0-9]{64}$/);
      expect(asset.origin_sha256).toBe(asset.sha256);
      expect(asset.original_path).toMatch(/^ROOT_/);
      expect(asset.boundary).toBe("INTERNAL_REVIEWED_ASSET");
      expect(asset.publication_allowed).toBe(false);
    }
  });

  it("does not copy REVIEW_REQUIRED or DENY entries", () => {
    const copied = new Set(reviewed.assets.map((asset: any) => asset.id));
    for (const entry of allowlist.entries) {
      if (copied.has(entry.id)) {
        expect(entry.copy_decision).toBe("APPROVE_INTERNAL_REVIEW_COPY");
      }
    }
  });
});

function readJson(path: string): any {
  return JSON.parse(readFileSync(new URL(path, import.meta.url), "utf8"));
}
