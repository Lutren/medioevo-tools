import type { Gate, Mode, TileType } from "../core/types";
import type { ViewMode } from "../graphics/types";

export const ENABLE_ISO3D_RENDERER_DEFAULT = false;

export type IsoRendererMode = "canvas" | "iso3d";
export type IsoLayerKey = "terrain" | "buildings" | "lights" | "agents" | "heatmap" | "qglyphs" | "ui";
export type IsoLightProfile = "vermeer" | "caravaggio" | "van_eyck" | "medioevo";

export interface IsoVector2 {
  x: number;
  y: number;
}

export interface IsoVector3 extends IsoVector2 {
  z: number;
}

export interface IsoCamera {
  position: IsoVector3;
  target: IsoVector3;
  zoom: number;
  yaw: number;
  pitch: number;
  modePreset: Mode | "HORMIGUERO" | "PRESIDENT" | "METROIDVANIA";
}

export interface IsoGridConfig {
  width: number;
  height: number;
  tileWidth: number;
  tileHeight: number;
  elevationScale: number;
}

export interface IsoWorldTile {
  id: string;
  tileId?: number;
  grid: IsoVector2;
  world: IsoVector3;
  type: TileType | "material" | "prop" | "agent" | "glyph";
  elevation: number;
  depth: number;
  R: number;
  Phi_eff: number;
  gate?: Gate;
}

export interface IsoLightSource {
  id: string;
  kind: "window" | "sun" | "moon" | "fire" | "neon" | "agent" | "ambient";
  position: IsoVector3;
  color: { r: number; g: number; b: number };
  intensity: number;
  radius: number;
  softness: number;
}

export interface IsoBillboard {
  id: string;
  kind: "agent" | "building" | "prop" | "material" | "particle" | "qglyph";
  label: string;
  position: IsoVector3;
  size: IsoVector2;
  anchor: IsoVector2;
  spriteKey: string;
  tint: string;
  brightness: number;
  facesCamera: boolean;
  selected: boolean;
  hoverable: boolean;
  depth: number;
  fallback: true;
  metadata: Record<string, string | number | boolean>;
}

export interface IsoOverlay {
  id: string;
  layer: "heatmap" | "qstate" | "selection" | "task";
  position: IsoVector3;
  radius: number;
  color: string;
  alpha: number;
}

export interface IsoScene {
  id: string;
  rendererMode: IsoRendererMode;
  featureFlagEnabled: boolean;
  canvasFallbackAvailable: true;
  camera: IsoCamera;
  grid: IsoGridConfig;
  tiles: IsoWorldTile[];
  billboards: IsoBillboard[];
  lights: IsoLightSource[];
  overlays: IsoOverlay[];
  viewMode: ViewMode;
  mode: Mode;
  lightProfile: IsoLightProfile;
  metrics: IsoRenderMetrics;
}

export interface IsoRenderMetrics {
  visibleSprites: number;
  drawCallsEstimate: number;
  activeLightCells: number;
  activeMaterialCells: number;
  cacheHitRatio: number;
  avgFrameCostMs: number;
  p95FrameCostMs: number;
  R_iso: number;
  Phi_iso: number;
}

export interface IsoLayerCacheEntry {
  key: IsoLayerKey;
  dirtyKey: string;
  reused: boolean;
  lastUpdatedTick: number;
}

export interface IsoRendererConfig {
  enabled: boolean;
  mode: IsoRendererMode;
  populateBillboards: boolean;
  qOverlay: boolean;
  heatmapOverlay: boolean;
  lightProfile: IsoLightProfile;
  quality: "LOW" | "MEDIUM" | "HIGH" | "BEAUTIFUL" | "DEBUG";
}
