import type { CityState } from "../core/types";

export function compileResidueDreamCycle(city: CityState) {
  return {
    enabled: false,
    designOnly: true,
    residueInputs: city.witnesslog.slice(-5).map(entry => entry.summary),
    note: "Dream cycle stores residue prompts only; it does not execute Wabi or cloud models.",
  };
}
