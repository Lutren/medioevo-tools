import type { CityState } from "../core/types";
import type { AudioGameFeelConfig, AudioGameFeelSnapshot } from "./audioTypes";
import { DEFAULT_AUDIO_GAMEFEEL_CONFIG } from "./audioTypes";
import { computeAudioMetrics, mapWorldToAudioCues } from "./audioEventMapper";

export function createAudioGameFeelSnapshot(
  state: CityState,
  config: AudioGameFeelConfig = DEFAULT_AUDIO_GAMEFEEL_CONFIG,
): AudioGameFeelSnapshot {
  const cues = mapWorldToAudioCues(state, { maxCues: config.maxCues, seed: config.seed });
  const metrics = computeAudioMetrics(cues);
  const scene = state.playableScene;
  const activeFire = scene?.materials.filter(cell => cell.material === "fire").length ?? 0;
  const activeNeon = scene?.materials.filter(cell => cell.material === "neon").length ?? 0;
  const activeSmoke = scene?.materials.filter(cell => cell.material === "smoke").length ?? 0;
  const lightPulse = clamp01((scene?.metrics.emissiveCells ?? 0) * 0.08 + (scene?.metrics.activeLightSources ?? 0) * 0.05);
  const screenShake = clamp01(activeFire * 0.04 + activeSmoke * 0.01 + state.R * 0.08);
  const controllerPulse = clamp01(activeFire * 0.06 + activeNeon * 0.035 + metrics.highPriorityCues * 0.012);
  const agentMoodPulse = clamp01(state.agents.reduce((sum, agent) => sum + (1 - agent.mood) * 0.01 + agent.R * 0.006, 0));

  return {
    schema: "duat/audio-gamefeel/v1.3.1",
    fingerprint: "DUAT-v1.3.1-AUDIO-GAMEFEEL-FULL",
    enabled: config.enabled,
    requiresUserGesture: true,
    cues,
    metrics,
    gameFeel: {
      screenShake: round3(screenShake),
      lightPulse: round3(lightPulse),
      controllerPulse: round3(controllerPulse),
      agentMoodPulse: round3(agentMoodPulse),
    },
    boundary: {
      proceduralOnly: true,
      externalSamplesCopied: false,
      publicationAllowed: false,
      noCloud: true,
      wabiExecutionAllowed: false,
    },
  };
}

export function createMutedAudioGameFeelConfig(overrides: Partial<AudioGameFeelConfig> = {}): AudioGameFeelConfig {
  return {
    ...DEFAULT_AUDIO_GAMEFEEL_CONFIG,
    ...overrides,
    enabled: Boolean(overrides.enabled),
    requiresUserGesture: true,
    proceduralOnly: true,
    externalSamplesCopied: false,
    publicationAllowed: false,
    boundary: "OWNER_PROVIDED_INTERNAL_PROTECTED_IP",
  };
}

export function isAudioSnapshotFinite(snapshot: AudioGameFeelSnapshot): boolean {
  return snapshot.metrics.finite
    && [snapshot.metrics.R_audio, snapshot.metrics.Phi_audio, snapshot.gameFeel.screenShake, snapshot.gameFeel.lightPulse, snapshot.gameFeel.controllerPulse, snapshot.gameFeel.agentMoodPulse].every(Number.isFinite);
}

function clamp01(value: number): number {
  return Math.max(0, Math.min(1, Number.isFinite(value) ? value : 0));
}

function round3(value: number): number {
  return Number(Number.isFinite(value) ? value.toFixed(3) : "0");
}
