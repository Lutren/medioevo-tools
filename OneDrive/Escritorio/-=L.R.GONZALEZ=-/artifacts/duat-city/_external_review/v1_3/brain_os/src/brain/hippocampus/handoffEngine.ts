/**
 * Hipocampo / Handoff Persistence Engine
 * 
 * No guarda todo. Guarda solo el residuo que los filtros FBI 
 * no pudieron predecir. Es memoria comprimida por olvido selectivo.
 * 
 * Principio: la continuidad no depende de recordar todo.
 * Depende de externalizar lo mínimo necesario para reconstruir.
 */

import { HandoffManifest, OSITState, SystemMetrics } from '../../types';

export class HandoffPersistenceEngine {
  private manifests: Map<string, HandoffManifest> = new Map();
  private maxManifests = 64;
  private compressionRatio = 0.0;

  /**
   * Crear handoff desde estado actual.
   * Solo guarda el residuo, no el estado completo.
   */
  createHandoff(
    fingerprint: string,
    fullState: any,
    observer: OSITState,
    nextAction: string
  ): HandoffManifest {
    // Calcular residuo: diferencia entre estado actual y predicción
    const predicted = this.predictNextState(observer);
    const residueVector = this.computeResidueVector(fullState, predicted);

    const manifest: HandoffManifest = {
      fingerprint,
      timestamp: Date.now(),
      residueVector,
      predictedState: predicted,
      observerSnapshot: { ...observer, memory: new Float32Array(observer.memory) },
      nextAction,
      evidence: []
    };

    this.manifests.set(fingerprint, manifest);
    this.enforceLimit();

    this.compressionRatio = residueVector.length / JSON.stringify(fullState).length;

    return manifest;
  }

  /**
   * Reconstruir estado desde handoff + filtros.
   * El estado completo no se guarda; se reconstuye desde predicción + residuo.
   */
  reconstructState(fingerprint: string): { state: any; observer: OSITState } | null {
    const manifest = this.manifests.get(fingerprint);
    if (!manifest) return null;

    // Reconstruir: predicción + residuo = estado aproximado
    const reconstructed = this.applyResidueVector(
      manifest.predictedState, 
      manifest.residueVector
    );

    return {
      state: reconstructed,
      observer: manifest.observerSnapshot
    };
  }

  /**
   * Predicción simple basada en tendencia de memoria OSIT
   */
  private predictNextState(observer: OSITState): any {
    const m = observer.memory;
    const trend = m[3] - m[0];
    return {
      estimatedSignal: m[3] + trend * 0.5,
      estimatedGate: observer.gate,
      estimatedQ: observer.state,
      confidence: 1 - observer.noise
    };
  }

  /**
   * Vector de residuo: solo las componentes donde la predicción falló
   */
  private computeResidueVector(actual: any, predicted: any): Float32Array {
    const keys = Object.keys(actual).filter(k => typeof actual[k] === 'number');
    const residue = new Float32Array(keys.length);
    for (let i = 0; i < keys.length; i++) {
      const key = keys[i];
      const pred = predicted[key] !== undefined ? predicted[key] : 0;
      residue[i] = (actual[key] || 0) - pred;
    }
    return residue;
  }

  private applyResidueVector(predicted: any, residue: Float32Array): any {
    const keys = Object.keys(predicted).filter(k => typeof predicted[k] === 'number');
    const reconstructed: any = { ...predicted };
    for (let i = 0; i < Math.min(keys.length, residue.length); i++) {
      reconstructed[keys[i]] = (predicted[keys[i]] || 0) + residue[i];
    }
    return reconstructed;
  }

  private enforceLimit() {
    while (this.manifests.size > this.maxManifests) {
      const oldest = Array.from(this.manifests.entries())
        .sort((a, b) => a[1].timestamp - b[1].timestamp)[0];
      if (oldest) this.manifests.delete(oldest[0]);
    }
  }

  getManifest(fingerprint: string): HandoffManifest | undefined {
    return this.manifests.get(fingerprint);
  }

  getAllManifests(): HandoffManifest[] {
    return Array.from(this.manifests.values());
  }

  getCompressionRatio(): number { return this.compressionRatio; }
  getManifestCount(): number { return this.manifests.size; }
}
