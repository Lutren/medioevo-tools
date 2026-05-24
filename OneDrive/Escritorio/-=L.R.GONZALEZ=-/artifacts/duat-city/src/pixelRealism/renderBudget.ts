import type { CityState } from "../core/types";
import { lightBudgetForPreset, type LightBudget } from "../light/lightBudget";
import type { PixelRealismConfig, RenderQualityPreset } from "./renderPasses";

export interface RenderBudget {
  preset: RenderQualityPreset;
  light: LightBudget;
  maxParticles: number;
  debugOverlayEnabled: boolean;
}

export function renderBudgetForConfig(config: PixelRealismConfig): RenderBudget {
  const light = lightBudgetForPreset(config.qualityPreset);
  return {
    preset: config.qualityPreset,
    light,
    maxParticles: light.particleCap,
    debugOverlayEnabled: config.qualityPreset === "DEBUG",
  };
}

export function capParticles(count: number, config: PixelRealismConfig): number {
  const budget = renderBudgetForConfig(config);
  if (!Number.isFinite(count)) return 0;
  return Math.max(0, Math.min(Math.floor(count), budget.maxParticles));
}

export function shouldRunReflectionPass(state: CityState, config: PixelRealismConfig): boolean {
  const scene = state.playableScene;
  const sceneReflective = Boolean(scene?.materials.some(cell => cell.material === "water" || cell.wetness > 0.35));
  const cityWater = state.tiles.some(tile => tile.type === "water");
  if (!sceneReflective && !cityWater) return false;
  return config.qualityPreset !== "LOW" && lightBudgetForPreset(config.qualityPreset).reflectionScale > 0;
}
