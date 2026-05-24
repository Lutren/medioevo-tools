// ============================================================
// DUAT Procedural Audio Engine v1.2.1
// Motif Generator — Generación de motivos procedurales
// Fingerprint: DUAT-v1.2.1-PROCEDURAL-AUDIO-AI-NPC
// ============================================================

import { type MoodType, type Motif } from '../audioTypes';

const PHI = 1.618033988749895;

/** Mapa de moods a escalas (intervalos en semitonos) */
const MoodScales: Record<string, number[]> = {
  archive: [0, 3, 5, 7, 10, 12], // menor melódica
  forge: [0, 2, 4, 7, 9, 12], // mayor pentatónica
  garden: [0, 2, 4, 5, 7, 9, 11, 12], // lidia
  market: [0, 2, 3, 5, 7, 8, 10, 12], // frigia
  ruin: [0, 1, 3, 6, 8, 12], // locria fragmentada
  gate_review: [0, 2, 5, 7, 9, 12], // suspendida
  gate_block: [0, 1, 4, 6, 8, 11, 12], // disonante
  silence: [0, 12],
};

/** Base notes por mood */
const MoodRoots: Record<string, number> = {
  archive: 220, // A3
  forge: 165, // E3
  garden: 330, // E4
  market: 196, // G3
  ruin: 146, // D3
  gate_review: 247, // B3
  gate_block: 110, // A2
  silence: 440,
};

/** Genera motivos musicales procedurales */
export class MotifGenerator {
  private seed: number;

  constructor(seed = Date.now()) {
    this.seed = seed;
  }

  /** RNG con seed */
  private random(): number {
    this.seed = (this.seed * 1103515245 + 12345) & 0x7fffffff;
    return this.seed / 0x7fffffff;
  }

  /** Genera motivo para un mood */
  generateMotif(
    mood: MoodType,
    length = 4,
    tension = 0.5
  ): Motif {
    const scale = MoodScales[mood] || MoodScales.archive;
    const root = MoodRoots[mood] || 220;

    const notes: number[] = [];
    const durations: number[] = [];
    const amplitudes: number[] = [];

    for (let i = 0; i < length; i++) {
      const scaleIndex = Math.floor(this.random() * scale.length);
      const octave = Math.floor(this.random() * 2); // 0 o 1 octava arriba
      const semitones = scale[scaleIndex] + octave * 12;
      const freq = root * Math.pow(2, semitones / 12);

      notes.push(freq);
      durations.push(0.25 + this.random() * 0.75);
      amplitudes.push(0.3 + this.random() * 0.4 * (1 - tension * 0.3));
    }

    return {
      notes,
      durations,
      amplitudes,
      instrument: this.selectInstrument(mood),
      tension,
    };
  }

  /** Motif de rol para NPC */
  generateRoleMotif(role: string): Motif {
    const rolePatterns: Record<string, { root: number; intervals: number[] }> = {
      guard: { root: 200, intervals: [0, 0, 4, 7, 4, 0] },
      merchant: { root: 300, intervals: [0, 2, 4, 2, 0, 5, 4] },
      scholar: { root: 250, intervals: [0, 3, 7, 12, 7, 3] },
      mystic: { root: 180, intervals: [0, 1, 6, 8, 6, 1] },
      rogue: { root: 350, intervals: [0, 3, 5, 8, 5, 3, 0] },
      elder: { root: 150, intervals: [0, 4, 7, 12, 7, 4, 0] },
    };

    const pattern = rolePatterns[role] || rolePatterns.guard;
    const notes = pattern.intervals.map(n => pattern.root * Math.pow(2, n / 12));
    const durations = notes.map(() => 0.3 + this.random() * 0.4);
    const amplitudes = notes.map(() => 0.3 + this.random() * 0.3);

    return { notes, durations, amplitudes, instrument: 'strings', tension: 0.4 };
  }

  /** Motif emocional */
  generateEmotionalMotif(
    emotion: 'calm' | 'alert' | 'agitated' | 'fearful' | 'curious' | 'hostile' | 'mystical'
  ): Motif {
    const emotionConfig: Record<string, { root: number; tension: number; intervals: number[] }> = {
      calm: { root: 264, tension: 0.1, intervals: [0, 4, 7, 12, 7, 4, 0] },
      alert: { root: 330, tension: 0.4, intervals: [0, 2, 5, 7, 5, 2] },
      agitated: { root: 220, tension: 0.7, intervals: [0, 1, 3, 6, 1, 8] },
      fearful: { root: 185, tension: 0.8, intervals: [0, 1, 4, 6, 11, 4] },
      curious: { root: 370, tension: 0.3, intervals: [0, 2, 4, 7, 9, 4, 2] },
      hostile: { root: 146, tension: 0.9, intervals: [0, 1, 3, 6, 8, 1] },
      mystical: { root: 220, tension: 0.5, intervals: [0, 3, 5, 8, 12, 8, 5, 3] },
    };

    const config = emotionConfig[emotion] || emotionConfig.calm;
    const notes = config.intervals.map(n => config.root * Math.pow(2, n / 12));
    const durations = notes.map(() => 0.2 + this.random() * 0.5);
    const amplitudes = notes.map(() => 0.3 + this.random() * 0.3);

    return {
      notes,
      durations,
      amplitudes,
      instrument: emotion === 'mystical' ? 'choir' : emotion === 'hostile' ? 'brass' : 'strings',
      tension: config.tension,
    };
  }

  /** Fibonacci motif — usa φ para generar intervalos */
  generateFibMotif(baseFreq = 220, length = 5): Motif {
    const notes: number[] = [];
    const durations: number[] = [];
    const amplitudes: number[] = [];

    let a = 1, b = 1;
    for (let i = 0; i < length; i++) {
      const interval = (a * PHI) % 12;
      notes.push(baseFreq * Math.pow(2, interval / 12));
      durations.push(0.5 * (b / (a + b)));
      amplitudes.push(0.5 / (1 + i * 0.2));

      const temp = a + b;
      a = b;
      b = temp;
    }

    return { notes, durations, amplitudes, instrument: 'choir', tension: 0.4 };
  }

  /** Selecciona instrumento según mood */
  private selectInstrument(mood: MoodType): string {
    const mapping: Record<string, string> = {
      archive: 'choir',
      forge: 'brass',
      garden: 'strings',
      market: 'percussion',
      ruin: 'additive',
      gate_review: 'strings',
      gate_block: 'brass',
      silence: 'none',
    };
    return mapping[mood] || 'strings';
  }
}
