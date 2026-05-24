// ============================================================
// DUAT Procedural Audio Engine v1.2.1
// Oscillators — Osciladores con Fibonacci detuning
// Fingerprint: DUAT-v1.2.1-PROCEDURAL-AUDIO-AI-NPC
// ============================================================

const PHI = 1.618033988749895; // Golden ratio

/** Oscilador DUAT con capacidades extendidas */
export class Oscillator {
  private node: OscillatorNode | null = null;
  private gain: GainNode | null = null;
  private ctx: AudioContext;
  private isPlaying = false;

  constructor(ctx: AudioContext) {
    this.ctx = ctx;
  }

  /** Crea oscilador básico */
  create(
    frequency: number,
    type: OscillatorType = 'sine',
    gain = 0.5,
    detune = 0
  ): GainNode {
    this.node = this.ctx.createOscillator();
    this.gain = this.ctx.createGain();

    this.node.type = type;
    this.node.frequency.setValueAtTime(frequency, this.ctx.currentTime);
    this.node.detune.setValueAtTime(detune, this.ctx.currentTime);
    this.gain.gain.setValueAtTime(gain, this.ctx.currentTime);

    this.node.connect(this.gain);
    this.node.start(this.ctx.currentTime);
    this.isPlaying = true;

    return this.gain;
  }

  /** Crea oscilador con parciales Fibonacci (paradigma FibMob) */
  createFibPartials(
    fundamental: number,
    partials: number,
    type: OscillatorType = 'sine',
    gain = 0.3
  ): GainNode {
    const merger = this.ctx.createChannelMerger(1);

    for (let i = 1; i <= partials; i++) {
      const osc = this.ctx.createOscillator();
      const partialGain = this.ctx.createGain();
      const freq = fundamental * Math.pow(PHI, i / 2); // Fib-scaled frequencies

      osc.type = type;
      osc.frequency.setValueAtTime(freq, this.ctx.currentTime);
      osc.detune.setValueAtTime(Math.sin(i * PHI) * 5, this.ctx.currentTime);

      // Amplitud decrece con índice
      partialGain.gain.setValueAtTime(gain / (i * 0.8 + 0.2), this.ctx.currentTime);

      osc.connect(partialGain);
      partialGain.connect(merger);
      osc.start(this.ctx.currentTime);
    }

    const outputGain = this.ctx.createGain();
    merger.connect(outputGain);
    return outputGain;
  }

  /** Sweep de frecuencia */
  frequencyRamp(to: number, duration: number): void {
    if (this.node) {
      this.node.frequency.setTargetAtTime(to, this.ctx.currentTime, duration / 3);
    }
  }

  /** Stop con release */
  stop(releaseTime = 0.1): void {
    if (!this.node || !this.gain) return;
    const stopAt = this.ctx.currentTime + releaseTime;
    this.gain.gain.setTargetAtTime(0, this.ctx.currentTime, releaseTime / 3);
    try {
      this.node.stop(stopAt + 0.1);
    } catch {
      // Node might already be stopped
    }
    this.isPlaying = false;
  }

  /** Si está sonando */
  playing(): boolean {
    return this.isPlaying;
  }
}

/** Utilidades de frecuencia */
export const Freq = {
  note: (note: string): number => {
    const notes: Record<string, number> = {
      C4: 261.63, D4: 293.66, E4: 329.63, F4: 349.23,
      G4: 392.0, A4: 440.0, B4: 493.88, C5: 523.25,
      D5: 587.33, E5: 659.25, F5: 698.46, G5: 783.99,
    };
    return notes[note] || 440;
  },
  midi: (note: number): number => 440 * Math.pow(2, (note - 69) / 12),
  phiScale: (base: number, steps: number): number[] =>
    Array.from({ length: steps }, (_, i) => base * Math.pow(PHI, i / steps)),
  randomDetune: (base: number, cents: number): number =>
    base * Math.pow(2, ((Math.random() - 0.5) * cents * 2) / 1200),
};
