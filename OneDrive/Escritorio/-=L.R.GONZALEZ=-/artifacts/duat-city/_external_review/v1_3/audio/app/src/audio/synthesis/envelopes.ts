// ============================================================
// DUAT Procedural Audio Engine v1.2.1
// Envelopes — Envolventes ADSR con Fibonacci timing
// Fingerprint: DUAT-v1.2.1-PROCEDURAL-AUDIO-AI-NPC
// ============================================================

import { type ADSRConfig } from '../audioTypes';

const PHI = 1.618033988749895;

/** Envolvente ADSR */
export class Envelope {
  private ctx: AudioContext;

  constructor(ctx: AudioContext) {
    this.ctx = ctx;
  }

  /** Aplica envolvente ADSR a un AudioParam */
  apply(
    param: AudioParam,
    config: ADSRConfig,
    peakValue = 1
  ): void {
    const t = this.ctx.currentTime;
    param.setValueAtTime(0, t);
    param.linearRampToValueAtTime(peakValue, t + config.attack);
    param.exponentialRampToValueAtTime(
      peakValue * config.sustain,
      t + config.attack + config.decay
    );
  }

  /** Release */
  release(param: AudioParam, config: ADSRConfig): void {
    const t = this.ctx.currentTime;
    param.setTargetAtTime(0, t, config.release / 3);
  }

  /** Presets comunes */
  static presets = {
    pluck: (): ADSRConfig => ({ attack: 0.01, decay: 0.1, sustain: 0.3, release: 0.2 }),
    pad: (): ADSRConfig => ({ attack: 0.5, decay: 0.3, sustain: 0.7, release: 1.5 }),
    bell: (): ADSRConfig => ({ attack: 0.001, decay: 1.5, sustain: 0.01, release: 3.0 }),
    drum: (): ADSRConfig => ({ attack: 0.005, decay: 0.2, sustain: 0.1, release: 0.3 }),
    bow: (): ADSRConfig => ({ attack: 0.3, decay: 0.1, sustain: 0.8, release: 0.8 }),
    brass: (): ADSRConfig => ({ attack: 0.1, decay: 0.2, sustain: 0.9, release: 0.4 }),
    breath: (): ADSRConfig => ({ attack: 0.8, decay: 0.5, sustain: 0.6, release: 1.2 }),
    explosion: (): ADSRConfig => ({ attack: 0.005, decay: 0.5, sustain: 0, release: 2.0 }),
    // Fib-scaled: tiempos siguen proporción áurea
    phiPad: (): ADSRConfig => ({
      attack: 0.1 * PHI,
      decay: 0.1 * PHI * PHI,
      sustain: 0.7,
      release: 0.1 * PHI * PHI * PHI,
    }),
  };

  /** Aplica envolvente a gain node completo */
  applyToGain(gainNode: GainNode, config: ADSRConfig, peakValue = 1): void {
    this.apply(gainNode.gain, config, peakValue);
  }
}
