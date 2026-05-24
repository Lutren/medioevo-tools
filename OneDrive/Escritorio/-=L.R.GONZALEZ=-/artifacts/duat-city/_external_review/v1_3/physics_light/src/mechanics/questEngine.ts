/**
 * Quest Engine — Misiones como Resolución de Residuo
 * 
 * Cada quest tiene R_quest que mide lo que falta por resolver.
 * Phi_quest mide eficiencia de progreso.
 * 
 * Quest hooks desde audio/luz/física:
 * - "follow missing signal" → Q=01 detectado
 * - "repair silent lumen vial" → emissive=0 en objeto que debería brillar
 * - "decode forbidden archive resonance" → audio evento archive + R alto
 * - "stabilize forge rhythm" → physics pressure irregular
 * - "calm market noise panic" → NPCs en gate BLOCK
 */

import { QState, WorldCell, SystemMetrics } from '../types';

export interface Quest {
  id: string;
  title: string;
  description: string;
  hookType: 'MISSING_SIGNAL' | 'SILENT_LUMEN' | 'ARCHIVE_RESONANCE' | 
            'FORGE_RHYTHM' | 'MARKET_PANIC' | 'CUSTOM';
  targetQ: QState;
  targetMaterial?: string;
  targetNPCRole?: string;
  R_quest: number;         // residuo de la quest 0-1
  Phi_quest: number;       // eficiencia de progreso
  completed: boolean;
  steps: QuestStep[];
}

export interface QuestStep {
  id: string;
  description: string;
  condition: (world: WorldCell[], metrics: SystemMetrics) => boolean;
  completed: boolean;
}

export class QuestEngine {
  private quests: Map<string, Quest> = new Map();
  private activeQuests: Set<string> = new Set();

  createQuest(template: Partial<Quest>): Quest {
    const quest: Quest = {
      id: template.id || `quest_${Date.now()}`,
      title: template.title || 'Unnamed Quest',
      description: template.description || '',
      hookType: template.hookType || 'CUSTOM',
      targetQ: template.targetQ || '10',
      R_quest: 1.0,
      Phi_quest: 0.0,
      completed: false,
      steps: template.steps || []
    };
    this.quests.set(quest.id, quest);
    return quest;
  }

  /**
   * Detectar quests automáticamente desde anomalías del mundo
   */
  detectQuests(cells: WorldCell[], metrics: SystemMetrics): Quest[] {
    const detected: Quest[] = [];

    // 1. Missing signal: celdas Q=01 sin explicación
    const missingSignals = cells.filter(c => c.light.qLight === '01' && c.light.emissive === 0);
    if (missingSignals.length > 0 && metrics.R > 0.3) {
      detected.push(this.createQuest({
        title: 'Follow the Missing Signal',
        description: `Anomaly detected at ${missingSignals[0].x},${missingSignals[0].y}`,
        hookType: 'MISSING_SIGNAL',
        targetQ: '10',
        steps: [
          { id: 'locate', description: 'Locate source of anomaly', condition: () => false, completed: false },
          { id: 'stabilize', description: 'Stabilize signal to Q=10', condition: (w) => 
            w.some(c => c.light.qLight === '10' && Math.hypot(c.x - missingSignals[0].x, c.y - missingSignals[0].y) < 50),
          completed: false }
        ]
      }));
    }

    // 2. Silent lumen: objeto emissive que no emite
    const silentLumens = cells.filter(c => 
      c.material === 'NEON' && c.light.emissive < 0.1 && c.physics.temperature < 50
    );
    if (silentLumens.length > 0) {
      detected.push(this.createQuest({
        title: 'Repair the Silent Lumen Vial',
        description: 'A light source has gone dark. Restore its emissive state.',
        hookType: 'SILENT_LUMEN',
        targetQ: '11',
        targetMaterial: 'NEON',
        steps: [
          { id: 'repair', description: 'Restore emissive > 0.5', condition: (w) => 
            w.some(c => c.material === 'NEON' && c.light.emissive > 0.5),
          completed: false }
        ]
      }));
    }

    // 3. Forge rhythm: presión irregular en celdas METAL
    const forgeCells = cells.filter(c => c.material === 'METAL' && Math.abs(c.physics.pressure) > 1.5);
    if (forgeCells.length > 3) {
      detected.push(this.createQuest({
        title: 'Stabilize the Forge Rhythm',
        description: 'Pressure irregularities detected in metal cells.',
        hookType: 'FORGE_RHYTHM',
        targetQ: '10',
        targetMaterial: 'METAL',
        steps: [
          { id: 'stabilize', description: 'Reduce pressure variance', condition: (w) => 
            w.filter(c => c.material === 'METAL').every(c => Math.abs(c.physics.pressure) < 0.5),
          completed: false }
        ]
      }));
    }

    return detected;
  }

  /**
   * Actualizar progreso de quests activas
   */
  updateQuests(cells: WorldCell[], metrics: SystemMetrics): void {
    for (const id of this.activeQuests) {
      const quest = this.quests.get(id);
      if (!quest || quest.completed) continue;

      let completedSteps = 0;
      for (const step of quest.steps) {
        if (!step.completed && step.condition(cells, metrics)) {
          step.completed = true;
        }
        if (step.completed) completedSteps++;
      }

      quest.Phi_quest = completedSteps / quest.steps.length;
      quest.R_quest = 1 - quest.Phi_quest;
      quest.completed = quest.R_quest < 0.1;
    }
  }

  activateQuest(id: string) { this.activeQuests.add(id); }
  getQuest(id: string): Quest | undefined { return this.quests.get(id); }
  getActiveQuests(): Quest[] {
    return Array.from(this.activeQuests).map(id => this.quests.get(id)).filter(Boolean) as Quest[];
  }
}
