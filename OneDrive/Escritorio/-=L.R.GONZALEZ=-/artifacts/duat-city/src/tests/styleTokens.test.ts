import { describe, expect, it } from "vitest";
import { readFileSync } from "node:fs";
import { analyzeStyleFromManifest } from "../style/styleAnalyzer";
import { listStyleProfiles } from "../style/styleProfiles";

const manifestUrl = new URL("../../public/asset-manifest/assets_du_wabi_manifest_v1_2.json", import.meta.url);
const styleUrl = new URL("../../public/asset-manifest/style_tokens_v1_2.json", import.meta.url);

describe("style tokens v1.2", () => {
  it("palette extracted and finite", () => {
    const manifest = JSON.parse(readFileSync(manifestUrl, "utf8"));
    const tokens = analyzeStyleFromManifest(manifest);
    expect(tokens.paletteTokens.length).toBeGreaterThan(0);
    expect(Number.isFinite(tokens.edgeDetailDensity)).toBe(true);
  });

  it("style profiles and generated JSON are valid", () => {
    expect(listStyleProfiles().length).toBeGreaterThanOrEqual(10);
    const tokens = JSON.parse(readFileSync(styleUrl, "utf8"));
    expect(tokens.publicationAllowed).toBe(false);
    expect(tokens.paletteTokens.length).toBeGreaterThan(0);
  });
});
