import type { CityState, ResourceKey } from "../core/types";
import type { CityPolicyPatch, GameModeState } from "./gameModeTypes";

const POLICY_RESOURCE: Record<CityPolicyPatch["policy"], ResourceKey> = {
  housing: "trust",
  food: "food",
  knowledge: "knowledge",
  safety: "materials",
  signal: "signal",
};

export function applyCityPolicy(mode: GameModeState, city: CityState, patch: CityPolicyPatch): { mode: GameModeState; city: CityState } {
  const resource = POLICY_RESOURCE[patch.policy];
  const delta = clampDelta(patch.delta);
  return {
    mode: {
      ...mode,
      policies: { ...mode.policies, [patch.policy]: finite((mode.policies[patch.policy] ?? 0) + delta) },
      resourcesDelta: { ...mode.resourcesDelta, [resource]: finite((mode.resourcesDelta[resource] ?? 0) + delta * 10) },
      notes: [...mode.notes, `Policy ${patch.policy} shifted by ${delta}.`].slice(-12),
    },
    city: {
      ...city,
      resources: { ...city.resources, [resource]: Math.max(0, city.resources[resource] + delta * 10) },
      agents: city.agents.map(agent => ({ ...agent, trust: finite(agent.trust + delta * 0.02), R: finite(Math.max(0, agent.R - delta * 0.01)) })),
    },
  };
}

function clampDelta(value: number): number {
  return Math.max(-1, Math.min(1, Number.isFinite(value) ? value : 0));
}

function finite(value: number): number {
  return Number(value.toFixed(3));
}
