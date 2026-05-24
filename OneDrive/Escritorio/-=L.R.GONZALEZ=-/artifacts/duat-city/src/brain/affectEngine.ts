import type { CityState } from "../core/types";

export function estimateAffectState(city: CityState) {
  return {
    mood: city.Phi_eff > 0.75 ? "focused" : city.R > 0.45 ? "strained" : "working",
    tension: Number(Math.max(0, Math.min(1, city.R)).toFixed(3)),
  };
}
