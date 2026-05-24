// ============================================================
// DUAT Procedural Audio Engine v1.2.1
// Granular — Síntesis granular para fuego/agua/burbujeo
// Fingerprint: DUAT-v1.2.1-PROCEDURAL-AUDIO-AI-NPC
// ============================================================

/** Motor de síntesis granular */
export class GranularSynth {
  private ctx: AudioContext;
  private grains: AudioBufferSourceNode[] = [];
  private isPlaying = false;

  constructor(ctx: AudioContext) {
    this.ctx = ctx;
  }

  /** Genera un grain de ruido */
  private createGrain(
    duration: number,
    frequency: number,
    type: OscillatorType = 'sine',
    envelope = true
  ): { source: OscillatorNode; gain: GainNode } {
    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();

    osc.type = type;
    osc.frequency.setValueAtTime(frequency, this.ctx.currentTime);

    if (envelope) {
      gain.gain.setValueAtTime(0, this.ctx.currentTime);
      gain.gain.linearRampToValueAtTime(1, this.ctx.currentTime + duration * 0.1);
      gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + duration);
    } else {
      gain.gain.setValueAtTime(0.5, this.ctx.currentTime);
    }

    osc.connect(gain);
    osc.start(this.ctx.currentTime);
    osc.stop(this.ctx.currentTime + duration);

    return { source: osc, gain };
  }

  /** Flujo de grains con densidad controlada */
  startStream(
    density: number, // 0-1, grains por segundo
    minFreq: number,
    maxFreq: number,
    minGrainDur: number,
    maxGrainDur: number,
    gain = 0.3
  ): GainNode {
    const outputGain = this.ctx.createGain();
    outputGain.gain.setValueAtTime(gain, this.ctx.currentTime);
    this.isPlaying = true;

    const scheduleGrain = () => {
      if (!this.isPlaying) return;

      const grainDur = minGrainDur + Math.random() * (maxGrainDur - minGrainDur);
      const freq = minFreq + Math.random() * (maxFreq - minFreq);
      const type: OscillatorType = Math.random() > 0.5 ? 'sine' : 'triangle';

      const { gain: grainGain } = this.createGrain(grainDur, freq, type);
      grainGain.connect(outputGain);

      // Schedule next grain based on density
      const interval = (1000 / (density * 20 + 1)) * (0.8 + Math.random() * 0.4);
      setTimeout(scheduleGrain, interval);
    };

    scheduleGrain();
    return outputGain;
  }

  /** Crackle tipo fuego — impulses aleatorios */
  crackle(intensity = 0.5, density = 0.3): GainNode {
    const output = this.ctx.createGain();
    output.gain.setValueAtTime(intensity, this.ctx.currentTime);

    const scheduleCrackle = () => {
      if (!this.isPlaying) return;

      if (Math.random() < density) {
        // Impulso corto de ruido
        const bufferSize = Math.ceil(this.ctx.sampleRate * 0.01);
        const buffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
        const data = buffer.getChannelData(0);
        for (let i = 0; i < bufferSize; i++) {
          data[i] = (Math.random() * 2 - 1) * Math.exp(-i / (bufferSize * 0.3));
        }
        const source = this.ctx.createBufferSource();
        source.buffer = buffer;

        const gain = this.ctx.createGain();
        gain.gain.setValueAtTime(0.3 + Math.random() * 0.5, this.ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.02);

        // Filtro de frecuencia aleatoria
        const filter = this.ctx.createBiquadFilter();
        filter.type = 'bandpass';
        filter.frequency.setValueAtTime(
          2000 + Math.random() * 6000,
          this.ctx.currentTime
        );
        filter.Q.setValueAtTime(2 + Math.random() * 5, this.ctx.currentTime);

        source.connect(filter);
        filter.connect(gain);
        gain.connect(output);
        source.start(this.ctx.currentTime);
      }

      setTimeout(scheduleCrackle, 20 + Math.random() * 200);
    };

    this.isPlaying = true;
    scheduleCrackle();
    return output;
  }

  /** Burbujeo — grains cortos tipo agua */
  bubbles(density = 0.4, gain = 0.3): GainNode {
    return this.startStream(density, 400, 2000, 0.05, 0.15, gain);
  }

  /** Steam burst — grains de vapor */
  steamBursts(intensity = 0.5): GainNode {
    const output = this.ctx.createGain();
    output.gain.setValueAtTime(intensity, this.ctx.currentTime);
    this.isPlaying = true;

    const scheduleBurst = () => {
      if (!this.isPlaying) return;

      const bufferSize = Math.ceil(this.ctx.sampleRate * 0.3);
      const buffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
      const data = buffer.getChannelData(0);

      for (let i = 0; i < bufferSize; i++) {
        data[i] = (Math.random() * 2 - 1) * Math.exp(-i / (bufferSize * 0.4));
      }

      const source = this.ctx.createBufferSource();
      source.buffer = buffer;

      const filter = this.ctx.createBiquadFilter();
      filter.type = 'lowpass';
      filter.frequency.setValueAtTime(1500 + Math.random() * 1000, this.ctx.currentTime);

      const gain = this.ctx.createGain();
      gain.gain.setValueAtTime(0.2 + Math.random() * 0.3, this.ctx.currentTime);

      source.connect(filter);
      filter.connect(gain);
      gain.connect(output);
      source.start(this.ctx.currentTime);

      setTimeout(scheduleBurst, 300 + Math.random() * 1500);
    };

    scheduleBurst();
    return output;
  }

  /** Stop */
  stop(): void {
    this.isPlaying = false;
  }

  dispose(): void {
    this.stop();
    for (const grain of this.grains) {
      try { grain.stop(); } catch { /* ignore */ }
    }
    this.grains = [];
  }
}
