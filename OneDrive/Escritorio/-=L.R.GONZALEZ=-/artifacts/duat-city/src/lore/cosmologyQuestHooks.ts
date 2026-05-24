import type { CosmologyQuestHook } from "./cosmologyTypes";
import { compileInWorldCosmology } from "./medioevoCosmology";

export function generateCosmologyQuestHooks(): CosmologyQuestHook[] {
  return compileInWorldCosmology().concepts.map(concept => ({
    id: `cosmo:${concept.id}`,
    title: titleFor(concept.id),
    mechanic: concept.mechanicUse.join(","),
    boundary: concept.boundary,
  }));
}

function titleFor(id: string): string {
  const titles: Record<string, string> = {
    apparent_matter_fluid: "Map the pressure of apparent matter",
    gravity_as_compression: "Stabilize the compression gate",
    fire_event_conversion: "Contain the visible conversion fire",
    photon_observability_fluid: "Trace the observability carrier",
    self_observing_universe: "Ask the city what it remembers",
    noumenon_phenomenon_tension: "Separate appearance from evidence",
    collapse_release_cycle: "Interrupt the ruin release cycle",
  };
  return titles[id] ?? "Investigate formal-lab myth";
}
