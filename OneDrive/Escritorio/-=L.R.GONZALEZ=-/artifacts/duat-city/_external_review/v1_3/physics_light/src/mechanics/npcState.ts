/**
 * NPC State — IA con OSIT
 * 
 * Cada NPC es un observador que no observa desde cero.
 * Observa desde estado: memoria, calibración, ruido, objetivo, gate.
 * 
 * Los NPCs usan Q-states para decidir acción.
 * R alto → ritmo inestable.
 * Phi_eff alto → ritmo estable.
 * BLOCK → advertencia baja.
 * REVIEW → motivo suspendido.
 */

import { OSITState, QState, WorldCell, AudioEvent } from '../types';
import { OSITObserver } from '../core/osit';
import { qAggregate } from '../core/qstate';

export interface NPCProfile {
  id: string;
  role: string;           // role motif
  task: string;           // task motif
  observer: OSITObserver;
  position: { x: number; y: number };
  audioState: {
    roleMotif: string;
    taskMotif: string;
    emotionalMotif: string;
    proximityGain: number;
  };
}

export class NPCStateManager {
  private npcs: Map<string, NPCProfile> = new Map();

  createNPC(id: string, role: string, x: number, y: number): NPCProfile {
    const observer = new OSITObserver(role);
    const npc: NPCProfile = {
      id,
      role,
      task: 'idle',
      observer,
      position: { x, y },
      audioState: {
        roleMotif: this.roleToMotif(role),
        taskMotif: 'idle_hum',
        emotionalMotif: 'neutral',
        proximityGain: 0.5
      }
    };
    this.npcs.set(id, npc);
    return npc;
  }

  /**
   * Actualizar NPC desde entorno (celdas vecinas)
   */
  updateNPC(id: string, nearbyCells: WorldCell[], frame: number): NPCProfile | null {
    const npc = this.npcs.get(id);
    if (!npc) return null;

    // Agregar estados Q del entorno
    const qStates = nearbyCells.map(c => c.light.qLight);
    const envQ = qAggregate(qStates);

    // Señal compuesta del entorno
    const signal = this.computeEnvironmentalSignal(nearbyCells);
    const noise = this.computeEnvironmentalNoise(nearbyCells);

    // Observar
    const state = npc.observer.observe(signal, 'environment', noise, frame);

    // Audio state desde OSIT
    npc.audioState.emotionalMotif = this.ositToEmotionalMotif(state);
    npc.audioState.taskMotif = this.taskToMotif(npc.task, state);

    // R high → unstable rhythm
    // Phi_eff high → stable rhythm
    const metrics = this.computeNPCMetrics(npc, nearbyCells);
    if (metrics.R > 0.5) {
      npc.audioState.emotionalMotif = 'unstable';
    } else if (metrics.Phi_eff > 0.7) {
      npc.audioState.emotionalMotif = 'stable';
    }

    return npc;
  }

  private computeEnvironmentalSignal(cells: WorldCell[]): number {
    let sum = 0;
    for (const c of cells) {
      sum += c.light.receivedLux + c.physics.pressure * 0.1;
    }
    return cells.length > 0 ? sum / cells.length : 0;
  }

  private computeEnvironmentalNoise(cells: WorldCell[]): number {
    let variance = 0;
    const avg = this.computeEnvironmentalSignal(cells);
    for (const c of cells) {
      const v = c.light.receivedLux + c.physics.pressure * 0.1;
      variance += (v - avg) ** 2;
    }
    return cells.length > 0 ? Math.min(1, variance / cells.length) : 0.1;
  }

  private computeNPCMetrics(npc: NPCProfile, cells: WorldCell[]) {
    const state = npc.observer.getState();
    const R = state.gate === 'BLOCK' ? 0.8 : state.gate === 'REVIEW' ? 0.4 : 0.1;
    const mem = state.memory;
    const Phi_eff = mem[3] / (Math.abs(mem[0]) + 0.001);
    return { R, Phi_eff: Math.min(1, Phi_eff) };
  }

  private roleToMotif(role: string): string {
    const map: Record<string, string> = {
      'archivist': 'archive_drone',
      'guard': 'forge_pulse',
      'merchant': 'market_chatter',
      'gardener': 'garden_shimmer',
      'explorer': 'ruin_echo'
    };
    return map[role] || 'neutral_hum';
  }

  private taskToMotif(task: string, state: OSITState): string {
    if (state.gate === 'BLOCK') return 'warning_low';
    if (state.gate === 'REVIEW') return 'suspended_motif';
    const map: Record<string, string> = {
      'idle': 'idle_hum',
      'patrol': 'footstep_rhythm',
      'trade': 'market_pulse',
      'repair': 'forge_tick',
      'research': 'archive_resonance'
    };
    return map[task] || 'neutral';
  }

  private ositToEmotionalMotif(state: OSITState): string {
    if (state.state === '00') return 'calm';
    if (state.state === '01') return 'curious';
    if (state.state === '10') return 'focused';
    if (state.state === '11') return 'alert';
    return 'neutral';
  }

  getNPC(id: string): NPCProfile | undefined { return this.npcs.get(id); }
  getAllNPCs(): NPCProfile[] { return Array.from(this.npcs.values()); }
}
