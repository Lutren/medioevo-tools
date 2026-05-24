/**
 * Verlet + EML Substepping
 * 
 * Verlet como memoria: la posición anterior es memoria.
 * La física es nostalgia con fricción.
 * 
 * EML decide subpasos: más pasos donde hay tensión,
 * menos donde hay calma.
 */

import { Vec2, PhysicsState, WorldCell } from '../types';
import { emlSubsteps } from '../core/eml';

export interface VerletConfig {
  dt: number;           // paso de tiempo base
  gravity: Vec2;
  damping: number;      // fricción global
}

export class VerletEML {
  private config: VerletConfig;

  constructor(config: VerletConfig = { dt: 1/60, gravity: {x:0, y:9.8}, damping: 0.99 }) {
    this.config = config;
  }

  /**
   * Integra una celda con substepping EML
   */
  integrate(cell: WorldCell, neighborCells: WorldCell[], frame: number): PhysicsState {
    const p = cell.physics;
    if (!p.active || p.solid) return p; // objetos estáticos no se integran

    // Calcular energía local y residuo para EML
    const energy = this.computeLocalEnergy(cell, neighborCells);
    const residue = this.computeLocalResidue(cell, neighborCells);

    // EML decide subpasos
    const substeps = emlSubsteps(energy, residue, 8);
    const subDt = this.config.dt / substeps;

    let pos = { ...p.position };
    let prev = { ...p.prevPosition };

    for (let step = 0; step < substeps; step++) {
      // Verlet: x(t+dt) = 2x(t) - x(t-dt) + a*dt²
      const acc = {
        x: this.config.gravity.x + this.computeForcesX(cell, neighborCells),
        y: this.config.gravity.y + this.computeForcesY(cell, neighborCells)
      };

      const nextX = 2 * pos.x - prev.x + acc.x * subDt * subDt;
      const nextY = 2 * pos.y - prev.y + acc.y * subDt * subDt;

      prev = { ...pos };
      pos = { x: nextX, y: nextY };

      // Damping por material
      const materialDamping = this.getMaterialDamping(cell);
      pos.x += (pos.x - prev.x) * (materialDamping - 1);
      pos.y += (pos.y - prev.y) * (materialDamping - 1);
    }

    return {
      ...p,
      prevPosition: { ...p.position },
      position: pos,
      velocity: {
        x: (pos.x - p.position.x) / this.config.dt,
        y: (pos.y - p.position.y) / this.config.dt
      }
    };
  }

  private computeLocalEnergy(cell: WorldCell, neighbors: WorldCell[]): number {
    let e = 0;
    e += Math.hypot(cell.physics.velocity.x, cell.physics.velocity.y);
    e += Math.abs(cell.physics.pressure);
    e += Math.abs(cell.physics.temperature) / 100;
    for (const n of neighbors) {
      const dist = Math.hypot(n.x - cell.x, n.y - cell.y);
      if (dist > 0) e += n.physics.mass / dist;
    }
    return Math.min(1, e / 10);
  }

  private computeLocalResidue(cell: WorldCell, neighbors: WorldCell[]): number {
    let r = 0;
    // Residuo por contradicción de vecinos (materiales incompatibles)
    for (const n of neighbors) {
      if (n.material !== cell.material && n.material !== 'VOID') {
        r += 0.1;
      }
    }
    // Residuo por inestabilidad numérica
    if (cell.physics.velocity.x > 100 || cell.physics.velocity.y > 100) r += 0.3;
    return Math.min(1, r);
  }

  private computeForcesX(cell: WorldCell, neighbors: WorldCell[]): number {
    let fx = 0;
    for (const n of neighbors) {
      const dx = n.x - cell.x;
      const dist = Math.hypot(dx, n.y - cell.y);
      if (dist > 0 && dist < 2) {
        // Repulsión suave
        fx -= (dx / dist) * 0.5;
      }
    }
    return fx;
  }

  private computeForcesY(cell: WorldCell, neighbors: WorldCell[]): number {
    let fy = 0;
    for (const n of neighbors) {
      const dy = n.y - cell.y;
      const dist = Math.hypot(n.x - cell.x, dy);
      if (dist > 0 && dist < 2) {
        fy -= (dy / dist) * 0.5;
      }
    }
    return fy;
  }

  private getMaterialDamping(cell: WorldCell): number {
    const map: Record<string, number> = {
      'WATER': 0.95, 'SMOKE': 0.98, 'FIRE': 0.9,
      'METAL': 0.999, 'STONE': 0.99, 'ORGANIC': 0.97
    };
    return map[cell.material] || this.config.damping;
  }
}
