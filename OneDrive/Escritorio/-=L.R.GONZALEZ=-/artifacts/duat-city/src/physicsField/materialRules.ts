import type { PixelMaterial } from "./pixelTypes";
import type { MaterialDefinition, MaterialInteractionResult } from "./materialTypes";

export const MATERIAL_DEFINITIONS: Record<PixelMaterial, MaterialDefinition> = {
  empty: def("empty", "#000000", 0, 0.05, 0, 0, 1, 0, 0, 0, 0, 0, 0, "stable"),
  air: def("air", "#141a22", 0.01, 0.01, 0, 0, 1, 0, 0.1, 0, 0, 0, 0.05, "stable"),
  stone: def("stone", "#6b6760", 3, 0.9, 0.85, 0.12, 0.72, 0, 0.9, 0, 0.1, 1, 0.03, "stable"),
  brick: def("brick", "#8b5142", 2.6, 0.86, 0.78, 0.1, 0.78, 0, 0.82, 0.08, 0.2, 1, 0.04, "stable"),
  wood: def("wood", "#72523a", 1.2, 0.7, 0.58, 0.08, 0.86, 0, 0.45, 0.72, 0.34, 0.8, 0.08, "stable"),
  metal: def("metal", "#8b9296", 4, 0.55, 0.74, 0.62, 0.24, 0, 0.42, 0, 0.08, 1, 0.02, "reflects"),
  glass: def("glass", "#a9d8e6", 2.1, 0.25, 0.18, 0.28, 0.08, 0, 0.3, 0, 0.04, 0.82, 0.22, "transmits"),
  water: def("water", "#3678a8", 1, 0.2, 0.12, 0.68, 0.04, 0, 0.95, 0, 1, 0, 0.18, "falls"),
  soil: def("soil", "#594532", 1.5, 0.75, 0.35, 0.08, 0.92, 0, 0.72, 0.1, 0.5, 0.7, 0.08, "settles"),
  grass: def("grass", "#477448", 0.9, 0.68, 0.26, 0.05, 0.9, 0, 0.62, 0.38, 0.7, 0.35, 0.1, "stable"),
  fire: def("fire", "#ff7a2f", 0.05, 0.02, 0.02, 0.05, 0.35, 1, 0.05, 1, 0, 0, 0.42, "flickers"),
  smoke: def("smoke", "#6f747d", 0.02, 0.04, 0.2, 0.02, 0.96, 0.04, 0.2, 0, 0.05, 0, 0.55, "rises"),
  dust: def("dust", "#9c866a", 0.18, 0.22, 0.18, 0.03, 0.98, 0, 0.15, 0.08, 0.08, 0, 0.35, "settles"),
  neon: def("neon", "#22e8ff", 0.04, 0.02, 0.04, 0.18, 0.12, 1, 0.2, 0, 0, 0.1, 0.32, "flickers"),
  cloth: def("cloth", "#9d5c49", 0.45, 0.6, 0.35, 0.04, 0.92, 0, 0.4, 0.48, 0.45, 0.24, 0.12, "settles"),
  skin: def("skin", "#b87a63", 0.9, 0.42, 0.24, 0.05, 0.76, 0, 0.72, 0.08, 0.22, 0.2, 0.08, "stable"),
  obsidian: def("obsidian", "#11131a", 3.4, 0.48, 0.88, 0.5, 0.05, 0.02, 0.86, 0, 0.02, 1, 0.01, "reflects"),
  gold: def("gold", "#d6a642", 5, 0.36, 0.7, 0.74, 0.18, 0.06, 0.35, 0, 0.02, 1, 0.03, "reflects"),
  crystal: def("crystal", "#89ddff", 2.4, 0.3, 0.22, 0.36, 0.05, 0.25, 0.28, 0, 0.02, 0.9, 0.3, "transmits"),
  ruinMatter: def("ruinMatter", "#5c3f6f", 2.7, 0.76, 0.66, 0.22, 0.68, 0.22, 0.7, 0.16, 0.12, 0.85, 0.26, "flickers"),
  light: def("light", "#fff2a8", 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0.1, "flickers"),
  agent: def("agent", "#7cb9ff", 0.8, 0.35, 0.22, 0.05, 0.8, 0, 0.7, 0, 0.1, 0.2, 0.05, "stable"),
  resource: def("resource", "#8bd45a", 0.5, 0.6, 0.32, 0.06, 0.84, 0, 0.55, 0.18, 0.12, 0.4, 0.08, "stable"),
};

export function getMaterialDefinition(material: PixelMaterial): MaterialDefinition {
  return MATERIAL_DEFINITIONS[material] ?? MATERIAL_DEFINITIONS.air;
}

export function evaluateMaterialRules(material: PixelMaterial, wetness = 0, tick = 0): MaterialInteractionResult {
  const m = getMaterialDefinition(material);
  const wetReflectance = material === "stone" || material === "brick"
    ? Math.min(1, m.reflectance + wetness * 0.35)
    : Math.min(1, m.reflectance + wetness * 0.1);
  const flicker = m.qBehavior === "flickers" ? (Math.sin(tick * 0.7) > 0.25 ? "11" : "01") : undefined;
  return {
    material,
    emitsLight: m.emissive > 0.2,
    heatDelta: material === "fire" ? 0.35 : material === "water" ? -0.05 : 0,
    wetnessDelta: material === "water" ? 1 : material === "fire" ? -0.35 : 0,
    velocity: velocityForBehavior(m.qBehavior),
    reflectance: wetReflectance,
    scatter: m.lightScatter,
    qState: flicker ?? (m.qBehavior === "falls" ? "10" : m.qBehavior === "stable" ? "00" : "11"),
  };
}

function def(
  material: PixelMaterial,
  baseColor: string,
  density: number,
  friction: number,
  opacity: number,
  reflectance: number,
  roughness: number,
  emissive: number,
  heatCapacity: number,
  flammable: number,
  wettable: number,
  solidity: number,
  lightScatter: number,
  qBehavior: MaterialDefinition["qBehavior"],
): MaterialDefinition {
  return { material, baseColor, density, friction, opacity, reflectance, roughness, emissive, heatCapacity, flammable, wettable, solidity, lightScatter, qBehavior };
}

function velocityForBehavior(qBehavior: MaterialDefinition["qBehavior"]): { x: number; y: number } {
  if (qBehavior === "falls") return { x: 0.04, y: 0.18 };
  if (qBehavior === "rises") return { x: 0.02, y: -0.16 };
  if (qBehavior === "settles") return { x: 0.01, y: 0.04 };
  return { x: 0, y: 0 };
}
