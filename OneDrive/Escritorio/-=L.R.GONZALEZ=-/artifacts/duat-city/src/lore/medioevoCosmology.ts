import type { CosmologyProfile } from "./cosmologyTypes";
import type { CosmologyBoundary } from "./cosmologyTypes";

export function compileInWorldCosmology(): CosmologyProfile {
  return {
    schema: "duat/medioevo-cosmology/v1.3",
    publicClaimAllowed: false,
    scienceBoundaryNote: "This is MEDIOEVO in-world lore/formal-lab material, not a real physics claim or public science assertion.",
    concepts: [
      concept("apparent_matter_fluid", "Materia aparente", ["materials", "anomalies"], "Matter is treated in-world as a primordial medium under pressure."),
      concept("gravity_as_compression", "Compression gravity myth", ["era_progression", "rituals"], "Movement and field pressure compress the medium in fictional DUAT lore."),
      concept("fire_event_conversion", "Fire event", ["fire", "audio", "light", "quests"], "Fire is a visible conversion event: bloom, heat, smoke and residue."),
      concept("photon_observability_fluid", "Observability carrier", ["light", "source_cards"], "Light carries observability through the fictional medium."),
      concept("self_observing_universe", "Self-observing system", ["agents", "OSIT", "handoff"], "The world narratively observes itself through agents and gates."),
      concept("noumenon_phenomenon_tension", "Noumenon/phenomenon tension", ["language", "dialogue"], "Characters separate what appears from what can be evidenced."),
      concept("collapse_release_cycle", "Collapse/release cycle", ["ruins", "dream_cycle"], "Pressure, cooling and release drive mythic ruin events."),
    ],
  };
}

function concept(id: string, label: string, mechanicUse: string[], loreText: string) {
  const boundary: CosmologyBoundary[] = ["IN_WORLD_COSMOLOGY", "FORMAL_LAB", "PUBLIC_CLAIM_BLOCKED"];
  return {
    id,
    label,
    mechanicUse,
    loreText,
    boundary,
  };
}
