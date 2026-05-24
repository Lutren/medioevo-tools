/**
 * Tests Brain OS — Todos los subsistemas
 */

import { HandoffPersistenceEngine } from '../src/brain/hippocampus';
import { ActionGateExecutive } from '../src/brain/prefrontal';
import { GhostGateAttention } from '../src/brain/attention';
import { QuaternaryTimingCore } from '../src/brain/cerebellum';
import { TruthGateTestEngine } from '../src/brain/immune';
import { ResourceRegulator } from '../src/brain/homeostasis';
import { CrossModalTransduction } from '../src/brain/corpusCallosum';
import { BodySchemaEngine } from '../src/brain/proprioception';

describe('Hipocampo / Handoff', () => {
  test('crea handoff con residuo comprimido', () => {
    const hippo = new HandoffPersistenceEngine();
    const observer = {
      state: '10' as any, memory: new Float32Array([0.1, 0.2, 0.3, 0.4]),
      calibration: 0.5, noise: 0.1, goal: 'test', gate: 'APPROVE' as any, lastUpdate: 0
    };
    const manifest = hippo.createHandoff('test-1', { a: 1, b: 2 }, observer, 'next');
    expect(manifest.fingerprint).toBe('test-1');
    expect(manifest.residueVector.length).toBeGreaterThan(0);
    expect(hippo.getCompressionRatio()).toBeGreaterThanOrEqual(0);
  });

  test('reconstruye desde handoff', () => {
    const hippo = new HandoffPersistenceEngine();
    const observer = {
      state: '10' as any, memory: new Float32Array([0.1, 0.2, 0.3, 0.4]),
      calibration: 0.5, noise: 0.1, goal: 'test', gate: 'APPROVE' as any, lastUpdate: 0
    };
    hippo.createHandoff('test-2', { a: 5, b: 10 }, observer, 'next');
    const reconstructed = hippo.reconstructState('test-2');
    expect(reconstructed).not.toBeNull();
    expect(reconstructed!.observer.goal).toBe('test');
  });
});

describe('Prefrontal / ActionGate', () => {
  test('registra motores y decide', () => {
    const exec = new ActionGateExecutive();
    exec.registerMotor('audio', 10, 50, 8);
    exec.registerMotor('render', 30, 100, 16);
    const decisions = exec.decide(
      { R: 0.2, Phi_eff: 0.9, J_c: 0.8, regime: 'OPTIMO' },
      { cpu: 40, memory: 200 }
    );
    expect(decisions.length).toBe(2);
    expect(decisions[0].gate).toBe('APPROVE');
  });

  test('comprime en saturación', () => {
    const exec = new ActionGateExecutive();
    exec.registerMotor('render', 30, 100, 16);
    exec.decide(
      { R: 0.6, Phi_eff: 0.3, J_c: 0.8, regime: 'SATURADO' },
      { cpu: 85, memory: 400 }
    );
    const motor = exec.getMotor('render');
    expect(motor!.currentLOD).toBeLessThan(16);
  });
});

describe('Atención / GhostGate', () => {
  test('bloquea señal débil', () => {
    const gate = new GhostGateAttention();
    const result = gate.evaluate(
      { channel: 'visual', data: {}, intensity: 0.05, noise: 0.1, timestamp: 0 },
      { R: 0.2, Phi_eff: 0.9, J_c: 0.8, regime: 'OPTIMO' }
    );
    expect(result.passed).toBe(false);
    expect(result.reason).toBe('below_threshold');
  });

  test('pasa señal fuerte y novedosa', () => {
    const gate = new GhostGateAttention();
    const result = gate.evaluate(
      { channel: 'audio', data: {}, intensity: 0.9, noise: 0.1, timestamp: 0 },
      { R: 0.2, Phi_eff: 0.9, J_c: 0.8, regime: 'OPTIMO' }
    );
    expect(result.passed).toBe(true);
    expect(result.reason).toBe('reduces_residue');
  });
});

describe('Cerebelo / Timing', () => {
  test('tick avanza frame', () => {
    const timing = new QuaternaryTimingCore();
    const tick = timing.tick(1/60);
    expect(tick.globalFrame).toBe(1);
    expect(tick.phase).toBeGreaterThanOrEqual(0);
  });

  test('Q-state del timing', () => {
    const timing = new QuaternaryTimingCore({ bpm: 60, beatsPerBar: 4, subdivisions: 4 });
    timing.tick(0.1); // 0.1s en beat de 1s
    const q = timing.getTimingQ();
    expect(['00', '01', '10', '11']).toContain(q);
  });
});

describe('Inmune / TruthGate', () => {
  test('registra y ejecuta claims', () => {
    const immune = new TruthGateTestEngine();
    immune.registerDefaultClaims();
    const stats = immune.runAllTests(1);
    expect(stats.total).toBeGreaterThan(0);
    expect(stats.passed + stats.failed).toBeGreaterThanOrEqual(0);
  });

  test('bloquea claim falsificado', () => {
    const immune = new TruthGateTestEngine();
    immune.registerClaim(
      'fake',
      'siempre falso',
      () => true,
      () => true // falsificador activo
    );
    immune.runAllTests(1);
    expect(immune.isBlocked('fake')).toBe(true);
  });
});

describe('Homeostasis / ResourceRegulator', () => {
  test('mide CPU crítica', () => {
    const homeo = new ResourceRegulator();
    const alerts = homeo.measure({
      cpuUsed: 98, memoryUsed: 200, temperature: 40, fps: 60
    });
    expect(alerts.some(a => a.type === 'CPU' && a.severity === 'CRITICAL')).toBe(true);
  });

  test('métricas del sistema', () => {
    const homeo = new ResourceRegulator();
    homeo.measure({ cpuUsed: 50, memoryUsed: 256, temperature: 50, fps: 60 });
    const metrics = homeo.computeResourceMetrics();
    expect(metrics.R).toBeGreaterThanOrEqual(0);
    expect(metrics.Phi_eff).toBeGreaterThanOrEqual(0);
  });
});

describe('Cuerpo Calloso / CrossModal', () => {
  test('audio fuerte genera luz', () => {
    const bridge = new CrossModalTransduction();
    const cell = {
      x: 0, y: 0, material: 'STONE',
      osit: { state: '10', memory: new Float32Array(4), calibration: 0.5, noise: 0.1, goal: 'test', gate: 'APPROVE', lastUpdate: 0 },
      physics: { position: {x:0,y:0}, prevPosition: {x:0,y:0}, velocity: {x:0,y:0}, mass: 1, restitution: 0.5, friction: 0.3, solid: true, pressure: 0, temperature: 20, active: true },
      light: { emissive: 0, absorbtion: 0.3, transmission: 0.5, receivedLux: 0, qLight: '00', color: {r:128,g:128,b:128} },
      audio: { eventQueue: [{ type: 'boom', intensity: 0.9, qSource: '11', timestamp: 0 }], materialResonance: 0 }
    };
    const events = bridge.processAll([cell]);
    expect(events.some(e => e.source === 'audio' && e.target === 'light')).toBe(true);
  });
});

describe('Propiocepción / BodySchema', () => {
  test('mueve observador', () => {
    const body = new BodySchemaEngine();
    body.moveObserver({ x: 100, y: 200 });
    expect(body.getSchema().observerPosition.x).toBe(100);
  });

  test('filtra percepción por rango', () => {
    const body = new BodySchemaEngine({ x: 0, y: 0 });
    const cells = [
      { x: 10, y: 10, material: 'STONE', osit: {} as any, physics: {} as any, light: {} as any },
      { x: 1000, y: 1000, material: 'STONE', osit: {} as any, physics: {} as any, light: {} as any }
    ];
    const perceived = body.perceive(cells);
    expect(perceived.length).toBe(1);
  });
});
