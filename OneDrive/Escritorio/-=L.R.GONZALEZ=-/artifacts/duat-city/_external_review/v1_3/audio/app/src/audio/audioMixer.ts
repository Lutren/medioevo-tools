// ============================================================
// DUAT Procedural Audio Engine v1.2.1
// Audio Mixer — Mezclador multi-bus
// Fingerprint: DUAT-v1.2.1-PROCEDURAL-AUDIO-AI-NPC
// ============================================================

import { type AudioBusName, type BusConfig } from './audioTypes';

/** Mezclador que controla niveles de todos los buses */
export class AudioMixer {
  private busGains: Map<AudioBusName, number> = new Map();
  private busMutes: Map<AudioBusName, boolean> = new Map();
  private soloBus: AudioBusName | null = null;

  constructor(defaults: BusConfig[]) {
    for (const bus of defaults) {
      this.busGains.set(bus.name, bus.gain);
      this.busMutes.set(bus.name, bus.muted);
    }
  }

  /** Establece gain de bus (0-1) */
  setBusGain(bus: AudioBusName, value: number): void {
    const clamped = Math.max(0, Math.min(2, value));
    this.busGains.set(bus, clamped);
  }

  /** Obtiene gain de bus */
  getBusGain(bus: AudioBusName): number {
    if (this.soloBus && bus !== this.soloBus && bus !== 'master') return 0;
    if (this.busMutes.get(bus)) return 0;
    return this.busGains.get(bus) ?? 0.5;
  }

  /** Mute/unmute bus */
  setBusMute(bus: AudioBusName, muted: boolean): void {
    this.busMutes.set(bus, muted);
  }

  /** Solo un bus */
  setSolo(bus: AudioBusName | null): void {
    this.soloBus = bus;
  }

  /** Obtiene estado de todos los buses */
  getAllLevels(): Record<AudioBusName, number> {
    const result = {} as Record<AudioBusName, number>;
    for (const [name] of this.busGains) {
      result[name] = this.getBusGain(name);
    }
    return result;
  }

  /** Resetea todos los niveles */
  reset(): void {
    for (const [name] of this.busGains) {
      this.busGains.set(name, 0.5);
      this.busMutes.set(name, false);
    }
    this.soloBus = null;
  }

  /** Exporta configuración */
  exportConfig(): Partial<Record<AudioBusName, { gain: number; muted: boolean }>> {
    const result: Partial<Record<AudioBusName, { gain: number; muted: boolean }>> = {};
    for (const [name] of this.busGains) {
      result[name] = {
        gain: this.busGains.get(name) ?? 0.5,
        muted: this.busMutes.get(name) ?? false,
      };
    }
    return result;
  }
}
