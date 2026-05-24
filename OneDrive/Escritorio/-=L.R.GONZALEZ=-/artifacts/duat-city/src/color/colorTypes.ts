export interface RGB {
  r: number;
  g: number;
  b: number;
}

export interface HSL {
  h: number;
  s: number;
  l: number;
}

export interface HSV {
  h: number;
  s: number;
  v: number;
}

export interface OKLab {
  L: number;
  a: number;
  b: number;
}

export interface ToneMappingOptions {
  exposure: number;
  contrast: number;
  gamma: number;
  saturation: number;
  bloomThreshold: number;
  shadowLift: number;
  highlightRolloff: number;
}

export type HarmonyKind =
  | "complementary"
  | "analogous"
  | "triadic"
  | "split-complementary"
  | "monochrome"
  | "cinematic-teal-amber"
  | "medioevo-archeopunk";

export interface PaletteProfile {
  id: string;
  name: string;
  colors: RGB[];
  tags: string[];
  temperature: "warm" | "cool" | "mixed";
}

export interface DitherOptions {
  matrix: "bayer4" | "bayer8";
  strength: number;
  seed?: number;
}

export const DEFAULT_TONE_MAPPING: ToneMappingOptions = {
  exposure: 1,
  contrast: 1.08,
  gamma: 2.2,
  saturation: 1.05,
  bloomThreshold: 0.78,
  shadowLift: 0.03,
  highlightRolloff: 0.85,
};
