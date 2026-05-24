/**
 * Tests Physics: SpatialHash, CellState, Verlet, PhysicsEngine
 */

import { SpatialHashFib } from '../src/physics/spatialHashFib';
import { CellStateManager, MaterialRules } from '../src/physics/cellState';
import { VerletEML } from '../src/physics/verletEML';
import { PhysicsEngine } from '../src/physics/physicsEngine';
import { WorldCell } from '../src/types';

function makeCell(x: number, y: number, material: string): WorldCell {
  return {
    x, y, material: material as any,
    osit: { state: '10', memory: new Float32Array(4), calibration: 0.5, noise: 0.1, goal: 'survive', gate: 'APPROVE', lastUpdate: 0 },
    physics: {
      position: {x, y}, prevPosition: {x, y}, velocity: {x:0, y:0},
      mass: 1, restitution: 0.5, friction: 0.3, solid: material !== 'VOID' && material !== 'WATER',
      pressure: 0, temperature: 20, active: true
    },
    light: { emissive: 0, absorbtion: 0.5, transmission: 0, receivedLux: 0, qLight: '00', color: {r:128,g:128,b:128} }
  };
}

describe('SpatialHashFib', () => {
  test('insert and query', () => {
    const hash = new SpatialHashFib(32);
    const cell = makeCell(100, 200, 'STONE');
    hash.insert(cell);
    const found = hash.query(100, 200, 50);
    expect(found.length).toBeGreaterThanOrEqual(1);
  });

  test('query radius filters correctly', () => {
    const hash = new SpatialHashFib(32);
    hash.insert(makeCell(0, 0, 'STONE'));
    hash.insert(makeCell(1000, 1000, 'STONE'));
    const found = hash.query(0, 0, 100);
    expect(found.length).toBe(1);
  });
});

describe('CellStateManager', () => {
  test('Conway water to steam on heat', () => {
    const mgr = new CellStateManager();
    const cell = makeCell(0, 0, 'WATER');
    cell.physics.temperature = 250;
    mgr.setCell(cell);
    const neighbors = [makeCell(1, 0, 'WATER'), makeCell(-1, 0, 'WATER')];
    const result = mgr.stepConway(neighbors, cell);
    expect(result).toBe('STEAM');
  });

  test('metal survives normal conditions', () => {
    const mgr = new CellStateManager();
    const cell = makeCell(0, 0, 'METAL');
    mgr.setCell(cell);
    const neighbors = [makeCell(1, 0, 'METAL'), makeCell(-1, 0, 'METAL')];
    const result = mgr.stepConway(neighbors, cell);
    expect(result).toBe('METAL');
  });
});

describe('VerletEML', () => {
  test('integrates without NaN', () => {
    const verlet = new VerletEML();
    const cell = makeCell(0, 0, 'STONE');
    const result = verlet.integrate(cell, [], 1);
    expect(Number.isFinite(result.position.x)).toBe(true);
    expect(Number.isFinite(result.position.y)).toBe(true);
  });

  test('solid cells do not move', () => {
    const verlet = new VerletEML();
    const cell = makeCell(0, 0, 'STONE');
    cell.physics.solid = true;
    const result = verlet.integrate(cell, [], 1);
    expect(result.position.x).toBe(0);
    expect(result.position.y).toBe(0);
  });
});

describe('PhysicsEngine', () => {
  test('step returns metrics', () => {
    const engine = new PhysicsEngine({
      gridSize: 32, gridWidth: 20, gridHeight: 20,
      maxSubsteps: 4, emlThreshold: 0.5, jammingThreshold: 0.8,
      enableAudioBridge: false, enableLightBridge: false
    });
    engine.addCell(makeCell(100, 100, 'STONE'));
    const metrics = engine.step();
    expect(metrics).toHaveProperty('R_physics');
    expect(metrics).toHaveProperty('Phi_physics');
    expect(metrics).toHaveProperty('regime');
  });
});
