import type { Gate } from "../core/types";

export type AudioCueKind =
  | "material_water"
  | "material_fire"
  | "material_smoke"
  | "material_stone"
  | "material_wood"
  | "material_neon"
  | "light_torch"
  | "light_window"
  | "light_neon"
  | "light_fire"
  | "light_magic"
  | "light_signal"
  | "light_ruin_anomaly"
  | "agent_need"
  | "agent_task"
  | "gate_approve"
  | "gate_review"
  | "gate_block"
  | "language_certeza"
  | "language_inferencia"
  | "language_incognita"
  | "language_bloqueo"
  | "cosmology_fire_event"
  | "rpg_transition"
  | "ui_confirm"
  | "ui_warning";

export type AudioCueSource = "material" | "light" | "agent" | "language" | "cosmology" | "rpg" | "ui" | "system";

export interface AudioCue {
  id: string;
  kind: AudioCueKind;
  source: AudioCueSource;
  label: string;
  frequencyHz: number;
  durationMs: number;
  gain: number;
  pan: number;
  priority: number;
  gate?: Gate;
  qState?: "00" | "01" | "10" | "11";
  tags: string[];
}

export interface AudioGameFeelConfig {
  enabled: boolean;
  masterGain: number;
  maxCues: number;
  seed: number;
  mode: "off" | "preview" | "runtime";
  requiresUserGesture: true;
  proceduralOnly: true;
  externalSamplesCopied: false;
  publicationAllowed: false;
  boundary: "OWNER_PROVIDED_INTERNAL_PROTECTED_IP";
}

export interface AudioGameFeelMetrics {
  R_audio: number;
  Phi_audio: number;
  cueCount: number;
  highPriorityCues: number;
  materialCues: number;
  lightCues: number;
  agentCues: number;
  averageGain: number;
  peakGain: number;
  deterministicHash: number;
  finite: boolean;
  proceduralOnly: true;
}

export interface AudioGameFeelSnapshot {
  schema: "duat/audio-gamefeel/v1.3.1";
  fingerprint: "DUAT-v1.3.1-AUDIO-GAMEFEEL-FULL";
  enabled: boolean;
  requiresUserGesture: true;
  cues: AudioCue[];
  metrics: AudioGameFeelMetrics;
  gameFeel: {
    screenShake: number;
    lightPulse: number;
    controllerPulse: number;
    agentMoodPulse: number;
  };
  boundary: {
    proceduralOnly: true;
    externalSamplesCopied: false;
    publicationAllowed: false;
    noCloud: true;
    wabiExecutionAllowed: false;
  };
}

export interface ProceduralTonePlan {
  cueId: string;
  oscillatorType: OscillatorType;
  frequencyHz: number;
  durationMs: number;
  gain: number;
  pan: number;
  attackMs: number;
  decayMs: number;
  releaseMs: number;
  filterHz: number;
  deterministic: true;
}

export interface AudioBenchmarkScenario {
  id: string;
  label: string;
  materials: string[];
  lights: string[];
  agents: number;
  expectedCueKinds: AudioCueKind[];
}

export interface AudioBenchmarkResult {
  scenario: string;
  label: string;
  avgMapMs: number;
  p95MapMs: number;
  cueCount: number;
  R_audio: number;
  Phi_audio: number;
  proceduralOnly: true;
  finite: boolean;
}

export interface AudioBenchmarkDocument {
  schema: "duat/audio-gamefeel-benchmark/v1.3.1";
  fingerprint: "DUAT-v1.3.1-AUDIO-GAMEFEEL-CONTINUITY";
  generatedAt: string;
  iterationsPerScenario: number;
  browserAudioUsed: false;
  scenarios: AudioBenchmarkResult[];
  notes: string[];
}

export interface AudioManifest {
  schema: "duat/audio-gamefeel-manifest/v1.3.1";
  fingerprint: "DUAT-v1.3.1-AUDIO-GAMEFEEL-CONTINUITY";
  generatedAt: string;
  boundary: {
    ownerProvidedInternalProtectedIp: true;
    proceduralOnly: true;
    externalSamplesCopied: false;
    publicationAllowed: false;
    noCloud: true;
    requiresUserGesture: true;
    wabiExecutionAllowed: false;
  };
  cueKinds: AudioCueKind[];
  synthesisPolicy: string;
  manifests: string[];
}

export const DEFAULT_AUDIO_GAMEFEEL_CONFIG: AudioGameFeelConfig = {
  enabled: false,
  masterGain: 0.42,
  maxCues: 32,
  seed: 131,
  mode: "off",
  requiresUserGesture: true,
  proceduralOnly: true,
  externalSamplesCopied: false,
  publicationAllowed: false,
  boundary: "OWNER_PROVIDED_INTERNAL_PROTECTED_IP",
};
