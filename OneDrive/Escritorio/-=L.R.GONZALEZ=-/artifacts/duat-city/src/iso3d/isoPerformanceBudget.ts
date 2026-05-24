import type { ViewMode } from "../graphics/types";

export interface IsoPerformanceBudget {
  maxVisibleSprites: number;
  maxDynamicLights: number;
  cacheStaticLayers: boolean;
  updateLightEveryFrames: number;
  heatmapResolution: "low" | "medium" | "high";
  reason: string;
}

export function getIsoPerformanceBudget(viewMode: ViewMode): IsoPerformanceBudget {
  switch (viewMode) {
    case "DEBUG":
      return {
        maxVisibleSprites: 360,
        maxDynamicLights: 48,
        cacheStaticLayers: true,
        updateLightEveryFrames: 12,
        heatmapResolution: "high",
        reason: "Debug preserves overlays but separates dynamic agent and qglyph layers.",
      };
    case "BEAUTIFUL":
      return {
        maxVisibleSprites: 520,
        maxDynamicLights: 64,
        cacheStaticLayers: true,
        updateLightEveryFrames: 8,
        heatmapResolution: "medium",
        reason: "Beautiful keeps Vermeer light and billboard population while caching static layers.",
      };
    default:
      return {
        maxVisibleSprites: 280,
        maxDynamicLights: 36,
        cacheStaticLayers: true,
        updateLightEveryFrames: 16,
        heatmapResolution: "low",
        reason: "Operational prioritizes stable interaction and Canvas fallback.",
      };
  }
}

export function applyIsoSpriteBudget<T>(items: T[], budget: IsoPerformanceBudget): T[] {
  return items.slice(0, Math.max(1, budget.maxVisibleSprites));
}
