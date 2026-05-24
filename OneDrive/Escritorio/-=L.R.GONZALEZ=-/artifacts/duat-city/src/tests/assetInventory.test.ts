import { describe, expect, it } from "vitest";
import { readFileSync } from "node:fs";

const visualManifest = readJson("../../public/asset-manifest/visual_assets_manifest_v0_6.json");
const codeManifest = readJson("../../public/asset-manifest/code_candidates_manifest_v0_6.json");
const variantsManifest = readJson("../../public/asset-manifest/duat_variants_manifest_v0_6.json");

describe("asset forensics manifests v0.6", () => {
  it("parse and expose required asset fields", () => {
    expect(visualManifest.schema).toBe("duat.asset_manifest.v0.6");
    expect(Array.isArray(visualManifest.assets)).toBe(true);
    const sample = visualManifest.assets[0];
    expect(sample).toHaveProperty("path_original");
    expect(sample).toHaveProperty("public_safe_guess");
    expect(sample).toHaveProperty("copy_status");
  });

  it("does not expose absolute private Windows paths in public manifests", () => {
    const all = JSON.stringify([visualManifest, codeManifest, variantsManifest]);
    expect(all).not.toMatch(/C:\\Users\\/i);
    expect(all).not.toMatch(/OneDrive\\Escritorio/i);
  });

  it("marks public safety guess on every asset", () => {
    for (const asset of visualManifest.assets) {
      expect(["yes", "no", "review"]).toContain(asset.public_safe_guess);
    }
  });
});

function readJson(path: string): any {
  return JSON.parse(readFileSync(new URL(path, import.meta.url), "utf8"));
}
