import type { SpriteRef } from "./atlas";
import type { ReviewedAssetsManifest } from "./assetManifestLoader";

export interface SpriteResolver {
  resolve(spriteId: string): SpriteRef;
}

export function createSpriteResolver(manifest: ReviewedAssetsManifest | null | undefined): SpriteResolver {
  const bySpriteId = new Map<string, SpriteRef>();
  for (const asset of manifest?.assets ?? []) {
    for (const spriteId of asset.sprite_ids) {
      bySpriteId.set(spriteId, {
        id: spriteId,
        kind: inferKind(spriteId),
        src: asset.copied_path,
        fallback: "procedural",
        color: "#24e8ff",
      });
    }
  }
  return {
    resolve(spriteId: string): SpriteRef {
      return bySpriteId.get(spriteId) ?? {
        id: spriteId,
        kind: inferKind(spriteId),
        fallback: "procedural",
        color: "#8cb7c9",
      };
    },
  };
}

function inferKind(spriteId: string): SpriteRef["kind"] {
  const prefix = spriteId.split("/")[0];
  if (prefix === "tile" || prefix === "building" || prefix === "agent" || prefix === "object" || prefix === "effect" || prefix === "ui") return prefix;
  return "effect";
}
