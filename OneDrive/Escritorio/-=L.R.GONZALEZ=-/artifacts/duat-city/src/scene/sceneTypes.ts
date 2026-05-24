import type { PixelMaterial } from "../physicsField/pixelTypes";
import type { TimeOfDay, WeatherMode } from "../pixelRealism/renderPasses";
import type { LightSourceKind } from "../light/lightTypes";
import type { VibeSceneConfig } from "../vibecoding/vibeTypes";

export type SceneInteractionTool = "select" | "city" | "material" | "light" | "erase";

export type PlayableMaterial =
  | "water"
  | "fire"
  | "smoke"
  | "stone"
  | "wood"
  | "neon";

export type PlayableLightKind = Extract<LightSourceKind, "torch" | "window" | "neon" | "fire" | "magic" | "signal" | "ruin_anomaly">;

export interface PlacedMaterialCell {
  id: string;
  x: number;
  y: number;
  material: PlayableMaterial;
  wetness: number;
  temperature: number;
  light: number;
  active: boolean;
  qState: "00" | "01" | "10" | "11";
  tickPlaced: number;
}

export interface PlacedLightSource {
  id: string;
  x: number;
  y: number;
  kind: PlayableLightKind;
  color: string;
  intensity: number;
  radius: number;
  active: boolean;
  tickPlaced: number;
}

export interface PlayableSceneMetrics {
  activeMaterialCells: number;
  activeLightSources: number;
  particles: number;
  reflectiveCells: number;
  blockedCells: number;
  emissiveCells: number;
  wetCells: number;
  qStateCounts: Record<"00" | "01" | "10" | "11", number>;
}

export interface PlayableSceneState {
  schema: "duat/playable-scene/v1.1";
  version: "1.1";
  tick: number;
  paused: boolean;
  timeOfDay: TimeOfDay;
  weather: WeatherMode;
  activeVibe?: VibeSceneConfig;
  materials: PlacedMaterialCell[];
  lights: PlacedLightSource[];
  selected?: { kind: "material" | "light"; id: string; x: number; y: number };
  lastIntent?: string[];
  metrics: PlayableSceneMetrics;
}

export interface PlayableSceneSave {
  schema: "duat/playable-scene-save/v1.1";
  exportedAt: string;
  scene: PlayableSceneState;
}

export type SceneSerializableMaterial = PlayableMaterial | PixelMaterial;
