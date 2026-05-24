import type { PlayableSceneState } from "../scene/sceneTypes";
import { placeSceneLight, placeSceneMaterial, setSceneTime, setSceneWeather } from "../scene/sceneState";
import type { VibeScenePatch } from "./vibeSceneActions";

export interface VibeGameActionResult {
  scene: PlayableSceneState;
  applied: string[];
}

export function applyVibeGamePatch(scene: PlayableSceneState, patch: VibeScenePatch): VibeGameActionResult {
  let next = scene;
  const applied: string[] = [];
  if (patch.timeOfDay) {
    next = setSceneTime(next, patch.timeOfDay);
    applied.push(`time:${patch.timeOfDay}`);
  }
  if (patch.weather) {
    next = setSceneWeather(next, patch.weather);
    applied.push(`weather:${patch.weather}`);
  }
  for (const material of patch.materials ?? []) {
    next = placeSceneMaterial(next, material.x, material.y, material.material);
    applied.push(`material:${material.material}`);
  }
  for (const light of patch.lights ?? []) {
    next = placeSceneLight(next, light.x, light.y, light.kind);
    applied.push(`light:${light.kind}`);
  }
  return { scene: next, applied };
}

export function undoVibeGamePatch(previous: PlayableSceneState): PlayableSceneState {
  return previous;
}
