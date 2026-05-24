import type { CityContext, CityState, ClimateType, GeographyType } from "../core/types";

export const CLIMATE_OPTIONS: ClimateType[] = ["temperate", "arid", "rainy", "cold", "tropical", "industrial_smog"];
export const GEOGRAPHY_OPTIONS: GeographyType[] = ["river_delta", "mountain_gate", "forest_edge", "coastal_ruins", "desert_crossing", "dense_city"];

export function createDefaultCityContext(): CityContext {
  return {
    schema: "duat.city-context.v1",
    era: "cyber_archeopunk",
    climate: "rainy",
    geography: "river_delta",
    weather: "rain",
    notes: ["default_playable_context"],
  };
}

export function selectCityContext(state: CityState, patch: Partial<Omit<CityContext, "schema">>): CityState {
  return {
    ...state,
    context: {
      ...state.context,
      ...patch,
      schema: "duat.city-context.v1",
      notes: [...state.context.notes, "context_selection_updated"].slice(-12),
    },
  };
}
