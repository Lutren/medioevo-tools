import type { ViewMode } from "../graphics/types";

export type RenderQualityPreset = "LOW" | "MEDIUM" | "HIGH" | "BEAUTIFUL" | "DEBUG";
export type TimeOfDay = "dawn" | "day" | "golden" | "night" | "interior";
export type WeatherMode = "clear" | "rain" | "snow" | "fog" | "jungle_mist" | "desert_haze";

export interface RenderQualitySettings {
  internalWidth: number;
  internalHeight: number;
  bouncePasses: number;
  bloom: boolean;
  reflections: boolean;
  fog: boolean;
  debugGrids: boolean;
}

export interface PixelRealismConfig {
  qualityPreset: RenderQualityPreset;
  timeOfDay: TimeOfDay;
  weather: WeatherMode;
  paletteProfile: string;
  lightProfile: string;
  lightIntensity: number;
  bloomAmount: number;
  dither: boolean;
  pixelScale: number;
  hideUiForCapture: boolean;
  vibePreset?: string;
  mood?: string;
}

export type PixelRenderPass =
  | "world"
  | "material"
  | "light"
  | "shadow"
  | "reflection"
  | "atmosphere"
  | "bloom"
  | "colorGrade"
  | "dither"
  | "pixelScale"
  | "uiOverlay";

export const PIXEL_RENDER_PASS_ORDER: PixelRenderPass[] = [
  "world",
  "material",
  "light",
  "shadow",
  "reflection",
  "atmosphere",
  "bloom",
  "colorGrade",
  "dither",
  "pixelScale",
  "uiOverlay",
];

export const QUALITY_SETTINGS: Record<RenderQualityPreset, RenderQualitySettings> = {
  LOW: { internalWidth: 80, internalHeight: 45, bouncePasses: 0, bloom: false, reflections: false, fog: false, debugGrids: false },
  MEDIUM: { internalWidth: 160, internalHeight: 90, bouncePasses: 1, bloom: true, reflections: true, fog: true, debugGrids: false },
  HIGH: { internalWidth: 320, internalHeight: 180, bouncePasses: 2, bloom: true, reflections: true, fog: true, debugGrids: false },
  BEAUTIFUL: { internalWidth: 320, internalHeight: 180, bouncePasses: 2, bloom: true, reflections: true, fog: true, debugGrids: false },
  DEBUG: { internalWidth: 160, internalHeight: 90, bouncePasses: 1, bloom: false, reflections: true, fog: true, debugGrids: true },
};

export function defaultPixelRealismConfig(viewMode: ViewMode = "OPERATIONAL"): PixelRealismConfig {
  if (viewMode === "BEAUTIFUL") {
    return {
      qualityPreset: "BEAUTIFUL",
      timeOfDay: "golden",
      weather: "clear",
      paletteProfile: "medioevo_archeopunk",
      lightProfile: "cinematic-interior-exterior",
      lightIntensity: 1.18,
      bloomAmount: 0.42,
      dither: true,
      pixelScale: 3,
      hideUiForCapture: true,
      mood: "cinematic",
    };
  }
  if (viewMode === "DEBUG") {
    return {
      qualityPreset: "DEBUG",
      timeOfDay: "night",
      weather: "fog",
      paletteProfile: "cinematic_teal_amber",
      lightProfile: "debug-light-grid",
      lightIntensity: 1,
      bloomAmount: 0,
      dither: false,
      pixelScale: 2,
      hideUiForCapture: false,
      mood: "diagnostic",
    };
  }
  return {
    qualityPreset: "MEDIUM",
    timeOfDay: "day",
    weather: "clear",
    paletteProfile: "medioevo_archeopunk",
    lightProfile: "operational-balanced",
    lightIntensity: 1,
    bloomAmount: 0.22,
    dither: true,
    pixelScale: 2,
    hideUiForCapture: false,
    mood: "operational",
  };
}

export function normalizeQualityForView(config: PixelRealismConfig, viewMode: ViewMode): PixelRealismConfig {
  if (viewMode === "BEAUTIFUL") return { ...config, qualityPreset: "BEAUTIFUL", hideUiForCapture: true };
  if (viewMode === "DEBUG") return { ...config, qualityPreset: "DEBUG", hideUiForCapture: false };
  return config.qualityPreset === "BEAUTIFUL" || config.qualityPreset === "DEBUG"
    ? { ...config, qualityPreset: "MEDIUM", hideUiForCapture: false }
    : config;
}
