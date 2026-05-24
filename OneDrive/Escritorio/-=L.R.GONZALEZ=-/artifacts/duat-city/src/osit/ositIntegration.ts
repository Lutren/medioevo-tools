import type { CityState } from "../core/types";
import { listOSITFormulaOperators } from "./formulaRegistry";
import { evaluateScienceClaimGate } from "./scienceClaimGate";
import type { OSITFormulaProfile, OSITRuntimeModule } from "./ositTypes";

const MODULES: OSITRuntimeModule[] = [
  "MTS",
  "CausalRendering",
  "Phi_eff",
  "R",
  "J_c",
  "ActionGate",
  "GhostGate",
  "TruthGate",
  "WitnessLog",
  "PixelLightEngine",
  "AudioGameFeel",
  "LanguageCortex",
  "BrainRuntime",
  "RPGBridge",
];

export function compileOSITFormulaProfile(state: CityState): OSITFormulaProfile {
  const formulas = listOSITFormulaOperators();
  const gateResults = formulas.map(formula => evaluateScienceClaimGate(formula));
  const R_formula = round((average(gateResults.map(result => result.R)) + state.R * 0.25) / 1.25);
  const Phi_formula = round((average(gateResults.map(result => result.Phi_eff)) + state.Phi_eff * 0.25) / 1.25);
  const gate = gateResults.some(result => result.gate === "BLOCK") || R_formula > 0.55
    ? "BLOCK"
    : gateResults.some(result => result.gate === "REVIEW") || Phi_formula < 0.6
      ? "REVIEW"
      : "APPROVE";

  return {
    schema: "duat/osit-formula-profile/v1.4",
    fingerprint: "DUAT-v1.4-OSIT-OBSERVACIONISMO-FULL",
    formulaCount: formulas.length,
    gate,
    R_formula,
    Phi_formula,
    modules: Object.fromEntries(MODULES.map(module => [module, formulas.filter(formula => formula.modules.includes(module)).map(formula => formula.id)])) as Record<OSITRuntimeModule, string[]>,
    formulas,
    boundary: {
      scienceClaimGate: "ACTIVE",
      publicPhysicsClaimAllowed: false,
      exactPhysicsClaim: false,
      physicallyInspiredApproximation: true,
    },
  };
}

function average(values: number[]): number {
  return values.length ? values.reduce((sum, value) => sum + value, 0) / values.length : 0;
}

function round(value: number): number {
  return Number(Math.max(0, Math.min(1, Number.isFinite(value) ? value : 0)).toFixed(3));
}
