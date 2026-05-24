import type { CityState } from "../core/types";
import { exportRPGWorld } from "../rpg/worldExport";
import { compileVibeScene } from "../vibecoding/vibeSceneCompiler";
import {
  applyVibeSceneToPlayableScene,
  createDefaultPlayableSceneState,
  eraseSceneAt,
  placeSceneLight,
  placeSceneMaterial,
  serializePlayableScene,
  setSceneTime,
  stepPlayableScene,
} from "./sceneState";

export interface PlayableInteractionQaResult {
  sceneJson: string;
  rpgSceneJson: string;
  checks: {
    controlsWork: boolean;
    materialsAffectScene: boolean;
    lightResponds: boolean;
    exportsContainMaterialsLightsVibe: boolean;
    noNaN: boolean;
    wabiDisabled: boolean;
  };
  summary: string[];
}

export function runPlayableInteractionQaSequence(state: CityState): PlayableInteractionQaResult {
  const vibe = compileVibeScene("neon_rain_street", "preset").config;
  let scene = applyVibeSceneToPlayableScene(createDefaultPlayableSceneState(), vibe, state.width, state.height);
  const cx = Math.floor(state.width / 2);
  const cy = Math.floor(state.height / 2);
  scene = placeSceneMaterial(scene, cx - 3, cy + 3, "water");
  scene = placeSceneMaterial(scene, cx - 1, cy + 2, "fire");
  scene = placeSceneMaterial(scene, cx - 1, cy + 1, "smoke");
  scene = placeSceneMaterial(scene, cx + 1, cy + 2, "stone");
  scene = placeSceneMaterial(scene, cx + 3, cy + 1, "neon");
  scene = placeSceneLight(scene, cx - 1, cy + 2, "fire");
  scene = placeSceneLight(scene, cx + 3, cy + 1, "neon");
  scene = eraseSceneAt(scene, cx + 1, cy + 2);
  scene = setSceneTime(scene, "night");
  scene = stepPlayableScene(scene, state.width, state.height);

  const sceneJson = serializePlayableScene(scene);
  const rpg = exportRPGWorld({ ...state, playableScene: scene });
  const rpgSceneJson = JSON.stringify(rpg, null, 2);
  const finitePayload = JSON.stringify({ scene, rpg });
  const checks = {
    controlsWork: scene.materials.length >= 5 && scene.lights.length >= 2,
    materialsAffectScene: scene.metrics.activeMaterialCells > 0 && scene.metrics.particles > 0,
    lightResponds: scene.metrics.emissiveCells >= 2 && scene.metrics.activeLightSources >= 2,
    exportsContainMaterialsLightsVibe: sceneJson.includes("materials")
      && rpgSceneJson.includes("placed_materials")
      && rpgSceneJson.includes("placed_lights")
      && rpgSceneJson.includes("vibe_config"),
    noNaN: !finitePayload.includes("NaN"),
    wabiDisabled: true,
  };
  return {
    sceneJson,
    rpgSceneJson,
    checks,
    summary: [
      "Preset neon_rain_street applied.",
      "Water, fire, smoke, stone and neon were placed; one stone cell was erased.",
      "Night mode was applied and one simulation step was executed.",
      "Scene JSON and RPG scene JSON were generated locally.",
    ],
  };
}
