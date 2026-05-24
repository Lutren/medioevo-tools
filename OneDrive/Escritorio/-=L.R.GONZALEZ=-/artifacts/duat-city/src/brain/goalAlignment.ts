import type { CityState } from "../core/types";

export function evaluateGoalAlignment(city: CityState) {
  return {
    aligned: city.gate !== "BLOCK" && city.Phi_eff >= 0.55,
    gate: city.gate,
    nextAction: city.gate === "BLOCK" ? "close loops before new action" : "continue local playable game loop",
  };
}
