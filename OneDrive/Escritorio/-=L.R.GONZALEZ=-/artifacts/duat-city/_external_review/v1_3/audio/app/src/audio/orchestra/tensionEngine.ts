// ============================================================
// DUAT Procedural Audio Engine v1.2.1
// Tension Engine — Motor de tensión armónica
// Fingerprint: DUAT-v1.2.1-PROCEDURAL-AUDIO-AI-NPC
// ============================================================

// MoodType available for future mood-based tension curves

interface TensionConfig {
  level: number;
  intervals: number[];
  clusters: boolean;
  dissonance: number;
}

/** Motor de tensión para audio dinámico */
export class TensionEngine {
  private currentTension = 0;
  private targetTension = 0;
  private tensionVelocity = 0;

  /** Establece tensión objetivo */
  setTargetTension(level: number): void {
    this.targetTension = Math.max(0, Math.min(1, level));
  }

  /** Obtiene tensión actual */
  getTension(): number {
    return this.currentTension;
  }

  /** Update — interpola tensión */
  update(dt: number): void {
    const diff = this.targetTension - this.currentTension;
    this.tensionVelocity += diff * dt * 2;
    this.tensionVelocity *= 0.9; // damping
    this.currentTension += this.tensionVelocity * dt;
    this.currentTension = Math.max(0, Math.min(1, this.currentTension));
  }

  /** Tensión desde R (residuo) */
  tensionFromR(R: number): number {
    // R alto = más tensión
    return Math.min(1, R * 2);
  }

  /** Tensión desde Phi_eff */
  tensionFromPhiEff(PhiEff: number): number {
    // Phi_eff bajo = más tensión
    return Math.max(0, 1 - PhiEff);
  }

  /** Config de tensión basada en nivel */
  getTensionConfig(level = this.currentTension): TensionConfig {
    if (level < 0.25) {
      return {
        level,
        intervals: [0, 4, 7, 12], // consonante
        clusters: false,
        dissonance: 0,
      };
    } else if (level < 0.5) {
      return {
        level,
        intervals: [0, 3, 7, 10], // menor
        clusters: false,
        dissonance: 0.3,
      };
    } else if (level < 0.75) {
      return {
        level,
        intervals: [0, 1, 4, 6, 8], // tensa
        clusters: true,
        dissonance: 0.6,
      };
    } else {
      return {
        level,
        intervals: [0, 1, 2, 3, 6, 8], // muy tensa
        clusters: true,
        dissonance: 0.9,
      };
    }
  }

  /** Intervalos seguros para nivel de tensión */
  getSafeIntervals(level = this.currentTension): number[] {
    const config = this.getTensionConfig(level);
    return config.intervals;
  }

  /** Frecuencias de tensión a partir de fundamental */
  getTensionFrequencies(fundamental: number, level = this.currentTension): number[] {
    const intervals = this.getSafeIntervals(level);
    return intervals.map(semitones => fundamental * Math.pow(2, semitones / 12));
  }

  /** Score de tensión para un conjunto de frecuencias */
  calculateTensionScore(frequencies: number[]): number {
    let dissonance = 0;
    for (let i = 0; i < frequencies.length; i++) {
      for (let j = i + 1; j < frequencies.length; j++) {
        const ratio = frequencies[j] / frequencies[i];
        const semitones = 12 * Math.log2(ratio);
        const roundSemitones = Math.round(semitones);
        const error = Math.abs(semitones - roundSemitones);

        // Disonancia basada en error de afinación
        if (error > 0.1) {
          dissonance += error;
        }
      }
    }
    return Math.min(1, dissonance / frequencies.length);
  }
}
