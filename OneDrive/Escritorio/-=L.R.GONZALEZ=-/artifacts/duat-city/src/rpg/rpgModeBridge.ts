import type { CityState } from "../core/types";
import { generateNpcUtterance } from "../language/npcSpeechEngine";
import { createCityToMetroidvaniaTransition } from "./cityToMetroidvaniaTransition";
import { buildMetroidvaniaScene } from "./metroidvaniaScene";

export function createRpgModeBridge(city: CityState) {
  const questRuntime = {
    schema: "duat/rpg-quest-runtime/v1.3",
    activeQuests: city.buildings.slice(0, 4).map((building, index) => ({
      id: `bridge-quest-${building.id}`,
      title: index === 0 ? "Cross the evidence gate" : `Investigate ${building.name}`,
    })),
    hazards: city.fieldSummary?.hazards ?? [],
    cityEvents: city.events.slice(-8).map(event => event.title),
  };
  const questIds = questRuntime.activeQuests.slice(0, 3).map(quest => quest.id);
  const transition = createCityToMetroidvaniaTransition(city, undefined, questIds);
  const scene = buildMetroidvaniaScene(city, questIds);
  const dialogue = city.agents.slice(0, 3).map(agent => generateNpcUtterance(agent, city, "rpg"));
  return {
    schema: "duat/rpg-metroidvania-bridge/v1.3",
    cityLayer: "isometric",
    outsideCityLayer: "metroidvania",
    transition,
    metroidvaniaScene: scene,
    questRuntime,
    npcDialogue: dialogue,
    boundary: "Original MEDIOEVO bridge; no protected world copied.",
  };
}
