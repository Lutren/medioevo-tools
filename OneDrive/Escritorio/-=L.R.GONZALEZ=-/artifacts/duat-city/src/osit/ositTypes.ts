import type { Gate } from "../core/types";

export type OSITFormulaId =
  | "shannon_entropy"
  | "boltzmann_entropy"
  | "maxwell_field_proxy"
  | "navier_stokes_flow_proxy"
  | "fourier_signal_decomposition"
  | "schrodinger_probability_boundary"
  | "black_scholes_risk_proxy"
  | "euler_step"
  | "gauss_evidence_weight"
  | "newton_motion_proxy";

export type OSITRuntimeModule =
  | "MTS"
  | "CausalRendering"
  | "Phi_eff"
  | "R"
  | "J_c"
  | "ActionGate"
  | "GhostGate"
  | "TruthGate"
  | "WitnessLog"
  | "PixelLightEngine"
  | "AudioGameFeel"
  | "LanguageCortex"
  | "BrainRuntime"
  | "RPGBridge";

export type OSITClaimBoundary =
  | "OPERATIONAL_METAPHOR"
  | "NUMERIC_APPROXIMATION"
  | "FORMAL_LAB_ONLY"
  | "IN_WORLD_LORE";

export interface OSITFormulaOperator {
  id: OSITFormulaId;
  label: string;
  historicalReference: string;
  boundary: OSITClaimBoundary;
  modules: OSITRuntimeModule[];
  implementationStatus: "implemented_proxy" | "mapped_contract" | "reference_only";
  risk: number;
  Phi_eff: number;
  publicClaimAllowed: false;
  notes: string;
}

export interface OSITFormulaProfile {
  schema: "duat/osit-formula-profile/v1.4";
  fingerprint: "DUAT-v1.4-OSIT-OBSERVACIONISMO-FULL";
  formulaCount: number;
  gate: Gate;
  R_formula: number;
  Phi_formula: number;
  modules: Record<OSITRuntimeModule, string[]>;
  formulas: OSITFormulaOperator[];
  boundary: {
    scienceClaimGate: "ACTIVE";
    publicPhysicsClaimAllowed: false;
    exactPhysicsClaim: false;
    physicallyInspiredApproximation: true;
  };
}

export interface ScienceClaimGateResult {
  gate: Gate;
  R: number;
  Phi_eff: number;
  downgraded: boolean;
  reason: string;
}
