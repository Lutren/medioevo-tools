import type { CityState } from "../core/types";

export interface CityMetroidvaniaTransition {
  schema: "duat/city-metroidvania-transition/v1.3";
  from: "city_isometric";
  to: "metroidvania";
  gateId: string;
  carriedQuestIds: string[];
  allowed: boolean;
  reason: string;
}

export function createCityToMetroidvaniaTransition(city: CityState, gateId?: string, questIds: string[] = []): CityMetroidvaniaTransition {
  const gate = gateId
    ? city.buildings.find(building => building.id === gateId)
    : city.buildings.find(building => ["gatehouse", "ruin", "archive"].includes(building.type));
  const allowed = !gate || gate.gate !== "BLOCK";
  return {
    schema: "duat/city-metroidvania-transition/v1.3",
    from: "city_isometric",
    to: "metroidvania",
    gateId: gate?.id ?? "procedural-gate",
    carriedQuestIds: questIds,
    allowed,
    reason: allowed ? "Transition gate is playable." : "ActionGate blocks transition until evidence improves.",
  };
}
