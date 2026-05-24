import type { ArtDirectedScene, LightCanonName, LightCanonProfile } from "./artDirectionTypes";

export const LIGHT_CANON_PROFILES: Record<LightCanonName, LightCanonProfile> = {
  balanced_medioevo: {
    name: "balanced_medioevo",
    publicToken: "balanced_medioevo_cinematic_light",
    contrast: 0.58,
    backgroundDarkness: 0.42,
    lateralLight: 0.45,
    shadowDepth: 0.48,
    interiorSoftness: 0.42,
    detailBoost: 0.5,
    reflectionBoost: 0.48,
    uses: ["city readability", "default exploration", "OSIT overlays"],
  },
  caravaggio_chiaroscuro: {
    name: "caravaggio_chiaroscuro",
    publicToken: "high_contrast_revelation",
    contrast: 0.92,
    backgroundDarkness: 0.88,
    lateralLight: 0.9,
    shadowDepth: 0.9,
    interiorSoftness: 0.18,
    detailBoost: 0.62,
    reflectionBoost: 0.54,
    uses: ["gates", "danger", "revelation", "judgement", "ritual ruins"],
  },
  vermeer_interior_light: {
    name: "vermeer_interior_light",
    publicToken: "soft_interior_window_light",
    contrast: 0.5,
    backgroundDarkness: 0.38,
    lateralLight: 0.64,
    shadowDepth: 0.35,
    interiorSoftness: 0.88,
    detailBoost: 0.6,
    reflectionBoost: 0.42,
    uses: ["interiors", "archives", "workshops", "taverns", "memory", "conversation"],
  },
  van_eyck_detail_light: {
    name: "van_eyck_detail_light",
    publicToken: "micro_material_detail",
    contrast: 0.68,
    backgroundDarkness: 0.46,
    lateralLight: 0.58,
    shadowDepth: 0.54,
    interiorSoftness: 0.52,
    detailBoost: 0.94,
    reflectionBoost: 0.82,
    uses: ["props", "relics", "diegetic UI", "portraits", "inventory", "material studies"],
  },
};

export function getLightCanonProfile(name: LightCanonName | string): LightCanonProfile {
  return LIGHT_CANON_PROFILES[name as LightCanonName] ?? LIGHT_CANON_PROFILES.balanced_medioevo;
}

export function applyLightCanon<T extends ArtDirectedScene>(scene: T, profileInput: LightCanonProfile | LightCanonName): T {
  const profile = typeof profileInput === "string" ? getLightCanonProfile(profileInput) : profileInput;
  const moodTags = new Set([...(scene.moodTags ?? []), profile.publicToken, ...profile.uses.slice(0, 3)]);
  return {
    ...scene,
    lightProfile: profile.publicToken,
    contrast: clamp01((Number(scene.contrast) || 0.5) * 0.45 + profile.contrast * 0.55),
    backgroundDarkness: clamp01((Number(scene.backgroundDarkness) || 0.35) * 0.4 + profile.backgroundDarkness * 0.6),
    shadowStrength: clamp01((Number(scene.shadowStrength) || 0.45) * 0.4 + profile.shadowDepth * 0.6),
    detailDensity: clamp01((Number(scene.detailDensity) || 0.45) * 0.35 + profile.detailBoost * 0.65),
    materialReflection: clamp01((Number(scene.materialReflection) || 0.4) * 0.45 + profile.reflectionBoost * 0.55),
    atmosphere: clamp01((Number(scene.atmosphere) || 0.2) + profile.backgroundDarkness * 0.08),
    moodTags: Array.from(moodTags),
  };
}

export function scoreLightDrama(scene: ArtDirectedScene): number {
  const contrast = finite01(scene.contrast, 0.5);
  const darkness = finite01(scene.backgroundDarkness, 0.4);
  const shadow = finite01(scene.shadowStrength, 0.45);
  return round01(contrast * 0.4 + darkness * 0.3 + shadow * 0.3);
}

export function scoreMaterialDetail(scene: ArtDirectedScene): number {
  const detail = finite01(scene.detailDensity, 0.5);
  const reflection = finite01(scene.materialReflection, 0.4);
  const contrast = finite01(scene.contrast, 0.5);
  return round01(detail * 0.55 + reflection * 0.3 + contrast * 0.15);
}

function finite01(value: unknown, fallback: number): number {
  return typeof value === "number" && Number.isFinite(value) ? clamp01(value) : fallback;
}

function clamp01(value: number): number {
  return Math.max(0, Math.min(1, Number.isFinite(value) ? value : 0));
}

function round01(value: number): number {
  return Number(clamp01(value).toFixed(3));
}
