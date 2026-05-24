/**
 * Cell State — Conway-Material States
 * 
 * Cada celda tiene estado físico codificado en bits.
 * Transiciones son reglas locales tipo Conway.
 * 
 * Materiales como personajes:
 * - WATER: fluye, olvida (difumina estado anterior)
 * - FIRE: insiste (propagación con memoria corta)
 * - METAL: resiste hasta J_c, luego cede
 * - SMOKE: miente (oculta sin borrar)
 * - GLASS: refracta/distorsiona
 */

import { WorldCell, MaterialType, PhysicsState, OSITState } from '../types';
import { OSITObserver } from '../core/osit';

export interface MaterialRule {
  type: MaterialType;
  // Reglas Conway-like
  minNeighbors: number;      // mínimo vecinos para sobrevivir
  maxNeighbors: number;      // máximo vecinos antes de transición
  transitionTo?: MaterialType; // a qué transicionar
  probability: number;       // probabilidad de transición 0-1
  // Propiedades físicas
  density: number;
  conductivity: number;      // transmisión de calor/energía
  viscosity: number;         // para fluidos
}

export const MaterialRules: Record<MaterialType, MaterialRule> = {
  VOID:     { type: 'VOID',     minNeighbors: 0, maxNeighbors: 0, probability: 0, density: 0,    conductivity: 0, viscosity: 0 },
  STONE:    { type: 'STONE',    minNeighbors: 1, maxNeighbors: 8, probability: 0, density: 2.5,  conductivity: 0.3, viscosity: 0 },
  WATER:    { type: 'WATER',    minNeighbors: 1, maxNeighbors: 6, transitionTo: 'STEAM', probability: 0.1, density: 1.0,  conductivity: 0.8, viscosity: 0.01 },
  FIRE:     { type: 'FIRE',     minNeighbors: 1, maxNeighbors: 4, transitionTo: 'SMOKE', probability: 0.3, density: 0.1,  conductivity: 1.0, viscosity: 0 },
  SMOKE:    { type: 'SMOKE',    minNeighbors: 0, maxNeighbors: 3, transitionTo: 'VOID',  probability: 0.2, density: 0.05, conductivity: 0.1, viscosity: 0.1 },
  METAL:    { type: 'METAL',    minNeighbors: 2, maxNeighbors: 8, probability: 0, density: 7.8,  conductivity: 0.9, viscosity: 0 },
  GLASS:    { type: 'GLASS',    minNeighbors: 2, maxNeighbors: 8, probability: 0, density: 2.4,  conductivity: 0.2, viscosity: 0 },
  NEON:     { type: 'NEON',     minNeighbors: 1, maxNeighbors: 6, probability: 0, density: 0.001, conductivity: 1.0, viscosity: 0 },
  STEAM:    { type: 'STEAM',    minNeighbors: 0, maxNeighbors: 4, transitionTo: 'WATER', probability: 0.15, density: 0.5, conductivity: 0.4, viscosity: 0.05 },
  ORGANIC:  { type: 'ORGANIC',  minNeighbors: 2, maxNeighbors: 7, probability: 0, density: 1.0,  conductivity: 0.5, viscosity: 0.2 }
};

export class CellStateManager {
  private cells: Map<string, WorldCell> = new Map();
  private observers: Map<string, OSITObserver> = new Map();

  getKey(x: number, y: number): string { return `${x},${y}`; }

  setCell(cell: WorldCell) {
    this.cells.set(this.getKey(cell.x, cell.y), cell);
    if (!this.observers.has(this.getKey(cell.x, cell.y))) {
      this.observers.set(this.getKey(cell.x, cell.y), new OSITObserver(cell.material));
    }
  }

  getCell(x: number, y: number): WorldCell | undefined {
    return this.cells.get(this.getKey(x, y));
  }

  getObserver(x: number, y: number): OSITObserver | undefined {
    return this.observers.get(this.getKey(x, y));
  }

  /**
   * Paso Conway-Material: aplica reglas locales a cada celda
   */
  stepConway(neighbors: WorldCell[], cell: WorldCell): MaterialType {
    const rule = MaterialRules[cell.material];
    const n = neighbors.filter(n => n.material === cell.material).length;

    // Jamming: si presión/temperatura excede umbral, transición forzada
    const pressureJam = cell.physics.pressure > 2.0;
    const tempJam = cell.physics.temperature > 200;

    if (pressureJam || tempJam) {
      if (cell.material === 'METAL' && tempJam) return 'WATER'; // fusión
      if (cell.material === 'WATER' && tempJam) return 'STEAM';
      if (cell.material === 'ORGANIC' && tempJam) return 'FIRE';
    }

    // Reglas Conway estándar
    if (n < rule.minNeighbors) {
      // Muere por aislamiento
      if (cell.material === 'FIRE') return 'SMOKE';
      if (cell.material === 'WATER') return 'VOID';
    }
    if (n > rule.maxNeighbors) {
      // Muere por sobrepoblación / transición
      if (rule.transitionTo && Math.random() < rule.probability) {
        return rule.transitionTo;
      }
    }

    // Propagación especial
    if (cell.material === 'FIRE') {
      const fuel = neighbors.find(n => n.material === 'ORGANIC' || n.material === 'WOOD');
      if (fuel) return 'FIRE'; // se propaga
    }
    if (cell.material === 'WATER') {
      const lower = neighbors.find(n => n.y > cell.y && n.material === 'VOID');
      if (lower) return 'VOID'; // flujo hacia abajo
    }

    return cell.material;
  }

  getAllCells(): WorldCell[] { return Array.from(this.cells.values()); }
  getAllObservers(): OSITObserver[] { return Array.from(this.observers.values()); }
}
