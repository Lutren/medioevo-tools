import type { CityState } from "../core/types";

export function computeCerebellumTiming(city: CityState) {
  const q = city.quaternary;
  return {
    tick: city.tick,
    cadence: q ? Number((q.avgStability * 1000).toFixed(2)) : 1000,
    stable: (q?.avgStability ?? 0.8) > 0.5,
  };
}
