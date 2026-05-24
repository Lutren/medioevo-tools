import type { MaterialDetailProfile } from "./artDirectionTypes";

export const MATERIAL_DETAIL_PROFILES: Record<string, MaterialDetailProfile> = {
  aged_brass: profile("aged_brass", "#9b7a3f", 0.42, 0.58, 1, 0, 0.55, 0.72, 0.68),
  burnished_copper: profile("burnished_copper", "#b46a32", 0.32, 0.68, 1, 0, 0.62, 0.76, 0.66),
  obsidian_glass: profile("obsidian_glass", "#12131a", 0.16, 0.78, 0.72, 0.04, 0.5, 0.84, 0.82),
  wet_stone: profile("wet_stone", "#586068", 0.36, 0.64, 1, 0, 0.9, 0.62, 0.52),
  patinated_bronze: profile("patinated_bronze", "#4d6f62", 0.48, 0.52, 1, 0, 0.58, 0.78, 0.74),
  bioluminescent_algae: profile("bioluminescent_algae", "#38d9a9", 0.62, 0.34, 0.78, 0.62, 0.88, 0.7, 0.64),
  ritual_amber: profile("ritual_amber", "#ffb23f", 0.28, 0.5, 0.92, 0.34, 0.42, 0.66, 0.86),
  smoked_crystal: profile("smoked_crystal", "#7b748f", 0.22, 0.72, 0.58, 0.12, 0.46, 0.82, 0.76),
  carbonized_wood: profile("carbonized_wood", "#2a211b", 0.7, 0.22, 1, 0.02, 0.2, 0.68, 0.58),
  moss_organic_membrane: profile("moss_organic_membrane", "#587a46", 0.76, 0.2, 0.94, 0.05, 0.8, 0.74, 0.7),
  rain_wet_metal: profile("rain_wet_metal", "#6d7782", 0.26, 0.78, 1, 0, 0.96, 0.7, 0.62),
  old_paper_archive_tablet: profile("old_paper_archive_tablet", "#c2a46e", 0.84, 0.08, 1, 0, 0.16, 0.88, 0.8),
};

export function getMaterialDetailProfile(id: string): MaterialDetailProfile {
  return MATERIAL_DETAIL_PROFILES[id] ?? MATERIAL_DETAIL_PROFILES.wet_stone;
}

export function listMaterialDetailProfiles(): MaterialDetailProfile[] {
  return Object.values(MATERIAL_DETAIL_PROFILES);
}

function profile(
  id: string,
  baseColor: string,
  roughness: number,
  reflectance: number,
  opacity: number,
  emissive: number,
  wetnessResponse: number,
  detailDensity: number,
  symbolicWeight: number,
): MaterialDetailProfile {
  return { id, baseColor, roughness, reflectance, opacity, emissive, wetnessResponse, detailDensity, symbolicWeight };
}
