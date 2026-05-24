// ============================================================
// DUAT Procedural Audio Engine v1.2.1
// Noise — Generadores de ruido con tipos variados
// Fingerprint: DUAT-v1.2.1-PROCEDURAL-AUDIO-AI-NPC
// ============================================================

export type NoiseType = 'white' | 'pink' | 'brown' | 'blue' | 'violet';

/** Generador de ruido procedural */
export class NoiseGenerator {
  private ctx: AudioContext;

  constructor(ctx: AudioContext) {
    this.ctx = ctx;
  }

  /** Genera buffer de ruido del tipo especificado */
  generateBuffer(duration: number, type: NoiseType = 'white'): AudioBuffer {
    const samples = Math.ceil(this.ctx.sampleRate * duration);
    const buffer = this.ctx.createBuffer(1, samples, this.ctx.sampleRate);
    const data = buffer.getChannelData(0);

    switch (type) {
      case 'white':
        for (let i = 0; i < samples; i++) {
          data[i] = Math.random() * 2 - 1;
        }
        break;

      case 'pink': {
        // Voss-McCartney pink noise algorithm
        let b0 = 0, b1 = 0, b2 = 0, b3 = 0, b4 = 0, b5 = 0, b6 = 0;
        for (let i = 0; i < samples; i++) {
          const white = Math.random() * 2 - 1;
          b0 = 0.99886 * b0 + white * 0.0555179;
          b1 = 0.99332 * b1 + white * 0.0750759;
          b2 = 0.96900 * b2 + white * 0.1538520;
          b3 = 0.86650 * b3 + white * 0.3104856;
          b4 = 0.55000 * b4 + white * 0.5329522;
          b5 = -0.7616 * b5 - white * 0.0168980;
          data[i] = (b0 + b1 + b2 + b3 + b4 + b5 + b6 + white * 0.5362) * 0.11;
          b6 = white * 0.115926;
        }
        break;
      }

      case 'brown': {
        let lastOut = 0;
        for (let i = 0; i < samples; i++) {
          const white = Math.random() * 2 - 1;
          lastOut = (lastOut + 0.02 * white) / 1.02;
          data[i] = lastOut * 3.5;
        }
        break;
      }

      case 'blue': {
        let prev = 0;
        for (let i = 0; i < samples; i++) {
          const white = Math.random() * 2 - 1;
          data[i] = (white - prev) * 0.5;
          prev = white;
        }
        break;
      }

      case 'violet': {
        let prev = 0;
        for (let i = 0; i < samples; i++) {
          const white = Math.random() * 2 - 1;
          data[i] = (white - prev);
          prev = white;
        }
        break;
      }
    }

    return buffer;
  }

  /** Crea fuente de ruido en loop */
  createSource(
    duration = 2,
    type: NoiseType = 'white',
    gain = 0.5
  ): { source: AudioBufferSourceNode; gainNode: GainNode } {
    const buffer = this.generateBuffer(duration, type);
    const source = this.ctx.createBufferSource();
    source.buffer = buffer;
    source.loop = true;

    const gainNode = this.ctx.createGain();
    gainNode.gain.setValueAtTime(gain, this.ctx.currentTime);

    source.connect(gainNode);
    source.start(this.ctx.currentTime);

    return { source, gainNode };
  }

  /** Ruido con filtro aplicado — utilidad rápida */
  filteredNoise(
    type: NoiseType,
    filterType: BiquadFilterType,
    freq: number,
    Q: number,
    gain = 0.5,
    duration = 2
  ): { source: AudioBufferSourceNode; gainNode: GainNode; filter: BiquadFilterNode } {
    const { source, gainNode } = this.createSource(duration, type, 1);
    const filter = this.ctx.createBiquadFilter();
    filter.type = filterType;
    filter.frequency.setValueAtTime(freq, this.ctx.currentTime);
    filter.Q.setValueAtTime(Q, this.ctx.currentTime);

    gainNode.disconnect();
    gainNode.connect(filter);
    filter.connect(this.ctx.createGain());
    filter.connect(this.ctx.destination);

    const outputGain = this.ctx.createGain();
    outputGain.gain.setValueAtTime(gain, this.ctx.currentTime);
    filter.connect(outputGain);

    return { source, gainNode: outputGain, filter };
  }
}
