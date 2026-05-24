import { describe, expect, it } from "vitest";
import { createAssetAtlas, getSpriteRef } from "../graphics/atlas";
import { parseReviewedAssetsManifest } from "../graphics/assetManifestLoader";
import { createSpriteResolver } from "../graphics/spriteResolver";

const reviewed = parseReviewedAssetsManifest({
  schema: "duat.reviewed-assets.v0.7",
  generated_at: "2026-05-19T00:00:00.000Z",
  boundary: "INTERNAL_REVIEWED_ASSET",
  publication_allowed: false,
  assets: [
    {
      id: "duat-icon-gate",
      filename: "duat-icon-gate.svg",
      original_path: "ROOT_BRAIN_OS/DUAT ASSETS/icons/svg/duat-icon-gate.svg",
      copied_path: "/reviewed-assets/v0_7/duat-icon-gate.svg",
      intended_use: "gate state icon",
      boundary: "INTERNAL_REVIEWED_ASSET",
      publication_allowed: false,
      sha256: "A".repeat(64),
      origin_sha256: "A".repeat(64),
      sprite_ids: ["building/gatehouse", "ui/gate"],
    },
  ],
});

describe("asset atlas v0.7", () => {
  it("resolver returns fallback when asset is absent", () => {
    const resolver = createSpriteResolver(null);
    const sprite = resolver.resolve("building/archive");
    expect(sprite.src).toBeUndefined();
    expect(sprite.fallback).toBe("procedural");
  });

  it("resolver returns reviewed path when present", () => {
    const resolver = createSpriteResolver(reviewed);
    const sprite = resolver.resolve("building/gatehouse");
    expect(sprite.src).toBe("/reviewed-assets/v0_7/duat-icon-gate.svg");
    expect(sprite.kind).toBe("building");
  });

  it("asset atlas keeps procedural fallback for missing sprites", () => {
    const atlas = createAssetAtlas(reviewed);
    expect(atlas.schema).toBe("duat.sprite-atlas.v0.7");
    expect(getSpriteRef(atlas, "building/gatehouse").src).toBeDefined();
    expect(getSpriteRef(atlas, "tile/forest").fallback).toBe("procedural");
  });
});
