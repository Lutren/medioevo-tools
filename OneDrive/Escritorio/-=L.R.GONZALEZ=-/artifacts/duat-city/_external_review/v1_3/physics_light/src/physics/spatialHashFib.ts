/**
 * Spatial Hash con Fibonacci-Möbius
 * 
 * Distribución de Fibonacci para indexación uniforme.
 * Reduce colisiones de hash en clusters.
 */

import { WorldCell, Vec2 } from '../types';
import { fibMobSpatialHash } from '../core/fibmob';

export class SpatialHashFib {
  private gridSize: number;
  private buckets: Map<number, WorldCell[]> = new Map();

  constructor(gridSize: number = 32) {
    this.gridSize = gridSize;
  }

  clear() {
    this.buckets.clear();
  }

  insert(cell: WorldCell) {
    const hash = fibMobSpatialHash(cell.x, cell.y, this.gridSize);
    if (!this.buckets.has(hash)) {
      this.buckets.set(hash, []);
    }
    this.buckets.get(hash)!.push(cell);
  }

  query(x: number, y: number, radius: number = 1): WorldCell[] {
    const results: WorldCell[] = [];
    const rCells = Math.ceil(radius / this.gridSize);

    for (let dx = -rCells; dx <= rCells; dx++) {
      for (let dy = -rCells; dy <= rCells; dy++) {
        const hash = fibMobSpatialHash(x + dx * this.gridSize, y + dy * this.gridSize, this.gridSize);
        const bucket = this.buckets.get(hash);
        if (bucket) {
          for (const cell of bucket) {
            const dist = Math.hypot(cell.x - x, cell.y - y);
            if (dist <= radius) results.push(cell);
          }
        }
      }
    }
    return results;
  }

  queryNeighbors(cell: WorldCell, radius: number = 1): WorldCell[] {
    return this.query(cell.x, cell.y, radius).filter(c => c !== cell);
  }

  getGridSize(): number { return this.gridSize; }
}
