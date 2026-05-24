import type { PixelCell, PixelMaterial } from "./pixelTypes";

const MATERIALS: Record<PixelMaterial, Omit<PixelCell, "active">> = {
  empty: { material: "empty", mass: 0, vx: 0, vy: 0, temperature: 0.2, pressure: 0, wetness: 0, light: 0, solidity: 0, friction: 0.05, R: 0.02, Phi_eff: 0.95 },
  air: { material: "air", mass: 0.01, vx: 0, vy: 0, temperature: 0.2, pressure: 0.02, wetness: 0, light: 0, solidity: 0, friction: 0.01, R: 0.02, Phi_eff: 0.95 },
  stone: { material: "stone", mass: 3, vx: 0, vy: 0, temperature: 0.2, pressure: 0.1, wetness: 0, light: 0, solidity: 1, friction: 0.9, R: 0.05, Phi_eff: 0.9 },
  brick: { material: "brick", mass: 2.6, vx: 0, vy: 0, temperature: 0.22, pressure: 0.1, wetness: 0.05, light: 0, solidity: 1, friction: 0.86, R: 0.05, Phi_eff: 0.9 },
  wood: { material: "wood", mass: 1.2, vx: 0, vy: 0, temperature: 0.2, pressure: 0.05, wetness: 0.1, light: 0, solidity: 0.8, friction: 0.7, R: 0.06, Phi_eff: 0.88 },
  metal: { material: "metal", mass: 4, vx: 0, vy: 0, temperature: 0.18, pressure: 0.08, wetness: 0, light: 0, solidity: 1, friction: 0.55, R: 0.05, Phi_eff: 0.9 },
  glass: { material: "glass", mass: 2.1, vx: 0, vy: 0, temperature: 0.18, pressure: 0.04, wetness: 0, light: 0, solidity: 0.82, friction: 0.25, R: 0.07, Phi_eff: 0.86 },
  water: { material: "water", mass: 1, vx: 0, vy: 0.02, temperature: 0.15, pressure: 0.25, wetness: 1, light: 0, solidity: 0, friction: 0.2, R: 0.08, Phi_eff: 0.82 },
  soil: { material: "soil", mass: 1.5, vx: 0, vy: 0, temperature: 0.2, pressure: 0.08, wetness: 0.25, light: 0, solidity: 0.7, friction: 0.75, R: 0.05, Phi_eff: 0.88 },
  grass: { material: "grass", mass: 0.9, vx: 0, vy: 0, temperature: 0.2, pressure: 0.06, wetness: 0.35, light: 0, solidity: 0.35, friction: 0.68, R: 0.04, Phi_eff: 0.9 },
  fire: { material: "fire", mass: 0.05, vx: 0, vy: -0.04, temperature: 1, pressure: 0.45, wetness: 0, light: 1, solidity: 0, friction: 0.02, R: 0.45, Phi_eff: 0.42 },
  smoke: { material: "smoke", mass: 0.02, vx: 0, vy: -0.03, temperature: 0.55, pressure: 0.35, wetness: 0, light: 0.05, solidity: 0, friction: 0.04, R: 0.2, Phi_eff: 0.65 },
  dust: { material: "dust", mass: 0.18, vx: 0, vy: 0.03, temperature: 0.25, pressure: 0.16, wetness: 0, light: 0, solidity: 0, friction: 0.22, R: 0.12, Phi_eff: 0.72 },
  neon: { material: "neon", mass: 0.04, vx: 0, vy: 0, temperature: 0.42, pressure: 0.02, wetness: 0, light: 1, solidity: 0.1, friction: 0.02, R: 0.16, Phi_eff: 0.74 },
  cloth: { material: "cloth", mass: 0.45, vx: 0, vy: 0, temperature: 0.22, pressure: 0.04, wetness: 0.2, light: 0, solidity: 0.24, friction: 0.6, R: 0.07, Phi_eff: 0.84 },
  skin: { material: "skin", mass: 0.9, vx: 0, vy: 0, temperature: 0.35, pressure: 0.08, wetness: 0.1, light: 0, solidity: 0.2, friction: 0.42, R: 0.09, Phi_eff: 0.82 },
  obsidian: { material: "obsidian", mass: 3.4, vx: 0, vy: 0, temperature: 0.16, pressure: 0.06, wetness: 0, light: 0, solidity: 1, friction: 0.48, R: 0.08, Phi_eff: 0.86 },
  gold: { material: "gold", mass: 5, vx: 0, vy: 0, temperature: 0.2, pressure: 0.05, wetness: 0, light: 0.05, solidity: 1, friction: 0.36, R: 0.04, Phi_eff: 0.91 },
  crystal: { material: "crystal", mass: 2.4, vx: 0, vy: 0, temperature: 0.18, pressure: 0.04, wetness: 0, light: 0.18, solidity: 0.9, friction: 0.3, R: 0.09, Phi_eff: 0.84 },
  ruinMatter: { material: "ruinMatter", mass: 2.7, vx: 0, vy: 0, temperature: 0.28, pressure: 0.2, wetness: 0.1, light: 0.14, solidity: 0.85, friction: 0.76, R: 0.28, Phi_eff: 0.58 },
  light: { material: "light", mass: 0, vx: 0, vy: 0, temperature: 0.35, pressure: 0, wetness: 0, light: 1, solidity: 0, friction: 0, R: 0.03, Phi_eff: 0.93 },
  agent: { material: "agent", mass: 0.8, vx: 0, vy: 0, temperature: 0.25, pressure: 0.2, wetness: 0, light: 0, solidity: 0.2, friction: 0.35, R: 0.1, Phi_eff: 0.8 },
  resource: { material: "resource", mass: 0.5, vx: 0, vy: 0, temperature: 0.2, pressure: 0.1, wetness: 0, light: 0, solidity: 0.4, friction: 0.6, R: 0.06, Phi_eff: 0.86 },
};

export function makeCell(material: PixelMaterial = "air", active = false): PixelCell {
  return { ...MATERIALS[material], active };
}

export function isFluid(material: PixelMaterial): boolean {
  return material === "water" || material === "smoke" || material === "dust" || material === "fire";
}

export function isSolid(material: PixelMaterial): boolean {
  return MATERIALS[material].solidity >= 0.7;
}
