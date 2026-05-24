// ============================================================
// DUAT Procedural Audio Engine v1.2.1
// Sample Loader — Cargador de samples con verificación
// Fingerprint: DUAT-v1.2.1-PROCEDURAL-AUDIO-AI-NPC
// ============================================================

import { type SampleDescriptor } from './sampleTypes';
import { getSampleRegistry } from './sampleRegistry';

/** Cargador de samples */
export class SampleLoader {
  private ctx: AudioContext;
  private cache: Map<string, AudioBuffer> = new Map();

  constructor(ctx: AudioContext) {
    this.ctx = ctx;
  }

  /** Carga un sample si está en allowlist */
  async loadSample(descriptor: SampleDescriptor): Promise<AudioBuffer | null> {
    const registry = getSampleRegistry();

    // Verificar allowlist
    if (!registry.isAllowed(descriptor.id)) {
      console.warn(`[DUAT-AUDIO] Sample ${descriptor.id} no está en allowlist`);
      return null;
    }

    // Verificar cache
    if (this.cache.has(descriptor.id)) {
      return this.cache.get(descriptor.id)!;
    }

    try {
      // En un entorno real, aquí se cargaría desde URL
      // Para este motor procedural, generamos un buffer placeholder
      const buffer = await this.generatePlaceholderBuffer(descriptor);
      this.cache.set(descriptor.id, buffer);
      return buffer;
    } catch (err) {
      console.warn(`[DUAT-AUDIO] Error cargando sample ${descriptor.id}:`, err);
      return null;
    }
  }

  /** Genera buffer placeholder (el motor es procedural, no sample-based) */
  private async generatePlaceholderBuffer(descriptor: SampleDescriptor): Promise<AudioBuffer> {
    const duration = descriptor.duration || 1.0;
    const sampleRate = this.ctx.sampleRate;
    const samples = Math.ceil(sampleRate * duration);
    const buffer = this.ctx.createBuffer(1, samples, sampleRate);
    const data = buffer.getChannelData(0);

    // Generar silencio (el motor es procedural)
    for (let i = 0; i < samples; i++) {
      data[i] = 0;
    }

    return buffer;
  }

  /** Obtiene de cache */
  getFromCache(id: string): AudioBuffer | undefined {
    return this.cache.get(id);
  }

  /** Limpia cache */
  clearCache(): void {
    this.cache.clear();
  }

  /** Tamaño de cache */
  cacheSize(): number {
    return this.cache.size;
  }
}

export function createSampleLoader(ctx: AudioContext): SampleLoader {
  return new SampleLoader(ctx);
}
