/**
 * Game Mechanics — Sistema de Mecánicas Unificado
 * 
 * Conecta física, luz, audio y NPCs bajo OSIT.
 * 
 * Reglas del mundo como leyes narrativas:
 * - Dos cuerpos de obsidiana que chocan no rebotan; reconocen parentesco.
 * - El agua no fluye; olvida.
 * - El fuego no quema; insiste.
 * - El metal resiste hasta J_c, luego cede de golpe.
 */

import { WorldCell, EngineConfig, SystemMetrics } from '../types';
import { PhysicsEngine } from '../physics/physicsEngine';
import { LightFieldFM } from '../light/lightFieldFM';
import { NPCStateManager } from './npcState';
import { QuestEngine } from './questEngine';
import { LightAudioBridge } from '../light/lightBridge';
import { computeSystemMetrics } from '../core/osit';

export interface GameState {
  frame: number;
  metrics: SystemMetrics;
  physicsMetrics: any;
  activeQuests: any[];
  npcCount: number;
  lightEvents: number;
}

export class GameMechanics {
  private config: EngineConfig;
  private physics: PhysicsEngine;
  private lightField: LightFieldFM;
  private npcManager: NPCStateManager;
  private questEngine: QuestEngine;
  private lightAudioBridge: LightAudioBridge;
  private frame: number = 0;

  constructor(config: EngineConfig) {
    this.config = config;
    this.physics = new PhysicsEngine(config);
    this.lightField = new LightFieldFM(
      config.gridWidth, config.gridHeight, config.gridSize,
      { maxPropagationSteps: 4, attenuationBase: 0.8, enableQState: true }
    );
    this.npcManager = new NPCStateManager();
    this.questEngine = new QuestEngine();
    this.lightAudioBridge = new LightAudioBridge();
  }

  addCell(cell: WorldCell) {
    this.physics.addCell(cell);
  }

  addNPC(id: string, role: string, x: number, y: number) {
    return this.npcManager.createNPC(id, role, x, y);
  }

  /**
   * Paso completo del mundo
   */
  step(): GameState {
    this.frame++;

    // 1. Física
    const physMetrics = this.physics.step();

    // 2. Luz
    const allCells = this.physics.getCellManager().getAllCells();
    this.lightField.propagate(allCells);
    this.lightField.applyToCells(allCells);

    // 3. NPCs
    for (const npc of this.npcManager.getAllNPCs()) {
      const nearby = this.physics.getSpatialHash().query(npc.position.x, npc.position.y, 100);
      this.npcManager.updateNPC(npc.id, nearby, this.frame);
    }

    // 4. Bridge Luz → Audio
    const lightEvents = this.lightAudioBridge.process(allCells, this.frame);

    // 5. Quests
    const observers = this.physics.getCellManager().getAllObservers();
    const sysMetrics = computeSystemMetrics(observers, this.config.jammingThreshold);
    const detected = this.questEngine.detectQuests(allCells, sysMetrics);
    for (const q of detected) {
      this.questEngine.activateQuest(q.id);
    }
    this.questEngine.updateQuests(allCells, sysMetrics);

    return {
      frame: this.frame,
      metrics: sysMetrics,
      physicsMetrics: physMetrics,
      activeQuests: this.questEngine.getActiveQuests(),
      npcCount: this.npcManager.getAllNPCs().length,
      lightEvents: lightEvents.length
    };
  }

  getPhysics(): PhysicsEngine { return this.physics; }
  getLightField(): LightFieldFM { return this.lightField; }
  getNPCManager(): NPCStateManager { return this.npcManager; }
  getQuestEngine(): QuestEngine { return this.questEngine; }
}
