import type { TileType } from "../core/types";
import type { ReviewedAssetsManifest } from "./assetManifestLoader";

export interface SpriteRef {
  id: string;
  kind: "tile" | "building" | "agent" | "object" | "effect" | "ui";
  src?: string;
  fallback: "procedural";
  color: string;
}

export interface SpriteAtlasManifest {
  schema: "duat.sprite-atlas.v0.6" | "duat.sprite-atlas.v0.7";
  generated_from: "procedural" | "asset-manifest";
  sprites: SpriteRef[];
}

const TILE_COLORS: Record<TileType, string> = {
  empty: "#1d2430",
  road: "#3c4148",
  plaza: "#526451",
  residential: "#315a7d",
  workshop: "#7a542e",
  archive: "#235b78",
  observatory: "#253f70",
  market: "#77602e",
  clinic: "#28775c",
  academy: "#46307d",
  theater: "#744062",
  temple: "#58306a",
  garden: "#267047",
  ruin: "#6a533a",
  gatehouse: "#69694a",
  water: "#1f5e86",
  forest: "#206b3d",
  stone: "#60666d",
  wall: "#555a63",
};

export function createProceduralAtlas(): SpriteAtlasManifest {
  const tileSprites = Object.entries(TILE_COLORS).map(([type, color]) => ({
    id: `tile/${type}`,
    kind: "tile" as const,
    fallback: "procedural" as const,
    color,
  }));
  return {
    schema: "duat.sprite-atlas.v0.6",
    generated_from: "procedural",
    sprites: [
      ...tileSprites,
      { id: "agent/default", kind: "agent", fallback: "procedural", color: "#24e8ff" },
      { id: "effect/signal", kind: "effect", fallback: "procedural", color: "#00f5d4" },
      { id: "effect/anomaly", kind: "effect", fallback: "procedural", color: "#ffd166" },
    ],
  };
}

export function getSpriteRef(manifest: SpriteAtlasManifest, id: string): SpriteRef {
  return manifest.sprites.find(sprite => sprite.id === id) ?? {
    id,
    kind: id.split("/")[0] as SpriteRef["kind"],
    fallback: "procedural",
    color: "#8cb7c9",
  };
}

export function createAssetAtlas(reviewed: ReviewedAssetsManifest | null | undefined): SpriteAtlasManifest {
  const base = createProceduralAtlas();
  if (!reviewed || reviewed.assets.length === 0) return base;
  const reviewedSprites = reviewed.assets.flatMap(asset =>
    asset.sprite_ids.map(spriteId => ({
      id: spriteId,
      kind: inferKind(spriteId),
      src: asset.copied_path,
      fallback: "procedural" as const,
      color: "#24e8ff",
    })),
  );
  return {
    schema: "duat.sprite-atlas.v0.7",
    generated_from: "asset-manifest",
    sprites: [...reviewedSprites, ...base.sprites],
  };
}

function inferKind(spriteId: string): SpriteRef["kind"] {
  const prefix = spriteId.split("/")[0];
  if (["tile", "building", "agent", "object", "effect", "ui"].includes(prefix)) return prefix as SpriteRef["kind"];
  return "effect";
}
