/**
 * Light Bridge — Luz genera Audio
 * 
 * Un cambio de estado lumínico emite un delta de audio automáticamente.
 * Transducción MTS directa.
 * 
 * Q=11 (burst lumínico) → evento sonoro gateApprove / eventBurst
 * Q=01 (anomalía) → missing signal pulse
 */

import { WorldCell, AudioEvent, QState } from '../types';
import { QStateMap } from '../core/qstate';

export interface LightAudioEvent {
  cell: WorldCell;
  event: AudioEvent;
}

export class LightAudioBridge {
  private lastQStates: Map<string, QState> = new Map();

  process(cells: WorldCell[], frame: number): LightAudioEvent[] {
    const events: LightAudioEvent[] = [];

    for (const cell of cells) {
      const key = `${cell.x},${cell.y}`;
      const lastQ = this.lastQStates.get(key);
      const currentQ = cell.light.qLight;

      if (lastQ && lastQ !== currentQ) {
        // Transición Q detectada → evento de audio
        const event = this.qTransitionToAudio(lastQ, currentQ, cell, frame);
        if (event) {
          events.push({ cell, event });
          if (!cell.audio) cell.audio = { eventQueue: [], materialResonance: 0 };
          cell.audio.eventQueue.push(event);
        }
      }

      this.lastQStates.set(key, currentQ);
    }

    return events;
  }

  private qTransitionToAudio(
    from: QState, 
    to: QState, 
    cell: WorldCell, 
    frame: number
  ): AudioEvent | null {
    const key = `${from}->${to}`;

    const map: Record<string, { type: string; intensity: number }> = {
      '00->01': { type: 'missing_signal_pulse', intensity: 0.3 },
      '00->10': { type: 'light_stable_hum', intensity: 0.5 },
      '00->11': { type: 'event_burst', intensity: 1.0 },
      '01->00': { type: 'silence_return', intensity: 0.2 },
      '01->10': { type: 'anomaly_resolve', intensity: 0.6 },
      '01->11': { type: 'anomaly_burst', intensity: 0.9 },
      '10->00': { type: 'light_fade', intensity: 0.4 },
      '10->01': { type: 'stable_anomaly', intensity: 0.5 },
      '10->11': { type: 'stable_burst', intensity: 0.8 },
      '11->00': { type: 'burst_end', intensity: 0.3 },
      '11->01': { type: 'burst_anomaly', intensity: 0.7 },
      '11->10': { type: 'burst_stabilize', intensity: 0.6 }
    };

    const def = map[key];
    if (!def) return null;

    // Modulación por material
    let intensity = def.intensity;
    if (cell.material === 'GLASS') intensity *= 1.2; // resonancia
    if (cell.material === 'METAL') intensity *= 0.8; // amortigua
    if (cell.material === 'WATER') intensity *= 0.6; // difumina

    return {
      type: def.type,
      intensity: Math.min(1, intensity),
      qSource: to,
      timestamp: frame
    };
  }
}
