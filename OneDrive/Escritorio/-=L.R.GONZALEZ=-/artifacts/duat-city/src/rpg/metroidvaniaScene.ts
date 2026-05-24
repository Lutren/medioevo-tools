import type { CityState } from "../core/types";
import { createMetroidvaniaModeScene } from "../gameModes/metroidvaniaMode";

export type MetroidvaniaScene = ReturnType<typeof createMetroidvaniaModeScene> & {
  questIds: string[];
  dialogueIds: string[];
};

export function buildMetroidvaniaScene(city: CityState, questIds: string[] = []): MetroidvaniaScene {
  return {
    ...createMetroidvaniaModeScene(city),
    questIds,
    dialogueIds: city.agents.slice(0, 4).map(agent => `dialogue:${agent.id}`),
  };
}
