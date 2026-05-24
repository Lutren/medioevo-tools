/**
 * Tests Core: FibMob, EML, OSIT, Q-State
 */

import { fibMobWeight, fibMobConvolution, fibMobLOD, fibMobSpatialHash } from '../src/core/fibmob';
import { emlEvaluate, emlSubsteps, emlLOD } from '../src/core/eml';
import { OSITObserver, computeSystemMetrics } from '../src/core/osit';
import { qTransition, qAggregate, QStateMap } from '../src/core/qstate';

describe('FibMob Core', () => {
  test('fibMobWeight decreases with distance', () => {
    const w1 = fibMobWeight(1);
    const w2 = fibMobWeight(2);
    expect(w1).toBeGreaterThan(w2);
    expect(w1).toBeLessThanOrEqual(1);
    expect(w2).toBeGreaterThanOrEqual(0);
  });

  test('fibMobConvolution produces finite result', () => {
    const values = new Float32Array([1, 2, 3, 4, 5]);
    const result = fibMobConvolution(values, 2, 2);
    expect(Number.isFinite(result)).toBe(true);
    expect(result).toBeGreaterThan(0);
  });

  test('fibMobLOD increases with distance', () => {
    const lod1 = fibMobLOD(10);
    const lod2 = fibMobLOD(200);
    expect(lod2).toBeGreaterThanOrEqual(lod1);
  });

  test('fibMobSpatialHash is deterministic', () => {
    const h1 = fibMobSpatialHash(100, 200, 32);
    const h2 = fibMobSpatialHash(100, 200, 32);
    expect(h1).toBe(h2);
  });
});

describe('EML Core', () => {
  test('emlEvaluate returns valid mode', () => {
    const r = emlEvaluate(0.5, 0.2);
    expect(['EXPAND', 'COMPRESS', 'HOLD']).toContain(r.mode);
    expect(Number.isFinite(r.value)).toBe(true);
    expect(Number.isFinite(r.tension)).toBe(true);
  });

  test('emlSubsteps returns within bounds', () => {
    const steps = emlSubsteps(0.8, 0.1, 8);
    expect(steps).toBeGreaterThanOrEqual(1);
    expect(steps).toBeLessThanOrEqual(8);
  });

  test('emlLOD respects max', () => {
    const lod = emlLOD(0.9, 0.1, 16);
    expect(lod).toBeGreaterThanOrEqual(1);
    expect(lod).toBeLessThanOrEqual(16);
  });
});

describe('OSIT Core', () => {
  test('observer starts with state 10', () => {
    const obs = new OSITObserver();
    expect(obs.getState().state).toBe('10');
  });

  test('observer updates state on observe', () => {
    const obs = new OSITObserver();
    obs.observe(0.8, 'test', 0.1, 1);
    const state = obs.getState();
    expect(state.lastUpdate).toBe(1);
    expect(state.memory[3]).not.toBe(0);
  });

  test('system metrics computed', () => {
    const obs1 = new OSITObserver();
    const obs2 = new OSITObserver();
    obs1.observe(0.5, 'a', 0.1, 1);
    obs2.observe(-0.8, 'b', 0.2, 1);
    const m = computeSystemMetrics([obs1, obs2], 0.5);
    expect(m.R).toBeGreaterThanOrEqual(0);
    expect(m.R).toBeLessThanOrEqual(1);
    expect(m.Phi_eff).toBeGreaterThanOrEqual(0);
    expect(['OPTIMO', 'SATURADO', 'JAMMED', 'CRITICO']).toContain(m.regime);
  });
});

describe('Q-State Core', () => {
  test('qTransition is deterministic', () => {
    expect(qTransition('00', '00')).toBe('00');
    expect(qTransition('11', '11')).toBe('10');
  });

  test('qAggregate with equal weights', () => {
    const result = qAggregate(['00', '00', '11', '11']);
    expect(['00', '01', '10', '11']).toContain(result);
  });

  test('QStateMap has all states', () => {
    expect(QStateMap['00'].label).toContain('Silencio');
    expect(QStateMap['11'].label).toContain('Burst');
  });
});
