import type { CityState } from "../core/types";
import type { RPGQuest } from "./rpgTypes";
import { exportRPGWorld } from "./worldExport";

export function createRpgQuestRuntime(city: CityState) {
  const world = exportRPGWorld(city);
  return {
    schema: "duat/rpg-quest-runtime/v1.3",
    activeQuests: world.quests.slice(0, 8),
    hazards: world.environmental_hazards ?? [],
    cityEvents: city.events.slice(-8).map(event => event.title),
  };
}

export function carryQuestToMetroidvania(quest: RPGQuest) {
  return {
    id: quest.id,
    title: quest.title,
    sideViewObjective: quest.type === "exploration" ? "Reach the locked passage." : "Find the evidence marker.",
    dialogueSeed: quest.hook,
  };
}
