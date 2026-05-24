import type { PixelMaterial } from "./pixelTypes";

export type MaterialQBehavior = "stable" | "settles" | "rises" | "falls" | "flickers" | "transmits" | "reflects";

export interface MaterialDefinition {
  material: PixelMaterial;
  baseColor: string;
  density: number;
  friction: number;
  opacity: number;
  reflectance: number;
  roughness: number;
  emissive: number;
  heatCapacity: number;
  flammable: number;
  wettable: number;
  solidity: number;
  lightScatter: number;
  qBehavior: MaterialQBehavior;
}

export interface MaterialInteractionResult {
  material: PixelMaterial;
  emitsLight: boolean;
  heatDelta: number;
  wetnessDelta: number;
  velocity: { x: number; y: number };
  reflectance: number;
  scatter: number;
  qState: "00" | "01" | "10" | "11";
}
