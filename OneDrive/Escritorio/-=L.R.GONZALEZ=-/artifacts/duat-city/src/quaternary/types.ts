import type { Gate } from "../core/types";

export type QState = "00" | "01" | "10" | "11";

export type QMeaning =
  | "SILENCE_STABLE"
  | "ABSENCE_SIGNIFICANT"
  | "PRESENCE_STABLE"
  | "EVENT_ACTIVE";

export type QSourceKind =
  | "agent"
  | "tile"
  | "building"
  | "task"
  | "pixel_cell"
  | "render_chunk"
  | "physics_body"
  | "resource"
  | "witness"
  | "system";

export type QAction = "IGNORE" | "COMPRESS" | "HOLD" | "EXPAND" | "REVIEW" | "BLOCK";

export interface QInput {
  presence: boolean;
  difference: boolean;
  expected?: boolean;
  rawValue?: number;
  previousValue?: number;
  threshold?: number;
  timestamp?: number;
  tick: number;
  sourceId: string;
  sourceKind: QSourceKind;
}

export interface QTimingStats {
  current: QState;
  previous: QState;
  dwellTicks: number;
  transitions: number;
  frequency: number;
  period: number | null;
  permanence: number;
  stability: number;
  confidence: number;
  residue: number;
  windowSize: number;
}

export interface QEvaluation {
  sourceId: string;
  sourceKind: QSourceKind;
  tick: number;
  state: QState;
  meaning: QMeaning;
  action: QAction;
  R_delta: number;
  Phi_delta: number;
  confidence: number;
  reason: string;
  timing: QTimingStats;
}

export interface QuaternaryGateOptions {
  windowSize?: number;
  minDwellTicks?: number;
  anomalyWeight?: number;
  frequencyPenalty?: number;
  useFibMob?: boolean;
  k?: number;
}

export interface QuaternarySystemMetrics {
  total: number;
  counts: Record<QState, number>;
  anomalyRate: number;
  eventRate: number;
  stablePresenceRate: number;
  silenceRate: number;
  avgFrequency: number;
  avgPermanence: number;
  avgStability: number;
  R_quaternary: number;
  Phi_quaternary: number;
  recommendedGate: Gate;
}

export interface QuaternaryStateSummary {
  R: number;
  Phi_eff: number;
  gate: Gate;
  counts: Record<QState, number>;
  avgFrequency: number;
  avgPermanence: number;
  avgStability: number;
  anomalyRate: number;
  eventRate: number;
  R_delta: number;
  Phi_delta: number;
  combinedR: number;
  combinedPhi: number;
  topAnomalies: string[];
  topUnstable: string[];
  recent: QEvaluation[];
  next_action: string;
}

export interface QuaternaryHandoff {
  schema: "duat/quaternary-timing/v0.9";
  R_quaternary: number;
  Phi_quaternary: number;
  gate: Gate;
  counts: Record<QState, number>;
  top_anomalies: string[];
  top_unstable: string[];
  next_action: string;
}

