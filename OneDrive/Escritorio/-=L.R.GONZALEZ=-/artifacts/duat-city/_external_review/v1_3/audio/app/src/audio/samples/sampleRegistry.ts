// ============================================================
// DUAT Procedural Audio Engine v1.2.1
// Sample Registry — Registro de samples con allowlist
// Fingerprint: DUAT-v1.2.1-PROCEDURAL-AUDIO-AI-NPC
// ============================================================

import { type SampleDescriptor, type SampleRegistryEntry, type SampleApprovalStatus } from './sampleTypes';

/** Registro de samples con verificación */
export class SampleRegistry {
  private entries: Map<string, SampleRegistryEntry> = new Map();
  private allowlist: Set<string> = new Set();

  /** Registra un sample */
  register(descriptor: SampleDescriptor): SampleApprovalStatus {
    const status = this.determineStatus(descriptor);

    this.entries.set(descriptor.id, {
      ...descriptor,
      status,
      loaded: false,
      lastVerified: new Date().toISOString(),
    });

    if (status === 'APPROVED') {
      this.allowlist.add(descriptor.id);
    }

    return status;
  }

  /** Determina estado de aprobación */
  private determineStatus(descriptor: SampleDescriptor): SampleApprovalStatus {
    switch (descriptor.license) {
      case 'CC0':
        return 'APPROVED';
      case 'CC-BY':
        return descriptor.attribution ? 'APPROVED' : 'REVIEW';
      case 'CC-BY-NC':
        return 'BLOCKED';
      case 'UNKNOWN':
        return 'REVIEW';
      default:
        return 'REVIEW';
    }
  }

  /** Verifica si un sample está permitido */
  isAllowed(id: string): boolean {
    return this.allowlist.has(id);
  }

  /** Obtiene entry */
  get(id: string): SampleRegistryEntry | undefined {
    return this.entries.get(id);
  }

  /** Lista de entries aprobadas */
  getApproved(): SampleRegistryEntry[] {
    return Array.from(this.entries.values()).filter(e => e.status === 'APPROVED');
  }

  /** Lista de entries en review */
  getReview(): SampleRegistryEntry[] {
    return Array.from(this.entries.values()).filter(e => e.status === 'REVIEW');
  }

  /** Lista bloqueada */
  getBlocked(): SampleRegistryEntry[] {
    return Array.from(this.entries.values()).filter(e => e.status === 'BLOCKED');
  }

  /** Todos los entries */
  getAll(): SampleRegistryEntry[] {
    return Array.from(this.entries.values());
  }

  /** Número de samples */
  count(): number {
    return this.entries.size;
  }

  /** Exporta allowlist */
  exportAllowlist(): string[] {
    return Array.from(this.allowlist);
  }

  /** Limpia registro */
  clear(): void {
    this.entries.clear();
    this.allowlist.clear();
  }
}

/** Singleton */
let registryInstance: SampleRegistry | null = null;

export function getSampleRegistry(): SampleRegistry {
  if (!registryInstance) {
    registryInstance = new SampleRegistry();
  }
  return registryInstance;
}
