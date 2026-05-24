/**
 * Physics Audio Bridge — Física genera Audio
 * 
 * Colisiones, transiciones de material, y cambios de presión
 * generan eventos sonoros automáticamente.
 */

import { WorldCell, AudioEvent } from '../types';

export class PhysicsAudioBridge {
  private lastPressures: Map<string, number> = new Map();
  private lastMaterials: Map<string, string> = new Map();

  process(cells: WorldCell[], frame: number): AudioEvent[] {
    const events: AudioEvent[] = [];

    for (const cell of cells) {
      const key = `${cell.x},${cell.y}`;
      const lastP = this.lastPressures.get(key) || 0;
      const lastM = this.lastMaterials.get(key) || cell.material;

      // Evento por cambio de material
      if (lastM !== cell.material) {
        const event = this.materialTransitionToAudio(lastM, cell.material, cell, frame);
        if (event) {
          events.push(event);
          if (!cell.audio) cell.audio = { eventQueue: [], materialResonance: 0 };
          cell.audio.eventQueue.push(event);
        }
      }

      // Evento por cambio brusco de presión
      const deltaP = Math.abs(cell.physics.pressure - lastP);
      if (deltaP > 1.0) {
        const event: AudioEvent = {
          type: 'pressure_burst',
          intensity: Math.min(1, deltaP / 5),
          qSource: cell.light.qLight,
          timestamp: frame
        };
        events.push(event);
        if (!cell.audio) cell.audio = { eventQueue: [], materialResonance: 0 };
        cell.audio.eventQueue.push(event);
      }

      // Evento por colisión (velocity spike)
      const v = Math.hypot(cell.physics.velocity.x, cell.physics.velocity.y);
      if (v > 50 && cell.physics.solid) {
        const event: AudioEvent = {
          type: 'collision_impact',
          intensity: Math.min(1, v / 200),
          qSource: cell.light.qLight,
          timestamp: frame
        };
        events.push(event);
        if (!cell.audio) cell.audio = { eventQueue: [], materialResonance: 0 };
        cell.audio.eventQueue.push(event);
      }

      this.lastPressures.set(key, cell.physics.pressure);
      this.lastMaterials.set(key, cell.material);
    }

    return events;
  }

  private materialTransitionToAudio(
    from: string, to: string, cell: WorldCell, frame: number
  ): AudioEvent | null {
    const map: Record<string, string> = {
      'WATER->STEAM': 'water_boil',
      'STEAM->WATER': 'steam_condense',
      'ICE->WATER': 'ice_melt',
      'ORGANIC->FIRE': 'combustion',
      'METAL->WATER': 'metal_melt',
      'STONE->LAVA': 'stone_melt'
    };
    const type = map[`${from}->${to}`];
    if (!type) return null;

    return {
      type,
      intensity: 0.7,
      qSource: cell.light.qLight,
      timestamp: frame
    };
  }
}
