import type { DuatStyleTokens } from "./styleTypes";

export const DEFAULT_DUAT_STYLE_TOKENS: DuatStyleTokens = {
  schema: "duat.style_tokens.v1_2",
  generatedAt: "static-fallback",
  paletteTokens: ["obsidian", "aged_brass", "burnished_copper", "operational_cyan", "ritual_amber", "wet_stone"],
  contrastProfile: "high",
  edgeDetailDensity: 0.72,
  metalCopperObsidianCyanAmberRatios: {
    metal: 0.28,
    copper: 0.18,
    obsidian: 0.2,
    cyan: 0.18,
    amber: 0.16,
  },
  glowColorTendencies: ["cyan", "amber", "pink", "algae_green"],
  uiFrameStyle: "diegetic brass/obsidian terminal frame",
  materialCategories: ["wet_stone", "rain_wet_metal", "aged_brass", "obsidian_glass", "old_paper_archive_tablet"],
  sceneMoodTags: ["archeopunk", "steampunk", "cyberpunk", "biopunk", "cinematic-light"],
  lightDirectionTags: ["side_light", "window_soft", "neon_reflection", "fire_core"],
  proportions: {
    tile: "2.5d isometric 2:1 footprint",
    building: "compact vertical city module",
    prop: "readable 8-24px symbolic silhouette",
  },
  sourceAssetCount: 0,
  publicationAllowed: false,
};

export function mergeStyleTokens(partial: Partial<DuatStyleTokens>): DuatStyleTokens {
  return {
    ...DEFAULT_DUAT_STYLE_TOKENS,
    ...partial,
    schema: "duat.style_tokens.v1_2",
    publicationAllowed: false,
    paletteTokens: partial.paletteTokens?.length ? partial.paletteTokens : DEFAULT_DUAT_STYLE_TOKENS.paletteTokens,
    glowColorTendencies: partial.glowColorTendencies?.length ? partial.glowColorTendencies : DEFAULT_DUAT_STYLE_TOKENS.glowColorTendencies,
    materialCategories: partial.materialCategories?.length ? partial.materialCategories : DEFAULT_DUAT_STYLE_TOKENS.materialCategories,
    sceneMoodTags: partial.sceneMoodTags?.length ? partial.sceneMoodTags : DEFAULT_DUAT_STYLE_TOKENS.sceneMoodTags,
    lightDirectionTags: partial.lightDirectionTags?.length ? partial.lightDirectionTags : DEFAULT_DUAT_STYLE_TOKENS.lightDirectionTags,
  };
}
