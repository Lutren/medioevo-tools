/**
 * Cerebelo / Quaternary Timing Core Global
 * 
 * Reloj maestro del cerebro. Todos los motores sincronizados
 * a un mismo τ (tau) de tiempo.
 * 
 * No cada motor con su propio delta. Un τ maestro reduce drift.
 * 
 * Principio: el tiempo no es uniforme. Es quaternario.
 * 00 = pausa/silencio
 * 01 = preparación/anticipación  
 * 10 = ejecución/acción
 * 11 = resolución/cierre
 */

import { TimingTick, QState } from '../../types';

export interface TimingConfig {
  bpm: number;           // beats per minute
  beatsPerBar: number;   // compás
  subdivisions: number;  // subdivisiones por beat
}

export class QuaternaryTimingCore {
  private config: TimingConfig;
  private globalFrame = 0;
  private phase = 0;      // 0-1 dentro del beat
  private beat = 0;       // beat actual
  private bar = 0;        // compás actual
  private subscribers: Map<string, (tick: TimingTick) => void> = new Map();

  constructor(config: TimingConfig = { bpm: 120, beatsPerBar: 4, subdivisions: 4 }) {
    this.config = config;
  }

  /**
   * Tick maestro. Todos los motores reciben este τ.
   */
  tick(dt: number): TimingTick {
    this.globalFrame++;

    // Avanzar fase
    const beatDuration = 60 / this.config.bpm;
    this.phase += dt / beatDuration;

    if (this.phase >= 1) {
      this.phase -= 1;
      this.beat++;

      if (this.beat >= this.config.beatsPerBar) {
        this.beat = 0;
        this.bar++;
      }
    }

    const tick: TimingTick = {
      tau: this.globalFrame * dt,
      phase: this.phase,
      beat: this.beat,
      globalFrame: this.globalFrame
    };

    // Notificar suscriptores
    for (const callback of this.subscribers.values()) {
      callback(tick);
    }

    return tick;
  }

  /**
   * Q-state del timing actual
   */
  getTimingQ(): QState {
    const subPhase = Math.floor(this.phase * 4) / 4;
    if (subPhase < 0.25) return '00'; // pausa
    if (subPhase < 0.5) return '01';  // preparación
    if (subPhase < 0.75) return '10'; // ejecución
    return '11'; // resolución
  }

  /**
   * Suscribir motor al reloj maestro
   */
  subscribe(name: string, callback: (tick: TimingTick) => void) {
    this.subscribers.set(name, callback);
  }

  unsubscribe(name: string) {
    this.subscribers.delete(name);
  }

  /**
   * Tempo adaptativo: si R alto, baja BPM (más tiempo para procesar)
   */
  adaptTempo(R: number) {
    const baseBpm = this.config.bpm;
    if (R > 0.6) {
      this.config.bpm = Math.max(60, baseBpm * 0.7);
    } else if (R < 0.2) {
      this.config.bpm = Math.min(180, baseBpm * 1.1);
    }
  }

  getConfig(): TimingConfig { return { ...this.config }; }
  getGlobalFrame(): number { return this.globalFrame; }
  getBeat(): number { return this.beat; }
  getBar(): number { return this.bar; }
}
