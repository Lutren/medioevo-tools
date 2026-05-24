import type { CityState } from "../core/types";
import { colorHealth } from "../color/colorGrade";
import { getPaletteProfile } from "../color/paletteEngine";
import { buildLightGridForCity } from "../light/lightPropagation";
import { computeLightMetrics } from "../light/lightMetrics";
import type { LightGrid, LightMetrics } from "../light/lightTypes";
import { applyLightBudget, lightBudgetForPreset, lightUpdateBucket } from "../light/lightBudget";
import type { PixelRealismConfig, RenderQualitySettings } from "./renderPasses";
import { QUALITY_SETTINGS } from "./renderPasses";
import { lightDirtySignature } from "./dirtyRegions";

export interface PixelRealismMetrics {
  qualityPreset: string;
  lightProfile: string;
  palette: string;
  R_light: number;
  Phi_light: number;
  R_color: number;
  Phi_color: number;
  R_pixelField: number;
  Phi_pixelField: number;
  activeMaterialCells: number;
  activeLightCells: number;
  qStateCounts: Record<string, number>;
  vibePreset?: string;
  finite: boolean;
}

export interface PixelRealismRuntime {
  config: PixelRealismConfig;
  quality: RenderQualitySettings;
  lightGrid: LightGrid;
  lightMetrics: LightMetrics;
  metrics: PixelRealismMetrics;
}

interface CachedLightRuntime {
  signature: string;
  bucket: number;
  lightGrid: LightGrid;
  lightMetrics: LightMetrics;
}

let cachedLightRuntime: CachedLightRuntime | undefined;

export function createPixelRealismRuntime(state: CityState, config: PixelRealismConfig): PixelRealismRuntime {
  const quality = QUALITY_SETTINGS[config.qualityPreset];
  const budget = lightBudgetForPreset(config.qualityPreset);
  const signature = lightDirtySignature(state, config);
  const bucket = lightUpdateBucket(state.tick + (state.playableScene?.tick ?? 0), budget);
  const cached = cachedLightRuntime && cachedLightRuntime.signature === signature && cachedLightRuntime.bucket === bucket
    ? cachedLightRuntime
    : undefined;
  const lightGrid = cached?.lightGrid ?? applyLightBudget(buildLightGridForCity(state, {
    width: quality.internalWidth,
    height: quality.internalHeight,
    bouncePasses: Math.min(quality.bouncePasses, budget.maxBouncePasses),
    fog: quality.fog ? fogAmount(config) : 0,
    intensityScale: config.lightIntensity,
  }), budget);
  const lightMetrics = cached?.lightMetrics ?? computeLightMetrics(lightGrid);
  if (!cached) cachedLightRuntime = { signature, bucket, lightGrid, lightMetrics };
  const palette = getPaletteProfile(config.paletteProfile);
  const color = colorHealth(palette.colors);
  const R_pixelField = state.fieldMetrics?.R_field ?? 0;
  const Phi_pixelField = state.fieldMetrics?.Phi_field ?? 1;
  const sceneMetrics = state.playableScene?.metrics;
  const sceneR = sceneMetrics
    ? Math.min(1, sceneMetrics.blockedCells * 0.01 + sceneMetrics.emissiveCells * 0.015 + sceneMetrics.particles * 0.002)
    : 0;
  const qStateCounts = mergeQCounts(state.quaternary?.counts ?? { "00": 0, "01": 0, "10": 0, "11": 0 }, sceneMetrics?.qStateCounts);
  const metrics: PixelRealismMetrics = {
    qualityPreset: config.qualityPreset,
    lightProfile: config.lightProfile,
    palette: palette.id,
    R_light: lightMetrics.R_light,
    Phi_light: lightMetrics.Phi_light,
    R_color: color.R_color,
    Phi_color: color.Phi_color,
    R_pixelField: Math.min(1, R_pixelField + sceneR),
    Phi_pixelField: Math.max(0, Math.min(1, Phi_pixelField - sceneR * 0.2 + (sceneMetrics?.reflectiveCells ?? 0) * 0.003)),
    activeMaterialCells: (state.fieldMetrics?.activeCells ?? 0) + (sceneMetrics?.activeMaterialCells ?? 0),
    activeLightCells: lightMetrics.activeLightCells + (sceneMetrics?.activeLightSources ?? 0),
    qStateCounts,
    vibePreset: config.vibePreset,
    finite: lightMetrics.finite && color.finite && Number.isFinite(R_pixelField) && Number.isFinite(Phi_pixelField),
  };
  return { config, quality, lightGrid, lightMetrics, metrics };
}

export function pixelRealismHandoff(metrics: PixelRealismMetrics): PixelRealismMetrics {
  return { ...metrics, qStateCounts: { ...metrics.qStateCounts } };
}

function fogAmount(config: PixelRealismConfig): number {
  if (config.weather === "fog" || config.weather === "jungle_mist") return 0.18;
  if (config.weather === "rain") return 0.12;
  if (config.weather === "snow") return 0.08;
  if (config.weather === "desert_haze") return 0.1;
  return 0.03;
}

function mergeQCounts(base: Record<string, number>, scene?: Record<string, number>): Record<string, number> {
  return {
    "00": (base["00"] ?? 0) + (scene?.["00"] ?? 0),
    "01": (base["01"] ?? 0) + (scene?.["01"] ?? 0),
    "10": (base["10"] ?? 0) + (scene?.["10"] ?? 0),
    "11": (base["11"] ?? 0) + (scene?.["11"] ?? 0),
  };
}
