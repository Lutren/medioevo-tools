// ============================================================
// DUAT Procedural Audio Engine v1.2.1
// OSIT Audio — Audio desde métricas OSIT (R/Phi_eff)
// Fingerprint: DUAT-v1.2.1-PROCEDURAL-AUDIO-AI-NPC
// ============================================================

/** Genera audio desde estado OSIT */
export function ositToAudio(
  ctx: AudioContext,
  R: number,
  PhiEff: number,
  isJamming: boolean,
  hasHandoff: boolean
): GainNode | null {
  const output = ctx.createGain();
  output.gain.setValueAtTime(0.3, ctx.currentTime);

  // R rising -> noise/tension
  if (R > 0.5) {
    const bufSize = Math.ceil(ctx.sampleRate * 0.5);
    const buf = ctx.createBuffer(1, bufSize, ctx.sampleRate);
    const d = buf.getChannelData(0);
    for (let i = 0; i < bufSize; i++) {
      d[i] = (Math.random() * 2 - 1) * R * 0.1;
    }
    const src = ctx.createBufferSource();
    src.buffer = buf;
    src.loop = true;

    const filter = ctx.createBiquadFilter();
    filter.type = 'bandpass';
    filter.frequency.setValueAtTime(500 + R * 2000, ctx.currentTime);
    filter.Q.setValueAtTime(2, ctx.currentTime);

    const g = ctx.createGain();
    g.gain.setValueAtTime(R * 0.15, ctx.currentTime);

    src.connect(filter);
    filter.connect(g);
    g.connect(output);
    src.start(ctx.currentTime);
  }

  // Phi_eff rising -> harmonic clarity
  if (PhiEff > 0.7) {
    const osc = ctx.createOscillator();
    const g = ctx.createGain();
    osc.type = 'sine';
    osc.frequency.setValueAtTime(440 * PhiEff, ctx.currentTime);
    g.gain.setValueAtTime(PhiEff * 0.1, ctx.currentTime);
    g.gain.setTargetAtTime(0.001, ctx.currentTime + 2, 0.5);
    osc.connect(g);
    g.connect(output);
    osc.start(ctx.currentTime);
    osc.stop(ctx.currentTime + 3);
  }

  // Jamming -> filtered distortion
  if (isJamming) {
    const osc = ctx.createOscillator();
    const g = ctx.createGain();
    osc.type = 'sawtooth';
    osc.frequency.setValueAtTime(100 + Math.random() * 200, ctx.currentTime);
    osc.detune.setValueAtTime(Math.random() * 100, ctx.currentTime);
    g.gain.setValueAtTime(0.08, ctx.currentTime);
    g.gain.setTargetAtTime(0.001, ctx.currentTime + 0.5, 0.1);
    osc.connect(g);
    g.connect(output);
    osc.start(ctx.currentTime);
    osc.stop(ctx.currentTime + 0.6);
  }

  // Handoff stored -> sealed motif
  if (hasHandoff) {
    const osc = ctx.createOscillator();
    const g = ctx.createGain();
    osc.type = 'sine';
    osc.frequency.setValueAtTime(330, ctx.currentTime);
    g.gain.setValueAtTime(0, ctx.currentTime);
    g.gain.linearRampToValueAtTime(0.1, ctx.currentTime + 0.1);
    g.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.8);
    osc.connect(g);
    g.connect(output);
    osc.start(ctx.currentTime);
    osc.stop(ctx.currentTime + 1);
  }

  return output;
}
