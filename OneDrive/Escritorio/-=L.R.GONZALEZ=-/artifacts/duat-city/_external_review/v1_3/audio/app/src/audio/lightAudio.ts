// ============================================================
// DUAT Procedural Audio Engine v1.2.1
// Light Audio — Audio desde estado de luz
// Fingerprint: DUAT-v1.2.1-PROCEDURAL-AUDIO-AI-NPC
// ============================================================

/** Mapeo de luz a audio */
export const LightAudioMap = {
  highEmissive: { freq: 200, type: 'sine' as OscillatorType, gain: 0.2, modulation: 'shimmer' },
  flicker: { freq: 440, type: 'triangle' as OscillatorType, gain: 0.15, modulation: 'tremolo' },
  anomaly: { freq: 300, type: 'sawtooth' as OscillatorType, gain: 0.1, modulation: 'detuned' },
  darkness: { freq: 50, type: 'sine' as OscillatorType, gain: 0.05, modulation: 'pulse' },
};

/** Genera audio desde parámetros de luz */
export function lightToAudio(
  ctx: AudioContext,
  emissive: number,
  flicker: number,
  isAnomaly: boolean,
  expectedDarkness: boolean
): GainNode | null {
  const output = ctx.createGain();
  output.gain.setValueAtTime(0.3, ctx.currentTime);

  if (isAnomaly) {
    // Cluster desafinado
    for (let i = 0; i < 4; i++) {
      const osc = ctx.createOscillator();
      const g = ctx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(300 + i * 40 + Math.random() * 20, ctx.currentTime);
      osc.detune.setValueAtTime((Math.random() - 0.5) * 30, ctx.currentTime);
      g.gain.setValueAtTime(0.04, ctx.currentTime);
      osc.connect(g);
      g.connect(output);
      osc.start(ctx.currentTime);
    }
    return output;
  }

  if (flicker > 0.5) {
    // Tremolo
    const osc = ctx.createOscillator();
    const g = ctx.createGain();
    const tremolo = ctx.createOscillator();
    const tremGain = ctx.createGain();

    osc.type = 'triangle';
    osc.frequency.setValueAtTime(440, ctx.currentTime);
    tremolo.frequency.setValueAtTime(4 + flicker * 4, ctx.currentTime);
    tremGain.gain.setValueAtTime(0.1, ctx.currentTime);

    tremolo.connect(tremGain);
    tremGain.connect(g.gain);
    osc.connect(g);
    g.connect(output);

    osc.start(ctx.currentTime);
    tremolo.start(ctx.currentTime);
    return output;
  }

  if (emissive > 0.8) {
    // Hum brillante
    const osc = ctx.createOscillator();
    const g = ctx.createGain();
    osc.type = 'sine';
    osc.frequency.setValueAtTime(200 + emissive * 300, ctx.currentTime);
    g.gain.setValueAtTime(emissive * 0.15, ctx.currentTime);
    osc.connect(g);
    g.connect(output);
    osc.start(ctx.currentTime);
    return output;
  }

  if (expectedDarkness) {
    // Pulse Q-01
    const osc = ctx.createOscillator();
    const g = ctx.createGain();
    osc.type = 'sine';
    osc.frequency.setValueAtTime(50, ctx.currentTime);
    g.gain.setValueAtTime(0.03, ctx.currentTime);
    osc.connect(g);
    g.connect(output);
    osc.start(ctx.currentTime);
    return output;
  }

  return null;
}
