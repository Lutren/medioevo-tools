/**
 * Physics Engine — CPU-First, Residue-First
 * 
 * No simula todo. Propaga deltas de estado.
 * Solo recalcula celdas donde ΔState > 0 o vecinos cambiaron.
 */

import { WorldCell, EngineConfig, SystemMetrics } from '../types';
import { SpatialHashFib } from './spatialHashFib';
import { CellStateManager, MaterialRules } from './cellState';
import { VerletEML } from './verletEML';
import { computeSystemMetrics } from '../core/osit';
import { fibMobLOD } from '../core/fibmob';

export interface PhysicsMetrics {
  activeCells: number;
  totalCells: number;
  collisions: number;
  transitions: number;
  R_physics: number;
  Phi_physics: number;
  regime: SystemMetrics['regime'];
}

export class PhysicsEngine {
  private config: EngineConfig;
  private spatialHash: SpatialHashFib;
  private cellManager: CellStateManager;
  private verlet: VerletEML;
  private metrics: PhysicsMetrics;
  private dirtyCells: Set<string> = new Set();
  private frame: number = 0;

  constructor(config: EngineConfig) {
    this.config = config;
    this.spatialHash = new SpatialHashFib(config.gridSize);
    this.cellManager = new CellStateManager();
    this.verlet = new VerletEML();
    this.metrics = {
      activeCells: 0, totalCells: 0, collisions: 0, transitions: 0,
      R_physics: 0, Phi_physics: 0, regime: 'OPTIMO'
    };
  }

  addCell(cell: WorldCell) {
    this.cellManager.setCell(cell);
    this.spatialHash.insert(cell);
    this.dirtyCells.add(this.cellManager.getKey(cell.x, cell.y));
  }

  /**
   * Paso principal: residue-first
   */
  step(): PhysicsMetrics {
    this.frame++;
    this.spatialHash.clear();

    // Reconstruir spatial hash
    const allCells = this.cellManager.getAllCells();
    for (const cell of allCells) {
      this.spatialHash.insert(cell);
    }

    // Determinar celdas activas (dirty + vecinos de dirty)
    const activeSet = new Set<string>();
    for (const key of this.dirtyCells) {
      activeSet.add(key);
      const [x, y] = key.split(',').map(Number);
      const cell = this.cellManager.getCell(x, y);
      if (cell) {
        const neighbors = this.spatialHash.queryNeighbors(cell, this.config.gridSize * 2);
        for (const n of neighbors) {
          activeSet.add(this.cellManager.getKey(n.x, n.y));
        }
      }
    }

    // Procesar celdas activas
    const newDirty = new Set<string>();
    let transitions = 0;
    let collisions = 0;

    for (const key of activeSet) {
      const [x, y] = key.split(',').map(Number);
      const cell = this.cellManager.getCell(x, y);
      if (!cell) continue;

      // LOD físico por distancia al centro de atención (cámara/player)
      const lod = fibMobLOD(this.distanceToFocus(cell), this.config.gridSize * 4);
      if (lod > 1 && Math.random() > 1/lod) continue; // skip por LOD

      // Vecinos
      const neighbors = this.spatialHash.queryNeighbors(cell, this.config.gridSize * 1.5);

      // 1. Conway-Material step
      const newMaterial = this.cellManager.stepConway(neighbors, cell);
      if (newMaterial !== cell.material) {
        cell.material = newMaterial;
        cell.physics.mass = MaterialRules[newMaterial].density;
        transitions++;
        newDirty.add(key);
        for (const n of neighbors) {
          newDirty.add(this.cellManager.getKey(n.x, n.y));
        }
      }

      // 2. Verlet integration
      const newPhysics = this.verlet.integrate(cell, neighbors, this.frame);
      if (this.physicsChanged(cell.physics, newPhysics)) {
        cell.physics = newPhysics;
        newDirty.add(key);
      }

      // 3. Colisiones simples
      for (const n of neighbors) {
        if (n.physics.solid && cell.physics.solid) {
          const dist = Math.hypot(n.x - cell.x, n.y - cell.y);
          if (dist < this.config.gridSize) {
            collisions++;
            // Separación simple
            const overlap = this.config.gridSize - dist;
            const nx = (cell.x - n.x) / dist;
            const ny = (cell.y - n.y) / dist;
            cell.physics.position.x += nx * overlap * 0.5;
            cell.physics.position.y += ny * overlap * 0.5;
            newDirty.add(key);
            newDirty.add(this.cellManager.getKey(n.x, n.y));
          }
        }
      }

      // 4. OSIT observe
      const observer = this.cellManager.getObserver(x, y);
      if (observer) {
        const signal = cell.physics.pressure + cell.physics.temperature / 100;
        observer.observe(signal, 'physics', cell.physics.velocity.x / 10, this.frame);
      }
    }

    this.dirtyCells = newDirty;

    // Métricas
    const observers = this.cellManager.getAllObservers();
    const sysMetrics = computeSystemMetrics(observers, this.config.jammingThreshold);

    this.metrics = {
      activeCells: activeSet.size,
      totalCells: allCells.length,
      collisions,
      transitions,
      R_physics: sysMetrics.R,
      Phi_physics: sysMetrics.Phi_eff,
      regime: sysMetrics.regime
    };

    return this.metrics;
  }

  private distanceToFocus(cell: WorldCell): number {
    // Asumimos foco en centro del grid por ahora
    const cx = (this.config.gridWidth * this.config.gridSize) / 2;
    const cy = (this.config.gridHeight * this.config.gridSize) / 2;
    return Math.hypot(cell.x - cx, cell.y - cy);
  }

  private physicsChanged(a: any, b: any): boolean {
    const eps = 0.001;
    return Math.abs(a.position.x - b.position.x) > eps ||
           Math.abs(a.position.y - b.position.y) > eps ||
           Math.abs(a.velocity.x - b.velocity.x) > eps;
  }

  getMetrics(): PhysicsMetrics { return this.metrics; }
  getCellManager(): CellStateManager { return this.cellManager; }
  getSpatialHash(): SpatialHashFib { return this.spatialHash; }
}
