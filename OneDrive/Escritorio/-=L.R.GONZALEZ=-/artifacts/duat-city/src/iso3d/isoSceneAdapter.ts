import type { CityState, Mode } from "../core/types";
import type { ViewMode } from "../graphics/types";
import { createIsoCamera } from "./isoCamera";
import { createIsoGrid } from "./isoGrid";
import { createIsoLightSources } from "./isoLighting";
import { computeIsoRenderMetrics } from "./isoRenderMetrics";
import { createPixelBillboardPopulation, flattenBillboardPopulation } from "./isoSpriteLayer";
import { updateIsoLayerCache } from "./isoLayerCache";
import type { IsoLayerCacheState } from "./isoLayerCache";
import { applyIsoSpriteBudget, getIsoPerformanceBudget } from "./isoPerformanceBudget";
import { buildIsoWorldTiles } from "./isoWorld";
import type { IsoRendererConfig, IsoScene } from "./isoTypes";

export interface IsoSceneAdapterOptions {
  mode: Mode;
  viewMode: ViewMode;
  config: IsoRendererConfig;
  previousCache?: IsoLayerCacheState;
}

export function createIsoSceneAdapter(state: CityState, options: IsoSceneAdapterOptions): IsoScene {
  const grid = createIsoGrid(state.width, state.height);
  const cameraMode = options.mode === "OSIT" && options.viewMode === "DEBUG" ? "HORMIGUERO" : options.mode;
  const camera = createIsoCamera(cameraMode);
  const lights = createIsoLightSources(state, grid, options.config.lightProfile);
  const cache = updateIsoLayerCache(options.previousCache, state);
  const population = createPixelBillboardPopulation(state, grid, camera, lights);
  const budget = getIsoPerformanceBudget(options.viewMode);
  const billboards = options.config.populateBillboards
    ? applyIsoSpriteBudget(flattenBillboardPopulation(population), budget)
    : [];
  const tiles = buildIsoWorldTiles(state, grid);
  const overlays = options.config.heatmapOverlay
    ? tiles.filter(tile => tile.R > 0.35).slice(0, 80).map(tile => ({
      id: `heat-${tile.id}`,
      layer: "heatmap" as const,
      position: tile.world,
      radius: 10 + tile.R * 16,
      color: tile.R > 0.55 ? "#c86b5c" : "#d7b95e",
      alpha: Math.min(0.72, 0.18 + tile.R),
    }))
    : [];
  const metrics = computeIsoRenderMetrics(state, billboards, cache.hitRatio);

  return {
    id: `iso3d-${state.tick}-${options.mode}-${options.viewMode}`,
    rendererMode: options.config.enabled && options.config.mode === "iso3d" ? "iso3d" : "canvas",
    featureFlagEnabled: options.config.enabled,
    canvasFallbackAvailable: true,
    camera,
    grid,
    tiles,
    billboards,
    lights,
    overlays,
    viewMode: options.viewMode,
    mode: options.mode,
    lightProfile: options.config.lightProfile,
    metrics,
  };
}

export function createDefaultIsoRendererConfig(viewMode: ViewMode): IsoRendererConfig {
  return {
    enabled: false,
    mode: "canvas",
    populateBillboards: true,
    qOverlay: viewMode === "DEBUG",
    heatmapOverlay: viewMode !== "BEAUTIFUL",
    lightProfile: "vermeer",
    quality: viewMode === "BEAUTIFUL" ? "BEAUTIFUL" : viewMode === "DEBUG" ? "DEBUG" : "MEDIUM",
  };
}
