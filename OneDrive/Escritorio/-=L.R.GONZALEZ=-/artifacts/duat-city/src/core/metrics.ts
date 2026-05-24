import type { Gate, Regime } from "./types";

export function computeRegime(R: number, Phi_eff: number): Regime {
  if (R <= 0.15 && Phi_eff >= 0.75) return "OPTIMO";
  if (R <= 0.30 && Phi_eff >= 0.60) return "FUNCIONAL";
  if (R <= 0.60) return "CARGADO";
  return "SATURADO";
}

export function computeGate(R: number): Gate {
  if (R > 0.60) return "BLOCK";
  if (R > 0.35) return "REVIEW";
  return "APPROVE";
}

export function computePhiEff(R: number, mood = 0.5, trust = 0.5): number {
  const base = 1 - R;
  const adjustment = (mood + trust) / 2 - 0.5;
  return Math.max(0, Math.min(1, base + adjustment * 0.2));
}

export function computeAgentGate(R: number): Gate {
  if (R > 0.65) return "BLOCK";
  if (R > 0.35) return "REVIEW";
  return "APPROVE";
}

export function computeNextAction(gate: Gate, regime: Regime): string {
  if (gate === "BLOCK") return "COMPRESS: pause expansion, resolve needs, generate handoff";
  if (gate === "REVIEW") return "REVIEW: inspect failing needs/tasks/resources";
  if (regime === "OPTIMO") return "EXPAND: add district, quest, or agent";
  return "HOLD: continue simulation";
}
