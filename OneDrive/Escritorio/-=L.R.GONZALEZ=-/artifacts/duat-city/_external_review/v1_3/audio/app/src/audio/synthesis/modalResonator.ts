// ============================================================
// DUAT Procedural Audio Engine v1.2.1
// Modal Resonator — Resonancia para metal/cristal/madera
// Fingerprint: DUAT-v1.2.1-PROCEDURAL-AUDIO-AI-NPC
// ============================================================

const PHI = 1.618033988749895;

/** Presets de resonancia por material */
export const ModalPresets = {
  // Metal: parciales inarmónicos altos, decay largo
  metal: {
    ratios: [1, 2.76, 5.4, 8.9, 13.3],
    decays: [2.0, 1.5, 1.0, 0.7, 0.5],
    gains: [1.0, 0.6, 0.4, 0.25, 0.15],
  },
  // Cristal: parciales limpios, decay muy largo
  crystal: {
    ratios: [1, 2.0, 3.0, 4.2, 5.4],
    decays: [4.0, 3.5, 3.0, 2.5, 2.0],
    gains: [1.0, 0.7, 0.5, 0.35, 0.2],
  },
  // Madera: parciales dispersos, decay corto
  wood: {
    ratios: [1, 1.6, 2.8, 4.5, 6.8],
    decays: [0.8, 0.6, 0.4, 0.25, 0.15],
    gains: [1.0, 0.5, 0.3, 0.2, 0.1],
  },
  // Piedra: pocos parciales, decay muy corto
  stone: {
    ratios: [1, 1.8, 3.2],
    decays: [0.4, 0.25, 0.15],
    gains: [1.0, 0.4, 0.2],
  },
  // Fibonacci-Mobius: parciales escalados por φ
  fibmob: {
    ratios: [1, PHI, PHI * PHI, PHI * PHI * PHI, PHI * PHI * PHI * PHI],
    decays: [3.0, 2.5, 2.0, 1.5, 1.0],
    gains: [1.0, 0.618, 0.382, 0.236, 0.146],
  },
};

export type ModalPreset = keyof typeof ModalPresets;

/** Resonador modal — simula vibración de objetos físicos */
export class ModalResonator {
  private ctx: AudioContext;
  private oscillators: OscillatorNode[] = [];
  private gains: GainNode[] = [];

  constructor(ctx: AudioContext) {
    this.ctx = ctx;
  }

  /** Excita el resonador con parámetros */
  excite(
    fundamental: number,
    preset: ModalPreset = 'metal',
    excitationGain = 0.5
  ): GainNode {
    const config = ModalPresets[preset];
    const output = this.ctx.createGain();
    output.gain.setValueAtTime(excitationGain, this.ctx.currentTime);

    for (let i = 0; i < config.ratios.length; i++) {
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();

      osc.type = 'sine';
      osc.frequency.setValueAtTime(fundamental * config.ratios[i], this.ctx.currentTime);

      // Detune sutil para naturalidad
      osc.detune.setValueAtTime(
        (Math.random() - 0.5) * 10,
        this.ctx.currentTime
      );

      // Amplitud inicial
      gain.gain.setValueAtTime(config.gains[i], this.ctx.currentTime);

      // Decay exponencial
      gain.gain.setTargetAtTime(
        0.001,
        this.ctx.currentTime + 0.01,
        config.decays[i] / 3
      );

      osc.connect(gain);
      gain.connect(output);
      osc.start(this.ctx.currentTime);

      // Stop después del decay
      setTimeout(() => {
        try { osc.stop(); } catch { /* ignore */ }
      }, config.decays[i] * 1000 + 100);

      this.oscillators.push(osc);
      this.gains.push(gain);
    }

    return output;
  }

  /** Golpe de metal */
  metalHit(frequency = 800, gain = 0.5): GainNode {
    return this.excite(frequency, 'metal', gain);
  }

  /** Cristal/glass */
  glassHit(frequency = 1200, gain = 0.4): GainNode {
    return this.excite(frequency, 'crystal', gain);
  }

  /** Piedra */
  stoneHit(frequency = 400, gain = 0.6): GainNode {
    return this.excite(frequency, 'stone', gain);
  }

  /** Madera */
  woodHit(frequency = 600, gain = 0.5): GainNode {
    return this.excite(frequency, 'wood', gain);
  }

  /** FibMob resonancia (para sonidos místicos) */
  fibResonance(fundamental = 220, gain = 0.4): GainNode {
    return this.excite(fundamental, 'fibmob', gain);
  }

  /** Libera recursos */
  dispose(): void {
    for (const osc of this.oscillators) {
      try { osc.stop(); } catch { /* ignore */ }
    }
    for (const g of this.gains) {
      g.disconnect();
    }
    this.oscillators = [];
    this.gains = [];
  }
}
