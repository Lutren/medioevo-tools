import type { WitnessEntry, CityState } from "./types";
import { computeGate } from "./metrics";

let _counter = 0;

export function makeWitnessId(): string {
  return `W${String(++_counter).padStart(5, "0")}`;
}

export function addWitnessEntry(
  state: CityState,
  type: string,
  summary: string,
  evidence: string[] = []
): CityState {
  const entry: WitnessEntry = {
    id: makeWitnessId(),
    tick: state.tick,
    type,
    summary,
    evidence,
    R: state.R,
    Phi_eff: state.Phi_eff,
    gate: computeGate(state.R),
  };
  const log = [...state.witnesslog, entry];
  return { ...state, witnesslog: log.slice(-200) };
}

export function getWitnessTail(state: CityState, n = 20): WitnessEntry[] {
  return state.witnesslog.slice(-n);
}
