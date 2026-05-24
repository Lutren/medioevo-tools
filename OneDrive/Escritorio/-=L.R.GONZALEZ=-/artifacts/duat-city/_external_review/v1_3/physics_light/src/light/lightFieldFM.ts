/**
 * Light Field FM — Propagación Lumínica con Fibonacci-Möbius
 * 
 * La luz no se "difumina" con inversa cuadrada.
 * Se AGREGA con Möbius, como si cada pared fuera un divisor
 * que modula la señal.
 * 
 * Materiales que cantan con luz:
 * - cristal: refracta intención (Q=10 → Q=01+Q=11)
 * - humo: low-pass espacial
 * - agua: desplazamiento de índice
 * - metal: reflejo modal (resonancia)
 */

import { WorldCell, LightState, QState, RGB } from '../types';
import { fibMobConvolution, fibMobWeight } from '../core/fibmob';
import { qTransition, qAggregate } from '../core/qstate';
import { emlLOD } from '../core/eml';

export interface LightFieldConfig {
  maxPropagationSteps: number;
  attenuationBase: number;
  enableQState: boolean;
}

export class LightFieldFM {
  private config: LightFieldConfig;
  private luxBuffer: Float32Array;
  private qBuffer: QState[];
  private width: number;
  private height: number;
  private gridSize: number;

  constructor(width: number, height: number, gridSize: number, config: LightFieldConfig) {
    this.width = width;
    this.height = height;
    this.gridSize = gridSize;
    this.config = config;
    this.luxBuffer = new Float32Array(width * height);
    this.qBuffer = new Array(width * height).fill('00');
  }

  private idx(x: number, y: number): number {
    return y * this.width + x;
  }

  /**
   * Propagación principal: campo lumínico con FM
   */
  propagate(cells: WorldCell[]): void {
    // Reset buffer
    this.luxBuffer.fill(0);
    this.qBuffer.fill('00');

    // Paso 1: Emisión directa
    for (const cell of cells) {
      const gx = Math.floor(cell.x / this.gridSize);
      const gy = Math.floor(cell.y / this.gridSize);
      if (gx < 0 || gx >= this.width || gy < 0 || gy >= this.height) continue;

      const i = this.idx(gx, gy);
      if (cell.light.emissive > 0) {
        this.luxBuffer[i] += cell.light.emissive;
        this.qBuffer[i] = cell.light.qLight;
      }
    }

    // Paso 2: Propagación FM por vecindario
    const newLux = new Float32Array(this.luxBuffer);
    const newQ = [...this.qBuffer];

    for (let step = 0; step < this.config.maxPropagationSteps; step++) {
      const tempLux = new Float32Array(newLux);

      for (let y = 1; y < this.height - 1; y++) {
        for (let x = 1; x < this.width - 1; x++) {
          const cell = cells.find(c => 
            Math.floor(c.x / this.gridSize) === x && 
            Math.floor(c.y / this.gridSize) === y
          );

          if (!cell) continue;

          // EML LOD: decidir si propagar a resolución completa
          const lod = emlLOD(cell.light.emissive, cell.osit.gate === 'BLOCK' ? 0.8 : 0.2, 8);
          if (step > 0 && lod > step * 2) continue;

          // Propagación con pesos FM
          let sum = 0;
          let weightSum = 0;
          const qNeighbors: QState[] = [];

          for (let dy = -1; dy <= 1; dy++) {
            for (let dx = -1; dx <= 1; dx++) {
              if (dx === 0 && dy === 0) continue;
              const nx = x + dx;
              const ny = y + dy;
              const ni = this.idx(nx, ny);
              const d = Math.hypot(dx, dy);
              const w = fibMobWeight(d, 2) * this.getTransmission(cell);

              sum += tempLux[ni] * w;
              weightSum += w;
              qNeighbors.push(this.qBuffer[ni]);
            }
          }

          const propagated = weightSum > 0 ? sum / weightSum : 0;
          const attenuated = propagated * (1 - cell.light.absorbtion) * this.config.attenuationBase;

          if (attenuated > newLux[this.idx(x, y)]) {
            newLux[this.idx(x, y)] = attenuated;
            // Q-state por transición con vecinos
            if (this.config.enableQState) {
              newQ[this.idx(x, y)] = qAggregate([this.qBuffer[this.idx(x, y)], ...qNeighbors]);
            }
          }
        }
      }

      newLux.set(tempLux);
    }

    this.luxBuffer = newLux;
    this.qBuffer = newQ;
  }

  /**
   * Aplicar resultados del buffer a las celdas
   */
  applyToCells(cells: WorldCell[]): void {
    for (const cell of cells) {
      const gx = Math.floor(cell.x / this.gridSize);
      const gy = Math.floor(cell.y / this.gridSize);
      if (gx < 0 || gx >= this.width || gy < 0 || gy >= this.height) continue;

      const i = this.idx(gx, gy);
      cell.light.receivedLux = this.luxBuffer[i];
      if (this.config.enableQState) {
        cell.light.qLight = this.qBuffer[i];
      }
    }
  }

  private getTransmission(cell: WorldCell): number {
    const map: Record<string, number> = {
      'VOID': 1.0, 'GLASS': 0.9, 'WATER': 0.7,
      'SMOKE': 0.3, 'STONE': 0.0, 'METAL': 0.0,
      'FIRE': 0.5, 'NEON': 1.0, 'ORGANIC': 0.1
    };
    return cell ? (map[cell.material] || 0) * cell.light.transmission : 0;
  }

  getLuxAt(x: number, y: number): number {
    const gx = Math.floor(x / this.gridSize);
    const gy = Math.floor(y / this.gridSize);
    if (gx < 0 || gx >= this.width || gy < 0 || gy >= this.height) return 0;
    return this.luxBuffer[this.idx(gx, gy)];
  }

  getQAt(x: number, y: number): QState {
    const gx = Math.floor(x / this.gridSize);
    const gy = Math.floor(y / this.gridSize);
    if (gx < 0 || gx >= this.width || gy < 0 || gy >= this.height) return '00';
    return this.qBuffer[this.idx(gx, gy)];
  }
}
