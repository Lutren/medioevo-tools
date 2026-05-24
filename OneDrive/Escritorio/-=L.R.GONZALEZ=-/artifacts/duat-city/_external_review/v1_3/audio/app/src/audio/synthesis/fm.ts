// ============================================================
// DUAT Procedural Audio Engine v1.2.1
// FM Synthesis — Síntesis FM para bronces/campanas
// Fingerprint: DUAT-v1.2.1-PROCEDURAL-AUDIO-AI-NPC
// ============================================================

const PHI = 1.618033988749895;

/** Síntesis FM (Frequency Modulation) */
export class FMSynth {
  private ctx: AudioContext;

  constructor(ctx: AudioContext) {
    this.ctx = ctx;
  }

  /** FM básico: carrier + modulator */
  play(
    carrierFreq: number,
    modFreq: number,
    modIndex: number,
    carrierWave: OscillatorType = 'sine',
    modWave: OscillatorType = 'sine',
    duration = 1,
    gain = 0.5
  ): GainNode {
    const carrier = this.ctx.createOscillator();
    const modulator = this.ctx.createOscillator();
    const modGain = this.ctx.createGain();
    const outputGain = this.ctx.createGain();

    carrier.type = carrierWave;
    carrier.frequency.setValueAtTime(carrierFreq, this.ctx.currentTime);

    modulator.type = modWave;
    modulator.frequency.setValueAtTime(modFreq, this.ctx.currentTime);

    modGain.gain.setValueAtTime(modIndex, this.ctx.currentTime);
    outputGain.gain.setValueAtTime(gain, this.ctx.currentTime);
    outputGain.gain.setTargetAtTime(0.001, this.ctx.currentTime + duration, duration / 3);

    modulator.connect(modGain);
    modGain.connect(carrier.frequency);
    carrier.connect(outputGain);

    modulator.start(this.ctx.currentTime);
    carrier.start(this.ctx.currentTime);
    carrier.stop(this.ctx.currentTime + duration + 0.1);
    modulator.stop(this.ctx.currentTime + duration + 0.1);

    return outputGain;
  }

  /** Campana FM (ratio 1:√2) */
  bell(frequency = 440, gain = 0.4): GainNode {
    return this.play(
      frequency,
      frequency * Math.SQRT2,
      frequency * 2,
      'sine',
      'sine',
      3.0,
      gain
    );
  }

  /** Bronce con riqueza armónica */
  brass(frequency = 300, gain = 0.5): GainNode {
    return this.play(
      frequency,
      frequency * 1.4,
      frequency * 0.8,
      'sawtooth',
      'sine',
      1.5,
      gain
    );
  }

  /** Cuerno ritual — ratios irracionales */
  ritualHorn(fundamental = 150, gain = 0.5): GainNode {
    const output = this.ctx.createGain();
    output.gain.setValueAtTime(gain, this.ctx.currentTime);

    // Múltiples carriers con ratios φ
    for (let i = 1; i <= 3; i++) {
      const carrier = this.ctx.createOscillator();
      const mod = this.ctx.createOscillator();
      const modG = this.ctx.createGain();
      const g = this.ctx.createGain();

      carrier.type = 'sawtooth';
      carrier.frequency.setValueAtTime(fundamental * i, this.ctx.currentTime);

      mod.type = 'square';
      mod.frequency.setValueAtTime(fundamental * PHI * i, this.ctx.currentTime);

      modG.gain.setValueAtTime(fundamental * 0.5, this.ctx.currentTime);
      g.gain.setValueAtTime(0.3 / i, this.ctx.currentTime);
      g.gain.setTargetAtTime(0.001, this.ctx.currentTime + 2, 0.5);

      mod.connect(modG);
      modG.connect(carrier.frequency);
      carrier.connect(g);
      g.connect(output);

      mod.start(this.ctx.currentTime);
      carrier.start(this.ctx.currentTime);
      carrier.stop(this.ctx.currentTime + 3);
      mod.stop(this.ctx.currentTime + 3);
    }

    return output;
  }

  /** Efecto de campana celesta */
  celesta(note = 880, gain = 0.3): GainNode {
    const output = this.ctx.createGain();
    output.gain.setValueAtTime(gain, this.ctx.currentTime);

    // Fundamental + octava + quinta FM
    const freqs = [note, note * 2, note * PHI];
    const mods = [note * 2.2, note * 3.5, note * 1.7];

    for (let i = 0; i < 3; i++) {
      const g = this.play(freqs[i], mods[i], note * 1.5, 'sine', 'sine', 2, 0.33);
      g.connect(output);
    }

    return output;
  }
}
