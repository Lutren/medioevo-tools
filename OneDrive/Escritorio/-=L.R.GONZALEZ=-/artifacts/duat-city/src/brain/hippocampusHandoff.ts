import type { CityState } from "../core/types";
import { generateHandoff } from "../core/handoff";

export function createHippocampusHandoff(city: CityState) {
  return {
    schema: "duat/hippocampus-handoff/v1.3",
    tick: city.tick,
    summary: `Stored handoff at tick ${city.tick} with ${city.agents.length} agents and gate ${city.gate}.`,
    handoff: generateHandoff(city),
  };
}
