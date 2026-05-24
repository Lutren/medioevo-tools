import type { PlayableLightKind, PlayableMaterial } from "../scene/sceneTypes";
import type { TimeOfDay, WeatherMode } from "../pixelRealism/renderPasses";

export interface VibeScenePatch {
  styleProfile?: string;
  timeOfDay?: TimeOfDay;
  weather?: WeatherMode;
  materials?: Array<{ x: number; y: number; material: PlayableMaterial }>;
  lights?: Array<{ x: number; y: number; kind: PlayableLightKind }>;
  buildings?: string[];
  agents?: number;
  quests?: string[];
  vibePreset?: string;
}

export const EMPTY_VIBE_SCENE_PATCH: VibeScenePatch = {
  materials: [],
  lights: [],
  buildings: [],
  quests: [],
};
