// ============================================================
// DUAT Procedural Audio Engine v1.2.1
// Additive — Síntesis aditiva para cuerdas/coro
// Fingerprint: DUAT-v1.2.1-PROCEDURAL-AUDIO-AI-NPC
// ============================================================

const PHI = 1.618033988749895;

/** Síntesis aditiva — construye sonidos sumando parciales */
export class AdditiveSynth {
  private ctx: AudioContext;
  private oscillators: OscillatorNode[] = [];

  constructor(ctx: AudioContext) {
    this.ctx = ctx;
  }

  /** Síntesis aditiva con parciales controlados */
  play(
    fundamental: number,
    partials: number[],
    amplitudes: number[],
    decays: number[],
    detune = 0,
    gain = 0.5
  ): GainNode {
    const output = this.ctx.createGain();
    output.gain.setValueAtTime(gain, this.ctx.currentTime);

    const oscs: OscillatorNode[] = [];

    for (let i = 0; i < partials.length; i++) {
      const osc = this.ctx.createOscillator();
      const g = this.ctx.createGain();

      osc.type = 'sine';
      osc.frequency.setValueAtTime(fundamental * partials[i], this.ctx.currentTime);
      osc.detune.setValueAtTime(detune, this.ctx.currentTime);

      const amp = amplitudes[i] ?? 1 / (i + 1);
      g.gain.setValueAtTime(amp, this.ctx.currentTime);
      g.gain.setTargetAtTime(0.001, this.ctx.currentTime + 0.01, (decays[i] ?? 1) / 3);

      osc.connect(g);
      g.connect(output);
      osc.start(this.ctx.currentTime);

      // Auto-stop
      setTimeout(() => {
        try { osc.stop(); } catch { /* */ }
      }, ((decays[i] ?? 1) * 1000) + 200);

      oscs.push(osc);
    }

    this.oscillators.push(...oscs);
    return output;
  }

  /** Parciales armónicos */
  harmonics(
    fundamental: number,
    count = 8,
    gain = 0.4,
    decay = 2
  ): GainNode {
    const partials = Array.from({ length: count }, (_, i) => i + 1);
    const amps = partials.map((_, i) => 1 / (i + 1));
    const decays = partials.map(() => decay);
    return this.play(fundamental, partials, amps, decays, 0, gain);
  }

  /** Parciales inarmónicos (cristal) */
  inharmonic(
    fundamental: number,
    gain = 0.4,
    decay = 3
  ): GainNode {
    const partials = [
      1, PHI, 1 + PHI, PHI * PHI, 2 + PHI, PHI * PHI * PHI * 0.5,
    ];
    const amps = [1, 0.7, 0.5, 0.35, 0.25, 0.2];
    const decays = partials.map(() => decay * (0.8 + Math.random() * 0.4));
    return this.play(fundamental, partials, amps, decays, 0, gain);
  }

  /** Cuerdas — parciales armónicos con ataque lento */
  strings(fundamental = 220, gain = 0.4): GainNode {
    const partials = [1, 2, 3, 4, 5, 6];
    const amps = [0.8, 0.5, 0.35, 0.2, 0.15, 0.1];
    const decays = [4, 3.5, 3, 2.5, 2, 1.5];

    const output = this.ctx.createGain();
    output.gain.setValueAtTime(gain, this.ctx.currentTime);

    // Vibrato LFO
    const vibrato = this.ctx.createOscillator();
    const vibratoGain = this.ctx.createGain();
    vibrato.frequency.setValueAtTime(5, this.ctx.currentTime);
    vibratoGain.gain.setValueAtTime(15, this.ctx.currentTime); // 15 cents

    vibrato.connect(vibratoGain);
    vibrato.start(this.ctx.currentTime);

    for (let i = 0; i < partials.length; i++) {
      const osc = this.ctx.createOscillator();
      const g = this.ctx.createGain();

      osc.type = 'sine';
      osc.frequency.setValueAtTime(fundamental * partials[i], this.ctx.currentTime);
      g.gain.setValueAtTime(0, this.ctx.currentTime);
      g.gain.linearRampToValueAtTime(amps[i], this.ctx.currentTime + 0.3);
      g.gain.setTargetAtTime(0.001, this.ctx.currentTime + decays[i], decays[i] / 3);

      vibratoGain.connect(osc.frequency);
      osc.connect(g);
      g.connect(output);
      osc.start(this.ctx.currentTime);
    }

    return output;
  }

  /** Coro — múltiples voces ligeramente desafinadas */
  choir(fundamental = 330, gain = 0.3): GainNode {
    const output = this.ctx.createGain();
    output.gain.setValueAtTime(gain, this.ctx.currentTime);

    // Vowels: A, E, O
    const formantFreqs = [730, 1090, 2440, 300, 870, 2240];

    for (let v = 0; v < 3; v++) {
      // 3 voces por nota, ligeramente desafinadas
      for (let d = 0; d < 3; d++) {
        const detune = (d - 1) * 8 + (Math.random() - 0.5) * 4;
        const osc = this.ctx.createOscillator();
        const g = this.ctx.createGain();

        osc.type = v === 0 ? 'sine' : v === 1 ? 'triangle' : 'sawtooth';
        osc.frequency.setValueAtTime(fundamental, this.ctx.currentTime);
        osc.detune.setValueAtTime(detune, this.ctx.currentTime);

        g.gain.setValueAtTime(0, this.ctx.currentTime);
        g.gain.linearRampToValueAtTime(0.15, this.ctx.currentTime + 0.5);
        g.gain.setTargetAtTime(0.001, this.ctx.currentTime + 3, 1);

        osc.connect(g);
        g.connect(output);
        osc.start(this.ctx.currentTime);
      }
    }

    // Filtros de formante
    for (const ff of formantFreqs) {
      const filter = this.ctx.createBiquadFilter();
      filter.type = 'peaking';
      filter.frequency.setValueAtTime(ff, this.ctx.currentTime);
      filter.Q.setValueAtTime(5, this.ctx.currentTime);
      filter.gain.setValueAtTime(8, this.ctx.currentTime);
    }

    return output;
  }

  /** Drone sostenido con parciales Fibonacci */
  drone(fundamental = 110, gain = 0.3): GainNode {
    const partials = [
      1, PHI * 0.5, PHI, PHI * 1.5, PHI * PHI, PHI * PHI * 0.8,
    ];
    const amps = [0.6, 0.4, 0.5, 0.3, 0.35, 0.25];
    const decays = partials.map(() => 10); // Sostenido largo

    const output = this.play(fundamental, partials, amps, decays, 0, gain);

    // Tremolo lento
    const tremolo = this.ctx.createOscillator();
    const tremGain = this.ctx.createGain();
    tremolo.frequency.setValueAtTime(0.3, this.ctx.currentTime);
    tremGain.gain.setValueAtTime(0.1, this.ctx.currentTime);
    tremolo.connect(tremGain);
    tremGain.connect(output.gain);
    tremolo.start(this.ctx.currentTime);

    return output;
  }

  dispose(): void {
    for (const osc of this.oscillators) {
      try { osc.stop(); } catch { /* */ }
    }
    this.oscillators = [];
  }
}
