import type { CityState, Handoff } from "./types";
import { computeNextAction } from "./metrics";
import { createAudioGameFeelSnapshot } from "../audio/gameFeelAdapter";

export function generateHandoff(state: CityState): Handoff {
  const activeTasks = state.tasks
    .filter(t => t.status === "active")
    .map(t => t.title)
    .slice(0, 5);

  const risks: string[] = [];
  if (state.R > 0.60) risks.push("Critical R level — city near saturation");
  if (state.resources.food < 20) risks.push("Food shortage — agents hunger rising");
  if (state.resources.trust < 10) risks.push("Trust collapse — social unrest");
  if (state.resources.signal < 5) risks.push("Signal loss — observatory needed");

  const ruinCount = state.buildings.filter(b => b.type === "ruin").length;
  if (ruinCount > 0) risks.push(`${ruinCount} ruin(s) unresolved — R accumulating`);

  const blockedAgents = state.agents.filter(a => a.gate === "BLOCK").length;
  if (blockedAgents > 0) risks.push(`${blockedAgents} agent(s) blocked`);

  const handoff: Handoff = {
    schema: "duat-agent-city/handoff/v1",
    tick: state.tick,
    R: state.R,
    Phi_eff: state.Phi_eff,
    regime: state.regime,
    gate: state.gate,
    city: {
      agents: state.agents.length,
      buildings: state.buildings.length,
      resources: { ...state.resources },
    },
    active_tasks: activeTasks,
    risks,
    rpg_export_ready: state.buildings.length >= 3,
    next_action: computeNextAction(state.gate, state.regime),
    open_loops: [
      "Validate FibMob LOD against DUAT main renderer",
      "Compare residue benchmark with real DUAT channel fusion",
      "Keep formal-lab boundary: no physical magnetism claims",
    ],
  };

  if (state.quaternary) {
    handoff.quaternary_timing = {
      R: state.quaternary.R,
      Phi_eff: state.quaternary.Phi_eff,
      gate: state.quaternary.gate,
      counts: state.quaternary.counts,
      avgFrequency: state.quaternary.avgFrequency,
      avgPermanence: state.quaternary.avgPermanence,
      avgStability: state.quaternary.avgStability,
      next_action: state.quaternary.next_action,
    };
  }

  if (state.pixelRealism) {
    handoff.pixel_realism = {
      ...state.pixelRealism,
      qStateCounts: { ...state.pixelRealism.qStateCounts },
    };
  }

  const audio = createAudioGameFeelSnapshot(state);
  handoff.audio_gamefeel = {
    enabled: audio.enabled,
    R_audio: audio.metrics.R_audio,
    Phi_audio: audio.metrics.Phi_audio,
    cueCount: audio.metrics.cueCount,
    proceduralOnly: true,
    requiresUserGesture: true,
    externalSamplesCopied: false,
    publicationAllowed: false,
  };

  return handoff;
}
