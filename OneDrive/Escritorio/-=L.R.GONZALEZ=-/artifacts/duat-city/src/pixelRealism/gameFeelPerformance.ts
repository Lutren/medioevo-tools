import type { AudioGameFeelSnapshot } from "../audio/audioTypes";
import type { RenderQualityPreset } from "./renderPasses";

export interface GameFeelRenderBudget {
  maxAudioCues: number;
  maxParticles: number;
  maxLightPulses: number;
  dirtyOnly: true;
  skipIfMuted: boolean;
}

const BUDGETS: Record<RenderQualityPreset, GameFeelRenderBudget> = {
  LOW: { maxAudioCues: 10, maxParticles: 24, maxLightPulses: 4, dirtyOnly: true, skipIfMuted: true },
  MEDIUM: { maxAudioCues: 18, maxParticles: 54, maxLightPulses: 8, dirtyOnly: true, skipIfMuted: true },
  HIGH: { maxAudioCues: 28, maxParticles: 90, maxLightPulses: 14, dirtyOnly: true, skipIfMuted: true },
  BEAUTIFUL: { maxAudioCues: 32, maxParticles: 130, maxLightPulses: 18, dirtyOnly: true, skipIfMuted: false },
  DEBUG: { maxAudioCues: 16, maxParticles: 44, maxLightPulses: 10, dirtyOnly: true, skipIfMuted: true },
};

export function computeGameFeelRenderBudget(qualityPreset: RenderQualityPreset, snapshot: AudioGameFeelSnapshot): GameFeelRenderBudget {
  const base = BUDGETS[qualityPreset] ?? BUDGETS.MEDIUM;
  const pressure = snapshot.metrics.R_audio > 0.35 ? 0.72 : snapshot.metrics.R_audio > 0.22 ? 0.86 : 1;
  return {
    ...base,
    maxAudioCues: Math.max(4, Math.floor(base.maxAudioCues * pressure)),
    maxParticles: Math.max(12, Math.floor(base.maxParticles * pressure)),
    maxLightPulses: Math.max(2, Math.floor(base.maxLightPulses * pressure)),
  };
}

export function capAudioGameFeelSnapshot(snapshot: AudioGameFeelSnapshot, budget: GameFeelRenderBudget): AudioGameFeelSnapshot {
  const cues = snapshot.cues
    .slice()
    .sort((a, b) => b.priority - a.priority || a.id.localeCompare(b.id))
    .slice(0, budget.maxAudioCues);
  return {
    ...snapshot,
    cues,
    gameFeel: {
      ...snapshot.gameFeel,
      lightPulse: Math.min(snapshot.gameFeel.lightPulse, budget.maxLightPulses / 18),
    },
  };
}
