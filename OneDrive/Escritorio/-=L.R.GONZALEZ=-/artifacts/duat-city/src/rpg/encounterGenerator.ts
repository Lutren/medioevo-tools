import type { CityState } from "../core/types";
import type { RPGEncounter } from "./rpgTypes";
import { uid, seededRandom } from "../core/math";

const ENCOUNTER_TEMPLATES: Omit<RPGEncounter, "id">[] = [
  {
    type: "social",
    title: "Market Dispute",
    description: "Two traders argue over scarce materials. The tension is rising.",
    outcome_approve: "Mediation succeeds. Trust +5, conflict resolved.",
    outcome_block: "Dispute escalates. Trust -8, R +0.04.",
    R_delta: 0.02,
  },
  {
    type: "resource_conflict",
    title: "Food Shortage Queue",
    description: "Agents line up at the garden but supply is short. Tempers flare.",
    outcome_approve: "Orderly rationing implemented. Hunger crisis managed.",
    outcome_block: "Riot breaks out. Food -15, R +0.08.",
    R_delta: 0.05,
  },
  {
    type: "ruin_anomaly",
    title: "Void Signal Detected",
    description: "A ruin pulses with μ=0 energy. Archivists and Ruin Seekers both want access.",
    outcome_approve: "Controlled investigation. Knowledge +10, ruin R reduced.",
    outcome_block: "Uncontrolled entry. Signal spike, R +0.06.",
    R_delta: 0.04,
  },
  {
    type: "archive_discovery",
    title: "Lost Archive Fragment",
    description: "A courier finds a data fragment from a previous DUAT cycle. Authenticate it?",
    outcome_approve: "Fragment authenticated. Knowledge +20, Phi_eff +0.03.",
    outcome_block: "Fragment quarantined. Investigation pending.",
    R_delta: -0.02,
  },
  {
    type: "market_negotiation",
    title: "Resource Exchange Offer",
    description: "Market Circle proposes a materials-for-food swap. Terms are complex.",
    outcome_approve: "Deal struck. Materials +15, food +20.",
    outcome_block: "Deal collapses. Market Circle reputation -0.1.",
    R_delta: 0.01,
  },
];

export function generateEncounters(state: CityState): RPGEncounter[] {
  const count = Math.min(3 + Math.floor(state.buildings.length / 3), 5);
  const rng = seededRandom(`rpg-encounters:${state.tick}:${state.R.toFixed(6)}:${state.buildings.length}:${state.agents.length}`);
  const shuffled = [...ENCOUNTER_TEMPLATES];
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(rng() * (i + 1));
    [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
  }
  return shuffled.slice(0, count).map(e => ({ id: uid(rng), ...e }));
}
