import type { CityState } from "../core/types";

export function summarizeSocialCortex(city: CityState) {
  const avgTrust = city.agents.length ? city.agents.reduce((sum, agent) => sum + agent.trust, 0) / city.agents.length : 0;
  return {
    agents: city.agents.length,
    avgTrust: Number(avgTrust.toFixed(3)),
    factionSignal: avgTrust > 0.6 ? "cohesive" : "fragile",
  };
}
