import type { CityState } from "../core/types";
import { compileInWorldCosmology } from "../lore/medioevoCosmology";

export function compileLoreFromWorld(state: CityState) {
  const cosmology = compileInWorldCosmology();
  return {
    schema: "duat/lore-compiler/v1.3",
    tick: state.tick,
    tags: ["MEDIOEVO-original", "IN_WORLD_COSMOLOGY", state.regime],
    motifs: cosmology.concepts.slice(0, 6).map(concept => concept.id),
    publicClaimAllowed: false,
  };
}
