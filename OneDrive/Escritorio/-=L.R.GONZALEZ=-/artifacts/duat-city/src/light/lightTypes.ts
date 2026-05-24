import type { RGB } from "../color/colorTypes";

export type LightSourceKind =
  | "sun"
  | "moon"
  | "torch"
  | "window"
  | "neon"
  | "fire"
  | "magic"
  | "signal"
  | "water_reflection"
  | "ruin_anomaly";

export interface LightCell {
  r: number;
  g: number;
  b: number;
  intensity: number;
  opacity: number;
  emission: RGB;
  reflectance: number;
  scatter: number;
  temperature: number;
  dirty: boolean;
}

export interface LightSource {
  id: string;
  kind: LightSourceKind;
  x: number;
  y: number;
  radius: number;
  intensity: number;
  color: RGB;
  direction?: { x: number; y: number };
  flicker?: number;
}

export interface LightGrid {
  width: number;
  height: number;
  cells: LightCell[];
  ambient: RGB;
  sources: LightSource[];
  bouncePasses: number;
  budget?: {
    activeLightCellCap: number;
    particleCap: number;
    intensityThreshold: number;
    updateCadenceFrames: number;
    reflectionScale: number;
  };
}

export interface LightMetrics {
  activeLightCells: number;
  blockedCells: number;
  emittedCells: number;
  reflectedCells: number;
  R_light: number;
  Phi_light: number;
  finite: boolean;
}

export const EMPTY_LIGHT_CELL: LightCell = {
  r: 0,
  g: 0,
  b: 0,
  intensity: 0,
  opacity: 0,
  emission: { r: 0, g: 0, b: 0 },
  reflectance: 0,
  scatter: 0,
  temperature: 6500,
  dirty: false,
};
