/**
 * Sistema de Atención / GhostGate
 * 
 * No todo lo que entra al cerebro se procesa.
 * GhostGate filtra el intake: ¿esta señal reduce R o lo aumenta?
 * Si aumenta R, se bloquea antes de llegar a las cortezas.
 * 
 * Es el sistema inmune de información.
 * Crítico para no saturar CPU con ruido.
 * 
 * Principio: si no reduce residuo, no pasa.
 */

import { AttentionFilter, OSITState, SystemMetrics } from '../../types';
import { emlEvaluate } from '../../core/eml';

export interface Signal {
  channel: string;
  data: any;
  intensity: number;
  noise: number;
  timestamp: number;
}

export interface FilterResult {
  signal: Signal;
  passed: boolean;
  reason: string;
  predictedDeltaR: number;
}

export class GhostGateAttention {
  private filters: Map<string, AttentionFilter> = new Map();
  private history: Signal[] = [];
  private maxHistory = 32;
  private blockedCount = 0;
  private passedCount = 0;

  constructor() {
    // Filtros por defecto
    this.addFilter({
      channel: 'audio',
      signalThreshold: 0.1,
      noiseMax: 0.6,
      R_max: 0.7,
      pattern: 'reduce_residue'
    });
    this.addFilter({
      channel: 'visual',
      signalThreshold: 0.2,
      noiseMax: 0.5,
      R_max: 0.6,
      pattern: 'novelty_or_goal'
    });
    this.addFilter({
      channel: 'physics',
      signalThreshold: 0.05,
      noiseMax: 0.8,
      R_max: 0.8,
      pattern: 'delta_state'
    });
    this.addFilter({
      channel: 'npc',
      signalThreshold: 0.3,
      noiseMax: 0.4,
      R_max: 0.5,
      pattern: 'goal_aligned'
    });
  }

  addFilter(filter: AttentionFilter) {
    this.filters.set(filter.channel, filter);
  }

  /**
   * Evaluar señal: ¿pasa o se bloquea?
   */
  evaluate(signal: Signal, currentMetrics: SystemMetrics): FilterResult {
    const filter = this.filters.get(signal.channel);

    if (!filter) {
      // Canal desconocido: bloquear por defecto
      this.blockedCount++;
      return { signal, passed: false, reason: 'unknown_channel', predictedDeltaR: 0 };
    }

    // 1. Umbral de intensidad
    if (signal.intensity < filter.signalThreshold) {
      this.blockedCount++;
      return { signal, passed: false, reason: 'below_threshold', predictedDeltaR: 0 };
    }

    // 2. Umbral de ruido
    if (signal.noise > filter.noiseMax) {
      this.blockedCount++;
      return { signal, passed: false, reason: 'too_noisy', predictedDeltaR: 0 };
    }

    // 3. R del sistema
    if (currentMetrics.R > filter.R_max) {
      this.blockedCount++;
      return { signal, passed: false, reason: 'system_saturated', predictedDeltaR: 0 };
    }

    // 4. Predicción de delta R
    const predictedDeltaR = this.predictDeltaR(signal, filter);
    if (predictedDeltaR > 0) {
      // Esta señal aumentaría el residuo
      this.blockedCount++;
      return { signal, passed: false, reason: 'increases_residue', predictedDeltaR };
    }

    // Pasa
    this.passedCount++;
    this.history.push(signal);
    if (this.history.length > this.maxHistory) this.history.shift();

    return { signal, passed: true, reason: 'reduces_residue', predictedDeltaR };
  }

  /**
   * Predice si la señal aumentará o reducirá R
   */
  private predictDeltaR(signal: Signal, filter: AttentionFilter): number {
    // Modelo simple: señales repetidas aumentan R (redundancia)
    // señales novedosas alineadas con goal reducen R
    const recent = this.history.filter(h => h.channel === signal.channel);
    const avgRecent = recent.length > 0 
      ? recent.reduce((s, h) => s + h.intensity, 0) / recent.length 
      : 0;

    const novelty = Math.abs(signal.intensity - avgRecent);
    const signalQuality = signal.intensity * (1 - signal.noise);

    // Si es novedosa y de calidad, reduce R
    // Si es repetitiva o ruidosa, aumenta R
    return signalQuality < 0.3 ? 0.1 : -novelty * 0.2;
  }

  getStats() {
    const total = this.blockedCount + this.passedCount;
    return {
      blocked: this.blockedCount,
      passed: this.passedCount,
      ratio: total > 0 ? this.blockedCount / total : 0,
      channels: Array.from(this.filters.keys())
    };
  }

  getHistory(): Signal[] { return [...this.history]; }
}
