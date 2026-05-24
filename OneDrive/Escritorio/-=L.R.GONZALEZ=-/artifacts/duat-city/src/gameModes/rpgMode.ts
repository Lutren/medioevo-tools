import type { CityState } from "../core/types";
import { exportRPGWorld } from "../rpg/worldExport";

export function createRpgModeSummary(city: CityState) {
  const world = exportRPGWorld(city);
  return {
    layer: "city_isometric" as const,
    quests: world.quests.slice(0, 5).map(quest => quest.title),
    factions: world.factions.map(faction => faction.name),
    npcCount: world.npcs.length,
    boundary: "RPG mode uses generated MEDIOEVO data, not protected worlds.",
  };
}
