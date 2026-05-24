import type { CityState } from "../core/types";
import { createCity } from "../sim/city";
import { generateHandoff } from "../core/handoff";
import { createDefaultPlayableSceneState } from "../scene/sceneState";
import { createAudioGameFeelSnapshot } from "../audio/gameFeelAdapter";
import type { GameState } from "./gameTypes";

export function createGameState(city: CityState = createCity()): GameState {
  const scene = city.playableScene ?? createDefaultPlayableSceneState();
  return {
    schema: "duat.game_state.v1_2",
    scene,
    city,
    actors: city.agents,
    quests: [],
    resources: city.resources,
    camera: { x: city.width / 2, y: city.height / 2, zoom: 1.8 },
    time: city.tick,
    weather: scene.weather,
    ositMetrics: {
      R_material: 0,
      Phi_material: 1,
      R_light: 0,
      Phi_light: 1,
      activeCells: scene.metrics.activeMaterialCells,
      skippedCells: 0,
      materialEvents: 0,
    },
    audioGameFeel: createAudioGameFeelSnapshot({ ...city, playableScene: scene }),
    vibeHistory: [],
    handoff: generateHandoff(city),
  };
}

export function computeGameOsitMetrics(game: Pick<GameState, "scene" | "city">): GameState["ositMetrics"] {
  const activeCells = game.scene.metrics.activeMaterialCells;
  const lightCells = game.scene.metrics.activeLightSources + game.scene.metrics.emissiveCells;
  const hazards = game.scene.materials.filter(cell => cell.material === "fire" || cell.material === "smoke").length;
  const R_material = clamp01(activeCells / 400 + hazards * 0.025);
  const Phi_material = clamp01(1 - R_material * 0.65 + game.scene.metrics.qStateCounts["10"] * 0.005);
  const R_light = clamp01(lightCells / 24 + game.scene.metrics.qStateCounts["11"] * 0.01);
  const Phi_light = clamp01(1 - R_light * 0.5 + game.scene.metrics.reflectiveCells * 0.002);
  return {
    R_material,
    Phi_material,
    R_light,
    Phi_light,
    activeCells,
    skippedCells: Math.max(0, game.city.width * game.city.height - activeCells),
    materialEvents: game.scene.materials.filter(cell => cell.active).length,
  };
}

function clamp01(value: number): number {
  return Number(Math.max(0, Math.min(1, Number.isFinite(value) ? value : 0)).toFixed(3));
}
