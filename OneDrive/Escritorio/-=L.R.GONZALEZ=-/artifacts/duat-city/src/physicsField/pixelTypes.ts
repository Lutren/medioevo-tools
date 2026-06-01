export type PixelMaterial =
  | "empty"
  | "air"
  | "stone"
  | "brick"
  | "wood"
  | "metal"
  | "glass"
  | "water"
  | "soil"
  | "grass"
  | "fire"
  | "smoke"
  | "dust"
  | "neon"
  | "cloth"
  | "skin"
  | "obsidian"
  | "gold"
  | "crystal"
  | "ruinMatter"
  | "light"
  | "agent"
  | "resource";

export interface PixelCell {
  material: PixelMaterial;
  mass: number;
  vx: number;
  vy: number;
  temperature: number;
  pressure: number;
  wetness: number;
  light: number;
  color?: string;
  emissive?: number;
  opacity?: number;
  density?: number;
  reflectance?: number;
  roughness?: number;
  qState?: "00" | "01" | "10" | "11";
  phaseState?: "solid" | "liquid" | "gas";
  solidity: number;
  friction: number;
  R: number;
  Phi_eff: number;
  active: boolean;
}

export interface PixelField {
  width: number;
  height: number;
  cells: PixelCell[];
  tick: number;
  qPacked?: Uint8Array;
}

export interface FieldMetrics {
  activeCells: number;
  updatedCells: number;
  skippedCells: number;
  heat: number;
  pressure: number;
  unresolvedField: number;
  R_field: number;
  Phi_field: number;
}

export interface PhysicsFieldSummary {
  resolution: string;
  dominant_materials: Record<string, number>;
  hazards: string[];
  R_field: number;
  Phi_field: number;
}

export const EMPTY_FIELD_METRICS: FieldMetrics = {
  activeCells: 0,
  updatedCells: 0,
  skippedCells: 0,
  heat: 0,
  pressure: 0,
  unresolvedField: 0,
  R_field: 0,
  Phi_field: 1,
};
