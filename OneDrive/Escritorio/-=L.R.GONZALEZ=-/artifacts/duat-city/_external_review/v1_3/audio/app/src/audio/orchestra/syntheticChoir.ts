// ============================================================
// DUAT Procedural Audio Engine v1.2.1
// Synthetic Choir — Coro sintético con formantes vocálicas
// Fingerprint: DUAT-v1.2.1-PROCEDURAL-AUDIO-AI-NPC
// ============================================================

/** Coro sintético con formantes A, E, I, O, U */
export class SyntheticChoir {
  private ctx: AudioContext;

  constructor(ctx: AudioContext) {
    this.ctx = ctx;
  }

  /** Coro pad sostenido */
  pad(fundamental = 330, vowel: 'a' | 'e' | 'i' | 'o' | 'u' = 'o', gain = 0.3): GainNode {
    const output = this.ctx.createGain();
    output.gain.setValueAtTime(gain, this.ctx.currentTime);

    // Formantes de la vocal
    const formants: Record<string, number[]> = {
      a: [730, 1090, 2440],
      e: [660, 1720, 2410],
      i: [270, 2290, 3010],
      o: [300, 870, 2240],
      u: [300, 1220, 2240],
    };
    const freqs = formants[vowel];

    // Múltiples voces desafinadas
    for (let v = 0; v < 5; v++) {
      // Oscilador base
      const osc = this.ctx.createOscillator();
      const g = this.ctx.createGain();

      osc.type = v < 2 ? 'sine' : v < 4 ? 'triangle' : 'sawtooth';
      osc.frequency.setValueAtTime(fundamental, this.ctx.currentTime);
      osc.detune.setValueAtTime((v - 2) * 10 + (Math.random() - 0.5) * 4, this.ctx.currentTime);

      g.gain.setValueAtTime(0, this.ctx.currentTime);
      g.gain.linearRampToValueAtTime(0.15, this.ctx.currentTime + 1.0);
      g.gain.setTargetAtTime(0.001, this.ctx.currentTime + 4, 1.5);

      // Aplicar formantes como filtros
      let filtered: AudioNode = osc;
      for (const ff of freqs) {
        const filter = this.ctx.createBiquadFilter();
        filter.type = 'peaking';
        filter.frequency.setValueAtTime(ff, this.ctx.currentTime);
        filter.Q.setValueAtTime(8, this.ctx.currentTime);
        filter.gain.setValueAtTime(10, this.ctx.currentTime);
        filtered.connect(filter);
        filtered = filter;
      }

      g.connect(output);
      if (filtered !== osc) {
        (filtered as AudioNode).connect(g);
      }
      osc.start(this.ctx.currentTime);
    }

    return output;
  }

  /** Drone coral */
  drone(fundamental = 220, gain = 0.25): GainNode {
    return this.pad(fundamental, 'o', gain);
  }

  /** Suspiro coral (breath) */
  breath(gain = 0.2): GainNode {
    const output = this.ctx.createGain();
    output.gain.setValueAtTime(gain, this.ctx.currentTime);

    // Ruido filtrado con envolvente de respiración
    const bufferSize = Math.ceil(this.ctx.sampleRate * 2);
    const buffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
    const data = buffer.getChannelData(0);
    for (let i = 0; i < bufferSize; i++) {
      data[i] = (Math.random() * 2 - 1) * 0.5;
    }
    const src = this.ctx.createBufferSource();
    src.buffer = buffer;
    src.loop = true;

    const filter = this.ctx.createBiquadFilter();
    filter.type = 'bandpass';
    filter.frequency.setValueAtTime(2000, this.ctx.currentTime);
    filter.Q.setValueAtTime(0.5, this.ctx.currentTime);

    const g = this.ctx.createGain();
    g.gain.setValueAtTime(0, this.ctx.currentTime);
    g.gain.linearRampToValueAtTime(0.5, this.ctx.currentTime + 0.8);
    g.gain.setTargetAtTime(0.001, this.ctx.currentTime + 2, 0.5);

    src.connect(filter);
    filter.connect(g);
    g.connect(output);
    src.start(this.ctx.currentTime);

    return output;
  }
}
