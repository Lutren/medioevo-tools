import { generateHandoff } from "../core/handoff";
import { tickEngine } from "../sim/engine";
import { stepPlayableScene } from "../scene/sceneState";
import { applyVibeGamePatch } from "../vibecoding/vibeGameActions";
import type { VibeCommandParseResult } from "../vibecoding/vibeCommandParser";
import type { GameState } from "./gameTypes";
import { computeGameOsitMetrics } from "./gameState";
import { applyMaterialGameplayToAgents } from "./gameSystems";
import { createAudioGameFeelSnapshot } from "../audio/gameFeelAdapter";

export function tickGame(game: GameState, command?: VibeCommandParseResult): GameState {
  const patchedScene = command ? applyVibeGamePatch(game.scene, command.scenePatch).scene : game.scene;
  const scene = patchedScene.paused ? patchedScene : stepPlayableScene(patchedScene, game.city.width, game.city.height);
  const cityBase = tickEngine({ ...game.city, playableScene: scene }, { enablePixelField: true, enableAgentPhysics: true });
  const city = { ...cityBase, agents: applyMaterialGameplayToAgents(cityBase.agents, scene), playableScene: scene };
  const next: GameState = {
    ...game,
    scene,
    city,
    actors: city.agents,
    resources: city.resources,
    time: city.tick,
    weather: scene.weather,
    vibeHistory: command ? [...game.vibeHistory, command].slice(-20) : game.vibeHistory,
    audioGameFeel: createAudioGameFeelSnapshot(city),
    handoff: generateHandoff(city),
  };
  return { ...next, ositMetrics: computeGameOsitMetrics(next) };
}
