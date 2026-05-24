import { generateHandoff } from "../core/handoff";
import type { BrainRuntime, BrainRuntimeInput, BrainSystemStatus } from "./brainTypes";
import { createHippocampusHandoff } from "./hippocampusHandoff";
import { evaluatePrefrontalActionGate } from "./prefrontalActionGate";
import { filterAttentionGhostEvent } from "./attentionGhostGate";
import { runTruthGate } from "./truthGate";
import { createAudioGameFeelSnapshot } from "../audio/gameFeelAdapter";
import { compileOSITFormulaProfile } from "../osit/ositIntegration";

export function createBrainRuntime(input: BrainRuntimeInput): BrainRuntime {
  const city = input.city;
  const languageR = input.languageMetrics?.R_language ?? 0;
  const languagePhi = input.languageMetrics?.Phi_language ?? 1;
  const audioGameFeel = input.audioGameFeel ?? createAudioGameFeelSnapshot(city);
  const ositFormulaProfile = input.ositFormulaProfile ?? compileOSITFormulaProfile(city);
  return {
    schema: "duat/brain-runtime/v1.3",
    tick: city.tick,
    systems: {
      hippocampus: status("hippocampus", city.R * 0.5, city.Phi_eff, createHippocampusHandoff(city).summary),
      prefrontal: status("prefrontal", city.R, city.Phi_eff, evaluatePrefrontalActionGate({ action: "local_game_os_tick", risk: city.R }).reason),
      attention: status("attention", city.R * 0.6, city.Phi_eff, filterAttentionGhostEvent({ id: "tick", R: city.R, signal: city.Phi_eff }).reason),
      crossModal: status("cross_modal", 0.08, 0.86, "Visual/audio/physics/language adapters aligned by typed state."),
      truthGate: status("truth_gate", runTruthGate(["tests", "typecheck"]).R, runTruthGate(["tests", "typecheck"]).Phi_eff, "TruthGate requires local evidence before claims."),
      languageCortex: status("language_cortex", languageR, languagePhi, "Template language cortex connected."),
      audioGameFeel: status("audio_gamefeel", audioGameFeel.metrics.R_audio, audioGameFeel.metrics.Phi_audio, "Procedural audio/game-feel adapter is connected and off until local user gesture."),
      ositFormulaLab: status("osit_formula_lab", ositFormulaProfile.R_formula, ositFormulaProfile.Phi_formula, "Formula/operator map connected to ScienceClaimGate, ActionGate, GhostGate and WitnessLog boundaries."),
      affect: status("affect", Math.max(0, 0.2 - city.Phi_eff * 0.1), 0.8, "Affect stays advisory."),
      social: status("social", 0.12, 0.78, "Social cortex reads relationships only."),
      cerebellum: status("cerebellum", 0.08, 0.9, "Timing aligned to quaternary tick cadence."),
      residueDream: status("residue_dream", Math.min(0.4, city.R), Math.max(0.5, city.Phi_eff), "Residue dream cycle remains offline/design-only."),
      goalAlignment: status("goal_alignment", city.gate === "BLOCK" ? 0.5 : 0.1, city.gate === "APPROVE" ? 0.9 : 0.65, "Goal alignment follows ActionGate."),
    },
    handoff: generateHandoff(city),
    gameMode: input.gameMode,
    languageMetrics: input.languageMetrics,
    audioGameFeel,
    ositFormulaProfile,
    executionAllowed: false,
  };
}

export function tickBrainRuntime(runtime: BrainRuntime, input: BrainRuntimeInput): BrainRuntime {
  return { ...createBrainRuntime(input), tick: Math.max(runtime.tick + 1, input.city.tick) };
}

function status(id: string, R: number, Phi_eff: number, note: string): BrainSystemStatus {
  const r = finite(R);
  const phi = finite(Phi_eff);
  return {
    id,
    active: true,
    R: r,
    Phi_eff: phi,
    gate: r > 0.55 ? "BLOCK" : r > 0.32 ? "REVIEW" : "APPROVE",
    notes: [note],
  };
}

function finite(value: number): number {
  return Number(Math.max(0, Math.min(1, Number.isFinite(value) ? value : 0)).toFixed(3));
}
