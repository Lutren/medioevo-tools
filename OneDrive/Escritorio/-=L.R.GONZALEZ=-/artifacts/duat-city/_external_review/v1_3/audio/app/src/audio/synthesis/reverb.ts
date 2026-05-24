// ============================================================
// DUAT Procedural Audio Engine v1.2.1
// Reverb — Reverb por retardo múltiple (sin convolution)
// Fingerprint: DUAT-v1.2.1-PROCEDURAL-AUDIO-AI-NPC
// ============================================================

import { type ReverbProfile } from '../audioTypes';

/** Configuración de reverb por perfil */
export const ReverbPresets: Record<ReverbProfile, { duration: number; decay: number; preDelay: number }> = {
  catacomb: { duration: 3.5, decay: 0.75, preDelay: 0.08 },
  stone_chamber: { duration: 2.0, decay: 0.6, preDelay: 0.03 },
  open_cavern: { duration: 4.0, decay: 0.8, preDelay: 0.12 },
  small_room: { duration: 0.8, decay: 0.4, preDelay:0.01 },
  metal_tunnel: { duration: 2.5, decay: 0.7, preDelay: 0.04 },
  outdoor: { duration: 0.5, decay: 0.3, preDelay: 0.02 },
  water_surface: { duration: 1.5, decay: 0.5, preDelay: 0.06 },
  dense_forest: { duration: 1.2, decay: 0.45, preDelay: 0.05 },
};

/** Reverb por retardo múltiple (Schroeder-like) */
export class Reverb {
  private ctx: AudioContext;

  constructor(ctx: AudioContext) {
    this.ctx = ctx;
  }

  /** Crea reverb con perfil específico */
  create(profile: ReverbProfile, wet = 0.3): { input: GainNode; output: GainNode } {
    const preset = ReverbPresets[profile];
    return this.createCustom(preset.duration, preset.decay, preset.preDelay, wet);
  }

  /** Crea reverb personalizado */
  createCustom(
    duration: number,
    decay: number,
    preDelay: number,
    wet = 0.3,
    dry = 0.7
  ): { input: GainNode; output: GainNode } {
    const input = this.ctx.createGain();
    const output = this.ctx.createGain();
    const dryGain = this.ctx.createGain();
    const wetGain = this.ctx.createGain();

    dryGain.gain.setValueAtTime(dry, this.ctx.currentTime);
    wetGain.gain.setValueAtTime(wet, this.ctx.currentTime);

    // Pre-delay
    const preDelayNode = this.ctx.createDelay();
    preDelayNode.delayTime.setValueAtTime(preDelay, this.ctx.currentTime);

    // Parallel comb filters (6 delays con feedback)
    const combDelays = [0.03, 0.04, 0.05, 0.07, 0.09, 0.12];
    const combOutputs: GainNode[] = [];

    for (const delayTime of combDelays) {
      const delay = this.ctx.createDelay();
      const feedback = this.ctx.createGain();
      const combOut = this.ctx.createGain();

      delay.delayTime.setValueAtTime(delayTime, this.ctx.currentTime);
      feedback.gain.setValueAtTime(decay * (1 - delayTime / duration), this.ctx.currentTime);

      preDelayNode.connect(delay);
      delay.connect(feedback);
      feedback.connect(delay);
      delay.connect(combOut);
      combOutputs.push(combOut);
    }

    // All-pass filters (2 para difusión)
    const ap1 = this.createAllPass(0.005);
    const ap2 = this.createAllPass(0.016);

    // Chain
    input.connect(dryGain);
    dryGain.connect(output);

    input.connect(preDelayNode);

    // Merge combs
    const combMerger = this.ctx.createGain();
    for (const co of combOutputs) {
      co.connect(combMerger);
    }

    combMerger.connect(ap1.input);
    ap1.output.connect(ap2.input);
    ap2.output.connect(wetGain);
    wetGain.connect(output);

    return { input, output };
  }

  /** Filtro all-pass */
  private createAllPass(delayTime: number): { input: BiquadFilterNode; output: BiquadFilterNode } {
    const input = this.ctx.createBiquadFilter();
    const output = this.ctx.createBiquadFilter();

    input.type = 'allpass';
    input.frequency.setValueAtTime(1 / (2 * Math.PI * delayTime), this.ctx.currentTime);

    output.type = 'allpass';
    output.frequency.setValueAtTime(1 / (2 * Math.PI * delayTime * 1.618), this.ctx.currentTime);

    input.connect(output);
    return { input, output };
  }

  /** Reverb simple de una etapa (más barato en CPU) */
  createSimple(duration = 1.5, decay = 0.5, wet = 0.25): { input: GainNode; output: GainNode } {
    const input = this.ctx.createGain();
    const output = this.ctx.createGain();
    const delay = this.ctx.createDelay();
    const feedback = this.ctx.createGain();
    const wetGain = this.ctx.createGain();

    delay.delayTime.setValueAtTime(duration * 0.1, this.ctx.currentTime);
    feedback.gain.setValueAtTime(decay, this.ctx.currentTime);
    wetGain.gain.setValueAtTime(wet, this.ctx.currentTime);

    input.connect(delay);
    delay.connect(feedback);
    feedback.connect(delay);
    delay.connect(wetGain);
    wetGain.connect(output);
    input.connect(output);

    return { input, output };
  }
}
