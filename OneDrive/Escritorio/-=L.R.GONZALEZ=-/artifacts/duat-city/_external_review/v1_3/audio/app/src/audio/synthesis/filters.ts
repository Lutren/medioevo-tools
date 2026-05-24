// ============================================================
// DUAT Procedural Audio Engine v1.2.1
// Filters — Filtros biquad con modulación
// Fingerprint: DUAT-v1.2.1-PROCEDURAL-AUDIO-AI-NPC
// ============================================================

import { type FilterConfig } from '../audioTypes';

/** Filtro con capacidad de modulación */
export class Filter {
  private node: BiquadFilterNode;
  private ctx: AudioContext;
  private lfo: OscillatorNode | null = null;
  private lfoGain: GainNode | null = null;

  constructor(ctx: AudioContext) {
    this.ctx = ctx;
    this.node = ctx.createBiquadFilter();
  }

  /** Configura filtro */
  configure(config: FilterConfig): BiquadFilterNode {
    this.node.type = config.type;
    this.node.frequency.setValueAtTime(config.frequency, this.ctx.currentTime);
    this.node.Q.setValueAtTime(config.Q, this.ctx.currentTime);
    if (config.gain !== undefined) {
      this.node.gain.setValueAtTime(config.gain, this.ctx.currentTime);
    }
    return this.node;
  }

  /** Añade modulación LFO a la frecuencia */
  addLFO(lfoFreq: number, depth: number): void {
    this.lfo = this.ctx.createOscillator();
    this.lfoGain = this.ctx.createGain();
    this.lfo.frequency.setValueAtTime(lfoFreq, this.ctx.currentTime);
    this.lfoGain.gain.setValueAtTime(depth, this.ctx.currentTime);
    this.lfo.connect(this.lfoGain);
    this.lfoGain.connect(this.node.frequency);
    this.lfo.start(this.ctx.currentTime);
  }

  /** Filtro pasa-bajos resonante */
  lowpass(frequency: number, Q = 1): BiquadFilterNode {
    return this.configure({ type: 'lowpass', frequency, Q });
  }

  /** Filtro pasa-altos */
  highpass(frequency: number, Q = 1): BiquadFilterNode {
    return this.configure({ type: 'highpass', frequency, Q });
  }

  /** Filtro pasa-banda */
  bandpass(frequency: number, Q = 1): BiquadFilterNode {
    return this.configure({ type: 'bandpass', frequency, Q });
  }

  /** Filtro pico (vowel/formant) */
  peaking(frequency: number, Q: number, gain: number): BiquadFilterNode {
    return this.configure({ type: 'peaking', frequency, Q, gain });
  }

  /** Formante vocal — simula vocales A, E, I, O, U */
  formant(vowel: 'a' | 'e' | 'i' | 'o' | 'u', baseFreq = 200): BiquadFilterNode[] {
    const formants: Record<string, number[]> = {
      a: [730, 1090, 2440],
      e: [660, 1720, 2410],
      i: [270, 2290, 3010],
      o: [300, 870, 2240],
      u: [300, 1220, 2240],
    };
    const freqs = formants[vowel] || formants.a;
    return freqs.map((f, i) => this.peaking(baseFreq + f, 5 + i * 2, 10 + i * 3));
  }

  /** Sweep de frecuencia */
  sweep(to: number, duration: number): void {
    this.node.frequency.setTargetAtTime(to, this.ctx.currentTime, duration / 3);
  }

  /** Obtiene el nodo */
  getNode(): BiquadFilterNode {
    return this.node;
  }

  /** Conecta entrada */
  connectSource(source: AudioNode): void {
    source.connect(this.node);
  }

  /** Conecta salida */
  connectDestination(dest: AudioNode): void {
    this.node.connect(dest);
  }
}

/** Utilidades de filtro */
export const FilterUtil = {
  // Frecuencias de corte por tipo de material
  materialFilters: {
    water: { type: 'lowpass' as const, freq: 800, Q: 0.5 },
    fire: { type: 'highpass' as const, freq: 200, Q: 0.7 },
    metal: { type: 'bandpass' as const, freq: 3000, Q: 8 },
    glass: { type: 'highpass' as const, freq: 2000, Q: 4 },
    stone: { type: 'lowpass' as const, freq: 600, Q: 1 },
    wood: { type: 'lowpass' as const, freq: 1200, Q: 1.2 },
  },
  // Flicker LFO para neon
  flickerLFO: (ctx: AudioContext, rate = 8): { lfo: OscillatorNode; gain: GainNode } => {
    const lfo = ctx.createOscillator();
    const gain = ctx.createGain();
    lfo.type = 'sawtooth';
    lfo.frequency.setValueAtTime(rate, ctx.currentTime);
    gain.gain.setValueAtTime(30, ctx.currentTime);
    lfo.connect(gain);
    lfo.start(ctx.currentTime);
    return { lfo, gain };
  },
};
