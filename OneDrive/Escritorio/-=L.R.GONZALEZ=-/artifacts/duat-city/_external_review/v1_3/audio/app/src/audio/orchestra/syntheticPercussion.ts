// ============================================================
// DUAT Procedural Audio Engine v1.2.1
// Synthetic Percussion — Percusión sintética
// Fingerprint: DUAT-v1.2.1-PROCEDURAL-AUDIO-AI-NPC
// ============================================================

/** Percusión sintética: timpani, bells, bowed metal */
export class SyntheticPercussion {
  private ctx: AudioContext;

  constructor(ctx: AudioContext) {
    this.ctx = ctx;
  }

  /** Staccato hit */
  staccatoHit(frequency = 400, gain = 0.5): GainNode {
    const output = this.ctx.createGain();
    output.gain.setValueAtTime(gain, this.ctx.currentTime);

    const osc = this.ctx.createOscillator();
    const g = this.ctx.createGain();
    osc.type = 'sine';
    osc.frequency.setValueAtTime(frequency, this.ctx.currentTime);
    g.gain.setValueAtTime(0, this.ctx.currentTime);
    g.gain.linearRampToValueAtTime(0.8, this.ctx.currentTime + 0.02);
    g.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.3);
    osc.connect(g);
    g.connect(output);
    osc.start(this.ctx.currentTime);
    osc.stop(this.ctx.currentTime + 0.4);

    return output;
  }

  /** Timpani hit */
  timpaniHit(frequency = 100, gain = 0.6): GainNode {
    const output = this.ctx.createGain();
    output.gain.setValueAtTime(gain, this.ctx.currentTime);

    // Cuerpo: oscilador con pitch envelope descendente
    const osc = this.ctx.createOscillator();
    const g = this.ctx.createGain();

    osc.type = 'sine';
    osc.frequency.setValueAtTime(frequency * 1.5, this.ctx.currentTime);
    osc.frequency.setTargetAtTime(frequency, this.ctx.currentTime, 0.05);

    g.gain.setValueAtTime(0, this.ctx.currentTime);
    g.gain.linearRampToValueAtTime(1, this.ctx.currentTime + 0.01);
    g.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 1.2);

    osc.connect(g);
    g.connect(output);
    osc.start(this.ctx.currentTime);
    osc.stop(this.ctx.currentTime + 1.5);

    // Ruido de impacto
    const bufferSize = Math.ceil(this.ctx.sampleRate * 0.05);
    const buffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
    const data = buffer.getChannelData(0);
    for (let i = 0; i < bufferSize; i++) {
      data[i] = (Math.random() * 2 - 1) * Math.exp(-i / (bufferSize * 0.3));
    }
    const noise = this.ctx.createBufferSource();
    noise.buffer = buffer;

    const noiseGain = this.ctx.createGain();
    noiseGain.gain.setValueAtTime(0.3, this.ctx.currentTime);
    noiseGain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.05);

    noise.connect(noiseGain);
    noiseGain.connect(output);
    noise.start(this.ctx.currentTime);

    return output;
  }

  /** Campana/celesta */
  bell(frequency = 880, gain = 0.4): GainNode {
    const output = this.ctx.createGain();
    output.gain.setValueAtTime(gain, this.ctx.currentTime);

    // Parciales inarmónicos de campana
    const partials = [1, 1.17, 1.33, 1.53, 2.0, 2.67];
    const amps = [1, 0.7, 0.5, 0.35, 0.25, 0.2];
    const decays = [4, 3.5, 3, 2.5, 2, 1.5];

    for (let i = 0; i < partials.length; i++) {
      const osc = this.ctx.createOscillator();
      const g = this.ctx.createGain();

      osc.type = 'sine';
      osc.frequency.setValueAtTime(frequency * partials[i], this.ctx.currentTime);
      // Micro-detune para espesor
      osc.detune.setValueAtTime((Math.random() - 0.5) * 5, this.ctx.currentTime);

      g.gain.setValueAtTime(0, this.ctx.currentTime);
      g.gain.linearRampToValueAtTime(amps[i], this.ctx.currentTime + 0.005);
      g.gain.setTargetAtTime(0.001, this.ctx.currentTime + 0.1, decays[i] / 3);

      osc.connect(g);
      g.connect(output);
      osc.start(this.ctx.currentTime);
      osc.stop(this.ctx.currentTime + decays[i] + 0.5);
    }

    return output;
  }

  /** Bowed metal — metal frotado */
  bowedMetal(frequency = 200, gain = 0.3): GainNode {
    const output = this.ctx.createGain();
    output.gain.setValueAtTime(gain, this.ctx.currentTime);

    // Osciladores con vibrato irregular
    for (let i = 1; i <= 4; i++) {
      const osc = this.ctx.createOscillator();
      const g = this.ctx.createGain();

      osc.type = i === 1 ? 'triangle' : 'sine';
      osc.frequency.setValueAtTime(frequency * i * 1.01, this.ctx.currentTime);

      // Vibrato irregular
      const vibrato = this.ctx.createOscillator();
      const vibGain = this.ctx.createGain();
      vibrato.frequency.setValueAtTime(2 + i * 1.5, this.ctx.currentTime);
      vibGain.gain.setValueAtTime(20 + i * 5, this.ctx.currentTime);
      vibrato.connect(vibGain);
      vibGain.connect(osc.frequency);
      vibrato.start(this.ctx.currentTime);

      g.gain.setValueAtTime(0, this.ctx.currentTime);
      g.gain.linearRampToValueAtTime(0.2 / i, this.ctx.currentTime + 0.5);
      g.gain.setTargetAtTime(0.001, this.ctx.currentTime + 3, 0.8);

      osc.connect(g);
      g.connect(output);
      osc.start(this.ctx.currentTime);
    }

    // Bow noise
    const bufferSize = Math.ceil(this.ctx.sampleRate * 1);
    const buffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
    const data = buffer.getChannelData(0);
    for (let i = 0; i < bufferSize; i++) {
      data[i] = (Math.random() * 2 - 1) * 0.05;
    }
    const bow = this.ctx.createBufferSource();
    bow.buffer = buffer;
    bow.loop = true;

    const bowFilter = this.ctx.createBiquadFilter();
    bowFilter.type = 'bandpass';
    bowFilter.frequency.setValueAtTime(frequency * 2, this.ctx.currentTime);
    bowFilter.Q.setValueAtTime(2, this.ctx.currentTime);

    const bowGain = this.ctx.createGain();
    bowGain.gain.setValueAtTime(0.08, this.ctx.currentTime);

    bow.connect(bowFilter);
    bowFilter.connect(bowGain);
    bowGain.connect(output);
    bow.start(this.ctx.currentTime);

    return output;
  }

  /** Low percussion — golpe grave de tambor */
  lowPercussion(gain = 0.5): GainNode {
    const output = this.ctx.createGain();
    output.gain.setValueAtTime(gain, this.ctx.currentTime);

    // Ton + ruido
    const osc = this.ctx.createOscillator();
    const g = this.ctx.createGain();

    osc.type = 'sine';
    osc.frequency.setValueAtTime(80, this.ctx.currentTime);
    osc.frequency.setTargetAtTime(40, this.ctx.currentTime, 0.03);

    g.gain.setValueAtTime(0, this.ctx.currentTime);
    g.gain.linearRampToValueAtTime(1, this.ctx.currentTime + 0.005);
    g.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.6);

    osc.connect(g);
    g.connect(output);
    osc.start(this.ctx.currentTime);
    osc.stop(this.ctx.currentTime + 0.8);

    // Impact noise
    const bufSize = Math.ceil(this.ctx.sampleRate * 0.03);
    const buf = this.ctx.createBuffer(1, bufSize, this.ctx.sampleRate);
    const d = buf.getChannelData(0);
    for (let i = 0; i < bufSize; i++) {
      d[i] = (Math.random() * 2 - 1) * Math.exp(-i / (bufSize * 0.2));
    }
    const noise = this.ctx.createBufferSource();
    noise.buffer = buf;

    const ng = this.ctx.createGain();
    ng.gain.setValueAtTime(0.4, this.ctx.currentTime);
    ng.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.03);

    noise.connect(ng);
    ng.connect(output);
    noise.start(this.ctx.currentTime);

    return output;
  }
}
