import type { ArtDirectedScene } from "./artDirectionTypes";
import { applyLightCanon, getLightCanonProfile } from "./lightCanon";

export interface VermeerLightProfile {
  name: "vermeer_interior_light";
  publicToken: "soft_interior_window_light";
  sideLight: number;
  windowSourceClarity: number;
  shadowControl: number;
  warmCoolBalance: number;
  wetReflectionSoftness: number;
  bloomDiscipline: number;
  atmosphereCalm: number;
}

export function createVermeerLightProfile(): VermeerLightProfile {
  return {
    name: "vermeer_interior_light",
    publicToken: "soft_interior_window_light",
    sideLight: 0.68,
    windowSourceClarity: 0.86,
    shadowControl: 0.78,
    warmCoolBalance: 0.62,
    wetReflectionSoftness: 0.55,
    bloomDiscipline: 0.84,
    atmosphereCalm: 0.8,
  };
}

export function applyVermeerLightProfile<T extends ArtDirectedScene>(scene: T): T {
  const canon = applyLightCanon(scene, getLightCanonProfile("vermeer_interior_light"));
  return {
    ...canon,
    contrast: mix(canon.contrast ?? 0.5, 0.52, 0.5),
    shadowStrength: mix(canon.shadowStrength ?? 0.35, 0.34, 0.55),
    materialReflection: mix(canon.materialReflection ?? 0.42, 0.48, 0.45),
    atmosphere: mix(canon.atmosphere ?? 0.22, 0.28, 0.35),
    moodTags: Array.from(new Set([...(canon.moodTags ?? []), "soft_window_source", "controlled_shadow", "warm_interior_calm"])),
  };
}

export function scoreVermeerLight(scene: ArtDirectedScene): number {
  const contrast = finite(scene.contrast, 0.5);
  const shadow = finite(scene.shadowStrength, 0.35);
  const reflection = finite(scene.materialReflection, 0.45);
  const calm = 1 - Math.abs(contrast - 0.52);
  return round(calm * 0.38 + (1 - Math.abs(shadow - 0.34)) * 0.32 + reflection * 0.3);
}

function mix(a: number, b: number, t: number): number {
  return round(a * (1 - t) + b * t);
}

function finite(value: unknown, fallback: number): number {
  return typeof value === "number" && Number.isFinite(value) ? clamp(value) : fallback;
}

function clamp(value: number): number {
  return Math.max(0, Math.min(1, value));
}

function round(value: number): number {
  return Number(clamp(value).toFixed(3));
}
