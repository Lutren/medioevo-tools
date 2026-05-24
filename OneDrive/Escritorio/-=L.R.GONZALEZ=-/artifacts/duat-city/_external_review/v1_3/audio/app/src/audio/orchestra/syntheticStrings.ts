// ============================================================
// DUAT Procedural Audio Engine v1.2.1
// Synthetic Strings — Cuerdas sintéticas
// Fingerprint: DUAT-v1.2.1-PROCEDURAL-AUDIO-AI-NPC
// ============================================================

/** Cuerdas sintéticas con vibrato y bow noise */
export class SyntheticStrings {
  private ctx: AudioContext;

  constructor(ctx: AudioContext) {
    this.ctx = ctx;
  }

  /** Cuerdas graves (low drone) */
  lowDrone(frequency = 110, gain = 0.3): GainNode {
    const output = this.ctx.createGain();
    output.gain.setValueAtTime(gain, this.ctx.currentTime);

    // Parciales armónicos de cuerda
    const partials = [1, 2, 3, 4, 5, 6];
    const amps = [0.7, 0.5, 0.3, 0.2, 0.15, 0.1];

    for (let i = 0; i < partials.length; i++) {
      const osc = this.ctx.createOscillator();
      const g = this.ctx.createGain();

      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(frequency * partials[i], this.ctx.currentTime);

      // Vibrato
      const vibrato = this.ctx.createOscillator();
      const vibratoGain = this.ctx.createGain();
      vibrato.frequency.setValueAtTime(5 + i * 0.5, this.ctx.currentTime);
      vibratoGain.gain.setValueAtTime(10, this.ctx.currentTime);
      vibrato.connect(vibratoGain);
      vibratoGain.connect(osc.frequency);
      vibrato.start(this.ctx.currentTime);

      g.gain.setValueAtTime(0, this.ctx.currentTime);
      g.gain.linearRampToValueAtTime(amps[i], this.ctx.currentTime + 0.5);
      g.gain.setTargetAtTime(amps[i] * 0.8, this.ctx.currentTime + 2, 1);

      osc.connect(g);
      g.connect(output);
      osc.start(this.ctx.currentTime);
    }

    // Bow noise (filtered noise)
    const bufferSize = Math.ceil(this.ctx.sampleRate * 0.5);
    const buffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
    const data = buffer.getChannelData(0);
    for (let i = 0; i < bufferSize; i++) {
      data[i] = (Math.random() * 2 - 1) * 0.1;
    }
    const bowSrc = this.ctx.createBufferSource();
    bowSrc.buffer = buffer;
    bowSrc.loop = true;

    const bowFilter = this.ctx.createBiquadFilter();
    bowFilter.type = 'bandpass';
    bowFilter.frequency.setValueAtTime(2000, this.ctx.currentTime);
    bowFilter.Q.setValueAtTime(1, this.ctx.currentTime);

    const bowGain = this.ctx.createGain();
    bowGain.gain.setValueAtTime(0.05, this.ctx.currentTime);

    bowSrc.connect(bowFilter);
    bowFilter.connect(bowGain);
    bowGain.connect(output);
    bowSrc.start(this.ctx.currentTime);

    return output;
  }

  /** Cuerdas brillantes (high shimmer) */
  highShimmer(frequency = 880, gain = 0.25): GainNode {
    const output = this.ctx.createGain();
    output.gain.setValueAtTime(gain, this.ctx.currentTime);

    // Múltiples voces desafinadas sutilmente
    for (let v = 0; v < 4; v++) {
      const osc = this.ctx.createOscillator();
      const g = this.ctx.createGain();
      const detune = (v - 1.5) * 6;

      osc.type = 'sine';
      osc.frequency.setValueAtTime(frequency, this.ctx.currentTime);
      osc.detune.setValueAtTime(detune, this.ctx.currentTime);

      // Vibrato rápido para shimmer
      const vibrato = this.ctx.createOscillator();
      const vibGain = this.ctx.createGain();
      vibrato.frequency.setValueAtTime(6 + v, this.ctx.currentTime);
      vibGain.gain.setValueAtTime(8, this.ctx.currentTime);
      vibrato.connect(vibGain);
      vibGain.connect(osc.frequency);
      vibrato.start(this.ctx.currentTime);

      g.gain.setValueAtTime(0, this.ctx.currentTime);
      g.gain.linearRampToValueAtTime(0.2, this.ctx.currentTime + 0.3);
      g.gain.setTargetAtTime(0.001, this.ctx.currentTime + 3, 0.8);

      osc.connect(g);
      g.connect(output);
      osc.start(this.ctx.currentTime);
    }

    return output;
  }
}
