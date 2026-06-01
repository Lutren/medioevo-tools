// Canonical type aliases so DUAT Genesis code compiles against duat-city core types.
// These mirror "New project 3/src/simulation/types.ts" but import from the local tree.

import type { Gate } from "../core/types";

export type CosmologyState = "NU" | "ATUM" | "DUAT" | "MAAT" | "OSIRIS" | "COLAPSO";
export type RuleMode = "duat" | "conway";
export type AblationMode = "full" | "no-g" | "no-l" | "no-observer" | "no-noise";
export type DuatOverlayMode = "psi" | "gravity" | "light" | "observer-delta";
export type ObserverModality = "visual" | "sonora" | "tactil";

export interface DuatEngineParams {
  chi: number;
  sigma: number;
  dt: number;
  noise: number;
  observerStrength: number;
  speed: number;
  running: boolean;
  ruleMode: RuleMode;
  ablationMode?: AblationMode;
}

export interface ObserverProfile {
  id: "a" | "b" | "c";
  name: string;
  resolution: number;
  saturation: number;
  noise: number;
  temporalWindow: number;
  modality: ObserverModality;
}

export interface ActiveObserver {
  x: number;
  y: number;
  strength: number;
  profile: ObserverProfile;
}

export interface KernelCell {
  dx: number;
  dy: number;
  w: number;
}

export interface SimulationMetrics {
  mean: number;
  variance: number;
  entropy: number;
  activity: number;
  edge: number;
  gMean: number;
  lMean: number;
  balance: number;
  lgBalance: number;
  spectralEntropy: number;
  dimObs: number;
  atumScore: number;
  osirisScore: number;
  clipArtifactRatio: number;
  liveness: number;
  residue: number;
  phiEff: number;
  centroidX: number;
  centroidY: number;
  persistentFrames: number;
  cosmologyState: CosmologyState;
}

export interface LGModeSpectrum {
  modes: [number, number, number, number, number];
  threshold: number;
  lgBalance: number;
  spectralEntropy: number;
}

export interface SweepConfig {
  chis: number[];
  sigmas: number[];
  noises: number[];
  observerStrengths: number[];
  seeds: number[];
  steps: number;
  width: number;
  height: number;
}

export interface SweepRow {
  chi: number;
  sigma: number;
  noise: number;
  observerStrength: number;
  seed: number;
  frame: number;
  cosmologyState: CosmologyState;
  mean: number;
  liveness: number;
  residue: number;
  phiEff: number;
  dimObs: number;
  atumScore: number;
  osirisScore: number;
  spectralEntropy: number;
  clipArtifactRatio: number;
}

export interface SweepSummary {
  rows: number;
  fertileRows: number;
  lowClipRows: number;
  meanLiveness: number;
  meanResidue: number;
  maxClipArtifactRatio: number;
  observerEffectLivenessDelta: number;
  bestLiveness: number;
  bestState: CosmologyState;
  bestParams: Pick<SweepRow, "chi" | "sigma" | "noise" | "observerStrength" | "seed">;
  phaseCounts: Record<CosmologyState, number>;
}

export interface PhaseMapCell {
  chi: number;
  sigma: number;
  cases: number;
  dominantState: CosmologyState;
  meanLiveness: number;
  meanResidue: number;
  maxClipArtifactRatio: number;
  phaseCounts: Record<CosmologyState, number>;
}
