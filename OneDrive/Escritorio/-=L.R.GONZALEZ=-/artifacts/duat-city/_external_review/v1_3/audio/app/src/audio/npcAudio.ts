// ============================================================
// DUAT Procedural Audio Engine v1.2.1
// NPC Audio — Audio para personajes/NPCs IA
// Fingerprint: DUAT-v1.2.1-PROCEDURAL-AUDIO-AI-NPC
// ============================================================

import { type NPCAudioState } from './audioTypes';

/** Genera audio para NPC */
export function npcToAudio(ctx: AudioContext, state: NPCAudioState): GainNode | null {
  const output = ctx.createGain();
  const proxGain = 1 - state.proximity;
  output.gain.setValueAtTime(proxGain * 0.25, ctx.currentTime);

  // Footsteps si se mueve
  if (state.footstepMaterial && proxGain > 0.1) {
    const footGain = ctx.createGain();
    footGain.gain.setValueAtTime(0.1, ctx.currentTime);

    const osc = ctx.createOscillator();
    const g = ctx.createGain();
    osc.type = 'sine';
    const freqs: Record<string, number> = {
      stone: 200, metal: 600, wood: 300, sand: 100,
      water: 150, glass: 800, wet_stone: 180,
    };
    osc.frequency.setValueAtTime(freqs[state.footstepMaterial] || 200, ctx.currentTime);
    g.gain.setValueAtTime(0.05, ctx.currentTime);
    g.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.1);
    osc.connect(g);
    g.connect(footGain);
    footGain.connect(output);
    osc.start(ctx.currentTime);
    osc.stop(ctx.currentTime + 0.15);
  }

  // Breath si está cerca
  if (state.breathEnabled && state.proximity < 0.5) {
    const bufSize = Math.ceil(ctx.sampleRate * 0.5);
    const buf = ctx.createBuffer(1, bufSize, ctx.sampleRate);
    const d = buf.getChannelData(0);
    for (let i = 0; i < bufSize; i++) {
      d[i] = (Math.random() * 2 - 1) * 0.08 * Math.sin(i / bufSize * Math.PI);
    }
    const src = ctx.createBufferSource();
    src.buffer = buf;

    const filter = ctx.createBiquadFilter();
    filter.type = 'lowpass';
    filter.frequency.setValueAtTime(800, ctx.currentTime);

    const g = ctx.createGain();
    g.gain.setValueAtTime(0.05, ctx.currentTime);

    src.connect(filter);
    filter.connect(g);
    g.connect(output);
    src.start(ctx.currentTime);
  }

  // Motif por rol
  if (state.actionMotif) {
    const roleFreqs: Record<string, number> = {
      guard: 200, merchant: 350, scholar: 280, mystic: 220,
      rogue: 400, elder: 160,
    };
    const freq = roleFreqs[state.actionMotif] || 300;
    const osc = ctx.createOscillator();
    const g = ctx.createGain();
    osc.type = 'triangle';
    osc.frequency.setValueAtTime(freq, ctx.currentTime);
    g.gain.setValueAtTime(0.05, ctx.currentTime);
    g.gain.setTargetAtTime(0.001, ctx.currentTime + 1, 0.3);
    osc.connect(g);
    g.connect(output);
    osc.start(ctx.currentTime);
    osc.stop(ctx.currentTime + 1.5);
  }

  // R alto = ritmo inestable
  if (state.R_influence > 0.6) {
    const jitter = ctx.createOscillator();
    const jg = ctx.createGain();
    jitter.type = 'sine';
    jitter.frequency.setValueAtTime(2 + state.R_influence * 5, ctx.currentTime);
    jg.gain.setValueAtTime(0.03, ctx.currentTime);
    jitter.connect(jg);
    jg.connect(output);
    jitter.start(ctx.currentTime);
  }

  // BLOCK -> low warning
  if (state.R_influence > 0.8) {
    const osc = ctx.createOscillator();
    const g = ctx.createGain();
    osc.type = 'sine';
    osc.frequency.setValueAtTime(80, ctx.currentTime);
    g.gain.setValueAtTime(0.08, ctx.currentTime);
    g.gain.setTargetAtTime(0.001, ctx.currentTime + 0.5, 0.1);
    osc.connect(g);
    g.connect(output);
    osc.start(ctx.currentTime);
    osc.stop(ctx.currentTime + 0.6);
  }

  return output;
}
