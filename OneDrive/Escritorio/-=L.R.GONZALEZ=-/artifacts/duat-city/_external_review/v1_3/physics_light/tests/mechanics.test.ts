/**
 * Tests Mechanics: NPC, Quest, GameMechanics
 */

import { NPCStateManager } from '../src/mechanics/npcState';
import { QuestEngine } from '../src/mechanics/questEngine';
import { GameMechanics } from '../src/mechanics/gameMechanics';
import { WorldCell } from '../src/types';

function makeCell(x: number, y: number, material: string, q: any): WorldCell {
  return {
    x, y, material: material as any,
    osit: { state: '10', memory: new Float32Array(4), calibration: 0.5, noise: 0.1, goal: 'survive', gate: 'APPROVE', lastUpdate: 0 },
    physics: { position: {x, y}, prevPosition: {x, y}, velocity: {x:0, y:0}, mass: 1, restitution: 0.5, friction: 0.3, solid: true, pressure: 0, temperature: 20, active: true },
    light: { emissive: 0, absorbtion: 0.3, transmission: 0.5, receivedLux: 0, qLight: q, color: {r:128,g:128,b:128} }
  };
}

describe('NPCStateManager', () => {
  test('creates NPC with role motif', () => {
    const mgr = new NPCStateManager();
    const npc = mgr.createNPC('npc1', 'archivist', 100, 100);
    expect(npc.audioState.roleMotif).toBe('archive_drone');
    expect(npc.observer.getState().goal).toBe('archivist');
  });

  test('updates NPC from environment', () => {
    const mgr = new NPCStateManager();
    mgr.createNPC('npc1', 'guard', 100, 100);
    const cells = [makeCell(100, 100, 'STONE', '11')];
    const updated = mgr.updateNPC('npc1', cells, 1);
    expect(updated).not.toBeNull();
    expect(updated!.observer.getState().lastUpdate).toBe(1);
  });
});

describe('QuestEngine', () => {
  test('detects missing signal quest', () => {
    const engine = new QuestEngine();
    const cells = [makeCell(0, 0, 'STONE', '01')];
    const quests = engine.detectQuests(cells, { R: 0.4, Phi_eff: 0.6, J_c: 0.5, regime: 'SATURADO' });
    expect(quests.some(q => q.hookType === 'MISSING_SIGNAL')).toBe(true);
  });

  test('quest progress updates', () => {
    const engine = new QuestEngine();
    const quest = engine.createQuest({
      title: 'Test',
      steps: [{ id: 's1', description: 'Test step', condition: () => true, completed: false }]
    });
    engine.activateQuest(quest.id);
    engine.updateQuests([], { R: 0.1, Phi_eff: 0.9, J_c: 0.5, regime: 'OPTIMO' });
    expect(engine.getQuest(quest.id)!.Phi_quest).toBeGreaterThan(0);
  });
});

describe('GameMechanics', () => {
  test('step returns game state', () => {
    const game = new GameMechanics({
      gridSize: 32, gridWidth: 10, gridHeight: 10,
      maxSubsteps: 4, emlThreshold: 0.5, jammingThreshold: 0.8,
      enableAudioBridge: true, enableLightBridge: true
    });
    game.addCell(makeCell(100, 100, 'STONE', '10'));
    game.addNPC('npc1', 'archivist', 100, 100);
    const state = game.step();
    expect(state.frame).toBe(1);
    expect(state.npcCount).toBe(1);
    expect(state).toHaveProperty('metrics');
  });
});
