// ============================================================
// DUAT Procedural Audio Engine v1.2.1
// Synthetic Brass — Bronces sintéticos
// Fingerprint: DUAT-v1.2.1-PROCEDURAL-AUDIO-AI-NPC
// ============================================================

const PHI = 1.618033988749895;

/** Bronces sintéticos con formant filters */
export class SyntheticBrass {
  private ctx: AudioContext;

  constructor(ctx: AudioContext) {
    this.ctx = ctx;
  }

  /** Brass swell — creciente dramático */
  swell(frequency = 300, gain = 0.4): GainNode {
    const output = this.ctx.createGain();
    output.gain.setValueAtTime(gain, this.ctx.currentTime);

    // Saw + triangle softened
    const saw = this.ctx.createOscillator();
    const tri = this.ctx.createOscillator();
    const mixGain = this.ctx.createGain();

    saw.type = 'sawtooth';
    saw.frequency.setValueAtTime(frequency, this.ctx.currentTime);

    tri.type = 'triangle';
    tri.frequency.setValueAtTime(frequency, this.ctx.currentTime);

    mixGain.gain.setValueAtTime(0, this.ctx.currentTime);
    mixGain.gain.linearRampToValueAtTime(0.8, this.ctx.currentTime + 0.8);
    mixGain.gain.setTargetAtTime(0.001, this.ctx.currentTime + 2.5, 0.6);

    saw.connect(mixGain);
    tri.connect(mixGain);

    // Formant filter para simular tuba/trombón
    const formants = [300, 850, 2500];
    const formantQ = [5, 8, 12];
    const formantGains = [6, 3, 2];

    let lastNode: AudioNode = mixGain;
    for (let i = 0; i < formants.length; i++) {
      const filter = this.ctx.createBiquadFilter();
      filter.type = 'peaking';
      filter.frequency.setValueAtTime(formants[i], this.ctx.currentTime);
      filter.Q.setValueAtTime(formantQ[i], this.ctx.currentTime);
      filter.gain.setValueAtTime(formantGains[i], this.ctx.currentTime);
      lastNode.connect(filter);
      lastNode = filter;
    }

    lastNode.connect(output);

    saw.start(this.ctx.currentTime);
    tri.start(this.ctx.currentTime);

    return output;
  }

  /** Brass staccato — golpe corto */
  staccatoHit(frequency = 400, gain = 0.5): GainNode {
    const output = this.ctx.createGain();
    output.gain.setValueAtTime(gain, this.ctx.currentTime);

    const saw = this.ctx.createOscillator();
    const g = this.ctx.createGain();

    saw.type = 'sawtooth';
    saw.frequency.setValueAtTime(frequency, this.ctx.currentTime);

    g.gain.setValueAtTime(0, this.ctx.currentTime);
    g.gain.linearRampToValueAtTime(0.8, this.ctx.currentTime + 0.05);
    g.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.3);

    saw.connect(g);

    // Low-pass para suavizar
    const filter = this.ctx.createBiquadFilter();
    filter.type = 'lowpass';
    filter.frequency.setValueAtTime(1500, this.ctx.currentTime);
    filter.frequency.setTargetAtTime(500, this.ctx.currentTime + 0.1, 0.05);

    g.connect(filter);
    filter.connect(output);

    saw.start(this.ctx.currentTime);
    saw.stop(this.ctx.currentTime + 0.4);

    return output;
  }

  /** Ritual horn — cuerno ceremonial */
  ritualHorn(fundamental = 150, gain = 0.5): GainNode {
    const output = this.ctx.createGain();
    output.gain.setValueAtTime(gain, this.ctx.currentTime);

    for (let i = 1; i <= 3; i++) {
      const osc = this.ctx.createOscillator();
      const g = this.ctx.createGain();

      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(fundamental * i * PHI * 0.5, this.ctx.currentTime);

      g.gain.setValueAtTime(0.3 / i, this.ctx.currentTime);
      g.gain.setTargetAtTime(0.001, this.ctx.currentTime + 2, 0.4);

      // Formant
      const filter = this.ctx.createBiquadFilter();
      filter.type = 'bandpass';
      filter.frequency.setValueAtTime(500 + i * 300, this.ctx.currentTime);
      filter.Q.setValueAtTime(5, this.ctx.currentTime);

      osc.connect(g);
      g.connect(filter);
      filter.connect(output);
      osc.start(this.ctx.currentTime);
      osc.stop(this.ctx.currentTime + 3);
    }

    return output;
  }
}
